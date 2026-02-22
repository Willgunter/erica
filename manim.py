from manim import *


class QuadraticFormulaLesson(Scene):
    def construct(self):
        self.show_intro()
        self.show_derivation()
        self.show_graph_connection()
        self.show_discriminant_summary()
        self.show_outro()

    def show_intro(self):
        title = Text("Quadratic Formula", weight=BOLD).scale(1.0)
        subtitle = Text(
            "Derive it by completing the square, then connect it to the graph."
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.2)

        formula = Text("x = (-b +/- sqrt(b^2 - 4ac)) / (2a)", color=YELLOW).scale(0.56)
        formula.next_to(subtitle, DOWN, buff=0.45)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.play(Write(formula))
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, subtitle, formula)))

    def show_derivation(self):
        header = Text("1) Completing the Square Derivation", weight=BOLD).scale(0.5)
        header.to_edge(UP)

        steps = [
            Text("a*x^2 + b*x + c = 0,   a != 0", font="Menlo"),
            Text("x^2 + (b/a)*x + c/a = 0", font="Menlo"),
            Text("x^2 + (b/a)*x = -c/a", font="Menlo"),
            Text(
                "x^2 + (b/a)*x + (b/2a)^2 = -c/a + (b/2a)^2",
                font="Menlo",
            ),
            Text("(x + b/2a)^2 = (b^2 - 4ac) / (4a^2)", font="Menlo"),
            Text("x + b/2a = +/- sqrt(b^2 - 4ac) / (2a)", font="Menlo"),
            Text("x = (-b +/- sqrt(b^2 - 4ac)) / (2a)", color=YELLOW, font="Menlo"),
        ]
        for step in steps:
            step.scale(0.52).next_to(header, DOWN, buff=1.1)

        captions = [
            "Start with the general quadratic equation.",
            "Divide every term by a so the x^2 coefficient is 1.",
            "Move the constant to the right side.",
            "Add (b/2a)^2 to both sides to complete the square.",
            "Left side becomes a perfect square binomial.",
            "Take square roots on both sides.",
            "Solve for x: this is the quadratic formula.",
        ]

        caption = Text(captions[0]).scale(0.38).to_edge(DOWN)
        current_step = steps[0]

        self.play(FadeIn(header), Write(current_step))
        self.play(FadeIn(caption, shift=UP * 0.2))
        self.wait(0.6)

        for idx in range(1, len(steps)):
            next_caption = Text(captions[idx]).scale(0.38).to_edge(DOWN)
            self.play(
                ReplacementTransform(current_step, steps[idx]),
                FadeTransform(caption, next_caption),
                run_time=1.6,
            )
            self.wait(0.3)
            current_step = steps[idx]
            caption = next_caption

        self.wait(1.0)
        self.play(FadeOut(VGroup(header, current_step, caption)))

    def show_graph_connection(self):
        header = Text("2) Graph Connection", weight=BOLD).scale(0.56).to_edge(UP)

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 6, 1],
            x_length=6.2,
            y_length=4.8,
            axis_config={
                "include_numbers": True,
                "font_size": 24,
                "label_constructor": Text,
            },
        )
        axes_labels = axes.get_axis_labels(Text("x").scale(0.45), Text("y").scale(0.45))
        parabola = axes.plot(lambda x: x**2 - 4 * x + 3, color=BLUE, x_range=[-0.5, 4.5])

        graph_group = VGroup(axes, axes_labels, parabola).scale(0.9).to_edge(LEFT, buff=0.5)

        eq1 = Text("y = x^2 - 4x + 3", font="Menlo").scale(0.55)
        eq2 = Text("a = 1,  b = -4,  c = 3", font="Menlo").scale(0.5)
        eq3 = Text("x = (4 +/- sqrt(16 - 12)) / 2", font="Menlo").scale(0.5)
        eq4 = Text("x = (4 +/- 2) / 2", font="Menlo").scale(0.5)
        eq5 = Text("x = 1 and x = 3", color=YELLOW, font="Menlo").scale(0.58)
        equation_group = VGroup(eq1, eq2, eq3, eq4, eq5).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        )
        equation_group.to_edge(RIGHT, buff=0.4).shift(UP * 0.1)

        root1 = Dot(axes.c2p(1, 0), color=YELLOW)
        root2 = Dot(axes.c2p(3, 0), color=YELLOW)
        root1_label = Text("(1,0)", font="Menlo").scale(0.36).next_to(root1, DOWN)
        root2_label = Text("(3,0)", font="Menlo").scale(0.36).next_to(root2, DOWN)

        vertex = Dot(axes.c2p(2, -1), color=GREEN)
        vertex_label = Text("vertex (2,-1)", color=GREEN, font="Menlo").scale(0.35)
        vertex_label.next_to(vertex, LEFT)

        self.play(FadeIn(header))
        self.play(Create(axes), FadeIn(axes_labels), run_time=1.4)
        self.play(Create(parabola), run_time=1.8)
        self.play(FadeIn(eq1), FadeIn(eq2))
        self.play(Write(eq3))
        self.play(Write(eq4))
        self.play(FadeIn(eq5))
        self.play(
            FadeIn(root1),
            FadeIn(root2),
            FadeIn(root1_label),
            FadeIn(root2_label),
            run_time=1.0,
        )
        self.play(FadeIn(vertex), FadeIn(vertex_label), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, graph_group, equation_group, root1, root2, root1_label, root2_label, vertex, vertex_label)))

    def show_discriminant_summary(self):
        header = Text("3) What the Discriminant Tells You", weight=BOLD).scale(0.54)
        header.to_edge(UP)

        disc = Text("D = b^2 - 4ac", color=YELLOW, font="Menlo").scale(0.7)
        disc.next_to(header, DOWN, buff=0.5)

        line1 = Text("D > 0: two distinct real roots (graph crosses twice)").scale(0.44)
        line2 = Text("D = 0: one repeated real root (touches once)").scale(0.44)
        line3 = Text("D < 0: no real roots (does not touch x-axis)").scale(0.44)
        lines = VGroup(line1, line2, line3).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        lines.next_to(disc, DOWN, buff=0.45)

        self.play(FadeIn(header))
        self.play(Write(disc))
        self.play(LaggedStart(*(FadeIn(line, shift=UP * 0.2) for line in lines), lag_ratio=0.2))
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, disc, lines)))

    def show_outro(self):
        line1 = Text("Quadratic formula = completing the square + algebra.", weight=BOLD).scale(0.56)
        line2 = Text("Its roots are exactly the x-intercepts of the parabola.").scale(0.48)
        line2.next_to(line1, DOWN, buff=0.22)

        self.play(FadeIn(line1, shift=UP * 0.3))
        self.play(FadeIn(line2, shift=UP * 0.2))
        self.wait(1.4)
