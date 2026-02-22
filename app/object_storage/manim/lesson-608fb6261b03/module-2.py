from manim import *

# Custom colors for 3B1B style
BLUE_ACCENT = "#50e3c2"  # A bright turquoise-blue
GOLD_ACCENT = "#ffc107"  # A vibrant gold/amber
MAIN_TEXT_COLOR = WHITE

config.background_color = BLACK

# --- Helper Functions for "no Tex" mathematical expressions ---

def create_power_mobject(base_mobj, power_str, color=MAIN_TEXT_COLOR, base_scale=0.7, power_scale=0.4):
    """Creates a VGroup representing a base with a superscript power."""
    if isinstance(base_mobj, str):
        base = Text(base_mobj, color=color).scale(base_scale)
    else:
        base = base_mobj.copy().scale(base_scale / base_mobj.height * Text("x").scale(base_scale).height if base_mobj.height > 0 else base_scale) # Scale to match text height
    
    power = Text(power_str, color=color).scale(power_scale)
    power.next_to(base, UP_RIGHT, buff=0.05).shift(0.05 * RIGHT)
    return VGroup(base, power)

def create_fraction_mobject(numerator_mobj, denominator_mobj, color=MAIN_TEXT_COLOR, scale_factor=0.7):
    """Creates a VGroup representing a fraction, accepting mobjects or strings."""
    if isinstance(numerator_mobj, str):
        numerator = Text(numerator_mobj, color=color).scale(scale_factor)
    else:
        numerator = numerator_mobj.copy().scale_to_fit_height(Text("x").scale(scale_factor).height * 0.9)
    
    if isinstance(denominator_mobj, str):
        denominator = Text(denominator_mobj, color=color).scale(scale_factor)
    else:
        denominator = denominator_mobj.copy().scale_to_fit_height(Text("x").scale(scale_factor).height * 0.9)
        
    line_width = max(numerator.width, denominator.width) * 1.1
    line = Line(LEFT, RIGHT, color=color, stroke_width=2).set_width(line_width)
    
    frac_group = VGroup(numerator, line, denominator)
    line.move_to(ORIGIN)
    numerator.next_to(line, UP, buff=0.1)
    denominator.next_to(line, DOWN, buff=0.1)
    
    frac_group.move_to(VGroup(numerator, denominator).get_center())
    return frac_group

def create_sqrt_mobject(content_mobject, color=MAIN_TEXT_COLOR, stroke_width=3):
    """Creates a VGroup representing a square root symbol around another mobject."""
    content = content_mobject.copy()
    
    v_line = Line(DOWN * 0.3, UP * 0.3, color=color, stroke_width=stroke_width)
    slant_line = Line(LEFT * 0.1, RIGHT * 0.3 + UP * 0.4, color=color, stroke_width=stroke_width)
    top_line = Line(RIGHT * 0.3 + UP * 0.4, RIGHT * 0.7 + UP * 0.4, color=color, stroke_width=stroke_width)
    root_symbol = VGroup(v_line, slant_line, top_line)
    
    root_symbol.stretch_to_fit_height(content.height * 1.4)
    root_symbol.next_to(content, LEFT, buff=0.05)
    root_symbol.align_to(content, UP).shift(0.05*DOWN)
    
    return VGroup(root_symbol, content)

def create_plus_minus_mobject(color=MAIN_TEXT_COLOR, scale=0.7):
    """Creates a VGroup representing a plus-minus symbol."""
    plus = Text("+", color=color).scale(scale)
    minus = Text("-", color=color).scale(scale)
    minus.next_to(plus, DOWN, buff=0.05).align_to(plus, LEFT)
    return VGroup(plus, minus)


