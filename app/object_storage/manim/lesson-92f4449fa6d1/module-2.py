from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        text_color = BLUE_C
        highlight_color = GOLD_C
        equation_color = BLUE_A # For operators and static parts like '='
        coeff_color = GOLD_C # For coefficients a, b, c

        # --- Helper functions for custom text components without Tex/MathTex ---
        def create_power_text(base_str, power_str, font_size=36, color=equation_color, base_color=equation_color):
            base = Text(base_str, font_size=font_size, color=base_color)
            power = Text(power_str, font_size=font_size * 0.6, color=color) # Smaller font for power
            power.next_to(base.get_corner(UP + RIGHT), buff=0.02).align_to(base, UP) # Position relative to top-right of base
            return VGroup(base, power)

        def create_fraction_text(numerator_mobj, denominator_mobj, line_color=equation_color, scale_factor=0.9):
            line = Line(ORIGIN, ORIGIN, color=line_color) # Placeholder for length
            
            # Create a temporary group to measure combined width for the line
            temp_num_den_group = VGroup(numerator_mobj, denominator_mobj)
            line.set_width(max(temp_num_den_group.width, 0.5)) # Ensure minimum line length
            
            # Arrange numerator, line, and denominator
            numerator_mobj.move_to(ORIGIN) # Reset positions for fresh arrangement
            denominator_mobj.move_to(ORIGIN)
            line.move_to(ORIGIN)

            fraction_group = VGroup(numerator_mobj, line, denominator_mobj)
            numerator_mobj.next_to(line, UP, buff=0.1)
            denominator_mobj.next_to(line, DOWN, buff=0.1)
            
            return fraction_group.scale(scale_factor)

        def create_sqrt_term(content_mobj, symbol_color=equation_color, line_color=equation_color, font_size=36, scale_factor=0.9):
            # Scale content first if it's not already scaled appropriately
            content_mobj_scaled = content_mobj.copy() # Work with a copy to not modify original
            
            # Create symbol and line at a base size, then adjust
            sqrt_symbol = Text("√", font_size=font_size * 1.5, color=symbol_color) # Bigger sqrt symbol
            over_line = Line(ORIGIN, ORIGIN, color=line_color)

            # Position content, then adjust line length and position, then adjust symbol
            content_mobj_scaled.move_to(ORIGIN)
            over_line.set_width(content_mobj_scaled.width + 0.3)
            over_line.next_to(content_mobj_scaled, UP, buff=0.05).set_x(content_mobj_scaled.get_center()[0])

            sqrt_symbol.next_to(over_line, LEFT, buff=0.05).set_y(over_line.get_y())
            
            return VGroup(sqrt_symbol, over_line, content_mobj_scaled).scale(scale_factor)

        # --- Beat 1: Visual Hook & Problem Statement ---
        title = Text("Deriving the Quadratic Formula", font_size=50, color=highlight_color)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": GRAY_D, "include_numbers": False},
        ).to_edge(LEFT)
        
        parabola_func = lambda x: 0.5 * x**2 - 2
        parabola = axes.get_graph(parabola_func, color=equation_color)
        root1_val = -np.sqrt(4)
        root2_val = np.sqrt(4)
        root1 = Dot(axes.c2p(root1_val, 0), color=highlight_color)
        root2 = Dot(axes.c2p(root2_val, 0), color=highlight_color)
        root_label1 = Text("X", font_size=24, color=highlight_color).next_to(root1, DOWN)
        root_label2 = Text("X", font_size=24, color=highlight_color).next_to(root2, DOWN)

        self.play(Create(axes), run_time=1.0)
        self.play(Create(parabola), run_time=1.0)
        self.play(FadeIn(root1, root2, root_label1, root_label2), run_time=0.8)
        self.wait(0.5)

        question = Text("How to find these X values?", font_size=32, color=text_color).next_to(parabola, RIGHT, buff=0.8).shift(UP*0.5)
        self.play(Write(question))
        self.wait(1)

        self.play(FadeOut(axes, parabola, root1, root2, root_label1, root_label2, question), run_time=1)
        self.wait(0.5)

        # Equation 1: ax^2 + bx + c = 0
        eq1_a = Text("a", color=coeff_color)
        eq1_x2 = create_power_text("x", "2", base_color=equation_color)
        eq1_plus1 = Text("+", color=equation_color)
        eq1_b = Text("b", color=coeff_color)
        eq1_x = Text("x", color=equation_color)
        eq1_plus2 = Text("+", color=equation_color)
        eq1_c = Text("c", color=coeff_color)
        eq1_eq = Text("=", color=equation_color)
        eq1_zero = Text("0", color=equation_color)
        
        eq1_ax2_term = VGroup(eq1_a, eq1_x2).arrange(RIGHT, buff=0.05)
        eq1_bx_term = VGroup(eq1_b, eq1_x).arrange(RIGHT, buff=0.05)

        eq1_group = VGroup(eq1_ax2_term, eq1_plus1, eq1_bx_term, eq1_plus2, eq1_c, eq1_eq, eq1_zero).arrange(RIGHT, buff=0.2).scale(0.9)
        self.play(Write(eq1_group), run_time=1.5)
        self.wait(1)

        # --- Beat 2: Isolate X-terms & Prepare for Completing the Square ---
        
        # Equation 2: x^2 + (b/a)x + (c/a) = 0 (after dividing by a)
        eq2_x2 = create_power_text("x", "2", base_color=equation_color)
        eq2_b_over_a = create_fraction_text(Text("b", color=coeff_color), Text("a", color=coeff_color))
        eq2_bx_term = VGroup(eq2_b_over_a, Text("x", color=equation_color)).arrange(RIGHT, buff=0.05)
        eq2_c_over_a = create_fraction_text(Text("c", color=coeff_color), Text("a", color=coeff_color))
        
        eq2_group = VGroup(eq2_x2, eq1_plus1.copy(), eq2_bx_term, eq1_plus2.copy(), eq2_c_over_a, eq1_eq.copy(), eq1_zero.copy()).arrange(RIGHT, buff=0.2).scale(0.9)
        eq2_group.move_to(eq1_group.get_center())

        divide_by_a_label = Text("Divide by 'a'", font_size=28, color=text_color).next_to(eq1_group, DOWN, buff=0.5)
        self.play(
            Write(divide_by_a_label),
            Transform(eq1_group, eq2_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(divide_by_a_label))

        # Equation 3: x^2 + (b/a)x = -c/a (move c/a to right)
        eq3_minus_c_over_a = VGroup(Text("-", color=equation_color), eq2_c_over_a.copy()).arrange(RIGHT, buff=0.05)
        
        eq3_group = VGroup(eq2_x2.copy(), eq1_plus1.copy(), eq2_bx_term.copy(), eq1_eq.copy(), eq3_minus_c_over_a).arrange(RIGHT, buff=0.2).scale(0.9)
        eq3_group.move_to(eq2_group.get_center())

        move_c_label = Text("Move 'c/a' to the right", font_size=28, color=text_color).next_to(eq2_group, DOWN, buff=0.5)
        self.play(
            Write(move_c_label),
            Transform(eq2_group, eq3_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(move_c_label))
        self.wait(0.5)

        # --- Beat 3: Completing the Square - Geometric Intuition & Algebra ---
        self.play(eq3_group.animate.shift(UP*2.5), run_time=1)

        # Geometric Visualization
        square_x_side = 2.0
        b_over_2a_val = 0.8 # Represents a scaled b/2a for visualization

        x_square = Square(side_length=square_x_side, color=equation_color, fill_opacity=0.4).shift(LEFT*1.5 + DOWN*0.5)
        x_label1 = Text("x", font_size=28, color=coeff_color).next_to(x_square, LEFT, buff=0.1)
        x_label2 = Text("x", font_size=28, color=coeff_color).next_to(x_square, DOWN, buff=0.1)

        self.play(Create(x_square), Write(x_label1), Write(x_label2), run_time=1)
        self.wait(0.5)

        # Represent (b/a)x as two rectangles: x * (b/2a)
        half_ba_numerator = Text("b", font_size=28, color=coeff_color)
        half_ba_denominator = Text("2a", font_size=28, color=coeff_color)
        half_ba_fraction = create_fraction_text(half_ba_numerator, half_ba_denominator, scale_factor=0.8)

        rect1 = Rectangle(width=square_x_side, height=b_over_2a_val, color=equation_color, fill_opacity=0.4).next_to(x_square, UP, buff=0)
        rect2 = Rectangle(width=b_over_2a_val, height=square_x_side + b_over_2a_val, color=equation_color, fill_opacity=0.4).next_to(x_square, RIGHT, buff=0)

        b_over_2a_label_top = half_ba_fraction.copy().next_to(rect1, UP, buff=0.1)
        b_over_2a_label_right = half_ba_fraction.copy().next_to(rect2, RIGHT, buff=0.1).shift(UP*0.1) 

        self.play(Create(rect1), Create(rect2), Write(b_over_2a_label_top), Write(b_over_2a_label_right), run_time=1.5)
        self.wait(1)

        # The missing piece (b/2a)^2
        missing_square = Square(side_length=b_over_2a_val, color=highlight_color, fill_opacity=0.6).next_to(rect1, RIGHT, buff=0)
        
        b2_numerator = create_power_text("b", "2", base_color=coeff_color, color=coeff_color)
        four_a2_denominator = VGroup(Text("4", color=equation_color), create_power_text("a", "2", base_color=coeff_color, color=coeff_color)).arrange(RIGHT, buff=0.05)
        missing_label_fraction = create_fraction_text(b2_numerator.copy(), four_a2_denominator.copy(), line_color=highlight_color, scale_factor=0.8).move_to(missing_square.get_center())
        
        complete_square_txt = Text("Complete the Square!", font_size=32, color=text_color).next_to(missing_square, DOWN, buff=0.5)

        self.play(Create(missing_square), Write(missing_label_fraction), Write(complete_square_txt), run_time=1.5)
        self.wait(1)

        # Group everything into the completed square (x + b/2a)^2
        full_square_group = VGroup(x_square, rect1, rect2, missing_square, x_label1, x_label2, b_over_2a_label_top, b_over_2a_label_right, missing_label_fraction)
        self.play(FadeOut(complete_square_txt))
        self.play(full_square_group.animate.scale(0.7).to_edge(LEFT).shift(UP*0.5), run_time=1.5)
        self.wait(0.5)

        # Algebra: Add (b/2a)^2 to both sides
        b_over_2a_text_for_sq = create_fraction_text(Text("b", color=coeff_color), Text("2a", color=coeff_color), scale_factor=0.9)
        b_over_2a_squared_term = VGroup(Text("(", color=equation_color), b_over_2a_text_for_sq, Text(")", color=equation_color), Text("^2", color=equation_color).shift(UP*0.1).scale(0.7)).arrange(RIGHT, buff=0.05).scale(0.8)
        
        plus_b_over_2a_sq_left = VGroup(Text("+", color=equation_color), b_over_2a_squared_term.copy()).arrange(RIGHT, buff=0.1)
        plus_b_over_2a_sq_right = VGroup(Text("+", color=equation_color), b_over_2a_squared_term.copy()).arrange(RIGHT, buff=0.1)

        eq4_left_part = VGroup(eq3_group[0].copy(), eq3_group[1].copy(), eq3_group[2].copy(), plus_b_over_2a_sq_left).arrange(RIGHT, buff=0.1)
        eq4_right_part = VGroup(eq3_group[4].copy(), plus_b_over_2a_sq_right).arrange(RIGHT, buff=0.1)
        eq4_eq_sign = eq3_group[3].copy()

        eq4_group = VGroup(eq4_left_part, eq4_eq_sign, eq4_right_part).arrange(RIGHT, buff=0.2).scale(0.9)
        eq4_group.move_to(ORIGIN).shift(RIGHT*1.5 + UP*1)

        add_sq_label = Text("Add (b/2a)^2 to both sides", font_size=28, color=text_color).next_to(eq3_group, DOWN, buff=0.5)
        self.play(
            Write(add_sq_label),
            Transform(eq3_group, eq4_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(add_sq_label))

        # Simplify left side: (x + b/2a)^2
        x_plus_b_over_2a_term = VGroup(
            Text("x", color=equation_color),
            Text("+", color=equation_color),
            create_fraction_text(Text("b", color=coeff_color), Text("2a", color=coeff_color), scale_factor=0.9)
        ).arrange(RIGHT, buff=0.05)
        
        eq5_left_part = VGroup(Text("(", color=equation_color), x_plus_b_over_2a_term, Text(")", color=equation_color), Text("^2", color=equation_color).shift(UP*0.1).scale(0.7)).arrange(RIGHT, buff=0.05).scale(0.8)
        
        eq5_right_part = eq4_right_part.copy()
        eq5_eq_sign = eq4_eq_sign.copy()

        eq5_group = VGroup(eq5_left_part, eq5_eq_sign, eq5_right_part).arrange(RIGHT, buff=0.2).scale(0.9)
        eq5_group.move_to(eq4_group.get_center())

        simplify_left_label = Text("Simplify left side", font_size=28, color=text_color).next_to(eq4_group, DOWN, buff=0.5)
        self.play(
            Write(simplify_left_label),
            Transform(eq4_group, eq5_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(simplify_left_label))
        self.wait(0.5)

        # --- Beat 4: Solving for X ---
        self.play(FadeOut(full_square_group), run_time=0.5) 
        self.play(eq5_group.animate.shift(UP*2), run_time=1)

        # Equation 6: x + b/2a = +/- sqrt(-c/a + (b/2a)^2)
        eq6_x_plus_b_over_2a = x_plus_b_over_2a_term.copy()
        
        eq6_plus_minus = Text("±", color=equation_color).scale(0.9)
        eq6_sqrt_content = eq5_group[2].copy() # The -c/a + (b/2a)^2 part
        eq6_sqrt_term = create_sqrt_term(eq6_sqrt_content, font_size=36, scale_factor=0.8)

        eq6_right_part = VGroup(eq6_plus_minus, eq6_sqrt_term).arrange(RIGHT, buff=0.1)

        eq6_group = VGroup(eq6_x_plus_b_over_2a, eq5_eq_sign.copy(), eq6_right_part).arrange(RIGHT, buff=0.2).scale(0.9)
        eq6_group.move_to(eq5_group.get_center())

        take_sqrt_label = Text("Take square root of both sides", font_size=28, color=text_color).next_to(eq5_group, DOWN, buff=0.5)
        self.play(
            Write(take_sqrt_label),
            Transform(eq5_group, eq6_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(take_sqrt_label))

        # Simplify the right side under the square root
        b2_minus_4ac_num = VGroup(
            create_power_text("b", "2", base_color=coeff_color, color=coeff_color), Text("-", color=equation_color), Text("4", color=equation_color),
            Text("a", color=coeff_color), Text("c", color=coeff_color)
        ).arrange(RIGHT, buff=0.05).scale(0.8)
        four_a2_den = VGroup(Text("4", color=equation_color), create_power_text("a", "2", base_color=coeff_color, color=coeff_color)).arrange(RIGHT, buff=0.05).scale(0.8)
        
        simplified_fraction_content = create_fraction_text(b2_minus_4ac_num, four_a2_den, scale_factor=0.9)
        eq7_sqrt_term = create_sqrt_term(simplified_fraction_content, font_size=36, scale_factor=0.8)
        
        eq7_right_part = VGroup(eq6_plus_minus.copy(), eq7_sqrt_term).arrange(RIGHT, buff=0.1)
        eq7_group = VGroup(eq6_x_plus_b_over_2a.copy(), eq5_eq_sign.copy(), eq7_right_part).arrange(RIGHT, buff=0.2).scale(0.9)
        eq7_group.move_to(eq6_group.get_center())

        simplify_right_label = Text("Simplify under the root", font_size=28, color=text_color).next_to(eq6_group, DOWN, buff=0.5)
        self.play(
            Write(simplify_right_label),
            Transform(eq6_group, eq7_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(simplify_right_label))

        # Take sqrt of denominator: sqrt(4a^2) = 2a
        final_sqrt_numerator_content = b2_minus_4ac_num.copy()
        final_sqrt_den = VGroup(Text("2", color=equation_color), Text("a", color=coeff_color)).arrange(RIGHT, buff=0.05).scale(0.8)
        
        final_sqrt_term_frac_num = create_sqrt_term(final_sqrt_numerator_content, font_size=28, scale_factor=0.8) # sqrt only on numerator, smaller sqrt symbol
        
        final_sqrt_fraction_term = create_fraction_text(final_sqrt_term_frac_num, final_sqrt_den, scale_factor=0.9)

        eq8_right_part = VGroup(eq6_plus_minus.copy(), final_sqrt_fraction_term).arrange(RIGHT, buff=0.1)
        eq8_group = VGroup(eq6_x_plus_b_over_2a.copy(), eq5_eq_sign.copy(), eq8_right_part).arrange(RIGHT, buff=0.2).scale(0.9)
        eq8_group.move_to(eq7_group.get_center())

        take_sqrt_denom_label = Text("√ of denominator (2a)", font_size=28, color=text_color).next_to(eq7_group, DOWN, buff=0.5)
        self.play(
            Write(take_sqrt_denom_label),
            Transform(eq7_group, eq8_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(take_sqrt_denom_label))

        # Isolate x: x = -b/2a +/- sqrt(b^2 - 4ac) / 2a
        minus_b_over_2a_term = VGroup(Text("-", color=equation_color), create_fraction_text(Text("b", color=coeff_color), Text("2a", color=coeff_color), scale_factor=0.9)).arrange(RIGHT, buff=0.05)

        eq9_x_alone = Text("x", color=equation_color)
        eq9_right_part = VGroup(minus_b_over_2a_term, eq8_right_part.copy()).arrange(RIGHT, buff=0.1)
        
        eq9_group = VGroup(eq9_x_alone, eq5_eq_sign.copy(), eq9_right_part).arrange(RIGHT, buff=0.2).scale(0.9)
        eq9_group.move_to(eq8_group.get_center())

        isolate_x_label = Text("Isolate 'x'", font_size=28, color=text_color).next_to(eq8_group, DOWN, buff=0.5)
        self.play(
            Write(isolate_x_label),
            Transform(eq8_group, eq9_group, run_time=1.5)
        )
        self.wait(1)
        self.play(FadeOut(isolate_x_label))

        # Combine into single fraction
        # x = (-b +/- sqrt(b^2 - 4ac)) / 2a
        final_num_term = VGroup(
            Text("-", color=equation_color), Text("b", color=coeff_color), eq6_plus_minus.copy(),
            create_sqrt_term(b2_minus_4ac_num.copy(), font_size=28, scale_factor=0.8)
        ).arrange(RIGHT, buff=0.05).scale(0.8)

        final_den_term = VGroup(Text("2", color=equation_color), Text("a", color=coeff_color)).arrange(RIGHT, buff=0.05).scale(0.8)
        
        final_fraction_combined = create_fraction_text(final_num_term, final_den_term, line_color=equation_color, scale_factor=1.0) # Larger scale for final formula

        quadratic_formula_final = VGroup(
            Text("x", color=equation_color),
            Text("=", color=equation_color),
            final_fraction_combined
        ).arrange(RIGHT, buff=0.2).scale(0.9)
        quadratic_formula_final.move_to(eq9_group.get_center())

        combine_terms_label = Text("Combine terms", font_size=28, color=text_color).next_to(eq9_group, DOWN, buff=0.5)
        self.play(
            Write(combine_terms_label),
            Transform(eq9_group, quadratic_formula_final, run_time=1.5)
        )
        self.wait(2)
        self.play(FadeOut(combine_terms_label))
        self.wait(1)

        # --- Beat 5: Recap Card ---
        self.play(FadeOut(title))
        self.play(quadratic_formula_final.animate.scale(1.5).move_to(ORIGIN), run_time=1.5)

        recap_text1 = Text("The Quadratic Formula!", font_size=40, color=highlight_color).next_to(quadratic_formula_final, UP, buff=1)
        recap_text2 = Text("Solves for X when ax^2 + bx + c = 0", font_size=32, color=text_color).next_to(quadratic_formula_final, DOWN, buff=1)

        self.play(Write(recap_text1), Write(recap_text2), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(quadratic_formula_final, recap_text1, recap_text2), run_time=1)
        self.wait(1)