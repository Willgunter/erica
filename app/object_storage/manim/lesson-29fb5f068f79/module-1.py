from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_C = '#5299D3'  # A brighter blue
        GOLD_C = '#E3C16F'  # A brighter gold
        ACCENT_C = '#9BD3D3' # A lighter accent color

        # --- Helper for creating Text-based math expressions ---
        # expression_parts is a list of tuples: (string, scale_factor, position_relative_to_prev, buffer_to_prev)
        # Example: [("a", 1, None, None), ("x", 1, RIGHT, 0.05), ("2", 0.7, UP+RIGHT, 0.05)] for ax^2
        def create_math_text(expression_parts, color=WHITE):
            mobs = VGroup()
            for i, part in enumerate(expression_parts):
                text_str, scale_factor, position_dir, buff_val = part
                
                new_text = Text(text_str, color=color).scale(scale_factor)
                
                if mobs.is_empty():
                    mobs.add(new_text)
                else:
                    buff = buff_val if buff_val is not None else MED_SMALL_BUFF
                    if position_dir is not None:
                        new_text.next_to(mobs[-1], position_dir, buff=buff)
                    else:
                        new_text.next_to(mobs[-1], RIGHT, buff=buff)
                    mobs.add(new_text)
            return mobs

        # --- BEAT 1: Visual Hook - Parabola and Roots ---
        title = Text("Quadratic Formula", color=GOLD_C).scale(1.2).to_edge(UP)
        subtitle = Text("Form and Derivation", color=ACCENT_C).scale(0.8).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": ACCENT_C, "font_size": 24},
            x_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
            y_axis_config={"numbers_to_include": [-4, -2, 2, 4]}
        ).add_coordinates().to_edge(DOWN)

        parabola_func = lambda x: 0.5 * x**2 - 2
        parabola = axes.get_graph(parabola_func, color=BLUE_C, x_range=[-3.5, 3.5])

        root1 = Dot(axes.c2p(-2, 0), color=GOLD_C, radius=0.1)
        root2 = Dot(axes.c2p(2, 0), color=GOLD_C, radius=0.1)
        
        root_label1 = Text("x = -2", color=GOLD_C).scale(0.6).next_to(root1, DOWN+LEFT, buff=0.1)
        root_label2 = Text("x = 2", color=GOLD_C).scale(0.6).next_to(root2, DOWN+RIGHT, buff=0.1)

        question = Text("Where is y = 0?", color=WHITE).scale(0.7).next_to(axes, UP, buff=0.5)

        self.play(
            FadeIn(axes),
            Create(parabola),
            run_time=2
        )
        self.play(Write(question))
        self.play(
            GrowFromCenter(root1),
            GrowFromCenter(root2),
            FadeIn(root_label1),
            FadeIn(root_label2),
            run_time=1.5
        )
        self.wait(1.5)

        # --- BEAT 2: Standard Form of Quadratic Equation ---
        self.play(
            FadeOut(parabola, root1, root2, root_label1, root_label2, question),
            axes.animate.scale(0.7).to_corner(UL)
        )
        
        # ax^2 + bx + c = 0
        a_sq = create_math_text([("a", 1, None, None), ("x", 1, RIGHT, 0.05), ("2", 0.7, UP+RIGHT, 0.05)], color=BLUE_C)
        plus_b_x = create_math_text([("+", 1, None, None), ("b", 1, RIGHT, None), ("x", 1, RIGHT, 0.05)], color=BLUE_C)
        plus_c = create_math_text([("+", 1, None, None), ("c", 1, RIGHT, None)], color=BLUE_C)
        equals_0 = create_math_text([("=", 1, None, None), ("0", 1, RIGHT, None)], color=BLUE_C)

        equation_parts = VGroup(a_sq, plus_b_x, plus_c, equals_0).arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        
        standard_form_text = Text("Standard Form:", color=GOLD_C).scale(0.7).next_to(equation_parts, UP, buff=0.5)

        self.play(Write(standard_form_text))
        self.play(
            LaggedStart(*[FadeIn(part) for part in equation_parts], lag_ratio=0.5),
            run_time=2
        )
        self.wait(1)

        # Highlight a, b, c
        a_brace = Brace(a_sq[0], DOWN, color=GOLD_C)
        b_brace = Brace(plus_b_x[1], DOWN, color=GOLD_C)
        c_brace = Brace(plus_c[1], DOWN, color=GOLD_C)
        
        a_label = Text("Coefficient", color=GOLD_C).scale(0.5).next_to(a_brace, DOWN)
        b_label = Text("Coefficient", color=GOLD_C).scale(0.5).next_to(b_brace, DOWN)
        c_label = Text("Constant", color=GOLD_C).scale(0.5).next_to(c_brace, DOWN)

        self.play(GrowFromCenter(a_brace), FadeIn(a_label))
        self.wait(0.5)
        self.play(
            ReplacementTransform(a_brace, b_brace),
            ReplacementTransform(a_label, b_label)
        )
        self.wait(0.5)
        self.play(
            ReplacementTransform(b_brace, c_brace),
            ReplacementTransform(b_label, c_label)
        )
        self.wait(0.5)
        self.play(FadeOut(c_brace, c_label))
        self.wait(0.5)

        # --- BEAT 3: Intuition for Derivation (Completing the Square idea) ---
        derivation_title = Text("How do we find 'x'?", color=GOLD_C).scale(0.9).next_to(standard_form_text, UP, buff=0.8)
        self.play(FadeTransform(standard_form_text, derivation_title))
        self.wait(0.5)
        
        # Start with the equation again, perhaps slightly smaller and centered
        equation_vgroup = VGroup(*equation_parts).move_to(ORIGIN).scale(0.9)
        self.play(
            equation_vgroup.animate.shift(UP * 1.5)
        )
        self.wait(0.5)

        # Step 1: Move c to the other side
        # a x^2 + b x = -c
        eq1_a_sq = a_sq.copy().move_to(equation_vgroup[0].get_center())
        eq1_plus_b_x = plus_b_x.copy().move_to(equation_vgroup[1].get_center())
        eq1_equals = Text("=", color=BLUE_C).scale(0.9).next_to(eq1_plus_b_x, RIGHT, buff=0.4)
        eq1_rhs_c = create_math_text([("-", 1, None, None), ("c", 1, RIGHT, None)], color=BLUE_C).next_to(eq1_equals, RIGHT, buff=0.4)

        eq_line1_new = VGroup(eq1_a_sq, eq1_plus_b_x, eq1_equals, eq1_rhs_c).move_to(equation_vgroup.get_center())

        self.play(
            Transform(equation_vgroup[0], eq1_a_sq),
            Transform(equation_vgroup[1], eq1_plus_b_x),
            ReplacementTransform(equation_vgroup[2], eq1_equals), # Transform +c into =
            ReplacementTransform(equation_vgroup[3], eq1_rhs_c), # Transform =0 into -c
            run_time=1.5
        )
        equation_vgroup = eq_line1_new
        self.wait(0.5)
        
        # Step 2: Divide by a
        divide_a_text = Text("Divide by 'a'", color=GOLD_C).scale(0.6).next_to(equation_vgroup, DOWN, buff=0.7)
        self.play(FadeIn(divide_a_text))
        
        # x^2 + (b/a)x = -c/a
        x_sq_text = create_math_text([("x", 1, None, None), ("2", 0.7, UP+RIGHT, 0.05)], color=BLUE_C)
        
        b_over_a_x_parts = [
            ("(", 1, None, None), ("b", 1, RIGHT, None), ("/", 1, RIGHT, None), ("a", 1, RIGHT, None), (")", 1, RIGHT, None), ("x", 1, RIGHT, 0.05)
        ]
        b_over_a_x = create_math_text(b_over_a_x_parts, color=BLUE_C)
        
        neg_c_over_a_parts = [
            ("-", 1, None, None), ("c", 1, RIGHT, None), ("/", 1, RIGHT, None), ("a", 1, RIGHT, None)
        ]
        neg_c_over_a = create_math_text(neg_c_over_a_parts, color=BLUE_C)

        eq_line2_parts = VGroup(x_sq_text, Text("+", color=BLUE_C).scale(0.9), b_over_a_x, Text("=", color=BLUE_C).scale(0.9), neg_c_over_a)
        eq_line2_parts.arrange(RIGHT, buff=0.3).move_to(equation_vgroup.get_center()).shift(DOWN * 1.5)
        
        self.play(
            FadeOut(equation_vgroup, shift=UP*0.5), # Make previous line fade up and out
            FadeIn(eq_line2_parts, shift=DOWN*0.5),  # New line fades in from below
            FadeOut(divide_a_text),
            run_time=2
        )
        equation_vgroup = eq_line2_parts # Update for next step
        self.wait(1)

        # Step 3: Completing the Square visual intuition
        complete_square_text = Text("Completing the Square", color=GOLD_C).scale(0.6).next_to(equation_vgroup, UP, buff=0.7)
        self.play(FadeIn(complete_square_text))

        # We're aiming for (x + b/2a)^2 = x^2 + (b/a)x + (b/2a)^2
        # So we need to add (b/2a)^2 to both sides.
        
        b_over_2a_sq_parts = [
            ("(", 1, None, None), ("b", 1, RIGHT, None), ("/", 1, RIGHT, None), ("2", 1, RIGHT, None), ("a", 1, RIGHT, None), (")", 1, RIGHT, None), ("2", 0.7, UP+RIGHT, 0.05)
        ]
        b_over_2a_sq_term = create_math_text(b_over_2a_sq_parts, color=ACCENT_C)

        plus_b_over_2a_sq_lhs = VGroup(Text("+", color=ACCENT_C).scale(1), b_over_2a_sq_term.copy()).arrange(RIGHT, buff=0.05)
        plus_b_over_2a_sq_lhs.next_to(equation_vgroup[2], RIGHT, buff=0.2)

        plus_b_over_2a_sq_rhs = VGroup(Text("+", color=ACCENT_C).scale(1), b_over_2a_sq_term.copy()).arrange(RIGHT, buff=0.05)
        plus_b_over_2a_sq_rhs.next_to(equation_vgroup[4], RIGHT, buff=0.2)
        
        # New combined LHS and RHS for the next line
        eq_line3_lhs_content = VGroup(equation_vgroup[0].copy(), equation_vgroup[1].copy(), equation_vgroup[2].copy(), plus_b_over_2a_sq_lhs)
        eq_line3_lhs_content.arrange(RIGHT, buff=0.3)
        
        eq_line3_rhs_content = VGroup(equation_vgroup[4].copy(), plus_b_over_2a_sq_rhs)
        eq_line3_rhs_content.arrange(RIGHT, buff=0.3)
        
        equals_sign_line3 = Text("=", color=BLUE_C).scale(0.9)
        
        # Position the full new line
        temp_group_for_position = VGroup(eq_line3_lhs_content, equals_sign_line3, eq_line3_rhs_content).arrange(RIGHT, buff=0.4).move_to(equation_vgroup.get_center()).shift(DOWN*1.5)

        self.play(
            FadeOut(equation_vgroup), # Clear the old equation line
            FadeIn(eq_line3_lhs_content, shift=DOWN*0.5),
            FadeIn(equals_sign_line3, shift=DOWN*0.5),
            FadeIn(eq_line3_rhs_content, shift=DOWN*0.5),
            FadeOut(complete_square_text),
            run_time=2.5
        )
        self.wait(1)

        # Left side becomes (x + b/2a)^2
        x_plus_b_over_2a_sq_parts = [
            ("(", 1, None, None), ("x", 1, RIGHT, None), ("+", 1, RIGHT, None), ("b", 1, RIGHT, None), ("/", 1, RIGHT, None), ("2", 1, RIGHT, None), ("a", 1, RIGHT, None), (")", 1, RIGHT, None), ("2", 0.7, UP+RIGHT, 0.05)
        ]
        x_plus_b_over_2a_sq = create_math_text(x_plus_b_over_2a_sq_parts, color=BLUE_C)
        
        final_eq_lhs = x_plus_b_over_2a_sq.copy().move_to(eq_line3_lhs_content.get_center())
        final_eq_rhs = eq_line3_rhs_content.copy().move_to(eq_line3_rhs_content.get_center()) # Keep RHS as is for now

        self.play(
            Transform(eq_line3_lhs_content, final_eq_lhs),
            run_time=1.5
        )
        
        # Bring everything to one line for the final formula reveal
        final_eq_equals = Text("=", color=BLUE_C).scale(0.9)
        
        final_eq_line_assembled = VGroup(final_eq_lhs, final_eq_equals, final_eq_rhs).arrange(RIGHT, buff=0.4).center().shift(DOWN*1.5)

        self.play(
            final_eq_lhs.animate.move_to(final_eq_line_assembled[0].get_center()),
            FadeIn(final_eq_equals),
            final_eq_rhs.animate.move_to(final_eq_line_assembled[2].get_center()),
            run_time=1.5
        )
        self.wait(1)
        
        # Fade out everything related to derivation to prepare for the formula
        self.play(
            FadeOut(derivation_title),
            FadeOut(axes),
            FadeOut(final_eq_lhs, final_eq_equals, final_eq_rhs),
            FadeOut(title, subtitle), # Fade out main title to replace with formula
            run_time=1.5
        )
        
        # --- BEAT 4: The Quadratic Formula Revealed ---
        formula_title = Text("The Quadratic Formula", color=GOLD_C).scale(1.2).to_edge(UP)
        
        # x = (-b +- sqrt(b^2 - 4ac)) / 2a
        x_eq = create_math_text([("x", 1, None, None), ("=", 1, RIGHT, None)], color=BLUE_C)
        
        numerator_b = create_math_text([("-", 1, None, None), ("b", 1, RIGHT, None)], color=BLUE_C)
        plus_minus = Text("±", color=ACCENT_C).scale(1)
        
        sqrt_term_b_sq = create_math_text([("b", 1, None, None), ("2", 0.7, UP+RIGHT, 0.05)], color=BLUE_C)
        sqrt_term_minus_4ac = create_math_text([("-", 1, None, None), ("4", 1, RIGHT, None), ("a", 1, RIGHT, 0.05), ("c", 1, RIGHT, 0.05)], color=BLUE_C)
        
        # Group b^2 - 4ac
        discriminant_group = VGroup(sqrt_term_b_sq, sqrt_term_minus_4ac).arrange(RIGHT, buff=0.2)

        # Square root symbol (approximate with line and hat)
        sqrt_line_base = Line(LEFT, RIGHT, color=BLUE_C).scale(1.5)
        sqrt_symbol = VGroup(
            Line(sqrt_line_base.get_left() + LEFT*0.2, sqrt_line_base.get_left() + UP*0.1, color=BLUE_C, stroke_width=2),
            Line(sqrt_line_base.get_left() + UP*0.1, sqrt_line_base.get_left() + UP*0.1 + RIGHT*0.2, color=BLUE_C, stroke_width=2),
            sqrt_line_base
        ).move_to(sqrt_line_base.get_center())
        
        # Combine everything under the square root
        sqrt_expression = VGroup(discriminant_group, sqrt_symbol).move_to(discriminant_group.get_center())

        # Numerator assembled: -b ± sqrt(b^2 - 4ac)
        numerator_group = VGroup(numerator_b, plus_minus, sqrt_expression).arrange(RIGHT, buff=0.3)

        # Denominator: 2a
        denominator_group = create_math_text([("2", 1, None, None), ("a", 1, RIGHT, 0.05)], color=BLUE_C)

        # Fraction line
        fraction_line = Line(LEFT, RIGHT, color=BLUE_C).scale(2.5)
        
        # Position numerator, fraction line, denominator
        fraction_line.move_to(ORIGIN)
        numerator_group.next_to(fraction_line, UP, buff=0.3)
        denominator_group.next_to(fraction_line, DOWN, buff=0.3)

        # Entire formula group
        formula_rhs = VGroup(numerator_group, fraction_line, denominator_group)
        formula_line = VGroup(x_eq, formula_rhs).arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        
        self.play(Write(formula_title))
        self.wait(0.5)
        self.play(
            LaggedStart(
                FadeIn(x_eq),
                FadeIn(numerator_b),
                FadeIn(plus_minus),
                FadeIn(discriminant_group),
                Create(sqrt_symbol),
                Create(fraction_line),
                FadeIn(denominator_group),
                lag_ratio=0.2
            ),
            run_time=3.5
        )
        self.wait(2)

        # Highlight a, b, c connections
        a_orig_text = Text("a", color=GOLD_C).scale(0.8).next_to(formula_title, DOWN, buff=1.0).shift(LEFT*4)
        b_orig_text = Text("b", color=GOLD_C).scale(0.8).next_to(a_orig_text, RIGHT, buff=1.5)
        c_orig_text = Text("c", color=GOLD_C).scale(0.8).next_to(b_orig_text, RIGHT, buff=1.5)

        self.play(FadeIn(a_orig_text), FadeIn(b_orig_text), FadeIn(c_orig_text))
        
        # Arrows from a, b, c labels to their occurrences in the formula
        arrow_a1 = Arrow(a_orig_text.get_bottom(), discriminant_group[1][2].get_top(), color=GOLD_C, buff=0.1, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)
        arrow_a2 = Arrow(a_orig_text.get_bottom(), denominator_group[1].get_top(), color=GOLD_C, buff=0.1, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)

        arrow_b1 = Arrow(b_orig_text.get_bottom(), numerator_b[1].get_top(), color=GOLD_C, buff=0.1, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)
        arrow_b2 = Arrow(b_orig_text.get_bottom(), discriminant_group[0][0].get_top(), color=GOLD_C, buff=0.1, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)
        
        arrow_c1 = Arrow(c_orig_text.get_bottom(), discriminant_group[1][3].get_top(), color=GOLD_C, buff=0.1, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)

        self.play(GrowArrow(arrow_a1), GrowArrow(arrow_a2))
        self.wait(0.5)
        self.play(GrowArrow(arrow_b1), GrowArrow(arrow_b2))
        self.wait(0.5)
        self.play(GrowArrow(arrow_c1))
        self.wait(2)
        
        self.play(
            FadeOut(a_orig_text, b_orig_text, c_orig_text),
            FadeOut(arrow_a1, arrow_a2, arrow_b1, arrow_b2, arrow_c1)
        )

        # --- BEAT 5: Recap Card ---
        self.play(FadeOut(formula_title)) # Keep formula on screen

        recap_card = Rectangle(
            width=8, 
            height=4.5, 
            color=ACCENT_C, 
            fill_opacity=0.1, 
            stroke_width=3
        ).scale(0.9).center()
        
        recap_text = Text("Recall: For ax² + bx + c = 0", color=GOLD_C).scale(0.7).next_to(recap_card.get_top(), DOWN, buff=0.5)
        
        final_formula = formula_line.copy().scale(1.1).move_to(recap_card.get_center())
        
        self.play(
            Create(recap_card),
            FadeIn(recap_text)
        )
        self.play(
            Transform(formula_line, final_formula),
            run_time=1.5
        )
        self.wait(3)
        
        thank_you = Text("Thanks for watching!", color=BLUE_C).scale(0.8).to_edge(DOWN)
        self.play(FadeIn(thank_you))
        self.wait(2)