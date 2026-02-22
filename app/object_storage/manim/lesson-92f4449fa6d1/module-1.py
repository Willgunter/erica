from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # 1. Configuration & Setup
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E

        # 2. Strong visual hook: Parabola and its roots
        title = Text("Understanding the Quadratic Formula", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE_ACCENT, "include_numbers": False, "include_ticks": False},
        ).to_edge(LEFT, buff=1).shift(DOWN * 0.5)
        
        labels = axes.get_axis_labels(x_label="x", y_label="y").set_color(BLUE_ACCENT)

        def parabola_func(x):
            return x**2 - 4

        parabola = axes.plot(parabola_func, x_range=[-2.5, 2.5], color=GOLD_ACCENT)

        root1_dot = Dot(axes.c2p(-2, 0), color=GOLD_ACCENT)
        root2_dot = Dot(axes.c2p(2, 0), color=GOLD_ACCENT)

        root1_label = Text("Root", font_size=24, color=GOLD_ACCENT).next_to(root1_dot, DOWN)
        root2_label = Text("Root", font_size=24, color=GOLD_ACCENT).next_to(root2_dot, DOWN)

        roots_group = VGroup(root1_dot, root2_dot, root1_label, root2_label)

        initial_question = Text("How do we find these precise points?", font_size=32, color=BLUE_ACCENT)
        initial_question.next_to(title, DOWN, buff=0.8).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)

        self.play(
            Create(axes),
            Write(labels),
            run_time=1.5
        )
        self.play(
            Create(parabola),
            run_time=1
        )
        self.play(
            GrowFromCenter(root1_dot),
            GrowFromCenter(root2_dot),
            Write(root1_label),
            Write(root2_label),
            Write(initial_question),
            run_time=2
        )
        self.wait(1)

        # Beat 2: The General Form ax^2 + bx + c = 0
        self.play(
            FadeOut(initial_question),
            FadeOut(roots_group),
            parabola.animate.set_opacity(0.3), # Dim the parabola for context
            run_time=1
        )

        # Construct y = ax^2 + bx + c using Text objects
        y_eq = Text("y = ", color=BLUE_ACCENT)
        a_coeff_y = Text("a", color=GOLD_ACCENT)
        x_sq_y = Text("x", color=BLUE_ACCENT)
        exp2_y = Text("2", font_size=24, color=BLUE_ACCENT).scale(0.7).next_to(x_sq_y, UP + RIGHT, buff=0.01).align_to(x_sq_y.get_corner(UP + RIGHT), DOWN)
        plus1_y = Text(" + ", color=BLUE_ACCENT)
        b_coeff_y = Text("b", color=GOLD_ACCENT)
        x_val_y = Text("x", color=BLUE_ACCENT)
        plus2_y = Text(" + ", color=BLUE_ACCENT)
        c_coeff_y = Text("c", color=GOLD_ACCENT)

        general_eq_y_form = VGroup(
            y_eq, a_coeff_y, x_sq_y, exp2_y, plus1_y, b_coeff_y, x_val_y, plus2_y, c_coeff_y
        ).arrange(RIGHT, buff=0.05).scale(0.9)
        general_eq_y_form.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.5)

        self.play(
            FadeIn(y_eq),
            LaggedStart(*[FadeIn(m) for m in general_eq_y_form[1:]], lag_ratio=0.05),
            run_time=2
        )
        self.wait(0.5)

        # Transform to ax^2 + bx + c = 0
        eq_zero_text = Text(" = 0", color=BLUE_ACCENT).next_to(general_eq_y_form[-1], RIGHT, buff=0.05)
        
        # Create the target equation group
        target_equation = VGroup(
            VGroup(a_coeff_y, x_sq_y, exp2_y).copy(),
            plus1_y.copy(),
            VGroup(b_coeff_y, x_val_y).copy(),
            plus2_y.copy(),
            c_coeff_y.copy(),
            eq_zero_text
        ).arrange(RIGHT, buff=0.05).scale(0.9) # Re-scale to ensure consistent size
        target_equation.move_to(general_eq_y_form.get_center())

        self.play(
            ReplacementTransform(general_eq_y_form, target_equation),
            run_time=1.5
        )

        problem_statement = Text("Find 'x' when y = 0.", font_size=28, color=BLUE_ACCENT).next_to(target_equation, DOWN, buff=0.5)
        self.play(Write(problem_statement), run_time=1)
        self.wait(1)

        # Beat 3: Intuition - A Universal Solution (without explicit derivation)
        self.play(FadeOut(problem_statement))

        # Highlight a, b, c in the equation
        a_highlight = SurroundingRectangle(target_equation[0][0], color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)
        b_highlight = SurroundingRectangle(target_equation[2][0], color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)
        c_highlight = SurroundingRectangle(target_equation[4], color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)

        self.play(
            Create(a_highlight),
            Create(b_highlight),
            Create(c_highlight),
            run_time=1
        )
        self.wait(0.5)

        intuition_text = Text(
            "A universal tool for ANY quadratic equation.",
            font_size=32,
            color=BLUE_ACCENT
        ).next_to(target_equation, DOWN, buff=0.5)

        self.play(
            FadeOut(a_highlight),
            FadeOut(b_highlight),
            FadeOut(c_highlight),
            Write(intuition_text),
            run_time=1.5
        )
        self.wait(1)
        
        # Beat 4: The Quadratic Formula Revealed
        self.play(FadeOut(parabola), axes.animate.set_opacity(0.3), labels.animate.set_opacity(0.3), run_time=1)
        self.play(
            target_equation.animate.scale(0.8).to_corner(UP+LEFT).shift(RIGHT*0.5),
            FadeOut(intuition_text),
            title.animate.set_opacity(0.0), # Temporarily hide title
            run_time=1.5
        )
        title_formula = Text("The Quadratic Formula", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title_formula))

        # Building the formula without MathTex
        x_equals = Text("x =", color=BLUE_ACCENT, font_size=40)
        
        # Numerator components
        num_minus_b = Text("-b", color=GOLD_ACCENT, font_size=40)
        num_plus_minus = Text("±", color=BLUE_ACCENT, font_size=40)

        # b^2
        b_sq_val = Text("b", color=GOLD_ACCENT, font_size=40)
        sq_exp_val = Text("2", color=BLUE_ACCENT, font_size=24).scale(0.7).next_to(b_sq_val, UP + RIGHT, buff=0.01).align_to(b_sq_val.get_corner(UP + RIGHT), DOWN)
        b_squared_group = VGroup(b_sq_val, sq_exp_val)

        # -4ac (separated for individual highlighting)
        minus_4_text = Text("- 4", color=GOLD_ACCENT, font_size=40)
        a_val_in_4ac = Text("a", color=GOLD_ACCENT, font_size=40)
        c_val_in_4ac = Text("c", color=GOLD_ACCENT, font_size=40)
        minus_4ac_group = VGroup(minus_4_text, a_val_in_4ac, c_val_in_4ac).arrange(RIGHT, buff=0.05)

        # Discriminant content
        discriminant_content_group = VGroup(b_squared_group, minus_4ac_group).arrange(RIGHT, buff=0.1)

        sqrt_open = Text("sqrt(", color=BLUE_ACCENT, font_size=40)
        sqrt_close = Text(")", color=BLUE_ACCENT, font_size=40)

        # Arrange numerator parts, then group them
        numerator_elements_arranged = VGroup(
            num_minus_b,
            num_plus_minus,
            sqrt_open,
            discriminant_content_group,
            sqrt_close
        ).arrange(RIGHT, buff=0.05)
        
        # Align `discriminant_content_group` and `sqrt_close` vertically relative to `sqrt_open`
        # Need to align their centers, or top/bottom
        sqrt_open.align_to(num_minus_b, DOWN) # Align "sqrt(" with "-b"
        num_plus_minus.align_to(num_minus_b, DOWN) # Align "±" with "-b"
        discriminant_content_group.align_to(num_minus_b, DOWN)
        sqrt_close.align_to(num_minus_b, DOWN)


        # Fraction line (needs to be wide enough for the numerator)
        fraction_line_formula = Line(
            numerator_elements_arranged.get_left() - LEFT * 0.2,
            numerator_elements_arranged.get_right() + RIGHT * 0.2
        ).set_color(BLUE_ACCENT)
        
        # Denominator (2a)
        denom_two = Text("2", color=BLUE_ACCENT, font_size=40)
        denom_a = Text("a", color=GOLD_ACCENT, font_size=40)
        denominator_formula_group = VGroup(denom_two, denom_a).arrange(RIGHT, buff=0.05)

        # Combine and position vertically
        full_formula_group = VGroup(
            numerator_elements_arranged,
            fraction_line_formula,
            denominator_formula_group
        )
        full_formula_group.arrange(DOWN, buff=0.4) # Arrange vertically, with buff between line and elements

        quadratic_formula_display = VGroup(x_equals, full_formula_group).arrange(RIGHT, buff=0.2).center()

        # Animation of the formula building
        self.play(
            FadeTransform(target_equation, x_equals),
            Create(num_minus_b),
            run_time=1
        )
        self.play(
            Create(num_plus_minus),
            run_time=0.5
        )
        self.play(
            Create(sqrt_open),
            Create(b_sq_val), Create(sq_exp_val),
            run_time=1
        )
        self.play(
            Create(minus_4_text), Create(a_val_in_4ac), Create(c_val_in_4ac),
            run_time=1
        )
        self.play(
            Create(sqrt_close),
            Create(fraction_line_formula),
            Create(denom_two), Create(denom_a),
            run_time=1.5
        )
        self.wait(1)

        # Highlight a, b, c in the formula using the pre-defined Mobjects
        b_highlight_rect1 = SurroundingRectangle(num_minus_b, color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)
        b_highlight_rect2 = SurroundingRectangle(b_sq_val, color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)
        a_highlight_rect1 = SurroundingRectangle(a_val_in_4ac, color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)
        c_highlight_rect1 = SurroundingRectangle(c_val_in_4ac, color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)
        a_highlight_rect2 = SurroundingRectangle(denom_a, color=GOLD_ACCENT, buff=0.1).set_stroke(width=3)

        self.play(
            Create(b_highlight_rect1),
            Create(b_highlight_rect2),
            Create(a_highlight_rect1),
            Create(c_highlight_rect1),
            Create(a_highlight_rect2),
            run_time=2
        )
        self.wait(1)
        self.play(
            FadeOut(b_highlight_rect1),
            FadeOut(b_highlight_rect2),
            FadeOut(a_highlight_rect1),
            FadeOut(c_highlight_rect1),
            FadeOut(a_highlight_rect2),
            run_time=1
        )
        self.wait(1)

        # Beat 5: Recap Card
        self.play(
            FadeOut(title_formula),
            FadeOut(axes),
            FadeOut(labels),
            quadratic_formula_display.animate.scale(1.2).center(), # Keep formula, scale up
            run_time=1.5
        )

        recap_title = Text("Recap: The Quadratic Formula", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        recap_text = Text(
            "Use it to solve any equation of the form:",
            font_size=32, color=BLUE_ACCENT
        ).next_to(recap_title, DOWN, buff=0.5)

        # Re-create the ax^2+bx+c=0 for recap
        recap_a = Text("a", color=GOLD_ACCENT)
        recap_x_sq = Text("x", color=BLUE_ACCENT)
        recap_exp2 = Text("2", font_size=24, color=BLUE_ACCENT).scale(0.7).next_to(recap_x_sq, UP + RIGHT, buff=0.01).align_to(recap_x_sq.get_corner(UP + RIGHT), DOWN)
        recap_plus1 = Text(" + ", color=BLUE_ACCENT)
        recap_b = Text("b", color=GOLD_ACCENT)
        recap_x = Text("x", color=BLUE_ACCENT)
        recap_plus2 = Text(" + ", color=BLUE_ACCENT)
        recap_c = Text("c", color=GOLD_ACCENT)
        recap_eq_zero = Text(" = 0", color=BLUE_ACCENT)

        recap_equation = VGroup(
            recap_a, recap_x_sq, recap_exp2, recap_plus1, recap_b, recap_x, recap_plus2, recap_c, recap_eq_zero
        ).arrange(RIGHT, buff=0.05).scale(0.8)
        recap_equation.next_to(recap_text, DOWN, buff=0.3)

        self.play(
            Write(recap_title),
            Write(recap_text),
            Create(recap_equation),
            run_time=2
        )
        self.wait(3)

        self.play(
            FadeOut(recap_title),
            FadeOut(recap_text),
            FadeOut(recap_equation),
            FadeOut(quadratic_formula_display),
            run_time=1
        )
        self.wait(1)