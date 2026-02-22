from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # 1. Configuration for dark background, blue/gold accents
        self.camera.background_color = BLACK

        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C

        # Helper to create exponents manually
        def create_exponent_text(base_mobject, exp_str="2", color=BLUE_ACCENT):
            exp_text = Text(exp_str, font_size=24, color=color)
            exp_text.scale_to_fit_height(base_mobject.get_height() * 0.5)
            exp_text.next_to(base_mobject.get_corner(UR), buff=0.05).shift(UP * 0.05)
            return exp_text

        # Helper to create fractions manually
        def create_fraction_mobject(numerator_mobject, denominator_mobject, bar_color=WHITE, scale=1.0):
            line = Line(LEFT, RIGHT, color=bar_color)
            
            max_width = max(numerator_mobject.get_width(), denominator_mobject.get_width())
            line.set_width(max_width * 1.2)

            line.move_to(ORIGIN)
            numerator_mobject.next_to(line, UP, buff=0.1)
            denominator_mobject.next_to(line, DOWN, buff=0.1)
            
            numerator_mobject.align_to(line, ORIGIN)
            denominator_mobject.align_to(line, ORIGIN)

            frac_group = VGroup(numerator_mobject, line, denominator_mobject)
            frac_group.scale(scale)
            return frac_group

        # Helper to create square root manually
        def create_sqrt_mobject(expression_mobject, color=WHITE, scale=1.0):
            # Radical part (hook)
            radical_hook = VGroup(
                Line(ORIGIN, LEFT * 0.2 + DOWN * 0.2, color=color, stroke_width=3),
                Line(LEFT * 0.2 + DOWN * 0.2, LEFT * 0.1 + UP * 0.3, color=color, stroke_width=3)
            )
            
            # Top line
            top_line_start = radical_hook.get_corner(UR)
            top_line_end = RIGHT * (expression_mobject.get_width() + 0.2) + top_line_start[1]*UP
            top_line = Line(top_line_start, top_line_end, color=color, stroke_width=3)
            
            sqrt_symbol = VGroup(radical_hook, top_line)
            sqrt_symbol.scale_to_fit_height(expression_mobject.get_height() * 1.2)
            
            sqrt_symbol.next_to(expression_mobject, LEFT, buff=0.05).align_to(expression_mobject, DOWN)
            
            return VGroup(sqrt_symbol, expression_mobject).scale(scale)

        # --- Scene Start ---

        # 2. Strong visual hook: Parabola and its roots
        intro_title = Text("Unlocking the Quadratic Formula", font_size=50, color=GOLD_ACCENT)
        self.play(Write(intro_title))
        self.wait(1)
        self.play(FadeOut(intro_title, shift=UP))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": BLUE_ACCENT, "include_numbers": False, "include_ticks": False},
        ).to_edge(DOWN)

        parabola = axes.plot(lambda x: x**2 - 1, color=GOLD_ACCENT)
        x_label = Text("x", color=BLUE_ACCENT).next_to(axes.x_axis, DOWN)
        y_label = Text("y", color=BLUE_ACCENT).next_to(axes.y_axis, LEFT)

        label_y_eq_0 = Text("y = 0 (Roots)", font_size=30, color=BLUE_ACCENT).to_edge(UP).shift(LEFT*2)
        root_1 = Dot(axes.c2p(-1, 0), color=RED)
        root_2 = Dot(axes.c2p(1, 0), color=RED)
        root_label_1 = Text("x = -1", font_size=24, color=RED).next_to(root_1, DOWN)
        root_label_2 = Text("x = 1", font_size=24, color=RED).next_to(root_2, DOWN)
        
        # Initial quadratic equation in text form
        eq_a_cur = Text("a", color=GOLD_ACCENT)
        eq_x_cur_sq = Text("x", color=BLUE_ACCENT)
        eq_exp2_cur = create_exponent_text(eq_x_cur_sq, "2", BLUE_ACCENT)
        eq_ax2_cur = VGroup(eq_a_cur, eq_x_cur_sq, eq_exp2_cur).arrange(RIGHT, buff=0.1)
        
        eq_plus1_cur = Text("+", color=WHITE)
        eq_b_cur = Text("b", color=GOLD_ACCENT)
        eq_x_cur_b = Text("x", color=BLUE_ACCENT)
        eq_bx_cur = VGroup(eq_b_cur, eq_x_cur_b).arrange(RIGHT, buff=0.1)
        
        eq_plus2_cur = Text("+", color=WHITE)
        eq_c_cur = Text("c", color=GOLD_ACCENT)
        
        eq_equals_cur = Text("=", color=WHITE)
        eq_zero_cur = Text("0", color=BLUE_ACCENT)
        
        current_eq_mobj = VGroup(
            eq_ax2_cur, eq_plus1_cur, eq_bx_cur, eq_plus2_cur, eq_c_cur, eq_equals_cur, eq_zero_cur
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)

        problem_text = Text("Find 'x' when y=0", font_size=30, color=WHITE)
        problem_text.next_to(current_eq_mobj, DOWN, buff=0.5)

        self.play(
            Create(axes),
            Create(parabola),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        self.play(Write(label_y_eq_0))
        self.play(Create(root_1), Create(root_2), FadeIn(root_label_1, root_label_2))
        self.play(FadeOut(label_y_eq_0, root_1, root_2, root_label_1, root_label_2))
        self.play(Write(current_eq_mobj))
        self.play(Write(problem_text))
        self.wait(1.5)
        self.remove(axes, parabola, x_label, y_label, problem_text)

        # --- Beat 1: Isolate constant term ---
        # ax^2 + bx + c = 0  ->  ax^2 + bx = -c
        beat_title_1 = Text("1. Isolate 'c'", font_size=35, color=GOLD_ACCENT).to_corner(UL)
        
        # Target 1: ax^2 + bx = -c
        target_ax2_1 = VGroup(eq_a_cur.copy(), eq_x_cur_sq.copy(), eq_exp2_cur.copy()).arrange(RIGHT, buff=0.1)
        target_plus1_1 = eq_plus1_cur.copy()
        target_bx1 = VGroup(eq_b_cur.copy(), eq_x_cur_b.copy()).arrange(RIGHT, buff=0.1)
        target_equals_1 = eq_equals_cur.copy()
        target_minus1 = Text("-", color=WHITE)
        target_c1 = eq_c_cur.copy()
        target_minus_c1 = VGroup(target_minus1, target_c1).arrange(RIGHT, buff=0.1)

        target_eq_mobj_1 = VGroup(
            target_ax2_1, target_plus1_1, target_bx1, target_equals_1, target_minus_c1
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)
        
        self.play(Write(beat_title_1))
        self.wait(0.5)

        self.play(
            ReplacementTransform(current_eq_mobj[0], target_eq_mobj_1[0]),
            ReplacementTransform(current_eq_mobj[1], target_eq_mobj_1[1]),
            ReplacementTransform(current_eq_mobj[2], target_eq_mobj_1[2]),
            ReplacementTransform(current_eq_mobj[5], target_eq_mobj_1[3]),
            FadeOut(current_eq_mobj[3]), # Fade out '+' before c
            ReplacementTransform(current_eq_mobj[4], target_c1), # 'c' moves to right
            ReplacementTransform(current_eq_mobj[6], target_minus1), # '0' becomes '-'
            run_time=1.5
        )
        self.wait(0.5)
        current_eq_mobj = target_eq_mobj_1
        self.remove(beat_title_1)
        
        # --- Beat 2: Divide by 'a' ---
        # ax^2 + bx = -c  ->  x^2 + (b/a)x = -c/a
        beat_title_2 = Text("2. Divide by 'a'", font_size=35, color=GOLD_ACCENT).to_corner(UL)

        # Target 2: x^2 + (b/a)x = -c/a
        target_x2_2 = VGroup(Text("x", color=BLUE_ACCENT), create_exponent_text(Text("x"), "2", BLUE_ACCENT))
        target_plus1_2 = Text("+", color=WHITE)
        
        target_b2_num = Text("b", color=GOLD_ACCENT)
        target_a2_den = Text("a", color=GOLD_ACCENT)
        target_bx_over_a_frac = create_fraction_mobject(target_b2_num, target_a2_den, scale=0.8)
        target_x2 = Text("x", color=BLUE_ACCENT).next_to(target_bx_over_a_frac, RIGHT, buff=0.1)
        target_bx_fraction_term = VGroup(target_bx_over_a_frac, target_x2)
        target_bx_fraction_term.arrange(RIGHT, buff=0.1)
        
        target_equals_2 = Text("=", color=WHITE)
        target_minus2 = Text("-", color=WHITE)
        target_c2_num = Text("c", color=GOLD_ACCENT)
        target_a2_den_2 = Text("a", color=GOLD_ACCENT)
        target_c_over_a_frac = create_fraction_mobject(target_c2_num, target_a2_den_2, scale=0.8)
        target_minus_c_fraction_term = VGroup(target_minus2, target_c_over_a_frac).arrange(RIGHT, buff=0.1)

        target_eq_mobj_2 = VGroup(
            target_x2_2, target_plus1_2, target_bx_fraction_term, target_equals_2, target_minus_c_fraction_term
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)

        self.play(Write(beat_title_2))
        self.wait(0.5)

        self.play(
            FadeOut(current_eq_mobj[0][0]), # Fade out 'a' from ax^2
            ReplacementTransform(current_eq_mobj[0][1], target_eq_mobj_2[0][0]), # x
            ReplacementTransform(current_eq_mobj[0][2], target_eq_mobj_2[0][1]), # ^2
            ReplacementTransform(current_eq_mobj[1], target_eq_mobj_2[1]), # Plus
            ReplacementTransform(current_eq_mobj[2][0], target_bx_over_a_frac.submobjects[0]), # 'b' to numerator
            ReplacementTransform(current_eq_mobj[2][1], target_bx_fraction_term.submobjects[1]), # 'x' (right of frac)
            Create(target_bx_over_a_frac.submobjects[1]), # Fraction bar
            Create(target_bx_over_a_frac.submobjects[2]), # 'a' in denominator
            ReplacementTransform(current_eq_mobj[3], target_eq_mobj_2[3]), # '='
            ReplacementTransform(current_eq_mobj[4][0], target_minus_c_fraction_term.submobjects[0]), # '-'
            ReplacementTransform(current_eq_mobj[4][1], target_c_over_a_frac.submobjects[0]), # 'c' to numerator
            Create(target_c_over_a_frac.submobjects[1]), # Fraction bar
            Create(target_c_over_a_frac.submobjects[2]), # 'a' in denominator
            run_time=2
        )
        self.wait(0.5)
        current_eq_mobj = target_eq_mobj_2
        self.remove(beat_title_2)

        # --- Beat 3: Complete the Square (Visual Intuition) ---
        beat_title_3 = Text("3. Complete the Square", font_size=35, color=GOLD_ACCENT).to_corner(UL)
        
        # Square of side x
        square_x_side_length = 2.0
        square_x = Square(side_length=square_x_side_length, color=BLUE_ACCENT, fill_opacity=0.2)
        label_x_side = Text("x", font_size=30, color=BLUE_ACCENT).next_to(square_x.get_left(), LEFT * 0.5)
        label_x_top = Text("x", font_size=30, color=BLUE_ACCENT).next_to(square_x.get_top(), UP * 0.5)
        x_squared_vis = VGroup(square_x, label_x_side, label_x_top).shift(LEFT * 3)

        # Labels for b/2a
        b_num_vis = Text("b", color=GOLD_ACCENT, font_size=24)
        den_2a_vis = VGroup(Text("2", color=BLUE_ACCENT, font_size=24), Text("a", color=GOLD_ACCENT, font_size=24)).arrange(RIGHT, buff=0.05)
        frac_b_2a_vis = create_fraction_mobject(b_num_vis, den_2a_vis, scale=0.8)

        # Rectangles for x*(b/2a)
        rect_width_val = square_x_side_length / 2 # for visual symmetry
        
        rect1 = Rectangle(height=square_x_side_length, width=rect_width_val, color=GOLD_ACCENT, fill_opacity=0.5)
        rect1.next_to(square_x, RIGHT, buff=0)
        label_rect1 = frac_b_2a_vis.copy().next_to(rect1.get_top(), UP * 0.5)
        
        rect2 = Rectangle(height=rect_width_val, width=square_x_side_length, color=GOLD_ACCENT, fill_opacity=0.5)
        rect2.next_to(square_x, DOWN, buff=0)
        label_rect2 = frac_b_2a_vis.copy().next_to(rect2.get_left(), LEFT * 0.5)

        # Missing square for (b/2a)^2
        missing_square = Square(side_length=rect_width_val, color=WHITE, fill_opacity=0.7)
        missing_square.next_to(rect1, DOWN, buff=0)
        
        label_missing_paren_open = Text("(", color=WHITE, font_size=24)
        label_missing_paren_close = Text(")", color=WHITE, font_size=24)
        label_missing_exp2 = create_exponent_text(label_missing_paren_close, "2", BLUE_ACCENT)
        label_missing_square_frac = frac_b_2a_vis.copy()
        
        label_missing_square = VGroup(label_missing_paren_open, label_missing_square_frac, label_missing_paren_close, label_missing_exp2).arrange(RIGHT, buff=0.1)
        label_missing_exp2.next_to(label_missing_paren_close, UP + RIGHT, buff=0.05)
        label_missing_square.move_to(missing_square.get_center())

        full_square_elements = VGroup(x_squared_vis, rect1, label_rect1, rect2, label_rect2, missing_square, label_missing_square).center()
        
        self.play(FadeOut(current_eq_mobj.copy()), run_time=0.5) # Temporarily remove equation copy
        
        self.play(Write(beat_title_3))
        self.wait(0.5)

        self.play(Create(x_squared_vis))
        self.wait(0.5)
        self.play(
            Create(rect1), Write(label_rect1),
            Create(rect2), Write(label_rect2)
        )
        self.wait(1)
        self.play(
            FadeIn(missing_square, shift=UP),
            Write(label_missing_square)
        )
        self.wait(1.5)
        
        self.play(FadeOut(full_square_elements, shift=DOWN), run_time=1.0)
        self.remove(beat_title_3)
        self.add(current_eq_mobj) # Restore current equation

        # Back to equations: (x + b/2a)^2 = (b/2a)^2 - c/a
        # Target 3
        # Left side: (x + b/2a)^2
        open_paren_L3 = Text("(", color=WHITE)
        x_L3 = Text("x", color=BLUE_ACCENT)
        plus_L3 = Text("+", color=WHITE)
        b_L3_num = Text("b", color=GOLD_ACCENT)
        b_L3_den_2a = VGroup(Text("2", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        frac_b_2a_L3 = create_fraction_mobject(b_L3_num, b_L3_den_2a, scale=0.8)
        close_paren_L3 = Text(")", color=WHITE)
        exp2_L3 = create_exponent_text(close_paren_L3, "2", BLUE_ACCENT)
        
        LHS_L3 = VGroup(open_paren_L3, x_L3, plus_L3, frac_b_2a_L3, close_paren_L3)
        LHS_L3.arrange(RIGHT, buff=0.1)
        exp2_L3.next_to(close_paren_L3, UP + RIGHT, buff=0.05)
        LHS_L3 = VGroup(LHS_L3, exp2_L3) # Group the exponent properly

        # Right side: (b/2a)^2 - c/a
        equals_L3 = Text("=", color=WHITE)
        open_paren_R3 = Text("(", color=WHITE)
        b_R3_num = Text("b", color=GOLD_ACCENT)
        b_R3_den_2a = VGroup(Text("2", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        frac_b_2a_R3 = create_fraction_mobject(b_R3_num, b_R3_den_2a, scale=0.8)
        close_paren_R3 = Text(")", color=WHITE)
        exp2_R3 = create_exponent_text(close_paren_R3, "2", BLUE_ACCENT)
        
        minus_L3_term = Text("-", color=WHITE)
        c_L3_num = Text("c", color=GOLD_ACCENT)
        a_L3_den = Text("a", color=GOLD_ACCENT)
        frac_c_a_L3 = create_fraction_mobject(c_L3_num, a_L3_den, scale=0.8)
        
        RHS_first_term_L3 = VGroup(open_paren_R3, frac_b_2a_R3, close_paren_R3)
        RHS_first_term_L3.arrange(RIGHT, buff=0.1)
        exp2_R3.next_to(close_paren_R3, UP + RIGHT, buff=0.05)
        RHS_first_term_L3 = VGroup(RHS_first_term_L3, exp2_R3)

        RHS_L3 = VGroup(RHS_first_term_L3, minus_L3_term, frac_c_a_L3).arrange(RIGHT, buff=0.2)

        target_eq_mobj_3_initial = VGroup(LHS_L3, equals_L3, RHS_L3).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)
        
        # Animate adding (b/2a)^2 to both sides
        plus_rhs_vis = Text("+", color=WHITE)
        added_term_rhs_vis = RHS_first_term_L3.copy()
        
        current_eq_mobj.to_edge(UP, buff=0.5).scale(0.9)
        self.play(
            FadeIn(plus_rhs_vis.next_to(current_eq_mobj[4], LEFT, buff=0.1)),
            FadeIn(added_term_rhs_vis.next_to(current_eq_mobj[4], RIGHT, buff=0.2)),
            run_time=1
        )
        self.wait(0.5)

        # Transform to (x + b/2a)^2 = (b/2a)^2 - c/a
        self.play(
            FadeOut(current_eq_mobj[0]), # x^2
            FadeOut(current_eq_mobj[1]), # +
            FadeOut(current_eq_mobj[2]), # (b/a)x
            FadeOut(plus_rhs_vis), # Added + on RHS
            
            FadeIn(LHS_L3[0][0]), # '('
            ReplacementTransform(current_eq_mobj[0][0], LHS_L3[0][1]), # 'x'
            FadeIn(LHS_L3[0][2]), # '+'
            ReplacementTransform(current_eq_mobj[2][0], LHS_L3[0][3].submobjects[0]), # 'b' to b/2a num
            Create(LHS_L3[0][3].submobjects[1]), # b/2a frac bar
            Create(LHS_L3[0][3].submobjects[2]), # b/2a den
            FadeIn(LHS_L3[0][4]), # ')'
            FadeIn(LHS_L3[1]), # '^2'
            
            ReplacementTransform(current_eq_mobj[3], target_eq_mobj_3_initial[1]), # '='
            ReplacementTransform(added_term_rhs_vis, RHS_L3.submobjects[0]), # Added term becomes (b/2a)^2
            ReplacementTransform(current_eq_mobj[4][0], RHS_L3.submobjects[1]), # '-'
            ReplacementTransform(current_eq_mobj[4][1], RHS_L3.submobjects[2]), # 'c/a'
            run_time=2.5
        )
        self.wait(0.5)
        current_eq_mobj = target_eq_mobj_3_initial
        
        # Simplification of RHS: (b/2a)^2 - c/a -> b^2/(4a^2) - 4ac/(4a^2)
        target_b2_4a2_num = VGroup(Text("b", color=GOLD_ACCENT), create_exponent_text(Text("b"), "2", GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        target_b2_4a2_den = VGroup(Text("4", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT), create_exponent_text(Text("a"), "2", GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        frac_b2_4a2 = create_fraction_mobject(target_b2_4a2_num, target_b2_4a2_den, scale=0.8)

        target_minus_mid = Text("-", color=WHITE)

        target_4ac_num = VGroup(Text("4", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT), Text("c", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)
        target_4a2_den_mid = VGroup(Text("4", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT), create_exponent_text(Text("a"), "2", GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        frac_4ac_4a2 = create_fraction_mobject(target_4ac_num, target_4a2_den_mid, scale=0.8)

        rhs_simplified_group = VGroup(frac_b2_4a2, target_minus_mid, frac_4ac_4a2).arrange(RIGHT, buff=0.2)
        target_eq_mobj_3_simplified = VGroup(LHS_L3.copy(), equals_L3.copy(), rhs_simplified_group).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)
        
        self.play(
            ReplacementTransform(current_eq_mobj[2].submobjects[0], frac_b2_4a2), # (b/2a)^2 -> b^2/4a^2
            ReplacementTransform(current_eq_mobj[2].submobjects[1], target_minus_mid), # - -> -
            ReplacementTransform(current_eq_mobj[2].submobjects[2], frac_4ac_4a2), # c/a -> 4ac/4a^2
            run_time=1.5
        )
        self.wait(0.5)
        current_eq_mobj = target_eq_mobj_3_simplified
        
        # Combine fractions on RHS: b^2/(4a^2) - 4ac/(4a^2) -> (b^2 - 4ac) / (4a^2)
        target_combined_num = VGroup(
            Text("b", color=GOLD_ACCENT), create_exponent_text(Text("b"), "2", GOLD_ACCENT),
            Text("-", color=WHITE),
            Text("4", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT), Text("c", color=GOLD_ACCENT)
        ).arrange(RIGHT, buff=0.1)
        target_combined_den = VGroup(Text("4", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT), create_exponent_text(Text("a"), "2", GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        
        frac_combined_rhs = create_fraction_mobject(target_combined_num, target_combined_den, scale=0.8)
        
        target_eq_mobj_3_combined = VGroup(LHS_L3.copy(), equals_L3.copy(), frac_combined_rhs).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)

        self.play(
            ReplacementTransform(current_eq_mobj[2].submobjects[0], frac_combined_rhs), # Transform two fractions into one
            FadeOut(current_eq_mobj[2].submobjects[1]), # Fade out '-'
            FadeOut(current_eq_mobj[2].submobjects[2]), # Fade out 4ac/4a^2
            run_time=1.5
        )
        self.wait(0.5)
        current_eq_mobj = target_eq_mobj_3_combined
        
        # --- Beat 4: Take Square Root ---
        # (x + b/2a)^2 = (b^2 - 4ac) / (4a^2) -> x + b/2a = ±sqrt(b^2 - 4ac) / (2a)
        beat_title_4 = Text("4. Take Square Root", font_size=35, color=GOLD_ACCENT).to_corner(UL)
        
        # Target 4: x + b/2a = ±sqrt(b^2 - 4ac) / (2a)
        x_L4 = Text("x", color=BLUE_ACCENT)
        plus_L4 = Text("+", color=WHITE)
        b_L4_num = Text("b", color=GOLD_ACCENT)
        b_L4_den_2a = VGroup(Text("2", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        frac_b_2a_L4 = create_fraction_mobject(b_L4_num, b_L4_den_2a, scale=0.8)
        LHS_L4 = VGroup(x_L4, plus_L4, frac_b_2a_L4).arrange(RIGHT, buff=0.2)
        
        equals_L4 = Text("=", color=WHITE)
        pm_L4 = Text("±", color=WHITE) # Use unicode character if possible, otherwise Text("+/-")
        
        sqrt_expr_num = VGroup(
            Text("b", color=GOLD_ACCENT), create_exponent_text(Text("b"), "2", GOLD_ACCENT),
            Text("-", color=WHITE),
            Text("4", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT), Text("c", color=GOLD_ACCENT)
        ).arrange(RIGHT, buff=0.1)
        sqrt_num_mobj = create_sqrt_mobject(sqrt_expr_num, scale=0.8)
        
        den_L4 = VGroup(Text("2", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)
        
        RHS_L4 = VGroup(pm_L4, create_fraction_mobject(sqrt_num_mobj, den_L4)).arrange(RIGHT, buff=0.1)
        
        target_eq_mobj_4 = VGroup(LHS_L4, equals_L4, RHS_L4).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)

        self.play(Write(beat_title_4))
        self.wait(0.5)
        
        self.play(
            FadeOut(current_eq_mobj[0].submobjects[0]), # '(' group
            FadeOut(current_eq_mobj[0].submobjects[4]), # ')'
            FadeOut(current_eq_mobj[0].submobjects[5]), # '^2'
            ReplacementTransform(current_eq_mobj[0].submobjects[1], x_L4), # 'x'
            ReplacementTransform(current_eq_mobj[0].submobjects[2], plus_L4), # '+'
            ReplacementTransform(current_eq_mobj[0].submobjects[3], frac_b_2a_L4), # 'b/2a'
            
            ReplacementTransform(current_eq_mobj[1], equals_L4), # '='
            Create(pm_L4.next_to(equals_L4, RIGHT, buff=0.1)), # Create '±'
            
            # RHS: take square root of numerator and denominator
            Create(sqrt_num_mobj.submobjects[0]), # Create sqrt symbol
            ReplacementTransform(current_eq_mobj[2].submobjects[0].submobjects[0], sqrt_num_mobj.submobjects[1]), # Num content into sqrt
            ReplacementTransform(current_eq_mobj[2].submobjects[2].submobjects[0], den_L4.submobjects[0]), # '4' to '2'
            FadeOut(current_eq_mobj[2].submobjects[2].submobjects[1]), # Fade out 'a^2' exponent
            ReplacementTransform(current_eq_mobj[2].submobjects[2].submobjects[1].submobjects[0], den_L4.submobjects[1]), # 'a'
            run_time=2.5
        )
        self.wait(0.5)
        current_eq_mobj = target_eq_mobj_4
        self.remove(beat_title_4)
        
        # --- Beat 5: Isolate 'x' ---
        # x + b/2a = ±sqrt(b^2 - 4ac) / (2a) -> x = [-b ± sqrt(b^2 - 4ac)] / (2a)
        beat_title_5 = Text("5. Isolate 'x'", font_size=35, color=GOLD_ACCENT).to_corner(UL)
        
        # Target 5: x = (-b ± sqrt(b^2 - 4ac)) / (2a)
        final_x_L5 = Text("x", color=BLUE_ACCENT)
        final_equals_L5 = Text("=", color=WHITE)
        
        final_minus_b = Text("-", color=WHITE)
        final_b = Text("b", color=GOLD_ACCENT)
        final_pm = Text("±", color=WHITE)
        
        final_sqrt_expr = VGroup(
            Text("b", color=GOLD_ACCENT), create_exponent_text(Text("b"), "2", GOLD_ACCENT),
            Text("-", color=WHITE),
            Text("4", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT), Text("c", color=GOLD_ACCENT)
        ).arrange(RIGHT, buff=0.1)
        final_sqrt_mobj = create_sqrt_mobject(final_sqrt_expr, scale=0.8)

        final_num = VGroup(final_minus_b, final_b, final_pm, final_sqrt_mobj).arrange(RIGHT, buff=0.1)
        final_den = VGroup(Text("2", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)
        
        final_fraction = create_fraction_mobject(final_num, final_den, scale=0.8)
        
        target_eq_mobj_5 = VGroup(final_x_L5, final_equals_L5, final_fraction).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.0)

        self.play(Write(beat_title_5))
        self.wait(0.5)

        self.play(
            ReplacementTransform(current_eq_mobj[0].submobjects[0], final_x_L5), # 'x' stays
            FadeOut(current_eq_mobj[0].submobjects[1]), # '+'
            FadeOut(current_eq_mobj[0].submobjects[2]), # 'b/2a'
            
            ReplacementTransform(current_eq_mobj[1], final_equals_L5), # '='
            
            # RHS: move -b/2a from left, combine with existing RHS fraction
            # This is complex, will transform the whole RHS structure.
            ReplacementTransform(current_eq_mobj[2].submobjects[0], final_pm), # '±'
            ReplacementTransform(current_eq_mobj[2].submobjects[1].submobjects[0], final_sqrt_mobj), # Sqrt expression
            ReplacementTransform(current_eq_mobj[2].submobjects[1].submobjects[2], final_den), # Denominator '2a'
            Create(final_minus_b.next_to(final_b, LEFT, buff=0.1)), # Add '-b' to numerator
            Create(final_fraction.submobjects[1]), # Create new fraction bar
            run_time=2.5
        )
        self.wait(1)
        current_eq_mobj = target_eq_mobj_5
        self.remove(beat_title_5)

        # --- Final Recap Card ---
        self.play(FadeOut(current_eq_mobj))
        
        recap_title = Text("Quadratic Formula", font_size=40, color=GOLD_ACCENT).to_edge(UP, buff=0.8)
        
        final_formula_display = target_eq_mobj_5.copy()
        final_formula_display.center().scale(1.2)
        
        recap_points = VGroup(
            Text("1. Isolate 'c'", font_size=30, color=BLUE_ACCENT),
            Text("2. Divide by 'a'", font_size=30, color=BLUE_ACCENT),
            Text("3. Complete the Square", font_size=30, color=BLUE_ACCENT),
            Text("4. Take Square Root", font_size=30, color=BLUE_ACCENT),
            Text("5. Isolate 'x'", font_size=30, color=BLUE_ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(final_formula_display, DOWN, buff=1.0)

        self.play(Write(recap_title))
        self.play(FadeIn(final_formula_display))
        self.play(LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.5), run_time=3)
        self.wait(3)
        self.play(FadeOut(recap_title, final_formula_display, recap_points))