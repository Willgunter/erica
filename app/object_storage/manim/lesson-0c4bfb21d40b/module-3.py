from manim import *

class DiscriminantAnimation(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = "#1A1A1A"  # Dark grey/black background
        self.BLUE = "#87CEEB"  # Sky Blue for accents
        self.GOLD = "#FFD700"  # Gold for key elements
        self.GREY_BROWN = "#8D806D" # For axes

    def construct(self):
        # 1. Module Title Introduction
        title = Text("The Discriminant", font_size=72, color=self.GOLD)
        subtitle = Text("Nature of Quadratic Solutions", font_size=48, color=self.BLUE).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        self.play(FadeOut(title, subtitle))
        self.wait(0.5)

        # 2. Visual Hook: Parabola and its roots changing
        axes_hook = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 4, 1],
            x_length=8, y_length=6,
            axis_config={"color": self.GREY_BROWN},
            y_axis_config={"numbers_to_exclude": [0]} # Don't label 0 on y-axis for cleaner look
        ).scale(0.8).to_edge(LEFT).shift(RIGHT*0.5)

        labels_hook = axes_hook.get_axis_labels(x_label="x", y_label="f(x)")
        self.play(Create(axes_hook), Create(labels_hook), run_time=1)

        # Case: 2 Real Roots
        func1 = lambda x: 0.5 * x**2 - 1.5
        graph1 = axes_hook.plot(func1, color=self.BLUE)
        dots1 = VGroup(*[Dot(axes_hook.coords_to_point(r, 0), color=self.GOLD, radius=0.1) for r in [-np.sqrt(3), np.sqrt(3)]])
        text_2_roots = MathTex("2 \\text{ Real Roots}", color=self.BLUE, font_size=40).next_to(axes_hook, RIGHT).shift(UP*0.5)
        
        self.play(Create(graph1), run_time=1)
        self.play(Create(dots1), Write(text_2_roots), run_time=0.7)
        self.wait(1)

        # Case: 1 Real Root
        func2 = lambda x: 0.5 * x**2
        graph2 = axes_hook.plot(func2, color=self.BLUE)
        dots2 = Dot(axes_hook.coords_to_point(0, 0), color=self.GOLD, radius=0.1)
        text_1_root = MathTex("1 \\text{ Real Root}", color=self.BLUE, font_size=40).move_to(text_2_roots.get_center())
        
        self.play(
            Transform(graph1, graph2),
            FadeOut(dots1),
            ReplacementTransform(text_2_roots, text_1_root),
            run_time=1.5
        )
        self.play(Create(dots2), run_time=0.7)
        self.wait(1)

        # Case: 0 Real Roots
        func3 = lambda x: 0.5 * x**2 + 1.5
        graph3 = axes_hook.plot(func3, color=self.BLUE)
        text_0_roots = MathTex("0 \\text{ Real Roots}", color=self.BLUE, font_size=40).move_to(text_1_root.get_center())
        
        self.play(
            Transform(graph1, graph3), # graph1 is now graph2, transforming to graph3
            FadeOut(dots2),
            ReplacementTransform(text_1_root, text_0_roots),
            run_time=1.5
        )
        self.wait(1)

        self.play(FadeOut(axes_hook, labels_hook, graph1, text_0_roots))
        self.wait(0.5) # End of Beat 1 (Visual Hook)

        # 3. Introduce Quadratic Formula & Discriminant
        quad_eq = MathTex("ax^2 + bx + c = 0", color=self.GOLD, font_size=60).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(quad_eq), run_time=1.5)
        self.wait(1)

        quad_formula_tex = MathTex(
            "x = ", "\\frac{-b \\pm \\sqrt{", "b^2 - 4ac", "}}{2a}", font_size=50
        ).move_to(quad_eq.get_center())
        
        self.play(
            ReplacementTransform(quad_eq, quad_formula_tex),
            run_time=1.5
        )
        self.wait(1)

        # Highlight and extract the discriminant
        discriminant_expr_in_formula = quad_formula_tex.get_parts_by_tex("b^2 - 4ac")[0]
        
        discriminant_label = MathTex("\\Delta = ", "b^2 - 4ac", color=self.GOLD, font_size=60).next_to(quad_formula_tex, DOWN, buff=1.0)
        discriminant_label_expr = discriminant_label.get_parts_by_tex("b^2 - 4ac")[0]
        discriminant_label_delta = discriminant_label.get_parts_by_tex("\\Delta = ")[0]

        self.play(
            FadeIn(discriminant_label_delta, shift=UP),
            ReplacementTransform(discriminant_expr_in_formula.copy(), discriminant_label_expr),
            run_time=1.5
        )
        self.wait(1.5)
        
        self.play(FadeOut(quad_formula_tex))
        self.play(discriminant_label.animate.to_edge(UP).shift(DOWN*0.5))
        self.wait(0.5) # End of Beat 2 (Discriminant Introduction)

        # Common Axes for graphs in the next beats
        common_axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 4, 1],
            x_length=7, y_length=5,
            axis_config={"color": self.GREY_BROWN},
            y_axis_config={"numbers_to_exclude": [0]}
        ).scale(0.8).to_corner(DR).shift(LEFT*0.5+UP*0.5)
        common_labels = common_axes.get_axis_labels(x_label="x", y_label="y")

        # 4. Case 1: Delta > 0 (Two Real Roots)
        delta_greater_zero = MathTex("\\Delta > 0", color=self.GOLD, font_size=60).next_to(discriminant_label, DOWN, buff=1.0)
        self.play(FadeIn(delta_greater_zero, shift=UP))

        example_eq1 = MathTex("x^2 - 4x + 3 = 0", color=self.BLUE, font_size=40).next_to(delta_greater_zero, DOWN, buff=0.7)
        self.play(Write(example_eq1))

        calc_delta1 = MathTex(
            "\\Delta = (-4)^2 - 4(1)(3) = 16 - 12 = 4", color=self.BLUE, font_size=40
        ).next_to(example_eq1, DOWN, buff=0.5)
        self.play(Write(calc_delta1), run_time=1.5)
        
        root_result1 = MathTex("\\sqrt{4} = 2", color=self.GOLD, font_size=40).next_to(calc_delta1, DOWN, buff=0.5)
        self.play(Write(root_result1), run_time=0.8)
        self.wait(1)
        
        self.play(Create(common_axes), Create(common_labels), run_time=0.8)
        self.play(FadeOut(delta_greater_zero, example_eq1, calc_delta1, root_result1), run_time=0.5)

        func_pos = lambda x: x**2 - 4*x + 3
        graph_pos = common_axes.plot(func_pos, color=self.BLUE)
        roots_pos = VGroup(
            Dot(common_axes.coords_to_point(1, 0), color=self.GOLD, radius=0.1),
            Dot(common_axes.coords_to_point(3, 0), color=self.GOLD, radius=0.1)
        )
        result_text1 = MathTex("2 \\text{ Real, Distinct Roots}", color=self.BLUE, font_size=45).next_to(common_axes, UP, buff=0.5)
        
        self.play(Create(graph_pos), run_time=1)
        self.play(Create(roots_pos), Write(result_text1), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(common_axes, common_labels, graph_pos, roots_pos, result_text1))
        self.wait(0.5) # End of Beat 3

        # 5. Case 2: Delta = 0 (One Real Root)
        delta_equal_zero = MathTex("\\Delta = 0", color=self.GOLD, font_size=60).next_to(discriminant_label, DOWN, buff=1.0)
        self.play(FadeIn(delta_equal_zero, shift=UP))

        example_eq2 = MathTex("x^2 - 4x + 4 = 0", color=self.BLUE, font_size=40).next_to(delta_equal_zero, DOWN, buff=0.7)
        self.play(Write(example_eq2))

        calc_delta2 = MathTex(
            "\\Delta = (-4)^2 - 4(1)(4) = 16 - 16 = 0", color=self.BLUE, font_size=40
        ).next_to(example_eq2, DOWN, buff=0.5)
        self.play(Write(calc_delta2), run_time=1.5)
        
        root_result2 = MathTex("\\sqrt{0} = 0", color=self.GOLD, font_size=40).next_to(calc_delta2, DOWN, buff=0.5)
        self.play(Write(root_result2), run_time=0.8)
        self.wait(1)

        self.play(Create(common_axes), Create(common_labels), run_time=0.8)
        self.play(FadeOut(delta_equal_zero, example_eq2, calc_delta2, root_result2), run_time=0.5)

        func_zero = lambda x: x**2 - 4*x + 4
        graph_zero = common_axes.plot(func_zero, color=self.BLUE)
        roots_zero = Dot(common_axes.coords_to_point(2, 0), color=self.GOLD, radius=0.1)
        result_text2 = MathTex("1 \\text{ Real, Repeated Root}", color=self.BLUE, font_size=45).next_to(common_axes, UP, buff=0.5)
        
        self.play(Create(graph_zero), run_time=1)
        self.play(Create(roots_zero), Write(result_text2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(common_axes, common_labels, graph_zero, roots_zero, result_text2))
        self.wait(0.5) # End of Beat 4

        # 6. Case 3: Delta < 0 (No Real Roots / Complex Roots)
        delta_less_zero = MathTex("\\Delta < 0", color=self.GOLD, font_size=60).next_to(discriminant_label, DOWN, buff=1.0)
        self.play(FadeIn(delta_less_zero, shift=UP))

        example_eq3 = MathTex("x^2 - 4x + 5 = 0", color=self.BLUE, font_size=40).next_to(delta_less_zero, DOWN, buff=0.7)
        self.play(Write(example_eq3))

        calc_delta3 = MathTex(
            "\\Delta = (-4)^2 - 4(1)(5) = 16 - 20 = -4", color=self.BLUE, font_size=40
        ).next_to(example_eq3, DOWN, buff=0.5)
        self.play(Write(calc_delta3), run_time=1.5)
        
        root_result3 = MathTex("\\sqrt{-4} = 2i", color=self.GOLD, font_size=40).next_to(calc_delta3, DOWN, buff=0.5)
        self.play(Write(root_result3), run_time=0.8)
        self.wait(1)

        self.play(Create(common_axes), Create(common_labels), run_time=0.8)
        self.play(FadeOut(delta_less_zero, example_eq3, calc_delta3, root_result3), run_time=0.5)

        func_neg = lambda x: x**2 - 4*x + 5
        graph_neg = common_axes.plot(func_neg, color=self.BLUE)
        result_text3 = MathTex("2 \\text{ Complex Roots}", color=self.BLUE, font_size=45).next_to(common_axes, UP, buff=0.5)
        result_text3_alt = MathTex("(\\text{No Real Roots})", color=self.GREY_BROWN, font_size=36).next_to(result_text3, DOWN, buff=0.1)
        
        self.play(Create(graph_neg), run_time=1)
        self.play(Write(result_text3), Write(result_text3_alt), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(common_axes, common_labels, graph_neg, result_text3, result_text3_alt))
        self.wait(0.5) # End of Beat 5

        # 7. Recap Card
        self.play(FadeOut(discriminant_label))

        recap_title = Text("Recap: The Discriminant", font_size=60, color=self.GOLD).to_edge(UP)
        self.play(Write(recap_title), run_time=1)

        case1 = MathTex("\\Delta > 0", " \\implies ", "2 \\text{ Real, Distinct Roots}", color=self.BLUE, font_size=48)
        case2 = MathTex("\\Delta = 0", " \\implies ", "1 \\text{ Real, Repeated Root}", color=self.BLUE, font_size=48)
        case3 = MathTex("\\Delta < 0", " \\implies ", "2 \\text{ Complex Roots}", color=self.BLUE, font_size=48)

        recap_group = VGroup(case1, case2, case3).arrange(DOWN, buff=0.7).center()
        
        # Highlight delta values in gold
        case1.get_parts_by_tex("\\Delta > 0")[0].set_color(self.GOLD)
        case2.get_parts_by_tex("\\Delta = 0")[0].set_color(self.GOLD)
        case3.get_parts_by_tex("\\Delta < 0")[0].set_color(self.GOLD)

        self.play(LaggedStart(
            FadeIn(recap_group[0], shift=UP),
            FadeIn(recap_group[1], shift=UP),
            FadeIn(recap_group[2], shift=UP),
            lag_ratio=0.7,
            run_time=2
        ))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_group))
        self.wait(1)