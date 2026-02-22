from manim import *

# Custom color palette (3Blue1Brown inspired)
BLUE_COLOR = BLUE_E
GOLD_COLOR = GOLD_E
PRIMARY_TEXT_COLOR = WHITE
SECONDARY_TEXT_COLOR = GRAY_A

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        self.camera.background_color = "#202020" # A darker background

        # --- Beat 1: The Visual Hook & Introducing the Problem ---
        # 1. Visual Hook: A simple parabola and its roots
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 6, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": SECONDARY_TEXT_COLOR}
        ).shift(DOWN * 0.5)
        
        # A simple parabola: y = 0.5x^2 - 0.5x - 2
        parabola_func = lambda x: 0.5 * x**2 - 0.5 * x - 2
        parabola = always_redraw(
            lambda: FunctionGraph(
                parabola_func,
                x_range=[-3.5, 4.5],
                color=BLUE_COLOR
            )
        )
        
        # Approximate x-intercepts for the example parabola
        x_intercept_1 = Dot(plane.c2p(-1.56, 0), color=GOLD_COLOR, radius=0.08)
        x_intercept_2 = Dot(plane.c2p(2.56, 0), color=GOLD_COLOR, radius=0.08)

        intro_title = Text("Deriving the Quadratic Formula", font_size=50, color=PRIMARY_TEXT_COLOR).to_edge(UP).shift(DOWN*0.5)
        
        # Build the equation ax^2 + bx + c = 0 using Text
        a_txt = Text("a", color=GOLD_COLOR, font_size=40)
        x2_txt = Text("x", color=PRIMARY_TEXT_COLOR, font_size=40).next_to(a_txt, RIGHT, buff=0.1)
        _2_super = Text("2", color=PRIMARY_TEXT_COLOR, font_size=20).align_to(x2_txt, UP).shift(RIGHT*0.1)
        plus_b_txt = Text("+ b", color=BLUE_COLOR, font_size=40).next_to(x2_txt, RIGHT, buff=0.1)
        x_txt = Text("x", color=PRIMARY_TEXT_COLOR, font_size=40).next_to(plus_b_txt, RIGHT, buff=0.1)
        plus_c_txt = Text("+ c", color=GOLD_COLOR, font_size=40).next_to(x_txt, RIGHT, buff=0.1)
        eq_0_txt = Text("= 0", color=PRIMARY_TEXT_COLOR, font_size=40).next_to(plus_c_txt, RIGHT, buff=0.1)

        equation_mobj = VGroup(a_txt, x2_txt, _2_super, plus_b_txt, x_txt, plus_c_txt, eq_0_txt)
        equation_mobj.move_to(ORIGIN).shift(UP * 2)

        goal_text = Text("Find 'x' that makes this true.", color=SECONDARY_TEXT_COLOR, font_size=30).next_to(equation_mobj, DOWN, buff=0.5)

        self.play(
            FadeIn(intro_title),
            Create(plane),
            Create(parabola),
            GrowFromCenter(x_intercept_1),
            GrowFromCenter(x_intercept_2),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            FadeOut(plane, shift=UP),
            FadeOut(parabola, shift=UP),
            FadeOut(x_intercept_1, shift=UP),
            FadeOut(x_intercept_2, shift=UP),
            Transform(intro_title, Text("The General Quadratic Equation", font_size=50, color=PRIMARY_TEXT_COLOR).to_edge(UP).shift(DOWN*0.5)),
            run_time=1.5
        )
        self.play(
            Write(equation_mobj),
            Write(goal_text),
            run_time=2
        )
        self.wait(1)

        # --- Beat 2: Isolating the x terms (Divide by 'a' and move 'c') ---
        self.play(FadeOut(goal_text))

        current_eq_beat2_start = equation_mobj.copy()
        self.play(current_eq_beat2_start.animate.shift(UP * 2))

        divide_a_text = Text("Divide all terms by 'a'", color=SECONDARY_TEXT_COLOR, font_size=25).next_to(current_eq_beat2_start, DOWN, buff=0.3)
        self.play(Write(divide_a_text))
        self.wait(0.5)

        # x^2 + (b/a)x + (c/a) = 0
        x2_new = Text("x", color=PRIMARY_TEXT_COLOR, font_size=40)
        _2_super_new = Text("2", color=PRIMARY_TEXT_COLOR, font_size=20).align_to(x2_new, UP).shift(RIGHT*0.1)
        
        b_over_a = Fraction(Text("b", color=BLUE_COLOR, font_size=40), Text("a", color=GOLD_COLOR, font_size=40))
        b_over_a_x = VGroup(b_over_a, Text("x", color=PRIMARY_TEXT_COLOR, font_size=40)).arrange(RIGHT, buff=0.1)
        
        c_over_a = Fraction(Text("c", color=GOLD_COLOR, font_size=40), Text("a", color=GOLD_COLOR, font_size=40))
        
        new_eq_terms = VGroup(
            VGroup(x2_new, _2_super_new),
            Text(" + ", color=PRIMARY_TEXT_COLOR, font_size=40),
            b_over_a_x,
            Text(" + ", color=PRIMARY_TEXT_COLOR, font_size=40),
            c_over_a,
            Text(" = 0", color=PRIMARY_TEXT_COLOR, font_size=40)
        ).arrange(RIGHT, buff=0.1).move_to(ORIGIN)

        self.play(
            FadeOut(divide_a_text),
            ReplacementTransform(current_eq_beat2_start, new_eq_terms)
        )
        self.wait(1)

        # Move c/a to the right side
        move_c_text = Text("Move constant 'c/a' to the right side", color=SECONDARY_TEXT_COLOR, font_size=25).next_to(new_eq_terms, DOWN, buff=0.3)
        self.play(Write(move_c_text))
        self.wait(0.5)

        minus_c_over_a = VGroup(Text("-", color=PRIMARY_TEXT_COLOR, font_size=40), c_over_a.copy()).arrange(RIGHT, buff=0.05)
        
        # Reconstruct the equation with -c/a on the right
        final_eq_beat2_lhs = VGroup(
            new_eq_terms[0].copy(),
            new_eq_terms[1].copy(),
            new_eq_terms[2].copy()
        ).arrange(RIGHT, buff=0.1)

        final_eq_beat2_rhs = VGroup(
            Text(" = ", color=PRIMARY_TEXT_COLOR, font_size=40),
            minus_c_over_a
        ).arrange(RIGHT, buff=0.1)
        
        final_eq_beat2_combined = VGroup(final_eq_beat2_lhs, final_eq_beat2_rhs).arrange(RIGHT, buff=0.1).move_to(ORIGIN).shift(UP*2)

        self.play(
            FadeOut(new_eq_terms[3]), # The '+' before c/a
            FadeOut(new_eq_terms[4]), # c/a
            FadeOut(new_eq_terms[5]), # '= 0'
            FadeOut(move_c_text),
            ReplacementTransform(VGroup(new_eq_terms[0], new_eq_terms[1], new_eq_terms[2]), final_eq_beat2_lhs),
            FadeIn(final_eq_beat2_rhs),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 3: Completing the Square (Visual Intuition) ---
        title_beat3 = Text("Completing the Square", color=PRIMARY_TEXT_COLOR, font_size=45).to_edge(UP).shift(DOWN*0.5)
        self.play(ReplacementTransform(intro_title, title_beat3), final_eq_beat2_combined.animate.scale(0.8).to_corner(UP + LEFT))

        # Visual representation of x^2
        x_square = Square(side_length=2, color=BLUE_COLOR, fill_opacity=0.5).shift(LEFT * 3)
        x_label_left = Text("x", color=PRIMARY_TEXT_COLOR, font_size=30).next_to(x_square.get_left(), LEFT).shift(RIGHT*0.1)
        x_label_top = Text("x", color=PRIMARY_TEXT_COLOR, font_size=30).next_to(x_square.get_top(), UP).shift(DOWN*0.1)

        self.play(
            Create(x_square),
            Write(x_label_left), Write(x_label_top)
        )
        self.wait(0.5)

        # Split the `(b/a)x` term into two halves for completing the square
        rect_width_val = 1.2 # Representative value for (b/a) for visual
        rect_side_val = 2 # height/width = x
        
        # Side rectangle (x * (b/2a))
        x_side_rect = Rectangle(width=rect_width_val/2, height=rect_side_val, color=GOLD_COLOR, fill_opacity=0.5).next_to(x_square, RIGHT, buff=0)
        
        # Bottom rectangle (x * (b/2a))
        x_bottom_rect = Rectangle(width=rect_side_val, height=rect_width_val/2, color=GOLD_COLOR, fill_opacity=0.5).next_to(x_square, DOWN, buff=0)

        # Labels for (b/2a)
        b_over_2a_label = Fraction(Text("b", color=BLUE_COLOR, font_size=25), VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=25), Text("a", color=GOLD_COLOR, font_size=25)).arrange(RIGHT, buff=0.05))

        b_over_2a_label_right = b_over_2a_label.copy().next_to(x_side_rect.get_top(), UP, buff=0.1)
        b_over_2a_label_bottom = b_over_2a_label.copy().next_to(x_bottom_rect.get_left(), LEFT, buff=0.1).rotate(PI/2)

        self.play(
            Create(x_side_rect),
            Create(x_bottom_rect),
            Write(b_over_2a_label_right),
            Write(b_over_2a_label_bottom)
        )
        self.wait(0.5)

        # The missing piece to complete the square: ((b/2a))^2
        missing_square = Square(side_length=rect_width_val/2, color=BLUE_COLOR, fill_opacity=0.8).next_to(x_side_rect, DOWN, buff=0)
        
        b_over_2a_sq_label_content = Fraction(Text("b", color=BLUE_COLOR, font_size=20), VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=20), Text("a", color=GOLD_COLOR, font_size=20)).arrange(RIGHT, buff=0.05))
        b_over_2a_sq_label = VGroup(
            Text("(", color=PRIMARY_TEXT_COLOR, font_size=30),
            b_over_2a_sq_label_content,
            Text(")", color=PRIMARY_TEXT_COLOR, font_size=30),
            Text("2", color=PRIMARY_TEXT_COLOR, font_size=15).align_to(Text(")", font_size=30), UP).shift(RIGHT*0.05)
        ).arrange(RIGHT, buff=0.05)
        
        b_over_2a_sq_label.move_to(missing_square.get_center())

        self.play(
            Create(missing_square),
            Write(b_over_2a_sq_label)
        )
        self.wait(0.5)

        all_geometric_parts = VGroup(x_square, x_side_rect, x_bottom_rect, missing_square, 
                                     x_label_left, x_label_top, b_over_2a_label_right, 
                                     b_over_2a_label_bottom, b_over_2a_sq_label)
        
        # Show (x + b/2a)^2 algebraically
        total_square_text_lhs = VGroup(
            Text("(", color=PRIMARY_TEXT_COLOR, font_size=50),
            Text("x", color=PRIMARY_TEXT_COLOR, font_size=40),
            Text(" + ", color=PRIMARY_TEXT_COLOR, font_size=40),
            Fraction(Text("b", color=BLUE_COLOR, font_size=40), VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=40), Text("a", color=GOLD_COLOR, font_size=40)).arrange(RIGHT, buff=0.05)),
            Text(")", color=PRIMARY_TEXT_COLOR, font_size=50),
            Text("2", color=PRIMARY_TEXT_COLOR, font_size=20).align_to(Text(")", font_size=50), UP).shift(RIGHT*0.1)
        ).arrange(RIGHT, buff=0.05)
        total_square_text_lhs.next_to(all_geometric_parts, RIGHT, buff=1.5).shift(UP*0.5)
        
        self.play(
            all_geometric_parts.animate.scale(0.8).shift(LEFT*2.5),
            Write(total_square_text_lhs)
        )
        self.wait(1)

        # Apply to the equation: add ((b/2a))^2 to both sides
        add_b2a_sq_text = Text("Add ((b/2a))^2 to both sides", color=SECONDARY_TEXT_COLOR, font_size=25).next_to(final_eq_beat2_combined, DOWN, buff=0.3)
        self.play(Write(add_b2a_sq_text))
        
        # Left Side (x + b/2a)^2
        lhs_transformed_eq = total_square_text_lhs.copy().to_edge(LEFT).shift(UP*1.5)

        # Right Side = -c/a + (b/2a)^2
        b_over_2a_sq_for_rhs = VGroup(
            Text(" + ", color=PRIMARY_TEXT_COLOR, font_size=35),
            Fraction(Text("b", color=BLUE_COLOR, font_size=35), VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=35), Text("a", color=GOLD_COLOR, font_size=35)).arrange(RIGHT, buff=0.05)),
            Text("2", color=PRIMARY_TEXT_COLOR, font_size=18).align_to(Fraction(Text("b"), VGroup(Text("2"), Text("a"))), UP).shift(RIGHT*0.08)
        ).arrange(RIGHT, buff=0.05)

        rhs_transformed_eq = VGroup(
            final_eq_beat2_combined[1].copy(), # The "= -c/a" part
            b_over_2a_sq_for_rhs
        ).arrange(RIGHT, buff=0.05).next_to(lhs_transformed_eq, RIGHT, buff=0.1)
        
        self.play(
            FadeOut(final_eq_beat2_combined),
            FadeOut(add_b2a_sq_text),
            FadeOut(total_square_text_lhs), # It's transformed into lhs_transformed_eq
            ReplacementTransform(final_eq_beat2_combined[0], lhs_transformed_eq), # Transform lhs part
            FadeIn(rhs_transformed_eq) # Fade in the new RHS part
        )
        self.wait(1)

        # Clean up visual squares
        self.play(
            FadeOut(all_geometric_parts),
            FadeOut(title_beat3)
        )
        self.wait(0.5)

        # --- Beat 4: Simplifying the Right Side ---
        title_beat4 = Text("Simplify the Right Side", color=PRIMARY_TEXT_COLOR, font_size=45).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(title_beat4))

        current_eq_lhs = lhs_transformed_eq.copy().to_edge(LEFT).shift(UP*1.5)
        current_eq_rhs = rhs_transformed_eq.copy().next_to(current_eq_lhs, RIGHT, buff=0.1)
        self.add(current_eq_lhs, current_eq_rhs)

        # Expand (b/2a)^2 to b^2/(4a^2)
        b_sq = VGroup(Text("b", color=BLUE_COLOR, font_size=35), Text("2", font_size=18).align_to(Text("b"), UP).shift(RIGHT*0.05))
        four_a_sq = VGroup(Text("4", color=PRIMARY_TEXT_COLOR, font_size=35), Text("a", color=GOLD_COLOR, font_size=35), Text("2", font_size=18).align_to(Text("a"), UP).shift(RIGHT*0.05))
        b_sq_over_4a_sq_frac = Fraction(b_sq, four_a_sq).scale(0.8) # Adjusted scale for fit
        
        expanded_b_sq_rhs_frac_mobj = VGroup(
            Text(" + ", color=PRIMARY_TEXT_COLOR, font_size=35),
            b_sq_over_4a_sq_frac
        ).arrange(RIGHT, buff=0.05)
        
        simplified_rhs_part1 = VGroup(current_eq_rhs[0].copy(), current_eq_rhs[1][0].copy(), current_eq_rhs[1][1].copy()).arrange(RIGHT, buff=0.05) # = -c/a
        
        self.play(
            FadeOut(current_eq_rhs[1]), # Old (b/2a)^2 term
            ReplacementTransform(current_eq_rhs[2], expanded_b_sq_rhs_frac_mobj),
            # reposition the entire RHS after transformation
            simplified_rhs_part1.animate.next_to(current_eq_lhs, RIGHT, buff=0.1)
        )
        self.wait(1)

        # Combine fractions: -c/a + b^2/(4a^2)
        # Need common denominator 4a^2
        multiply_4a = Text("Find common denominator: 4a^2", color=SECONDARY_TEXT_COLOR, font_size=25).next_to(current_eq_lhs, DOWN, buff=0.3)
        self.play(Write(multiply_4a))
        self.wait(0.5)

        neg_4ac_num = VGroup(Text("-", color=PRIMARY_TEXT_COLOR), Text("4", color=PRIMARY_TEXT_COLOR), Text("a", color=GOLD_COLOR), Text("c", color=GOLD_COLOR)).scale(0.9)
        four_a_sq_denom_val = VGroup(Text("4", color=PRIMARY_TEXT_COLOR), Text("a", color=GOLD_COLOR), Text("2", font_size=18).align_to(Text("a"), UP).shift(RIGHT*0.05)).scale(0.9)
        
        neg_4ac_over_4a_sq = Fraction(neg_4ac_num, four_a_sq_denom_val)

        rhs_combining_lhs = VGroup(Text(" = ", color=PRIMARY_TEXT_COLOR, font_size=35), neg_4ac_over_4a_sq).arrange(RIGHT, buff=0.05)
        rhs_combining_rhs = VGroup(Text(" + ", color=PRIMARY_TEXT_COLOR, font_size=35), b_sq_over_4a_sq_frac.copy()).arrange(RIGHT, buff=0.05)
        
        rhs_combining = VGroup(rhs_combining_lhs, rhs_combining_rhs).arrange(RIGHT, buff=0.05).next_to(current_eq_lhs, RIGHT, buff=0.1)

        self.play(
            FadeOut(simplified_rhs_part1),
            FadeOut(expanded_b_sq_rhs_frac_mobj),
            FadeOut(multiply_4a),
            FadeIn(rhs_combining)
        )
        self.wait(1)

        # Combine into a single fraction
        b_sq_minus_4ac_num = VGroup(
            Text("b", color=BLUE_COLOR, font_size=35),
            Text("2", font_size=18).align_to(Text("b"), UP).shift(RIGHT*0.05),
            Text(" - ", color=PRIMARY_TEXT_COLOR, font_size=35),
            Text("4", color=PRIMARY_TEXT_COLOR, font_size=35),
            Text("a", color=GOLD_COLOR, font_size=35),
            Text("c", color=GOLD_COLOR, font_size=35)
        ).arrange(RIGHT, buff=0.05)
        
        final_rhs_fraction_combined = Fraction(b_sq_minus_4ac_num, four_a_sq_denom_val.copy()).scale(0.8)
        
        final_rhs_group_beat4 = VGroup(Text(" = ", color=PRIMARY_TEXT_COLOR, font_size=40), final_rhs_fraction_combined).arrange(RIGHT, buff=0.05).next_to(current_eq_lhs, RIGHT, buff=0.1)

        self.play(
            FadeOut(rhs_combining),
            FadeIn(final_rhs_group_beat4)
        )
        self.wait(1)

        # Move equation to center for next step
        final_equation_beat4 = VGroup(current_eq_lhs, final_rhs_group_beat4).center().shift(UP*1)
        self.play(
            FadeOut(title_beat4),
            Transform(current_eq_lhs, final_equation_beat4[0]),
            Transform(final_rhs_group_beat4, final_equation_beat4[1])
        )
        self.wait(0.5)
        
        current_eq_lhs_beat5 = final_equation_beat4[0]
        current_eq_rhs_beat5 = final_equation_beat4[1]


        # --- Beat 5: Taking the Square Root & Solving for x ---
        title_beat5 = Text("Take Square Root & Isolate 'x'", color=PRIMARY_TEXT_COLOR, font_size=45).to_edge(UP).shift(DOWN*0.5)
        self.play(FadeIn(title_beat5))

        # Take square root of both sides
        sqrt_text_explanation = Text("Take square root of both sides", color=SECONDARY_TEXT_COLOR, font_size=25).next_to(current_eq_lhs_beat5, DOWN, buff=0.3)
        self.play(Write(sqrt_text_explanation))

        # LHS: x + b/2a
        lhs_after_sqrt_applied = VGroup(
            Text("x", color=PRIMARY_TEXT_COLOR, font_size=40),
            Text(" + ", color=PRIMARY_TEXT_COLOR, font_size=40),
            Fraction(Text("b", color=BLUE_COLOR, font_size=40), VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=40), Text("a", color=GOLD_COLOR, font_size=40)).arrange(RIGHT, buff=0.05))
        ).arrange(RIGHT, buff=0.05).to_edge(LEFT).shift(UP*1.5)
        
        # RHS: +/- sqrt((b^2 - 4ac) / (4a^2))
        plus_minus_symbol = Text("±", color=PRIMARY_TEXT_COLOR, font_size=40)
        
        # The numerator content: b^2 - 4ac
        rhs_sqrt_numerator_content = b_sq_minus_4ac_num.copy().scale(0.9) 

        # Create the radical symbol visually over the numerator content
        radical_hat_line = Line(ORIGIN, RIGHT * (rhs_sqrt_numerator_content.width + 0.3), color=PRIMARY_TEXT_COLOR)
        radical_hat_line.next_to(rhs_sqrt_numerator_content, UP, buff=0.1)
        
        radical_tick_part = VGroup(
            Line(ORIGIN, DR * 0.15, color=PRIMARY_TEXT_COLOR),
            Line(DR * 0.15, UP * 0.3 + RIGHT * 0.1, color=PRIMARY_TEXT_COLOR)
        ).scale(0.6)
        radical_tick_part.next_to(radical_hat_line.get_left(), LEFT, buff=-0.05).align_to(radical_hat_line, DOWN).shift(UP*0.05)
        
        radical_numerator_visual_group = VGroup(radical_tick_part, radical_hat_line, rhs_sqrt_numerator_content)
        
        # The denominator content: sqrt(4a^2) = 2a
        rhs_sqrt_denominator_content = VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=40), Text("a", color=GOLD_COLOR, font_size=40)).arrange(RIGHT, buff=0.05).scale(0.9)

        # The fraction line for the simplified RHS
        fraction_line_rhs_final = Line(ORIGIN, RIGHT * max(radical_numerator_visual_group.width, rhs_sqrt_denominator_content.width), color=PRIMARY_TEXT_COLOR)
        fraction_line_rhs_final.set_width(max(radical_numerator_visual_group.width, rhs_sqrt_denominator_content.width) * 1.1)
        radical_numerator_visual_group.next_to(fraction_line_rhs_final, UP, buff=0.2)
        rhs_sqrt_denominator_content.next_to(fraction_line_rhs_final, DOWN, buff=0.2)
        
        rhs_sqrt_fraction_assembled = VGroup(
            radical_numerator_visual_group,
            fraction_line_rhs_final,
            rhs_sqrt_denominator_content
        ).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        
        rhs_group_after_sqrt_applied = VGroup(
            Text(" = ", color=PRIMARY_TEXT_COLOR, font_size=40),
            plus_minus_symbol,
            rhs_sqrt_fraction_assembled
        ).arrange(RIGHT, buff=0.05).next_to(lhs_after_sqrt_applied, RIGHT, buff=0.1)

        self.play(
            FadeOut(current_eq_lhs_beat5),
            FadeOut(current_eq_rhs_beat5),
            FadeOut(sqrt_text_explanation),
            FadeIn(lhs_after_sqrt_applied),
            FadeIn(rhs_group_after_sqrt_applied)
        )
        self.wait(1)

        # Isolate x: Move b/2a to the right side
        isolate_x_text = Text("Isolate 'x' by moving b/2a", color=SECONDARY_TEXT_COLOR, font_size=25).next_to(lhs_after_sqrt_applied, DOWN, buff=0.3)
        self.play(Write(isolate_x_text))

        # -b/2a
        neg_b_over_2a_part = VGroup(
            Text("-", color=PRIMARY_TEXT_COLOR, font_size=40),
            Fraction(Text("b", color=BLUE_COLOR, font_size=40), VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=40), Text("a", color=GOLD_COLOR, font_size=40)).arrange(RIGHT, buff=0.05))
        ).arrange(RIGHT, buff=0.05).scale(0.9)

        # x = ...
        x_equals_lhs = Text("x = ", color=PRIMARY_TEXT_COLOR, font_size=40).to_edge(LEFT).shift(UP*1.5)
        
        final_formula_rhs_combined = VGroup(
            neg_b_over_2a_part,
            plus_minus_symbol.copy(),
            rhs_sqrt_fraction_assembled.copy() # Reuse the assembled sqrt fraction
        ).arrange(RIGHT, buff=0.05).next_to(x_equals_lhs, RIGHT, buff=0.1)

        self.play(
            Transform(lhs_after_sqrt_applied[0], x_equals_lhs[0]), # x
            FadeOut(lhs_after_sqrt_applied[1]), # +
            FadeOut(lhs_after_sqrt_applied[2]), # b/2a
            ReplacementTransform(rhs_group_after_sqrt_applied[0], x_equals_lhs[1]), # =
            Transform(rhs_group_after_sqrt_applied[1], final_formula_rhs_combined[1]), # +-
            Transform(rhs_group_after_sqrt_applied[2], final_formula_rhs_combined[2]), # sqrt(...) / ...
            FadeIn(final_formula_rhs_combined[0]), # -b/2a
            FadeOut(isolate_x_text)
        )
        self.wait(1)

        # Combine into one fraction
        final_numerator_full = VGroup(
            Text("-", color=PRIMARY_TEXT_COLOR, font_size=40),
            Text("b", color=BLUE_COLOR, font_size=40),
            plus_minus_symbol.copy(),
            radical_numerator_visual_group.copy() # The sqrt(b^2-4ac) part
        ).arrange(RIGHT, buff=0.05).scale(0.9)

        final_denominator_full = VGroup(Text("2", color=PRIMARY_TEXT_COLOR, font_size=40), Text("a", color=GOLD_COLOR, font_size=40)).arrange(RIGHT, buff=0.05).scale(0.9)
        
        final_formula_division_line = Line(ORIGIN, RIGHT * max(final_numerator_full.width, final_denominator_full.width)*1.1, color=PRIMARY_TEXT_COLOR)
        final_numerator_full.next_to(final_formula_division_line, UP, buff=0.2)
        final_denominator_full.next_to(final_formula_division_line, DOWN, buff=0.2)

        final_quadratic_formula_assembled = VGroup(
            final_numerator_full,
            final_formula_division_line,
            final_denominator_full
        ).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        
        final_formula_mobj = VGroup(Text("x = ", color=PRIMARY_TEXT_COLOR, font_size=45), final_quadratic_formula_assembled).arrange(RIGHT, buff=0.1).center()

        self.play(
            FadeOut(x_equals_lhs[0]),
            FadeOut(final_formula_rhs_combined[0]), # -b/2a
            FadeOut(final_formula_rhs_combined[1]), # +-
            FadeOut(final_formula_rhs_combined[2]), # sqrt(b^2-4ac)/2a
            Transform(title_beat5, Text("The Quadratic Formula!", color=PRIMARY_TEXT_COLOR, font_size=50).to_edge(UP).shift(DOWN*0.5)),
            Write(final_formula_mobj),
            run_time=2
        )
        self.wait(2)


        # --- Recap Card ---
        self.play(FadeOut(final_formula_mobj), FadeOut(title_beat5))

        recap_title = Text("Recap: Deriving the Quadratic Formula", font_size=45, color=GOLD_COLOR).to_edge(UP).shift(DOWN*0.5)
        
        # Manually create the bullet points to handle superscript
        bullet1_text_part1 = Text("1. Start with ax", font_size=35, color=PRIMARY_TEXT_COLOR)
        bullet1_exp_2 = Text("2", font_size=18, color=PRIMARY_TEXT_COLOR).next_to(bullet1_text_part1[-1], UP * 0.5 + RIGHT * 0.05, buff=0.05)
        bullet1_text_part2 = Text(" + bx + c = 0", font_size=35, color=PRIMARY_TEXT_COLOR).next_to(bullet1_exp_2, RIGHT, buff=0.05).shift(DOWN*0.05)
        bullet1 = VGroup(bullet1_text_part1, bullet1_exp_2, bullet1_text_part2).arrange(RIGHT, buff=0.05).to_edge(LEFT, buff=1.5).shift(UP*0.5)
        
        bullet2 = Text("2. Isolate x-terms (divide by 'a', move 'c')", font_size=35, color=PRIMARY_TEXT_COLOR).next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet3 = Text("3. Complete the square", font_size=35, color=PRIMARY_TEXT_COLOR).next_to(bullet2, DOWN, buff=0.5).align_to(bullet2, LEFT)
        bullet4 = Text("4. Simplify the right side", font_size=35, color=PRIMARY_TEXT_COLOR).next_to(bullet3, DOWN, buff=0.5).align_to(bullet3, LEFT)
        bullet5 = Text("5. Take square root, isolate 'x'", font_size=35, color=PRIMARY_TEXT_COLOR).next_to(bullet4, DOWN, buff=0.5).align_to(bullet4, LEFT)
        
        recap_list = VGroup(bullet1, bullet2, bullet3, bullet4, bullet5)

        self.play(FadeIn(recap_title))
        self.play(LaggedStart(*[Write(bullet) for bullet in recap_list], lag_ratio=0.5))
        self.wait(2)

        final_formula_mobj_recap = final_formula_mobj.copy().scale(0.8).move_to(ORIGIN).shift(DOWN*2.5) # Re-add formula for recap
        
        self.play(Write(final_formula_mobj_recap))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_list, final_formula_mobj_recap))
        self.wait(1)