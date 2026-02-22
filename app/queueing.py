from __future__ import annotations

from typing import Any

from .config import Config


class QueueManager:
    def __init__(self, config: Config):
        self.config = config

    def _queue(self):
        try:
            from redis import Redis
            from rq import Queue
        except ImportError as exc:
            raise RuntimeError("redis and rq are required for async queue mode") from exc

        if not self.config.redis_url:
            raise RuntimeError("REDIS_URL is required for async queue mode")
        conn = Redis.from_url(self.config.redis_url)
        return Queue("ingest", connection=conn)

    def enqueue_ingestion(self, source_id: str) -> dict[str, Any]:
        if self.config.ingest_sync:
            from .tasks import process_ingestion

            try:
                process_ingestion(source_id)
            except Exception:
                # Sync mode is a local fallback; status details are persisted by the task.
                pass
            return {"mode": "sync", "job_id": None}

        try:
            queue = self._queue()
            job = queue.enqueue("app.tasks.process_ingestion", source_id)
            return {"mode": "rq", "job_id": job.id}
        except RuntimeError:
            from .tasks import process_ingestion

            try:
                process_ingestion(source_id)
            except Exception:
                pass
            return {"mode": "sync-fallback", "job_id": None}
