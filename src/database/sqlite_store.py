"""src/database/sqlite_store.py
SQLite-backed local metadata store.

This is the persistence backbone for E02 (Ingestion Library):
- Document identity (sha256) + dedupe
- Persistent extraction storage
- Persistent reviews and corrections

Design goals:
- No additional runtime dependencies (uses stdlib sqlite3)
- Explicit, lightweight migrations
- Safe defaults for local single-user use
"""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Optional
from uuid import uuid4


def sha256_bytes(content: bytes) -> str:
    return sha256(content).hexdigest()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class DocumentRecord:
    document_id: str
    sha256: str
    filename: str
    size_bytes: int
    doc_type: str
    text_excerpt: Optional[str]
    client_id: Optional[str]
    project_id: Optional[str]
    batch_id: Optional[str]
    created_at: str


class SQLiteStore:
    def __init__(self, *, db_path: str):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init(self) -> None:
        with self._connect() as conn:
            self._migrate(conn)

    def _migrate(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
              version INTEGER PRIMARY KEY,
              applied_at TEXT NOT NULL
            );
            """
        )
        current = conn.execute("SELECT COALESCE(MAX(version), 0) AS v FROM schema_migrations").fetchone()["v"]

        def apply(version: int, sql: str) -> None:
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO schema_migrations(version, applied_at) VALUES(?, ?)",
                (version, _utc_now_iso()),
            )

        if current < 1:
            apply(
                1,
                """
                CREATE TABLE IF NOT EXISTS documents (
                  document_id TEXT PRIMARY KEY,
                  sha256 TEXT NOT NULL UNIQUE,
                  filename TEXT NOT NULL,
                  size_bytes INTEGER NOT NULL,
                                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS extractions (
                  extraction_id TEXT PRIMARY KEY,
                  document_id TEXT,
                  extraction_json TEXT NOT NULL,
                  created_at TEXT NOT NULL,
                  FOREIGN KEY(document_id) REFERENCES documents(document_id)
                );

                CREATE INDEX IF NOT EXISTS idx_extractions_created_at ON extractions(created_at);
                CREATE INDEX IF NOT EXISTS idx_extractions_document_id ON extractions(document_id);

                CREATE TABLE IF NOT EXISTS reviews (
                  extraction_id TEXT PRIMARY KEY,
                  approved INTEGER NOT NULL,
                  reviewed_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS corrections (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  extraction_id TEXT NOT NULL,
                  field_name TEXT NOT NULL,
                  old_value TEXT,
                  new_value TEXT,
                  created_at TEXT NOT NULL
                );
                """,
            )

        if current < 2:
            apply(
                2,
                """
                ALTER TABLE documents ADD COLUMN doc_type TEXT NOT NULL DEFAULT 'unknown';
                ALTER TABLE documents ADD COLUMN text_excerpt TEXT;
                CREATE INDEX IF NOT EXISTS idx_documents_doc_type ON documents(doc_type);
                """,
            )

        if current < 3:
            apply(
                3,
                """
                ALTER TABLE documents ADD COLUMN client_id TEXT;
                ALTER TABLE documents ADD COLUMN project_id TEXT;
                ALTER TABLE documents ADD COLUMN batch_id TEXT;

                CREATE INDEX IF NOT EXISTS idx_documents_client_id ON documents(client_id);
                CREATE INDEX IF NOT EXISTS idx_documents_project_id ON documents(project_id);
                CREATE INDEX IF NOT EXISTS idx_documents_batch_id ON documents(batch_id);
                """,
            )

    def upsert_document_from_bytes(
        self,
        *,
        filename: str,
        content: bytes,
        doc_type: str = "unknown",
        text_excerpt: Optional[str] = None,
        client_id: Optional[str] = None,
        project_id: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> DocumentRecord:
        digest = sha256_bytes(content)
        size_bytes = len(content)

        with self._connect() as conn:
            existing = conn.execute(
                """
                SELECT document_id, sha256, filename, size_bytes, doc_type, text_excerpt,
                       client_id, project_id, batch_id, created_at
                FROM documents WHERE sha256 = ?
                """,
                (digest,),
            ).fetchone()
            if existing:
                # Opportunistically enrich classification/excerpt if not present.
                if (existing["doc_type"] in (None, "", "unknown") and doc_type) or (
                    (existing["text_excerpt"] in (None, "") and text_excerpt)
                ):
                    conn.execute(
                        """
                        UPDATE documents
                        SET doc_type = COALESCE(NULLIF(doc_type, ''), doc_type),
                            text_excerpt = COALESCE(text_excerpt, ?)
                        WHERE document_id = ?
                        """,
                        (text_excerpt, existing["document_id"]),
                    )

                # Opportunistically enrich scoping identifiers if not present.
                if (
                    (existing["client_id"] in (None, "") and client_id)
                    or (existing["project_id"] in (None, "") and project_id)
                    or (existing["batch_id"] in (None, "") and batch_id)
                ):
                    conn.execute(
                        """
                        UPDATE documents
                        SET client_id = COALESCE(client_id, ?),
                            project_id = COALESCE(project_id, ?),
                            batch_id = COALESCE(batch_id, ?)
                        WHERE document_id = ?
                        """,
                        (client_id, project_id, batch_id, existing["document_id"]),
                    )
                return DocumentRecord(
                    document_id=existing["document_id"],
                    sha256=existing["sha256"],
                    filename=existing["filename"],
                    size_bytes=int(existing["size_bytes"]),
                    doc_type=(existing["doc_type"] or "unknown"),
                    text_excerpt=existing["text_excerpt"],
                    client_id=existing["client_id"],
                    project_id=existing["project_id"],
                    batch_id=existing["batch_id"],
                    created_at=existing["created_at"],
                )

            document_id = str(uuid4())
            created_at = _utc_now_iso()
            conn.execute(
                """
                INSERT INTO documents(
                  document_id, sha256, filename, size_bytes, doc_type, text_excerpt,
                  client_id, project_id, batch_id,
                  created_at
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (document_id, digest, filename, size_bytes, doc_type, text_excerpt, client_id, project_id, batch_id, created_at),
            )
            return DocumentRecord(
                document_id=document_id,
                sha256=digest,
                filename=filename,
                size_bytes=size_bytes,
                doc_type=doc_type,
                text_excerpt=text_excerpt,
                client_id=client_id,
                project_id=project_id,
                batch_id=batch_id,
                created_at=created_at,
            )

    def list_documents(
        self,
        *,
        limit: int = 100,
        doc_type: Optional[str] = None,
        client_id: Optional[str] = None,
        project_id: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        with self._connect() as conn:
            filters: list[str] = []
            params: list[Any] = []

            if doc_type:
                filters.append("doc_type = ?")
                params.append(doc_type)
            if client_id:
                filters.append("client_id = ?")
                params.append(client_id)
            if project_id:
                filters.append("project_id = ?")
                params.append(project_id)
            if batch_id:
                filters.append("batch_id = ?")
                params.append(batch_id)

            where = ("WHERE " + " AND ".join(filters)) if filters else ""
            params.append(limit)

            rows = conn.execute(
                f"""
                SELECT document_id, sha256, filename, size_bytes, doc_type, text_excerpt,
                       client_id, project_id, batch_id, created_at
                FROM documents
                {where}
                ORDER BY created_at DESC
                LIMIT ?
                """,
                tuple(params),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_document(self, *, document_id: str) -> Optional[dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT document_id, sha256, filename, size_bytes, doc_type, text_excerpt,
                       client_id, project_id, batch_id, created_at
                FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            ).fetchone()
        return dict(row) if row else None

    def save_extraction(self, *, extraction_id: str, document_id: Optional[str], payload: dict[str, Any]) -> None:
        created_at = (
            ((payload.get("_source") or {}).get("uploaded_at"))
            or payload.get("created_at")
            or _utc_now_iso()
        )
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO extractions(extraction_id, document_id, extraction_json, created_at)
                VALUES(?, ?, ?, ?)
                ON CONFLICT(extraction_id) DO UPDATE SET
                  document_id=excluded.document_id,
                  extraction_json=excluded.extraction_json,
                  created_at=excluded.created_at;
                """,
                (extraction_id, document_id, json.dumps(payload), created_at),
            )

    def list_extractions(
        self,
        *,
        limit: int = 25,
        client_id: Optional[str] = None,
        project_id: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        with self._connect() as conn:
            filters: list[str] = []
            params: list[Any] = []

            if client_id:
                filters.append("d.client_id = ?")
                params.append(client_id)
            if project_id:
                filters.append("d.project_id = ?")
                params.append(project_id)
            if batch_id:
                filters.append("d.batch_id = ?")
                params.append(batch_id)

            where = ("WHERE " + " AND ".join(filters)) if filters else ""
            params.append(limit)

            rows = conn.execute(
                f"""
                SELECT e.extraction_json
                FROM extractions e
                LEFT JOIN documents d ON d.document_id = e.document_id
                {where}
                ORDER BY e.created_at DESC
                LIMIT ?
                """,
                tuple(params),
            ).fetchall()
        return [json.loads(r["extraction_json"]) for r in rows]

    def get_extraction(self, *, extraction_id: str) -> Optional[dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT extraction_json FROM extractions WHERE extraction_id = ?",
                (extraction_id,),
            ).fetchone()
        if not row:
            return None
        return json.loads(row["extraction_json"])

    def get_latest_extraction(self) -> Optional[dict[str, Any]]:
        items = self.list_extractions(limit=1)
        return items[0] if items else None

    def save_review(self, *, extraction_id: str, approved: bool, reviewed_at: Optional[str] = None) -> dict[str, Any]:
        reviewed_at = reviewed_at or _utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO reviews(extraction_id, approved, reviewed_at)
                VALUES(?, ?, ?)
                ON CONFLICT(extraction_id) DO UPDATE SET
                  approved=excluded.approved,
                  reviewed_at=excluded.reviewed_at;
                """,
                (extraction_id, 1 if approved else 0, reviewed_at),
            )
        return {"extraction_id": extraction_id, "approved": approved, "reviewed_at": reviewed_at}

    def list_reviews(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT extraction_id, approved, reviewed_at FROM reviews ORDER BY reviewed_at DESC"
            ).fetchall()
        return [
            {
                "extraction_id": r["extraction_id"],
                "approved": bool(r["approved"]),
                "reviewed_at": r["reviewed_at"],
            }
            for r in rows
        ]

    def add_correction(
        self,
        *,
        extraction_id: str,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
        created_at: Optional[str] = None,
    ) -> dict[str, Any]:
        created_at = created_at or _utc_now_iso()
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO corrections(extraction_id, field_name, old_value, new_value, created_at)
                VALUES(?, ?, ?, ?, ?)
                """,
                (extraction_id, field_name, old_value, new_value, created_at),
            )
            correction_id = int(cur.lastrowid)
        return {
            "id": correction_id,
            "extraction_id": extraction_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": created_at,
        }

    def list_corrections(self, *, extraction_id: Optional[str] = None) -> list[dict[str, Any]]:
        with self._connect() as conn:
            if extraction_id:
                rows = conn.execute(
                    """
                    SELECT id, extraction_id, field_name, old_value, new_value, created_at
                    FROM corrections
                    WHERE extraction_id = ?
                    ORDER BY created_at DESC
                    """,
                    (extraction_id,),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT id, extraction_id, field_name, old_value, new_value, created_at
                    FROM corrections
                    ORDER BY created_at DESC
                    """
                ).fetchall()

        return [
            {
                "id": int(r["id"]),
                "extraction_id": r["extraction_id"],
                "field_name": r["field_name"],
                "old_value": r["old_value"],
                "new_value": r["new_value"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]
