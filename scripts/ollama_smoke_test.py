"""scripts/ollama_smoke_test.py

Local-only Ollama sanity checks.

This script does NOT start Ollama. It simply verifies:
- Ollama is reachable on localhost
- The configured model exists
- A small /api/chat request works

Usage:
  /Reserved/DocExtractor/.venv/bin/python scripts/ollama_smoke_test.py

Optional env vars:
  DOCEXTRACTOR_OLLAMA_HOST (default: http://localhost:11434)
  DOCEXTRACTOR_OLLAMA_MODEL (default: llama3.1:8b)
  DOCEXTRACTOR_OLLAMA_TIMEOUT_S (default: 6)
"""

from __future__ import annotations

import os
import sys

import httpx


def main() -> int:
    host = os.getenv("DOCEXTRACTOR_OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("DOCEXTRACTOR_OLLAMA_MODEL", "llama3.1:8b")
    timeout_s = float(os.getenv("DOCEXTRACTOR_OLLAMA_TIMEOUT_S", "6"))

    tags_url = host.rstrip("/") + "/api/tags"
    chat_url = host.rstrip("/") + "/api/chat"

    with httpx.Client(timeout=timeout_s) as client:
        try:
            tags = client.get(tags_url)
            tags.raise_for_status()
        except Exception as exc:
            print(f"ERROR: Ollama not reachable at {tags_url}: {exc}")
            return 2

        payload = tags.json()
        models = [m.get("name") for m in (payload.get("models") or []) if isinstance(m, dict)]
        if model not in set(models):
            print(f"ERROR: Model '{model}' not installed.")
            print("Installed models (first 20):")
            for name in models[:20]:
                print(f"- {name}")
            return 3

        try:
            resp = client.post(
                chat_url,
                json={
                    "model": model,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": "Return JSON: {\"reply\": string}."},
                        {"role": "user", "content": "Say hello in one sentence."},
                    ],
                    "format": "json",
                },
            )
            resp.raise_for_status()
        except Exception as exc:
            print(f"ERROR: Ollama /api/chat failed at {chat_url}: {exc}")
            return 4

        data = resp.json()
        content = ((data or {}).get("message") or {}).get("content")
        if not isinstance(content, str) or not content.strip():
            print("ERROR: Unexpected Ollama response; missing message.content")
            print(data)
            return 5

        print("OK: Ollama reachable and chat responded.")
        print(f"host={host}")
        print(f"model={model}")
        print(f"sample_response={content.strip()[:200]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
