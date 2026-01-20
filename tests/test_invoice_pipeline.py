from src.extraction import invoice_pipeline


def test_format_lines_with_meta_includes_page_and_source():
    text = "Line one\nLine two"
    output = invoice_pipeline._format_lines_with_meta(
        text, line_page_map=[1, 1], line_source_map=["pdf", "ocr"]
    )

    assert "[P1 L1 pdf] Line one" in output
    assert "[P1 L2 ocr] Line two" in output


def test_extract_and_repair_json_parsing():
    raw = "response: {\"vendor\": {\"value\": \"ACME\"}}"
    parsed = invoice_pipeline._extract_json(raw)
    assert parsed["vendor"]["value"] == "ACME"

    broken = "response: {'vendor': {'value': 'ACME',},}"
    repaired = invoice_pipeline._repair_json(broken)
    assert repaired["vendor"]["value"] == "ACME"


def test_extract_invoice_from_text_llm_success(monkeypatch):
    class FakeClient:
        model = "mock-model"

        def load_model(self):
            return True

        def infer(self, prompt):
            return {
                "model": "mock-model",
                "tokens_used": 42,
                "response": '{"vendor": {"value": "ACME"}}',
            }

    monkeypatch.setattr(invoice_pipeline, "OllamaClient", FakeClient)

    result = invoice_pipeline.extract_invoice_from_text("ACME Supplies")

    assert result.vendor.value == "ACME"
    assert result.extraction_metadata["engine"] == "llm"
    assert result.extraction_metadata["prompt_version"] == "invoice_v1"


def test_extract_invoice_from_text_fallback_to_rules(monkeypatch):
    class FakeClient:
        model = "mock-model"

        def load_model(self):
            return False

    monkeypatch.setattr(invoice_pipeline, "OllamaClient", FakeClient)

    sample = "ACME Supplies\nTotal: 12.50"
    result = invoice_pipeline.extract_invoice_from_text(sample)

    assert result.extraction_metadata["engine"] == "rules"
    assert result.total.value == "12.50"