class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # BEAT 0: Visual Hook - Parabola Roots
        title = Text("Deriving the Quadratic Formula", color=GOLD_ACCENT).scale(0.9)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title, shift=UP))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-2, 2]},
            y_axis_config={"numbers_to_include": [-4]},
        ).add_coordinates()
        
        parabola_func = lambda x: x**2 - 4
        parabola = axes.plot(parabola_func, color=GOLD_ACCENT)
        parabola_label = Text("y = x^2 - 4", color=MAIN_TEXT_COLOR).scale(0.6).next_to(parabola, UP_LEFT, buff=0.5)

        root1_dot = Dot(axes.c2p(-2, 0), color=BLUE_ACCENT)
        root2_dot = Dot(axes.c2p(2, 0), color=BLUE_ACCENT)
        
        intro_text1 = Text("Where does the curve meet the axis?", color=MAIN_TEXT_COLOR).to_edge(UP).shift(DOWN*0.5)
        intro_text2 = Text("For any quadratic equation...", color=MAIN_TEXT_COLOR).to_edge(UP).shift(DOWN*0.5)

        self.play(Create(axes, run_time=1.5), Create(parabola, run_time=1.5), Write(parabola_label))
        self.play(Write(intro_text1))
        self.play(Flash(root1_dot, color=BLUE_ACCENT, flash_radius=0.3), Flash(root2_dot, color=BLUE_ACCENT, flash_radius=0.3))
        self.play(FadeIn(root1_dot, root2_dot))
        self.play(
            FadeOut(intro_text1, shift=UP),
            FadeIn(intro_text2, shift=DOWN)
        )
        self.play(FadeOut(VGroup(axes, parabola, parabola_label, root1_dot, root2_dot, intro_text2), shift=DOWN))
        self.wait(0.5)


        # BEAT 1: Standard Form & Divide by 'a'
        
        # Original Equation: ax^2 + bx + c = 0
        ax_squared = VGroup(Text("a", color=MAIN_TEXT_COLOR), create_power_mobject("x", "2", base_scale=0.7, power_scale=0.4)).arrange(RIGHT, buff=0.05)
        bx = VGroup(Text("b", color=MAIN_TEXT_COLOR), Text("x", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05)
        c_term = Text("c", color=MAIN_TEXT_COLOR)
        
        original_eq_mobjects = VGroup(
            ax_squared, Text("+", color=MAIN_TEXT_COLOR), bx, Text("+", color=MAIN_TEXT_COLOR), c_term,
            Text("=", color=MAIN_TEXT_COLOR), Text("0", color=MAIN_TEXT_COLOR)
        ).arrange(RIGHT, buff=0.2).scale(0.8).to_center().shift(UP*1.5)

        self.play(Write(original_eq_mobjects))
        self.wait(0.5)

        divide_by_a_text = Text("Divide by 'a'", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(divide_by_a_text))

        # New equation elements after division: x^2 + (b/a)x + (c/a) = 0
        x_squared_term_new = create_power_mobject("x", "2", base_scale=0.7, power_scale=0.4)
        b_over_a_x_term = VGroup(create_fraction_mobject("b", "a", scale_factor=0.7), Text("x", color=MAIN_TEXT_COLOR).scale(0.7)).arrange(RIGHT, buff=0.05)
        c_over_a_term = create_fraction_mobject("c", "a", scale_factor=0.7)

        new_eq_mobjects = VGroup(
            x_squared_term_new, Text("+", color=MAIN_TEXT_COLOR), b_over_a_x_term, Text("+", color=MAIN_TEXT_COLOR), c_over_a_term,
            Text("=", color=MAIN_TEXT_COLOR), Text("0", color=MAIN_TEXT_COLOR)
        ).arrange(RIGHT, buff=0.2).scale(0.8).next_to(original_eq_mobjects, DOWN, buff=0.5).to_center()

        self.play(
            FadeOut(original_eq_mobjects[0][0], shift=UP), # Fade out 'a' from ax^2
            ReplacementTransform(original_eq_mobjects[0][1], new_eq_mobjects[0]), # x^2
            ReplacementTransform(original_eq_mobjects[2], new_eq_mobjects[2]), # bx to (b/a)x
            ReplacementTransform(original_eq_mobjects[4], new_eq_mobjects[4]), # c to c/a
            FadeTransform(original_eq_mobjects[1], new_eq_mobjects[1]), # +
            FadeTransform(original_eq_mobjects[3], new_eq_mobjects[3]), # +
            FadeTransform(original_eq_mobjects[5], new_eq_mobjects[5]), # =
            FadeTransform(original_eq_mobjects[6], new_eq_mobjects[6]), # 0
            FadeOut(divide_by_a_text, shift=UP)
        )
        self.remove(original_eq_mobjects)
        current_eq = new_eq_mobjects # Update current equation
        self.play(current_eq.animate.to_center().shift(UP*1.5))
        self.wait(1)


        # BEAT 2: Move C & Completing the Square (Geometric + Algebraic)
        
        # 2a: Move c/a to RHS
        move_c_text = Text("Isolate x-terms", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(move_c_text))

        neg_c_over_a_term = VGroup(Text("-", color=MAIN_TEXT_COLOR), current_eq[4].copy()).arrange(RIGHT, buff=0.05) # -c/a

        eq_after_move_c = VGroup(
            current_eq[0].copy(), current_eq[1].copy(), current_eq[2].copy(), # x^2 + (b/a)x
            current_eq[5].copy(), # =
            neg_c_over_a_term # -c/a
        ).arrange(RIGHT, buff=0.2).scale(0.8).next_to(current_eq, DOWN, buff=0.5).to_center()

        self.play(
            ReplacementTransform(VGroup(current_eq[0], current_eq[1], current_eq[2]), VGroup(eq_after_move_c[0], eq_after_move_c[1], eq_after_move_c[2])),
            ReplacementTransform(current_eq[5], eq_after_move_c[3]), # =
            ReplacementTransform(current_eq[4], eq_after_move_c[4][1]), # c/a part of -c/a
            FadeIn(eq_after_move_c[4][0]), # '-' sign
            FadeOut(current_eq[3], current_eq[6]), # Fade out the '+' and '0'
            FadeOut(move_c_text, shift=UP)
        )
        self.remove(current_eq)
        current_eq = eq_after_move_c
        self.play(current_eq.animate.to_center().shift(UP*1.5))
        self.wait(1)

        # 2b: Geometric insight for Completing the Square
        completing_text = Text("Time to 'complete the square'", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(completing_text))

        x_val_geom = 2.0
        b_over_2a_val_geom = 0.5 # A value for b/2a

        square_x = Square(side_length=x_val_geom, color=BLUE_ACCENT, fill_opacity=0.3)
        rect_bx1 = Rectangle(width=b_over_2a_val_geom, height=x_val_geom, color=GOLD_ACCENT, fill_opacity=0.3)
        rect_bx2 = Rectangle(width=x_val_geom, height=b_over_2a_val_geom, color=GOLD_ACCENT, fill_opacity=0.3)
        
        square_x.move_to(ORIGIN + LEFT*2 + DOWN*0.5)
        rect_bx1.next_to(square_x, RIGHT, buff=0)
        rect_bx2.next_to(square_x, UP, buff=0)

        label_x_sq_geom = create_power_mobject("x", "2", base_scale=0.7, power_scale=0.4).move_to(square_x.get_center())
        
        b_over_2a_frac_geom_str = create_fraction_mobject("b", "2a", scale_factor=0.6)
        label_bx_geom_x = Text("x", color=MAIN_TEXT_COLOR).scale(0.6)
        label_bx_geom1 = VGroup(b_over_2a_frac_geom_str.copy(), label_bx_geom_x.copy()).arrange(RIGHT, buff=0.05).move_to(rect_bx1.get_center())
        label_bx_geom2 = VGroup(b_over_2a_frac_geom_str.copy(), label_bx_geom_x.copy()).arrange(RIGHT, buff=0.05).move_to(rect_bx2.get_center())

        self.play(
            FadeOut(current_eq, shift=LEFT),
            Create(square_x), Write(label_x_sq_geom),
            Create(rect_bx1), Write(label_bx_geom1),
            Create(rect_bx2), Write(label_bx_geom2),
        )
        self.wait(1)

        # Show the missing piece
        missing_square_geom = Square(side_length=b_over_2a_val_geom, color=BLUE_ACCENT, fill_opacity=0.1, stroke_opacity=0.5, stroke_dash_offset=0.5)
        missing_square_geom.next_to(rect_bx1, UP, buff=0).align_to(rect_bx2, RIGHT)

        label_missing_sq_exp_geom = create_power_mobject(create_fraction_mobject("b", "2a", scale_factor=0.5), "2", base_scale=0.5, power_scale=0.3).move_to(missing_square_geom.get_center())
        
        self.play(Create(missing_square_geom), Write(label_missing_sq_exp_geom))
        self.wait(1)

        self.play(
            FadeOut(VGroup(square_x, rect_bx1, rect_bx2, missing_square_geom, label_x_sq_geom, label_bx_geom1, label_bx_geom2, label_missing_sq_exp_geom)),
            FadeOut(completing_text, shift=UP)
        )
        self.wait(0.5)

        # 2c: Algebraically add (b/2a)^2 to both sides
        add_sq_text = Text("Add the missing piece to both sides", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(add_sq_text))

        current_eq.to_center().shift(UP*1.5)
        self.play(FadeIn(current_eq, shift=LEFT))
        
        b_over_2a_sq_term = create_power_mobject(create_fraction_mobject("b", "2a", scale_factor=0.7), "2", base_scale=0.7, power_scale=0.4)
        
        lhs_added = VGroup(
            current_eq[0].copy(), current_eq[1].copy(), current_eq[2].copy(),
            Text("+", color=MAIN_TEXT_COLOR).scale(0.8), b_over_2a_sq_term.copy()
        ).arrange(RIGHT, buff=0.2)

        rhs_added = VGroup(
            current_eq[4].copy(), Text("+", color=MAIN_TEXT_COLOR).scale(0.8), b_over_2a_sq_term.copy()
        ).arrange(RIGHT, buff=0.2)

        eq_after_add = VGroup(lhs_added, current_eq[3].copy(), rhs_added).arrange(RIGHT, buff=0.2).scale(0.8).to_center().shift(DOWN*0.5)

        self.play(
            FadeTransform(current_eq, eq_after_add),
            FadeOut(add_sq_text, shift=UP)
        )
        self.remove(current_eq)
        current_eq = eq_after_add
        self.wait(1)

        # Factor LHS and simplify RHS
        factor_text = Text("Factor LHS, expand RHS", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(factor_text))

        # LHS: (x + b/2a)^2
        x_plus_b_over_2a = VGroup(
            Text("(", color=MAIN_TEXT_COLOR),
            Text("x", color=MAIN_TEXT_COLOR), Text("+", color=MAIN_TEXT_COLOR), create_fraction_mobject("b", "2a", scale_factor=0.7),
            Text(")", color=MAIN_TEXT_COLOR)
        ).arrange(RIGHT, buff=0.05)
        lhs_factored = create_power_mobject(x_plus_b_over_2a, "2", base_scale=0.8, power_scale=0.4)

        # RHS: -c/a + b^2/4a^2
        b_sq = create_power_mobject("b", "2", base_scale=0.7, power_scale=0.4)
        four_a_sq = VGroup(Text("4", color=MAIN_TEXT_COLOR), create_power_mobject("a", "2", base_scale=0.7, power_scale=0.4)).arrange(RIGHT, buff=0.05)
        b_sq_over_4a_sq = create_fraction_mobject(b_sq, four_a_sq, scale_factor=0.7)
        
        rhs_expanded = VGroup(
            Text("-", color=MAIN_TEXT_COLOR), create_fraction_mobject("c", "a", scale_factor=0.7),
            Text("+", color=MAIN_TEXT_COLOR), b_sq_over_4a_sq
        ).arrange(RIGHT, buff=0.2)

        final_eq_beat2 = VGroup(
            lhs_factored, current_eq[1].copy(), rhs_expanded
        ).arrange(RIGHT, buff=0.2).scale(0.8).to_center().shift(UP*1.5)

        self.play(
            ReplacementTransform(current_eq, final_eq_beat2), # Transform previous equation to this one
            FadeOut(factor_text, shift=UP)
        )
        self.remove(current_eq)
        current_eq = final_eq_beat2
        self.wait(1)


        # BEAT 3: Simplify RHS & Take Square Root
        
        simplify_rhs_text = Text("Combine terms on the right", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(simplify_rhs_text))

        # RHS: (b^2 - 4ac) / 4a^2
        b_sq_num = create_power_mobject("b", "2", base_scale=0.7, power_scale=0.4)
        four_ac_num = VGroup(Text("4", color=MAIN_TEXT_COLOR), Text("a", color=MAIN_TEXT_COLOR), Text("c", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05)
        numerator_rhs = VGroup(b_sq_num, Text("-", color=MAIN_TEXT_COLOR), four_ac_num).arrange(RIGHT, buff=0.05)
        
        four_a_sq_den = VGroup(Text("4", color=MAIN_TEXT_COLOR), create_power_mobject("a", "2", base_scale=0.7, power_scale=0.4)).arrange(RIGHT, buff=0.05)
        
        combined_rhs_frac = create_fraction_mobject(numerator_rhs, four_a_sq_den, scale_factor=0.7)

        lhs_beat3 = current_eq[0].copy()
        equals_op_beat3 = current_eq[1].copy()

        eq_after_simplify_rhs = VGroup(
            lhs_beat3, equals_op_beat3, combined_rhs_frac
        ).arrange(RIGHT, buff=0.2).scale(0.8).to_center().shift(UP*1.5)

        self.play(
            ReplacementTransform(current_eq, eq_after_simplify_rhs),
            FadeOut(simplify_rhs_text, shift=UP)
        )
        self.remove(current_eq)
        current_eq = eq_after_simplify_rhs
        self.wait(1)

        # Take Square Root
        sqrt_text = Text("Take the square root of both sides", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(sqrt_text))

        # LHS: x + b/2a (remove ^2)
        lhs_sqrt = VGroup(
            Text("x", color=MAIN_TEXT_COLOR), Text("+", color=MAIN_TEXT_COLOR), create_fraction_mobject("b", "2a", scale_factor=0.7)
        ).arrange(RIGHT, buff=0.1).scale(0.8/0.8) # Adjust scale back to original for content of (x+b/2a)^2

        # RHS: ± sqrt((b^2 - 4ac) / 4a^2) -> ± √(b^2 - 4ac) / 2a
        plus_minus_op = create_plus_minus_mobject(scale=0.8)
        
        num_inside_sqrt = VGroup(
            create_power_mobject("b", "2", base_scale=0.7, power_scale=0.4), Text("-", color=MAIN_TEXT_COLOR).scale(0.7), 
            VGroup(Text("4", color=MAIN_TEXT_COLOR), Text("a", color=MAIN_TEXT_COLOR), Text("c", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05).scale(0.7/Text("4").height*Text("x").height)
        ).arrange(RIGHT, buff=0.05)
        
        den_after_sqrt = VGroup(Text("2", color=MAIN_TEXT_COLOR), Text("a", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05).scale(0.7)

        # Create the fractional part under the square root
        sqrt_content_frac = create_fraction_mobject(num_inside_sqrt, den_after_sqrt, scale_factor=0.7)

        rhs_sqrt = VGroup(plus_minus_op, create_sqrt_mobject(sqrt_content_frac, stroke_width=3)).arrange(RIGHT, buff=0.1)

        final_eq_beat3 = VGroup(
            lhs_sqrt, current_eq[1].copy(), rhs_sqrt
        ).arrange(RIGHT, buff=0.2).scale(0.8).to_center().shift(UP*1.5)

        self.play(
            ReplacementTransform(current_eq, final_eq_beat3),
            FadeOut(sqrt_text, shift=UP)
        )
        self.remove(current_eq)
        current_eq = final_eq_beat3
        self.wait(1)


        # BEAT 4: Isolate X & Final Formula
        
        isolate_x_text = Text("Isolate 'x' and combine terms", color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(isolate_x_text))

        x_final = Text("x", color=MAIN_TEXT_COLOR).scale(0.8)

        # Build the numerator for the final formula: -b ±√(b^2 - 4ac)
        neg_b_num = Text("-b", color=MAIN_TEXT_COLOR).scale(0.8)
        plus_minus_op_final = create_plus_minus_mobject(scale=0.8)

        b_sq_minus_4ac_num_final_content = VGroup(
            create_power_mobject("b", "2", base_scale=0.8, power_scale=0.5), Text("-", color=MAIN_TEXT_COLOR).scale(0.8), 
            VGroup(Text("4", color=MAIN_TEXT_COLOR), Text("a", color=MAIN_TEXT_COLOR), Text("c", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05).scale(0.8/Text("4").height*Text("x").height)
        ).arrange(RIGHT, buff=0.05)

        sqrt_part_num = create_sqrt_mobject(b_sq_minus_4ac_num_final_content, stroke_width=3)

        final_numerator = VGroup(
            neg_b_num, plus_minus_op_final, sqrt_part_num
        ).arrange(RIGHT, buff=0.1)

        final_denominator = VGroup(Text("2", color=MAIN_TEXT_COLOR), Text("a", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05).scale(0.8)

        final_rhs_frac = create_fraction_mobject(final_numerator, final_denominator, scale_factor=0.8)

        final_quadratic_formula = VGroup(
            x_final, current_eq[1].copy(), final_rhs_frac
        ).arrange(RIGHT, buff=0.2).to_center().shift(UP*1.5)

        self.play(
            ReplacementTransform(current_eq, final_quadratic_formula),
            FadeOut(isolate_x_text, shift=UP)
        )
        self.remove(current_eq)
        self.wait(2)


        # RECAP CARD
        recap_title = Text("The Quadratic Formula", color=GOLD_ACCENT).scale(1.2).to_edge(UP).shift(DOWN*0.5)
        
        x_final_recap = Text("x", color=MAIN_TEXT_COLOR).scale(1.0)
        neg_b_num_recap = Text("-b", color=MAIN_TEXT_COLOR).scale(1.0)
        plus_minus_op_recap = create_plus_minus_mobject(scale=1.0)

        b_sq_minus_4ac_num_recap_content = VGroup(
            create_power_mobject("b", "2", base_scale=1.0, power_scale=0.6), Text("-", color=MAIN_TEXT_COLOR).scale(1.0), 
            VGroup(Text("4", color=MAIN_TEXT_COLOR), Text("a", color=MAIN_TEXT_COLOR), Text("c", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05).scale(1.0/Text("4").height*Text("x").height)
        ).arrange(RIGHT, buff=0.05)

        sqrt_part_num_recap = create_sqrt_mobject(b_sq_minus_4ac_num_recap_content, stroke_width=4)

        final_numerator_recap = VGroup(
            neg_b_num_recap, plus_minus_op_recap, sqrt_part_num_recap
        ).arrange(RIGHT, buff=0.1)

        final_denominator_recap = VGroup(Text("2", color=MAIN_TEXT_COLOR), Text("a", color=MAIN_TEXT_COLOR)).arrange(RIGHT, buff=0.05).scale(1.0)

        recap_formula = VGroup(
            x_final_recap, Text("=", color=MAIN_TEXT_COLOR).scale(1.0), create_fraction_mobject(final_numerator_recap, final_denominator_recap, scale_factor=1.0)
        ).arrange(RIGHT, buff=0.2).to_center()

        purpose_text = Text(
            "Finds the roots of any quadratic equation",
            color=BLUE_ACCENT
        ).scale(0.7).next_to(recap_formula, DOWN, buff=1.0)
        
        self.play(FadeOut(final_quadratic_formula, shift=DOWN))
        self.play(Write(recap_title))
        self.play(Write(recap_formula))
        self.play(Write(purpose_text))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_formula, purpose_text)))