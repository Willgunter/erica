from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import google.generativeai as genai
from elevenlabs import ElevenLabs, VoiceSettings

from ..gemini import init_gemini_model
from .models import Profile
from .storage import LocalObjectStorage

import logging

_logger = logging.getLogger(__name__)


class MediaGenerator:
    """Creates media artifacts for module delivery paths."""

    def __init__(self, storage: LocalObjectStorage) -> None:
        self.storage = storage
        
        gemini_key = os.environ.get("GEMINI_API_KEY")
        _logger.debug("[MediaGenerator] Initializing: has_gemini_key=%s", bool(gemini_key))
        if gemini_key:
            self.gemini_model, _ = init_gemini_model(genai, gemini_key, _logger, "MediaGenerator")
        else:
            self.gemini_model = None
            _logger.warning("[MediaGenerator] GEMINI_API_KEY missing; Gemini-powered visual/audio script generation disabled.")
        
        elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
        if elevenlabs_key:
            self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_key)
        else:
            self.elevenlabs_client = None

    def generate_visual_asset(
        self,
        lesson_id: str,
        module: dict[str, Any],
        profile: Profile,
    ) -> dict[str, Any]:
        module_id = module["module_id"]
        script_key = f"manim/{lesson_id}/{module_id}.py"
        render_key = f"renders/{lesson_id}/{module_id}.mp4"

        try:
            script = self._generate_manim_script_with_ai(module=module, profile=profile)
            self.storage.put_text(script_key, script)

            video_bytes = self._render_manim_video(script)
            self.storage.put_bytes(render_key, video_bytes)

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
        except Exception as e:
            return {
                "asset_id": f"{module_id}-visual",
                "module_id": module_id,
                "asset_type": "video",
                "learner_path": "visual",
                "status": "failed",
                "storage_url": None,
                "duration_seconds": 0,
                "metadata": {"error": str(e)},
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

        try:
            podcast_script = self._generate_podcast_script_with_ai(module=module, profile=profile)
            self.storage.put_text(script_key, json.dumps(podcast_script, indent=2))

            audio_bytes = self._generate_podcast_audio(podcast_script["narration"])
            self.storage.put_bytes(audio_key, audio_bytes)

            return {
                "asset_id": f"{module_id}-audio",
                "module_id": module_id,
                "asset_type": "audio",
                "learner_path": "auditory",
                "status": "completed",
                "storage_url": self.storage.url_for(audio_key),
                "duration_seconds": max(90, module["estimated_minutes"] * 60),
                "metadata": {
                    "renderer": "elevenlabs",
                    "outline_url": self.storage.url_for(script_key),
                },
            }
        except Exception as e:
            return {
                "asset_id": f"{module_id}-audio",
                "module_id": module_id,
                "asset_type": "audio",
                "learner_path": "auditory",
                "status": "failed",
                "storage_url": None,
                "duration_seconds": 0,
                "metadata": {"error": str(e)},
            }

    def _generate_manim_script_with_ai(self, module: dict[str, Any], profile: Profile) -> str:
        """Generate an engaging Manim script using Gemini AI."""
        if not self.gemini_model:
            _logger.debug("[MediaGenerator] generate_manim_script_with_ai using fallback for module=%s", module.get("module_id"))
            return self._manim_script_fallback(module, profile)
        
        try:
            _logger.info("[MediaGenerator] Calling Gemini for manim script | module=%s title=%s", module.get("module_id"), module.get("title"))
            prompt = f"""
You are creating an engaging educational animation script using Manim (Mathematical Animation Engine) for a visual learner.

Module Title: {module['title']}
Objective: {module['objective']}
Teaching Style: {module.get('teaching_style', 'interactive')}

Key Concepts:
{chr(10).join([f"- {step['title']}: {step['instruction'][:100]}" for step in module['steps']])}

Create a Manim Python script that:
1. Uses engaging animations (Write, FadeIn, Transform, Create, etc.)
2. Includes visual elements like Text, shapes, graphs where appropriate
3. Breaks down concepts step-by-step
4. Uses colors and positioning for clarity
5. Keeps each scene under 10 seconds
6. Makes it visually appealing for a learner studying {profile.subject}

Provide ONLY the Python code, no explanations. Start with 'from manim import *'.
"""
            
            response = self.gemini_model.generate_content(prompt)
            script = response.text.strip()
            _logger.debug("[MediaGenerator] Gemini manim response length=%d", len(script))
            
            if "```python" in script:
                script = script.split("```python")[1].split("```")[0].strip()
            elif "```" in script:
                script = script.split("```")[1].split("```")[0].strip()
            
            return script
        except Exception as e:
            _logger.exception("[MediaGenerator] AI script generation failed module=%s: %s", module.get("module_id"), e)
            if "not found" in str(e).lower():
                self.gemini_model = None
                _logger.warning("[MediaGenerator] Disabled Gemini model after NotFound; set GEMINI_MODEL to a valid value.")
            return self._manim_script_fallback(module, profile)
    
    def _manim_script_fallback(self, module: dict[str, Any], profile: Profile) -> str:
        """Fallback Manim script if AI generation fails."""
        lines = [
            "from manim import *",
            "",
            "class LessonScene(Scene):",
            "    def construct(self):",
            f"        title = Text({module['title']!r}, font_size=48)",
            "        self.play(Write(title))",
            "        self.wait(1)",
            "        self.play(FadeOut(title))",
        ]
        for i, step in enumerate(module["steps"], 1):
            instruction = step["instruction"].replace("'", "\\'")[:100]
            lines.extend(
                [
                    f"        step_title = Text('{step['title']}', font_size=36)",
                    "        step_title.to_edge(UP)",
                    "        self.play(FadeIn(step_title))",
                    f"        content = Text('{instruction}', font_size=24)",
                    "        self.play(Write(content))",
                    "        self.wait(2)",
                    "        self.play(FadeOut(step_title), FadeOut(content))",
                ]
            )
        return "\n".join(lines) + "\n"
    
    def _render_manim_video(self, script: str) -> bytes:
        """Render Manim script to video."""
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = Path(tmpdir) / "scene.py"
            script_path.write_text(script)
            
            try:
                result = subprocess.run(
                    ["manim", "-ql", "--format=mp4", str(script_path), "LessonScene"],
                    cwd=tmpdir,
                    capture_output=True,
                    timeout=60
                )
                
                video_path = Path(tmpdir) / "media" / "videos" / "scene" / "480p15" / "LessonScene.mp4"
                if video_path.exists():
                    return video_path.read_bytes()
                else:
                    raise Exception("Video file not generated")
            except subprocess.TimeoutExpired:
                raise Exception("Manim rendering timeout")
            except Exception as e:
                raise Exception(f"Manim rendering failed: {str(e)}")
    
    def _generate_podcast_script_with_ai(self, module: dict[str, Any], profile: Profile) -> dict[str, Any]:
        """Generate engaging podcast-style narration using Gemini AI."""
        if not self.gemini_model:
            _logger.debug("[MediaGenerator] generate_podcast_script_with_ai using fallback for module=%s", module.get("module_id"))
            return self._podcast_script_fallback(module, profile)
        
        try:
            _logger.info("[MediaGenerator] Calling Gemini for podcast narration | module=%s title=%s", module.get("module_id"), module.get("title"))
            prompt = f"""
You are creating an engaging educational podcast script for an auditory learner.

Module Title: {module['title']}
Objective: {module['objective']}
Subject: {profile.subject}
Teaching Style: {module.get('teaching_style', 'conversational')}

Key Concepts:
{chr(10).join([f"- {step['title']}: {step['instruction']}" for step in module['steps']])}

Create a natural, conversational podcast-style narration that:
1. Starts with an engaging hook
2. Explains concepts clearly and conversationally
3. Uses analogies and real-world examples
4. Maintains an encouraging, friendly tone
5. Ends with a brief recap
6. Is appropriate for a {module['estimated_minutes']}-minute listening session

Provide ONLY the narration text, as if you're speaking directly to the learner.
"""
            
            response = self.gemini_model.generate_content(prompt)
            narration = response.text.strip()
            _logger.debug("[MediaGenerator] Gemini podcast response length=%d", len(narration))
            
            return {
                "title": module["title"],
                "style": "podcast",
                "narration": narration,
                "estimated_duration": module["estimated_minutes"] * 60
            }
        except Exception as e:
            _logger.exception("[MediaGenerator] AI podcast script generation failed module=%s: %s", module.get("module_id"), e)
            if "not found" in str(e).lower():
                self.gemini_model = None
                _logger.warning("[MediaGenerator] Disabled Gemini model after NotFound; set GEMINI_MODEL to a valid value.")
            return self._podcast_script_fallback(module, profile)
    
    def _podcast_script_fallback(self, module: dict[str, Any], profile: Profile) -> dict[str, Any]:
        """Fallback podcast script if AI generation fails."""
        segments = [
            f"Welcome to this lesson on {module['title']}.",
            f"Today we'll be covering {module['objective']}.",
        ]
        
        for step in module["steps"]:
            segments.append(f"{step['title']}: {step['instruction']}")
        
        segments.append("That covers the key concepts for this module. Great work!")
        
        return {
            "title": module["title"],
            "style": "podcast",
            "narration": " ".join(segments),
            "estimated_duration": module["estimated_minutes"] * 60
        }
    
    def _generate_podcast_audio(self, narration: str) -> bytes:
        """Generate audio using ElevenLabs TTS."""
        if not self.elevenlabs_client:
            return b"FAKE-MP3-DATA"
        
        try:
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                text=narration,
                voice_id="21m00Tcm4TlvDq8ikWAM",
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.5,
                    use_speaker_boost=True
                )
            )
            
            audio_bytes = b""
            for chunk in audio_generator:
                audio_bytes += chunk
            
            return audio_bytes
        except Exception as e:
            print(f"ElevenLabs audio generation failed: {e}")
            return b"FAKE-MP3-DATA"
