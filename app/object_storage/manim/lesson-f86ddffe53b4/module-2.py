from manim import *

# --- Global Colors ---
BLUE_FG = BLUE_E
GOLD_FG = GOLD_E
GRAY_FG = GRAY_A

# --- Helper Functions for Text-Based Math Expressions ---

def create_text_superscript(base_str, super_str, color=BLUE_FG, scale=0.7, super_scale=0.6):
    """Creates a VGroup for a base string with a superscript."""
    base_m = Text(base_str, color=color).scale(scale)
    super_m = Text(super_str, color=color).scale(super_scale)
    super_m.next_to(base_m, UP + RIGHT, buff=0.05).align_to(base_m, UP)
    return VGroup(base_m, super_m)

def create_text_fraction(numerator_str, denominator_str, color=GOLD_FG, scale=0.7):
    """Creates a VGroup for a fraction (Text numerator, Text denominator, Line)."""
    num = Text(numerator_str, color=color).scale(scale * 0.8)
    den = Text(denominator_str, color=color).scale(scale * 0.8)
    
    line_width = max(num.width, den.width) * 1.2
    line = Line(LEFT, RIGHT).set_width(line_width).set_color(color)
    
    line.move_to(ORIGIN)
    num.next_to(line, UP, buff=0.05 * scale)
    den.next_to(line, DOWN, buff=0.05 * scale)
    
    num.align_to(line, X_AXIS)
    den.align_to(line, X_AXIS)
    
    return VGroup(num, den, line)

def create_math_group(parts, color_default=BLUE_FG, scale=0.7, buff=0.1):
    """
    Arranges a list of strings or Mobjects into a VGroup horizontally.
    Strings will be converted to Text Mobjects.
    """
    mobjects = VGroup()
    for part in parts:
        if isinstance(part, str):
            mobjects.add(Text(part, color=color_default).scale(scale))
        elif isinstance(part, Mobject):
            mobjects.add(part)
        else:
            raise TypeError(f"Unsupported part type in create_math_group: {type(part)}")
    return mobjects.arrange(RIGHT, buff=buff)

def create_parenthesized_squared(inner_mobject, color=BLUE_FG, scale=0.7):
    """Creates a VGroup for (inner_mobject)^2."""
    left_paren = Text("(", color=color).scale(scale)
    right_paren = Text(")", color=color).scale(scale)
    super_2 = Text("2", color=color).scale(scale * 0.6)
    
    group = VGroup(left_paren, inner_mobject, right_paren).arrange(RIGHT, buff=0.05 * scale)
    super_2.next_to(group[-1], UP + RIGHT, buff=0.05).align_to(group[-1], UP) 
    return VGroup(group, super_2)

def create_simple_sqrt_group(inner_mobject, color=BLUE_FG, scale=0.7):
    """Creates a VGroup for sqrt(inner_mobject) using a unicode square root symbol."""
    sqrt_char = Text(u"\u221A", color=color).scale(scale)
    sqrt_char.next_to(inner_mobject, LEFT, buff=0.05)
    return VGroup(sqrt_char, inner_mobject)


