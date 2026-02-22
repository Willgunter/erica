from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        # High-contrast colors
        blue_accent = BLUE_C
        gold_accent = GOLD_C
        text_color = WHITE

        # --- Beat 1: The Parabola and its Roots (Visual Hook & Intuition) ---
        # Title appears early but not dominant
        title = Text("Solving with the Quadratic Formula", font_size=45, color=gold_accent).to_edge(UP * 0.8)
        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)

        # Create Axes, slightly shifted down
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 6, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": text_color, "stroke_width": 1.5},
            tips=False # Minimalist tips
        ).shift(DOWN * 0.5)
        # Labels for axes
        labels = axes.get_axis_labels(
            x_label=MathTex("x", color=text_color),
            y_label=MathTex("y", color=text_color)
        )
        self.play(Create(axes), Write(labels, run_time=0.8))
        self.wait(0.5)

        # Initial parabola (y = x^2 - 2x - 2), showing two distinct roots
        parabola_initial = axes.get_graph(lambda x: x**2 - 2*x - 2, color=blue_accent)
        parabola_label = MathTex("y = ax^2 + bx + c", color=blue_accent, font_size=38).next_to(parabola_initial, UP + RIGHT, buff=0.5).shift(RIGHT*0.5)
        
        self.play(Create(parabola_initial))
        self.play(Write(parabola_label))

        # Highlight the roots (x-intercepts)
        root1_dot = Dot(axes.c2p(-0.732, 0), color=gold_accent, radius=0.1)
        root2_dot = Dot(axes.c2p(2.732, 0), color=gold_accent, radius=0.1)
        
        # Text explaining what roots are
        solutions_text = Text("Find x when y = 0", color=gold_accent, font_size=32).next_to(root2_dot, RIGHT, buff=0.5)
        solution_arrow = Arrow(solutions_text.get_left(), root2_dot.get_right(), color=gold_accent, buff=0.1)

        self.play(FadeIn(root1_dot, root2_dot))
        self.play(Write(solutions_text), Create(solution_arrow))
        self.wait(1.5)

        # Illustrate discriminant visually: 1 root, then 0 roots
        parabola_one_root = axes.get_graph(lambda x: x**2 - 2*x + 1, color=blue_accent) # (x-1)^2, root at x=1
        parabola_no_roots = axes.get_graph(lambda x: x**2 - 2*x + 3, color=blue_accent) # No real roots

        single_root_dot = Dot(axes.c2p(1, 0), color=gold_accent, radius=0.1)

        self.play(
            ReplacementTransform(parabola_initial, parabola_one_root),
            FadeOut(root1_dot, root2_dot, solutions_text, solution_arrow)
        )
        self.play(FadeIn(single_root_dot))
        self.wait(0.8)
        self.play(
            ReplacementTransform(parabola_one_root, parabola_no_roots),
            FadeOut(single_root_dot)
        )
        self.wait(1)
        
        # Clean up for next beat
        self.play(FadeOut(parabola_no_roots, parabola_label, axes, labels))

        # --- Beat 2: The General Form & The Problem ---
        # The standard quadratic equation
        eq_general = MathTex("ax^2 + bx + c = 0", color=text_color).scale(1.2)
        self.play(Write(eq_general))
        self.wait(1)

        # Highlight a, b, c
        a_highlight = MathTex("a", color=blue_accent).move_to(eq_general[0])
        b_highlight = MathTex("b", color=gold_accent).move_to(eq_general[2])
        c_highlight = MathTex("c", color=blue_accent).move_to(eq_general[4])

        self.play(
            FadeTransform(eq_general[0].copy(), a_highlight),
            FadeTransform(eq_general[2].copy(), b_highlight),
            FadeTransform(eq_general[4].copy(), c_highlight)
        )
        self.wait(1)
        
        problem_text = Text("How to find 'x' consistently?", font_size=38, color=gold_accent).next_to(eq_general, DOWN, buff=1)
        self.play(FadeIn(problem_text, shift=DOWN))
        self.wait(1.5)
        self.play(FadeOut(a_highlight, b_highlight, c_highlight, problem_text))

        # --- Beat 3: The Universal Tool - Quadratic Formula ---
        # Introduce the quadratic formula
        formula_tex = MathTex(
            "x = ",
            "{-b \\pm \\sqrt{b^2 - 4ac}}",
            "\\over",
            "{2a}",
            color=gold_accent
        ).scale(1.5).move_to(eq_general) # Replaces general equation

        universal_text = Text("A Universal Solution!", font_size=40, color=blue_accent).next_to(formula_tex, DOWN, buff=0.8)

        self.play(
            ReplacementTransform(eq_general, formula_tex)
        )
        self.play(Write(universal_text))
        self.wait(1.5)

        # Shrink and move the formula and the original equation for mapping
        eq_general_copy = MathTex("ax^2 + bx + c = 0", color=text_color).scale(0.8).to_edge(UP + LEFT).shift(RIGHT*0.5)
        self.play(
            FadeTransform(title, eq_general_copy), # Repurpose title space
            formula_tex.animate.scale(0.8).to_edge(RIGHT).shift(LEFT*0.5),
            FadeOut(universal_text)
        )

        # Show mapping from a,b,c in equation to formula
        a_map = Arrow(eq_general_copy[0].get_top(), formula_tex[3][1].get_bottom(), color=blue_accent, buff=0.1, max_stroke_width_to_length_ratio=0.08)
        b_map1 = Arrow(eq_general_copy[2].get_top(), formula_tex[1][1].get_bottom(), color=gold_accent, buff=0.1, max_stroke_width_to_length_ratio=0.08)
        b_map2 = Arrow(eq_general_copy[2].get_bottom(), formula_tex[1][4].get_top(), color=gold_accent, buff=0.1, max_stroke_width_to_length_ratio=0.08)
        c_map = Arrow(eq_general_copy[4].get_top(), formula_tex[1][6].get_bottom(), color=blue_accent, buff=0.1, max_stroke_width_to_length_ratio=0.08)

        self.play(
            LaggedStart(
                GrowArrow(a_map),
                GrowArrow(b_map1),
                GrowArrow(b_map2),
                GrowArrow(c_map),
                lag_ratio=0.2, run_time=2
            )
        )
        self.wait(1.5)
        self.play(FadeOut(a_map, b_map1, b_map2, c_map))

        # --- Beat 4: Applying the Formula (Conceptual) ---
        example_eq = MathTex("2x^2 + 5x - 3 = 0", color=text_color).scale(0.9).next_to(eq_general_copy, DOWN, buff=0.5).align_to(eq_general_copy, LEFT)
        self.play(Write(example_eq))

        # Label a, b, c values
        a_val_text = MathTex("a=2", color=blue_accent).next_to(example_eq, LEFT, buff=1).shift(DOWN*0.2)
        b_val_text = MathTex("b=5", color=gold_accent).next_to(a_val_text, DOWN, buff=0.3)
        c_val_text = MathTex("c=-3", color=blue_accent).next_to(b_val_text, DOWN, buff=0.3)

        self.play(
            Indicate(example_eq[0], color=blue_accent), Write(a_val_text), run_time=0.7
        )
        self.play(
            Indicate(example_eq[2], color=gold_accent), Write(b_val_text), run_time=0.7
        )
        self.play(
            Indicate(example_eq[4], color=blue_accent), Write(c_val_text), run_time=0.7
        )
        self.wait(1)

        # Show the formula with a,b,c placeholders
        formula_placeholders = MathTex(
            "x = ",
            "{-(\\color{gold_accent}b) \\pm \\sqrt{(\\color{gold_accent}b)^2 - 4(\\color{blue_accent}a)(\\color{blue_accent}c)}}",
            "\\over",
            "{2(\\color{blue_accent}a)}",
        ).scale(0.8).move_to(formula_tex) # Replaces the general formula
        self.play(ReplacementTransform(formula_tex, formula_placeholders))
        self.wait(1)

        # Emphasize the ± for two solutions
        plus_minus_symbol = formula_placeholders[1][3] # This is the "±" symbol
        self.play(
            Wiggle(plus_minus_symbol, scale_factor=1.3),
            run_time=1
        )
        two_solutions_explanation = Text("Remember: Two paths, two solutions!", color=gold_accent, font_size=32).next_to(formula_placeholders, DOWN, buff=0.8)
        self.play(Write(two_solutions_explanation))
        self.wait(1.5)

        # Clean up for recap
        self.play(FadeOut(example_eq, a_val_text, b_val_text, c_val_text, eq_general_copy, formula_placeholders, two_solutions_explanation))

        # --- Beat 5: Recap & Call to Action (Implicit) ---
        recap_card = Rectangle(
            width=config.frame_width * 0.8,
            height=config.frame_height * 0.7,
            color=blue_accent,
            fill_opacity=0.1,
            stroke_width=3
        ).center()
        self.play(FadeIn(recap_card))

        recap_title = Text("Recap: Quadratic Formula", font_size=45, color=gold_accent).next_to(recap_card.get_top(), DOWN, buff=0.5)
        self.play(Write(recap_title))

        summary_points_text = [
            "A universal tool for ANY quadratic equation.",
            "Finds the 'x' values where the parabola crosses the x-axis (y=0).",
            "Identify 'a', 'b', and 'c' from ax² + bx + c = 0.",
            "Substitute values into the formula: x = (-b ± sqrt(b² - 4ac)) / (2a)."
        ]
        
        summary_points_mobjects = VGroup()
        for point_text in summary_points_text:
            bullet = BulletPoint("•").scale(0.8).set_color(text_color)
            text = Text(point_text, font_size=30, color=text_color)
            summary_points_mobjects.add(VGroup(bullet, text).arrange(RIGHT, buff=0.3, aligned_edge=UP))

        summary_points_mobjects.arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(recap_title, DOWN, buff=0.7).align_to(recap_card.get_left(), LEFT).shift(RIGHT*1.2)
        
        # Animate points one by one
        self.play(LaggedStart(*[FadeIn(point, shift=LEFT * 0.2) for point in summary_points_mobjects], lag_ratio=0.5, run_time=3.5))
        self.wait(2)

        final_formula_display = MathTex(
            "x = ",
            "{-b \\pm \\sqrt{b^2 - 4ac}}",
            "\\over",
            "{2a}",
            color=gold_accent
        ).scale(1.2).next_to(recap_card.get_bottom(), UP, buff=0.5)
        self.play(FadeIn(final_formula_display, shift=UP))
        self.wait(3)

        self.play(FadeOut(recap_card, recap_title, summary_points_mobjects, final_formula_display))
        self.wait(1)