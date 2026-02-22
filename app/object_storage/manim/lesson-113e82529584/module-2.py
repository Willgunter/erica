from manim import *

class DerivingQuadraticFormula(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        blue_color = BLUE_C
        gold_color = GOLD_C
        white_color = WHITE

        # --- Beat 0: Visual Hook ---
        self.visual_hook(blue_color, gold_color, white_color)
        self.wait(1)

        # --- Beat 1: Geometric Completing the Square (x^2 + bx) ---
        self.geometric_completing_square(blue_color, gold_color, white_color)
        self.wait(1)

        # --- Beat 2: Algebra with Completing the Square (x^2 + bx + c = 0) ---
        self.algebraic_completing_square_a_is_1(blue_color, gold_color, white_color)
        self.wait(1)

        # --- Beat 3: Generalization (ax^2 + bx + c = 0) ---
        self.generalization_divide_by_a(blue_color, gold_color, white_color)
        self.wait(1)

        # --- Beat 4: Isolating x and Simplifying ---
        self.isolate_x_and_simplify(blue_color, gold_color, white_color)
        self.wait(2)

        # --- Recap Card ---
        self.recap_card(blue_color, gold_color, white_color)
        self.wait(3)

    # --- Helper methods for each beat ---

    def visual_hook(self, blue_color, gold_color, white_color):
        title = Text("Deriving the Quadratic Formula", font_size=50, color=blue_color).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 8, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": DARK_GRAY},
            background_line_style={"stroke_opacity": 0.4}
        ).shift(DOWN * 0.5)
        self.play(Create(plane), run_time=1)
        self.play(plane.animate.set_opacity(0.3), run_time=0.5)

        # Example parabola y = x^2 - 4
        def func(x):
            return x*x - 4

        graph = plane.get_graph(func, color=gold_color)
        self.play(Create(graph), run_time=2)

        # Highlight roots
        root1_dot = Dot(point=plane.coords_to_point(-2, 0), color=blue_color, radius=0.1)
        root2_dot = Dot(point=plane.coords_to_point(2, 0), color=blue_color, radius=0.1)

        roots_text = Text("Roots", color=blue_color, font_size=30).next_to(root1_dot, UP).shift(RIGHT*1.5)
        roots_arrow = Arrow(roots_text.get_bottom(), root1_dot.get_top(), buff=0.1, color=blue_color, tip_length=0.2)
        
        self.play(
            FadeIn(root1_dot, scale=0.8),
            FadeIn(root2_dot, scale=0.8),
            GrowArrow(roots_arrow),
            Write(roots_text),
            run_time=1.5
        )

        self.play(
            FadeOut(graph, shift=UP),
            FadeOut(root1_dot, root2_dot, roots_text, roots_arrow),
            FadeOut(plane),
            run_time=1.5
        )
        self.play(title.animate.to_edge(UP).scale(0.8), run_time=0.5)
        self.current_title = title 

    def geometric_completing_square(self, blue_color, gold_color, white_color):
        current_title = self.current_title
        beat_title = Text("1. Visualize x² + bx", font_size=35, color=gold_color).next_to(current_title, DOWN, buff=0.4)
        self.play(Write(beat_title))

        x_val = 2.5 # Side length for x
        b_half_val = 0.8 # Side length for b/2

        # x^2 square (top-left)
        x_square = Square(side_length=x_val, color=blue_color, fill_opacity=0.2)
        x_square.move_to(LEFT * (b_half_val/2 + x_val/2) + UP * (b_half_val/2 + x_val/2)) 
        x_sq_label = Text("x²", color=blue_color).move_to(x_square.get_center())
        
        # Labels for sides (initial)
        x_label_top = Text("x", color=blue_color).next_to(x_square.get_top(), UP)
        x_label_left = Text("x", color=blue_color).next_to(x_square.get_left(), LEFT)

        self.play(Create(x_square), Write(x_sq_label), Write(x_label_top), Write(x_label_left))

        # x * (b/2) rectangle (top-right)
        rect_xb_half_1 = Rectangle(width=b_half_val, height=x_val, color=gold_color, fill_opacity=0.2)
        rect_xb_half_1.next_to(x_square, RIGHT, buff=0)
        xb_half_label_1 = Text("x(b/2)", color=gold_color, font_size=25).move_to(rect_xb_half_1.get_center())
        b_half_label_top_right = Text("b/2", color=gold_color, font_size=25).next_to(rect_xb_half_1.get_top(), UP)

        self.play(Create(rect_xb_half_1), Write(xb_half_label_1), Write(b_half_label_top_right))

        # (b/2) * x rectangle (bottom-left)
        rect_xb_half_2 = Rectangle(width=x_val, height=b_half_val, color=gold_color, fill_opacity=0.2)
        rect_xb_half_2.next_to(x_square, DOWN, buff=0)
        xb_half_label_2 = Text("x(b/2)", color=gold_color, font_size=25).move_to(rect_xb_half_2.get_center())
        b_half_label_bottom_left = Text("b/2", color=gold_color, font_size=25).next_to(rect_xb_half_2.get_left(), LEFT)

        self.play(Create(rect_xb_half_2), Write(xb_half_label_2), Write(b_half_label_bottom_left))

        # Highlight the missing piece (bottom-right)
        missing_square = Square(side_length=b_half_val, color=BLUE_A, fill_opacity=0.4, stroke_opacity=1, stroke_width=2)
        missing_square.next_to(rect_xb_half_1, DOWN, buff=0).align_to(rect_xb_half_2, RIGHT) 
        missing_label = Text("(b/2)²", color=BLUE_A, font_size=25).move_to(missing_square.get_center())
        
        missing_text = Text("Missing Piece!", color=white_color, font_size=30).next_to(missing_square, DOWN, buff=0.5)
        missing_arrow = Arrow(missing_text.get_top(), missing_square.get_center(), buff=0.2, color=white_color, tip_length=0.2)
        
        self.play(
            Create(missing_square),
            Write(missing_label),
            Write(missing_text),
            GrowArrow(missing_arrow)
        )
        self.wait(1)

        self.play(FadeOut(missing_text, missing_arrow))
        
        all_shapes = VGroup(x_square, rect_xb_half_1, rect_xb_half_2, missing_square)
        all_area_labels = VGroup(x_sq_label, xb_half_label_1, xb_half_label_2, missing_label)
        all_side_labels = VGroup(x_label_top, x_label_left, b_half_label_top_right, b_half_label_bottom_left)

        all_geometric_elements = VGroup(all_shapes, all_area_labels, all_side_labels)
        
        self.play(all_geometric_elements.animate.shift(LEFT * 2.5), run_time=1.5)

        # Formula text
        formula_lhs_parts = VGroup(
            Text("(", color=white_color),
            Text("x", color=blue_color),
            Text(" + ", color=white_color),
            Text("b/2", color=gold_color), 
            Text(")²", color=white_color)
        ).arrange(RIGHT, buff=0.05)
        
        formula_rhs_parts = VGroup(
            Text("x²", color=blue_color),
            Text(" + ", color=white_color),
            Text("bx", color=gold_color),
            Text(" + ", color=white_color),
            Text("(b/2)²", color=gold_color)
        ).arrange(RIGHT, buff=0.1)

        formula_vgroup = VGroup(formula_lhs_parts, Text(" = ", color=white_color), formula_rhs_parts).arrange(RIGHT, buff=0.1).center().shift(RIGHT * 2 + UP * 0.5)

        self.play(Write(formula_vgroup))
        self.wait(1)

        self.play(
            FadeOut(all_geometric_elements, formula_vgroup),
            FadeOut(beat_title)
        )

    def algebraic_completing_square_a_is_1(self, blue_color, gold_color, white_color):
        current_title = self.current_title
        beat_title = Text("2. Algebra: x² + bx + c = 0", font_size=35, color=gold_color).next_to(current_title, DOWN, buff=0.4)
        self.play(Write(beat_title))

        eq1_x_sq = Text("x²", color=blue_color)
        eq1_plus_b_x = Text("+ bx", color=gold_color).next_to(eq1_x_sq, RIGHT)
        eq1_plus_c = Text("+ c", color=gold_color).next_to(eq1_plus_b_x, RIGHT)
        eq1_equals_0 = Text("= 0", color=white_color).next_to(eq1_plus_c, RIGHT)
        
        eq1 = VGroup(eq1_x_sq, eq1_plus_b_x, eq1_plus_c, eq1_equals_0).center().shift(UP * 2)
        self.play(Write(eq1))

        # Move c to RHS
        eq2_x_sq = Text("x²", color=blue_color).align_to(eq1_x_sq, LEFT)
        eq2_plus_b_x = Text("+ bx", color=gold_color).next_to(eq2_x_sq, RIGHT)
        eq2_equals_minus_c = Text("= -c", color=white_color).next_to(eq2_plus_b_x, RIGHT, buff=1.0)
        
        eq2_temp_group = VGroup(eq2_x_sq, eq2_plus_b_x, eq2_equals_minus_c).center().shift(UP * 1)
        
        self.play(
            ReplacementTransform(VGroup(eq1_x_sq, eq1_plus_b_x), VGroup(eq2_x_sq, eq2_plus_b_x).align_to(eq1_x_sq, LEFT)),
            ReplacementTransform(VGroup(eq1_plus_c, eq1_equals_0), eq2_equals_minus_c)
        )

        # Add (b/2)² to both sides
        add_b_half_sq_lhs_text = Text("+ (b/2)²", color=white_color, font_size=35).next_to(eq2_plus_b_x, RIGHT)
        add_b_half_sq_rhs_text = Text("+ (b/2)²", color=white_color, font_size=35).next_to(eq2_equals_minus_c, RIGHT)

        self.play(Write(add_b_half_sq_lhs_text), Write(add_b_half_sq_rhs_text))

        # Factor LHS and combine RHS
        eq3_lhs = Text("(x + b/2)²", color=blue_color)
        eq3_equals = Text("= ", color=white_color).next_to(eq3_lhs, RIGHT)
        eq3_rhs = Text("(b/2)² - c", color=white_color).next_to(eq3_equals, RIGHT)

        eq3_combined_group = VGroup(eq3_lhs, eq3_equals, eq3_rhs).center().shift(DOWN * 0.5)
        
        self.play(
            ReplacementTransform(VGroup(eq2_x_sq, eq2_plus_b_x, add_b_half_sq_lhs_text), eq3_lhs),
            ReplacementTransform(VGroup(eq2_equals_minus_c, add_b_half_sq_rhs_text), VGroup(eq3_equals, eq3_rhs))
        )
        self.wait(1)
        
        # Take square root
        eq4_lhs = Text("x + b/2", color=blue_color)
        eq4_equals_plus_minus = Text("= ±", color=white_color).next_to(eq4_lhs, RIGHT)
        eq4_rhs_sqrt = Text("√( (b/2)² - c )", color=white_color).next_to(eq4_equals_plus_minus, RIGHT)
        
        eq4_combined_group = VGroup(eq4_lhs, eq4_equals_plus_minus, eq4_rhs_sqrt).center().shift(DOWN * 2)
        
        self.play(
            ReplacementTransform(VGroup(eq3_lhs, eq3_equals, eq3_rhs), eq4_combined_group)
        )

        # Isolate x
        eq5_x = Text("x", color=blue_color)
        eq5_equals = Text("= ", color=white_color).next_to(eq5_x, RIGHT)
        eq5_rhs_term1 = Text("-b/2", color=white_color).next_to(eq5_equals, RIGHT)
        eq5_rhs_term2 = Text(" ± √( (b/2)² - c )", color=white_color).next_to(eq5_rhs_term1, RIGHT)

        eq5_final_group = VGroup(eq5_x, eq5_equals, eq5_rhs_term1, eq5_rhs_term2).center().shift(DOWN * 3.5)
        
        self.play(
            ReplacementTransform(eq4_combined_group, eq5_final_group)
        )
        self.wait(1)

        self.play(FadeOut(eq5_final_group, beat_title, eq1)) # Include eq1_general as well
        # self.current_equation not set here, next beat starts fresh.
        
    def generalization_divide_by_a(self, blue_color, gold_color, white_color):
        current_title = self.current_title
        beat_title = Text("3. Generalize: ax² + bx + c = 0", font_size=35, color=gold_color).next_to(current_title, DOWN, buff=0.4)
        self.play(Write(beat_title))

        # Initial general equation
        eq1_a_x_sq = Text("ax²", color=gold_color)
        eq1_plus_b_x = Text("+ bx", color=gold_color).next_to(eq1_a_x_sq, RIGHT)
        eq1_plus_c = Text("+ c", color=gold_color).next_to(eq1_plus_b_x, RIGHT)
        eq1_equals_0 = Text("= 0", color=white_color).next_to(eq1_plus_c, RIGHT)
        
        eq1_general = VGroup(eq1_a_x_sq, eq1_plus_b_x, eq1_plus_c, eq1_equals_0).center().shift(UP * 2)
        self.play(Write(eq1_general))

        # Displaying the operation
        div_a_symbol = Text(" ÷ a", color=white_color).next_to(eq1_general, RIGHT, buff=0.5)
        self.play(Write(div_a_symbol))

        # x² + (b/a)x + (c/a) = 0
        x_sq_text = Text("x²", color=blue_color)
        
        b_over_a_num = Text("b", color=gold_color)
        b_over_a_den = Text("a", color=gold_color)
        b_over_a_line = Line(LEFT, RIGHT, color=white_color).set_width(max(b_over_a_num.width, b_over_a_den.width) * 1.1)
        b_over_a_num.next_to(b_over_a_line, UP, buff=0.08)
        b_over_a_den.next_to(b_over_a_line, DOWN, buff=0.08)
        b_over_a_frac = VGroup(b_over_a_num, b_over_a_line, b_over_a_den)
        
        c_over_a_num = Text("c", color=gold_color)
        c_over_a_den = Text("a", color=gold_color)
        c_over_a_line = Line(LEFT, RIGHT, color=white_color).set_width(max(c_over_a_num.width, c_over_a_den.width) * 1.1)
        c_over_a_num.next_to(c_over_a_line, UP, buff=0.08)
        c_over_a_den.next_to(c_over_a_line, DOWN, buff=0.08)
        c_over_a_frac = VGroup(c_over_a_num, c_over_a_line, c_over_a_den)

        eq2_div_a = VGroup(
            x_sq_text,
            Text(" + ", color=white_color),
            b_over_a_frac,
            Text("x", color=blue_color),
            Text(" + ", color=white_color),
            c_over_a_frac,
            Text(" = 0", color=white_color)
        ).arrange(RIGHT, buff=0.1).center().shift(UP * 0.8)
        
        self.play(
            ReplacementTransform(eq1_general, eq2_div_a),
            FadeOut(div_a_symbol)
        )

        # Move c/a to RHS
        eq3_move_c = VGroup(
            x_sq_text.copy(),
            Text(" + ", color=white_color),
            b_over_a_frac.copy(),
            Text("x", color=blue_color),
            Text(" = ", color=white_color),
            Text("-", color=white_color),
            c_over_a_frac.copy()
        ).arrange(RIGHT, buff=0.1).center().shift(DOWN * 0.5)

        self.play(ReplacementTransform(eq2_div_a, eq3_move_c))

        # Add (b/2a)² to both sides
        b_over_2a_num = Text("b", color=gold_color)
        b_over_2a_den = Text("2a", color=gold_color)
        b_over_2a_line = Line(LEFT, RIGHT, color=white_color).set_width(max(b_over_2a_num.width, b_over_2a_den.width) * 1.1)
        b_over_2a_num.next_to(b_over_2a_line, UP, buff=0.08)
        b_over_2a_den.next_to(b_over_2a_line, DOWN, buff=0.08)
        b_over_2a_frac = VGroup(b_over_2a_num, b_over_2a_line, b_over_2a_den)
        
        b_over_2a_sq = VGroup(Text("(", color=white_color), b_over_2a_frac, Text(")²", color=white_color)).arrange(RIGHT, buff=0.05)

        eq4_lhs_part = VGroup(x_sq_text.copy(), Text(" + ", color=white_color), b_over_a_frac.copy(), Text("x", color=blue_color)).arrange(RIGHT, buff=0.1)
        eq4_rhs_part = VGroup(Text(" = ", color=white_color), Text("-", color=white_color), c_over_a_frac.copy()).arrange(RIGHT, buff=0.1)

        eq4_lhs_new = VGroup(eq4_lhs_part, Text(" + ", color=white_color), b_over_2a_sq.copy()).arrange(RIGHT, buff=0.1).shift(LEFT*1.5)
        eq4_rhs_new = VGroup(eq4_rhs_part, Text(" + ", color=white_color), b_over_2a_sq.copy()).arrange(RIGHT, buff=0.1).shift(RIGHT*2)

        self.play(
            ReplacementTransform(eq3_move_c, VGroup(eq4_lhs_new[0], eq4_lhs_new[2], eq4_lhs_new[4])), # x^2, b/a x, -c/a are reused
            Write(eq4_lhs_new[1]), Write(eq4_lhs_new[3]), # + and x
            Write(eq4_rhs_new[1]), Write(eq4_rhs_new[3]), # = and -
            Write(eq4_lhs_new[-1]), # (b/2a)^2 LHS
            Write(eq4_rhs_new[-1])  # (b/2a)^2 RHS
        )
        
        # Factor LHS and simplify RHS
        # LHS: (x + b/2a)²
        # RHS: (b/2a)² - c/a = b²/4a² - c/a = (b² - 4ac) / 4a²
        
        factored_lhs = VGroup(
            Text("(", color=white_color),
            Text("x", color=blue_color),
            Text(" + ", color=white_color),
            b_over_2a_frac.copy(),
            Text(")²", color=white_color)
        ).arrange(RIGHT, buff=0.05)

        rhs_num_text = Text("b² - 4ac", color=white_color)
        rhs_den_text = Text("4a²", color=white_color)
        rhs_line = Line(LEFT, RIGHT, color=white_color).set_width(max(rhs_num_text.width, rhs_den_text.width) * 1.1)
        rhs_num_text.next_to(rhs_line, UP, buff=0.08)
        rhs_den_text.next_to(rhs_line, DOWN, buff=0.08)
        rhs_simplified_frac = VGroup(rhs_num_text, rhs_line, rhs_den_text)

        eq5_combined = VGroup(
            factored_lhs,
            Text(" = ", color=white_color),
            rhs_simplified_frac
        ).arrange(RIGHT, buff=0.1).center().shift(DOWN * 1.5)

        self.play(
            FadeOut(eq4_lhs_new, eq4_rhs_new),
            Write(eq5_combined)
        )
        
        self.play(FadeOut(beat_title))
        self.current_equation = eq5_combined 

    def isolate_x_and_simplify(self, blue_color, gold_color, white_color):
        current_title = self.current_title
        beat_title = Text("4. Isolate x & Simplify", font_size=35, color=gold_color).next_to(current_title, DOWN, buff=0.4)
        self.play(Write(beat_title))

        eq_prev = self.current_equation
        self.play(eq_prev.animate.center().shift(UP*2))
        
        # LHS: x + b/2a
        b_over_2a_num = Text("b", color=gold_color)
        b_over_2a_den = Text("2a", color=gold_color)
        b_over_2a_line = Line(LEFT, RIGHT, color=white_color).set_width(max(b_over_2a_num.width, b_over_2a_den.width) * 1.1)
        b_over_2a_num.next_to(b_over_2a_line, UP, buff=0.08)
        b_over_2a_den.next_to(b_over_2a_line, DOWN, buff=0.08)
        b_over_2a_frac = VGroup(b_over_2a_num, b_over_2a_line, b_over_2a_den)

        eq1_lhs = VGroup(
            Text("x", color=blue_color),
            Text(" + ", color=white_color),
            b_over_2a_frac
        ).arrange(RIGHT, buff=0.1)

        eq1_equals_plus_minus = Text(" = ± ", color=white_color)
        
        # RHS: √(b² - 4ac) / 2a
        temp_sqrt_num = Text("√(b² - 4ac)", color=white_color)
        temp_sqrt_den = Text("2a", color=white_color)
        
        max_width = max(temp_sqrt_num.width, temp_sqrt_den.width)
        rhs_frac_line = Line(LEFT, RIGHT, color=white_color).set_width(max_width * 1.1)
        
        temp_sqrt_num.next_to(rhs_frac_line, UP, buff=0.08)
        temp_sqrt_den.next_to(rhs_frac_line, DOWN, buff=0.08)
        
        eq1_rhs_sqrt_frac = VGroup(temp_sqrt_num, rhs_frac_line, temp_sqrt_den)
        
        eq1_combined = VGroup(eq1_lhs, eq1_equals_plus_minus, eq1_rhs_sqrt_frac).arrange(RIGHT, buff=0.1).center().shift(DOWN * 0.5)

        self.play(
            ReplacementTransform(eq_prev, eq1_combined)
        )

        # Isolate x
        # x = (-b ± √(b² - 4ac)) / 2a

        final_numerator_parts = VGroup(
            Text("-b", color=gold_color),
            Text(" ± ", color=white_color),
            Text("√(b² - 4ac)", color=white_color)
        ).arrange(RIGHT, buff=0.1)

        final_denominator_text = Text("2a", color=white_color)
        
        max_width_final = max(final_numerator_parts.width, final_denominator_text.width)
        final_fraction_bar = Line(LEFT, RIGHT, color=white_color).set_width(max_width_final * 1.1)
        
        final_numerator_parts.next_to(final_fraction_bar, UP, buff=0.08)
        final_denominator_text.next_to(final_fraction_bar, DOWN, buff=0.08)

        final_rhs_fraction = VGroup(final_numerator_parts, final_fraction_bar, final_denominator_text)
        
        final_quadratic_formula = VGroup(
            Text("x", color=blue_color),
            Text(" = ", color=white_color),
            final_rhs_fraction
        ).arrange(RIGHT, buff=0.1).center().shift(DOWN * 2)

        self.play(
            ReplacementTransform(eq1_combined, final_quadratic_formula)
        )
        self.wait(1) 
        
        self.play(FadeOut(beat_title))
        self.final_formula = final_quadratic_formula 

    def recap_card(self, blue_color, gold_color, white_color):
        title = self.current_title
        self.play(title.animate.to_edge(UP).scale(1.2/0.8), FadeOut(self.final_formula))

        recap_text = Text("Recap:", font_size=40, color=gold_color).next_to(title, DOWN, buff=0.5).align_to(title, LEFT)
        self.play(Write(recap_text))

        step1 = Text("1. Visualize x² + bx with areas.", font_size=30, color=white_color).next_to(recap_text, DOWN, buff=0.3).align_to(recap_text, LEFT)
        step2 = Text("2. Complete the square by adding (b/2)².", font_size=30, color=white_color).next_to(step1, DOWN, buff=0.2).align_to(step1, LEFT)
        step3 = Text("3. Apply to ax² + bx + c = 0 (divide by a first).", font_size=30, color=white_color).next_to(step2, DOWN, buff=0.2).align_to(step2, LEFT)
        step4 = Text("4. Isolate x by taking square root and simplifying.", font_size=30, color=white_color).next_to(step3, DOWN, buff=0.2).align_to(step3, LEFT)

        self.play(
            LaggedStart(
                Write(step1),
                Write(step2),
                Write(step3),
                Write(step4),
                lag_ratio=0.7
            )
        )
        self.wait(2)

        final_formula_recap = self.final_formula.copy().scale(0.8).next_to(step4, DOWN, buff=0.5)
        self.play(Write(final_formula_recap))
        self.wait(1)

        call_to_action = Text("Practice makes perfect!", font_size=35, color=blue_color).next_to(final_formula_recap, DOWN, buff=0.8)
        self.play(Write(call_to_action))
        self.wait(2)