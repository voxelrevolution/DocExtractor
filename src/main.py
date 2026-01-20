"""
src/main.py
FastAPI application entry point.
"""

from __future__ import annotations

import os
import sys
import logging
import mimetypes
from hashlib import sha256
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
FILE_STORE_ROOT = os.getenv(
    "DOCEXTRACTOR_FILE_STORE",
    os.path.join(PROJECT_ROOT, "data", "file_store"),
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from src.evaluation.invoice_runner import evaluate_invoices
from src.evaluation.report import build_report
from src.evaluation.csv_report import scorecards_to_csv
from src.schemas.annotations import CorrectionInput, CorrectionRecord
from src.schemas.chat import ChatRequest, ChatResponse, ChatCitation
from src.schemas.clients import ClientCreateRequest, ClientRecord
from src.schemas.evaluation import EvaluationRequest, EvaluationResponse
from src.schemas.export import ExportRequest, ExportResponse

from src.llm import OllamaClient
from src.llm.ollama_http import OllamaError, extract_reply_from_json_content, ollama_chat

logger = logging.getLogger(__name__)

_store = None
_documents: dict[str, dict] = {}


def _safe_filename(filename: str, document_id: str) -> str:
    base = os.path.basename(filename or "")
    return base or f"{document_id}.bin"


def _document_file_path(*, document_id: str, filename: str) -> str:
    safe_name = _safe_filename(filename, document_id)
    return os.path.join(FILE_STORE_ROOT, document_id, safe_name)


def _persist_document_file(*, document_id: str, filename: str, content: bytes) -> str:
    file_path = _document_file_path(document_id=document_id, filename=filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "wb") as handle:
            handle.write(content)
    return file_path


def _resolve_document_record(document_id: str) -> Optional[dict]:
    if _store is not None:
        return _store.get_document(document_id=document_id)
    return _documents.get(document_id)


def _get_client_resolver():
    from src.clients.resolution import ClientResolver

    return ClientResolver.default()


def _get_client_registry():
    from src.clients.registry import ClientRegistry

    return ClientRegistry.default()


def _db_enabled() -> bool:
    return os.getenv("DOCEXTRACTOR_DB_ENABLED", "0").strip().lower() in {"1", "true", "yes"}


def _get_db_path() -> str:
    return os.getenv(
        "DOCEXTRACTOR_DB_PATH",
        os.path.join(PROJECT_ROOT, "data", "db", "doc_extractor.sqlite3"),
    )


def _init_store():
    global _store
    if not _db_enabled():
        _store = None
        return
    try:
        from src.database.sqlite_store import SQLiteStore

        _store = SQLiteStore(db_path=_get_db_path())
        _store.init()
        logger.info("SQLite store enabled: %s", _get_db_path())
    except Exception as exc:
        logger.error("Failed to initialize SQLite store; continuing in-memory. error=%s", exc)
        _store = None

app = FastAPI(
    title="Local Document Extraction Copilot",
    description="Privacy-first document extraction and Q&A interface",
    version="0.1.0",
)


@app.on_event("startup")
def _startup_init() -> None:
    _init_store()
    if os.getenv("DOCEXTRACTOR_OLLAMA_WARMUP", "0").strip().lower() in {"1", "true", "yes"}:
        try:
            model = os.getenv("DOCEXTRACTOR_OLLAMA_MODEL", "llama3.1:8b")
            host = os.getenv("DOCEXTRACTOR_OLLAMA_HOST", "http://localhost:11434")
            client = OllamaClient(host=host, model=model)
            if client.load_model():
                client.infer("Return JSON: {\"reply\": \"ok\"}.")
                logger.info("Ollama warmup complete model=%s", model)
            else:
                logger.warning("Ollama warmup skipped: model not available")
        except Exception as exc:
            logger.warning("Ollama warmup failed: %s", exc)

_corrections: List[CorrectionRecord] = []
_correction_id = 1
_extractions: dict[str, dict] = {}
_reviews: dict[str, dict] = {}


def _get_latest_extraction(
    *,
    client_id: Optional[str] = None,
    project_id: Optional[str] = None,
    batch_id: Optional[str] = None,
) -> Optional[dict]:
    if _store is not None:
        items = _store.list_extractions(
            limit=1,
            client_id=client_id,
            project_id=project_id,
            batch_id=batch_id,
        )
        return items[0] if items else None
    if not _extractions:
        return None
    items = list(_extractions.values())
    if client_id or project_id or batch_id:
        def _match_scope(extraction: dict) -> bool:
            src = (extraction.get("_source") or {}) if isinstance(extraction, dict) else {}
            if client_id and (src.get("client_id") or None) != client_id:
                return False
            if project_id and (src.get("project_id") or None) != project_id:
                return False
            if batch_id and (src.get("batch_id") or None) != batch_id:
                return False
            return True

        items = [item for item in items if _match_scope(item)]
    return items[-1] if items else None


def _citations_from_extraction_field(extraction: dict, field_name: str) -> list[ChatCitation]:
    field = extraction.get(field_name, {}) or {}
    evidence = field.get("evidence", []) or []

    source_filename = (
        (extraction.get("_source", {}) or {}).get("filename")
        or extraction.get("_source_filename")
        or None
    )

    citations: list[ChatCitation] = []
    for item in evidence:
        citations.append(
            ChatCitation(
                source=str(source_filename or item.get("source") or "unknown"),
                page=item.get("page"),
                line=item.get("line"),
                snippet=item.get("text"),
            )
        )
    return citations


def _build_document_reply(extraction: dict) -> ChatResponse:
    vendor = (extraction.get("vendor", {}) or {}).get("value") or "(unknown vendor)"
    total = (extraction.get("total", {}) or {}).get("value") or "(unknown total)"
    citations = []
    citations.extend(_citations_from_extraction_field(extraction, "total"))
    citations.extend(_citations_from_extraction_field(extraction, "vendor"))
    reply = f"The invoice total is {total}. The vendor listed is {vendor}."
    return ChatResponse(reply=reply, citations=citations)


def _build_corpus_reply(
    *,
    client_id: Optional[str] = None,
    project_id: Optional[str] = None,
    batch_id: Optional[str] = None,
) -> ChatResponse:
    if _store is not None:
        extractions = {
            e.get("extraction_id"): e
            for e in _store.list_extractions(
                limit=500,
                client_id=client_id,
                project_id=project_id,
                batch_id=batch_id,
            )
        }
        documents = _store.list_documents(
            limit=500,
            client_id=client_id,
            project_id=project_id,
            batch_id=batch_id,
        )
    else:
        def _match_doc_scope(d: dict) -> bool:
            if client_id and (d.get("client_id") or None) != client_id:
                return False
            if project_id and (d.get("project_id") or None) != project_id:
                return False
            if batch_id and (d.get("batch_id") or None) != batch_id:
                return False
            return True

        def _match_extraction_scope(extraction: dict) -> bool:
            src = (extraction.get("_source") or {}) if isinstance(extraction, dict) else {}
            if client_id and (src.get("client_id") or None) != client_id:
                return False
            if project_id and (src.get("project_id") or None) != project_id:
                return False
            if batch_id and (src.get("batch_id") or None) != batch_id:
                return False
            return True

        extractions = {k: v for k, v in _extractions.items() if _match_extraction_scope(v)}
        documents = [d for d in _documents.values() if _match_doc_scope(d)]

    invoice_count = len(extractions)
    other_docs = [d for d in documents if (d.get("doc_type") or "unknown") != "invoice"]
    other_count = len(other_docs)

    if invoice_count == 0 and other_count == 0:
        return ChatResponse(reply="No documents have been ingested yet.")

    vendor_counts: dict[str, int] = {}
    totals: list[float] = []
    citations: list[ChatCitation] = []

    for extraction in extractions.values():
        vendor = (extraction.get("vendor", {}) or {}).get("value") or "(unknown vendor)"
        vendor_counts[vendor] = vendor_counts.get(vendor, 0) + 1

        total_raw = (extraction.get("total", {}) or {}).get("value") or ""
        cleaned = (
            str(total_raw)
            .replace("$", "")
            .replace(",", "")
            .strip()
        )
        try:
            totals.append(float(cleaned))
        except ValueError:
            pass

        if len(citations) < 6:
            citations.extend(_citations_from_extraction_field(extraction, "total"))
            citations.extend(_citations_from_extraction_field(extraction, "vendor"))

    # Add lightweight citations for non-invoice docs.
    for doc in other_docs[:3]:
        if len(citations) >= 6:
            break
        citations.append(
            ChatCitation(
                source=str(doc.get("filename") or "unknown"),
                page=None,
                line=None,
                snippet=(doc.get("text_excerpt") or "")[:200] or None,
            )
        )

    if invoice_count == 0:
        reply = f"Across the corpus, there are {other_count} non-invoice documents." \
            if other_count != 1 else "Across the corpus, there is 1 non-invoice document."
        return ChatResponse(reply=reply, citations=citations[:6])

    top_vendor = max(vendor_counts.items(), key=lambda item: item[1])[0]
    top_vendor_count = vendor_counts[top_vendor]

    if totals:
        reply = (
            f"Across the corpus, {top_vendor} appears in {top_vendor_count} documents "
            f"with totals ranging from ${min(totals):,.2f} to ${max(totals):,.2f}."
        )
    else:
        reply = f"Across the corpus, {top_vendor} appears in {top_vendor_count} documents."

    if other_count:
        reply += f" There are also {other_count} non-invoice documents in the library."

    return ChatResponse(reply=reply, citations=citations[:6])


def _ollama_enabled() -> bool:
    return os.getenv("DOCEXTRACTOR_OLLAMA_ENABLED", "0").strip().lower() in {"1", "true", "yes"}


def _build_ollama_messages(*, user_message: str, system_context: str, history: list[dict]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a local-only document extraction copilot. "
                "Answer using ONLY the provided context. "
                "If the answer is not in context, say you don't know. "
                "Return JSON: {\"reply\": string}."
            ),
        },
        {"role": "system", "content": system_context},
    ]

    for item in history:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})
    return messages


