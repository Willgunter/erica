from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_C # Use a bright blue
        GOLD_ACCENT = GOLD_A # Use a bright gold
        WHITE_TEXT = WHITE

        # --- Helper for creating equation elements using Text ---
        def create_text_mobject(s, color=WHITE_TEXT, scale=0.8):
            return Text(s, color=color).scale(scale)

        def create_exponent(base_mobject, exp_str, color=WHITE_TEXT, scale_exp=0.5):
            exp = Text(exp_str, color=color).scale(scale_exp)
            # Position relative to base_mobject's top-right
            # Shift slightly up and right for a natural exponent look
            exp.next_to(base_mobject, UP + RIGHT * 0.5, buff=0.05).shift(UP * 0.1)
            return exp

        # --- Scene Setup ---
        title = create_text_mobject("General Form & Formula Derivation", color=GOLD_ACCENT, scale=0.9).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-3, 7, 1],
            x_length=10, y_length=7,
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"color": GRAY}
        ).shift(DOWN * 0.5)
        self.play(Create(plane), run_time=1.5)

        # --- BEAT 1: The Parabola & Its Simplest Form (y = ax^2) ---
        beat1_label_part1 = create_text_mobject("Basic Parabola: y = ax", color=GOLD_ACCENT, scale=0.8)
        # Access the 'x' character Mobject for positioning the exponent
        x_char_in_label1 = beat1_label_part1[len("Basic Parabola: y = ax")-1] 
        beat1_label_exp = create_exponent(x_char_in_label1, "2", scale_exp=0.4)
        beat1_label_full = VGroup(beat1_label_part1, beat1_label_exp)
        # Position the full label group
        beat1_label_full.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(beat1_label_full))

        # Initial parabola (y = x^2)
        initial_parabola = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=4)
        current_parabola_anim = initial_parabola.copy() # Mobject to be transformed
        self.add(current_parabola_anim)
        self.play(Create(initial_parabola))

        # Construct "y = ax^2" equation
        y_text = create_text_mobject("y", color=BLUE_ACCENT)
        eq_sign = create_text_mobject("=")
        a_text = create_text_mobject("a", color=GOLD_ACCENT)
        x_text = create_text_mobject("x")
        exp_2_text = create_exponent(x_text, "2")
        
        # Manually arrange elements for "y = ax^2"
        y_text.move_to(ORIGIN)
        eq_sign.next_to(y_text, RIGHT, buff=0.1)
        a_text.next_to(eq_sign, RIGHT, buff=0.1)
        x_text.next_to(a_text, RIGHT, buff=0.1)
        exp_2_text.move_to(create_exponent(x_text, "2").get_center()) # Reposition exponent properly
        
        simple_eq_group = VGroup(y_text, eq_sign, a_text, x_text, exp_2_text)
        simple_eq_group.to_edge(UP).shift(DOWN*2)
        
        self.play(FadeIn(simple_eq_group))
        self.wait(0.5)

        # Animate 'a' changing its value and affecting the parabola
        a_value_tracker = ValueTracker(1)
        a_number = DecimalNumber(a_value_tracker.get_value(), num_decimal_places=1, color=GOLD_ACCENT)
        a_label_prefix = create_text_mobject("a = ", color=GOLD_ACCENT)
        a_label_full = VGroup(a_label_prefix, a_number).arrange(RIGHT, buff=0.1)
        a_label_full.next_to(simple_eq_group, DOWN, buff=0.3)
        self.play(FadeIn(a_label_full))
        
        a_number.add_updater(lambda m: m.set_value(a_value_tracker.get_value()))
        
        def update_parabola_a(a_val):
            return plane.get_graph(lambda x: a_val * x**2, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=4)

        # Transform the parabola and update 'a' value
        target_parabola_05 = update_parabola_a(0.5)
        self.play(a_value_tracker.animate.set_value(0.5), Transform(current_parabola_anim, target_parabola_05), run_time=1)
        target_parabola_2 = update_parabola_a(2)
        self.play(a_value_tracker.animate.set_value(2), Transform(current_parabola_anim, target_parabola_2), run_time=1)
        target_parabola_neg1 = update_parabola_a(-1)
        self.play(a_value_tracker.animate.set_value(-1), Transform(current_parabola_anim, target_parabola_neg1), run_time=1)
        target_parabola_1 = update_parabola_a(1)
        self.play(a_value_tracker.animate.set_value(1), Transform(current_parabola_anim, target_parabola_1), run_time=1)

        a_number.remove_updater(a_number.updaters[0]) # Remove updater before fading out
        self.play(FadeOut(a_label_full), FadeOut(beat1_label_full))
        self.wait(0.5)

        # --- BEAT 2: General Form (ax^2 + bx + c = 0) ---
        beat2_label_part1 = create_text_mobject("General Form: ax", color=GOLD_ACCENT, scale=0.8)
        x_char_in_label2 = beat2_label_part1[len("General Form: ax")-1]
        beat2_label_exp = create_exponent(x_char_in_label2, "2", scale_exp=0.4)
        beat2_label_part2 = create_text_mobject(" + bx + c = 0", color=GOLD_ACCENT, scale=0.8)
        
        # Position parts of the label
        beat2_label_part2.next_to(beat2_label_exp, RIGHT, buff=0.05).align_to(beat2_label_exp, DOWN)
        beat2_label_full = VGroup(beat2_label_part1, beat2_label_exp, beat2_label_part2)
        beat2_label_full.move_to(simple_eq_group.get_top() + DOWN*0.5) # Reposition as a group
        self.play(FadeIn(beat2_label_full))

        # Construct "ax^2 + bx + c = 0"
        gf_a_mobj = create_text_mobject("a", color=GOLD_ACCENT)
        gf_x_mobj = create_text_mobject("x")
        gf_exp2_mobj = create_exponent(gf_x_mobj, "2")
        gf_ax2_part = VGroup(gf_a_mobj, gf_x_mobj, gf_exp2_mobj)
        # Manual arrangement for "ax^2"
        gf_a_mobj.next_to(gf_x_mobj, LEFT, buff=0.05)
        gf_exp2_mobj.move_to(create_exponent(gf_x_mobj, "2").get_center())

        gf_plus_b_mobj = create_text_mobject("+")
        gf_b_mobj = create_text_mobject("b", color=GOLD_ACCENT)
        gf_x_term_mobj = create_text_mobject("x")
        gf_bx_part = VGroup(gf_plus_b_mobj, gf_b_mobj, gf_x_term_mobj).arrange(RIGHT, buff=0.1)

        gf_plus_c_mobj = create_text_mobject("+")
        gf_c_mobj = create_text_mobject("c", color=GOLD_ACCENT)
        gf_c_term_part = VGroup(gf_plus_c_mobj, gf_c_mobj).arrange(RIGHT, buff=0.1)

        gf_equals_0_part = VGroup(create_text_mobject("="), create_text_mobject("0")).arrange(RIGHT, buff=0.1)

        full_general_form = VGroup(gf_ax2_part, gf_bx_part, gf_c_term_part, gf_equals_0_part).arrange(RIGHT, buff=0.3)
        
        # Transform the simple equation to the general form
        self.play(ReplacementTransform(simple_eq_group, full_general_form.copy().move_to(simple_eq_group.get_center())))
        self.play(full_general_form.animate.to_edge(UP).shift(DOWN*2))

        # Reset parabola to a general one and demonstrate 'c' (y-intercept)
        general_parabola_c_demo = plane.get_graph(lambda x: x**2 + x - 2, x_range=[-3.5, 2.5], color=BLUE_ACCENT, stroke_width=4)
        self.play(Transform(current_parabola_anim, general_parabola_c_demo))

        c_dot = Dot(plane.c2p(0, -2), color=GOLD_ACCENT)
        c_tracker = ValueTracker(-2)
        c_value_label = DecimalNumber(c_tracker.get_value(), num_decimal_places=0, color=GOLD_ACCENT)
        c_label_prefix = create_text_mobject("c = ", color=GOLD_ACCENT)
        c_label_full = VGroup(c_label_prefix, c_value_label).arrange(RIGHT, buff=0.1).next_to(c_dot, RIGHT, buff=0.2)
        
        self.play(FadeIn(c_dot), FadeIn(c_label_full))
        c_value_label.add_updater(lambda m: m.set_value(c_tracker.get_value()))

        def update_parabola_c(val_c):
            return plane.get_graph(lambda x: x**2 + x + val_c, x_range=[-3.5, 2.5], color=BLUE_ACCENT, stroke_width=4)
        
        target_parabola_c2 = update_parabola_c(2)
        self.play(
            c_tracker.animate.set_value(2),
            Transform(current_parabola_anim, target_parabola_c2),
            c_dot.animate.move_to(plane.c2p(0, 2)),
            run_time=2
        )
        self.wait(0.5)

        c_value_label.remove_updater(c_value_label.updaters[0])
        self.play(FadeOut(c_dot), FadeOut(c_label_full), FadeOut(beat2_label_full))
        self.wait(0.5)

        # --- BEAT 3: Roots: Solving for X ---
        beat3_label = create_text_mobject("Roots: Solving for X", color=GOLD_ACCENT, scale=0.8).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(beat3_label))

        # Show parabola intersecting x-axis
        roots_parabola = plane.get_graph(lambda x: x**2 + x - 2, x_range=[-3.5, 2.5], color=BLUE_ACCENT, stroke_width=4)
        self.play(Transform(current_parabola_anim, roots_parabola))
        
        x_intercept1 = plane.c2p(-2, 0)
        x_intercept2 = plane.c2p(1, 0)
        dot1 = Dot(x_intercept1, color=GOLD_ACCENT)
        dot2 = Dot(x_intercept2, color=GOLD_ACCENT)

        self.play(FadeIn(dot1, dot2), run_time=1)
        
        solve_text = create_text_mobject("Find 'x' when y = 0", color=WHITE_TEXT, scale=0.7).to_edge(RIGHT).shift(UP * 1.5)
        arrow_to_roots = Arrow(solve_text.get_left(), dot1.get_center(), buff=0.2, color=WHITE_TEXT)
        self.play(FadeIn(solve_text), Create(arrow_to_roots))
        self.wait(1)

        self.play(FadeOut(dot1, dot2, solve_text, arrow_to_roots, beat3_label))
        self.wait(0.5)

        # --- BEAT 4: The Idea of Derivation (Conceptual) ---
        beat4_label = create_text_mobject("The General Solution", color=GOLD_ACCENT, scale=0.8).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(beat4_label))
        
        # Keep the full_general_form equation visible and move it
        self.play(full_general_form.animate.move_to(UP * 2.5 + LEFT * 2))

        question_mark = create_text_mobject("?", color=GOLD_ACCENT, scale=2).move_to(plane.get_center())
        derivation_text = create_text_mobject("A universal method to find 'x'", color=WHITE_TEXT, scale=0.7).next_to(question_mark, DOWN, buff=0.5)
        self.play(FadeIn(question_mark), FadeIn(derivation_text))
        self.wait(1.5)

        self.play(FadeOut(question_mark, derivation_text, beat4_label))
        self.play(FadeOut(current_parabola_anim, plane)) # Fade out the graph and plane
        self.wait(0.5)

        # --- BEAT 5: The Quadratic Formula ---
        beat5_label = create_text_mobject("The Quadratic Formula", color=GOLD_ACCENT, scale=0.8).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(beat5_label))

        # Construct Quadratic Formula using Text
        x_eq = create_text_mobject("x", color=BLUE_ACCENT)
        eq_sign = create_text_mobject("=")

        # Numerator: -b ± sqrt(b^2 - 4ac)
        minus_b_part_minus = create_text_mobject("-")
        minus_b_part_b = create_text_mobject("b", color=GOLD_ACCENT)
        minus_b_part = VGroup(minus_b_part_minus, minus_b_part_b).arrange(RIGHT, buff=0.05)
        
        plus_minus = create_text_mobject("±")

        # b^2 part
        b_sq_base_mobj = create_text_mobject("b", color=GOLD_ACCENT)
        b_sq_exp_mobj = create_exponent(b_sq_base_mobj, "2")
        b_sq_part = VGroup(b_sq_base_mobj, b_sq_exp_mobj)
        b_sq_exp_mobj.move_to(create_exponent(b_sq_base_mobj, "2").get_center()) # Ensure proper positioning

        # -4ac part
        minus_4ac_part = VGroup(
            create_text_mobject("-"), create_text_mobject("4"),
            create_text_mobject("a", color=GOLD_ACCENT), create_text_mobject("c", color=GOLD_ACCENT)
        ).arrange(RIGHT, buff=0.08)

        discriminant_vgroup = VGroup(b_sq_part, minus_4ac_part).arrange(RIGHT, buff=0.15)
        
        # Square root symbol (simplified for Text constraint)
        sqrt_line_top = Line(LEFT, RIGHT, color=WHITE_TEXT, stroke_width=3)
        sqrt_line_top.set_length(discriminant_vgroup.get_width() + 0.4)
        sqrt_line_top.next_to(discriminant_vgroup, UP, buff=0.1)
        
        # Manually draw a checkmark style square root symbol on the left
        sqrt_tick_start = sqrt_line_top.get_left() + LEFT * 0.1
        sqrt_tick_mid = sqrt_tick_start + DOWN * 0.2 + RIGHT * 0.1
        sqrt_tick_end = sqrt_tick_mid + UP * 0.3 + RIGHT * 0.1
        sqrt_tick = VGroup(
            Line(sqrt_tick_start, sqrt_tick_mid, color=WHITE_TEXT, stroke_width=3),
            Line(sqrt_tick_mid, sqrt_tick_end, color=WHITE_TEXT, stroke_width=3)
        )
        
        sqrt_group = VGroup(sqrt_tick, sqrt_line_top, discriminant_vgroup)

        numerator_elements = VGroup(minus_b_part, plus_minus, sqrt_group).arrange(RIGHT, buff=0.05)
        
        # Fraction line
        frac_line = Line(LEFT, RIGHT, color=WHITE_TEXT, stroke_width=3).set_length(numerator_elements.get_width() * 1.1)
        
        # Denominator: 2a
        den_2a = VGroup(create_text_mobject("2"), create_text_mobject("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)

        # Assemble the full quadratic formula
        quadratic_formula_content = VGroup(numerator_elements, frac_line, den_2a).arrange(DOWN, buff=0.1)
        quadratic_formula = VGroup(x_eq, eq_sign, quadratic_formula_content).arrange(RIGHT, buff=0.1).move_to(ORIGIN)

        self.play(FadeIn(quadratic_formula), run_time=3)
        self.wait(2)
        
        # Highlight coefficients in general form and formula
        # Access elements by index within their VGroups for flashing
        self.play(
            LaggedStart(
                Flash(full_general_form[0][0], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'a' in ax^2
                Flash(full_general_form[1][1], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'b' in bx
                Flash(full_general_form[2][1], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'c' in c
                Flash(quadratic_formula[2][0][0][1], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'b' in -b
                Flash(quadratic_formula[2][0][2][2][0][0], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'b' in b^2 (base)
                Flash(quadratic_formula[2][0][2][2][1][2], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'a' in -4ac
                Flash(quadratic_formula[2][0][2][2][1][3], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'c' in -4ac
                Flash(quadratic_formula[2][2][1], color=GOLD_ACCENT, line_length=0.1, num_lines=1), # 'a' in 2a
                lag_ratio=0.1,
                run_time=2
            )
        )
        self.wait(1)

        # --- BEAT 6: Recap Card ---
        self.play(FadeOut(full_general_form, quadratic_formula, beat5_label))

        recap_title = create_text_mobject("Recap", color=GOLD_ACCENT, scale=1).to_edge(UP, buff=1)
        self.play(FadeIn(recap_title))
        
        # 1. Quadratic equations: ax^2 + bx + c = 0
        p1_text_part1 = create_text_mobject("1. Quadratic equations: ax", color=WHITE_TEXT, scale=0.7)
        x_in_p1 = p1_text_part1[len("1. Quadratic equations: ax")-1] # Get the 'x' Mobject
        p1_exp = create_exponent(x_in_p1, "2", scale_exp=0.4)
        p1_text_part2 = create_text_mobject(" + bx + c = 0", color=WHITE_TEXT, scale=0.7)
        
        # Position parts of the first point
        p1_text_part1.to_edge(LEFT, buff=1).shift(UP * 1.5)
        p1_exp.move_to(create_exponent(x_in_p1, "2").get_center()) # Ensure it's correctly placed on the 'x'
        p1_text_part2.next_to(p1_exp, RIGHT, buff=0.1).align_to(p1_exp, DOWN)
        point1_assembled = VGroup(p1_text_part1, p1_exp, p1_text_part2)

        point2_assembled = create_text_mobject("2. Coefficients (a, b, c) define the parabola's shape and position.", color=WHITE_TEXT, scale=0.7).next_to(point1_assembled, DOWN, buff=0.3).align_to(point1_assembled, LEFT)
        point3_assembled = create_text_mobject("3. Quadratic Formula: Universal solution for 'x'.", color=WHITE_TEXT, scale=0.7).next_to(point2_assembled, DOWN, buff=0.3).align_to(point2_assembled, LEFT)

        recap_card_final = VGroup(point1_assembled, point2_assembled, point3_assembled).center().shift(UP * 0.5)

        self.play(FadeIn(recap_card_final), run_time=2)
        self.wait(3)
        self.play(FadeOut(recap_card_final, title, recap_title))
        self.wait(1)