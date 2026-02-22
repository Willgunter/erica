from __future__ import annotations

import json
import time
from typing import Any

from .models import Profile
from .storage import LocalObjectStorage


class MediaGenerator:
    """Creates media artifacts for module delivery paths."""

    def __init__(self, storage: LocalObjectStorage) -> None:
        self.storage = storage

    def generate_visual_asset(
        self,
        lesson_id: str,
        module: dict[str, Any],
        profile: Profile,
    ) -> dict[str, Any]:
        module_id = module["module_id"]
        script_key = f"manim/{lesson_id}/{module_id}.py"
        render_key = f"renders/{lesson_id}/{module_id}.mp4"

        script = self._manim_script(module=module, profile=profile)
        self.storage.put_text(script_key, script)

        time.sleep(0.05)
        self.storage.put_bytes(
            render_key,
            b"FAKE-MP4-DATA",
        )

        return {
            "asset_id": f"{module_id}-visual",
            "module_id": module_id,
            "asset_type": "video",
            "learner_path": "visual",
            "status": "completed",
            "storage_url": self.storage.url_for(render_key),
            "duration_seconds": max(45, module["estimated_minutes"] * 50),
            "metadata": {
                "renderer": "manim",
                "script_url": self.storage.url_for(script_key),
            },
        }

    def generate_audio_asset(
        self,
        lesson_id: str,
        module: dict[str, Any],
        profile: Profile,
    ) -> dict[str, Any]:
        module_id = module["module_id"]
        script_key = f"audio/{lesson_id}/{module_id}.json"
        audio_key = f"audio/{lesson_id}/{module_id}.mp3"

        podcast_outline = {
            "voice": profile.accessibility.get("preferred_voice", "neutral"),
            "style": "podcast",
            "title": module["title"],
            "segment": [
                f"Intro: What you will learn in {module['title']}.",
                module["steps"][0]["instruction"],
                module["steps"][1]["instruction"],
                "Recap and quick check-in.",
            ],
        }
        self.storage.put_text(script_key, json.dumps(podcast_outline, indent=2))

        time.sleep(0.05)
        self.storage.put_bytes(audio_key, b"FAKE-MP3-DATA")

        return {
            "asset_id": f"{module_id}-audio",
            "module_id": module_id,
            "asset_type": "audio",
            "learner_path": "auditory",
            "status": "completed",
            "storage_url": self.storage.url_for(audio_key),
            "duration_seconds": max(90, module["estimated_minutes"] * 60),
            "metadata": {
                "renderer": "notebooklm",
                "outline_url": self.storage.url_for(script_key),
            },
        }

    def _manim_script(self, module: dict[str, Any], profile: Profile) -> str:
        lines = [
            "from manim import *",
            "",
            "class LessonScene(Scene):",
            "    def construct(self):",
            f"        title = Text({module['title']!r})",
            "        self.play(Write(title))",
            "        self.wait(0.5)",
        ]
        for step in module["steps"]:
            instruction = step["instruction"].replace("'", "\\'")
            lines.extend(
                [
                    f"        step_text = Text('{instruction[:80]}')",
                    "        self.play(Transform(title, step_text))",
                    "        self.wait(0.5)",
                ]
            )
        lines.extend(
            [
                f"        checkpoint = Text('Checkpoint for {profile.user_id}')",
                "        self.play(FadeIn(checkpoint))",
                "        self.wait(0.5)",
            ]
        )
        return "\n".join(lines) + "\n"
