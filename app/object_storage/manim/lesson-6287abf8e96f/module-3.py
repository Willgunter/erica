from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = YELLOW_D
        GREY_TEXT = GREY_B

        # --- Module Title ---
        module_title = Text("Applying the Quadratic Formula", font_size=50, color=WHITE).to_edge(UP)
        self.play(Write(module_title), run_time=1)
        self.wait(0.5)

        # --- Beat 1: The Problem - Visual Hook & Parabola ---
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GREY_TEXT},
            x_axis_config={"numbers_to_include": [-3, -1, 1, 3]},
            y_axis_config={"numbers_to_include": [-4, -2, 2, 4]}
        ).add_coordinates().shift(DOWN * 0.5)
        self.play(Create(axes), run_time=1.5)

        # Example parabola: y = x^2 - 2x - 3
        parabola = axes.plot(lambda x: x**2 - 2*x - 3, color=BLUE_ACCENT)
        
        # Labels and roots for the parabola
        parabola_eq_label = MathTex("y = x^2 - 2x - 3", color=BLUE_ACCENT).next_to(parabola, UP, buff=0.5).shift(LEFT * 1.5)
        
        root1_dot = Dot(axes.c2p(-1, 0), color=GOLD_ACCENT)
        root2_dot = Dot(axes.c2p(3, 0), color=GOLD_ACCENT)
        root_labels = VGroup(
            MathTex("x = -1", color=GOLD_ACCENT).next_to(root1_dot, DOWN),
            MathTex("x = 3", color=GOLD_ACCENT).next_to(root2_dot, DOWN)
        )

        question_text = Text(
            "Finding where a curve crosses the x-axis...",
            font_size=30, color=WHITE
        ).next_to(module_title, DOWN, buff=0.8)

        self.play(
            Create(parabola),
            FadeIn(parabola_eq_label, shift=UP),
            FadeIn(question_text, shift=UP),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            FadeIn(root1_dot, scale=0.5), FadeIn(root2_dot, scale=0.5),
            FadeIn(root_labels),
            LaggedStart(
                Flash(root1_dot, flash_radius=0.3, color=GOLD_ACCENT),
                Flash(root2_dot, flash_radius=0.3, color=GOLD_ACCENT),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.wait(1)

        # --- Beat 2: The Goal - From Graph to Equation ---
        self.play(FadeOut(parabola_eq_label, question_text, root_labels, root1_dot, root2_dot))

        general_eq_question = Text(
            "How do we find these solutions algebraically?",
            font_size=30, color=WHITE
        ).next_to(module_title, DOWN, buff=0.8)

        # Transform y=eq to eq=0, then introduce general form
        eq_example_y = MathTex("y = x^2 - 2x - 3", color=BLUE_ACCENT).move_to(ORIGIN + UP * 1.5)
        eq_example_zero = MathTex("x^2 - 2x - 3 = 0", color=BLUE_ACCENT).move_to(ORIGIN + UP * 1.5)
        general_form_eq = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT).next_to(eq_example_zero, DOWN, buff=0.8)
        
        # For coefficient mapping
        coeffs_example = VGroup(
            MathTex("a=1", color=BLUE_ACCENT),
            MathTex("b=-2", color=BLUE_ACCENT),
            MathTex("c=-3", color=BLUE_ACCENT)
        ).arrange(RIGHT, buff=0.5).next_to(general_form_eq, DOWN, buff=0.8)

        self.play(
            Transform(MathTex("y = x^2 - 2x - 3", color=BLUE_ACCENT).next_to(parabola, UP, buff=0.5).shift(LEFT * 1.5), eq_example_y), # Start from old label position
            Write(general_eq_question),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(TransformMatchingTex(eq_example_y, eq_example_zero), run_time=1.5)
        self.play(Write(general_form_eq), run_time=1.5)
        self.wait(0.5)

        self.play(
            LaggedStart(
                FadeIn(coeffs_example[0], shift=LEFT),
                FadeIn(coeffs_example[1], shift=LEFT),
                FadeIn(coeffs_example[2], shift=LEFT),
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.wait(1)

        # --- Beat 3: The Tool - The Quadratic Formula ---
        self.play(
            FadeOut(general_eq_question, coeffs_example),
            VGroup(eq_example_zero, general_form_eq).animate.shift(UP*1.5).set_opacity(0.5) # Dim and move up
        )

        formula_intro_text = Text(
            "The Quadratic Formula provides a direct solution!",
            font_size=30, color=WHITE
        ).next_to(module_title, DOWN, buff=0.8)

        quadratic_formula = MathTex(
            "x = ",
            "{-b \\pm \\sqrt{b^2 - 4ac}}",
            "\\over",
            "{2a}",
            color=GOLD_ACCENT, font_size=60
        ).move_to(ORIGIN)

        self.play(Write(formula_intro_text), run_time=1)
        self.play(
            LaggedStart(
                FadeIn(quadratic_formula[0], shift=LEFT),
                Create(quadratic_formula[1]),
                Create(quadratic_formula[2]),
                Create(quadratic_formula[3]),
                lag_ratio=0.5
            ),
            run_time=3
        )
        self.wait(1.5)

        # --- Beat 4: Intuition/Application - Connecting a, b, c ---
        self.play(FadeOut(formula_intro_text))

        application_text = Text(
            "It uses the coefficients 'a', 'b', and 'c' directly.",
            font_size=30, color=WHITE
        ).next_to(module_title, DOWN, buff=0.8)
        self.play(Write(application_text), run_time=1)

        # Create virtual mobjects to highlight corresponding parts
        a_general = general_form_eq.get_parts_by_tex("a")[0]
        b_general = general_form_eq.get_parts_by_tex("b")[0]
        c_general = general_form_eq.get_parts_by_tex("c")[0]

        a_formula = quadratic_formula.get_parts_by_tex("a")[0]
        b_formula_minus = quadratic_formula.get_parts_by_tex("-b")[0]
        b_formula_sq = quadratic_formula.get_parts_by_tex("b^2")[0]
        c_formula = quadratic_formula.get_parts_by_tex("c")[0]

        # Use arrows to show mapping
        arrow_a = Arrow(a_general.get_bottom(), a_formula.get_top(), color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.2)
        arrow_b1 = Arrow(b_general.get_bottom(), b_formula_minus.get_top(), color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.2)
        arrow_b2 = Arrow(b_general.get_bottom(), b_formula_sq.get_top(), color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.2)
        arrow_c = Arrow(c_general.get_bottom(), c_formula.get_top(), color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.2)
        
        self.play(
            Create(arrow_a), Create(arrow_b1), Create(arrow_b2), Create(arrow_c),
            run_time=2.5
        )
        self.wait(1)
        self.play(FadeOut(arrow_a, arrow_b1, arrow_b2, arrow_c, application_text))
        self.wait(1)

        # --- Beat 5: The Discriminant - Number of Solutions ---
        self.play(
            VGroup(eq_example_zero, general_form_eq).animate.set_opacity(0), # Fade out general equations
            quadratic_formula.animate.scale(0.8).to_edge(UP).shift(DOWN*0.5) # Move formula up for space
        )
        
        # Highlight the discriminant
        discriminant_part = quadratic_formula.get_parts_by_tex("b^2 - 4ac")[0]
        discriminant_highlight = SurroundingRectangle(discriminant_part, color=GOLD_ACCENT, buff=0.1)
        self.play(Create(discriminant_highlight, run_time=1))

        discriminant_text = Text(
            "The Discriminant (b² - 4ac) determines the number of solutions!",
            font_size=30, color=WHITE
        ).next_to(module_title, DOWN, buff=0.8)
        self.play(Write(discriminant_text), run_time=1.5)

        # Animate different discriminant cases visually
        parabola_base = parabola.copy().set_opacity(0.3) # Keep the original parabola as a faded reference
        self.play(FadeIn(parabola_base), run_time=0.5)

        # Case 1: > 0 (two real roots) - Our original parabola
        parabola_case1 = axes.plot(lambda x: x**2 - 2*x - 3, color=BLUE_ACCENT)
        roots_case1 = VGroup(Dot(axes.c2p(-1, 0), color=GOLD_ACCENT), Dot(axes.c2p(3, 0), color=GOLD_ACCENT))
        text_case1 = MathTex("b^2 - 4ac > 0", " \\implies ", "2 \\text{ Real Roots}", color=WHITE).scale(0.7).next_to(discriminant_highlight, DOWN, buff=0.8).align_to(axes, LEFT)

        self.play(Create(parabola_case1), FadeIn(roots_case1), Write(text_case1), run_time=2)
        self.wait(1)

        # Case 2: = 0 (one real root)
        parabola_case2 = axes.plot(lambda x: x**2 - 2*x + 1, color=BLUE_ACCENT) # (x-1)^2
        root_case2 = Dot(axes.c2p(1, 0), color=GOLD_ACCENT)
        text_case2 = MathTex("b^2 - 4ac = 0", " \\implies ", "1 \\text{ Real Root}", color=WHITE).scale(0.7).next_to(text_case1, DOWN, buff=0.4).align_to(axes, LEFT)

        self.play(
            ReplacementTransform(parabola_case1, parabola_case2),
            Transform(roots_case1, root_case2), # Transforms the group of two dots to one dot
            Write(text_case2),
            run_time=2
        )
        self.wait(1)

        # Case 3: < 0 (no real roots)
        parabola_case3 = axes.plot(lambda x: x**2 + 1, color=BLUE_ACCENT) # No x-intercepts
        text_case3 = MathTex("b^2 - 4ac < 0", " \\implies ", "0 \\text{ Real Roots}", color=WHITE).scale(0.7).next_to(text_case2, DOWN, buff=0.4).align_to(axes, LEFT)

        self.play(
            ReplacementTransform(parabola_case2, parabola_case3),
            FadeOut(roots_case1), # Fade out the single dot
            Write(text_case3),
            run_time=2
        )
        self.wait(2)

        # --- Recap Card ---
        self.play(
            FadeOut(
                axes, parabola_base, parabola_case3, discriminant_highlight,
                discriminant_text, text_case1, text_case2, text_case3,
                quadratic_formula, module_title
            )
        )

        recap_title = Text("Recap: The Quadratic Formula", font_size=45, color=GOLD_ACCENT).to_edge(UP)
        final_formula = MathTex(
            "x = ",
            "{-b \\pm \\sqrt{b^2 - 4ac}}",
            "\\over",
            "{2a}",
            color=BLUE_ACCENT, font_size=70
        ).move_to(ORIGIN)

        recap_summary = Text(
            "Solves for 'x' (roots) in any quadratic equation:",
            font_size=30, color=WHITE
        ).next_to(final_formula, UP, buff=1.0)
        general_form_recap = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT, font_size=40).next_to(recap_summary, DOWN, buff=0.2)

        self.play(
            Write(recap_title),
            FadeIn(recap_summary),
            FadeIn(general_form_recap),
            Write(final_formula),
            run_time=3
        )
        self.wait(3)