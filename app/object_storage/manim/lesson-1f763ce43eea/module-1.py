from manim import *

# Define custom colors
BLUE_MANIM = "#58C4DD"  # A nice bright blue
GOLD_MANIM = "#FFD700"  # Standard Gold

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        self.camera.background_color = "#202020" # Dark background

        # Helper functions for "no Tex" math elements
        def create_text_squared(base_mobject, font_size=40, color=WHITE):
            """Creates a VGroup for a squared term, accepting a Mobject as the base."""
            exponent = Text("2", font_size=font_size * 0.7, color=color).next_to(base_mobject, UP + RIGHT, buff=0.05).shift(UP * 0.1)
            return VGroup(base_mobject, exponent)

        def create_text_fraction(numerator_mobject, denominator_mobject, font_size=40, color=WHITE):
            """Creates a VGroup for a fraction, accepting Mobjects for numerator and denominator."""
            line = Line(LEFT * 0.5, RIGHT * 0.5, color=color).set_width(max(numerator_mobject.width, denominator_mobject.width) * 1.1)

            numerator_mobject.next_to(line, UP, buff=0.1)
            denominator_mobject.next_to(line, DOWN, buff=0.1)
            return VGroup(numerator_mobject, line, denominator_mobject)

        def create_sqrt_vgroup(content_mobject, font_size=40, color=WHITE):
            """Creates a VGroup for a square root, with a custom radical symbol and overline."""
            # This creates the radical symbol (root checkmark)
            sqrt_char = Text("√", font_size=font_size * 1.5, color=color).shift(DOWN * 0.1) 
            
            # Position content to the right of the radical symbol
            content_mobject.next_to(sqrt_char, RIGHT, buff=0.05).align_to(sqrt_char, DOWN)
            
            # Create the line above the content
            # It starts roughly where the radical symbol visually "ends" its vertical part
            line_start_x = sqrt_char.get_right()[0] - sqrt_char.width * 0.2 
            line_end_x = content_mobject.get_right()[0] + 0.1 
            
            # Position slightly above content
            line_y = content_mobject.get_top()[1] + 0.1 
            
            over_line = Line(
                [line_start_x, line_y, 0],
                [line_end_x, line_y, 0],
                color=color,
                stroke_width=2
            )
            
            return VGroup(sqrt_char, content_mobject, over_line)

        # Beat 1: The Parabola and the Problem (Visual Hook)
        self.next_section("Visual Hook & Introduction")
        title = Text("Defining and Deriving", font_size=60, color=GOLD_MANIM).to_edge(UP, buff=0.5)
        subtitle = Text("The Quadratic Formula", font_size=40, color=BLUE_MANIM).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": BLUE_MANIM, "stroke_width": 2},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False}
        ).to_edge(LEFT, buff=0.5).scale(0.9).shift(DOWN*0.5)

        parabola = axes.get_graph(lambda x: 0.5 * x**2 - 1.5, color=GOLD_MANIM, stroke_width=4)
        x_intercept1 = Dot(axes.c2p(-np.sqrt(3), 0), color=BLUE_MANIM, radius=0.15)
        x_intercept2 = Dot(axes.c2p(np.sqrt(3), 0), color=BLUE_MANIM, radius=0.15)
        
        question_text = Text("Where does it cross the x-axis?", font_size=36, color=WHITE).next_to(axes, RIGHT, buff=1).align_to(title, DOWN).shift(DOWN*0.5)
        
        self.play(Create(axes), Create(parabola))
        self.play(FadeIn(x_intercept1, x_intercept2), Write(question_text))
        self.wait(1.5)

        self.play(FadeOut(parabola, x_intercept1, x_intercept2, question_text, subtitle))
        self.play(axes.animate.to_edge(UP+LEFT).scale(0.5).shift(DOWN*0.5), FadeOut(axes)) 
        self.play(title.animate.to_edge(UP, buff=0.2).scale(0.8))

        # Standard form equation
        a_sq_term = VGroup(Text("a", color=GOLD_MANIM), create_text_squared(Text("x", color=BLUE_MANIM))).arrange(RIGHT, buff=0.05)
        b_x_term = VGroup(Text("b", color=GOLD_MANIM), Text("x", color=BLUE_MANIM)).arrange(RIGHT, buff=0.05)
        c_term = Text("c", color=GOLD_MANIM)
        
        plus1 = Text(" + ", color=WHITE)
        plus2 = Text(" + ", color=WHITE)
        equals_zero = Text(" = 0", color=WHITE)

        standard_form_vgroup = VGroup(a_sq_term, plus1, b_x_term, plus2, c_term, equals_zero).arrange(RIGHT, buff=0.2).to_center().shift(UP*1.5)

        intro_text = Text("The Standard Form:", font_size=36, color=WHITE).next_to(standard_form_vgroup, UP, buff=0.5)
        
        self.play(FadeIn(intro_text), LaggedStart(*[Write(mob) for mob in standard_form_vgroup], lag_ratio=0.1))
        self.wait(1)

        find_x_text = Text("Our Goal: Solve for 'x'!", font_size=40, color=BLUE_MANIM).next_to(standard_form_vgroup, DOWN, buff=1)
        self.play(Write(find_x_text))
        self.wait(1.5)
        self.play(FadeOut(intro_text, find_x_text, title))

        # Beat 2: Completing the Square - Visual Intuition
        self.next_section("Visualizing Completing the Square")
        self.play(standard_form_vgroup.animate.scale(0.7).to_corner(UL).shift(RIGHT*0.5 + DOWN*0.2))

        # Start with x^2 + bx
        x_val = 1.5 
        b_val = 1.0  

        x_square_obj = Square(side_length=x_val, color=BLUE_MANIM, fill_opacity=0.7).to_edge(LEFT, buff=1).shift(DOWN*0.5)
        x_label = Text("x", color=WHITE, font_size=30).move_to(x_square_obj)
        
        bx_rect_obj = Rectangle(width=b_val, height=x_val, color=GOLD_MANIM, fill_opacity=0.7).next_to(x_square_obj, RIGHT, buff=0)
        bx_label = Text("bx", color=WHITE, font_size=30).move_to(bx_rect_obj)

        self.play(Create(x_square_obj), Write(x_label))
        self.play(Create(bx_rect_obj), Write(bx_label))
        self.wait(0.5)

        # Split bx_rect
        half_b_val = b_val / 2
        bx_rect_half1 = Rectangle(width=half_b_val, height=x_val, color=GOLD_MANIM, fill_opacity=0.7).move_to(bx_rect_obj.get_center() + LEFT * half_b_val / 2)
        bx_rect_half2 = Rectangle(width=half_b_val, height=x_val, color=GOLD_MANIM, fill_opacity=0.7).move_to(bx_rect_obj.get_center() + RIGHT * half_b_val / 2)
        
        bx_label_half1 = Text("b/2 x", font_size=25, color=WHITE).move_to(bx_rect_half1)
        bx_label_half2 = Text("b/2 x", font_size=25, color=WHITE).move_to(bx_rect_half2)

        self.play(
            ReplacementTransform(bx_rect_obj, bx_rect_half1),
            ReplacementTransform(bx_rect_obj.copy(), bx_rect_half2),
            ReplacementTransform(bx_label, bx_label_half1),
            ReplacementTransform(bx_label.copy(), bx_label_half2)
        )
        self.wait(0.5)

        # Arrange to form L-shape
        self.play(
            bx_rect_half1.animate.next_to(x_square_obj, RIGHT, buff=0),
            bx_label_half1.animate.next_to(x_square_obj, RIGHT, buff=0).move_to(bx_rect_half1),
            bx_rect_half2.animate.next_to(x_square_obj, UP, buff=0).rotate(PI/2),
            bx_label_half2.animate.next_to(x_square_obj, UP, buff=0).rotate(PI/2).move_to(bx_rect_half2)
        )
        self.wait(1)
        
        # The missing piece
        missing_square = Square(side_length=half_b_val, color=RED, fill_opacity=0.5).next_to(bx_rect_half2, RIGHT, buff=0)
        missing_square.align_to(bx_rect_half1, UP) 
        
        b_over_2_frac = create_text_fraction(Text("b", color=WHITE), Text("2", color=WHITE), font_size=25, color=WHITE)
        b_over_2_sq_vgroup = create_text_squared(b_over_2_frac, font_size=25, color=WHITE).move_to(missing_square)

        self.play(FadeIn(missing_square))
        self.play(Write(b_over_2_sq_vgroup))
        self.wait(1)

        # Complete the square visualization
        combined_width = x_val + half_b_val
        completed_square_form = Square(side_length=combined_width, color=BLUE_MANIM, fill_opacity=0.7).move_to(x_square_obj.get_corner(DL) + RIGHT * combined_width / 2 + UP * combined_width / 2)
        
        parentheses_open = Text("(", color=WHITE, font_size=30)
        x_in_paren = Text("x", color=BLUE_MANIM, font_size=30)
        plus_in_paren = Text(" + ", color=WHITE, font_size=30)
        b_over_2_in_paren = create_text_fraction(Text("b", color=WHITE), Text("2", color=WHITE), font_size=30, color=WHITE)
        parentheses_close = Text(")", color=WHITE, font_size=30)

        inner_paren_group = VGroup(x_in_paren, plus_in_paren, b_over_2_in_paren).arrange(RIGHT, buff=0.1)
        x_plus_b_over_2_text = VGroup(parentheses_open, inner_paren_group, parentheses_close).arrange(RIGHT, buff=0.05)
        x_plus_b_over_2_sq_text = create_text_squared(x_plus_b_over_2_text, font_size=30, color=WHITE).move_to(completed_square_form)

        self.play(
            FadeOut(x_square_obj, bx_rect_half1, bx_rect_half2, missing_square,
                    x_label, bx_label_half1, bx_label_half2, b_over_2_sq_vgroup),
            FadeIn(completed_square_form),
            Write(x_plus_b_over_2_sq_text),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(completed_square_form, x_plus_b_over_2_sq_text))


        # Beat 3: Completing the Square - Algebraic Derivation
        self.next_section("Algebraic Completing the Square")

        current_equation = standard_form_vgroup # Re-use and transform

        # Step 1: Divide by 'a'
        divide_by_a_text = Text("1. Divide by 'a'", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(divide_by_a_text))

        x_sq_term_eq = create_text_squared(Text("x", color=BLUE_MANIM))
        bx_over_a_frac = create_text_fraction(Text("b", color=GOLD_MANIM), Text("a", color=GOLD_MANIM))
        bx_over_a_term = VGroup(bx_over_a_frac, Text("x", color=BLUE_MANIM)).arrange(RIGHT, buff=0.05)
        c_over_a_frac = create_text_fraction(Text("c", color=GOLD_MANIM), Text("a", color=GOLD_MANIM))

        eq1_plus1 = Text(" + ", color=WHITE)
        eq1_plus2 = Text(" + ", color=WHITE)
        eq1_equals_zero = Text(" = 0", color=WHITE)

        equation1_parts = VGroup(x_sq_term_eq, eq1_plus1, bx_over_a_term, eq1_plus2, c_over_a_frac, eq1_equals_zero).arrange(RIGHT, buff=0.2)
        self.play(Transform(current_equation, equation1_parts))
        self.wait(1)

        # Step 2: Move c/a to the right side
        self.play(divide_by_a_text.animate.to_corner(UL).shift(DOWN*0.5).set_color(WHITE).set_opacity(0.5))
        move_c_text = Text("2. Move 'c/a' to right", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(move_c_text))

        minus_c_over_a_vgroup = VGroup(Text("-", color=WHITE), c_over_a_frac.copy()).arrange(RIGHT, buff=0.05)

        equation2_left = VGroup(x_sq_term_eq.copy(), eq1_plus1.copy(), bx_over_a_term.copy()).arrange(RIGHT, buff=0.2)
        equation2_right = VGroup(eq1_equals_zero.copy()[0], minus_c_over_a_vgroup).arrange(RIGHT, buff=0.2) # eq1_equals_zero[0] is "="
        equation2_parts = VGroup(equation2_left, equation2_right).arrange(RIGHT, buff=0.2)
        self.play(Transform(current_equation, equation2_parts))
        self.wait(1)

        # Step 3: Complete the Square
        self.play(move_c_text.animate.to_corner(UL).shift(DOWN*0.5).set_color(WHITE).set_opacity(0.5))
        complete_square_text = Text("3. Add (b/2a)^2 to both sides", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(complete_square_text))

        b_over_2a_frac_mobj = create_text_fraction(Text("b", color=GOLD_MANIM), Text("2a", color=GOLD_MANIM))
        b_over_2a_sq_term = create_text_squared(b_over_2a_frac_mobj)

        eq3_lhs_added_term = VGroup(Text(" + ", color=WHITE), b_over_2a_sq_term.copy()).arrange(RIGHT, buff=0.05)
        eq3_rhs_added_term = VGroup(Text(" + ", color=WHITE), b_over_2a_sq_term.copy()).arrange(RIGHT, buff=0.05)

        equation3_left = VGroup(equation2_left.copy(), eq3_lhs_added_term).arrange(RIGHT, buff=0.1)
        equation3_right = VGroup(equation2_right.copy(), eq3_rhs_added_term).arrange(RIGHT, buff=0.1)
        equation3_parts = VGroup(equation3_left, equation3_right).arrange(RIGHT, buff=0.2)
        self.play(Transform(current_equation, equation3_parts))
        self.wait(1.5)
        
        # Step 4: Factor Left Side
        self.play(complete_square_text.animate.to_corner(UL).shift(DOWN*0.5).set_color(WHITE).set_opacity(0.5))
        factor_left_text = Text("4. Factor Left Side", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(factor_left_text))

        # Re-use parts for (x + b/2a)^2
        x_plus_b_over_2a_inner = VGroup(Text("x", color=BLUE_MANIM), Text(" + ", color=WHITE), b_over_2a_frac_mobj.copy()).arrange(RIGHT, buff=0.05)
        lhs_paren_squared = create_text_squared(VGroup(Text("(", color=WHITE), x_plus_b_over_2a_inner, Text(")", color=WHITE)).arrange(RIGHT, buff=0.05))

        equation4_left = lhs_paren_squared
        equation4_right = equation3_right[1:] # Keep the = and the rest of the right side
        equation4_parts = VGroup(equation4_left, equation4_right).arrange(RIGHT, buff=0.2)
        self.play(Transform(current_equation, equation4_parts))
        self.wait(1.5)

        # Beat 4: Solving for x - The Formula
        self.next_section("Solving for x")
        self.play(factor_left_text.animate.to_corner(UL).shift(DOWN*0.5).set_color(WHITE).set_opacity(0.5))

        simplify_right_text = Text("5. Simplify Right Side", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(simplify_right_text))

        # Simplify right side: (b/2a)^2 - c/a = b^2/4a^2 - 4ac/4a^2 = (b^2 - 4ac) / 4a^2
        numerator_b_sq = create_text_squared(Text("b", color=GOLD_MANIM))
        numerator_4ac = VGroup(Text("4", color=WHITE), Text("a", color=GOLD_MANIM), Text("c", color=GOLD_MANIM)).arrange(RIGHT, buff=0.05)
        numerator_b_sq_minus_4ac = VGroup(numerator_b_sq, Text(" - ", color=WHITE), numerator_4ac).arrange(RIGHT, buff=0.05)
        
        denominator_4a_sq = VGroup(Text("4", color=WHITE), create_text_squared(Text("a", color=GOLD_MANIM))).arrange(RIGHT, buff=0.05)

        simplified_right_frac_mobj = create_text_fraction(numerator_b_sq_minus_4ac, denominator_4a_sq)

        equation5_right = VGroup(current_equation[1][0], simplified_right_frac_mobj).arrange(RIGHT, buff=0.2)
        equation5_parts = VGroup(equation4_left.copy(), equation5_right).arrange(RIGHT, buff=0.2)
        self.play(Transform(current_equation, equation5_parts))
        self.wait(1.5)

        # Step 6: Take Square Root of both sides
        self.play(simplify_right_text.animate.to_corner(UL).shift(DOWN*0.5).set_color(WHITE).set_opacity(0.5))
        take_sqrt_text = Text("6. Take Square Root", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(take_sqrt_text))

        plus_minus_sym = Text("±", color=WHITE)

        # Content for sqrt on numerator
        sqrt_numerator_content = numerator_b_sq_minus_4ac.copy()
        sqrt_numerator_vgroup = create_sqrt_vgroup(sqrt_numerator_content)
        
        denominator_2a_mobj = VGroup(Text("2", color=WHITE), Text("a", color=GOLD_MANIM)).arrange(RIGHT, buff=0.05)
        
        final_sqrt_frac_mobj = create_text_fraction(sqrt_numerator_vgroup, denominator_2a_mobj)
        
        equation6_right_part = VGroup(plus_minus_sym, final_sqrt_frac_mobj).arrange(RIGHT, buff=0.05)
        equation6_right = VGroup(current_equation[1][0].copy(), equation6_right_part).arrange(RIGHT, buff=0.2) # current_equation[1][0] is "="
        
        equation6_left = VGroup(Text("x", color=BLUE_MANIM), Text(" + ", color=WHITE), b_over_2a_frac_mobj.copy()).arrange(RIGHT, buff=0.05)
        equation6_parts = VGroup(equation6_left, equation6_right).arrange(RIGHT, buff=0.2)
        self.play(Transform(current_equation, equation6_parts))
        self.wait(1.5)

        # Step 7: Isolate x
        self.play(take_sqrt_text.animate.to_corner(UL).shift(DOWN*0.5).set_color(WHITE).set_opacity(0.5))
        isolate_x_text = Text("7. Isolate 'x'", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(isolate_x_text))

        minus_b_over_2a = VGroup(Text("-", color=WHITE), b_over_2a_frac_mobj.copy()).arrange(RIGHT, buff=0.05)
        
        equation7_right_part = VGroup(minus_b_over_2a, plus_minus_sym.copy(), final_sqrt_frac_mobj.copy()).arrange(RIGHT, buff=0.05)
        equation7_right = VGroup(current_equation[1][0].copy(), equation7_right_part).arrange(RIGHT, buff=0.2)
        
        equation7_left = Text("x", color=BLUE_MANIM)
        equation7_parts = VGroup(equation7_left, equation7_right).arrange(RIGHT, buff=0.2)
        self.play(Transform(current_equation, equation7_parts))
        self.wait(1.5)

        # Step 8: Combine fractions (final form)
        self.play(isolate_x_text.animate.to_corner(UL).shift(DOWN*0.5).set_color(WHITE).set_opacity(0.5))
        combine_fractions_text = Text("8. Combine Fractions", font_size=30, color=GOLD_MANIM).to_corner(UL)
        self.play(Write(combine_fractions_text))

        numerator_final = VGroup(Text("-", color=WHITE), Text("b", color=GOLD_MANIM), plus_minus_sym.copy(), sqrt_numerator_vgroup.copy()).arrange(RIGHT, buff=0.05)
        denominator_final = VGroup(Text("2", color=WHITE), Text("a", color=GOLD_MANIM)).arrange(RIGHT, buff=0.05)
        
        final_quadratic_formula_frac = create_text_fraction(numerator_final, denominator_final)

        final_formula_right = VGroup(current_equation[1][0].copy(), final_quadratic_formula_frac).arrange(RIGHT, buff=0.2)
        final_formula_left = Text("x", color=BLUE_MANIM)
        final_formula_vgroup = VGroup(final_formula_left, final_formula_right).arrange(RIGHT, buff=0.2).to_center().shift(UP*0.5)

        self.play(Transform(current_equation, final_formula_vgroup))
        self.wait(2)
        self.play(FadeOut(combine_fractions_text))

        # Beat 5: Recap Card
        self.next_section("Recap")
        self.play(FadeOut(*self.mobjects[:-1])) # Fade out everything except the final formula

        recap_title = Text("Recap: Quadratic Formula", font_size=50, color=GOLD_MANIM).to_edge(UP, buff=0.5)
        self.play(Write(recap_title))
        self.play(current_equation.animate.scale(1.2).next_to(recap_title, DOWN, buff=1))

        # Standard form
        standard_form_recap_label = Text("Standard Form:", font_size=30, color=WHITE).next_to(current_equation, UP, buff=1.5).align_to(current_equation, LEFT)
        standard_form_recap_eq = VGroup(
            a_sq_term.copy(), plus1.copy(), b_x_term.copy(), plus2.copy(), c_term.copy(), equals_zero.copy()
        ).arrange(RIGHT, buff=0.2).next_to(standard_form_recap_label, RIGHT, buff=0.2)
        
        self.play(FadeIn(standard_form_recap_label), Write(standard_form_recap_eq))
        self.wait(1)

        purpose_text = Text("Finds the roots (x-intercepts) of a quadratic equation.", font_size=36, color=BLUE_MANIM).next_to(current_equation, DOWN, buff=1.5)
        self.play(Write(purpose_text))
        self.wait(3)

        self.play(FadeOut(self.mobjects)) # Clear scene