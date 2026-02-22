from manim import *

# Define custom colors for the 3B1B style
BLUE_ACCENT = BLUE_C
GOLD_ACCENT = GOLD_C
TEAL_ACCENT = TEAL_E
DARK_BACKGROUND = '#1A1A1A' # A very dark grey, almost black

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = DARK_BACKGROUND
        self.camera.background_color = DARK_BACKGROUND # Ensure scene background also reflects this

        # Set default text and math colors for consistency
        MathTex.set_default(color=BLUE_ACCENT)
        Text.set_default(color=GOLD_ACCENT)

        # --- Beat 1: The Problem & The Goal (Initial Setup) ---
        # Title
        title = Text("Deriving the Quadratic Formula Steps", font_size=48).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Visual Hook: Parabola and its roots
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 8, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": DARK_GREY},
            background_line_style={"stroke_opacity": 0.3}
        ).shift(DOWN * 0.5)
        
        # Initial parabola (x^2)
        initial_parabola = plane.get_graph(lambda x: x**2, color=TEAL_ACCENT)
        
        # Target parabola (illustrative)
        a_val, b_val, c_val = 0.5, -1, -2  # Example coefficients for roots
        target_parabola = plane.get_graph(lambda x: a_val*x**2 + b_val*x + c_val, color=BLUE_ACCENT)
        
        # The general quadratic equation
        eq1 = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT, font_size=48).next_to(plane, UP, buff=0.8)
        
        self.play(
            Create(plane),
            Create(initial_parabola),
            run_time=2
        )
        self.play(
            Transform(initial_parabola, target_parabola),
            Write(eq1),
            run_time=2
        )
        self.wait(1)

        # Point out the roots conceptually
        root_dots = VGroup()
        for root_val in [-1.45, 3.45]: # Approximate roots for a=0.5, b=-1, c=-2
             root_dots.add(Dot(plane.coords_to_point(root_val, 0), color=GOLD_ACCENT, radius=0.1))

        goal_text = Text("Find x when y=0", font_size=28, color=TEAL_ACCENT).next_to(eq1, DOWN, buff=0.5)
        
        self.play(FadeIn(root_dots))
        self.play(root_dots.animate.scale(1.5).set_opacity(0.5), run_time=0.5)
        self.play(root_dots.animate.scale(1/1.5).set_opacity(1), run_time=0.5)
        self.play(Write(goal_text))
        self.wait(1.5)
        
        self.play(FadeOut(initial_parabola, root_dots, plane, goal_text, title))

        # Re-center eq1 for subsequent steps
        self.play(eq1.animate.to_edge(UP, buff=0.75))
        self.wait(0.5)

        # --- Beat 2: Normalize (Divide by 'a') ---
        step_label_1 = Text("1. Normalize (divide by 'a')", font_size=32, color=TEAL_ACCENT).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_1))

        eq_div_a = MathTex(
            r"\frac{ax^2}{a} + \frac{bx}{a} + \frac{c}{a} = \frac{0}{a}",
            color=BLUE_ACCENT, font_size=48
        ).move_to(eq1.get_center())

        self.play(ReplacementTransform(eq1, eq_div_a), run_time=1.5)
        self.wait(0.5)

        eq_normalized = MathTex(
            r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0",
            color=GOLD_ACCENT, font_size=48
        ).move_to(eq_div_a.get_center())

        self.play(TransformMatchingTex(eq_div_a, eq_normalized), run_time=1.5)
        self.wait(1)
        
        # Current equation for next step
        eq_current = eq_normalized

        # --- Beat 3: Isolate and Complete the Square ---
        self.play(FadeOut(step_label_1))
        step_label_2 = Text("2. Isolate and Complete the Square", font_size=32, color=TEAL_ACCENT).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_2))

        # Move constant term
        eq_isolated = MathTex(
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            color=BLUE_ACCENT, font_size=48
        ).move_to(eq_current.get_center())
        
        self.play(TransformMatchingTex(eq_current, eq_isolated), run_time=1.5)
        self.wait(0.5)

        # Geometric intuition for completing the square
        x_square = Square(side_length=2, color=BLUE_ACCENT, fill_opacity=0.3).shift(LEFT*3 + DOWN*1.5)
        x_label_inside = MathTex("x^2", color=BLUE_ACCENT).move_to(x_square)
        
        bx_rect = Rectangle(width=1, height=2, color=GOLD_ACCENT, fill_opacity=0.3).next_to(x_square, RIGHT, buff=0)
        bx_label_inside = MathTex(r"\frac{b}{a}x", color=GOLD_ACCENT).move_to(bx_rect)

        self.play(FadeIn(x_square, x_label_inside, bx_rect, bx_label_inside), run_time=1.5)
        self.wait(0.5)

        # Rearrange to form incomplete square
        bx_rect_half1 = Rectangle(width=1, height=1, color=GOLD_ACCENT, fill_opacity=0.3).move_to(x_square.get_corner(UR) + RIGHT*0.5 + DOWN*0.5)
        bx_rect_half2 = Rectangle(width=1, height=1, color=GOLD_ACCENT, fill_opacity=0.3).move_to(x_square.get_corner(DR) + DOWN*0.5)

        self.play(
            FadeOut(bx_rect, bx_label_inside),
            FadeIn(bx_rect_half1, bx_rect_half2),
            run_time=0.75
        )
        self.play(
            bx_rect_half1.animate.next_to(x_square, RIGHT, buff=0),
            bx_rect_half2.animate.next_to(x_square, DOWN, buff=0),
            bx_rect_half2.animate.rotate(PI/2), # Rotate to be horizontal
            run_time=1.2
        )

        missing_square = Square(side_length=1, color=TEAL_ACCENT, fill_opacity=0.5).next_to(bx_rect_half2, RIGHT, buff=0)
        missing_label = MathTex(r"(\frac{b}{2a})^2", color=TEAL_ACCENT).move_to(missing_square)

        self.play(FadeIn(missing_square, missing_label), run_time=1)
        self.wait(1)
        self.play(FadeOut(x_square, x_label_inside, bx_rect_half1, bx_rect_half2, missing_square, missing_label))
        
        # Algebraically add (b/2a)^2 to both sides
        term_to_add_math = MathTex(r"\left(\frac{b}{2a}\right)^2", color=TEAL_ACCENT, font_size=40)
        
        # Split eq_isolated for the addition animation
        eq_iso_left = MathTex(r"x^2 + \frac{b}{a}x", color=BLUE_ACCENT, font_size=48).move_to(eq_isolated.get_part_by_tex(r"x^2 + \frac{b}{a}x"))
        eq_iso_equals = MathTex("=", color=BLUE_ACCENT, font_size=48).move_to(eq_isolated.get_part_by_tex("="))
        eq_iso_right = MathTex(r"-\frac{c}{a}", color=BLUE_ACCENT, font_size=48).move_to(eq_isolated.get_part_by_tex(r"-\frac{c}{a}"))
        
        self.play(
            eq_iso_left.animate.shift(LEFT * 1.5),
            eq_iso_right.animate.shift(RIGHT * 1.5),
            FadeOut(eq_isolated), # Fade out original full equation
            run_time=1
        )

        plus_left = Text("+", color=TEAL_ACCENT, font_size=40).next_to(eq_iso_left, RIGHT, buff=0.3)
        plus_right = Text("+", color=TEAL_ACCENT, font_size=40).next_to(eq_iso_right, RIGHT, buff=0.3)
        add_term_left = term_to_add_math.copy().next_to(plus_left, RIGHT, buff=0.3)
        add_term_right = term_to_add_math.copy().next_to(plus_right, RIGHT, buff=0.3)

        self.play(
            LaggedStart(
                FadeIn(plus_left), FadeIn(add_term_left),
                FadeIn(plus_right), FadeIn(add_term_right),
                lag_ratio=0.3,
                run_time=1.5
            )
        )
        self.wait(0.5)

        eq_added_full = MathTex(
            r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \frac{b^2}{4a^2}",
            color=GOLD_ACCENT, font_size=48
        ).move_to(eq_isolated.get_center())

        self.play(
            TransformMatchingTex(VGroup(eq_iso_left, plus_left, add_term_left, eq_iso_equals, eq_iso_right, plus_right, add_term_right), eq_added_full),
            run_time=1.5
        )
        self.wait(1)
        eq_current = eq_added_full

        # --- Beat 4: Factor and Consolidate ---
        self.play(FadeOut(step_label_2))
        step_label_3 = Text("3. Factor and Consolidate", font_size=32, color=TEAL_ACCENT).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_3))

        # Factor left side
        eq_factored_left = MathTex(
            r"\left(x + \frac{b}{2a}\right)^2",
            color=BLUE_ACCENT, font_size=48
        ).move_to(eq_current.get_part_by_tex(r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2").get_center())
        
        # Consolidate right side (common denominator)
        eq_right_common_denom = MathTex(
            r"-\frac{4ac}{4a^2} + \frac{b^2}{4a^2}",
            color=BLUE_ACCENT, font_size=48
        ).move_to(eq_current.get_part_by_tex(r"-\frac{c}{a} + \frac{b^2}{4a^2}").get_center())

        eq_equals = MathTex("=", color=BLUE_ACCENT, font_size=48).move_to(eq_current.get_part_by_tex("="))

        self.play(
            TransformMatchingTex(eq_current.get_part_by_tex(r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2"), eq_factored_left),
            ReplacementTransform(eq_current.get_part_by_tex(r"-\frac{c}{a} + \frac{b^2}{4a^2}"), eq_right_common_denom),
            run_time=1.5
        )
        self.wait(0.5)

        eq_right_simplified = MathTex(
            r"\frac{b^2 - 4ac}{4a^2}",
            color=GOLD_ACCENT, font_size=48
        ).move_to(eq_right_common_denom.get_center())

        self.play(TransformMatchingTex(eq_right_common_denom, eq_right_simplified), run_time=1.5)
        self.wait(1)

        eq_consolidated_full = MathTex(
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            color=GOLD_ACCENT, font_size=48
        ).move_to(eq_current.get_center())

        self.play(TransformMatchingTex(VGroup(eq_factored_left, eq_equals, eq_right_simplified), eq_consolidated_full), run_time=1.5)
        self.wait(1)
        eq_current = eq_consolidated_full

        # --- Beat 5: Take the Square Root and Solve for x ---
        self.play(FadeOut(step_label_3))
        step_label_4 = Text("4. Take Square Root and Solve for x", font_size=32, color=TEAL_ACCENT).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_4))

        # Take square root
        sqrt_op_left = MathTex(r"\sqrt{\left(x + \frac{b}{2a}\right)^2}", color=BLUE_ACCENT, font_size=48).move_to(eq_current.get_part_by_tex(r"\left(x + \frac{b}{2a}\right)^2").get_center())
        sqrt_op_right = MathTex(r"\pm\sqrt{\frac{b^2 - 4ac}{4a^2}}", color=BLUE_ACCENT, font_size=48).move_to(eq_current.get_part_by_tex(r"\frac{b^2 - 4ac}{4a^2}").get_center())
        
        self.play(
            TransformMatchingTex(eq_current.get_part_by_tex(r"\left(x + \frac{b}{2a}\right)^2"), sqrt_op_left),
            TransformMatchingTex(eq_current.get_part_by_tex(r"\frac{b^2 - 4ac}{4a^2}"), sqrt_op_right),
            run_time=1.5
        )
        self.wait(0.5)

        eq_after_sqrt = MathTex(
            r"x + \frac{b}{2a} = \pm \frac{\sqrt{b^2 - 4ac}}{2a}",
            color=GOLD_ACCENT, font_size=48
        ).move_to(eq_current.get_center())

        self.play(TransformMatchingTex(VGroup(sqrt_op_left, eq_current.get_part_by_tex("="), sqrt_op_right), eq_after_sqrt), run_time=1.5)
        self.wait(1)
        eq_current = eq_after_sqrt

        # Isolate x
        eq_isolated_x = MathTex(
            r"x = -\frac{b}{2a} \pm \frac{\sqrt{b^2 - 4ac}}{2a}",
            color=BLUE_ACCENT, font_size=48
        ).move_to(eq_current.get_center())

        self.play(TransformMatchingTex(eq_current, eq_isolated_x), run_time=1.5)
        self.wait(0.5)

        # Combine terms
        final_formula = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            color=GOLD_ACCENT, font_size=64 # Make final formula larger
        ).move_to(eq_isolated_x.get_center())

        self.play(TransformMatchingTex(eq_isolated_x, final_formula), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(step_label_4))

        # --- Recap Card ---
        self.play(final_formula.animate.to_edge(UP, buff=0.75).scale(0.8))
        
        recap_title = Text("Recap: Steps to Derive Quadratic Formula", font_size=36, color=TEAL_ACCENT).next_to(final_formula, DOWN, buff=0.8).align_to(final_formula, LEFT)
        self.play(Write(recap_title))

        steps_list = VGroup(
            MathTex(r"\bullet \text{ Start with } ax^2+bx+c=0", font_size=32, color=BLUE_ACCENT),
            MathTex(r"\bullet \text{ Normalize by dividing by } a", font_size=32, color=BLUE_ACCENT),
            MathTex(r"\bullet \text{ Isolate } x \text{ terms and complete the square}", font_size=32, color=BLUE_ACCENT),
            MathTex(r"\bullet \text{ Factor and consolidate right side}", font_size=32, color=BLUE_ACCENT),
            MathTex(r"\bullet \text{ Take square root and solve for } x", font_size=32, color=BLUE_ACCENT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(recap_title, DOWN, buff=0.5).shift(RIGHT*0.5)

        self.play(LaggedStart(*[Write(step) for step in steps_list], lag_ratio=0.7), run_time=3)
        self.wait(3)

        self.play(FadeOut(self.mobjects)) # Fade out all mobjects