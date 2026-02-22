from manim import *

class QuadraticIntroduction(Scene):
    def construct(self):
        # Configuration
        self.camera.background_color = "#1A1A1A" # Dark grey
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD

        # Helper function for superscript (no Tex)
        # This needs to be a class method or defined within construct, 
        # but for reusability across methods, I'll pass it.
        # It doesn't use `self` so can be a standalone function too.
        def create_superscript(base_text_str, exp_text_str, color=WHITE, font_size=DEFAULT_FONT_SIZE):
            base = Text(base_text_str, color=color, font_size=font_size)
            exp = Text(exp_text_str, font_size=font_size * 0.7, color=color)
            exp.next_to(base, UP + RIGHT, buff=0.05)
            return VGroup(base, exp)
        
        # Helper for quadratic expression without MathTex
        def create_quadratic_expression_mtext(
            a_str="a", b_str="b", c_str="c", equals_zero=False,
            y_eq_prefix=False, font_size=DEFAULT_FONT_SIZE
        ):
            parts = []
            if y_eq_prefix:
                parts.append(VGroup(Text("y", color=BLUE_ACCENT, font_size=font_size), Text("=", color=WHITE, font_size=font_size)).arrange(RIGHT, buff=0.1))

            a_text = Text(a_str, color=GOLD_ACCENT, font_size=font_size)
            x_sq_text = create_superscript("x", "2", color=WHITE, font_size=font_size)
            plus1_text = Text("+", color=WHITE, font_size=font_size)
            b_text = Text(b_str, color=GOLD_ACCENT, font_size=font_size)
            x_text = Text("x", color=WHITE, font_size=font_size)
            plus2_text = Text("+", color=WHITE, font_size=font_size)
            c_text = Text(c_str, color=GOLD_ACCENT, font_size=font_size)

            current_group = VGroup()
            if y_eq_prefix:
                current_group.add(parts[0])
            
            # Manually position for precision
            a_text.next_to(current_group[-1] if current_group else ORIGIN, RIGHT, buff=0.2 if y_eq_prefix else 0)
            x_sq_text.next_to(a_text, RIGHT, buff=0.05)
            plus1_text.next_to(x_sq_text, RIGHT, buff=0.15)
            b_text.next_to(plus1_text, RIGHT, buff=0.15)
            x_text.next_to(b_text, RIGHT, buff=0.05)
            plus2_text.next_to(x_text, RIGHT, buff=0.15)
            c_text.next_to(plus2_text, RIGHT, buff=0.15)

            final_group_list = [a_text, x_sq_text, plus1_text, b_text, x_text, plus2_text, c_text]
            if y_eq_prefix:
                final_group_list.insert(0, parts[0])

            full_expression = VGroup(*final_group_list)
            
            if equals_zero:
                eq_zero_text = Text("= 0", color=WHITE, font_size=font_size)
                eq_zero_text.next_to(full_expression, RIGHT, buff=0.15)
                full_expression.add(eq_zero_text)
            
            return full_expression

        # Beat 1: Visual Hook - Projectile Motion
        self.beat_1_visual_hook(BLUE_ACCENT, GOLD_ACCENT)

        # Beat 2: From Linear to Quadratic
        self.beat_2_linear_to_quadratic(BLUE_ACCENT, GOLD_ACCENT, create_superscript)

        # Beat 3: General Form of Quadratic Equation
        self.beat_3_general_form(BLUE_ACCENT, GOLD_ACCENT, create_superscript, create_quadratic_expression_mtext)

        # Beat 4: The Quadratic Formula
        self.beat_4_quadratic_formula(BLUE_ACCENT, GOLD_ACCENT, create_superscript, create_quadratic_expression_mtext)

        # Beat 5: Recap
        self.beat_5_recap(BLUE_ACCENT, GOLD_ACCENT, create_superscript, create_quadratic_expression_mtext)

    def beat_1_visual_hook(self, BLUE_ACCENT, GOLD_ACCENT):
        title = Text("Uncovering Curves", font_size=60, color=WHITE).to_edge(UP)
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-2, 8, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": GREY_B}
        ).shift(DOWN * 1.5)
        plane.add_coordinates(font_size=20, color=GREY_B)
        
        x_label = Text("x", color=GREY_B, font_size=24).next_to(plane.x_axis.get_end(), RIGHT * 0.5)
        y_label = Text("y", color=GREY_B, font_size=24).next_to(plane.y_axis.get_end(), UP * 0.5)
        
        self.play(Create(plane), FadeIn(x_label, y_label), run_time=1.5)
        self.wait(0.5)

        parabola_func = lambda x: -0.5 * (x + 1)**2 + 6.5
        parabola = plane.get_graph(parabola_func, x_range=[-5, 3], color=BLUE_ACCENT)
        
        ball = Dot(point=plane.c2p(-5, parabola_func(-5)), color=GOLD_ACCENT, radius=0.15)
        
        self.play(Create(parabola), FadeIn(ball), run_time=1.5)
        self.play(MoveAlongPath(ball, parabola), run_time=2.5, rate_func=smooth)
        self.wait(0.5)

        question_text = Text("How do we describe this shape?", font_size=40, color=WHITE).next_to(parabola, UP, buff=0.5)
        self.play(Write(question_text), run_time=1.5)
        self.wait(1.5)
        
        self.play(
            FadeOut(VGroup(plane, x_label, y_label, parabola, ball, question_text, title)),
            run_time=1.5
        )

    def beat_2_linear_to_quadratic(self, BLUE_ACCENT, GOLD_ACCENT, create_superscript):
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY_B}
        ).to_edge(LEFT, buff=0.5)
        plane.add_coordinates(font_size=20, color=GREY_B)

        x_label = Text("x", color=GREY_B, font_size=24).next_to(plane.x_axis.get_end(), RIGHT * 0.5)
        y_label = Text("y", color=GREY_B, font_size=24).next_to(plane.y_axis.get_end(), UP * 0.5)
        
        self.play(Create(plane), FadeIn(x_label, y_label), run_time=1)

        line_func = lambda x: x
        line = plane.get_graph(line_func, x_range=[-3, 3], color=GOLD_ACCENT)
        
        eq_linear_y = Text("y", color=GOLD_ACCENT)
        eq_linear_equals = Text("=", color=WHITE)
        eq_linear_x = Text("x", color=WHITE)
        eq_linear = VGroup(eq_linear_y, eq_linear_equals, eq_linear_x).arrange(RIGHT, buff=0.2).next_to(plane, RIGHT, buff=1)

        self.play(Create(line), Write(eq_linear), run_time=1.5)
        self.wait(1)

        parabola_func = lambda x: x**2
        parabola = plane.get_graph(parabola_func, x_range=[-2.5, 2.5], color=BLUE_ACCENT)
        
        eq_quadratic_y = Text("y", color=BLUE_ACCENT)
        eq_quadratic_equals = Text("=", color=WHITE)
        eq_quadratic_x_squared = create_superscript("x", "2", color=WHITE)
        
        # Manually position for transition
        eq_quadratic_y.next_to(plane, RIGHT, buff=1).align_to(eq_linear_y, LEFT)
        eq_quadratic_equals.next_to(eq_quadratic_y, RIGHT, buff=0.2)
        eq_quadratic_x_squared[0].next_to(eq_quadratic_equals, RIGHT, buff=0.2) # 'x' part
        eq_quadratic_x_squared[1].next_to(eq_quadratic_x_squared[0], UP+RIGHT, buff=0.05) # '2' part
        eq_quadratic = VGroup(eq_quadratic_y, eq_quadratic_equals, eq_quadratic_x_squared)


        self.play(
            ReplacementTransform(line, parabola),
            ReplacementTransform(eq_linear_y, eq_quadratic_y),
            ReplacementTransform(eq_linear_equals, eq_quadratic_equals),
            ReplacementTransform(eq_linear_x, eq_quadratic_x_squared[0]),
            run_time=1.5
        )
        self.play(Write(eq_quadratic_x_squared[1]), run_time=0.5) # Write the '2'
        self.wait(1)

        defining_term = Text("The 'x²' term creates curves!", color=WHITE, font_size=32).next_to(eq_quadratic_x_squared, DOWN, buff=0.5)
        arrow_to_x_squared = Arrow(defining_term.get_top(), eq_quadratic_x_squared.get_bottom(), color=GOLD_ACCENT, buff=0.1)
        
        self.play(
            Indicate(eq_quadratic_x_squared, color=GOLD_ACCENT),
            Write(defining_term),
            Create(arrow_to_x_squared),
            run_time=2
        )
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(plane, x_label, y_label, parabola, eq_quadratic, defining_term, arrow_to_x_squared)),
            run_time=1.5
        )

    def beat_3_general_form(self, BLUE_ACCENT, GOLD_ACCENT, create_superscript, create_quadratic_expression_mtext):
        general_form_title = Text("General Form", font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(general_form_title), run_time=1)

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 6, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GREY_B}
        ).to_edge(LEFT, buff=0.5)
        plane.add_coordinates(font_size=20, color=GREY_B)

        x_label = Text("x", color=GREY_B, font_size=24).next_to(plane.x_axis.get_end(), RIGHT * 0.5)
        y_label = Text("y", color=GREY_B, font_size=24).next_to(plane.y_axis.get_end(), UP * 0.5)
        
        self.play(Create(plane), FadeIn(x_label, y_label), run_time=1)

        a_val_tracker = ValueTracker(1)
        b_val_tracker = ValueTracker(0)
        c_val_tracker = ValueTracker(0)

        parabola_func = lambda x: a_val_tracker.get_value() * x**2 + b_val_tracker.get_value() * x + c_val_tracker.get_value()
        parabola = always_redraw(lambda: plane.get_graph(parabola_func, x_range=[-3.5, 3.5], color=BLUE_ACCENT))

        general_equation = create_quadratic_expression_mtext(y_eq_prefix=True, font_size=40).next_to(plane, RIGHT, buff=0.7)
        
        self.play(Create(parabola), Write(general_equation), run_time=1.5)
        self.wait(1)

        # Show effects of a, b, c
        # Animate 'a'
        a_param_idx = 1 # Index for 'a' in the VGroup for the expression
        a_label = Text("Controls openness and direction", color=GOLD_ACCENT, font_size=28).next_to(general_equation, DOWN, buff=0.5).align_to(general_equation[a_param_idx], LEFT)
        arrow_a = Arrow(a_label.get_top(), general_equation[a_param_idx].get_bottom(), color=GOLD_ACCENT, buff=0.1)
        self.play(Write(a_label), Create(arrow_a), run_time=1)
        self.play(a_val_tracker.animate.set_value(0.5), run_time=1) # Wider
        self.play(a_val_tracker.animate.set_value(-1), run_time=1) # Opens down
        self.play(a_val_tracker.animate.set_value(2), run_time=1) # Narrower
        self.play(FadeOut(a_label, arrow_a), a_val_tracker.animate.set_value(1), run_time=0.5)
        self.wait(0.2)

        # Animate 'c'
        c_param_idx = 7 # Index for 'c'
        c_label = Text("Controls vertical position (y-intercept)", color=GOLD_ACCENT, font_size=28).next_to(general_equation, DOWN, buff=0.5).align_to(general_equation[c_param_idx], LEFT)
        arrow_c = Arrow(c_label.get_top(), general_equation[c_param_idx].get_bottom(), color=GOLD_ACCENT, buff=0.1)
        self.play(Write(c_label), Create(arrow_c), run_time=1)
        self.play(c_val_tracker.animate.set_value(2), run_time=1) # Shift up
        self.play(c_val_tracker.animate.set_value(-1), run_time=1) # Shift down
        self.play(FadeOut(c_label, arrow_c), c_val_tracker.animate.set_value(0), run_time=0.5)
        self.wait(0.2)

        # Animate 'b'
        b_param_idx = 4 # Index for 'b'
        b_label = Text("Affects horizontal position", color=GOLD_ACCENT, font_size=28).next_to(general_equation, DOWN, buff=0.5).align_to(general_equation[b_param_idx], LEFT)
        arrow_b = Arrow(b_label.get_top(), general_equation[b_param_idx].get_bottom(), color=GOLD_ACCENT, buff=0.1)
        self.play(Write(b_label), Create(arrow_b), run_time=1)
        self.play(b_val_tracker.animate.set_value(1.5), run_time=1) # Shift vertex
        self.play(b_val_tracker.animate.set_value(-1.5), run_time=1)
        self.play(FadeOut(b_label, arrow_b), b_val_tracker.animate.set_value(0), run_time=0.5)
        self.wait(0.2)

        # Emphasize setting to 0 for roots
        equals_zero = Text("= 0", color=WHITE, font_size=40).next_to(general_equation[-1], RIGHT, buff=0.15)
        finding_roots_text = Text("Finding x when y = 0", font_size=32, color=WHITE).next_to(general_equation, DOWN, buff=1)

        self.play(Write(equals_zero), run_time=0.5)
        self.play(Write(finding_roots_text), run_time=1.5)
        self.wait(2)

        self.play(
            FadeOut(VGroup(plane, x_label, y_label, parabola, general_equation, equals_zero, finding_roots_text, general_form_title)),
            run_time=1.5
        )

    def beat_4_quadratic_formula(self, BLUE_ACCENT, GOLD_ACCENT, create_superscript, create_quadratic_expression_mtext):
        formula_title = Text("The Quadratic Formula", font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(formula_title), run_time=1)

        # Re-introduce general form, set to 0
        current_quadratic_equation = create_quadratic_expression_mtext(equals_zero=True, font_size=40, y_eq_prefix=False).center().shift(UP*1)
        self.play(FadeIn(current_quadratic_equation), run_time=1)
        self.wait(1.5)

        problem_text = Text("When simple factoring doesn't work...", font_size=32, color=GREY_A).next_to(current_quadratic_equation, UP, buff=0.7)
        self.play(Write(problem_text), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(problem_text), run_time=0.5)

        # Build the Quadratic Formula: x = (-b +- sqrt(b^2 - 4ac)) / 2a
        x_eq = Text("x =", color=WHITE, font_size=45)
        
        minus_b = Text("-b", color=WHITE, font_size=45)
        plus_minus = Text("±", color=GOLD_ACCENT, font_size=45)
        
        b_sq = create_superscript("b", "2", color=WHITE, font_size=45)
        minus_4ac = Text("- 4ac", color=WHITE, font_size=45)
        
        # Creating a basic square root sign with a line
        sqrt_start = Text("√", color=GOLD_ACCENT, font_size=55) # Larger font for visual root
        
        # Manually position numerator elements
        num_elements_raw = VGroup(minus_b, plus_minus, sqrt_start, b_sq, minus_4ac)
        minus_b.align_to(sqrt_start, DOWN) # Align baselines
        plus_minus.next_to(minus_b, RIGHT, buff=0.15).align_to(minus_b, DOWN)
        sqrt_start.next_to(plus_minus, RIGHT, buff=0.05)
        b_sq.next_to(sqrt_start, RIGHT, buff=0.05).align_to(sqrt_start, DOWN)
        minus_4ac.next_to(b_sq, RIGHT, buff=0.05).align_to(sqrt_start, DOWN)
        
        # Line over the b^2 - 4ac part
        sqrt_line_over = Line(b_sq.get_left() - LEFT*0.05, minus_4ac.get_right() + RIGHT*0.05, color=GOLD_ACCENT)
        sqrt_line_over.next_to(VGroup(b_sq, minus_4ac), UP, buff=0.05)
        
        numerator_group = VGroup(num_elements_raw, sqrt_line_over)
        
        frac_line = Line(LEFT, RIGHT, color=WHITE).set_width(numerator_group.width * 1.05)
        denominator = Text("2a", color=WHITE, font_size=45)

        # Arrange into fraction structure
        fraction_parts = VGroup(numerator_group, frac_line, denominator).arrange(DOWN, buff=0.15)
        
        full_formula_group = VGroup(x_eq, fraction_parts).arrange(RIGHT, buff=0.3).center().scale(0.9)

        self.play(FadeOut(current_quadratic_equation), run_time=1)
        self.wait(0.5)

        # Animate formula build-up
        self.play(Write(x_eq), run_time=0.5)
        self.play(Write(minus_b), Write(plus_minus), run_time=1)
        self.play(
            LaggedStart(
                Write(sqrt_start),
                Create(sqrt_line_over),
                Write(b_sq),
                Write(minus_4ac),
                lag_ratio=0.2, run_time=2
            )
        )
        self.play(Create(frac_line), run_time=0.5)
        self.play(Write(denominator), run_time=0.5)
        self.wait(2.5)

        self.play(FadeOut(full_formula_group, formula_title), run_time=1.5)

    def beat_5_recap(self, BLUE_ACCENT, GOLD_ACCENT, create_superscript, create_quadratic_expression_mtext):
        recap_title = Text("Recap: Quadratic Equations", font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(recap_title), run_time=1)

        # General Form: ax^2 + bx + c = 0
        general_form_recap = create_quadratic_expression_mtext(equals_zero=True, y_eq_prefix=False, font_size=40).move_to(ORIGIN + UP*1.5).scale(0.9)

        # Quadratic Formula: x = (-b +- sqrt(b^2 - 4ac)) / 2a (re-create for clean display)
        x_eq = Text("x =", color=WHITE, font_size=45)
        minus_b = Text("-b", color=WHITE, font_size=45)
        plus_minus = Text("±", color=GOLD_ACCENT, font_size=45)
        b_sq = create_superscript("b", "2", color=WHITE, font_size=45)
        minus_4ac = Text("- 4ac", color=WHITE, font_size=45)
        
        sqrt_start = Text("√", color=GOLD_ACCENT, font_size=55)
        
        num_elements_raw = VGroup(minus_b, plus_minus, sqrt_start, b_sq, minus_4ac)
        minus_b.align_to(sqrt_start, DOWN)
        plus_minus.next_to(minus_b, RIGHT, buff=0.15).align_to(minus_b, DOWN)
        sqrt_start.next_to(plus_minus, RIGHT, buff=0.05)
        b_sq.next_to(sqrt_start, RIGHT, buff=0.05).align_to(sqrt_start, DOWN)
        minus_4ac.next_to(b_sq, RIGHT, buff=0.05).align_to(sqrt_start, DOWN)
        
        sqrt_line_over = Line(b_sq.get_left() - LEFT*0.05, minus_4ac.get_right() + RIGHT*0.05, color=GOLD_ACCENT)
        sqrt_line_over.next_to(VGroup(b_sq, minus_4ac), UP, buff=0.05)
        
        numerator_group = VGroup(num_elements_raw, sqrt_line_over)
        frac_line = Line(LEFT, RIGHT, color=WHITE).set_width(numerator_group.width * 1.05)
        denominator = Text("2a", color=WHITE, font_size=45)

        fraction_parts = VGroup(numerator_group, frac_line, denominator).arrange(DOWN, buff=0.15)
        quadratic_formula_recap = VGroup(x_eq, fraction_parts).arrange(RIGHT, buff=0.3).move_to(ORIGIN + DOWN*1).scale(0.9)

        self.play(FadeIn(general_form_recap, shift=UP), FadeIn(quadratic_formula_recap, shift=DOWN), run_time=2)
        self.wait(3)

        self.play(FadeOut(VGroup(recap_title, general_form_recap, quadratic_formula_recap)), run_time=1.5)