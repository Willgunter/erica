from __future__ import annotations

import unittest
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from unittest.mock import patch

from app.lesson_engine.media import MediaGenerator
from app.lesson_engine.storage import LocalObjectStorage


class MediaSanitizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp_storage_dir = mkdtemp(prefix="media-sanitize-test-")
        storage = LocalObjectStorage(self._tmp_storage_dir)
        self.generator = MediaGenerator(storage=storage)
        self.generator.latex_available = False

    def tearDown(self) -> None:
        rmtree(self._tmp_storage_dir, ignore_errors=True)

    def test_rewrites_get_graph_and_strips_horizontal_line_length(self) -> None:
        script = """from manim import *

class Demo(Scene):
    def construct(self):
        axes = Axes()
        parabola = axes.get_graph(lambda x: x**2, color=BLUE)
        helper = axes.get_horizontal_line(axes.c2p(0, 2), color=BLUE, length=axes.x_length)
"""
        sanitized = self.generator._sanitize_manim_script(script)
        self.assertIn(".plot(", sanitized)
        self.assertNotIn(".get_graph(", sanitized)
        self.assertNotIn("length=", sanitized)

    def test_injects_numpy_import_for_np_usage(self) -> None:
        script = """from manim import *

class Demo(Scene):
    def construct(self):
        value = np.sqrt(2)
        self.wait(value / 10)
"""
        sanitized = self.generator._sanitize_manim_script(script)
        self.assertIn("import numpy as np", sanitized)

    def test_replaces_tex_variants_when_latex_missing(self) -> None:
        script = """from manim import *

class Demo(Scene):
    def construct(self):
        a = Tex("x")
        b = MathTex("y")
        self.play(TransformMatchingTex(a, b))
"""
        sanitized = self.generator._sanitize_manim_script(script)
        self.assertNotIn("Tex(", sanitized)
        self.assertNotIn("MathTex(", sanitized)
        self.assertNotIn("TransformMatchingTex(", sanitized)
        self.assertIn("TransformMatchingShapes(", sanitized)

    def test_build_manim_command_prefers_binary_then_python_module(self) -> None:
        script_path = Path("/tmp/scene.py")
        with patch("app.lesson_engine.media.shutil.which", return_value="/usr/local/bin/manim"):
            command = self.generator._build_manim_command(script_path, "LessonScene")
            self.assertEqual(command[0], "/usr/local/bin/manim")

        with patch("app.lesson_engine.media.shutil.which", return_value=None), patch(
            "app.lesson_engine.media.sys.executable",
            "/usr/bin/python3",
        ):
            command = self.generator._build_manim_command(script_path, "LessonScene")
            self.assertEqual(command[0:3], ["/usr/bin/python3", "-m", "manim"])


if __name__ == "__main__":
    unittest.main()
