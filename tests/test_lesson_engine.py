from __future__ import annotations

import time
import unittest
from tempfile import mkdtemp
from shutil import rmtree

from app.lesson_engine.media import MediaGenerator
from app.lesson_engine.planner import LessonPlanner
from app.lesson_engine.repository import InMemoryLessonRepository
from app.lesson_engine.service import LessonGenerationService
from app.lesson_engine.storage import LocalObjectStorage
from app.lesson_engine.worker_queue import InProcessWorkerQueue


class LessonEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp_storage_dir = mkdtemp(prefix="lesson-engine-test-")
        storage = LocalObjectStorage(self._tmp_storage_dir)
        self.service = LessonGenerationService(
            repository=InMemoryLessonRepository(),
            planner=LessonPlanner(),
            media_generator=MediaGenerator(storage=storage),
            worker_queue=InProcessWorkerQueue(max_workers=2),
        )

    def tearDown(self) -> None:
        rmtree(self._tmp_storage_dir, ignore_errors=True)

    def test_checkpoints_are_present_in_every_module(self) -> None:
        payload = {
            "profile": {
                "user_id": "u-1",
                "subject": "Algorithms",
                "goals": ["Prepare for interviews"],
                "pacing": "medium",
                "content_formats": ["text"],
            },
            "content_chunks": [
                {"id": "c1", "source_id": "s1", "chunk_index": 0, "text": "Arrays store ordered data."},
                {"id": "c2", "source_id": "s1", "chunk_index": 1, "text": "Hash maps optimize lookup."},
                {"id": "c3", "source_id": "s1", "chunk_index": 2, "text": "Stacks are LIFO structures."},
            ],
        }

        lesson = self.service.generate_lesson(payload["profile"], payload["content_chunks"])

        self.assertGreater(len(lesson["modules"]), 0)
        self.assertEqual(len(lesson["checkpoints"]), len(lesson["modules"]))
        for module in lesson["modules"]:
            self.assertIn("checkpoint", module)
            self.assertEqual(module["checkpoint"]["marker"], "knowledge_check")
            self.assertGreaterEqual(len(module["checkpoint"]["questions"]), 2)
            self.assertLessEqual(len(module["checkpoint"]["questions"]), 3)

    def test_visual_and_audio_assets_are_generated(self) -> None:
        payload = {
            "profile": {
                "user_id": "u-2",
                "subject": "Python",
                "goals": ["Build ETL scripts"],
                "pacing": "medium",
                "content_formats": ["visual", "auditory"],
            },
            "content_chunks": [
                {"id": "c1", "source_id": "s1", "chunk_index": 0, "text": "Variables and data types."},
                {"id": "c2", "source_id": "s1", "chunk_index": 1, "text": "Control flow and loops."},
            ],
        }

        lesson = self.service.generate_lesson(payload["profile"], payload["content_chunks"])
        lesson_id = lesson["id"]

        for _ in range(50):
            latest = self.service.get_lesson(lesson_id)
            if latest and latest["status"] == "completed":
                break
            time.sleep(0.05)

        latest = self.service.get_lesson(lesson_id)
        assert latest is not None
        self.assertEqual(latest["status"], "completed")

        expected_assets = len(latest["modules"]) * 2
        self.assertEqual(len(latest["media_assets"]), expected_assets)
        asset_types = {asset["asset_type"] for asset in latest["media_assets"]}
        self.assertEqual(asset_types, {"video", "audio"})


if __name__ == "__main__":
    unittest.main()
