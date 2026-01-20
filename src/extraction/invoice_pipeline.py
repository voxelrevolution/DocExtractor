from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import List, Optional

from src.extraction.invoice import extract_invoice_fields, validate_invoice_extraction
from src.llm import OllamaClient
from src.schemas.invoice import InvoiceExtraction

_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)
_PROMPT_VERSION = "invoice_v1"
_MAX_RETRIES = 2

logger = logging.getLogger(__name__)


def _coerce_extracted_field(value) -> dict:
    if value is None:
        return {"value": None, "confidence": 0.0, "evidence": []}
    if isinstance(value, str):
        return {"value": value, "confidence": 0.0, "evidence": []}
    if isinstance(value, dict):
        coerced = dict(value)
        coerced.setdefault("value", None)
        coerced.setdefault("confidence", 0.0)
        coerced.setdefault("evidence", [])
        if isinstance(coerced.get("evidence"), list):
            normalized = []
            for item in coerced.get("evidence"):
                if not isinstance(item, dict):
                    continue
                item = dict(item)
                if item.get("source") is None:
                    item["source"] = "unknown"
                if item.get("confidence") is None:
                    item["confidence"] = 0.0
                normalized.append(item)
            coerced["evidence"] = normalized
        return coerced
    return {"value": str(value), "confidence": 0.0, "evidence": []}


def _coerce_line_item(item) -> dict:
    if not isinstance(item, dict):
        return {"description": str(item), "quantity": None, "unit_price": None, "amount": None, "evidence": []}
    coerced = dict(item)

    def _value_or_string(v):
        if isinstance(v, dict) and "value" in v:
            return v.get("value")
        return v

    coerced["description"] = _value_or_string(coerced.get("description"))
    coerced["quantity"] = _value_or_string(coerced.get("quantity"))
    coerced["unit_price"] = _value_or_string(coerced.get("unit_price"))
    coerced["amount"] = _value_or_string(coerced.get("amount"))

    if coerced.get("description") is not None and not isinstance(coerced.get("description"), str):
        coerced["description"] = str(coerced.get("description"))
    if coerced.get("quantity") is not None and not isinstance(coerced.get("quantity"), str):
        coerced["quantity"] = str(coerced.get("quantity"))
    if coerced.get("unit_price") is not None and not isinstance(coerced.get("unit_price"), str):
        coerced["unit_price"] = str(coerced.get("unit_price"))
    if coerced.get("amount") is not None and not isinstance(coerced.get("amount"), str):
        coerced["amount"] = str(coerced.get("amount"))

    coerced.setdefault("evidence", [])
    if isinstance(coerced.get("evidence"), list):
        normalized = []
        for ev in coerced.get("evidence"):
            if not isinstance(ev, dict):
                continue
            ev = dict(ev)
            if ev.get("source") is None:
                ev["source"] = "unknown"
            if ev.get("confidence") is None:
                ev["confidence"] = 0.0
            normalized.append(ev)
        coerced["evidence"] = normalized
    return coerced


def _coerce_invoice_payload(data: dict) -> dict:
    """Coerce common simplified LLM JSON into the InvoiceExtraction schema shape."""

    if not isinstance(data, dict):
        return {}

    coerced = dict(data)

    for key in [
        "vendor",
        "invoice_number",
        "invoice_date",
        "subtotal",
        "tax",
        "total",
    ]:
        if key in coerced:
            coerced[key] = _coerce_extracted_field(coerced.get(key))

    line_items = coerced.get("line_items")
    if isinstance(line_items, list):
        coerced["line_items"] = [_coerce_line_item(item) for item in line_items]

    coerced.setdefault("extraction_metadata", {})
    return coerced


def _format_lines_with_meta(
    text: str,
    line_page_map: Optional[List[Optional[int]]] = None,
    line_source_map: Optional[List[str]] = None,
    max_lines: Optional[int] = None,
) -> str:
    lines = [line.rstrip() for line in text.splitlines() if line.strip() != ""]
    if max_lines is not None and max_lines > 0 and len(lines) > max_lines:
        lines = lines[:max_lines]
    output_lines: List[str] = []
    for idx, line in enumerate(lines, start=1):
        page = None
        source = None
        if line_page_map and idx - 1 < len(line_page_map):
            page = line_page_map[idx - 1]
        if line_source_map and idx - 1 < len(line_source_map):
            source = line_source_map[idx - 1]
        if page is not None:
            tag = f"P{page} L{idx}"
        else:
            tag = f"L{idx}"
        if source:
            tag = f"{tag} {source}"
        output_lines.append(f"[{tag}] {line}")
    return "\n".join(output_lines)


def _extract_json(text: str) -> dict:
    match = _JSON_RE.search(text)
    if not match:
        raise ValueError("No JSON object found in LLM response")
    payload = match.group(0)
    return json.loads(payload)


def _repair_json(text: str) -> dict:
    match = _JSON_RE.search(text)
    if not match:
        raise ValueError("No JSON object found in LLM response")
    payload = match.group(0)
    payload = re.sub(r",\s*([}\]])", r"\1", payload)
    payload = payload.replace("\t", " ")
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        payload = payload.replace("'", '"')
        return json.loads(payload)


