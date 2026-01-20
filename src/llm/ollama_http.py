"""src/llm/ollama_http.py
Minimal, local-only Ollama HTTP client.

We intentionally avoid the optional `ollama` Python package to keep dependencies stable.
"""

from __future__ import annotations

import json
from typing import Any, Optional
from urllib.parse import urlparse

import httpx


_LOCAL_HOSTNAMES = {"localhost", "127.0.0.1", "::1"}


class OllamaError(RuntimeError):
    pass


def _validate_local_ollama_url(host: str) -> None:
    parsed = urlparse(host)
    if parsed.scheme not in {"http", "https"}:
        raise OllamaError(f"Unsupported Ollama URL scheme: {parsed.scheme}")

    if parsed.hostname not in _LOCAL_HOSTNAMES:
        raise OllamaError(
            f"Refusing non-local Ollama host: {parsed.hostname}. "
            "Use localhost/127.0.0.1/::1 only."
        )


def ollama_chat(
    *,
    host: str,
    model: str,
    messages: list[dict[str, str]],
    timeout_s: float,
) -> str:
    """Call local Ollama /api/chat and return the assistant message content."""

    _validate_local_ollama_url(host)

    url = host.rstrip("/") + "/api/chat"
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        # Ask for JSON so we can reliably map to our ChatResponse schema.
        "format": "json",
        "options": {
            "temperature": 0.2,
        },
    }

    try:
        with httpx.Client(timeout=timeout_s) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise OllamaError(str(exc)) from exc

    # Ollama chat response shape: {"message": {"role": "assistant", "content": "..."}, ...}
    message = (data or {}).get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise OllamaError("Unexpected Ollama response: missing message.content")

    return content


def extract_reply_from_json_content(content: str) -> Optional[str]:
    """Parse JSON content and return the 'reply' field if present."""

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return None

    if isinstance(parsed, dict) and isinstance(parsed.get("reply"), str):
        return parsed["reply"].strip()

    return None
