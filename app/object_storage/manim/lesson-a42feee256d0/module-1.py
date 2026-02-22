from manim import *

class LessonScene(Scene):
    def construct(self):
        title = Text('Module 1: Variables store values.')
        self.play(Write(title))
        self.wait(0.5)
        step_text = Text('Variables store values. Loops repeat work.')
        self.play(Transform(title, step_text))
        self.wait(0.5)
        step_text = Text('Follow a guided example using this idea: Variables store values. Loops repeat wo')
        self.play(Transform(title, step_text))
        self.wait(0.5)
        step_text = Text('Create a short solution that applies: Variables store values. Loops repeat work.')
        self.play(Transform(title, step_text))
        self.wait(0.5)
        checkpoint = Text('Checkpoint for u1')
        self.play(FadeIn(checkpoint))
        self.wait(0.5)