def _try_ollama_reply(*, payload: ChatRequest, context: str) -> Optional[str]:
    if not _ollama_enabled():
        return None

    host = os.getenv("DOCEXTRACTOR_OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("DOCEXTRACTOR_OLLAMA_MODEL", "llama3.1:8b")
    try:
        content = ollama_chat(
            host=host,
            model=model,
            messages=_build_ollama_messages(
                user_message=payload.message,
                system_context=context,
                history=[m.model_dump() for m in payload.history],
            ),
            timeout_s=float(os.getenv("DOCEXTRACTOR_OLLAMA_TIMEOUT_S", "6")),
        )
    except (OllamaError, ValueError):
        return None

    return extract_reply_from_json_content(content) or content.strip() or None


def _reset_corrections_state() -> None:
    global _corrections, _correction_id
    _corrections = []
    _correction_id = 1


def _reset_extractions_state() -> None:
    global _extractions
    _extractions = {}


def _reset_reviews_state() -> None:
    global _reviews
    _reviews = {}

# CORS middleware (allow local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/api/clients")
def list_clients() -> list[dict]:
    registry = _get_client_registry()
    return [c.model_dump() for c in registry.load()]


@app.post("/api/clients")
def upsert_client(payload: ClientCreateRequest) -> dict:
    registry = _get_client_registry()
    record = ClientRecord(client_id=payload.client_id, display_name=payload.display_name, aliases=payload.aliases)
    registry.upsert(record)
    return record.model_dump()


@app.post("/api/invoices/extract")
async def extract_invoice(
    file: UploadFile = File(...),
    client_id: Optional[str] = None,
    project_id: Optional[str] = None,
    batch_id: Optional[str] = None,
):
    """Extract invoice fields from a PDF or text file."""
    from src.extraction.invoice import extract_text_from_pdf_bytes
    from src.extraction.invoice_pipeline import extract_invoice_from_text

    content = await file.read()
    filename = (file.filename or "").lower()

    sha256_hex = sha256(content).hexdigest()

    if filename.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
    elif filename.endswith(".pdf"):
        try:
            text, line_page_map, line_source_map = extract_text_from_pdf_bytes(content)
        except RuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use .pdf or .txt")

    resolution = None
    if not client_id:
        resolution = _get_client_resolver().resolve(filename=file.filename or "", text=text)
        if resolution.policy == "auto" and resolution.client_id:
            client_id = resolution.client_id
        else:
            # Option A: require explicit selection when clients are configured.
            # If no clients exist yet, allow ingest to proceed unscoped.
            if _get_client_registry().load():
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": "client_id_required",
                        "message": "Client selection required. Provide client_id.",
                        "client_resolution": (resolution.model_dump() if resolution is not None else None),
                    },
                )

    if filename.endswith(".pdf"):
        extraction = extract_invoice_from_text(text, line_page_map, line_source_map, prefer_llm=True)
    else:
        extraction = extract_invoice_from_text(text, prefer_llm=True)
    extraction.extraction_id = str(uuid4())
    payload = extraction.model_dump()
    payload["_source"] = {
        "filename": file.filename,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "sha256": sha256_hex,
        "client_id": client_id,
        "project_id": project_id,
        "batch_id": batch_id,
    }
    if resolution is not None:
        payload["_client_resolution"] = resolution.model_dump()
    _extractions[extraction.extraction_id] = payload

    if _store is not None:
        doc = _store.upsert_document_from_bytes(
            filename=file.filename or "",
            content=content,
            doc_type="invoice",
            text_excerpt=(text or "")[:800],
            client_id=client_id,
            project_id=project_id,
            batch_id=batch_id,
        )
        _persist_document_file(
            document_id=doc.document_id,
            filename=file.filename or "",
            content=content,
        )
        _store.save_extraction(extraction_id=extraction.extraction_id, document_id=doc.document_id, payload=payload)
    else:
        # Minimal in-memory doc record for corpus context.
        _documents[sha256_hex] = {
            "document_id": sha256_hex,
            "sha256": sha256_hex,
            "filename": file.filename,
            "size_bytes": len(content),
            "doc_type": "invoice",
            "text_excerpt": (text or "")[:800],
            "client_id": client_id,
            "project_id": project_id,
            "batch_id": batch_id,
            "created_at": payload.get("_source", {}).get("uploaded_at"),
        }
        _persist_document_file(
            document_id=sha256_hex,
            filename=file.filename or "",
            content=content,
        )
    return payload


