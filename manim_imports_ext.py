"""Minimal compatibility layer for legacy 3Blue1Brown-style Manim scripts."""

from manim import *

import itertools as it
import numpy as np
import random


# Legacy aliases used by old scripts
OldTex = Tex
OldTexText = Tex
FRAME_X_RADIUS = config.frame_width / 2
FRAME_Y_RADIUS = config.frame_height / 2


class PiCreatureScene(Scene):
    pass


class TeacherStudentsScene(PiCreatureScene):
    pass


class PiCreature(VGroup):
    pass


class PatreonEndScreen(Scene):
    pass


class VideoWrapper(Scene):
    pass
