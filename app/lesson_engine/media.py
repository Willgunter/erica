from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
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
        self.latex_available = shutil.which("latex") is not None
        _logger.debug("[MediaGenerator] LaTeX available=%s", self.latex_available)
        
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
        *,
        prompt: str | None = None,
        duration_seconds: int | None = None,
    ) -> dict[str, Any]:
        module_id = module["module_id"]
        script_key = f"manim/{lesson_id}/{module_id}.py"
        fallback_script_key = f"manim/{lesson_id}/{module_id}.fallback.py"
        emergency_script_key = f"manim/{lesson_id}/{module_id}.emergency.py"
        render_key = f"renders/{lesson_id}/{module_id}.mp4"
        clip_duration = max(2, duration_seconds or 0) if duration_seconds else None
        render_timeout_seconds = 75 if clip_duration is not None else 180
        _logger.info(
            "[MediaGenerator] generate_visual_asset start | lesson=%s module=%s duration=%s has_prompt=%s",
            lesson_id,
            module_id,
            duration_seconds,
            bool(prompt),
        )

        try:
            script = self._generate_manim_script_with_ai(
                module=module,
                profile=profile,
                custom_prompt=prompt,
                target_duration_seconds=duration_seconds,
            )
            self.storage.put_text(script_key, script)
            _logger.debug(
                "[MediaGenerator] Stored script | lesson=%s module=%s script_key=%s chars=%d scene_classes=%s",
                lesson_id,
                module_id,
                script_key,
                len(script),
                self._extract_scene_class_names(script),
            )

            video_bytes: bytes
            used_fallback_render = False
            used_emergency_render = False
            primary_render_error: str | None = None
            fallback_render_error: str | None = None

            def _build_fallback_script() -> str:
                return (
                    self._short_manim_script_fallback(
                        module=module,
                        custom_prompt=prompt,
                        target_duration_seconds=clip_duration or 2,
                    )
                    if clip_duration is not None
                    else self._manim_script_fallback(module, profile)
                )

            if not self.latex_available:
                primary_render_error = "Skipped AI script: LaTeX executable not found on host."
                _logger.warning(
                    "[MediaGenerator] Skipping primary AI render because LaTeX is unavailable | lesson=%s module=%s",
                    lesson_id,
                    module_id,
                )
                fallback_script = _build_fallback_script()
                self.storage.put_text(fallback_script_key, fallback_script)
                _logger.debug(
                    "[MediaGenerator] Stored fallback script | lesson=%s module=%s script_key=%s chars=%d scene_classes=%s",
                    lesson_id,
                    module_id,
                    fallback_script_key,
                    len(fallback_script),
                    self._extract_scene_class_names(fallback_script),
                )
                video_bytes = self._render_manim_video(fallback_script, timeout_seconds=render_timeout_seconds)
                used_fallback_render = True
                _logger.info(
                    "[MediaGenerator] Fallback render succeeded (LaTeX unavailable path) | lesson=%s module=%s",
                    lesson_id,
                    module_id,
                )
            else:
                try:
                    video_bytes = self._render_manim_video(script, timeout_seconds=render_timeout_seconds)
                except Exception as render_exc:
                    primary_render_error = str(render_exc)
                    _logger.warning(
                        "[MediaGenerator] Primary manim render failed; retrying with fallback script | lesson=%s module=%s error=%s",
                        lesson_id,
                        module_id,
                        primary_render_error,
                    )
                    fallback_script = _build_fallback_script()
                    self.storage.put_text(fallback_script_key, fallback_script)
                    _logger.debug(
                        "[MediaGenerator] Stored fallback script | lesson=%s module=%s script_key=%s chars=%d scene_classes=%s",
                        lesson_id,
                        module_id,
                        fallback_script_key,
                        len(fallback_script),
                        self._extract_scene_class_names(fallback_script),
                    )
                    try:
                        video_bytes = self._render_manim_video(fallback_script, timeout_seconds=render_timeout_seconds)
                        used_fallback_render = True
                        _logger.info(
                            "[MediaGenerator] Fallback render succeeded | lesson=%s module=%s",
                            lesson_id,
                            module_id,
                        )
                    except Exception as fallback_exc:
                        fallback_render_error = str(fallback_exc)
                        _logger.warning(
                            "[MediaGenerator] Fallback manim render failed; retrying with emergency script | lesson=%s module=%s error=%s",
                            lesson_id,
                            module_id,
                            fallback_render_error,
                        )
                        emergency_script = self._minimal_manim_script(module=module, custom_prompt=prompt)
                        self.storage.put_text(emergency_script_key, emergency_script)
                        _logger.debug(
                            "[MediaGenerator] Stored emergency script | lesson=%s module=%s script_key=%s chars=%d scene_classes=%s",
                            lesson_id,
                            module_id,
                            emergency_script_key,
                            len(emergency_script),
                            self._extract_scene_class_names(emergency_script),
                        )
                        video_bytes = self._render_manim_video(emergency_script, timeout_seconds=45)
                        used_fallback_render = True
                        used_emergency_render = True
                        _logger.info(
                            "[MediaGenerator] Emergency render succeeded | lesson=%s module=%s",
                            lesson_id,
                            module_id,
                        )

            self.storage.put_bytes(render_key, video_bytes)
            _logger.info(
                "[MediaGenerator] generate_visual_asset success | lesson=%s module=%s render_key=%s bytes=%d",
                lesson_id,
                module_id,
                render_key,
                len(video_bytes),
            )

            return {
                "asset_id": f"{module_id}-visual",
                "module_id": module_id,
                "asset_type": "video",
                "learner_path": "visual",
                "status": "completed",
                "storage_url": self.storage.url_for(render_key),
                "duration_seconds": clip_duration if clip_duration is not None else max(45, module["estimated_minutes"] * 50),
                "metadata": {
                    "renderer": "manim",
                    "script_url": self.storage.url_for(script_key),
                    "requested_prompt": prompt,
                    "requested_duration_seconds": duration_seconds,
                    "used_fallback_render": used_fallback_render,
                    "used_emergency_render": used_emergency_render,
                    "fallback_script_url": self.storage.url_for(fallback_script_key) if used_fallback_render else None,
                    "emergency_script_url": self.storage.url_for(emergency_script_key) if used_emergency_render else None,
                    "primary_render_error": primary_render_error,
                    "fallback_render_error": fallback_render_error,
                },
            }
        except Exception as e:
            _logger.exception(
                "[MediaGenerator] generate_visual_asset failed | lesson=%s module=%s",
                lesson_id,
                module_id,
            )
            return {
                "asset_id": f"{module_id}-visual",
                "module_id": module_id,
                "asset_type": "video",
                "learner_path": "visual",
                "status": "failed",
                "storage_url": None,
                "duration_seconds": 0,
                "metadata": {
                    "error": str(e),
                    "requested_prompt": prompt,
                    "requested_duration_seconds": duration_seconds,
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

    def _generate_manim_script_with_ai(
        self,
        module: dict[str, Any],
        profile: Profile,
        custom_prompt: str | None = None,
        target_duration_seconds: int | None = None,
    ) -> str:
        """Generate an engaging Manim script using Gemini AI."""
        clip_length = max(2, target_duration_seconds or 2)

        if not self.gemini_model:
            _logger.debug("[MediaGenerator] generate_manim_script_with_ai using fallback for module=%s", module.get("module_id"))
            return self._manim_script_fallback(module, profile)
        
        try:
            _logger.info("[MediaGenerator] Calling Gemini for manim script | module=%s title=%s", module.get("module_id"), module.get("title"))
            if custom_prompt:
                prompt = f"""
You are creating a simple, short educational Manim animation from this request:

Simple Prompt: {custom_prompt}
Subject context: {profile.subject}
Duration target: ~{clip_length} seconds

Generate only production-safe Manim code using built-in primitives.
Keep the entire scene short and single-beat.
Do not use arrange_in_grid.
When using positioning helpers, always call methods like get_center() with parentheses.
{"Do not use Tex or MathTex." if not self.latex_available else ""}

Provide ONLY the Python code, no explanations. Start with 'from manim import *'.
"""
            else:
                tex_guidance = (
                    "3. Uses MathTex, NumberPlane, Axes, arrows, and geometric transformations where they clarify concepts."
                    if self.latex_available
                    else "3. Uses Text, NumberPlane, Axes, arrows, and geometric transformations. Do not use Tex or MathTex."
                )
                prompt = f"""
You are creating an engaging educational animation script using Manim (Mathematical Animation Engine) for a visual learner.

Module Title: {module['title']}
Objective: {module['objective']}
Teaching Style: {module.get('teaching_style', 'interactive')}

Key Concepts:
{chr(10).join([f"- {step['title']}: {step['instruction'][:100]}" for step in module['steps']])}

Create a Manim Python script in a 3Blue1Brown-inspired educational style that:
1. Uses a clean dark background with high-contrast blue and gold accents.
2. Opens with a strong visual hook before the explanation.
{tex_guidance}
4. Uses smooth transitions (TransformMatchingTex, ReplacementTransform, FadeTransform, LaggedStart).
5. Builds intuition first, then formal notation.
6. Breaks the topic into 3-5 concise beats with visual continuity across beats.
7. Keeps pacing lively and each beat under ~10 seconds.
8. Includes one short recap card at the end.
9. Uses only built-in Manim primitives and stays production-safe (no external assets/files).
10. Makes it visually compelling for a learner studying {profile.subject}.
11. Do not use arrange_in_grid.
12. When using positioning helpers, always call methods like get_center() with parentheses.
13. {"Do not use Tex, MathTex, or TransformMatchingTex." if not self.latex_available else "If you use TransformMatchingTex, ensure both inputs are valid MathTex objects."}

Provide ONLY the Python code, no explanations. Start with 'from manim import *'.
"""
            
            response = self.gemini_model.generate_content(prompt)
            script = response.text.strip()
            _logger.debug("[MediaGenerator] Gemini manim response length=%d", len(script))
            
            if "```python" in script:
                script = script.split("```python")[1].split("```")[0].strip()
            elif "```" in script:
                script = script.split("```")[1].split("```")[0].strip()

            _logger.debug(
                "[MediaGenerator] Cleaned manim script | module=%s chars=%d scene_classes=%s",
                module.get("module_id"),
                len(script),
                self._extract_scene_class_names(script),
            )
            return script
        except Exception as e:
            _logger.exception("[MediaGenerator] AI script generation failed module=%s: %s", module.get("module_id"), e)
            if "not found" in str(e).lower():
                self.gemini_model = None
                _logger.warning("[MediaGenerator] Disabled Gemini model after NotFound; set GEMINI_MODEL to a valid value.")
            return self._manim_script_fallback(module, profile)
    
    def _manim_script_fallback(self, module: dict[str, Any], profile: Profile) -> str:
        """Fallback Manim script if AI generation fails."""
        objective = str(module.get("objective", "")).replace("\n", " ").strip()
        lines = [
            "from manim import *",
            "",
            "class LessonScene(Scene):",
            "    def construct(self):",
            "        self.camera.background_color = '#0B1021'",
            "        grid = NumberPlane(",
            "            x_range=[-8, 8, 1],",
            "            y_range=[-4.5, 4.5, 1],",
            "            x_length=14,",
            "            y_length=8,",
            "            background_line_style={'stroke_color': BLUE_E, 'stroke_opacity': 0.35, 'stroke_width': 1}",
            "        )",
            "        self.play(FadeIn(grid), run_time=0.8)",
            f"        title = Text({module['title']!r}, font_size=52, color=BLUE_B, weight=BOLD)",
            "        title.to_edge(UP)",
            "        underline = Line(title.get_left() + DOWN * 0.2, title.get_right() + DOWN * 0.2, color=YELLOW_B)",
            "        self.play(FadeIn(title, shift=UP * 0.2), Create(underline), run_time=1.2)",
        ]
        if objective:
            lines.extend(
                [
                    f"        objective = Text({objective[:120]!r}, font_size=26, color=GREY_A)",
                    "        objective.next_to(title, DOWN, buff=0.45)",
                    "        self.play(Write(objective), run_time=0.9)",
                    "        self.wait(0.6)",
                    "        self.play(FadeOut(objective), run_time=0.5)",
                ]
            )
        for i, step in enumerate(module["steps"], 1):
            step_title = str(step.get("title", f"Concept {i}")).replace("\n", " ").strip()
            instruction = str(step.get("instruction", "")).replace("\n", " ").strip()[:120]
            lines.extend(
                [
                    f"        step_title = Text({step_title!r}, font_size=34, color=BLUE_C).to_edge(UP)",
                    f"        content = Text({instruction!r}, font_size=25, color=GREY_A, line_spacing=0.9)",
                    "        content.next_to(step_title, DOWN, buff=0.5)",
                    "        frame = RoundedRectangle(corner_radius=0.18, width=12.2, height=2.3)",
                    "        frame.set_stroke(BLUE_D, width=2)",
                    "        frame.move_to(content)",
                    "        pulse = Dot(point=frame.get_left(), color=YELLOW_B).scale(0.7)",
                    "        self.play(FadeTransform(title.copy(), step_title), run_time=0.7)",
                    "        self.play(Create(frame), Write(content), FadeIn(pulse), run_time=1.1)",
                    "        self.play(pulse.animate.move_to(frame.get_right()), content.animate.set_color(YELLOW_A), run_time=0.8)",
                    "        self.wait(0.5)",
                    "        self.play(FadeOut(step_title), FadeOut(content), FadeOut(frame), FadeOut(pulse), run_time=0.6)",
                ]
            )
        lines.extend(
            [
                "        recap = Text('Recap: visualize the structure, then apply it.', font_size=30, color=YELLOW_B)",
                "        recap.to_edge(DOWN)",
                "        self.play(Write(recap), run_time=0.8)",
                "        self.wait(0.9)",
                "        self.play(FadeOut(recap), FadeOut(title), FadeOut(underline), FadeOut(grid), run_time=0.8)",
            ]
        )
        return "\n".join(lines) + "\n"

    def _short_manim_script_fallback(
        self,
        module: dict[str, Any],
        custom_prompt: str | None,
        target_duration_seconds: int,
    ) -> str:
        title = str(module.get("title", "Quick Concept")).replace("\n", " ").strip()[:48]
        objective = str(module.get("objective", "")).replace("\n", " ").strip()
        prompt_text = str(custom_prompt or "").replace("\n", " ").strip()
        core_line = (prompt_text or objective or title)[:72]
        hold_time = max(0.2, min(0.6, float(target_duration_seconds) - 1.4))

        lines = [
            "from manim import *",
            "",
            "class LessonScene(Scene):",
            "    def construct(self):",
            "        self.camera.background_color = '#0E1325'",
            "        badge = Circle(radius=1.2, color=BLUE_B, fill_opacity=0.2)",
            "        pulse = Dot(color=YELLOW_B).move_to(badge.get_center())",
            f"        title = Text({title!r}, font_size=36, color=BLUE_B, weight=BOLD).to_edge(UP)",
            f"        idea = Text({core_line!r}, font_size=24, color=GREY_A)",
            "        idea.next_to(badge, DOWN, buff=0.5)",
            "        self.play(FadeIn(title, shift=UP * 0.2), Create(badge), FadeIn(pulse), run_time=0.6)",
            "        self.play(pulse.animate.scale(1.5).set_color(YELLOW_A), run_time=0.4)",
            "        self.play(Write(idea), run_time=0.6)",
            f"        self.wait({hold_time:.2f})",
            "        self.play(FadeOut(VGroup(title, badge, pulse, idea)), run_time=0.4)",
            "",
        ]
        return "\n".join(lines)

    def _minimal_manim_script(
        self,
        module: dict[str, Any],
        custom_prompt: str | None,
    ) -> str:
        title = str(module.get("title", "Concept")).replace("\n", " ").strip()[:56]
        caption = str(custom_prompt or module.get("objective") or "Quick concept overview").replace("\n", " ").strip()[:74]
        lines = [
            "from manim import *",
            "",
            "class LessonScene(Scene):",
            "    def construct(self):",
            "        self.camera.background_color = '#0E1325'",
            f"        title = Text({title!r}, font_size=38, color=BLUE_B, weight=BOLD).to_edge(UP)",
            f"        caption = Text({caption!r}, font_size=24, color=GREY_A)",
            "        marker = Dot(color=YELLOW_B).scale(1.2)",
            "        ring = Circle(radius=0.9, color=BLUE_C)",
            "        self.play(FadeIn(title), FadeIn(marker), Create(ring), run_time=0.7)",
            "        self.play(Write(caption), marker.animate.shift(RIGHT * 1.2), run_time=0.7)",
            "        self.wait(0.4)",
            "        self.play(FadeOut(VGroup(title, caption, marker, ring)), run_time=0.4)",
            "",
        ]
        return "\n".join(lines)

    def _extract_scene_class_names(self, script: str) -> list[str]:
        class_pattern = re.compile(r"^class\s+([A-Za-z_][A-Za-z0-9_]*)\(([^)]*)\)\s*:", re.MULTILINE)
        scene_classes: list[str] = []
        for class_name, base_expr in class_pattern.findall(script):
            bases = [part.strip() for part in base_expr.split(",") if part.strip()]
            if any(base == "Scene" or base.endswith("Scene") for base in bases):
                scene_classes.append(class_name)
        return scene_classes

    def _sanitize_manim_script(self, script: str) -> str:
        """Normalize common LLM-generated Manim mistakes before rendering."""
        sanitized = script
        sanitized = re.sub(r"\.get_graph\s*\(", ".plot(", sanitized)
        sanitized = re.sub(r",\s*length\s*=\s*[A-Za-z_][A-Za-z0-9_\.]*", "", sanitized)
        for accessor in ("get_center", "get_left", "get_right", "get_top", "get_bottom", "get_start", "get_end"):
            sanitized = re.sub(
                rf"\.{accessor}(?!\s*\()",
                f".{accessor}()",
                sanitized,
            )
        if "np." in sanitized and "import numpy as np" not in sanitized:
            if "from manim import *" in sanitized:
                sanitized = sanitized.replace("from manim import *", "from manim import *\nimport numpy as np", 1)
            else:
                sanitized = f"import numpy as np\n{sanitized}"
        if not self.latex_available:
            sanitized = re.sub(r"\bMathTex\s*\(", "Text(", sanitized)
            sanitized = re.sub(r"\bTex\s*\(", "Text(", sanitized)
            sanitized = re.sub(r"\bTransformMatchingTex\s*\(", "TransformMatchingShapes(", sanitized)
        if sanitized != script:
            _logger.warning("[MediaGenerator] Sanitized generated script for runtime safety")
        return sanitized

    def _script_uses_latex(self, script: str) -> bool:
        return bool(re.search(r"\b(MathTex|Tex|TransformMatchingTex)\s*\(", script))
    
    def _build_manim_command(self, script_path: Path, scene_name: str) -> list[str]:
        manim_executable = shutil.which("manim")
        if manim_executable:
            return [manim_executable, "-ql", "--format=mp4", str(script_path), scene_name]
        return [sys.executable, "-m", "manim", "-ql", "--format=mp4", str(script_path), scene_name]

    def _render_manim_video(self, script: str, *, timeout_seconds: int = 60) -> bytes:
        """Render Manim script to video."""
        script = self._sanitize_manim_script(script)
        scene_classes = self._extract_scene_class_names(script)
        scene_name = scene_classes[0] if scene_classes else "LessonScene"
        if not scene_classes:
            _logger.warning("[MediaGenerator] No Scene subclass found in script; defaulting to LessonScene")

        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = Path(tmpdir) / "scene.py"
            script_path.write_text(script)
            command = self._build_manim_command(script_path, scene_name)
            _logger.debug(
                "[MediaGenerator] Running manim | scene=%s classes=%s cmd=%s cwd=%s",
                scene_name,
                scene_classes,
                command,
                tmpdir,
            )
            
            try:
                result = subprocess.run(
                    command,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds
                )

                stdout_tail = (result.stdout or "").strip()[-1200:]
                stderr_tail = (result.stderr or "").strip()[-1200:]
                _logger.debug(
                    "[MediaGenerator] Manim finished | returncode=%s scene=%s stdout_tail=%r stderr_tail=%r",
                    result.returncode,
                    scene_name,
                    stdout_tail,
                    stderr_tail,
                )
                
                video_path = Path(tmpdir) / "media" / "videos" / "scene" / "480p15" / f"{scene_name}.mp4"
                if video_path.exists():
                    if result.returncode != 0:
                        _logger.warning(
                            "[MediaGenerator] Using expected video output despite non-zero exit | scene=%s returncode=%s",
                            scene_name,
                            result.returncode,
                        )
                    return video_path.read_bytes()

                discovered_mp4s = sorted((Path(tmpdir) / "media" / "videos").rglob("*.mp4"))
                usable_mp4s = [path for path in discovered_mp4s if "partial_movie_files" not in str(path)]
                if usable_mp4s:
                    fallback_path = usable_mp4s[-1]
                    _logger.warning(
                        "[MediaGenerator] Expected video path missing; using discovered output file=%s all_candidates=%s",
                        fallback_path,
                        [str(path) for path in usable_mp4s],
                    )
                    return fallback_path.read_bytes()

                if result.returncode != 0:
                    raise Exception(
                        f"Manim exited with code {result.returncode}; stderr={stderr_tail or '<empty>'}"
                    )

                if discovered_mp4s:
                    fallback_path = discovered_mp4s[-1]
                    _logger.warning(
                        "[MediaGenerator] Only partial movie files exist; using last candidate=%s all_candidates=%s",
                        fallback_path,
                        [str(path) for path in discovered_mp4s],
                    )
                    return fallback_path.read_bytes()

                raise Exception(f"Video file not generated at expected path: {video_path}")
            except subprocess.TimeoutExpired:
                _logger.warning(
                    "[MediaGenerator] Manim rendering timeout | scene=%s timeout_seconds=%s",
                    scene_name,
                    timeout_seconds,
                )
                raise Exception("Manim rendering timeout")
            except Exception as e:
                _logger.warning("[MediaGenerator] Manim rendering failed | scene=%s error=%s", scene_name, e)
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
