from manim import *

class LessonScene(Scene):
    def construct(self):
        title = Text('Module 1: Variables and data types.')
        self.play(Write(title))
        self.wait(0.5)
        step_text = Text('Variables and data types. Control flow and loops.')
        self.play(Transform(title, step_text))
        self.wait(0.5)
        step_text = Text('Follow a guided example using this idea: Variables and data types. Control flow ')
        self.play(Transform(title, step_text))
        self.wait(0.5)
        step_text = Text('Create a short solution that applies: Variables and data types. Control flow and')
        self.play(Transform(title, step_text))
        self.wait(0.5)
        checkpoint = Text('Checkpoint for u-2')
        self.play(FadeIn(checkpoint))
        self.wait(0.5)
