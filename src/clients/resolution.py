from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from src.clients.registry import ClientRegistry
from src.llm.ollama_http import OllamaError, extract_reply_from_json_content, ollama_chat
from src.schemas.clients import ClientRecord, ClientResolution


def _ollama_enabled() -> bool:
    return os.getenv("DOCEXTRACTOR_OLLAMA_ENABLED", "0").strip().lower() in {"1", "true", "yes"}


def _threshold_auto() -> float:
    try:
        return float(os.getenv("DOCEXTRACTOR_CLIENT_AUTO_THRESHOLD", "0.85"))
    except ValueError:
        return 0.85


def _threshold_ask() -> float:
    try:
        return float(os.getenv("DOCEXTRACTOR_CLIENT_ASK_THRESHOLD", "0.40"))
    except ValueError:
        return 0.40


def _normalize(s: str) -> str:
    return (s or "").lower().strip()


def _heuristic_resolve(*, candidates: list[ClientRecord], text: str) -> ClientResolution:
    haystack = _normalize(text)
    if not haystack or not candidates:
        return ClientResolution(client_id=None, confidence=0.0, evidence=[], policy="unknown")

    matches: list[tuple[ClientRecord, list[str]]] = []
    for client in candidates:
        evidence: list[str] = []
        if _normalize(client.display_name) and _normalize(client.display_name) in haystack:
            evidence.append(f"matched display_name: {client.display_name}")
        for alias in client.aliases:
            if _normalize(alias) and _normalize(alias) in haystack:
                evidence.append(f"matched alias: {alias}")
        if evidence:
            matches.append((client, evidence))

    if not matches:
        return ClientResolution(client_id=None, confidence=0.1, evidence=[], policy="unknown")

    # Prefer the client with the most evidence hits.
    matches.sort(key=lambda item: len(item[1]), reverse=True)
    best, evidence = matches[0]

    if len(matches) == 1 and len(evidence) >= 1:
        conf = 0.9
    else:
        conf = 0.6
        evidence.append(f"ambiguous: {len(matches)} clients matched")

    policy = "auto" if conf >= _threshold_auto() else ("suggest" if conf > _threshold_ask() else "unknown")
    return ClientResolution(client_id=best.client_id, confidence=conf, evidence=evidence, policy=policy)


def _ollama_resolve(*, candidates: list[ClientRecord], text: str) -> Optional[ClientResolution]:
    if not _ollama_enabled():
        return None
    if not candidates:
        return None

    host = os.getenv("DOCEXTRACTOR_OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("DOCEXTRACTOR_OLLAMA_MODEL", "llama3.1:8b")
    timeout_s = float(os.getenv("DOCEXTRACTOR_OLLAMA_TIMEOUT_S", "6"))

    # Keep the prompt tightly bounded: choose ONLY from provided candidates.
    client_list = [
        {
            "client_id": c.client_id,
            "display_name": c.display_name,
            "aliases": c.aliases,
        }
        for c in candidates
    ]

    system = (
        "You are a local-only classifier that assigns a document to a known client. "
        "Choose ONLY from the provided client list. "
        "If the client cannot be determined from the text, return client_id=null with low confidence. "
        "Return JSON only: {\"client_id\": string|null, \"confidence\": number, \"evidence\": [string, ...]}."
    )

    user = {
        "clients": client_list,
        "document_text": (text or "")[:8000],
    }

    try:
        content = ollama_chat(
            host=host,
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": str(user)},
            ],
            timeout_s=timeout_s,
        )
    except (OllamaError, ValueError):
        return None

    raw = extract_reply_from_json_content(content) or (content or "").strip()
    if not raw:
        return None

    try:
        import json

        parsed = json.loads(raw)
        client_id = parsed.get("client_id")
        confidence = float(parsed.get("confidence", 0.0))
        evidence = parsed.get("evidence") or []
        if not isinstance(evidence, list):
            evidence = []

        # Sanitize: must be one of the known candidates.
        candidate_ids = {c.client_id for c in candidates}
        if client_id is not None and client_id not in candidate_ids:
            return ClientResolution(client_id=None, confidence=0.0, evidence=["model returned unknown client_id"], policy="unknown")

        confidence = max(0.0, min(1.0, confidence))
        if client_id is None:
            policy = "unknown"
        else:
            policy = "auto" if confidence >= _threshold_auto() else ("suggest" if confidence > _threshold_ask() else "unknown")

        return ClientResolution(client_id=client_id, confidence=confidence, evidence=[str(x) for x in evidence], policy=policy)
    except Exception:
        return None


@dataclass
class ClientResolver:
    registry: ClientRegistry

    @classmethod
    def default(cls) -> "ClientResolver":
        return cls(registry=ClientRegistry.default())

    def resolve(self, *, filename: str, text: str) -> ClientResolution:
        candidates = self.registry.load()
        combined = f"filename: {filename}\n\n{text}"

        ai = _ollama_resolve(candidates=candidates, text=combined)
        if ai is not None:
            return ai

        return _heuristic_resolve(candidates=candidates, text=combined)
