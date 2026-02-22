from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable


class InProcessWorkerQueue:
    """Simple queue abstraction to mimic long-running worker tasks."""

    def __init__(self, max_workers: int = 4) -> None:
        self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="lesson-worker")

    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future[Any]:
        return self._executor.submit(fn, *args, **kwargs)
