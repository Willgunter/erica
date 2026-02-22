from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#1a1a1a" # Very dark gray
        BLUE_ACCENT = "#54A0FF" # A vibrant blue
        GOLD_ACCENT = "#FFD700" # Gold

        # --- Beat 1: The Problem (Visual Hook & Introduction) ---
        title = Text("Deriving the Quadratic Formula", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Show a parabola and its roots
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 6, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": BLUE_ACCENT, "include_numbers": False, "font_size": 20},
            tips=False
        ).shift(DOWN * 0.5)
        
        # Parabola with visible roots
        parabola_func = lambda x: 0.7 * (x - 1.5) * (x + 2.5) # Example roots at 1.5 and -2.5
        parabola_curve = axes.get_graph(parabola_func, x_range=[-3, 2], color=BLUE_ACCENT)
        parabola_label = MathTex("y = ax^2 + bx + c", color=GOLD_ACCENT, font_size=30).next_to(parabola_curve, UP, buff=0.5)
        
        root1_dot = Dot(axes.c2p(1.5, 0), color=GOLD_ACCENT, radius=0.08)
        root2_dot = Dot(axes.c2p(-2.5, 0), color=GOLD_ACCENT, radius=0.08)

        self.play(Create(axes), Create(parabola_curve))
        self.play(Write(parabola_label), Create(root1_dot), Create(root2_dot))
        self.wait(1.5)

        question = Text("How to find these x-intercepts?", color=WHITE, font_size=32).next_to(parabola_label, UP, buff=0.8)
        self.play(FadeIn(question, shift=UP))
        self.wait(1)

        general_eq = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT, font_size=45).next_to(question, DOWN, buff=0.8)
        self.play(FadeIn(general_eq, shift=DOWN))
        self.wait(2)

        self.play(
            FadeOut(title, axes, parabola_curve, parabola_label, root1_dot, root2_dot, question),
            general_eq.animate.center().scale(1.2)
        )
        self.wait(1)

        # --- Beat 2: Completing the Square - Intuition (Geometric Approach) ---
        eq_start_beat2 = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT)
        self.play(ReplacementTransform(general_eq, eq_start_beat2))
        self.wait(0.5)

        intuition_title = Text("Completing the Square", color=BLUE_ACCENT, font_size=40).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(intuition_title, shift=UP))
        self.wait(0.5)
        
        # Visual for x^2 + (b/2a)x + (b/2a)x + (b/2a)^2
        x_side = 2
        b_over_2a_side = 0.8
        
        square_x = Square(x_side, color=BLUE_ACCENT, fill_opacity=0.3).shift(LEFT * 2)
        label_x_h = MathTex("x", color=WHITE).next_to(square_x, DOWN, buff=0.1)
        label_x_v = MathTex("x", color=WHITE).next_to(square_x, LEFT, buff=0.1)

        rect_b_h = Rectangle(width=b_over_2a_side, height=x_side, color=GOLD_ACCENT, fill_opacity=0.3).next_to(square_x, RIGHT, buff=0)
        label_b_h = MathTex("\\frac{b}{2a}", color=WHITE).next_to(rect_b_h, DOWN, buff=0.1)

        rect_b_v = Rectangle(width=x_side, height=b_over_2a_side, color=GOLD_ACCENT, fill_opacity=0.3).next_to(square_x, UP, buff=0)
        label_b_v = MathTex("\\frac{b}{2a}", color=WHITE).next_to(rect_b_v, LEFT, buff=0.1)
        
        self.play(FadeOut(eq_start_beat2)) # Fade out previous equation
        self.play(Create(square_x), Write(label_x_h), Write(label_x_v))
        self.wait(0.5)
        self.play(Create(rect_b_h), Write(label_b_h))
        self.wait(0.5)
        self.play(Create(rect_b_v), Write(label_b_v))
        self.wait(0.7)

        # The missing piece
        missing_square = Square(b_over_2a_side, color=RED_C, fill_opacity=0.5).move_to(rect_b_h.get_top() + rect_b_h.get_right() + UP * (b_over_2a_side/2) + RIGHT * (b_over_2a_side/2))
        missing_square.next_to(rect_b_h, UP, buff=0).next_to(rect_b_v, RIGHT, buff=0) # Correct placement
        missing_square_text = MathTex("\\left(\\frac{b}{2a}\\right)^2", color=RED_C).move_to(missing_square.get_center())

        self.play(Create(missing_square), Write(missing_square_text))
        self.wait(1.5)

        # Show the completed square concept
        completed_square_group = VGroup(square_x, rect_b_h, rect_b_v, missing_square, 
                                        label_x_h, label_x_v, label_b_h, label_b_v, missing_square_text)
        
        final_square_label = MathTex("\\left(x + \\frac{b}{2a}\\right)^2", color=WHITE).scale(1.2)
        
        self.play(
            FadeOut(completed_square_group),
            FadeIn(final_square_label)
        )
        self.wait(1.5)

        self.play(FadeOut(final_square_label, intuition_title))


        # --- Beat 3: Completing the Square - Formal Derivation (Algebraic Transformation) ---
        eq_initial = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(eq_initial))
        self.wait(0.5)

        eq_divide_a = MathTex("x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0", color=WHITE)
        self.play(TransformMatchingTex(eq_initial, eq_divide_a, transform_mobject=True))
        self.wait(1)

        eq_move_c = MathTex("x^2 + \\frac{b}{a}x = -\\frac{c}{a}", color=WHITE)
        self.play(TransformMatchingTex(eq_divide_a, eq_move_c))
        self.wait(1)

        # Adding (b/2a)^2 to both sides
        term_to_add_str = "\\left(\\frac{b}{2a}\\right)^2"
        eq_add_term_full = MathTex(
            "x^2 + \\frac{b}{a}x", 
            " + " + term_to_add_str, 
            " = -\\frac{c}{a} ", 
            " + " + term_to_add_str, 
            color=WHITE
        ).arrange(RIGHT, buff=0.1)
        
        # Position it to align with the previous equation and highlight the added parts
        eq_add_term_full.next_to(eq_move_c, DOWN, buff=0.5) 
        
        # Prepare the terms for lagged display
        lhs_part = MathTex("x^2 + \\frac{b}{a}x", color=WHITE).move_to(eq_add_term_full[0])
        plus_term_lhs = MathTex("+\\left(\\frac{b}{2a}\\right)^2", color=BLUE_ACCENT).move_to(eq_add_term_full[1])
        rhs_part = MathTex(" = -\\frac{c}{a}", color=WHITE).move_to(eq_add_term_full[2])
        plus_term_rhs = MathTex("+\\left(\\frac{b}{2a}\\right)^2", color=BLUE_ACCENT).move_to(eq_add_term_full[3])

        # Animate adding the terms
        self.play(
            TransformMatchingTex(eq_move_c, VGroup(lhs_part, rhs_part), transform_mobject=False),
            FadeIn(plus_term_lhs, shift=UP),
            FadeIn(plus_term_rhs, shift=UP)
        )
        self.wait(1.5)
        
        eq_left_square = MathTex("\\left(x + \\frac{b}{2a}\\right)^2 = -\\frac{c}{a} + \\frac{b^2}{4a^2}", color=WHITE)
        self.play(TransformMatchingTex(VGroup(lhs_part, plus_term_lhs, rhs_part, plus_term_rhs), eq_left_square))
        self.wait(1.5)

        eq_common_denom = MathTex("\\left(x + \\frac{b}{2a}\\right)^2 = \\frac{b^2}{4a^2} - \\frac{4ac}{4a^2}", color=WHITE)
        self.play(TransformMatchingTex(eq_left_square, eq_common_denom))
        self.wait(1.5)

        eq_simplified_right = MathTex("\\left(x + \\frac{b}{2a}\\right)^2 = \\frac{b^2 - 4ac}{4a^2}", color=GOLD_ACCENT)
        self.play(TransformMatchingTex(eq_common_denom, eq_simplified_right))
        self.wait(2)


        # --- Beat 4: Solving for x (Final Steps) ---
        take_sqrt_text = Text("Take the square root of both sides...", color=BLUE_ACCENT, font_size=32).to_edge(DOWN).shift(UP*0.5)
        self.play(FadeIn(take_sqrt_text, shift=DOWN))
        self.wait(0.5)

        eq_sqrt = MathTex("x + \\frac{b}{2a} = \\pm\\sqrt{\\frac{b^2 - 4ac}{4a^2}}", color=WHITE)
        self.play(TransformMatchingTex(eq_simplified_right, eq_sqrt, transform_mobject=False))
        self.play(FadeOut(take_sqrt_text))
        self.wait(1.5)

        eq_sqrt_simplified = MathTex("x + \\frac{b}{2a} = \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}", color=WHITE)
        self.play(TransformMatchingTex(eq_sqrt, eq_sqrt_simplified))
        self.wait(1.5)

        eq_isolate_x = MathTex("x = -\\frac{b}{2a} \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}", color=WHITE)
        self.play(TransformMatchingTex(eq_sqrt_simplified, eq_isolate_x))
        self.wait(1.5)

        final_quadratic_formula = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT).scale(1.5)
        self.play(TransformMatchingTex(eq_isolate_x, final_quadratic_formula, transform_mobject=True))
        self.wait(3)

        self.play(FadeOut(final_quadratic_formula))


        # --- Beat 5: Using the Formula (Application) ---
        app_title = Text("Applying the Formula", color=BLUE_ACCENT, font_size=45).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(app_title, shift=UP))
        self.wait(0.5)

        example_eq = MathTex("2x^2 + 5x - 3 = 0", color=GOLD_ACCENT).move_to(UP)
        self.play(Write(example_eq))
        self.wait(1)

        abc_values = VGroup(
            MathTex("a = 2", color=WHITE),
            MathTex("b = 5", color=WHITE),
            MathTex("c = -3", color=WHITE)
        ).arrange(RIGHT, buff=1).next_to(example_eq, DOWN, buff=1)
        
        self.play(LaggedStart(*[Write(val) for val in abc_values], lag_ratio=0.5))
        self.wait(1.5)

        formula_template = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", color=WHITE).next_to(abc_values, DOWN, buff=1.5)
        self.play(Write(formula_template))
        self.wait(1)

        formula_filled = MathTex("x = \\frac{-(5) \\pm \\sqrt{(5)^2 - 4(2)(-3)}}{2(2)}", color=WHITE).next_to(formula_template, DOWN, buff=0.5)
        self.play(TransformMatchingTex(formula_template, formula_filled))
        self.wait(1.5)

        formula_simplified_sqrt = MathTex("x = \\frac{-5 \\pm \\sqrt{25 - (-24)}}{4}", color=WHITE)
        self.play(ReplacementTransform(formula_filled, formula_simplified_sqrt))
        self.wait(1.5)
        
        formula_simplified_sqrt2 = MathTex("x = \\frac{-5 \\pm \\sqrt{49}}{4}", color=WHITE)
        self.play(ReplacementTransform(formula_simplified_sqrt, formula_simplified_sqrt2))
        self.wait(1.5)

        formula_final_step = MathTex("x = \\frac{-5 \\pm 7}{4}", color=WHITE)
        self.play(ReplacementTransform(formula_simplified_sqrt2, formula_final_step))
        self.wait(1.5)

        solution_1 = MathTex("x_1 = \\frac{-5 + 7}{4} = \\frac{2}{4} = \\frac{1}{2}", color=GOLD_ACCENT)
        solution_2 = MathTex("x_2 = \\frac{-5 - 7}{4} = \\frac{-12}{4} = -3", color=GOLD_ACCENT)
        solutions_group = VGroup(solution_1, solution_2).arrange(DOWN, buff=0.5).shift(DOWN*0.5)

        self.play(FadeOut(example_eq, abc_values, formula_final_step))
        self.play(Write(solution_1))
        self.wait(1)
        self.play(Write(solution_2))
        self.wait(2)

        self.play(FadeOut(app_title, solutions_group))


        # --- Beat 6: Recap Card ---
        recap_title = Text("Recap: The Quadratic Formula", color=BLUE_ACCENT, font_size=50).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(recap_title))

        final_formula_recap = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT).scale(1.8).move_to(UP*0.5)
        self.play(Write(final_formula_recap))
        self.wait(1)

        key_points = VGroup(
            Tex("- Solves any $ax^2 + bx + c = 0$", color=WHITE).scale(0.8),
            Tex("- Derived by 'Completing the Square'", color=WHITE).scale(0.8),
            Tex("- Provides roots (x-intercepts) of parabolas", color=WHITE).scale(0.8)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(final_formula_recap, DOWN, buff=1)

        self.play(LaggedStart(*[Write(point) for point in key_points], lag_ratio=0.7))
        self.wait(3)
        self.play(FadeOut(recap_title, final_formula_recap, key_points))
        self.wait(1)