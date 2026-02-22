from __future__ import annotations

import os

from redis import Redis
from rq import Connection, Worker


def run_worker() -> None:
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("Set REDIS_URL to run the RQ worker")

    conn = Redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker(["ingest"])
        worker.work()


if __name__ == "__main__":
    run_worker()
