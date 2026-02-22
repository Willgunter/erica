from manim import *

# Set default configuration
config.background_color = BLACK
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30 # For smoother animations if needed, default is 30.

# Helper function to create superscript for Text Mobjects
def create_superscript(base_text_str, super_text_str, base_color=WHITE, super_color=WHITE, scale=1.0):
    base = Text(base_text_str, color=base_color).scale(scale)
    super_script = Text(super_text_str, font_size=base.font_size * 0.7, color=super_color)
    super_script.move_to(base.get_corner(UR) + 0.1 * RIGHT + 0.1 * UP) # Adjust position
    return VGroup(base, super_script)

# Helper for creating (b/a)x Text Mobject
def create_b_over_a_x_text(coeff_color=GOLD_C, x_color=BLUE_C, scale=1.0):
    return VGroup(
        Text("(", color=coeff_color), Text("b", color=coeff_color), Text("/", color=coeff_color), Text("a", color=coeff_color), Text(")", color=coeff_color), Text("x", color=x_color)
    ).arrange(RIGHT, buff=0.1).scale(scale)

# Helper for creating b/2a Text Mobject
def create_b_over_2a_text(color=GOLD_C, scale=1.0):
    return VGroup(
        Text("b", color=color), Text("/", color=color), Text("2", color=color), Text("a", color=color)
    ).arrange(RIGHT, buff=0.1).scale(scale)

# Helper for creating (b/2a)x Text Mobject
def create_b_over_2a_x_text(coeff_color=GOLD_C, x_color=BLUE_C, scale=1.0):
    return VGroup(
        Text("(", color=coeff_color), create_b_over_2a_text(color=coeff_color, scale=1.0), Text(")", color=coeff_color), Text("x", color=x_color)
    ).arrange(RIGHT, buff=0.05).scale(scale)

# Helper for creating (b/2a)^2 Text Mobject
def create_b_2a_squared_text(color=GOLD_C, scale=1.0):
    return VGroup(
        Text("(", color=color), create_b_over_2a_text(color=color, scale=1.0), Text(")", color=color), create_superscript("", "2", base_color=color, super_color=color, scale=0.8).shift(RIGHT * 0.1)
    ).arrange(RIGHT, buff=0.05).scale(scale)

# Helper for creating b^2 - 4ac Text Mobject
def create_b_squared_minus_4ac_text(coeff_color=GOLD_C, eq_color=WHITE, scale=1.0):
    return VGroup(
        create_superscript("b", "2", base_color=coeff_color, super_color=coeff_color, scale=scale*0.9),
        Text(" - ", color=eq_color).scale(scale),
        Text("4", color=coeff_color).scale(scale),
        Text("a", color=coeff_color).scale(scale),
        Text("c", color=coeff_color).scale(scale)
    ).arrange(RIGHT, buff=0.05)


