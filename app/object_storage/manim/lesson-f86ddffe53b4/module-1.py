from manim import *

# Helper to create superscript for Text objects
def create_superscripted_text(base_str, super_str, base_font_size=35, super_font_size_factor=0.6, color=WHITE):
    base_text = Text(base_str, font_size=base_font_size, color=color)
    super_text = Text(super_str, font_size=base_font_size * super_font_size_factor, color=color)
    super_text.next_to(base_text, UP + RIGHT, buff=0.05).shift(0.05 * UP + 0.05 * RIGHT) # Manual fine-tune
    return VGroup(base_text, super_text)

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1D1D1D" # Dark background

        # --- Color definitions ---
        GOLD = "#FFD700"
        BLUE = "#1E90FF"
        WHITE = "#FFFFFF"
        GREY = "#808080"
        LIGHT_BLUE = "#ADD8E6"

        # --- Beat 0: Opening Hook - Projectile Motion & Problem Setup ---
        title = Text("Understanding the Quadratic Formula", font_size=60, color=WHITE).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.5)

        # Create a NumberPlane
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-3, 7, 1],
            x_length=10, y_length=8,
            axis_config={"color": GREY, "stroke_width": 2},
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.5}
        ).shift(DOWN * 0.5)
        plane_label_x = Text("x", color=GREY, font_size=25).next_to(plane.x_axis, RIGHT, buff=0.2)
        plane_label_y = Text("y", color=GREY, font_size=25).next_to(plane.y_axis, UP, buff=0.2)

        self.play(Create(plane), FadeIn(plane_label_x, plane_label_y), run_time=1.5)
        self.wait(0.5)

        # Illustrate a projectile path (parabola)
        parabola_func = lambda x: -0.5 * (x - 1)**2 + 4.5
        parabola = plane.get_graph(parabola_func, x_range=[-2.5, 4.5], color=GOLD, stroke_width=4)
        
        path_text = Text("Projectile Path", font_size=30, color=GOLD).next_to(parabola, UP + LEFT, buff=0.1).shift(RIGHT*0.5)

        self.play(
            Create(parabola),
            FadeIn(path_text),
            run_time=2
        )
        self.wait(0.5)

        problem_text = Text("Where does it land?", font_size=40, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problem_text, shift=DOWN))

        # Show the roots visually
        root1_coord = plane.coords_to_point(-2, 0)
        root2_coord = plane.coords_to_point(4, 0)
        root1_dot = Dot(root1_coord, color=BLUE, radius=0.15)
        root2_dot = Dot(root2_coord, color=BLUE, radius=0.15)
        
        self.play(
            LaggedStart(
                GrowFromCenter(root1_dot),
                GrowFromCenter(root2_dot),
                lag_ratio=0.5
            ),
            run_time=1.5
        )
        self.wait(1)

        # Fade out intro elements except plane
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(problem_text, shift=UP),
            FadeOut(path_text),
            FadeOut(parabola),
            FadeOut(root1_dot),
            FadeOut(root2_dot),
            run_time=1.5
        )
        self.wait(0.5)


        # --- Beat 1: The Problem - General Form ---
        beat1_title = Text("1. The Problem: Finding the Roots", font_size=45, color=WHITE).to_edge(UP)
        self.play(FadeIn(beat1_title), run_time=0.8)
        self.wait(0.5)

        # Introduce a simpler parabola for explanation
        current_parabola = plane.get_graph(lambda x: x**2 - 4, x_range=[-3, 3], color=GOLD, stroke_width=4)
        self.play(Create(current_parabola), run_time=1.5)

        root1_val = -2
        root2_val = 2
        root1_dot = Dot(plane.coords_to_point(root1_val, 0), color=BLUE, radius=0.15)
        root2_dot = Dot(plane.coords_to_point(root2_val, 0), color=BLUE, radius=0.15)
        
        self.play(
            GrowFromCenter(root1_dot),
            GrowFromCenter(root2_dot),
            run_time=1
        )

        question = Text("How do we find these x-values?", font_size=35, color=LIGHT_BLUE).next_to(beat1_title, DOWN, buff=0.5)
        self.play(Write(question), run_time=1.0)
        self.wait(1)

        # Introduce the general form using Text objects
        a_text = Text("a", color=BLUE, font_size=35)
        x_squared = create_superscripted_text("x", "2", base_font_size=35)

        plus_b = Text("+", font_size=35)
        b_text = Text("b", color=BLUE, font_size=35)
        x_linear = Text("x", font_size=35)

        plus_c = Text("+", font_size=35)
        c_text = Text("c", color=BLUE, font_size=35)

        equals_zero_parts = VGroup(Text("=", font_size=35), Text("0", font_size=35)).arrange(RIGHT, buff=0.1)

        # Arrange general form equation
        equation_parts = VGroup(
            a_text, x_squared, plus_b, b_text, x_linear, plus_c, c_text, equals_zero_parts
        ).arrange(RIGHT, buff=0.2)
        
        equation_parts.next_to(current_parabola, UP, buff=0.8) # Position equation
        
        self.play(
            FadeOut(question),
            LaggedStart(
                FadeIn(a_text), FadeIn(x_squared),
                FadeIn(plus_b), FadeIn(b_text), FadeIn(x_linear),
                FadeIn(plus_c), FadeIn(c_text), FadeIn(equals_zero_parts),
                lag_ratio=0.1, run_time=2
            )
        )
        self.play(equation_parts.animate.scale(0.8).next_to(beat1_title, DOWN, buff=0.4), run_time=1.0)
        general_form_label = Text("General Quadratic Equation", font_size=25, color=WHITE).next_to(equation_parts, DOWN, buff=0.2)
        self.play(FadeIn(general_form_label, shift=DOWN), run_time=0.8)

        self.wait(1.5)
        self.play(
            FadeOut(current_parabola),
            FadeOut(root1_dot),
            FadeOut(root2_dot),
            FadeOut(general_form_label),
            FadeOut(plane_label_x),
            FadeOut(plane_label_y),
            FadeOut(plane),
            FadeOut(beat1_title),
            equation_parts.animate.center().to_edge(UP, buff=1.0).scale(1.2), # Reposition equation for continuity
            run_time=1.5
        )
        
        current_general_eq = equation_parts.copy()


        # --- Beat 2: Intuition - Completing the Square Concept (Visual) ---
        beat2_title = Text("2. Intuition: Shifting & Scaling", font_size=45, color=WHITE).to_edge(UP)
        self.play(FadeIn(beat2_title), run_time=0.8)
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            x_length=10, y_length=10,
            axis_config={"color": GREY, "stroke_width": 2},
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.5}
        ).shift(DOWN * 0.5)
        self.play(Create(plane), run_time=1.5)

        # Start with y = x^2
        x_sq_graph = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=LIGHT_BLUE, stroke_width=4)
        y_eq_text = Text("y =", font_size=35, color=WHITE)
        x_sq_eq_val = create_superscripted_text("x", "2", base_font_size=35, color=LIGHT_BLUE)
        y_eq_x_sq_eq = VGroup(y_eq_text, x_sq_eq_val).arrange(RIGHT, buff=0.1).to_corner(UP+LEFT, buff=0.5)

        self.play(Create(x_sq_graph), FadeIn(y_eq_x_sq_eq), run_time=1.0)
        self.wait(1)

        # Demonstrate horizontal shift (x-h)^2
        h_val_tracker = ValueTracker(0)
        shifted_parabola = always_redraw(
            lambda: plane.get_graph(lambda x: (x - h_val_tracker.get_value())**2, x_range=[-4, 4], color=GOLD, stroke_width=4)
        )
        x_minus_h_sq_val = VGroup(
            Text("(x", font_size=35, color=BLUE), Text("-", font_size=35, color=WHITE), Text("h)", font_size=35, color=BLUE),
            create_superscripted_text("", "2", base_font_size=35, color=BLUE).shift(0.05*UP + 0.05*LEFT) # Super 2 for ')'
        ).arrange(RIGHT, buff=0.05)
        x_minus_h_sq_val[-1].next_to(x_minus_h_sq_val[-2], UP+RIGHT, buff=0.05).shift(0.05*UP + 0.05*RIGHT)

        h_eq = VGroup(y_eq_text.copy(), x_minus_h_sq_val).arrange(RIGHT, buff=0.1).align_to(y_eq_x_sq_eq, LEFT).shift(DOWN*0.8) # Position for transformation
        
        self.play(
            ReplacementTransform(x_sq_graph, shifted_parabola),
            Transform(y_eq_x_sq_eq, h_eq),
            h_val_tracker.animate.set_value(1.5),
            run_time=2.0
        )
        self.wait(0.5)

        # Demonstrate vertical shift (x-h)^2 + k
        k_val_tracker = ValueTracker(0)
        # Re-create the updater to include k_val_tracker for clarity
        shifted_parabola.add_updater(
            lambda m: m.become(plane.get_graph(lambda x: (x - h_val_tracker.get_value())**2 + k_val_tracker.get_value(), x_range=[-4, 4], color=GOLD, stroke_width=4))
        )
        k_text_eq_val = VGroup(Text("+", font_size=35, color=WHITE), Text("k", font_size=35, color=BLUE)).arrange(RIGHT, buff=0.05)
        k_eq = VGroup(y_eq_text.copy(), x_minus_h_sq_val.copy(), k_text_eq_val).arrange(RIGHT, buff=0.1).align_to(y_eq_x_sq_eq, LEFT).shift(DOWN*0.8)

        self.play(
            Transform(y_eq_x_sq_eq, k_eq), # Transform the equation Mobject
            k_val_tracker.animate.set_value(-2),
            run_time=2.0
        )
        self.wait(0.5)

        # Demonstrate vertical scale a(x-h)^2 + k
        a_val_tracker = ValueTracker(1)
        shifted_parabola.add_updater( # Add the 'a' parameter to the updater
            lambda m: m.become(plane.get_graph(lambda x: a_val_tracker.get_value() * (x - h_val_tracker.get_value())**2 + k_val_tracker.get_value(), x_range=[-4, 4], color=GOLD, stroke_width=4))
        )
        a_text_eq_val = Text("a", font_size=35, color=BLUE)
        final_eq_parts = VGroup(y_eq_text.copy(), a_text_eq_val, x_minus_h_sq_val.copy(), k_text_eq_val.copy()).arrange(RIGHT, buff=0.1).align_to(y_eq_x_sq_eq, LEFT).shift(DOWN*0.8)
        
        self.play(
            Transform(y_eq_x_sq_eq, final_eq_parts), # Transform the equation Mobject
            a_val_tracker.animate.set_value(0.5), # Change 'a'
            run_time=2.0
        )
        
        shifted_parabola.clear_updaters() # Remove updaters to stop dynamic updates
        self.wait(1)

        summary_text = Text("Any parabola is just a shifted, scaled version of x².", font_size=30, color=WHITE).next_to(plane, DOWN, buff=0.5)
        self.play(FadeIn(summary_text, shift=DOWN), run_time=1.0)
        self.wait(1.5)

        self.play(
            FadeOut(beat2_title),
            FadeOut(plane),
            FadeOut(shifted_parabola),
            FadeOut(y_eq_x_sq_eq),
            FadeOut(summary_text),
            run_time=1.5
        )
        self.play(current_general_eq.animate.to_edge(UP, buff=0.5).scale(0.8), run_time=1.0)


        # --- Beat 3: Formalizing - The Formula (without Tex) ---
        beat3_title = Text("3. The Formula Unveiled", font_size=45, color=WHITE).to_edge(UP)
        self.play(FadeIn(beat3_title), run_time=0.8)
        self.wait(0.5)

        # Reference the general equation
        general_eq_ref = current_general_eq.copy().to_corner(UP + LEFT, buff=0.5).scale(0.7)
        self.play(Transform(current_general_eq, general_eq_ref), run_time=1.0) # Animate current_general_eq to its new position

        # Build the quadratic formula step by step
        x_equals = Text("x =", color=WHITE, font_size=40).next_to(beat3_title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Write(x_equals), run_time=0.8)

        # Numerator: -b
        minus_b = Text("-b", color=BLUE, font_size=40)
        minus_b.next_to(x_equals, RIGHT, buff=0.3)
        self.play(Write(minus_b), run_time=0.5)
        self.wait(0.2)

        # Numerator: +/- sqrt(...)
        plus_minus = Text(" ± ", color=WHITE, font_size=40).next_to(minus_b, RIGHT, buff=0.1)
        sqrt_symbol_char = Text("\u221A", font_size=60, color=GOLD) # Unicode square root
        sqrt_symbol_char.next_to(plus_minus, RIGHT, buff=0.05).align_to(minus_b, DOWN) # Align base of sqrt with base of -b
        
        self.play(Write(plus_minus), FadeIn(sqrt_symbol_char), run_time=0.8)
        self.wait(0.2)

        # Inside sqrt: b^2
        b_squared_val = create_superscripted_text("b", "2", base_font_size=30, color=BLUE)
        b_squared_val.next_to(sqrt_symbol_char, RIGHT, buff=0.1).align_to(minus_b, DOWN)
        self.play(FadeIn(b_squared_val), run_time=0.5)
        self.wait(0.2)

        # Inside sqrt: -4ac
        minus_4 = Text("-4", color=WHITE, font_size=30).next_to(b_squared_val, RIGHT, buff=0.1)
        a_inner = Text("a", color=BLUE, font_size=30).next_to(minus_4, RIGHT, buff=0.05)
        c_inner = Text("c", color=BLUE, font_size=30).next_to(a_inner, RIGHT, buff=0.05)
        discriminant_expr = VGroup(b_squared_val, minus_4, a_inner, c_inner)
        
        self.play(FadeIn(minus_4), FadeIn(a_inner), FadeIn(c_inner), run_time=0.8)
        self.wait(0.2)
        
        # Extend sqrt line over discriminant
        sqrt_line_start = sqrt_symbol_char.get_right() + 0.05 * RIGHT
        sqrt_line_end = discriminant_expr.get_right() + 0.1 * RIGHT
        sqrt_line = Line(sqrt_line_start, sqrt_line_end, color=GOLD, stroke_width=4).align_to(sqrt_symbol_char, UP).shift(UP*0.1) # Manual adjustment
        self.play(Create(sqrt_line), run_time=0.8)
        self.wait(0.5)

        # Create the full numerator
        numerator_elements = VGroup(minus_b, plus_minus, sqrt_symbol_char, discriminant_expr, sqrt_line)
        
        # Denominator: 2a
        two_a_two = Text("2", color=WHITE, font_size=40)
        two_a_a = Text("a", color=BLUE, font_size=40)
        denominator_elements = VGroup(two_a_two, two_a_a).arrange(RIGHT, buff=0.1)
        
        # Fraction line
        fraction_line = Line(LEFT, RIGHT, color=WHITE, stroke_width=4)
        fraction_line.set_width(numerator_elements.width * 1.1)
        
        # Position fraction parts
        fraction_line.next_to(numerator_elements, DOWN, buff=0.2)
        denominator_elements.next_to(fraction_line, DOWN, buff=0.2)
        
        # Combine all parts of the formula and reposition
        full_formula_temp = VGroup(numerator_elements, fraction_line, denominator_elements)
        full_formula_with_x = VGroup(x_equals, full_formula_temp).arrange(RIGHT, buff=0.2)
        
        self.play(
            FadeOut(x_equals), # Fade out original x_equals
            full_formula_with_x.animate.center().to_edge(UP, buff=2), # Position the complete formula
            run_time=2
        )
        self.wait(1)

        formula_label = Text("The Quadratic Formula!", font_size=35, color=GOLD).next_to(full_formula_with_x, DOWN, buff=0.5)
        self.play(FadeIn(formula_label, shift=DOWN), run_time=0.8)
        self.wait(2)
        
        self.play(
            FadeOut(beat3_title),
            FadeOut(formula_label),
            FadeOut(current_general_eq),
            full_formula_with_x.animate.to_edge(UP, buff=0.5).scale(0.7),
            run_time=1.5
        )
        current_formula = full_formula_with_x


        # --- Beat 4: Application Example ---
        beat4_title = Text("4. Applying the Formula", font_size=45, color=WHITE).to_edge(UP)
        self.play(FadeIn(beat4_title), run_time=0.8)
        self.wait(0.5)

        # Example equation: 2x^2 + 5x - 3 = 0
        ex_eq_2 = Text("2", font_size=35)
        ex_eq_x_sq = create_superscripted_text("x", "2", base_font_size=35)
        
        ex_eq_plus_5x = VGroup(Text("+", font_size=35), Text("5", font_size=35), Text("x", font_size=35)).arrange(RIGHT, buff=0.05)
        ex_eq_minus_3 = VGroup(Text("-", font_size=35), Text("3", font_size=35)).arrange(RIGHT, buff=0.05)
        ex_eq_equals_0 = VGroup(Text("=", font_size=35), Text("0", font_size=35)).arrange(RIGHT, buff=0.05)

        example_equation = VGroup(
            ex_eq_2, ex_eq_x_sq, ex_eq_plus_5x, ex_eq_minus_3, ex_eq_equals_0
        ).arrange(RIGHT, buff=0.2).next_to(current_formula, DOWN, buff=0.8)
        
        self.play(FadeIn(example_equation, shift=UP), run_time=1.0)
        self.wait(1)

        # Identify a, b, c
        a_val_text = Text("a = 2", color=BLUE, font_size=35)
        b_val_text = Text("b = 5", color=BLUE, font_size=35)
        c_val_text = Text("c = -3", color=BLUE, font_size=35)
        
        abc_values = VGroup(a_val_text, b_val_text, c_val_text).arrange(RIGHT, buff=0.8).next_to(example_equation, DOWN, buff=0.5)
        self.play(FadeIn(abc_values, shift=UP), run_time=1.0)
        self.wait(1)

        substitution_text = Text("Substitute values into the formula and calculate...", font_size=30, color=LIGHT_BLUE).next_to(abc_values, DOWN, buff=0.5)
        self.play(FadeIn(substitution_text, shift=UP), run_time=1.0)
        self.wait(1)

        # Placeholder for solution (visual only, not actual calculation)
        solution_x1_text = Text("x = 0.5", color=GOLD, font_size=40)
        solution_x2_text = Text("x = -3", color=GOLD, font_size=40)
        solutions = VGroup(solution_x1_text, solution_x2_text).arrange(RIGHT, buff=1.0).next_to(substitution_text, DOWN, buff=0.5)

        self.play(FadeOut(substitution_text, shift=UP), FadeIn(solutions, shift=UP), run_time=1.0)
        self.wait(2)

        self.play(
            FadeOut(beat4_title),
            FadeOut(example_equation),
            FadeOut(abc_values),
            FadeOut(solutions),
            current_formula.animate.center().scale(1.2), # Bring formula to center for recap transition
            run_time=1.5
        )

        # --- Recap Card ---
        recap_title = Text("Recap", font_size=50, color=WHITE).to_edge(UP)
        recap_card_background = Rectangle(width=10, height=6, fill_opacity=0.8, color="#2D2D2D").center()
        
        # Recreate general form for bullet 1
        a_rec = Text("a", font_size=35)
        x_rec_sq = create_superscripted_text("x", "2", base_font_size=35)
        plus_b_rec = Text("+", font_size=35)
        b_rec = Text("b", font_size=35)
        x_linear_rec = Text("x", font_size=35)
        plus_c_rec = Text("+", font_size=35)
        c_rec = Text("c", font_size=35)
        equals_zero_rec = VGroup(Text("=", font_size=35), Text("0", font_size=35)).arrange(RIGHT, buff=0.05)
        
        general_form_recap = VGroup(
            a_rec, x_rec_sq, plus_b_rec, b_rec, x_linear_rec, plus_c_rec, c_rec, equals_zero_rec
        ).arrange(RIGHT, buff=0.1).scale(0.7)
        
        bullet1_base = Text("1. Solves for x in ", font_size=35, color=WHITE)
        bullet1 = VGroup(bullet1_base, general_form_recap).arrange(RIGHT, buff=0.1).to_edge(LEFT, buff=1.0).shift(UP*1.8)

        bullet2 = Text("2. Reveals roots (x-intercepts) of parabolas", font_size=35, color=WHITE).next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet3 = Text("3. Works for all quadratic equations", font_size=35, color=WHITE).next_to(bullet2, DOWN, buff=0.5).align_to(bullet1, LEFT)

        recap_bullets = VGroup(bullet1, bullet2, bullet3).arrange(DOWN, buff=0.5, alignment=LEFT)
        recap_bullets.move_to(recap_card_background.get_center() + UP * 0.5).to_edge(LEFT, buff=0.8)

        self.play(
            FadeOut(current_formula),
            FadeIn(recap_card_background),
            FadeIn(recap_title),
            run_time=1.5
        )
        self.play(LaggedStart(*[Write(bullet) for bullet in recap_bullets], lag_ratio=0.5, run_time=3.0))
        self.wait(3)

        self.play(
            FadeOut(recap_title),
            FadeOut(recap_card_background),
            FadeOut(recap_bullets),
            run_time=1.5
        )
        self.wait(1)