def _build_prompt(numbered_text: str, schema: dict, strict: bool = False) -> str:
    strict_line = "Return ONLY JSON. No extra text." if strict else "Do not include any commentary, markdown, or code fences."
    return (
        "You are an invoice extraction engine. Return ONLY valid JSON that matches the schema.\n"
        "Use null when a value is missing. Ground every field with evidence if possible.\n"
        "Evidence must use the line tags provided (page and line numbers).\n"
        "IMPORTANT: Fields like vendor/total/invoice_number MUST be objects shaped like: "
        "{\"value\": string|null, \"confidence\": number, \"evidence\": []}. "
        "Do NOT return plain strings for these fields.\n"
        "Example minimal output (shape only): "
        "{\"vendor\": {\"value\": \"ACME\", \"confidence\": 0.0, \"evidence\": []}, "
        "\"invoice_number\": {\"value\": null, \"confidence\": 0.0, \"evidence\": []}, "
        "\"total\": {\"value\": \"17.50\", \"confidence\": 0.0, \"evidence\": []}, "
        "\"line_items\": []}.\n"
        f"{strict_line}\n\n"
        f"JSON schema:\n{json.dumps(schema, indent=2)}\n\n"
        f"Invoice text (line-tagged):\n{numbered_text}\n"
    )


def _mini_schema() -> dict:
    evidence_schema = {
        "type": "object",
        "properties": {
            "source": {"type": ["string", "null"]},
            "page": {"type": ["integer", "null"]},
            "line": {"type": ["integer", "null"]},
            "text": {"type": ["string", "null"]},
            "confidence": {"type": ["number", "null"]},
        },
    }
    field_schema = {
        "type": "object",
        "properties": {
            "value": {"type": ["string", "null"]},
            "confidence": {"type": "number"},
            "evidence": {"type": "array", "items": evidence_schema},
        },
    }
    line_item_schema = {
        "type": "object",
        "properties": {
            "description": {"type": ["string", "null"]},
            "quantity": {"type": ["string", "null"]},
            "unit_price": {"type": ["string", "null"]},
            "amount": {"type": ["string", "null"]},
            "evidence": {"type": "array", "items": evidence_schema},
        },
    }
    return {
        "type": "object",
        "properties": {
            "vendor": field_schema,
            "invoice_number": field_schema,
            "invoice_date": field_schema,
            "subtotal": field_schema,
            "tax": field_schema,
            "total": field_schema,
            "line_items": {"type": "array", "items": line_item_schema},
        },
    }


def extract_invoice_from_text(
    text: str,
    line_page_map: Optional[List[Optional[int]]] = None,
    line_source_map: Optional[List[str]] = None,
    prefer_llm: bool = True,
) -> InvoiceExtraction:
    if prefer_llm:
        llm_error: Optional[str] = None
        last_raw: Optional[str] = None
        try:
            model = os.getenv("DOCEXTRACTOR_OLLAMA_MODEL", "llama3.1:8b")
            host = os.getenv("DOCEXTRACTOR_OLLAMA_HOST", "http://localhost:11434")
            client = OllamaClient(host=host, model=model)
            if not client.load_model():
                raise RuntimeError("Ollama model not available")

            max_lines_env = os.getenv("DOCEXTRACTOR_OLLAMA_MAX_LINES", "120").strip()
            try:
                max_lines = int(max_lines_env)
            except ValueError:
                max_lines = 120
            numbered_text = _format_lines_with_meta(text, line_page_map, line_source_map, max_lines=max_lines)
            use_mini_schema = os.getenv("DOCEXTRACTOR_OLLAMA_MINI_SCHEMA", "0").strip().lower() in {"1", "true", "yes"}
            schema = _mini_schema() if use_mini_schema else InvoiceExtraction.model_json_schema()
            last_error: Optional[Exception] = None
            for attempt in range(_MAX_RETRIES):
                prompt = _build_prompt(numbered_text, schema, strict=attempt > 0)
                logger.info(
                    "LLM prompt prepared attempt=%s lines=%s chars=%s",
                    attempt + 1,
                    max_lines,
                    len(prompt),
                )
                infer_start = time.perf_counter()
                response = client.infer(prompt)
                infer_elapsed = time.perf_counter() - infer_start
                raw = response.get("response", "")
                last_raw = raw if isinstance(raw, str) else None
                logger.info(
                    "LLM infer complete attempt=%s engine=ollama model=%s elapsed_s=%.3f",
                    attempt + 1,
                    response.get("model", client.model),
                    infer_elapsed,
                )
                try:
                    parse_start = time.perf_counter()
                    data = _extract_json(raw)
                    parse_elapsed = time.perf_counter() - parse_start
                    logger.info("LLM parse ok attempt=%s elapsed_s=%.3f", attempt + 1, parse_elapsed)
                except Exception as exc:
                    last_error = exc
                    try:
                        repair_start = time.perf_counter()
                        data = _repair_json(raw)
                        repair_elapsed = time.perf_counter() - repair_start
                        logger.info("LLM repair ok attempt=%s elapsed_s=%.3f", attempt + 1, repair_elapsed)
                    except Exception:
                        continue
                try:
                    extraction = InvoiceExtraction.model_validate(_coerce_invoice_payload(data))
                except Exception as exc:
                    last_error = exc
                    llm_error = str(exc)
                    continue
                extraction.extraction_metadata.update(
                    {
                        "engine": "llm",
                        "model": response.get("model", client.model),
                        "prompt_version": _PROMPT_VERSION,
                        "tokens_used": int(response.get("tokens_used", 0)),
                    }
                )
                return validate_invoice_extraction(extraction)
            if last_error:
                raise last_error
        except Exception as exc:
            llm_error = llm_error or str(exc) or "llm_failed"
            raw_snippet = ""
            if isinstance(last_raw, str) and last_raw.strip():
                raw_snippet = last_raw.strip().replace("\n", " ")[:400]
            logger.info(
                "LLM extraction failed; falling back to rules. error=%s raw=%s",
                llm_error,
                raw_snippet,
            )

    extraction = extract_invoice_fields(text, line_page_map, line_source_map)
    extraction.extraction_metadata.update(
        {
            "engine": "rules",
            "prompt_version": _PROMPT_VERSION,
        }
    )
    return extraction
