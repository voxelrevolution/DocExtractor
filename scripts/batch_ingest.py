#!/usr/bin/env python3
"""scripts/batch_ingest.py
Resumable batch ingestion for local DocExtractor.

Uploads a folder of PDFs/TXTs to the running API and records progress to a JSON
file so reruns are idempotent.

- Local-only: refuses non-local API base URLs.
- Dedupe: computes sha256 per file and skips already-completed hashes.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import urlparse

import httpx


_LOCAL_HOSTNAMES = {"localhost", "127.0.0.1", "::1"}


def _validate_local_api_base(api_base: str) -> None:
    parsed = urlparse(api_base)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported API scheme: {parsed.scheme}")
    if parsed.hostname not in _LOCAL_HOSTNAMES:
        raise ValueError(f"Refusing non-local API host: {parsed.hostname}")


def sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class Progress:
    completed: dict[str, dict[str, Any]]
    failed: dict[str, dict[str, Any]]

    @classmethod
    def load(cls, progress_path: Path) -> "Progress":
        if not progress_path.exists():
            return cls(completed={}, failed={})
        data = json.loads(progress_path.read_text(encoding="utf-8"))
        return cls(
            completed=dict(data.get("completed") or {}),
            failed=dict(data.get("failed") or {}),
        )

    def save(self, progress_path: Path) -> None:
        progress_path.parent.mkdir(parents=True, exist_ok=True)
        progress_path.write_text(
            json.dumps(
                {
                    "completed": self.completed,
                    "failed": self.failed,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )


def iter_files(root: Path, extensions: set[str]) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in extensions:
            yield path


def ingest_paths(
    *,
    api_base: str,
    paths: list[Path],
    progress: Progress,
    progress_path: Path,
    timeout_s: float,
    endpoint: str = "/api/documents/ingest",
    client: Optional[httpx.Client] = None,
) -> dict[str, int]:
    _validate_local_api_base(api_base)
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    own_client = client is None
    http = client or httpx.Client(timeout=timeout_s)

    uploaded = 0
    skipped = 0
    failed = 0

    selected_client_id: Optional[str] = None

    def _fetch_clients() -> list[dict[str, Any]]:
        url = api_base.rstrip("/") + "/api/clients"
        resp = http.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else []

    def _prompt_for_client_id(clients: list[dict[str, Any]]) -> str:
        if not clients:
            raise RuntimeError("Client selection required but no clients are configured on the server")

        print("\nClient selection required to continue ingest.")
        for idx, item in enumerate(clients, start=1):
            cid = str(item.get("client_id") or "").strip()
            name = str(item.get("display_name") or cid).strip()
            print(f"  [{idx}] {name} ({cid})")

        while True:
            raw = input("Select client by number: ").strip()
            try:
                choice = int(raw)
            except ValueError:
                continue
            if 1 <= choice <= len(clients):
                cid = str(clients[choice - 1].get("client_id") or "").strip()
                if cid:
                    return cid

    try:
        for path in paths:
            digest = sha256_file(path)
            if digest in progress.completed:
                skipped += 1
                continue

            try:
                with path.open("rb") as f:
                    files = {"file": (path.name, f, "application/octet-stream")}
                    url = api_base.rstrip("/") + endpoint
                    if selected_client_id:
                        sep = "&" if "?" in url else "?"
                        url = f"{url}{sep}client_id={selected_client_id}"
                    resp = http.post(url, files=files)

                if resp.status_code == 409:
                    try:
                        detail = (resp.json() or {}).get("detail") or {}
                    except ValueError:
                        detail = {}

                    if detail.get("error") == "client_id_required":
                        if selected_client_id is None:
                            clients = _fetch_clients()
                            selected_client_id = _prompt_for_client_id(clients)

                        # Retry once with selected client_id
                        with path.open("rb") as f:
                            files = {"file": (path.name, f, "application/octet-stream")}
                            url = api_base.rstrip("/") + endpoint
                            sep = "&" if "?" in url else "?"
                            url = f"{url}{sep}client_id={selected_client_id}"
                            resp = http.post(url, files=files)

                resp.raise_for_status()
                payload = resp.json()
                progress.completed[digest] = {
                    "path": str(path),
                    "filename": path.name,
                    "doc_type": payload.get("doc_type") or (payload.get("extraction") or {}).get("_source", {}).get("doc_type"),
                    "document_id": payload.get("document_id") or (payload.get("extraction") or {}).get("_source", {}).get("document_id"),
                    "extraction_id": payload.get("extraction_id") or (payload.get("extraction") or {}).get("extraction_id"),
                }
                if digest in progress.failed:
                    progress.failed.pop(digest, None)
                uploaded += 1
            except Exception as exc:
                progress.failed[digest] = {
                    "path": str(path),
                    "filename": path.name,
                    "error": str(exc),
                }
                failed += 1

            progress.save(progress_path)
    finally:
        if own_client:
            http.close()

    return {"uploaded": uploaded, "skipped": skipped, "failed": failed}


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Resumable batch ingest for DocExtractor")
    parser.add_argument("root", type=str, help="Folder containing PDFs/TXTs")
    parser.add_argument(
        "--api-base",
        default=os.getenv("DOCEXTRACTOR_API_BASE", "http://127.0.0.1:8000"),
        help="API base URL (local-only). Default: http://127.0.0.1:8000",
    )
    parser.add_argument(
        "--endpoint",
        default=os.getenv("DOCEXTRACTOR_INGEST_ENDPOINT", "/api/documents/ingest"),
        help="Ingest endpoint path (default: /api/documents/ingest). Use /api/invoices/extract for invoice-only.",
    )
    parser.add_argument(
        "--progress",
        default=os.getenv("DOCEXTRACTOR_INGEST_PROGRESS", ""),
        help="Progress JSON path (default: <root>/.docextractor_ingest_progress.json)",
    )
    parser.add_argument(
        "--extensions",
        default=".pdf,.txt",
        help="Comma-separated extensions to ingest (default: .pdf,.txt)",
    )
    parser.add_argument(
        "--timeout-s",
        type=float,
        default=float(os.getenv("DOCEXTRACTOR_INGEST_TIMEOUT_S", "60")),
        help="HTTP timeout seconds (default: 60)",
    )

    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    extensions = {e.strip().lower() for e in args.extensions.split(",") if e.strip()}
    progress_path = (
        Path(args.progress).expanduser().resolve()
        if args.progress.strip()
        else root / ".docextractor_ingest_progress.json"
    )

    progress = Progress.load(progress_path)
    paths = list(iter_files(root, extensions))

    stats = ingest_paths(
        api_base=args.api_base,
        paths=paths,
        progress=progress,
        progress_path=progress_path,
        timeout_s=args.timeout_s,
        endpoint=args.endpoint,
    )

    print(json.dumps({"root": str(root), "files": len(paths), **stats}, indent=2))
    return 0 if stats["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
