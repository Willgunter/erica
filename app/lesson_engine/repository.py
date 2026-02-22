from __future__ import annotations

from copy import deepcopy
from threading import Lock
from typing import Any

from .models import Lesson, now_iso


class InMemoryLessonRepository:
    """Thread-safe in-memory repository for lesson state."""

    def __init__(self) -> None:
        self._lessons: dict[str, dict[str, Any]] = {}
        self._lock = Lock()

    def create(self, lesson: Lesson) -> dict[str, Any]:
        with self._lock:
            lesson_dict = lesson.as_dict()
            self._lessons[lesson.id] = deepcopy(lesson_dict)
            return deepcopy(lesson_dict)

    def get(self, lesson_id: str) -> dict[str, Any] | None:
        with self._lock:
            lesson = self._lessons.get(lesson_id)
            return deepcopy(lesson) if lesson else None

    def append_media_asset(self, lesson_id: str, asset: dict[str, Any]) -> dict[str, Any] | None:
        with self._lock:
            lesson = self._lessons.get(lesson_id)
            if lesson is None:
                return None
            lesson["media_assets"].append(asset)
            lesson["updated_at"] = now_iso()
            return deepcopy(lesson)

    def set_status(self, lesson_id: str, status: str) -> dict[str, Any] | None:
        with self._lock:
            lesson = self._lessons.get(lesson_id)
            if lesson is None:
                return None
            lesson["status"] = status
            lesson["updated_at"] = now_iso()
            return deepcopy(lesson)