class DerivingQuadraticFormula(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # --- Visual Hook ---
        title = Text("Deriving the Quadratic Formula Steps", color=BLUE_FG).scale(1.2).to_edge(UP)
        
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": GRAY, "stroke_width": 1}
        ).add_coordinates().scale(0.6).to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        
        # Initial parabola y = x^2 - 1
        parabola_initial = axes.plot(lambda x: x**2 - 1, color=GOLD_FG)
        coeff_a_text = Text("a = 1", color=GOLD_FG).scale(0.6).to_corner(UP+RIGHT).shift(LEFT*0.5)
        coeff_b_text = Text("b = 0", color=GOLD_FG).scale(0.6).next_to(coeff_a_text, DOWN, buff=0.2).align_to(coeff_a_text, LEFT)
        coeff_c_text = Text("c = -1", color=GOLD_FG).scale(0.6).next_to(coeff_b_text, DOWN, buff=0.2).align_to(coeff_b_text, LEFT)
        
        self.play(
            Create(title),
            Create(axes),
            Create(parabola_initial),
            FadeIn(VGroup(coeff_a_text, coeff_b_text, coeff_c_text)),
            run_time=2
        )
        self.wait(0.5)
        
        # Transform parabola: y = 0.5x^2 + 2x + 1.5
        def func_transformed(x):
            return 0.5 * x**2 + 2 * x + 1.5
        parabola_transformed = axes.plot(func_transformed, color=BLUE_FG)
        
        coeff_a_new = Text("a = 0.5", color=GOLD_FG).scale(0.6).align_to(coeff_a_text, LEFT)
        coeff_b_new = Text("b = 2", color=GOLD_FG).scale(0.6).align_to(coeff_b_text, LEFT)
        coeff_c_new = Text("c = 1.5", color=GOLD_FG).scale(0.6).align_to(coeff_c_text, LEFT)
        
        self.play(
            Transform(parabola_initial, parabola_transformed),
            Transform(coeff_a_text, coeff_a_new),
            Transform(coeff_b_text, coeff_b_new),
            Transform(coeff_c_text, coeff_c_new),
            run_time=2
        )
        self.wait(1)
        self.play(
            FadeOut(parabola_initial), 
            FadeOut(axes), 
            FadeOut(coeff_a_text, coeff_b_text, coeff_c_text)
        )
        
        # --- Beat 1: Start with the General Form ---
        beat1_title = Text("1. Start with the General Form", color=GOLD_FG).scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        
        # ax^2
        ax2_term = create_math_group([Text("a", color=GOLD_FG), create_text_superscript("x", "2", color=BLUE_FG)])
        # +bx
        plus_bx_term = create_math_group(["+", Text("b", color=GOLD_FG), Text("x", color=BLUE_FG)])
        # +c
        plus_c_term = create_math_group(["+", Text("c", color=GOLD_FG)])
        # =0
        equals_0_term = create_math_group(["=", Text("0", color=BLUE_FG)])
        
        quadratic_eq1 = create_math_group([ax2_term, plus_bx_term, plus_c_term, equals_0_term], buff=0.2)
        quadratic_eq1.move_to(ORIGIN)

        self.play(
            FadeIn(beat1_title, shift=UP),
            Create(quadratic_eq1)
        )
        
        solve_for_x_text = Text("Our goal: Find 'x'", color=GRAY_FG).scale(0.7).next_to(quadratic_eq1, DOWN, buff=0.5)
        self.play(FadeIn(solve_for_x_text))
        self.wait(1.5)
        
        self.play(FadeOut(solve_for_x_text))
        self.play(
            quadratic_eq1.animate.shift(UP * 3).scale(0.7),
            FadeOut(beat1_title)
        )
        
        # --- Beat 2: Normalize and Isolate ---
        beat2_title = Text("2. Normalize by 'a' & Isolate 'c/a'", color=GOLD_FG).scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(FadeIn(beat2_title, shift=UP))
        
        divide_by_a_label = Text("Divide by 'a'", color=GRAY_FG).scale(0.6).next_to(quadratic_eq1, DOWN, buff=0.3).align_to(quadratic_eq1, LEFT)
        self.play(FadeIn(divide_by_a_label))
        
        # x^2
        x2_term_new = create_text_superscript("x", "2", color=BLUE_FG)
        # (b/a)x
        b_over_a_frac = create_text_fraction("b", "a", color=GOLD_FG)
        b_over_a_x_term = create_math_group([b_over_a_frac, Text("x", color=BLUE_FG)], buff=0.05)
        # (c/a)
        c_over_a_frac = create_text_fraction("c", "a", color=GOLD_FG)
        
        # New equation VGroup after dividing by 'a'
        quadratic_eq2 = create_math_group([
            x2_term_new,
            Text("+", color=BLUE_FG),
            b_over_a_x_term,
            Text("+", color=BLUE_FG),
            c_over_a_frac,
            Text("=", color=BLUE_FG),
            Text("0", color=BLUE_FG)
        ])
        quadratic_eq2.move_to(quadratic_eq1.get_center())
        
        self.play(
            ReplacementTransform(quadratic_eq1, quadratic_eq2),
            FadeOut(divide_by_a_label)
        )
        self.wait(1)
        
        isolate_c_label = Text("Move constant to RHS", color=GRAY_FG).scale(0.6).next_to(quadratic_eq2, DOWN, buff=0.3).align_to(quadratic_eq2, LEFT)
        self.play(FadeIn(isolate_c_label))
        
        # Equation after isolating 'c/a'
        neg_c_over_a = create_math_group(["-", c_over_a_frac.copy()])
        
        quadratic_eq3 = create_math_group([
            x2_term_new.copy(),
            Text("+", color=BLUE_FG),
            b_over_a_x_term.copy(),
            Text("=", color=BLUE_FG),
            neg_c_over_a
        ])
        quadratic_eq3.move_to(quadratic_eq2.get_center())

        self.play(
            ReplacementTransform(quadratic_eq2, quadratic_eq3),
            FadeOut(isolate_c_label)
        )
        self.wait(1)
        self.play(
            quadratic_eq3.animate.shift(UP * 0.7), # Shift up a bit for next step
            FadeOut(beat2_title)
        )

        # --- Beat 3: Completing the Square ---
        beat3_title = Text("3. Complete the Square", color=GOLD_FG).scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(FadeIn(beat3_title, shift=UP))

        # Visual representation of completing the square
        x_length = 2.0
        
        # x^2 area
        x_sq_geo = Square(side_length=x_length, color=BLUE_FG, fill_opacity=0.5).to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
        x_label_h = Text("x", color=BLUE_FG).scale(0.6).next_to(x_sq_geo, UP, buff=0.1)
        x_label_v = Text("x", color=BLUE_FG).scale(0.6).next_to(x_sq_geo, LEFT, buff=0.1)

        # (b/a)x area: split into two (b/2a)x rectangles
        half_b_over_a_str = create_text_fraction("b", "2a", color=GOLD_FG, scale=0.6)
        half_b_over_a_length = half_b_over_a_str.width * 1.5 # Approximate visual width
        
        rect1 = Rectangle(width=half_b_over_a_length, height=x_length, color=GOLD_FG, fill_opacity=0.5)
        rect2 = Rectangle(width=x_length, height=half_b_over_a_length, color=GOLD_FG, fill_opacity=0.5)
        
        rect1.next_to(x_sq_geo, RIGHT, buff=0)
        rect2.next_to(x_sq_geo, DOWN, buff=0)

        half_b_a_label_h = half_b_over_a_str.copy().next_to(rect1, UP, buff=0.1)
        half_b_a_label_v = half_b_over_a_str.copy().next_to(rect2, LEFT, buff=0.1)
        
        self.play(
            Create(x_sq_geo), FadeIn(x_label_h, x_label_v),
            run_time=1
        )
        self.play(
            Create(rect1), Create(rect2), 
            FadeIn(half_b_a_label_h, half_b_a_label_v),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Missing square to complete it
        missing_square_size = half_b_over_a_length # Use the same length
        missing_square = Square(side_length=missing_square_size, color=BLUE_FG, fill_opacity=0.7)
        missing_square.next_to(rect1, DOWN, buff=0) # Position to complete the square
        
        self.play(Create(missing_square))
        self.wait(1)

        # Algebraic step: Add (b/2a)^2 to both sides
        add_term = create_parenthesized_squared(create_text_fraction("b", "2a", color=GOLD_FG, scale=0.7))
        plus_add_term = create_math_group(["+", add_term.copy()])

        # New equation VGroup
        # Left side: (x + b/2a)^2
        x_plus_b_over_2a = create_math_group([Text("x", color=BLUE_FG), "+", create_text_fraction("b", "2a", color=GOLD_FG)])
        lhs_squared = create_parenthesized_squared(x_plus_b_over_2a)

        # Right side: -(c/a) + (b/2a)^2
        rhs_with_added_term = create_math_group([neg_c_over_a.copy(), plus_add_term.copy()])
        
        quadratic_eq4 = create_math_group([lhs_squared, Text("=", color=BLUE_FG), rhs_with_added_term])
        quadratic_eq4.move_to(quadratic_eq3.get_center())

        self.play(
            ReplacementTransform(quadratic_eq3, quadratic_eq4),
            FadeOut(VGroup(x_sq_geo, rect1, rect2, missing_square, x_label_h, x_label_v, half_b_a_label_h, half_b_a_label_v)),
        )
        self.wait(1)
        self.play(
            quadratic_eq4.animate.shift(UP * 0.7), # Shift up for next step
            FadeOut(beat3_title)
        )

        # --- Beat 4: Solve for x (Square Root) ---
        beat4_title = Text("4. Take Square Root & Isolate 'x'", color=GOLD_FG).scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(FadeIn(beat4_title, shift=UP))

        # Take square root of both sides
        # LHS: sqrt((x + b/2a)^2) -> x + b/2a
        x_plus_b_over_2a_unsq = x_plus_b_over_2a.copy() # Already created
        
        # RHS: +/- sqrt(-(c/a) + (b/2a)^2)
        plus_minus = Text(u"\u00B1", color=BLUE_FG)
        rhs_sqrt_content = rhs_with_added_term.copy() # The VGroup -(c/a) + (b/2a)^2
        rhs_sqrt_group = create_simple_sqrt_group(rhs_sqrt_content)

        quadratic_eq5 = create_math_group([
            x_plus_b_over_2a_unsq,
            Text("=", color=BLUE_FG),
            plus_minus,
            rhs_sqrt_group
        ])
        quadratic_eq5.move_to(quadratic_eq4.get_center())

        self.play(
            ReplacementTransform(quadratic_eq4, quadratic_eq5)
        )
        self.wait(1)
        
        # Isolate x
        neg_b_over_2a = create_math_group(["-", create_text_fraction("b", "2a", color=GOLD_FG)])
        
        # Final equation for beat 4
        quadratic_eq6 = create_math_group([
            Text("x", color=BLUE_FG),
            Text("=", color=BLUE_FG),
            neg_b_over_2a,
            plus_minus.copy(),
            rhs_sqrt_group.copy()
        ])
        quadratic_eq6.move_to(quadratic_eq5.get_center())
        
        self.play(
            ReplacementTransform(quadratic_eq5, quadratic_eq6)
        )
        self.wait(1)
        self.play(
            quadratic_eq6.animate.shift(UP * 0.7), # Shift up for next step
            FadeOut(beat4_title)
        )

        # --- Beat 5: Simplify and Final Formula ---
        beat5_title = Text("5. Simplify Terms", color=GOLD_FG).scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(FadeIn(beat5_title, shift=UP))

        # Simplify RHS under the square root: -(c/a) + (b/2a)^2 = (b^2 - 4ac) / 4a^2
        b2_minus_4ac_num = create_math_group([
            create_text_superscript("b", "2", color=GOLD_FG),
            "-", "4", Text("a", color=GOLD_FG), Text("c", color=GOLD_FG)
        ], buff=0.05)
        four_a2_den = create_math_group([
            "4", create_text_superscript("a", "2", color=BLUE_FG)
        ], buff=0.05)
        
        simplified_fraction_under_sqrt = create_text_fraction(b2_minus_4ac_num, four_a2_den, color=GOLD_FG)
        
        # New RHS sqrt group
        simplified_rhs_sqrt_group = create_simple_sqrt_group(simplified_fraction_under_sqrt)
        
        # First transformation: simplify content under sqrt
        quadratic_eq7 = create_math_group([
            Text("x", color=BLUE_FG),
            Text("=", color=BLUE_FG),
            neg_b_over_2a.copy(),
            plus_minus.copy(),
            simplified_rhs_sqrt_group
        ])
        quadratic_eq7.move_to(quadratic_eq6.get_center())
        
        self.play(
            ReplacementTransform(quadratic_eq6, quadratic_eq7)
        )
        self.wait(1)
        
        # Simplify sqrt(4a^2) = 2a in the denominator
        sqrt_of_4a2_simplified = create_math_group(["2", Text("a", color=BLUE_FG)])

        # Construct the final quadratic formula
        final_numerator_parts = create_math_group([
            Text("-b", color=GOLD_FG),
            Text(u"\u00B1", color=BLUE_FG),
            create_simple_sqrt_group(b2_minus_4ac_num.copy()) # Just the numerator part
        ], buff=0.1)
        
        final_quadratic_formula_rhs = VGroup(
            final_numerator_parts,
            Line(LEFT, RIGHT).set_width(final_numerator_parts.width * 1.2).set_color(BLUE_FG),
            sqrt_of_4a2_simplified.copy()
        ).arrange(DOWN, buff=0.1)
        
        final_quadratic_formula = create_math_group([
            Text("x", color=BLUE_FG),
            Text("=", color=BLUE_FG),
            final_quadratic_formula_rhs
        ], buff=0.1)
        final_quadratic_formula.move_to(ORIGIN).shift(DOWN*0.5)

        self.play(
            ReplacementTransform(quadratic_eq7, final_quadratic_formula)
        )
        self.play(final_quadratic_formula.animate.scale(1.2))
        self.wait(2)
        
        # --- Recap Card ---
        self.play(FadeOut(final_quadratic_formula), FadeOut(title), FadeOut(beat5_title))
        
        recap_title = Text("Recap: Steps to Derive", color=BLUE_FG).scale(1.2).to_edge(UP)
        
        # Recap steps as text
        step1 = Text("1. Start with ax² + bx + c = 0", color=GOLD_FG).scale(0.7).next_to(recap_title, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        step2 = Text("2. Normalize by 'a' & Isolate 'c/a'", color=GOLD_FG).scale(0.7).next_to(step1, DOWN, buff=0.3).align_to(step1, LEFT)
        step3 = Text("3. Complete the square (add (b/2a)²) ", color=GOLD_FG).scale(0.7).next_to(step2, DOWN, buff=0.3).align_to(step2, LEFT)
        step4 = Text("4. Take square root & Isolate 'x'", color=GOLD_FG).scale(0.7).next_to(step3, DOWN, buff=0.3).align_to(step3, LEFT)
        step5 = Text("5. Simplify terms (common denominator)", color=GOLD_FG).scale(0.7).next_to(step4, DOWN, buff=0.3).align_to(step4, LEFT)
        
        self.play(Create(recap_title))
        self.play(LaggedStart(
            FadeIn(step1, shift=UP),
            FadeIn(step2, shift=UP),
            FadeIn(step3, shift=UP),
            FadeIn(step4, shift=UP),
            FadeIn(step5, shift=UP),
            lag_ratio=0.3
        ))
        
        self.wait(3)