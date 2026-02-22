from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator

from .config import Config


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Database:
    def __init__(self, config: Config):
        self.config = config
        self._shared_memory_conn: sqlite3.Connection | None = None

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        if self.config.db_path == ":memory:":
            if self._shared_memory_conn is None:
                self._shared_memory_conn = sqlite3.connect(":memory:")
                self._shared_memory_conn.row_factory = sqlite3.Row
            conn = self._shared_memory_conn
            yield conn
            conn.commit()
            return

        conn = sqlite3.connect(self.config.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS lesson_sources (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    filename TEXT NOT NULL,
                    type TEXT NOT NULL,
                    storage_url TEXT,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    input_mode TEXT NOT NULL,
                    source_metadata TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS content_chunks (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    metadata TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES lesson_sources(id)
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_content_chunks_source_id ON content_chunks(source_id)"
            )
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_content_chunks_source_index ON content_chunks(source_id, chunk_index)"
            )

    def create_source(
        self,
        *,
        source_id: str,
        user_id: str | None,
        filename: str,
        source_type: str,
        storage_url: str | None,
        input_mode: str,
        source_metadata: dict[str, Any] | None = None,
    ) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO lesson_sources (
                    id, user_id, filename, type, storage_url, status,
                    error_message, input_mode, source_metadata, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, 'queued', NULL, ?, ?, ?, ?)
                """,
                (
                    source_id,
                    user_id,
                    filename,
                    source_type,
                    storage_url,
                    input_mode,
                    json.dumps(source_metadata or {}),
                    now,
                    now,
                ),
            )

    def get_source(self, source_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM lesson_sources WHERE id = ?", (source_id,)
            ).fetchone()
        if not row:
            return None
        out = dict(row)
        out["source_metadata"] = json.loads(out["source_metadata"] or "{}")
        return out

    def update_source_status(
        self,
        source_id: str,
        status: str,
        *,
        error_message: str | None = None,
        source_metadata_patch: dict[str, Any] | None = None,
    ) -> None:
        with self.connect() as conn:
            current = conn.execute(
                "SELECT source_metadata FROM lesson_sources WHERE id = ?", (source_id,)
            ).fetchone()
            if current is None:
                return

            metadata = json.loads(current["source_metadata"] or "{}")
            if source_metadata_patch:
                metadata.update(source_metadata_patch)

            conn.execute(
                """
                UPDATE lesson_sources
                SET status = ?, error_message = ?, source_metadata = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    status,
                    error_message,
                    json.dumps(metadata),
                    utc_now_iso(),
                    source_id,
                ),
            )

    def replace_chunks(self, source_id: str, chunks: list[dict[str, Any]]) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute("DELETE FROM content_chunks WHERE source_id = ?", (source_id,))
            conn.executemany(
                """
                INSERT INTO content_chunks (id, source_id, chunk_index, text, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        chunk["id"],
                        source_id,
                        chunk["chunk_index"],
                        chunk["text"],
                        json.dumps(chunk.get("metadata") or {}),
                        now,
                    )
                    for chunk in chunks
                ],
            )

    def chunk_stats(self, source_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            count_row = conn.execute(
                "SELECT COUNT(*) AS count FROM content_chunks WHERE source_id = ?", (source_id,)
            ).fetchone()
            sample = conn.execute(
                """
                SELECT chunk_index, text, metadata
                FROM content_chunks
                WHERE source_id = ?
                ORDER BY chunk_index
                LIMIT 1
                """,
                (source_id,),
            ).fetchone()

        out: dict[str, Any] = {
            "chunk_count": int(count_row["count"]) if count_row else 0,
            "sample_chunk": None,
        }
        if sample:
            out["sample_chunk"] = {
                "chunk_index": sample["chunk_index"],
                "preview": sample["text"][:240],
                "metadata": json.loads(sample["metadata"] or "{}"),
            }
        return out
