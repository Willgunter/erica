from __future__ import annotations

from collections import defaultdict
from threading import Lock
from typing import Any

from .media import MediaGenerator
from .models import ContentChunk, Lesson, Profile
from .planner import LessonPlanner
from .repository import InMemoryLessonRepository
from .worker_queue import InProcessWorkerQueue


class LessonGenerationService:
    """Coordinates personalized planning and async media generation."""

    def __init__(
        self,
        repository: InMemoryLessonRepository,
        planner: LessonPlanner,
        media_generator: MediaGenerator,
        worker_queue: InProcessWorkerQueue,
    ) -> None:
        self.repository = repository
        self.planner = planner
        self.media_generator = media_generator
        self.worker_queue = worker_queue
        self._pending_assets: dict[str, int] = defaultdict(int)
        self._pending_lock = Lock()

    def generate_lesson(
        self,
        profile_payload: dict[str, Any],
        chunks_payload: list[dict[str, Any]],
    ) -> dict[str, Any]:
        profile = Profile.from_payload(profile_payload)
        chunks = [ContentChunk.from_payload(chunk, index) for index, chunk in enumerate(chunks_payload)]

        modules, checkpoints, estimated_duration = self.planner.plan(profile=profile, chunks=chunks)
        lesson = Lesson.new(
            profile=profile,
            modules=modules,
            checkpoints=checkpoints,
            estimated_duration=estimated_duration,
        )
        lesson_dict = self.repository.create(lesson)

        formats = set(profile.content_formats)
        wants_visual = "visual" in formats
        wants_audio = "auditory" in formats
        if not wants_visual and not wants_audio:
            self.repository.set_status(lesson.id, "completed")
            return self.repository.get(lesson.id) or lesson_dict

        for module in modules:
            if wants_visual:
                self._submit_media_task(
                    lesson_id=lesson.id,
                    module=module,
                    profile=profile,
                    mode="visual",
                )
            if wants_audio:
                self._submit_media_task(
                    lesson_id=lesson.id,
                    module=module,
                    profile=profile,
                    mode="audio",
                )
        return lesson_dict

    def get_lesson(self, lesson_id: str) -> dict[str, Any] | None:
        return self.repository.get(lesson_id)

    def generate_short_visual_asset(
        self,
        lesson_id: str,
        module: dict[str, Any],
        profile: Profile,
        prompt: str,
        duration_seconds: int = 2,
    ) -> dict[str, Any] | None:
        asset = self.media_generator.generate_visual_asset(
            lesson_id=lesson_id,
            module=module,
            profile=profile,
            prompt=prompt,
            duration_seconds=duration_seconds,
        )
        return self.repository.append_media_asset(lesson_id=lesson_id, asset=asset)

    def _submit_media_task(
        self,
        lesson_id: str,
        module: dict[str, Any],
        profile: Profile,
        mode: str,
    ) -> None:
        with self._pending_lock:
            self._pending_assets[lesson_id] += 1

        if mode == "visual":
            future = self.worker_queue.submit(
                self.media_generator.generate_visual_asset,
                lesson_id,
                module,
                profile,
            )
        else:
            future = self.worker_queue.submit(
                self.media_generator.generate_audio_asset,
                lesson_id,
                module,
                profile,
            )

        def on_complete(task: Any) -> None:
            try:
                asset = task.result()
            except Exception as exc:  # pragma: no cover
                asset = {
                    "asset_id": f"{module['module_id']}-{mode}-failed",
                    "module_id": module["module_id"],
                    "asset_type": "video" if mode == "visual" else "audio",
                    "learner_path": "visual" if mode == "visual" else "auditory",
                    "status": "failed",
                    "storage_url": None,
                    "duration_seconds": 0,
                    "metadata": {"error": str(exc)},
                }

            self.repository.append_media_asset(lesson_id=lesson_id, asset=asset)
            self._mark_task_complete(lesson_id=lesson_id)

        future.add_done_callback(on_complete)

    def _mark_task_complete(self, lesson_id: str) -> None:
        with self._pending_lock:
            self._pending_assets[lesson_id] -= 1
            pending = self._pending_assets[lesson_id]
            if pending <= 0:
                self._pending_assets.pop(lesson_id, None)
                self.repository.set_status(lesson_id, "completed")
