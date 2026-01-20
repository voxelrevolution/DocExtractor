"""src/llm/__init__.py
LLM runtime integration (Ollama).

This module provides an Ollama client used by invoice extraction.
It intentionally avoids the optional `ollama` Python package and uses HTTP.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Optional

import httpx

from src.llm.ollama_http import OllamaError, _validate_local_ollama_url

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with local Ollama instance (HTTP)."""

    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        self.host = host
        self.model = model
        self._ready = False
        logger.info(f"OllamaClient initialized: {host}, model={model}")

    def load_model(self) -> bool:
        """Verify the configured model exists on the local Ollama server."""

        try:
            _validate_local_ollama_url(self.host)
            url = self.host.rstrip("/") + "/api/tags"
            with httpx.Client(timeout=3.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()
            names = [m.get("name") for m in (data.get("models") or []) if isinstance(m, dict)]
            self._ready = any(self.model == name for name in names)
            if not self._ready:
                logger.warning(f"Model {self.model} not found. Available: {names}")
            return self._ready
        except Exception as exc:
            logger.error(f"Error loading model: {exc}")
            self._ready = False
            return False

    def infer(self, prompt: str, schema: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Run inference using Ollama /api/generate.

        Returns a dict with keys: response, model, tokens_used.
        """

        if not self._ready:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        _validate_local_ollama_url(self.host)
        url = self.host.rstrip("/") + "/api/generate"
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.0},
        }
        try:
            start = time.perf_counter()
            timeout_s = float(os.getenv("DOCEXTRACTOR_OLLAMA_TIMEOUT_S", "20"))
            with httpx.Client(timeout=timeout_s) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
            elapsed = time.perf_counter() - start
            logger.info("Ollama infer ok model=%s elapsed_s=%.3f timeout_s=%.1f", self.model, elapsed, timeout_s)
        except (httpx.HTTPError, ValueError) as exc:
            elapsed = time.perf_counter() - start if 'start' in locals() else None
            if elapsed is not None:
                logger.warning("Ollama infer failed model=%s elapsed_s=%.3f timeout_s=%.1f error=%s", self.model, elapsed, timeout_s, exc)
            raise OllamaError(str(exc)) from exc

        return {
            "response": (data or {}).get("response", "") or "",
            "model": self.model,
            "tokens_used": int((data or {}).get("eval_count", 0) or 0),
        }

    def count_tokens(self, text: str) -> int:
        return len(text) // 4
