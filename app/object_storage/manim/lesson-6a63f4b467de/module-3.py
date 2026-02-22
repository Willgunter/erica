from manim import *

class ParabolaXInterceptsDiscriminant(Scene):
    def construct(self):
        # --- Configuration for 3Blue1Brown style ---
        self.camera.background_color = BLACK
        blue_color = BLUE_C # Using a slightly darker blue for better contrast
        gold_color = GOLD_C # Using a slightly darker gold for better contrast

        # --- Helper functions for no Tex/MathTex ---
        def create_quadratic_equation_text(a_val="a", b_val="b", c_val="c", color=blue_color):
            eq_y = Text("y", color=color).scale(0.8)
            eq_equals = Text("=", color=gold_color).scale(0.8)
            
            # ax^2 term
            eq_ax2_a = Text(a_val, color=color).scale(0.8)
            eq_ax2_x = Text("x", color=color).scale(0.8).next_to(eq_ax2_a, RIGHT, buff=0.05)
            eq_ax2_2 = Text("2", font_size=25, color=color).align_to(eq_ax2_x, UP).shift(0.08 * RIGHT + 0.05 * UP)
            ax2_term = VGroup(eq_ax2_a, eq_ax2_x, eq_ax2_2)
            
            eq_plus1 = Text("+", color=gold_color).scale(0.8)
            
            # bx term
            eq_bx_b = Text(b_val, color=color).scale(0.8)
            eq_bx_x = Text("x", color=color).scale(0.8).next_to(eq_bx_b, RIGHT, buff=0.05)
            bx_term = VGroup(eq_bx_b, eq_bx_x)
            
            eq_plus2 = Text("+", color=gold_color).scale(0.8)
            eq_c = Text(c_val, color=color).scale(0.8)

            # Arrange the whole equation
            equation_elements = VGroup(eq_y, eq_equals, ax2_term, eq_plus1, bx_term, eq_plus2, eq_c)
            equation_elements.arrange(RIGHT, buff=0.15)
            return equation_elements

        def create_discriminant_expression(color=blue_color):
            # b^2 term
            b2 = Text("b", color=color).scale(0.7)
            power_2 = Text("2", font_size=20, color=color).align_to(b2, UP).shift(0.05 * RIGHT + 0.05 * UP)
            b2_term = VGroup(b2, power_2)
            
            minus = Text("-", color=gold_color).scale(0.7)
            four = Text("4", color=color).scale(0.7)
            a_val = Text("a", color=color).scale(0.7)
            c_val = Text("c", color=color).scale(0.7)

            discriminant = VGroup(b2_term, minus, four, a_val, c_val).arrange(RIGHT, buff=0.08)
            return discriminant

        # --- Beat 1: Visual Hook & Introducing the Parabola ---
        title = Text("Parabola's X-Intercepts and the Discriminant", color=gold_color).scale(0.9)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_corner(UP_LEFT).scale(0.7), run_time=0.8)

        # Create a NumberPlane
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-3, 5, 1],
            x_length=10, y_length=6,
            axis_config={"color": GREY_B},
            background_line_style={"stroke_opacity": 0.4}
        ).shift(DOWN * 0.5)
        
        # Add a coordinate system with axes labels
        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 5, 1],
            x_length=10, y_length=6,
            axis_config={"color": GREY_B}
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label("X", edge=RIGHT, direction=UP)
        y_label = axes.get_y_axis_label("Y", edge=UP, direction=RIGHT)
        
        # Initial parabola (2 intercepts)
        parabola_1 = plane.get_graph(lambda x: 0.5 * x**2 - 2, color=blue_color, x_range=[-3.5, 3.5])
        
        self.play(
            Create(plane),
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        self.play(Create(parabola_1), run_time=1)
        self.wait(0.5)

        # Introduce the general form of a quadratic equation
        eq_text = create_quadratic_equation_text().next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(FadeIn(eq_text, shift=UP))
        self.wait(1)

        # Highlight x-intercepts
        intercept_dots_1 = VGroup(
            Dot(plane.coords_to_point(-2, 0), color=gold_color),
            Dot(plane.coords_to_point(2, 0), color=gold_color)
        )
        x_intercepts_text = Text("X-Intercepts (where y = 0)", color=gold_color).scale(0.6)
        x_intercepts_text.next_to(eq_text, DOWN, buff=0.5).to_edge(LEFT)
        
        self.play(
            FadeIn(intercept_dots_1),
            Write(x_intercepts_text),
            run_time=1
        )
        self.wait(1)

        # --- Beat 2: Exploring Different Numbers of X-Intercepts ---
        self.play(FadeOut(intercept_dots_1))

        # Parabola with 1 intercept (tangent)
        parabola_2 = plane.get_graph(lambda x: 0.5 * x**2, color=blue_color, x_range=[-3.5, 3.5])
        self.play(Transform(parabola_1, parabola_2), run_time=1)
        intercept_dot_2 = Dot(plane.coords_to_point(0, 0), color=gold_color)
        self.play(FadeIn(intercept_dot_2), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(intercept_dot_2))

        # Parabola with 0 intercepts
        parabola_3 = plane.get_graph(lambda x: 0.5 * x**2 + 2, color=blue_color, x_range=[-3.5, 3.5])
        self.play(Transform(parabola_1, parabola_3), run_time=1)
        self.wait(0.8)

        # Animate back to 2 intercepts
        self.play(Transform(parabola_1, plane.get_graph(lambda x: 0.5 * x**2 - 2, color=blue_color, x_range=[-3.5, 3.5])), run_time=1)
        self.play(FadeIn(intercept_dots_1))
        self.wait(1)
        
        # --- Beat 3: Introducing the Discriminant (Intuition first) ---
        # "where y = 0" transforms to "ax^2 + bx + c = 0"
        equation_zero_text = create_quadratic_equation_text(color=blue_color)
        equation_zero_text_y = equation_zero_text.submobjects[0] # The "y" part
        # Extract the "= ax^2 + bx + c" part for transformation
        equation_zero_text_rest = VGroup(*equation_zero_text.submobjects[1:]) 
        equation_zero_text_rest.move_to(eq_text.get_center()) # Start from position of previous equation
        
        zero_text = Text("0", color=gold_color).scale(0.8)
        zero_text.move_to(equation_zero_text_y.get_center()) # Position "0" where "y" is
        
        self.play(
            ReplacementTransform(eq_text, equation_zero_text_rest),
            Transform(equation_zero_text_y, zero_text), # Replace 'y' with '0'
            x_intercepts_text.animate.next_to(zero_text, DOWN, buff=0.5).align_to(zero_text, LEFT) # reposition x-intercepts text
        )
        self.wait(1)

        # Introduce the quadratic formula (conceptual, not full formula at first)
        quadratic_formula_idea = Text("This equation has solutions given by...", color=gold_color).scale(0.7)
        quadratic_formula_idea.next_to(equation_zero_text_rest, DOWN, buff=1.0)
        self.play(Write(quadratic_formula_idea))
        self.wait(1)
        
        # Build parts of the quadratic formula (simplified visual)
        minus_b = Text("-b", color=blue_color).scale(0.7)
        plus_minus = Text("±", color=gold_color).scale(0.7)
        sqrt_symbol = Text("√", color=gold_color).scale(0.8)
        discriminant_expr = create_discriminant_expression().scale(0.9)
        over_2a = Text(" / 2a", color=blue_color).scale(0.7) # Simplified division line

        # Position elements intuitively
        main_terms = VGroup(minus_b, plus_minus)
        main_terms.arrange(RIGHT, buff=0.2)
        
        sqrt_group_placeholder = VGroup(sqrt_symbol, discriminant_expr).arrange(RIGHT, buff=0.1) # Group temporarily for positioning
        
        formula_parts = VGroup(main_terms, sqrt_group_placeholder, over_2a).arrange(RIGHT, buff=0.2)
        formula_parts.next_to(quadratic_formula_idea, DOWN, buff=0.5)

        self.play(
            FadeOut(quadratic_formula_idea),
            FadeIn(main_terms),
            FadeIn(sqrt_symbol.next_to(main_terms, RIGHT, buff=0.2)), # Position sqrt_symbol relative to main_terms
            FadeIn(over_2a.next_to(sqrt_symbol, RIGHT, buff=1.0)), # Position over_2a further right
            run_time=1
        )
        # Position discriminant_expr relative to sqrt_symbol
        self.play(FadeIn(discriminant_expr.move_to(sqrt_symbol.get_center() + RIGHT * 0.7)), run_time=1)
        self.wait(1)
        
        # Highlight the discriminant part
        discriminant_box = SurroundingRectangle(discriminant_expr, color=gold_color, buff=0.1)
        self.play(Create(discriminant_box), run_time=0.7)
        self.wait(0.5)

        # Introduce the term "Discriminant"
        discriminant_label = Text("Discriminant", color=gold_color).scale(0.7)
        discriminant_label.next_to(discriminant_box, DOWN, buff=0.5)
        self.play(Write(discriminant_label))
        self.wait(1)

        # Fade out quadratic formula parts
        self.play(
            FadeOut(main_terms),
            FadeOut(sqrt_symbol),
            FadeOut(over_2a),
            FadeOut(discriminant_box),
            FadeOut(discriminant_expr), # fade out the expression under sqrt
            FadeOut(discriminant_label),
            run_time=1
        )
        
        # --- Beat 4: Formalizing the Discriminant ---
        # Bring back the discriminant expression
        discriminant_expr_clean = create_discriminant_expression(color=blue_color).scale(1.0)
        delta_symbol = Text("Δ", color=gold_color).scale(1.2)
        equals_sign = Text("=", color=gold_color).scale(1.0)
        
        discriminant_formal = VGroup(delta_symbol, equals_sign, discriminant_expr_clean).arrange(RIGHT, buff=0.2)
        discriminant_formal.move_to(ORIGIN) # Center temporarily for animation
        
        # Fade out previous equation elements and bring in discriminant formal
        self.play(
            FadeOut(parabola_1), # The last parabola shown
            FadeOut(intercept_dots_1),
            FadeOut(equation_zero_text_rest), # Fade out the ax^2 + bx + c part
            FadeOut(zero_text), # Fade out the 0
            FadeOut(x_intercepts_text),
            FadeIn(discriminant_formal),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Reposition discriminant formal and prepare for case texts
        self.play(discriminant_formal.animate.to_corner(UP_LEFT).shift(RIGHT*1.5), run_time=1)
        self.wait(0.5)

        # Three cases
        case1_text = Text("Δ > 0 : Two Real Roots", color=blue_color).scale(0.7).next_to(discriminant_formal, DOWN, buff=0.8).align_to(discriminant_formal, LEFT)
        case2_text = Text("Δ = 0 : One Real Root", color=blue_color).scale(0.7).next_to(case1_text, DOWN, buff=0.3).align_to(case1_text, LEFT)
        case3_text = Text("Δ < 0 : Zero Real Roots", color=blue_color).scale(0.7).next_to(case2_text, DOWN, buff=0.3).align_to(case2_text, LEFT)

        self.play(Write(case1_text), run_time=0.8)
        self.wait(0.5)
        self.play(Write(case2_text), run_time=0.8)
        self.wait(0.5)
        self.play(Write(case3_text), run_time=0.8)
        self.wait(1)

        # Animate parabolas corresponding to each case on the right side of the screen
        parabola_base_x_shift = RIGHT * 3.5 # Consistent X position for example parabolas

        # Parabola for Δ > 0 (two x-intercepts)
        parabola_two_roots = plane.get_graph(lambda x: 0.5 * x**2 - 2, color=blue_color, x_range=[-3.5, 3.5]).shift(parabola_base_x_shift)
        self.play(Create(parabola_two_roots), run_time=1)
        intercept_dots_two = VGroup(
            Dot(plane.coords_to_point(-2, -2), color=gold_color), # Coords relative to original plane
            Dot(plane.coords_to_point(2, -2), color=gold_color)
        ).shift(parabola_base_x_shift) # Apply the same shift
        self.play(FadeIn(intercept_dots_two))
        self.wait(1)
        self.play(FadeOut(intercept_dots_two))
        self.play(FadeOut(parabola_two_roots), run_time=0.5)

        # Parabola for Δ = 0 (one x-intercept)
        parabola_one_root = plane.get_graph(lambda x: 0.5 * x**2, color=blue_color, x_range=[-3.5, 3.5]).shift(parabola_base_x_shift)
        self.play(Create(parabola_one_root), run_time=1)
        intercept_dot_one = Dot(plane.coords_to_point(0, 0), color=gold_color).shift(parabola_base_x_shift)
        self.play(FadeIn(intercept_dot_one))
        self.wait(1)
        self.play(FadeOut(intercept_dot_one))
        self.play(FadeOut(parabola_one_root), run_time=0.5)

        # Parabola for Δ < 0 (zero x-intercepts)
        parabola_zero_roots = plane.get_graph(lambda x: 0.5 * x**2 + 2, color=blue_color, x_range=[-3.5, 3.5]).shift(parabola_base_x_shift)
        self.play(Create(parabola_zero_roots), run_time=1)
        self.wait(1)
        self.play(FadeOut(parabola_zero_roots), run_time=0.5)

        # Fade out everything for recap
        self.play(
            FadeOut(plane), FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(title), FadeOut(discriminant_formal),
            FadeOut(case1_text), FadeOut(case2_text), FadeOut(case3_text),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: The Discriminant", color=gold_color).scale(0.9)
        recap_title.to_edge(UP, buff=0.8)

        # y = ax^2 + bx + c
        recap_y = Text("y", color=blue_color).scale(0.7)
        recap_equals = Text("=", color=gold_color).scale(0.7)
        recap_a = Text("a", color=blue_color).scale(0.7)
        recap_x1 = Text("x", color=blue_color).scale(0.7).next_to(recap_a, RIGHT, buff=0.05)
        recap_pow2_1 = Text("2", font_size=25, color=blue_color).align_to(recap_x1, UP).shift(0.08 * RIGHT + 0.05 * UP)
        recap_plus1 = Text("+", color=gold_color).scale(0.7)
        recap_b = Text("b", color=blue_color).scale(0.7)
        recap_x2 = Text("x", color=blue_color).scale(0.7).next_to(recap_b, RIGHT, buff=0.05)
        recap_plus2 = Text("+", color=gold_color).scale(0.7)
        recap_c = Text("c", color=blue_color).scale(0.7)
        
        recap_eq_line = VGroup(recap_y, recap_equals, recap_a, recap_x1, recap_pow2_1, recap_plus1, recap_b, recap_x2, recap_plus2, recap_c)
        recap_eq_line.arrange(RIGHT, buff=0.15)
        
        recap_text1_bullet = Text("-", color=gold_color).scale(0.7)
        recap_eq_group = VGroup(recap_text1_bullet, recap_eq_line).arrange(RIGHT, buff=0.2).to_edge(LEFT, buff=0.8)


        # Δ = b^2 - 4ac
        recap_delta = Text("Δ", color=gold_color).scale(0.7)
        recap_eq_sign_disc = Text("=", color=gold_color).scale(0.7)
        recap_b_disc = Text("b", color=blue_color).scale(0.7).next_to(recap_eq_sign_disc, RIGHT, buff=0.05)
        recap_pow2_disc = Text("2", font_size=25, color=blue_color).align_to(recap_b_disc, UP).shift(0.08 * RIGHT + 0.05 * UP)
        recap_minus = Text("-", color=gold_color).scale(0.7)
        recap_4 = Text("4", color=blue_color).scale(0.7)
        recap_a_disc = Text("a", color=blue_color).scale(0.7)
        recap_c_disc = Text("c", color=blue_color).scale(0.7)

        recap_discriminant_line = VGroup(recap_delta, recap_eq_sign_disc, recap_b_disc, recap_pow2_disc, recap_minus, recap_4, recap_a_disc, recap_c_disc)
        recap_discriminant_line.arrange(RIGHT, buff=0.15)

        recap_text_discriminant_bullet = Text("-", color=gold_color).scale(0.7)
        recap_discriminant_group = VGroup(recap_text_discriminant_bullet, recap_discriminant_line).arrange(RIGHT, buff=0.2).to_edge(LEFT, buff=0.8)


        recap_text2 = Text("- Δ > 0 : Two Real X-Intercepts", color=gold_color).scale(0.7).to_edge(LEFT, buff=0.8)
        recap_text3 = Text("- Δ = 0 : One Real X-Intercept", color=gold_color).scale(0.7).to_edge(LEFT, buff=0.8)
        recap_text4 = Text("- Δ < 0 : Zero Real X-Intercepts", color=gold_color).scale(0.7).to_edge(LEFT, buff=0.8)
        
        recap_elements = VGroup(
            recap_eq_group,
            recap_discriminant_group,
            recap_text2,
            recap_text3,
            recap_text4
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(recap_title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(mob, shift=UP) for mob in recap_elements], lag_ratio=0.4), run_time=3)
        self.wait(3)