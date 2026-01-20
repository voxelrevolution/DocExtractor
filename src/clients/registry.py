from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional

from src.schemas.clients import ClientRecord


def _default_clients_path() -> str:
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.getenv(
        "DOCEXTRACTOR_CLIENTS_PATH",
        os.path.join(project_root, "data", "clients", "clients.json"),
    )


@dataclass
class ClientRegistry:
    path: str

    @classmethod
    def default(cls) -> "ClientRegistry":
        return cls(path=_default_clients_path())

    def load(self) -> list[ClientRecord]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        items = raw.get("clients", raw) if isinstance(raw, dict) else raw
        if not isinstance(items, list):
            return []
        return [ClientRecord.model_validate(item) for item in items]

    def save(self, clients: list[ClientRecord]) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"clients": [c.model_dump() for c in clients]}, f, indent=2, sort_keys=True)

    def upsert(self, client: ClientRecord) -> ClientRecord:
        clients = self.load()
        by_id: dict[str, ClientRecord] = {c.client_id: c for c in clients}
        by_id[client.client_id] = client
        self.save(list(by_id.values()))
        return client

    def get(self, client_id: str) -> Optional[ClientRecord]:
        client_id = (client_id or "").strip()
        if not client_id:
            return None
        for c in self.load():
            if c.client_id == client_id:
                return c
        return None
