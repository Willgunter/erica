from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # 1. Configuration
        self.camera.background_color = BLACK

        # Helper functions for creating custom text expressions without Tex or MathTex
        # =================================================================================
        def create_text_power(base_str, power_str, base_scale=0.9, power_scale=0.6, color=WHITE):
            base_mobj = Text(base_str, color=color).scale(base_scale)
            power_mobj = Text(power_str, color=color).scale(power_scale)
            power_mobj.next_to(base_mobj, UP + RIGHT * 0.5, buff=0.05)
            return VGroup(base_mobj, power_mobj)

        def create_text_fraction(numerator_mobj, denominator_mobj, color=WHITE):
            line = Line(LEFT, RIGHT, color=color, stroke_width=2)
            
            # Temporarily arrange to find center for the line and width
            temp_group_for_sizing = VGroup(numerator_mobj.copy(), denominator_mobj.copy()).arrange(DOWN, buff=0.2)
            line.set_width(max(numerator_mobj.get_width(), denominator_mobj.get_width()) * 1.1)
            line.move_to(temp_group_for_sizing.get_center())
            
            # Position actual mobjects relative to the centered line
            numerator_mobj.next_to(line, UP, buff=0.1)
            denominator_mobj.next_to(line, DOWN, buff=0.1)
            
            return VGroup(numerator_mobj, line, denominator_mobj)

        def create_text_sqrt(content_mobject, color=WHITE):
            # A simplified radical symbol: a vertical line, a diagonal, and a horizontal bar.
            v_line = Line(ORIGIN, UP * 0.3, color=color, stroke_width=2)
            diag_line = Line(ORIGIN, RIGHT * 0.2 + DOWN * 0.2, color=color, stroke_width=2).next_to(v_line, RIGHT, buff=0)
            radical_base = VGroup(v_line, diag_line)
            
            # Horizontal bar over content
            horizontal_bar = Line(LEFT, RIGHT, color=color, stroke_width=2)
            horizontal_bar.set_width(content_mobject.get_width() * 1.1)
            horizontal_bar.next_to(content_mobject, UP, buff=0.1)

            # Position the radical base
            # Calculate height for radical base from content bottom to horizontal bar top
            radical_height_ref = horizontal_bar.get_top()[1] - content_mobject.get_bottom()[1]
            radical_base.scale_to_fit_height(radical_height_ref * 0.7) # Adjust to fit visually
            radical_base.next_to(horizontal_bar.get_left(), LEFT, buff=0.05).align_to(content_mobject, DOWN)
            
            return VGroup(radical_base, horizontal_bar, content_mobject)
        # =================================================================================

        # --- Beat 1: Visual Hook & Standard Form ---
        
        # Visual Hook: A simple parabola and its roots
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3, 5, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": BLUE_B},
            tips=False
        ).to_edge(LEFT, buff=1.5)
        
        parabola = axes.plot(lambda x: 0.8 * x**2 - 2, color=GOLD_C) # Example parabola: 0.8x^2 - 2 = 0
        x_intercept_left = Dot(axes.c2p(-1.581, 0), color=RED_C) # Roots are approx. +/- 1.581
        x_intercept_right = Dot(axes.c2p(1.581, 0), color=RED_C)
        
        intro_title = Text("Deriving the Quadratic Formula", color=WHITE).scale(0.8).to_edge(UP, buff=0.5)
        
        self.play(Write(intro_title), run_time=1.5)
        self.wait(0.5)
        self.play(
            LaggedStart(
                FadeIn(axes),
                Create(parabola),
                GrowFromCenter(x_intercept_left),
                GrowFromCenter(x_intercept_right),
                lag_ratio=0.3,
                run_time=2.5
            )
        )
        self.wait(1.5)

        # Fade out parabola and roots, move axes to the background
        self.play(
            FadeOut(parabola, x_intercept_left, x_intercept_right),
            axes.animate.set_opacity(0.3).scale(0.6).to_corner(UL),
            run_time=1.5
        )

        # Introduce the standard form (no Tex - manual Text objects)
        a_m = Text("a", color=BLUE_B).scale(0.9)
        x_sq_m = create_text_power("x", "2", base_scale=0.9, power_scale=0.6)
        plus1_m = Text(" + ", color=WHITE).scale(0.9)
        b_m = Text("b", color=BLUE_B).scale(0.9)
        x_m = Text("x", color=WHITE).scale(0.9)
        plus2_m = Text(" + ", color=WHITE).scale(0.9)
        c_m = Text("c", color=BLUE_B).scale(0.9)
        equals0_m = Text(" = 0", color=WHITE).scale(0.9)

        standard_form_mobjects = [a_m, x_sq_m, plus1_m, b_m, x_m, plus2_m, c_m, equals0_m]
        
        standard_form = VGroup()
        for i, mobj in enumerate(standard_form_mobjects):
            if i == 0:
                standard_form.add(mobj)
            else:
                standard_form.add(mobj.next_to(standard_form[-1], RIGHT, buff=0.05))
        
        standard_form.move_to(ORIGIN)
        
        self.play(
            Write(standard_form),
            run_time=2
        )
        self.wait(1)

        # --- Beat 2: Isolate x terms & Divide by 'a' ---
        step1_title = Text("1. Isolate x terms & Divide by 'a'", color=WHITE).scale(0.6).to_edge(UP).shift(DOWN * 0.5)
        self.play(FadeTransform(intro_title, step1_title), run_time=1)
        self.wait(0.5)

        # ax^2 + bx = -c
        c_moved_out = c_m.copy().set_color(RED_C)
        minus_c_new = Text("-c", color=RED_C).scale(0.9)
        equals_new_sign = Text(" = ", color=WHITE).scale(0.9)

        # Reconstruct equation for `ax^2 + bx = -c`
        eq_line1_mobjects = [a_m.copy(), x_sq_m.copy(), plus1_m.copy(), b_m.copy(), x_m.copy(), equals_new_sign]
        eq_line1 = VGroup()
        for i, mobj in enumerate(eq_line1_mobjects):
            if i == 0:
                eq_line1.add(mobj)
            else:
                eq_line1.add(mobj.next_to(eq_line1[-1], RIGHT, buff=0.05))
        
        minus_c_new.next_to(eq_line1[-1], RIGHT, buff=0.05).align_to(eq_line1, DOWN) # Align with baseline of x
        eq_line1.add(minus_c_new)
        eq_line1.move_to(standard_form.get_center())

        self.play(
            ReplacementTransform(standard_form, eq_line1),
            run_time=1.5
        )
        current_eq = eq_line1
        self.wait(1)

        # Divide by 'a' instruction
        divide_a_label = Text("Divide by 'a'", color=BLUE_B).scale(0.5).next_to(current_eq, DOWN, buff=0.5)
        self.play(FadeIn(divide_a_label), run_time=0.8)

        # Reconstruct x^2 + (b/a)x = -c/a
        x_sq_next = create_text_power("x", "2", base_scale=0.9, power_scale=0.6)
        plus_next = Text(" + ", color=WHITE).scale(0.9)
        b_num_next = Text("b", color=WHITE).scale(0.7)
        a_den_next = Text("a", color=WHITE).scale(0.7)
        b_over_a_frac = create_text_fraction(b_num_next, a_den_next)
        x_next = Text("x", color=WHITE).scale(0.9)
        equals_next = Text(" = ", color=WHITE).scale(0.9)
        minus_c_num_next = Text("-c", color=WHITE).scale(0.7)
        a_den_c_next = Text("a", color=WHITE).scale(0.7)
        minus_c_over_a_frac = create_text_fraction(minus_c_num_next, a_den_c_next)
        
        eq_line2_mobjects = [x_sq_next, plus_next, b_over_a_frac, x_next, equals_next, minus_c_over_a_frac]
        
        eq_line2 = VGroup()
        for i, mobj in enumerate(eq_line2_mobjects):
            if i == 0:
                eq_line2.add(mobj)
            else:
                # Special alignment for fractions and x's next to fractions
                if mobj in [b_over_a_frac, minus_c_over_a_frac, x_next]:
                    eq_line2.add(mobj.next_to(eq_line2[-1], RIGHT, buff=0.05).align_to(x_sq_next, DOWN))
                else:
                    eq_line2.add(mobj.next_to(eq_line2[-1], RIGHT, buff=0.05))
        
        eq_line2.move_to(ORIGIN).shift(DOWN * 1.5)

        self.play(
            FadeOut(divide_a_label),
            ReplacementTransform(current_eq, eq_line2),
            run_time=2
        )
        current_eq = eq_line2
        self.wait(1)

        # --- Beat 3: Completing the Square - Visual & Algebraic ---
        step2_title = Text("2. Complete the Square", color=WHITE).scale(0.6).to_edge(UP).shift(DOWN * 0.5)
        self.play(FadeTransform(step1_title, step2_title), run_time=1)
        self.wait(0.5)

        # Visual Part - move current_eq temporarily
        self.play(current_eq.animate.to_edge(DOWN, buff=0.5).scale(0.8), run_time=1)

        # Start square (x^2)
        square_x = Square(side_length=1.5, color=GOLD_C, fill_opacity=0.3).shift(LEFT * 2 + UP * 1.5)
        x_label_left = Text("x", color=WHITE).scale(0.6).next_to(square_x.get_corner(DL), LEFT, buff=0.1)
        x_label_bottom = Text("x", color=WHITE).scale(0.6).next_to(square_x.get_corner(DL), DOWN, buff=0.1)
        
        self.play(FadeIn(VGroup(square_x, x_label_left, x_label_bottom)), run_time=1)
        self.wait(0.5)

        # Add rectangles for (b/a)x split into (b/2a)x
        rect_fraction_len = 0.5 # Arbitrary visual proportion for b/2a
        rect_1 = Rectangle(width=rect_fraction_len, height=square_x.get_height(), color=BLUE_B, fill_opacity=0.3)
        rect_2 = Rectangle(width=square_x.get_width(), height=rect_fraction_len, color=BLUE_B, fill_opacity=0.3)
        
        rect_1.next_to(square_x, RIGHT, buff=0)
        rect_2.next_to(square_x, DOWN, buff=0)

        self.play(Create(rect_1), Create(rect_2), run_time=1)
        self.wait(0.5)

        # Label the new sides (b/2a)
        b_over_2a_vis_label = Text("(b/2a)", color=WHITE).scale(0.4)
        b_over_2a_vis_label_x = b_over_2a_vis_label.copy().next_to(rect_1, RIGHT, buff=0.1)
        b_over_2a_vis_label_y = b_over_2a_vis_label.copy().next_to(rect_2, DOWN, buff=0.1)
        self.play(FadeIn(b_over_2a_vis_label_x, b_over_2a_vis_label_y), run_time=0.8)

        # The missing piece: (b/2a)^2
        missing_square = Square(side_length=rect_fraction_len, color=GOLD_C, fill_opacity=0.7)
        missing_square.next_to(rect_1, DOWN, buff=0).align_to(rect_2, RIGHT)
        
        self.play(
            GrowFromCenter(missing_square),
            run_time=1
        )
        self.wait(1)
        
        # Fade out visual, bring equation back
        self.play(
            FadeOut(square_x, x_label_left, x_label_bottom, rect_1, rect_2, 
                    b_over_2a_vis_label_x, b_over_2a_vis_label_y, missing_square),
            current_eq.animate.move_to(ORIGIN).scale(1/0.8), # Restore original scale and position
            run_time=1.5
        )

        # Algebraic part: Add (b/2a)^2 to both sides
        b_num_p = Text("b", color=WHITE).scale(0.7)
        two_a_den_p = VGroup(Text("2", color=WHITE).scale(0.7), Text("a", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        b_over_2a_base = create_text_fraction(b_num_p, two_a_den_p)
        b_over_2a_sq = create_text_power(b_over_2a_base.copy(), Text("2", color=WHITE).scale(0.4))
        
        plus_term_l = Text(" + ", color=WHITE).scale(0.9)
        plus_term_r = Text(" + ", color=WHITE).scale(0.9)

        # Reconstruct equation: x^2 + (b/a)x + (b/2a)^2 = -c/a + (b/2a)^2
        # Elements from current_eq: [x_sq_next, plus_next, b_over_a_frac, x_next, equals_next, minus_c_over_a_frac]
        eq_line3_mobjects = [
            current_eq[0].copy(), current_eq[1].copy(), current_eq[2].copy(), current_eq[3].copy(), 
            plus_term_l, b_over_2a_sq.copy(),
            current_eq[4].copy(), current_eq[5].copy(), 
            plus_term_r, b_over_2a_sq.copy()
        ]
        
        eq_line3 = VGroup()
        for i, mobj in enumerate(eq_line3_mobjects):
            if i == 0:
                eq_line3.add(mobj)
            else:
                if mobj == b_over_2a_sq: # For the (b/2a)^2 terms
                    eq_line3.add(mobj.next_to(eq_line3[-1], RIGHT, buff=0.05).align_to(eq_line3[0], DOWN))
                elif mobj == eq_line3_mobjects[6]: # equals sign
                    eq_line3.add(mobj.next_to(eq_line3[-1], RIGHT, buff=0.1))
                elif mobj == eq_line3_mobjects[7]: # -c/a
                    eq_line3.add(mobj.next_to(eq_line3[-1], RIGHT, buff=0.05).align_to(eq_line3[0], DOWN))
                else:
                    eq_line3.add(mobj.next_to(eq_line3[-1], RIGHT, buff=0.05))
        
        eq_line3.move_to(ORIGIN)

        self.play(
            ReplacementTransform(current_eq, eq_line3),
            run_time=2
        )
        current_eq = eq_line3
        self.wait(1)

        # Factor the left side: (x + b/2a)^2
        open_paren = Text("(", color=WHITE).scale(0.9)
        x_term_factored = Text("x", color=WHITE).scale(0.9)
        plus_term_factored = Text(" + ", color=WHITE).scale(0.9)
        b_num_factored = Text("b", color=WHITE).scale(0.7)
        two_a_den_factored = VGroup(Text("2", color=WHITE).scale(0.7), Text("a", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        b_over_2a_factored = create_text_fraction(b_num_factored, two_a_den_factored)
        close_paren = Text(")", color=WHITE).scale(0.9)
        power_2_factored = Text("2", color=WHITE).scale(0.6)
        
        factored_left = VGroup(open_paren, x_term_factored, plus_term_factored, b_over_2a_factored, close_paren, power_2_factored)
        factored_left[1].next_to(factored_left[0], RIGHT, buff=0.05)
        factored_left[2].next_to(factored_left[1], RIGHT, buff=0.05)
        factored_left[3].next_to(factored_left[2], RIGHT, buff=0.05).align_to(factored_left[1], DOWN)
        factored_left[4].next_to(factored_left[3], RIGHT, buff=0.05)
        factored_left[5].next_to(factored_left[4], UP + RIGHT * 0.5, buff=0.05) # Manual power positioning
        
        # Combine right side: -c/a + b^2/4a^2  -> (b^2 - 4ac) / 4a^2
        # Numerator: b^2 - 4ac
        b_sq_num_comb = create_text_power("b", "2", base_scale=0.7, power_scale=0.5)
        minus_comb = Text(" - ", color=WHITE).scale(0.7)
        four_a_c_comb = VGroup(Text("4", color=WHITE).scale(0.7), Text("a", color=WHITE).scale(0.7), Text("c", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        right_num_mobj = VGroup(b_sq_num_comb, minus_comb, four_a_c_comb)
        right_num_mobj[1].next_to(right_num_mobj[0], RIGHT, buff=0.05)
        right_num_mobj[2].next_to(right_num_mobj[1], RIGHT, buff=0.05)

        # Denominator: 4a^2
        four_a_sq_den_comb = VGroup(Text("4", color=WHITE).scale(0.7), create_text_power("a", "2", base_scale=0.7, power_scale=0.5)).arrange(RIGHT, buff=0.05)
        
        right_side_combined_frac = create_text_fraction(right_num_mobj, four_a_sq_den_comb)

        equals_middle_final = Text(" = ", color=WHITE).scale(0.9)
        
        eq_line4 = VGroup(factored_left, equals_middle_final, right_side_combined_frac)
        eq_line4[1].next_to(eq_line4[0], RIGHT, buff=0.1)
        eq_line4[2].next_to(eq_line4[1], RIGHT, buff=0.05).align_to(eq_line4[0][1], DOWN) # Align with the 'x'
        eq_line4.move_to(ORIGIN)

        self.play(
            ReplacementTransform(current_eq, eq_line4),
            run_time=2
        )
        current_eq = eq_line4
        self.wait(1)

        # --- Beat 4: Solving for x ---
        step3_title = Text("3. Solve for x", color=WHITE).scale(0.6).to_edge(UP).shift(DOWN * 0.5)
        self.play(FadeTransform(step2_title, step3_title), run_time=1)
        self.wait(0.5)

        # Take square root of both sides
        plus_minus_sign = Text("±", color=GOLD_C).scale(0.9)
        
        # Content under the square root: b^2 - 4ac
        sqrt_content_b2_4ac = VGroup(create_text_power("b", "2", base_scale=0.7, power_scale=0.5), 
                                      Text(" - ", color=WHITE).scale(0.7), 
                                      Text("4", color=WHITE).scale(0.7), 
                                      Text("a", color=WHITE).scale(0.7), 
                                      Text("c", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        sqrt_term = create_text_sqrt(sqrt_content_b2_4ac)

        # Denominator: 2a (sqrt(4a^2) = 2a)
        two_a_denom_sqrt = VGroup(Text("2", color=WHITE).scale(0.7), Text("a", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        
        # The entire right side (±sqrt(...) / 2a)
        right_side_sqrt_frac = create_text_fraction(sqrt_term, two_a_denom_sqrt)

        # The left side (x + b/2a)
        open_paren_temp = Text("(", color=WHITE).scale(0.9)
        x_temp = Text("x", color=WHITE).scale(0.9)
        plus_temp = Text(" + ", color=WHITE).scale(0.9)
        b_num_temp = Text("b", color=WHITE).scale(0.7)
        two_a_den_temp = VGroup(Text("2", color=WHITE).scale(0.7), Text("a", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        b_over_2a_temp = create_text_fraction(b_num_temp, two_a_den_temp)
        close_paren_temp = Text(")", color=WHITE).scale(0.9)
        
        left_side_temp = VGroup(open_paren_temp, x_temp, plus_temp, b_over_2a_temp, close_paren_temp)
        left_side_temp[1].next_to(left_side_temp[0], RIGHT, buff=0.05)
        left_side_temp[2].next_to(left_side_temp[1], RIGHT, buff=0.05)
        left_side_temp[3].next_to(left_side_temp[2], RIGHT, buff=0.05).align_to(left_side_temp[1], DOWN)
        left_side_temp[4].next_to(left_side_temp[3], RIGHT, buff=0.05)
        
        equals_sign_mid_temp = Text(" = ", color=WHITE).scale(0.9)
        
        # Add the plus/minus sign explicitly to the right fraction
        right_side_with_pm = VGroup(plus_minus_sign, right_side_sqrt_frac)
        right_side_with_pm[0].next_to(right_side_with_pm[1], LEFT, buff=0.1) # Position PM to the left of the fraction
        
        eq_line5 = VGroup(left_side_temp, equals_sign_mid_temp, right_side_with_pm)
        eq_line5[1].next_to(eq_line5[0], RIGHT, buff=0.1)
        eq_line5[2].next_to(eq_line5[1], RIGHT, buff=0.05).align_to(eq_line5[0][1], DOWN) # Align with 'x'
        eq_line5.move_to(ORIGIN)

        self.play(
            ReplacementTransform(current_eq, eq_line5),
            run_time=2
        )
        current_eq = eq_line5
        self.wait(1)

        # Isolate x: x = -b/2a ± sqrt(...) / 2a
        x_isolate = Text("x", color=GOLD_C).scale(0.9)
        equals_isolate = Text(" = ", color=WHITE).scale(0.9)
        
        # New first fraction: -b/2a
        minus_b_num_isolate = Text("-b", color=BLUE_B).scale(0.7)
        two_a_den_isolate = VGroup(Text("2", color=WHITE).scale(0.7), Text("a", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        minus_b_over_2a_frac = create_text_fraction(minus_b_num_isolate, two_a_den_isolate)
        
        # The right side (±sqrt(...) / 2a) is already grouped from previous step: right_side_with_pm
        
        eq_line6_mobjects = [x_isolate, equals_isolate, minus_b_over_2a_frac, right_side_with_pm]

        eq_line6 = VGroup()
        for i, mobj in enumerate(eq_line6_mobjects):
            if i == 0:
                eq_line6.add(mobj)
            else:
                if mobj == right_side_with_pm: # This needs careful positioning after -b/2a
                    eq_line6.add(mobj.next_to(minus_b_over_2a_frac, RIGHT, buff=0.1).align_to(x_isolate, DOWN))
                else:
                    eq_line6.add(mobj.next_to(eq_line6[-1], RIGHT, buff=0.05))

        eq_line6.move_to(ORIGIN)

        self.play(
            ReplacementTransform(current_eq, eq_line6),
            run_time=2
        )
        current_eq = eq_line6
        self.wait(1)

        # Combine into single fraction: x = (-b ±√(b^2 - 4ac)) / 2a
        x_final = Text("x", color=GOLD_C).scale(0.9)
        equals_final = Text(" = ", color=WHITE).scale(0.9)

        # Final Numerator: (-b ±√(b^2 - 4ac))
        num_final_minus_b = Text("-b", color=BLUE_B).scale(0.7)
        num_final_plus_minus = Text("±", color=GOLD_C).scale(0.7)
        num_final_sqrt_content = VGroup(create_text_power("b", "2", base_scale=0.7, power_scale=0.5), 
                                      Text(" - ", color=WHITE).scale(0.7), 
                                      Text("4", color=WHITE).scale(0.7), 
                                      Text("a", color=WHITE).scale(0.7), 
                                      Text("c", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)
        num_final_sqrt = create_text_sqrt(num_final_sqrt_content)
        
        final_numerator_mobj = VGroup(num_final_minus_b, num_final_plus_minus, num_final_sqrt)
        final_numerator_mobj[1].next_to(final_numerator_mobj[0], RIGHT, buff=0.05)
        final_numerator_mobj[2].next_to(final_numerator_mobj[1], RIGHT, buff=0.05).align_to(final_numerator_mobj[0], DOWN) # Align sqrt base with -b
        
        # Final Denominator: 2a
        final_denom_mobj = VGroup(Text("2", color=WHITE).scale(0.7), Text("a", color=WHITE).scale(0.7)).arrange(RIGHT, buff=0.05)

        final_quadratic_formula_frac = create_text_fraction(final_numerator_mobj, final_denom_mobj)

        final_quadratic_formula = VGroup(x_final, equals_final, final_quadratic_formula_frac)
        final_quadratic_formula[1].next_to(final_quadratic_formula[0], RIGHT, buff=0.1)
        final_quadratic_formula[2].next_to(final_quadratic_formula[1], RIGHT, buff=0.05).align_to(final_quadratic_formula[0], DOWN)
        final_quadratic_formula.move_to(ORIGIN)

        self.play(
            ReplacementTransform(current_eq, final_quadratic_formula),
            run_time=2.5
        )
        self.wait(2)

        # --- Beat 5: Recap Card ---
        recap_title = Text("Quadratic Formula Recap:", color=GOLD_C).scale(0.7).to_edge(UP, buff=1)
        
        # Transform the final formula to the recap position and scale
        self.play(
            FadeTransform(step3_title, recap_title),
            final_quadratic_formula.animate.next_to(recap_title, DOWN, buff=0.5).scale(1.2).set_color(GOLD_C),
            run_time=1.5
        )
        self.wait(3)
        self.play(FadeOut(recap_title, final_quadratic_formula), run_time=1)