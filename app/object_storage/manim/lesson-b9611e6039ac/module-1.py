from manim import *

class QuadraticEquationsDerivation(Scene):
    def construct(self):
        # Configuration
        self.camera.background_color = BLACK

        # Define custom colors (3Blue1Brown inspired)
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E
        LIGHT_BLUE = BLUE_A
        LIGHT_GOLD = GOLD_A
        WHITE_TEXT = WHITE

        # Helper to create exponents
        def create_exponent(base_mobj, exp_str="2", color=WHITE_TEXT, scale=0.6):
            exp_mobj = Text(exp_str, color=color).scale(scale)
            exp_mobj.next_to(base_mobj, UP + RIGHT, buff=0.05).align_to(base_mobj, UP)
            return exp_mobj

        # Helper to create fraction terms like b/2 or b/(2a)
        def create_fraction(numerator_mobj, denominator_mobj, color=WHITE_TEXT, line_width_factor=1.1):
            frac_line = Line(LEFT, RIGHT, color=color).set_width(max(numerator_mobj.width, denominator_mobj.width) * line_width_factor)
            frac_line.move_to(ORIGIN) # Position temporarily
            
            numerator_mobj.next_to(frac_line, UP, buff=0.1)
            denominator_mobj.next_to(frac_line, DOWN, buff=0.1)
            
            return VGroup(numerator_mobj, frac_line, denominator_mobj)
        
        # Helper to create square root terms
        def create_sqrt_term(content_mobj, color=WHITE_TEXT, scale=1):
            sqrt_symbol = Text("√", color=color).scale(scale)
            # Create an overline
            overhead_line = Line(content_mobj.get_left(), content_mobj.get_right(), color=color)
            overhead_line.next_to(content_mobj, UP, buff=0.1)
            
            # Position the square root symbol
            sqrt_symbol.next_to(overhead_line.get_left(), LEFT, buff=0.1).shift(UP * 0.05 * scale) # Adjust y slightly
            
            return VGroup(sqrt_symbol, content_mobj, overhead_line)

        # --- Beat 1: The Parabola & The Problem ---
        title = Text("Quadratic Equations", color=WHITE_TEXT).scale(1.2).to_edge(UP)
        subtitle = Text("Finding the Formula", color=LIGHT_BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)

        self.play(FadeOut(subtitle))

        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 8, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-3, -1, 1, 3]},
            y_axis_config={"numbers_to_include": [0, 2, 4, 6]},
            tips=False
        ).shift(DOWN * 0.5)

        labels = axes.get_axis_labels(
            x_label=Text("x", color=LIGHT_BLUE),
            y_label=Text("y", color=LIGHT_BLUE)
        )

        self.play(Create(axes), Create(labels), run_time=1.5)

        # Parabola y = x^2 (initial visual hook)
        parabola_initial = axes.get_graph(lambda x: x**2, color=LIGHT_BLUE)
        self.play(Create(parabola_initial))
        self.wait(0.5)

        problem_text = Text("Where does y = 0?", color=WHITE_TEXT).to_edge(UP).shift(LEFT*2)
        self.play(FadeTransform(title, problem_text))
        self.wait(0.5)

        # General quadratic equation (ax^2 + bx + c = 0)
        text_a = Text("a", color=LIGHT_GOLD)
        text_x_base = Text("x", color=LIGHT_BLUE)
        text_x_exp = create_exponent(text_x_base)
        term_ax2 = VGroup(text_a, text_x_base, text_x_exp).arrange(RIGHT, buff=0.05).move_to(ORIGIN)
        text_plus1 = Text("+", color=WHITE_TEXT)
        text_b = Text("b", color=LIGHT_GOLD)
        text_x = Text("x", color=LIGHT_BLUE)
        term_bx = VGroup(text_plus1, text_b, text_x).arrange(RIGHT, buff=0.05).move_to(ORIGIN)
        text_plus2 = Text("+", color=WHITE_TEXT)
        text_c = Text("c", color=LIGHT_GOLD)
        term_c = VGroup(text_plus2, text_c).arrange(RIGHT, buff=0.05).move_to(ORIGIN)
        text_equals = Text("=", color=WHITE_TEXT)
        text_zero = Text("0", color=WHITE_TEXT)
        term_eq_zero = VGroup(text_equals, text_zero).arrange(RIGHT, buff=0.05).move_to(ORIGIN)

        quadratic_equation_vgroup = VGroup(term_ax2, term_bx, term_c, term_eq_zero).arrange(RIGHT, buff=0.2).next_to(axes, UP, buff=1)

        self.play(Write(quadratic_equation_vgroup))
        self.wait(0.5)

        # Animate a general parabola with roots
        parabola_general = axes.get_graph(lambda x: 0.5 * x**2 - x - 2, color=LIGHT_GOLD) # a=0.5, b=-1, c=-2 -> roots at -2, 4
        self.play(Transform(parabola_initial, parabola_general))

        # Highlight roots
        root1_dot = Dot(axes.c2p(-2, 0), color=GOLD_ACCENT)
        root2_dot = Dot(axes.c2p(4, 0), color=GOLD_ACCENT)
        root_label1 = Text("x₁", color=GOLD_ACCENT).next_to(root1_dot, DOWN, buff=0.2)
        root_label2 = Text("x₂", color=GOLD_ACCENT).next_to(root2_dot, DOWN, buff=0.2)

        self.play(
            Create(root1_dot), Write(root_label1),
            Create(root2_dot), Write(root_label2)
        )
        self.wait(1)

        self.play(
            FadeOut(root1_dot, root2_dot, root_label1, root_label2),
            FadeOut(parabola_initial, axes, labels, problem_text),
            quadratic_equation_vgroup.animate.to_edge(UP).scale(0.8)
        )
        self.wait(0.5)

        # --- Beat 2: Completing the Square - Visual Intuition (assuming a=1 for simplicity) ---
        simplify_a = Text("Let's simplify by assuming a=1", color=WHITE_TEXT).scale(0.7).next_to(quadratic_equation_vgroup, DOWN, buff=0.5)
        self.play(FadeIn(simplify_a))
        self.wait(1)

        # Simplified equation x^2 + bx + c = 0
        eq_x2_simp = VGroup(Text("x", color=LIGHT_BLUE), create_exponent(Text("x", color=LIGHT_BLUE), color=LIGHT_BLUE))
        eq_bx_simp = VGroup(Text("+", color=WHITE_TEXT), Text("b", color=LIGHT_GOLD), Text("x", color=LIGHT_BLUE))
        eq_c_simp = VGroup(Text("+", color=WHITE_TEXT), Text("c", color=LIGHT_GOLD))
        eq_eq0_simp = VGroup(Text("=", color=WHITE_TEXT), Text("0", color=WHITE_TEXT))
        
        simplified_equation = VGroup(eq_x2_simp, eq_bx_simp, eq_c_simp, eq_eq0_simp).arrange(RIGHT, buff=0.2).move_to(simplify_a.get_center())
        
        self.play(FadeTransform(quadratic_equation_vgroup, simplified_equation), FadeOut(simplify_a))
        self.wait(1)

        # Visualizing x^2 + bx
        self.play(simplified_equation.animate.shift(UP * 2.5))
        
        x_square_side = 2
        x_square = Square(side_length=x_square_side, color=LIGHT_BLUE, fill_opacity=0.3, stroke_width=3)
        x_label_left = Text("x", color=LIGHT_BLUE).next_to(x_square.get_left(), LEFT, buff=0.1)
        x_label_top = Text("x", color=LIGHT_BLUE).next_to(x_square.get_up(), UP, buff=0.1)

        # b * x rectangle
        b_rect_width_val = 1.5 # Arbitrary 'b' width for visualization
        b_rect = Rectangle(width=b_rect_width_val, height=x_square_side, color=LIGHT_GOLD, fill_opacity=0.3, stroke_width=3)
        b_label_top = Text("b", color=LIGHT_GOLD).next_to(b_rect.get_up(), UP, buff=0.1)

        initial_geom = VGroup(x_square, x_label_left, x_label_top, b_rect, b_label_top).arrange(RIGHT, buff=0.2).center().shift(DOWN*0.5)

        self.play(Create(x_square), Write(x_label_left), Write(x_label_top))
        self.wait(0.5)
        self.play(Create(b_rect), Write(b_label_top))
        self.wait(1)

        # Rearrange to form an incomplete square
        self.play(
            x_square.animate.move_to(LEFT * (x_square_side/2 + b_rect_width_val/4) + UP * b_rect_width_val/4), # Adjust position
            x_label_left.animate.next_to(x_square.get_left(), LEFT, buff=0.1),
            x_label_top.animate.next_to(x_square.get_up(), UP, buff=0.1),
            b_rect.animate.set_height(x_square_side).next_to(x_square, RIGHT, buff=0),
            b_label_top.animate.next_to(b_rect.get_up(), UP, buff=0.1),
            run_time=1.5
        )
        self.wait(0.5)

        # Cut 'b' rectangle in half
        half_b_width = b_rect_width_val / 2
        half_b_rect1 = Rectangle(width=half_b_width, height=x_square_side, color=LIGHT_GOLD, fill_opacity=0.3, stroke_width=3)
        half_b_rect2 = Rectangle(width=half_b_width, height=x_square_side, color=LIGHT_GOLD, fill_opacity=0.3, stroke_width=3)
        
        self.play(
            b_rect.animate.become(VGroup(
                half_b_rect1.move_to(b_rect.get_center() + LEFT * half_b_width / 2),
                half_b_rect2.move_to(b_rect.get_center() + RIGHT * half_b_width / 2)
            )),
            FadeOut(b_label_top)
        )
        self.wait(0.5)

        # Move one half to the bottom
        self.play(
            half_b_rect1.animate.next_to(x_square, RIGHT, buff=0),
            half_b_rect2.animate.set_width(x_square_side).set_height(half_b_width).next_to(x_square, DOWN, buff=0), # Rotate by setting width/height
            run_time=1
        )
        self.wait(0.5)

        # Add labels for b/2
        text_b_num = Text("b", color=LIGHT_GOLD)
        text_2_den = Text("2", color=WHITE_TEXT)
        frac_b_over_2_label = create_fraction(text_b_num, text_2_den).scale(0.6)
        
        b_over_2_label_right = frac_b_over_2_label.copy().next_to(half_b_rect1, UP, buff=0.1).align_to(half_b_rect1, UP)
        b_over_2_label_bottom = frac_b_over_2_label.copy().next_to(half_b_rect2, LEFT, buff=0.1).align_to(half_b_rect2, LEFT)
        
        self.play(Write(b_over_2_label_right), Write(b_over_2_label_bottom))
        self.wait(0.5)

        # Show the missing piece to complete the square
        missing_square_side = half_b_width
        missing_square = Square(side_length=missing_square_side, color=BLUE_ACCENT, fill_opacity=0.6, stroke_width=3)
        missing_square.next_to(half_b_rect1, DOWN, buff=0).align_to(half_b_rect2, RIGHT)

        missing_square_label_b_num = Text("b", color=BLUE_ACCENT)
        missing_square_label_2_den = Text("2", color=WHITE_TEXT)
        missing_square_label_frac = create_fraction(missing_square_label_b_num, missing_square_label_2_den, color=BLUE_ACCENT).scale(0.6)
        missing_square_label_exp = create_exponent(VGroup(Text("", color=BLUE_ACCENT), Text("", color=BLUE_ACCENT)), "2", color=BLUE_ACCENT) # dummy base for exponent
        missing_square_label = VGroup(Text("(", color=BLUE_ACCENT), missing_square_label_frac, Text(")", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05).add(missing_square_label_exp)
        missing_square_label_exp.next_to(missing_square_label[-2], UP+RIGHT, buff=0.05).align_to(missing_square_label[-2], UP)
        missing_square_label.move_to(missing_square.get_center())

        self.play(Create(missing_square), Write(missing_square_label))
        self.wait(1)
        
        # Fade out geometric elements and labels
        self.play(
            FadeOut(x_square, x_label_left, x_label_top, half_b_rect1, half_b_rect2, missing_square),
            FadeOut(b_over_2_label_right, b_over_2_label_bottom, missing_square_label)
        )
        self.wait(0.5)

        # --- Beat 3: Completing the Square - Algebraic Translation ---
        # Bring back simplified equation
        self.play(simplified_equation.animate.move_to(UP*2))

        # Add and subtract (b/2)^2
        plus_term_b_over_2_sq_num = Text("b", color=LIGHT_GOLD)
        plus_term_b_over_2_sq_den = Text("2", color=WHITE_TEXT)
        plus_term_b_over_2_frac = create_fraction(plus_term_b_over_2_sq_num, plus_term_b_over_2_sq_den)
        plus_term_b_over_2_exp = create_exponent(VGroup(Text("(", color=WHITE_TEXT), Text(")", color=WHITE_TEXT)), color=WHITE_TEXT) # Dummy for exp position
        plus_b_over_2_squared = VGroup(Text("+", color=WHITE_TEXT), Text("(", color=WHITE_TEXT), plus_term_b_over_2_frac, Text(")", color=WHITE_TEXT)).arrange(RIGHT, buff=0.05)
        plus_term_b_over_2_exp.next_to(plus_b_over_2_squared[-1], UP+RIGHT, buff=0.05).align_to(plus_b_over_2_squared[-1], UP)
        plus_b_over_2_squared.add(plus_term_b_over_2_exp)

        minus_term_b_over_2_sq_num = Text("b", color=LIGHT_GOLD)
        minus_term_b_over_2_sq_den = Text("2", color=WHITE_TEXT)
        minus_term_b_over_2_frac = create_fraction(minus_term_b_over_2_sq_num, minus_term_b_over_2_sq_den)
        minus_term_b_over_2_exp = create_exponent(VGroup(Text("(", color=WHITE_TEXT), Text(")", color=WHITE_TEXT)), color=WHITE_TEXT) # Dummy for exp position
        minus_b_over_2_squared = VGroup(Text("-", color=WHITE_TEXT), Text("(", color=WHITE_TEXT), minus_term_b_over_2_frac, Text(")", color=WHITE_TEXT)).arrange(RIGHT, buff=0.05)
        minus_term_b_over_2_exp.next_to(minus_b_over_2_squared[-1], UP+RIGHT, buff=0.05).align_to(minus_b_over_2_squared[-1], UP)
        minus_b_over_2_squared.add(minus_term_b_over_2_exp)

        # Assemble new equation line
        expanded_equation = VGroup(
            simplified_equation.submobjects[0].copy(), # x^2
            simplified_equation.submobjects[1].copy(), # +bx
            plus_b_over_2_squared.copy(), # + (b/2)^2
            minus_b_over_2_squared.copy(), # - (b/2)^2
            simplified_equation.submobjects[2].copy(), # +c
            simplified_equation.submobjects[3].copy()  # =0
        ).arrange(RIGHT, buff=0.2).move_to(simplified_equation.get_center())

        self.play(ReplacementTransform(simplified_equation, expanded_equation))
        self.wait(1)

        # Group (x^2 + bx + (b/2)^2) as (x + b/2)^2
        term_x = Text("x", color=LIGHT_BLUE)
        term_plus_b_over_2_num = Text("b", color=LIGHT_GOLD)
        term_plus_b_over_2_den = Text("2", color=WHITE_TEXT)
        term_plus_b_over_2_frac = create_fraction(term_plus_b_over_2_num, term_plus_b_over_2_den)
        
        x_plus_b_over_2_squared_group = VGroup(Text("(", color=WHITE_TEXT), term_x, Text("+", color=WHITE_TEXT), term_plus_b_over_2_frac, Text(")", color=WHITE_TEXT)).arrange(RIGHT, buff=0.05)
        x_plus_b_over_2_squared_exp = create_exponent(x_plus_b_over_2_squared_group[-1], color=WHITE_TEXT)
        x_plus_b_over_2_squared_group.add(x_plus_b_over_2_squared_exp)

        completed_square_equation = VGroup(
            x_plus_b_over_2_squared_group.copy(),
            expanded_equation.submobjects[3].copy(), # - (b/2)^2
            expanded_equation.submobjects[4].copy(), # +c
            expanded_equation.submobjects[5].copy()  # =0
        ).arrange(RIGHT, buff=0.2).move_to(expanded_equation.get_center())

        self.play(ReplacementTransform(expanded_equation, completed_square_equation))
        self.wait(1)

        # Isolate (x + b/2)^2
        term_rhs_b_num = Text("b", color=LIGHT_GOLD)
        term_rhs_b_den = Text("2", color=WHITE_TEXT)
        term_rhs_b_frac = create_fraction(term_rhs_b_num, term_rhs_b_den)
        term_rhs_b_exp = create_exponent(VGroup(Text("(", color=WHITE_TEXT), Text(")", color=WHITE_TEXT)), color=WHITE_TEXT) # Dummy for exp position
        rhs_b_over_2_squared = VGroup(Text("(", color=WHITE_TEXT), term_rhs_b_frac, Text(")", color=WHITE_TEXT)).arrange(RIGHT, buff=0.05)
        term_rhs_b_exp.next_to(rhs_b_over_2_squared[-1], UP+RIGHT, buff=0.05).align_to(rhs_b_over_2_squared[-1], UP)
        rhs_b_over_2_squared.add(term_rhs_b_exp)

        isolated_completed_square = VGroup(
            completed_square_equation.submobjects[0].copy(), # (x + b/2)^2
            completed_square_equation.submobjects[3].submobjects[0].copy(), # =
            rhs_b_over_2_squared.copy(), # (b/2)^2 (moved from LHS negative to RHS positive)
            VGroup(Text("-", color=WHITE_TEXT), completed_square_equation.submobjects[2].submobjects[1].copy()) # -c
        ).arrange(RIGHT, buff=0.2).move_to(completed_square_equation.get_center())

        self.play(ReplacementTransform(completed_square_equation, isolated_completed_square))
        self.wait(1)

        # Take square root of both sides
        lhs_sqrt_term = VGroup(
            Text("x", color=LIGHT_BLUE),
            Text("+", color=WHITE_TEXT),
            create_fraction(Text("b", color=LIGHT_GOLD), Text("2", color=WHITE_TEXT))
        ).arrange(RIGHT, buff=0.1)

        rhs_sqrt_content = VGroup(
            isolated_completed_square.submobjects[2].copy(), # (b/2)^2
            isolated_completed_square.submobjects[3].copy()  # -c
        ).arrange(RIGHT, buff=0.1)
        rhs_sqrt = create_sqrt_term(rhs_sqrt_content)

        sqrt_equation = VGroup(
            lhs_sqrt_term,
            isolated_completed_square.submobjects[1].copy(), # =
            Text("±", color=WHITE_TEXT),
            rhs_sqrt
        ).arrange(RIGHT, buff=0.2).move_to(isolated_completed_square.get_center())

        self.play(ReplacementTransform(isolated_completed_square, sqrt_equation))
        self.wait(1)

        # Isolate x
        final_x_isolated = VGroup(
            Text("x", color=LIGHT_BLUE),
            sqrt_equation.submobjects[1].copy(), # =
            VGroup(Text("-", color=WHITE_TEXT), create_fraction(Text("b", color=LIGHT_GOLD), Text("2", color=WHITE_TEXT))).arrange(RIGHT, buff=0.1), # -b/2
            sqrt_equation.submobjects[2].copy(), # ±
            sqrt_equation.submobjects[3].copy()  # sqrt term
        ).arrange(RIGHT, buff=0.2).move_to(sqrt_equation.get_center())

        self.play(ReplacementTransform(sqrt_equation, final_x_isolated))
        self.wait(1)
        
        # --- Beat 4: The Quadratic Formula ---
        # Introduce the general formula
        general_formula_intro = Text("This is for a=1. For any 'a':", color=WHITE_TEXT).scale(0.7).next_to(final_x_isolated, UP, buff=0.5)
        self.play(FadeIn(general_formula_intro))
        self.wait(1)

        # Construct the full quadratic formula
        # Numerator: -b ± sqrt(b^2 - 4ac)
        num_neg_b = Text("-b", color=LIGHT_GOLD)
        num_plus_minus = Text("±", color=WHITE_TEXT)
        
        # Discriminant (b^2 - 4ac)
        disc_b = Text("b", color=LIGHT_GOLD)
        disc_exp = create_exponent(disc_b, color=LIGHT_GOLD)
        disc_term_b2 = VGroup(disc_b, disc_exp)
        disc_minus = Text("-", color=WHITE_TEXT)
        disc_4 = Text("4", color=WHITE_TEXT)
        disc_a = Text("a", color=LIGHT_GOLD)
        disc_c = Text("c", color=LIGHT_GOLD)
        discriminant_content = VGroup(disc_term_b2, disc_minus, disc_4, disc_a, disc_c).arrange(RIGHT, buff=0.1)
        
        num_sqrt_discriminant = create_sqrt_term(discriminant_content)
        
        numerator_vgroup = VGroup(num_neg_b, num_plus_minus, num_sqrt_discriminant).arrange(RIGHT, buff=0.15)
        
        # Denominator: 2a
        den_2 = Text("2", color=WHITE_TEXT)
        den_a = Text("a", color=LIGHT_GOLD)
        denominator_vgroup = VGroup(den_2, den_a).arrange(RIGHT, buff=0.05)

        # Main fraction line
        formula_frac_line = Line(LEFT, RIGHT, color=WHITE_TEXT).set_width(max(numerator_vgroup.width, denominator_vgroup.width) * 1.1)
        
        # Assemble formula
        formula_equals_x = VGroup(Text("x", color=LIGHT_BLUE), Text("=", color=WHITE_TEXT)).arrange(RIGHT, buff=0.2)
        
        quadratic_formula = VGroup(formula_equals_x, formula_frac_line, numerator_vgroup, denominator_vgroup).center().scale(0.9)
        
        # Position parts relative to frac_line
        quadratic_formula.submobjects[2].next_to(quadratic_formula.submobjects[1], UP, buff=0.2) # Numerator
        quadratic_formula.submobjects[3].next_to(quadratic_formula.submobjects[1], DOWN, buff=0.2) # Denominator
        quadratic_formula.submobjects[0].next_to(quadratic_formula.submobjects[1], LEFT, buff=0.5).align_to(quadratic_formula.submobjects[1], LEFT) # x =

        self.play(
            FadeOut(final_x_isolated, general_formula_intro),
            FadeIn(quadratic_formula)
        )
        self.wait(1.5)

        formula_label = Text("The Quadratic Formula", color=GOLD_ACCENT).next_to(quadratic_formula, UP, buff=0.5)
        self.play(Write(formula_label))
        self.wait(2)

        # --- Beat 5: Recap Card ---
        self.play(FadeOut(quadratic_formula, formula_label))
        self.wait(0.5)

        recap_title = Text("Recap", color=LIGHT_BLUE).scale(1.2).to_edge(UP)
        self.play(Write(recap_title))

        # Bullet 1: Quadratic Equation definition
        recap_b1_ax2 = VGroup(Text("ax", color=LIGHT_GOLD), create_exponent(Text("ax", color=LIGHT_GOLD), color=LIGHT_GOLD))
        recap_b1_eq = VGroup(Text("• Quadratic Equation: ", color=WHITE_TEXT), recap_b1_ax2, Text("+bx+c=0", color=WHITE_TEXT)).arrange(RIGHT, buff=0.05).scale(0.7)
        recap_b1_eq.submobjects[1].next_to(recap_b1_eq.submobjects[0], RIGHT, buff=0.05)
        recap_b1_eq.submobjects[2].next_to(recap_b1_eq.submobjects[1], RIGHT, buff=0.05) # Need to shift this.
        
        # Manually fix spacing for recap_b1_eq due to exponent
        recap_b1_eq = VGroup(
            Text("• Quadratic Equation: ", color=WHITE_TEXT),
            Text("a", color=LIGHT_GOLD), Text("x", color=LIGHT_GOLD), create_exponent(Text("x", color=LIGHT_GOLD), color=LIGHT_GOLD),
            Text("+bx+c=0", color=WHITE_TEXT)
        )
        recap_b1_eq[1].next_to(recap_b1_eq[0], RIGHT, buff=0.05)
        recap_b1_eq[2].next_to(recap_b1_eq[1], RIGHT, buff=0.05)
        recap_b1_eq[3].next_to(recap_b1_eq[2], UP+RIGHT, buff=0.05).align_to(recap_b1_eq[2], UP)
        recap_b1_eq[4].next_to(recap_b1_eq[3], RIGHT, buff=0.05) # This will likely be too close
        recap_b1_eq = VGroup(recap_b1_eq[0], recap_b1_eq[1], recap_b1_eq[2], recap_b1_eq[3], recap_b1_eq[4]).arrange(RIGHT, buff=0.05).scale(0.7)


        bullet2_text = Text("• Roots are x-intercepts of the parabola.", color=WHITE_TEXT).scale(0.7)
        bullet3_text = Text("• Formula derived by Completing the Square.", color=WHITE_TEXT).scale(0.7)
        
        # Bullet 4: Quadratic Formula itself (simplified for recap display)
        recap_formula_num_content = VGroup(
            Text("-b ", color=LIGHT_GOLD),
            Text("± ", color=WHITE_TEXT),
            Text("b", color=WHITE_TEXT), create_exponent(Text("b", color=WHITE_TEXT), color=WHITE_TEXT), Text("-4ac", color=WHITE_TEXT)
        ).arrange(RIGHT, buff=0.05)
        
        recap_formula_num_content.submobjects[3].next_to(recap_formula_num_content.submobjects[2], UP+RIGHT, buff=0.05).align_to(recap_formula_num_content.submobjects[2], UP)
        recap_formula_num_content.submobjects[4].next_to(recap_formula_num_content.submobjects[3], RIGHT, buff=0.05)
        
        recap_formula_num_sqrt = create_sqrt_term(VGroup(
            recap_formula_num_content.submobjects[2], # b
            recap_formula_num_content.submobjects[3], # 2
            recap_formula_num_content.submobjects[4]  # -4ac
        ))
        
        recap_formula_num = VGroup(
            recap_formula_num_content.submobjects[0], # -b
            recap_formula_num_content.submobjects[1], # +-
            recap_formula_num_sqrt # sqrt term
        ).arrange(RIGHT, buff=0.1)

        recap_formula_den = Text("2a", color=LIGHT_GOLD)
        recap_frac = create_fraction(recap_formula_num, recap_formula_den)
        recap_formula_full = VGroup(Text("x = ", color=WHITE_TEXT), recap_frac).arrange(RIGHT, buff=0.2).scale(0.7)

        recap_bullets = VGroup(
            recap_b1_eq,
            bullet2_text,
            bullet3_text,
            VGroup(Text("• Quadratic Formula: ", color=WHITE_TEXT), recap_formula_full).arrange(RIGHT, buff=0.2).scale(1/0.7).scale(0.7) # Correct scale after nesting
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(recap_title, DOWN, buff=0.8)

        self.play(LaggedStart(*[Write(bullet) for bullet in recap_bullets], lag_ratio=0.7))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_bullets))
        self.wait(1)