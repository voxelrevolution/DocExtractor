from src.evaluation.manifest import load_manifest


def test_load_manifest(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text(
        '{"name":"invoice-bench","version":"1","documents":[{"extraction_id":"doc-1","filename":"a.pdf","source_type":"digital_pdf"}]}'
    )
    manifest = load_manifest(str(path))
    assert manifest.name == "invoice-bench"
    assert manifest.documents[0].extraction_id == "doc-1"
