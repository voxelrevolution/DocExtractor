import json

from src.database.sqlite_store import SQLiteStore, sha256_bytes


def test_sqlite_store_persists_extraction(tmp_path):
    db_path = tmp_path / "db.sqlite3"
    store = SQLiteStore(db_path=str(db_path))
    store.init()

    content = b"hello world"
    doc = store.upsert_document_from_bytes(filename="a.txt", content=content)
    assert doc.sha256 == sha256_bytes(content)

    payload = {"extraction_id": "ex-1", "vendor": {"value": "ACME"}, "_source": {"uploaded_at": "2026-01-01T00:00:00Z"}}
    store.save_extraction(extraction_id="ex-1", document_id=doc.document_id, payload=payload)

    got = store.get_extraction(extraction_id="ex-1")
    assert got["extraction_id"] == "ex-1"
    assert got["vendor"]["value"] == "ACME"

    items = store.list_extractions(limit=10)
    assert any(i["extraction_id"] == "ex-1" for i in items)


def test_sqlite_store_dedupes_by_sha256(tmp_path):
    db_path = tmp_path / "db.sqlite3"
    store = SQLiteStore(db_path=str(db_path))
    store.init()

    content = b"same"
    first = store.upsert_document_from_bytes(filename="a.txt", content=content)
    second = store.upsert_document_from_bytes(filename="b.txt", content=content)

    assert first.document_id == second.document_id
    assert first.sha256 == second.sha256


def test_sqlite_store_reviews_and_corrections(tmp_path):
    db_path = tmp_path / "db.sqlite3"
    store = SQLiteStore(db_path=str(db_path))
    store.init()

    review = store.save_review(extraction_id="ex-1", approved=True, reviewed_at="2026-01-01T00:00:00Z")
    assert review["approved"] is True

    reviews = store.list_reviews()
    assert reviews and reviews[0]["extraction_id"] == "ex-1"

    corr = store.add_correction(
        extraction_id="ex-1",
        field_name="total",
        old_value="10.00",
        new_value="12.00",
        created_at="2026-01-01T00:00:00Z",
    )
    assert corr["field_name"] == "total"

    all_corr = store.list_corrections()
    assert any(c["id"] == corr["id"] for c in all_corr)

    filtered = store.list_corrections(extraction_id="ex-1")
    assert len(filtered) >= 1
