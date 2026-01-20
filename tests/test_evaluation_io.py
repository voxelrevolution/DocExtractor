import pytest

from src.evaluation.io import load_json_records


def test_load_json_records_list(tmp_path):
    path = tmp_path / "records.json"
    path.write_text('[{"extraction_id": "doc-1"}]')
    records = load_json_records(str(path))
    assert records == [{"extraction_id": "doc-1"}]


def test_load_json_records_object(tmp_path):
    path = tmp_path / "records.json"
    path.write_text('{"records": [{"extraction_id": "doc-1"}]}')
    records = load_json_records(str(path))
    assert records == [{"extraction_id": "doc-1"}]


def test_load_json_records_invalid(tmp_path):
    path = tmp_path / "records.json"
    path.write_text('{"bad": 1}')
    with pytest.raises(ValueError):
        load_json_records(str(path))