class DeriveQuadraticFormula(Scene):
    def construct(self):
        # --- Colors ---
        X_COLOR = BLUE_C
        COEFF_COLOR = GOLD_C
        EQUATION_COLOR = WHITE
        HIGHLIGHT_COLOR = RED_E

        # --- Visual Hook: Parabola and its roots ---
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 10, 2],
            x_length=10,
            y_length=7,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False
        ).to_edge(LEFT, buff=0.5)
        axes_labels = axes.get_axis_labels(x_label=Text("x"), y_label=Text("y"))

        # Example parabola: y = x^2 - x - 2 = (x-2)(x+1)
        def parabola_func(x):
            return x**2 - x - 2

        graph = axes.plot(parabola_func, color=X_COLOR, x_range=[-3, 4])
        dot1 = Dot(axes.c2p(-1, 0), color=HIGHLIGHT_COLOR)
        dot2 = Dot(axes.c2p(2, 0), color=HIGHLIGHT_COLOR)
        root_labels = VGroup(
            Text("x1", color=HIGHLIGHT_COLOR).next_to(dot1, DOWN),
            Text("x2", color=HIGHLIGHT_COLOR).next_to(dot2, DOWN)
        )

        hook_title = Text("Finding the Roots of a Quadratic", color=WHITE).to_edge(UP)

        self.play(
            Create(axes), Create(axes_labels),
            Write(hook_title)
        )
        self.play(
            Create(graph),
            run_time=1.5
        )
        self.play(
            FadeIn(dot1, scale=0.5),
            FadeIn(dot2, scale=0.5),
            Write(root_labels),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(axes, axes_labels, graph, dot1, dot2, root_labels),
            FadeOut(hook_title)
        )
        self.wait(0.5)

        # --- Beat 1: The Equation and Initial Setup (ax^2 + bx + c = 0) ---
        title = Text("Deriving the Quadratic Formula", color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        a_x_squared_text = VGroup(Text("a", color=COEFF_COLOR), create_superscript("x", "2", base_color=X_COLOR, super_color=X_COLOR, scale=1.0)).arrange(RIGHT, buff=0.1)
        plus1 = Text(" + ", color=EQUATION_COLOR)
        b_x_text = VGroup(Text("b", color=COEFF_COLOR), Text("x", color=X_COLOR)).arrange(RIGHT, buff=0.1)
        plus2 = Text(" + ", color=EQUATION_COLOR)
        c_text = Text("c", color=COEFF_COLOR)
        equals_zero_full = Text(" = 0", color=EQUATION_COLOR)

        full_initial_equation = VGroup(a_x_squared_text, plus1, b_x_text, plus2, c_text, equals_zero_full).arrange(RIGHT, buff=0.2).center().shift(UP*2.5)
        self.play(FadeIn(full_initial_equation, shift=UP))
        self.wait(1)

        # Step 1: Divide by 'a'
        div_a_label = Text("Divide by 'a'", color=WHITE).to_edge(DR)
        self.play(Write(div_a_label))
        
        # Create the divided by 'a' version
        # x^2 + (b/a)x + (c/a) = 0
        x_squared_text = create_superscript("x", "2", base_color=X_COLOR, super_color=X_COLOR, scale=1.0)
        b_over_a_x_text = create_b_over_a_x_text(coeff_color=COEFF_COLOR, x_color=X_COLOR, scale=1.0)
        c_over_a_text_group = VGroup(Text("c", color=COEFF_COLOR), Text("/", color=EQUATION_COLOR), Text("a", color=COEFF_COLOR)).arrange(RIGHT, buff=0.1)
        equals_zero_div_a = Text(" = 0", color=EQUATION_COLOR)

        divided_eq = VGroup(x_squared_text, plus1.copy(), b_over_a_x_text, plus2.copy(), c_over_a_text_group, equals_zero_div_a).arrange(RIGHT, buff=0.2).move_to(full_initial_equation).shift(DOWN*0.8)

        self.play(
            ReplacementTransform(full_initial_equation, divided_eq),
            FadeOut(div_a_label)
        )
        self.wait(1)

        # Step 2: Move c/a to the right side
        # x^2 + (b/a)x = -c/a
        # Target for -c/a
        minus_c_over_a_target = VGroup(Text(" = ", color=EQUATION_COLOR), Text("-", color=EQUATION_COLOR), c_over_a_text_group.copy()).arrange(RIGHT, buff=0.1)
        minus_c_over_a_target.next_to(b_over_a_x_text, RIGHT, buff=0.2)

        lhs_current = VGroup(x_squared_text, divided_eq[1], b_over_a_x_text)
        
        move_c_arrow = Arrow(c_over_a_text_group.get_center(), minus_c_over_a_target[2].get_center(), color=HIGHLIGHT_COLOR)
        self.play(Create(move_c_arrow))
        self.play(
            ReplacementTransform(VGroup(divided_eq[3], c_over_a_text_group, equals_zero_div_a), minus_c_over_a_target),
            FadeOut(move_c_arrow)
        )
        self.wait(1)

        current_equation_line = VGroup(lhs_current, minus_c_over_a_target).arrange(RIGHT, buff=0.2).center().to_edge(UP, buff=1.5)
        self.play(current_equation_line.animate.center().to_edge(UP, buff=1.5))
        self.wait(0.5)

        # --- Beat 2: Completing the Square Geometrically ---
        # Geometric representation of x^2 + (b/a)x
        x_square = Square(side_length=3, color=X_COLOR, fill_opacity=0.5).to_edge(LEFT, buff=0.5).shift(DOWN*1)
        x_label_bottom = Text("x", color=X_COLOR).next_to(x_square.get_bottom(), DOWN, buff=0.1)
        x_label_left = Text("x", color=X_COLOR).next_to(x_square.get_left(), LEFT, buff=0.1)
        x_square_area_label = create_superscript("x", "2", base_color=X_COLOR, super_color=X_COLOR)
        x_square_area_label.move_to(x_square.get_center())

        self.play(FadeIn(x_square), FadeIn(x_label_bottom), FadeIn(x_label_left), FadeIn(x_square_area_label))
        self.wait(0.5)

        # Represent (b/a)x
        b_over_a_visual_width = 1.5 # Arbitrary visual value for (b/a)
        rect_bx = Rectangle(width=b_over_a_visual_width, height=x_square.side_length, color=COEFF_COLOR, fill_opacity=0.5)
        rect_bx.next_to(x_square, RIGHT, buff=0)
        bx_label_top = Text("b/a", color=COEFF_COLOR).next_to(rect_bx.get_top(), UP, buff=0.1)
        bx_area_label = create_b_over_a_x_text(coeff_color=COEFF_COLOR, x_color=X_COLOR, scale=0.8)
        bx_area_label.move_to(rect_bx.get_center())

        self.play(FadeIn(rect_bx), FadeIn(bx_label_top), FadeIn(bx_area_label))
        self.wait(1)

        # Split the (b/a)x rectangle
        half_b_over_a_visual_width = b_over_a_visual_width / 2
        rect_half_bx_1 = Rectangle(width=half_b_over_a_visual_width, height=x_square.side_length, color=COEFF_COLOR, fill_opacity=0.5)
        rect_half_bx_2 = Rectangle(width=x_square.side_length, height=half_b_over_a_visual_width, color=COEFF_COLOR, fill_opacity=0.5) # Rotated

        rect_half_bx_1.next_to(x_square, RIGHT, buff=0)
        rect_half_bx_2.next_to(x_square, DOWN, buff=0)

        bx_area_label_copy_1 = create_b_over_2a_x_text(coeff_color=COEFF_COLOR, x_color=X_COLOR, scale=0.6).move_to(rect_half_bx_1.get_center())
        bx_area_label_copy_2 = create_b_over_2a_x_text(coeff_color=COEFF_COLOR, x_color=X_COLOR, scale=0.6).move_to(rect_half_bx_2.get_center())

        self.play(
            ReplacementTransform(rect_bx, VGroup(rect_half_bx_1, rect_half_bx_2)),
            ReplacementTransform(bx_area_label, VGroup(bx_area_label_copy_1, bx_area_label_copy_2)),
            FadeOut(bx_label_top)
        )
        self.wait(0.5)

        # Add new labels for the split sides
        b_2a_label_top = create_b_over_2a_text(color=COEFF_COLOR).next_to(rect_half_bx_1.get_top(), UP, buff=0.1)
        b_2a_label_right = create_b_over_2a_text(color=COEFF_COLOR).next_to(rect_half_bx_2.get_right(), RIGHT, buff=0.1).rotate(PI/2) # Rotate for vertical
        self.play(FadeIn(b_2a_label_top), FadeIn(b_2a_label_right))
        self.wait(0.5)

        # Identify the missing square
        missing_square = Square(side_length=half_b_over_a_visual_width, color=HIGHLIGHT_COLOR, fill_opacity=0.7)
        missing_square.next_to(rect_half_bx_1, DOWN, buff=0).align_to(rect_half_bx_2, RIGHT)

        missing_square_area_label = create_b_2a_squared_text(color=HIGHLIGHT_COLOR, scale=0.6)
        missing_square_area_label.move_to(missing_square.get_center())

        self.play(Create(missing_square), FadeIn(missing_square_area_label))
        self.wait(1)

        # Add the missing square, completing the large square
        self.play(
            missing_square.animate.set_color(COEFF_COLOR).set_opacity(0.5),
            missing_square_area_label.animate.set_color(COEFF_COLOR)
        )
        self.wait(0.5)

        # Update the equation: add (b/2a)^2 to both sides
        b_2a_sq_term = create_b_2a_squared_text(color=COEFF_COLOR, scale=0.8)

        plus_b_2a_sq_lhs = VGroup(Text(" + ", color=EQUATION_COLOR), b_2a_sq_term.copy()).arrange(RIGHT, buff=0.05)
        plus_b_2a_sq_lhs.next_to(b_over_a_x_text, RIGHT, buff=0.1)
        
        plus_b_2a_sq_rhs = VGroup(Text(" + ", color=EQUATION_COLOR), b_2a_sq_term.copy()).arrange(RIGHT, buff=0.05)
        plus_b_2a_sq_rhs.next_to(minus_c_over_a_target, RIGHT, buff=0.1)

        self.play(FadeIn(plus_b_2a_sq_lhs), FadeIn(plus_b_2a_sq_rhs))
        self.wait(1)

        # Form the squared term on the left (x + b/2a)^2
        new_lhs_group = VGroup(x_squared_text, divided_eq[1], b_over_a_x_text, plus_b_2a_sq_lhs)
        target_lhs_squared = VGroup(
            Text("(", color=EQUATION_COLOR),
            Text("x", color=X_COLOR),
            Text(" + ", color=EQUATION_COLOR),
            create_b_over_2a_text(color=COEFF_COLOR, scale=1.0),
            Text(")", color=EQUATION_COLOR),
            create_superscript("", "2", base_color=EQUATION_COLOR, super_color=EQUATION_COLOR, scale=0.8).shift(RIGHT*0.05)
        ).arrange(RIGHT, buff=0.05).scale(0.9)
        target_lhs_squared.move_to(new_lhs_group.get_center())

        self.play(
            Transform(new_lhs_group, target_lhs_squared),
            FadeOut(x_square_area_label, bx_area_label_copy_1, bx_area_label_copy_2, missing_square_area_label, b_2a_label_top, b_2a_label_right),
            FadeOut(x_label_bottom, x_label_left),
            FadeOut(x_square, rect_half_bx_1, rect_half_bx_2, missing_square)
        )
        self.wait(1)

        # Update the entire equation
        current_equation_lhs_v = target_lhs_squared
        current_equation_rhs_v = VGroup(minus_c_over_a_target, plus_b_2a_sq_rhs).arrange(RIGHT, buff=0.1)
        
        current_equation_line = VGroup(current_equation_lhs_v, current_equation_rhs_v).arrange(RIGHT, buff=0.2).center().to_edge(UP, buff=1.5)
        self.play(current_equation_line.animate.center().to_edge(UP, buff=1.5))
        self.wait(1)

        # Simplify the RHS: (b^2 / 4a^2) - (c/a)
        b_sq_4a_sq = VGroup(
            create_superscript("b", "2", base_color=COEFF_COLOR, super_color=COEFF_COLOR, scale=0.9),
            Text("/", color=EQUATION_COLOR),
            Text("4", color=COEFF_COLOR),
            create_superscript("a", "2", base_color=COEFF_COLOR, super_color=COEFF_COLOR, scale=0.9)
        ).arrange(RIGHT, buff=0.05).scale(0.9)

        c_over_a_times_4a_over_4a = VGroup(
            Text("4", color=COEFF_COLOR), Text("a", color=COEFF_COLOR), Text("c", color=COEFF_COLOR),
            Text("/", color=EQUATION_COLOR),
            Text("4", color=COEFF_COLOR), create_superscript("a", "2", base_color=COEFF_COLOR, super_color=COEFF_COLOR, scale=0.9)
        ).arrange(RIGHT, buff=0.05).scale(0.9)

        # These terms are temporary for the transformation
        temp_minus_sign = minus_c_over_a_target[1]
        temp_c_over_a = minus_c_over_a_target[2]
        temp_plus_sign = plus_b_2a_sq_rhs[0]
        temp_b_2a_sq = plus_b_2a_sq_rhs[1]

        self.play(
            FadeOut(temp_c_over_a), # Fade out c/a
            FadeOut(temp_b_2a_sq), # Fade out (b/2a)^2
            ReplacementTransform(c_over_a_text_group.copy().move_to(temp_c_over_a.get_center()), c_over_a_times_4a_over_4a), # Animate transformation to 4ac/4a^2
            ReplacementTransform(b_2a_sq_term.copy().move_to(temp_b_2a_sq.get_center()), b_sq_4a_sq) # Animate transformation to b^2/4a^2
        )
        self.wait(1)

        # Combine them over a common denominator
        numerator_combined = create_b_squared_minus_4ac_text(coeff_color=COEFF_COLOR, eq_color=EQUATION_COLOR, scale=1.0)
        denominator_combined = VGroup(Text("4", color=COEFF_COLOR), create_superscript("a", "2", base_color=COEFF_COLOR, super_color=COEFF_COLOR, scale=1.0)).arrange(RIGHT, buff=0.05)

        frac_line_rhs = Line(ORIGIN, RIGHT, color=EQUATION_COLOR)
        
        frac_line_rhs.set_width(max(numerator_combined.width, denominator_combined.width) + 0.5)
        numerator_combined.move_to(frac_line_rhs.get_center() + UP * 0.3)
        denominator_combined.move_to(frac_line_rhs.get_center() + DOWN * 0.3)
        
        final_rhs_fraction_v = VGroup(numerator_combined, frac_line_rhs, denominator_combined)
        
        # Position it where the combined terms were
        final_rhs_fraction_v.move_to(VGroup(temp_minus_sign, c_over_a_times_4a_over_4a, temp_plus_sign, b_sq_4a_sq).get_center())

        self.play(
            FadeOut(temp_minus_sign),
            FadeOut(temp_plus_sign),
            ReplacementTransform(VGroup(c_over_a_times_4a_over_4a, b_sq_4a_sq), final_rhs_fraction_v)
        )
        self.wait(1)

        # Update the full equation on screen
        current_equation_rhs_v = VGroup(minus_c_over_a_target[0], final_rhs_fraction_v).arrange(RIGHT, buff=0.1)
        current_equation_line = VGroup(current_equation_lhs_v, current_equation_rhs_v).arrange(RIGHT, buff=0.2).center().to_edge(UP, buff=1.5)
        self.play(current_equation_line.animate.center().to_edge(UP, buff=1.5))
        self.wait(1)

        # --- Beat 3: Square Root Both Sides ---
        # (x + b/2a)^2 = (b^2 - 4ac) / 4a^2
        # Take square root
        plus_minus_lhs = Text("±", color=EQUATION_COLOR).scale(1.2).next_to(target_lhs_squared, LEFT, buff=0.1)
        plus_minus_rhs = Text("±", color=EQUATION_COLOR).scale(1.2).next_to(final_rhs_fraction_v[0], LEFT, buff=0.1)
        sqrt_symbol_rhs = Text("√", color=EQUATION_COLOR).scale(1.2).next_to(plus_minus_rhs, RIGHT, buff=0.1) # sqrt before the numerator
        
        # Line to denote the scope of the square root over the numerator
        line_over_rhs_num = Line(final_rhs_fraction_v[0][0].get_left() - 0.2 * LEFT, final_rhs_fraction_v[0][-1].get_right() + 0.2 * RIGHT, color=EQUATION_COLOR)
        
        self.play(
            FadeIn(plus_minus_lhs),
            FadeIn(plus_minus_rhs),
            Create(sqrt_symbol_rhs),
            Create(line_over_rhs_num)
        )
        self.wait(0.5)

        # Remove the square from LHS
        lhs_without_square = VGroup(
            Text("x", color=X_COLOR),
            Text(" + ", color=EQUATION_COLOR),
            create_b_over_2a_text(color=COEFF_COLOR, scale=1.0)
        ).arrange(RIGHT, buff=0.05).scale(0.9)
        lhs_without_square.move_to(current_equation_lhs_v.get_center())

        self.play(
            FadeOut(current_equation_lhs_v[-1]), # Remove the '2' from (x + b/2a)^2
            FadeOut(current_equation_lhs_v[0]), # Remove '('
            FadeOut(current_equation_lhs_v[4]), # Remove ')'
            Transform(VGroup(current_equation_lhs_v[1], current_equation_lhs_v[2], current_equation_lhs_v[3]), lhs_without_square),
            FadeOut(plus_minus_lhs) # Fade out root sign as it cancels the square
        )
        self.wait(1)

        # Simplify RHS: sqrt(numerator) / sqrt(4a^2)
        sqrt_denom_value = VGroup(Text("2", color=COEFF_COLOR), Text("a", color=COEFF_COLOR)).arrange(RIGHT, buff=0.1)
        sqrt_denom_value.move_to(final_rhs_fraction_v[2].get_center())

        self.play(
            ReplacementTransform(final_rhs_fraction_v[2], sqrt_denom_value),
            FadeOut(line_over_rhs_num) # No longer needed as part of sqrt is over num only
        )
        self.wait(1)

        # Update full equation on screen
        current_equation_lhs_v = lhs_without_square
        current_equation_rhs_v = VGroup(plus_minus_rhs, sqrt_symbol_rhs, VGroup(final_rhs_fraction_v[0], final_rhs_fraction_v[1], sqrt_denom_value)).arrange(RIGHT, buff=0.1)
        
        # Manually adjust fraction line
        current_equation_rhs_v[2][1].set_width(max(current_equation_rhs_v[2][0].width, current_equation_rhs_v[2][2].width)+0.5)
        current_equation_rhs_v[2][0].next_to(current_equation_rhs_v[2][1], UP, buff=0.3, aligned_edge=X_AXIS)
        current_equation_rhs_v[2][2].next_to(current_equation_rhs_v[2][1], DOWN, buff=0.3, aligned_edge=X_AXIS)
        
        # Reposition the whole RHS
        current_equation_rhs_v.next_to(current_equation_lhs_v, RIGHT, buff=0.5)
        current_equation_line = VGroup(current_equation_lhs_v, Text(" = ", color=EQUATION_COLOR), current_equation_rhs_v).arrange(RIGHT, buff=0.2).center().to_edge(UP, buff=1.5)
        self.play(current_equation_line.animate.center().to_edge(UP, buff=1.5))
        self.wait(1)

        # --- Beat 4: Isolate x and Final Formula ---
        # x + b/2a = +/- sqrt(b^2-4ac) / 2a
        # Move b/2a to the RHS
        b_2a_term_moved = VGroup(
            Text("-", color=EQUATION_COLOR),
            create_b_over_2a_text(color=COEFF_COLOR, scale=1.0)
        ).arrange(RIGHT, buff=0.05).scale(0.9)

        lhs_plus_b_2a = VGroup(lhs_without_square[1], lhs_without_square[2]) # + b/2a
        
        move_b2a_arrow = Arrow(lhs_plus_b_2a.get_center(), current_equation_rhs_v.get_center(), color=HIGHLIGHT_COLOR)
        self.play(Create(move_b2a_arrow))

        self.play(
            ReplacementTransform(lhs_plus_b_2a, b_2a_term_moved),
            FadeOut(move_b2a_arrow)
        )
        self.wait(0.5)

        # Only 'x' remains on LHS
        final_lhs_x = VGroup(lhs_without_square[0])
        x_equals_sign = Text(" = ", color=EQUATION_COLOR)
        x_equals_sign.next_to(final_lhs_x, RIGHT, buff=0.1)
        self.play(
            final_lhs_x.animate.move_to(lhs_without_square.get_center() + LEFT*0.5),
            Create(x_equals_sign)
        )
        self.wait(0.5)

        # Combine all parts into the final formula
        final_formula_num = VGroup(
            Text("-", color=COEFF_COLOR),
            Text("b", color=COEFF_COLOR),
            Text(" ", color=EQUATION_COLOR), # Space for +-
            Text("±", color=EQUATION_COLOR),
            Text(" ", color=EQUATION_COLOR), # Space for sqrt
            Text("√", color=EQUATION_COLOR),
            create_b_squared_minus_4ac_text(coeff_color=COEFF_COLOR, eq_color=EQUATION_COLOR, scale=1.0)
        ).arrange(RIGHT, buff=0.05)

        final_formula_denom = VGroup(
            Text("2", color=COEFF_COLOR),
            Text("a", color=COEFF_COLOR)
        ).arrange(RIGHT, buff=0.05)
        
        formula_frac_line = Line(LEFT, RIGHT, color=EQUATION_COLOR)
        formula_frac_line.set_width(final_formula_num.width + 0.5)
        
        final_formula_num.move_to(formula_frac_line.get_center() + UP * 0.3)
        final_formula_denom.move_to(formula_frac_line.get_center() + DOWN * 0.3)
        
        final_formula_rhs = VGroup(final_formula_num, formula_frac_line, final_formula_denom).center()

        final_formula = VGroup(final_lhs_x, x_equals_sign, final_formula_rhs).arrange(RIGHT, buff=0.1).center().shift(DOWN*2)

        # Animate assembly of the final formula from current terms
        self.play(
            # LHS: x =
            Transform(final_lhs_x, final_formula[0]),
            Transform(x_equals_sign, final_formula[1]),

            # Numerator: -b
            Transform(b_2a_term_moved[0], final_formula_num[0]), # - sign
            Transform(b_2a_term_moved[1][0], final_formula_num[1]), # b

            # Numerator: ±
            Transform(plus_minus_rhs, final_formula_num[3]),

            # Numerator: √(b^2-4ac)
            Transform(sqrt_symbol_rhs, final_formula_num[5]),
            Transform(current_equation_rhs_v[2][0], final_formula_num[6]), # b^2-4ac numerator

            # Denominator: 2a
            Transform(VGroup(b_2a_term_moved[1][2], b_2a_term_moved[1][3]), final_formula_denom), # 2a part of b/2a

            # Fraction line
            Transform(current_equation_rhs_v[2][1], formula_frac_line) # old frac line to new frac line
        )
        self.play(final_formula.animate.scale(1.1).center()) # Scale slightly for final prominence
        self.wait(3)

        # --- Recap Card ---
        self.play(FadeOut(final_formula, title))
        self.wait(1)

        recap_title = Text("Recap: Quadratic Formula Derivation", color=WHITE).to_edge(UP)
        
        recap_steps = VGroup(
            Text("1. Start with ax^2 + bx + c = 0", color=EQUATION_COLOR).scale(0.8),
            Text("2. Divide by 'a', move 'c/a' to RHS", color=COEFF_COLOR).scale(0.8),
            Text("3. Complete the square on LHS: (x + b/2a)^2", color=X_COLOR).scale(0.8),
            Text("4. Simplify RHS and take square roots", color=HIGHLIGHT_COLOR).scale(0.8),
            Text("5. Isolate 'x' to get the formula!", color=EQUATION_COLOR).scale(0.8)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).center().shift(UP*1)

        final_formula_recap_v = VGroup(
            VGroup(
                Text("x", color=X_COLOR), Text(" = ", color=EQUATION_COLOR)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                VGroup(
                    Text("-", color=COEFF_COLOR), Text("b", color=COEFF_COLOR),
                    Text(" ", color=EQUATION_COLOR), Text("±", color=EQUATION_COLOR), Text(" ", color=EQUATION_COLOR),
                    Text("√", color=EQUATION_COLOR),
                    create_b_squared_minus_4ac_text(coeff_color=COEFF_COLOR, eq_color=EQUATION_COLOR, scale=0.9)
                ).arrange(RIGHT, buff=0.05),
                Line(LEFT, RIGHT, color=EQUATION_COLOR).set_width(4), # Placeholder width
                VGroup(
                    Text("2", color=COEFF_COLOR), Text("a", color=COEFF_COLOR)
                ).arrange(RIGHT, buff=0.05)
            ).arrange(DOWN, buff=0.3)
        ).arrange(RIGHT, buff=0.5).center().shift(DOWN*1.5).scale(1.2)

        # Adjust line width and position elements precisely for recap
        final_formula_recap_v[1][1].set_width(final_formula_recap_v[1][0].width + 0.5)
        final_formula_recap_v[1][0].move_to(final_formula_recap_v[1][1].get_center() + UP * 0.3)
        final_formula_recap_v[1][2].move_to(final_formula_recap_v[1][1].get_center() + DOWN * 0.3)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[Write(step) for step in recap_steps], lag_ratio=0.3))
        self.play(FadeIn(final_formula_recap_v))
        self.wait(3)

        self.play(FadeOut(recap_title, recap_steps, final_formula_recap_v))
        self.wait(1)