@app.post("/api/documents/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    client_id: Optional[str] = None,
    project_id: Optional[str] = None,
    batch_id: Optional[str] = None,
):
    """Ingest a document into the local library (classification v1).

    For invoices, this also runs invoice extraction and stores an extraction.
    """

    from src.extraction.invoice import extract_text_from_pdf_bytes
    from src.extraction.invoice_pipeline import extract_invoice_from_text
    from src.ingestion.classification import classify_document

    content = await file.read()
    filename = file.filename or ""
    filename_lower = filename.lower()

    if filename_lower.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
        line_page_map = None
        line_source_map = None
    elif filename_lower.endswith(".pdf"):
        try:
            text, line_page_map, line_source_map = extract_text_from_pdf_bytes(content)
        except RuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use .pdf or .txt")

    sha256_hex = sha256(content).hexdigest()
    doc_type = classify_document(filename=filename, text=text)
    excerpt = (text or "")[:1200]

    resolution = None
    if not client_id:
        resolution = _get_client_resolver().resolve(filename=filename, text=text)
        if resolution.policy == "auto" and resolution.client_id:
            client_id = resolution.client_id
        else:
            # Option A: require explicit selection when clients are configured.
            if _get_client_registry().load():
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": "client_id_required",
                        "message": "Client selection required. Provide client_id.",
                        "client_resolution": (resolution.model_dump() if resolution is not None else None),
                    },
                )

    # Persist/record the document.
    if _store is not None:
        doc = _store.upsert_document_from_bytes(
            filename=filename,
            content=content,
            doc_type=doc_type,
            text_excerpt=excerpt,
            client_id=client_id,
            project_id=project_id,
            batch_id=batch_id,
        )
        document_id = doc.document_id
    else:
        document_id = sha256_hex
        _documents[document_id] = {
            "document_id": document_id,
            "sha256": sha256_hex,
            "filename": filename,
            "size_bytes": len(content),
            "doc_type": doc_type,
            "text_excerpt": excerpt,
            "client_id": client_id,
            "project_id": project_id,
            "batch_id": batch_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    _persist_document_file(document_id=document_id, filename=filename, content=content)

    # If invoice, run extraction and save it.
    if doc_type == "invoice":
        if filename_lower.endswith(".pdf"):
            extraction = extract_invoice_from_text(text, line_page_map, line_source_map, prefer_llm=True)
        else:
            extraction = extract_invoice_from_text(text, prefer_llm=True)

        extraction.extraction_id = str(uuid4())
        payload = extraction.model_dump()
        payload["_source"] = {
            "filename": filename,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "sha256": sha256_hex,
            "document_id": document_id,
            "doc_type": doc_type,
            "client_id": client_id,
            "project_id": project_id,
            "batch_id": batch_id,
        }
        if resolution is not None:
            payload["_client_resolution"] = resolution.model_dump()
        _extractions[extraction.extraction_id] = payload
        if _store is not None:
            _store.save_extraction(extraction_id=extraction.extraction_id, document_id=document_id, payload=payload)
        out = {"document_id": document_id, "doc_type": doc_type, "extraction": payload}
        if resolution is not None:
            out["client_resolution"] = resolution.model_dump()
        return out

    out = {
        "document_id": document_id,
        "doc_type": doc_type,
        "sha256": sha256_hex,
        "filename": filename,
        "text_excerpt": excerpt,
    }
    if resolution is not None:
        out["client_resolution"] = resolution.model_dump()
    return out


@app.get("/api/documents")
def list_documents(
    limit: int = 50,
    doc_type: Optional[str] = None,
    client_id: Optional[str] = None,
    project_id: Optional[str] = None,
    batch_id: Optional[str] = None,
):
    """List ingested documents (metadata only)."""

    if _store is not None:
        return _store.list_documents(
            limit=limit,
            doc_type=doc_type,
            client_id=client_id,
            project_id=project_id,
            batch_id=batch_id,
        )

    items = list(_documents.values())
    if doc_type:
        items = [d for d in items if (d.get("doc_type") or "unknown") == doc_type]
    if client_id:
        items = [d for d in items if (d.get("client_id") or None) == client_id]
    if project_id:
        items = [d for d in items if (d.get("project_id") or None) == project_id]
    if batch_id:
        items = [d for d in items if (d.get("batch_id") or None) == batch_id]
    return items[:limit]


@app.get("/api/documents/{document_id}")
def get_document(document_id: str):
    """Get a single document record by id."""

    if _store is not None:
        doc = _store.get_document(document_id=document_id)
    else:
        doc = _documents.get(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@app.get("/api/documents/{document_id}/file")
def get_document_file(document_id: str, client_id: Optional[str] = None):
    """Fetch the original document bytes from the local file store."""

    doc = _resolve_document_record(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc_client_id = (doc.get("client_id") or None) if isinstance(doc, dict) else None
    if doc_client_id and client_id != doc_client_id:
        raise HTTPException(status_code=403, detail="client_id_mismatch")

    filename = (doc.get("filename") or "") if isinstance(doc, dict) else ""
    file_path = _document_file_path(document_id=document_id, filename=filename)
    if not os.path.exists(file_path):
        fallback_dir = os.path.join(FILE_STORE_ROOT, document_id)
        if os.path.isdir(fallback_dir):
            entries = [
                os.path.join(fallback_dir, entry)
                for entry in os.listdir(fallback_dir)
                if os.path.isfile(os.path.join(fallback_dir, entry))
            ]
            if entries:
                file_path = entries[0]
                filename = filename or os.path.basename(file_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document file not found")

    media_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    return FileResponse(path=file_path, media_type=media_type, filename=filename)


@app.post("/api/invoices/corrections")
def record_corrections(corrections: List[CorrectionInput]):
    global _correction_id

    records: List[CorrectionRecord] = []
    for correction in corrections:
        record = CorrectionRecord(
            id=_correction_id,
            created_at=datetime.now(timezone.utc),
            **correction.model_dump(),
        )
        _corrections.append(record)
        records.append(record)
        _correction_id += 1
    return [record.model_dump() for record in records]


@app.get("/api/invoices/corrections")
def list_corrections(extraction_id: Optional[str] = None):
    if extraction_id:
        filtered = [c for c in _corrections if c.extraction_id == extraction_id]
        return [record.model_dump() for record in filtered]
    return [record.model_dump() for record in _corrections]


@app.get("/api/invoices/extractions")
def list_extractions(
    limit: int = 25,
    client_id: Optional[str] = None,
    project_id: Optional[str] = None,
    batch_id: Optional[str] = None,
):
    if _store is not None:
        return _store.list_extractions(
            limit=limit,
            client_id=client_id,
            project_id=project_id,
            batch_id=batch_id,
        )

    def _match_scope(extraction: dict) -> bool:
        src = (extraction.get("_source") or {}) if isinstance(extraction, dict) else {}
        if client_id and (src.get("client_id") or None) != client_id:
            return False
        if project_id and (src.get("project_id") or None) != project_id:
            return False
        if batch_id and (src.get("batch_id") or None) != batch_id:
            return False
        return True

    items = [e for e in _extractions.values() if _match_scope(e)]
    return items[:limit]


@app.get("/api/invoices/extractions/{extraction_id}")
def get_extraction(extraction_id: str):
    extraction = _store.get_extraction(extraction_id=extraction_id) if _store is not None else _extractions.get(extraction_id)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return extraction


@app.post("/api/invoices/extractions/{extraction_id}/review")
def mark_extraction_reviewed(extraction_id: str, approved: bool = True):
    exists = (
        _store.get_extraction(extraction_id=extraction_id) is not None
        if _store is not None
        else extraction_id in _extractions
    )
    if not exists:
        raise HTTPException(status_code=404, detail="Extraction not found")
    review = {
        "extraction_id": extraction_id,
        "approved": approved,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }
    _reviews[extraction_id] = review
    if _store is not None:
        return _store.save_review(extraction_id=extraction_id, approved=approved, reviewed_at=review["reviewed_at"])
    return review


@app.get("/api/invoices/reviews")
def list_reviews():
    if _store is not None:
        return _store.list_reviews()
    return list(_reviews.values())


@app.post("/api/invoices/export", response_model=ExportResponse)
def export_extractions(payload: ExportRequest):
    if _store is not None:
        source_items = _store.list_extractions(limit=5000, client_id=payload.client_id)
    else:
        source_items = list(_extractions.values())
    rows = []
    for item in source_items:
        if payload.client_id:
            src = item.get("_source") if isinstance(item, dict) else None
            if (src or {}).get("client_id") != payload.client_id:
                continue
        if payload.extraction_ids and item.get("extraction_id") not in payload.extraction_ids:
            continue
        row = {
            "extraction_id": item.get("extraction_id", "") or "",
            "vendor": item.get("vendor", {}).get("value", "") or "",
            "invoice_number": item.get("invoice_number", {}).get("value", "") or "",
            "invoice_date": item.get("invoice_date", {}).get("value", "") or "",
            "subtotal": item.get("subtotal", {}).get("value", "") or "",
            "tax": item.get("tax", {}).get("value", "") or "",
            "total": item.get("total", {}).get("value", "") or "",
        }
        rows.append(row)
        if payload.include_line_items:
            for line in item.get("line_items", []):
                rows.append(
                    {
                        "extraction_id": item.get("extraction_id", ""),
                        "vendor": item.get("vendor", {}).get("value", ""),
                        "invoice_number": item.get("invoice_number", {}).get("value", ""),
                        "invoice_date": item.get("invoice_date", {}).get("value", ""),
                        "subtotal": "",
                        "tax": "",
                        "total": "",
                        "line_description": line.get("description"),
                        "line_quantity": line.get("quantity"),
                        "line_unit_price": line.get("unit_price"),
                        "line_amount": line.get("amount"),
                    }
                )
    return ExportResponse(rows=rows)


@app.post("/api/invoices/evaluate", response_model=EvaluationResponse)
def evaluate_invoice_extractions(payload: EvaluationRequest):
    summary = evaluate_invoices(payload.expected_docs, payload.predicted_docs, payload.id_key)
    return EvaluationResponse(
        documents_scored=summary.documents_scored,
        mean_field_accuracy=summary.mean_field_accuracy,
        mean_line_item_accuracy=summary.mean_line_item_accuracy,
    )


@app.post("/api/invoices/evaluate/report")
def evaluate_invoice_report(payload: EvaluationRequest):
    summary = evaluate_invoices(payload.expected_docs, payload.predicted_docs, payload.id_key)
    return build_report(summary.scorecards)


@app.post("/api/invoices/evaluate/report/csv")
def evaluate_invoice_report_csv(payload: EvaluationRequest):
    summary = evaluate_invoices(payload.expected_docs, payload.predicted_docs, payload.id_key)
    return scorecards_to_csv(summary.scorecards)


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    """Local-only Copilot chat endpoint.

    Current implementation answers based on locally stored invoice extractions.
    """
    if payload.scope == "corpus":
        base = _build_corpus_reply(
            client_id=payload.client_id,
            project_id=payload.project_id,
            batch_id=payload.batch_id,
        )
        llm_reply = _try_ollama_reply(
            payload=payload,
            context=f"Corpus summary:\n{base.reply}\n\nUse citations indirectly; do not fabricate facts.",
        )
        if llm_reply:
            return ChatResponse(reply=llm_reply, citations=base.citations)
        return base

    extraction: Optional[dict]
    if payload.extraction_id:
        extraction = _store.get_extraction(extraction_id=payload.extraction_id) if _store is not None else _extractions.get(payload.extraction_id)
        if not extraction:
            raise HTTPException(status_code=404, detail="Extraction not found")
    else:
        extraction = _get_latest_extraction(
            client_id=payload.client_id,
            project_id=payload.project_id,
            batch_id=payload.batch_id,
        )

    if not extraction:
        return ChatResponse(reply="No documents have been ingested yet.")

    if payload.client_id or payload.project_id or payload.batch_id:
        src = (extraction.get("_source") or {}) if isinstance(extraction, dict) else {}
        if payload.client_id and (src.get("client_id") or None) != payload.client_id:
            raise HTTPException(status_code=403, detail="client_id_mismatch")
        if payload.project_id and (src.get("project_id") or None) != payload.project_id:
            raise HTTPException(status_code=403, detail="project_id_mismatch")
        if payload.batch_id and (src.get("batch_id") or None) != payload.batch_id:
            raise HTTPException(status_code=403, detail="batch_id_mismatch")

    base = _build_document_reply(extraction)
    doc_context = {
        "source": (extraction.get("_source", {}) or {}).get("filename"),
        "vendor": (extraction.get("vendor", {}) or {}).get("value"),
        "invoice_number": (extraction.get("invoice_number", {}) or {}).get("value"),
        "invoice_date": (extraction.get("invoice_date", {}) or {}).get("value"),
        "subtotal": (extraction.get("subtotal", {}) or {}).get("value"),
        "tax": (extraction.get("tax", {}) or {}).get("value"),
        "total": (extraction.get("total", {}) or {}).get("value"),
    }
    llm_reply = _try_ollama_reply(
        payload=payload,
        context=(
            "Document context (extracted fields):\n"
            f"{doc_context}\n\n"
            "Answer the user's question using these fields."
        ),
    )
    if llm_reply:
        return ChatResponse(reply=llm_reply, citations=base.citations)
    return base


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Local Document Extraction Copilot API",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
