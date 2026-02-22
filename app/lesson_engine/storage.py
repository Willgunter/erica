from __future__ import annotations

from pathlib import Path


class LocalObjectStorage:
    """Filesystem-backed object storage adapter used for local development."""

    def __init__(self, root_dir: str) -> None:
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def put_text(self, key: str, value: str) -> str:
        path = self.root_dir / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return self.url_for(key)

    def put_bytes(self, key: str, value: bytes) -> str:
        path = self.root_dir / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)
        return self.url_for(key)

    def url_for(self, key: str) -> str:
        return f"local://{key}"
