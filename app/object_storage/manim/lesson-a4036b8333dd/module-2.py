from manim import *

# Custom Colors for 3Blue1Brown style
BLUE_ACCENT = '#52C7F2'
GOLD_ACCENT = '#F4D03F'
WHITE_TEXT = '#FFFFFF'
GREY_TEXT = '#808080'

class CompletingTheSquareDerivation(Scene):
    def construct(self):
        self.camera.background_color = BLACK # Ensure true black background

        # --- Helper Functions for No-Tex Math ---
        # Helper for superscripts (e.g., x^2)
        def create_superscript(base_mobject, super_text_str, base_color=BLUE_ACCENT, super_color=BLUE_ACCENT, base_scale=1.0, super_scale=0.6):
            # If base_mobject is a string, convert to Text Mobject
            if isinstance(base_mobject, str):
                base_mobject = Text(base_mobject, color=base_color, font_size=base_scale * 48)
            
            sup = Text(super_text_str, color=super_color, font_size=super_scale * 48)
            sup.next_to(base_mobject, UP + RIGHT * 0.5, buff=0.05)
            return VGroup(base_mobject, sup)

        # Helper for fractions (e.g., b/a)
        def create_fraction(numerator_mobject, denominator_mobject, color=WHITE_TEXT, line_width=2, buff=0.15):
            frac_line = Line(LEFT, RIGHT, color=color, stroke_width=line_width)
            
            # Set width based on wider mobject, plus some padding
            frac_line.set_width(max(numerator_mobject.width, denominator_mobject.width) + 0.2)
            
            numerator_mobject.next_to(frac_line, UP, buff=buff)
            denominator_mobject.next_to(frac_line, DOWN, buff=buff)
            
            return VGroup(numerator_mobject, frac_line, denominator_mobject)

        # Helper for square root symbol (as a VGroup of Lines)
        def create_sqrt_symbol(mobject_to_root, color=WHITE_TEXT, stroke_width=2, buff_x=0.05, buff_y=0.1):
            # Calculate positions relative to the mobject_to_root
            content_left = mobject_to_root.get_left()[0]
            content_right = mobject_to_root.get_right()[0]
            content_top = mobject_to_root.get_top()[1]
            content_bottom = mobject_to_root.get_bottom()[1]

            # Start point for the root's checkmark
            v_start = [content_left - buff_x - 0.2, content_bottom - 0.1, 0]
            v_mid = [content_left - buff_x - 0.1, content_bottom - 0.3, 0]
            v_peak = [content_left - buff_x, content_bottom + 0.05, 0] # Peak of the checkmark
            
            # The top horizontal line needs to span the content
            bar_start = v_peak
            bar_end = [content_right + buff_x, content_top + buff_y, 0]

            # Ensure bar_start is aligned with the peak and slightly above content
            bar_start[1] = content_top + buff_y
            v_peak[1] = content_top + buff_y # Align peak with bar start height

            # Lines for the symbol
            l1 = Line(v_start, v_mid, color=color, stroke_width=stroke_width)
            l2 = Line(v_mid, v_peak, color=color, stroke_width=stroke_width)
            l3 = Line(bar_start, bar_end, color=color, stroke_width=stroke_width) # Top horizontal bar

            symbol = VGroup(l1, l2, l3)
            
            # Adjust the symbol's height and position to nicely wrap the content
            symbol_height = symbol.get_height()
            content_height = mobject_to_root.get_height()
            
            if symbol_height < content_height * 1.1:
                symbol.stretch_to_fit_height(content_height * 1.1)

            # Re-align for best visual
            symbol.align_to(mobject_to_root, UP)
            symbol.shift(UP * buff_y)
            symbol.align_to(mobject_to_root, LEFT)
            symbol.shift(LEFT * (symbol.get_width() * 0.7 + buff_x))
            
            return VGroup(symbol, mobject_to_root)


        # --- BEAT 1: The Square & Completing It ---
        title1 = Text("Deriving: Completing the Square", color=WHITE_TEXT, font_size=60).to_edge(UP)
        self.play(Write(title1))
        self.wait(0.5)

        # 1. Visual Hook: x^2 square
        plane = NumberPlane(
            x_range=(-2, 5, 1), y_range=(-2, 5, 1),
            x_length=7, y_length=7,
            background_line_style={"stroke_opacity": 0.4, "stroke_color": GREY_TEXT},
            axis_config={"stroke_opacity": 0.6, "stroke_color": GREY_TEXT}
        ).shift(DOWN * 0.5)
        
        self.play(Create(plane), run_time=1.5)

        x_val = 2.5 # A chosen value for x
        x_square = Square(side_length=x_val, color=BLUE_ACCENT, fill_opacity=0.6).align_to(plane.get_origin(), DL)
        
        x_label_bottom = Text("x", color=BLUE_ACCENT).next_to(x_square.get_bottom(), DOWN*0.5)
        x_label_left = Text("x", color=BLUE_ACCENT).next_to(x_square.get_left(), LEFT*0.5)
        
        x_squared_vis_text = create_superscript("x", "2", base_color=BLUE_ACCENT).move_to(x_square.get_center())

        self.play(
            GrowFromPoint(x_square, x_square.get_corner(DL)), 
            Write(x_label_bottom), 
            Write(x_label_left), 
            run_time=1.5
        )
        self.play(Write(x_squared_vis_text), run_time=1)
        self.wait(0.5)

        # 2. Adding bx rectangles
        b_val = 2 # So b/2 = 1. Used for visual size.
        
        # Two rectangles: x * (b/2)
        rect_b_half_x_top = Rectangle(width=x_val, height=b_val/2, color=GOLD_ACCENT, fill_opacity=0.6)
        rect_b_half_x_top.next_to(x_square, UP, buff=0).align_to(x_square, LEFT)
        
        rect_b_half_x_right = Rectangle(width=b_val/2, height=x_val, color=GOLD_ACCENT, fill_opacity=0.6)
        rect_b_half_x_right.next_to(x_square, RIGHT, buff=0).align_to(x_square, DOWN)
        
        b_over_2_label_horiz = create_fraction(Text("b", color=GOLD_ACCENT), Text("2", color=GOLD_ACCENT)).next_to(rect_b_half_x_right.get_right(), RIGHT*0.5)
        b_over_2_label_vert = create_fraction(Text("b", color=GOLD_ACCENT), Text("2", color=GOLD_ACCENT)).next_to(rect_b_half_x_top.get_top(), UP*0.5)

        eq_x_sq_plus_bx_parts = [
            x_squared_vis_text.copy(), 
            Text("+", color=WHITE_TEXT).scale(0.8), 
            Text("bx", color=GOLD_ACCENT).scale(0.8)
        ]
        eq_x_sq_plus_bx = VGroup(*eq_x_sq_plus_bx_parts).arrange(RIGHT, buff=0.1).shift(UP*2.5 + RIGHT*2)

        self.play(
            GrowFromPoint(rect_b_half_x_top, rect_b_half_x_top.get_corner(DL)), 
            GrowFromPoint(rect_b_half_x_right, rect_b_half_x_right.get_corner(DL)),
            Write(b_over_2_label_horiz),
            Write(b_over_2_label_vert),
            ReplacementTransform(x_squared_vis_text, eq_x_sq_plus_bx[0]),
            Write(VGroup(*eq_x_sq_plus_bx_parts[1:])),
            run_time=2
        )
        self.wait(0.5)

        # 3. Missing piece (b/2)^2
        b_half_square_fill = Square(side_length=b_val/2, color=BLUE_ACCENT, fill_opacity=0.4, stroke_color=GOLD_ACCENT, stroke_width=3)
        b_half_square_fill.next_to(rect_b_half_x_top, RIGHT, buff=0).align_to(rect_b_half_x_right, UP)
        
        # Text for (b/2)^2
        b_over_2_text = create_fraction(Text("b", color=BLUE_ACCENT), Text("2", color=BLUE_ACCENT))
        b_half_squared_term = create_superscript(VGroup(Text("(", color=BLUE_ACCENT), b_over_2_text, Text(")", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05), "2", base_color=BLUE_ACCENT)
        plus_b_half_squared = VGroup(Text("+", color=WHITE_TEXT).scale(0.8), b_half_squared_term.scale(0.8)).arrange(RIGHT, buff=0.1)
        plus_b_half_squared.next_to(eq_x_sq_plus_bx[-1], RIGHT, buff=0.1)

        self.play(
            GrowFromPoint(b_half_square_fill, b_half_square_fill.get_corner(DL)), 
            FadeIn(plus_b_half_squared)
        )
        self.wait(0.5)

        # 4. Completed Square and equation
        equals_text = Text("=", color=WHITE_TEXT).scale(0.8).next_to(plus_b_half_squared, RIGHT, buff=0.1)
        
        x_plus_b_half_core = VGroup(
            Text("x", color=BLUE_ACCENT),
            Text("+", color=WHITE_TEXT),
            create_fraction(Text("b", color=GOLD_ACCENT), Text("2", color=GOLD_ACCENT))
        ).arrange(RIGHT, buff=0.1)
        x_plus_b_half_paren = VGroup(Text("(", color=BLUE_ACCENT), x_plus_b_half_core, Text(")", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
        
        completed_square_math_text = create_superscript(x_plus_b_half_paren.scale(0.8), "2", base_color=BLUE_ACCENT)
        completed_square_math_text.next_to(equals_text, RIGHT, buff=0.1)
        
        full_equation_beat1 = VGroup(
            eq_x_sq_plus_bx, plus_b_half_squared, equals_text, completed_square_math_text
        ).arrange(RIGHT, buff=0.1).center().to_edge(DOWN*0.5)
        
        self.play(Write(equals_text), Write(completed_square_math_text), run_time=1.5)
        self.wait(0.5)

        # Reposition the formed equation
        self.play(
            VGroup(eq_x_sq_plus_bx[0], eq_x_sq_plus_bx[1:], plus_b_half_squared, equals_text, completed_square_math_text).animate.arrange(RIGHT, buff=0.1).center().to_edge(DOWN*0.5),
            run_time=1.5
        )
        current_equation_beat1 = VGroup(eq_x_sq_plus_bx[0], eq_x_sq_plus_bx[1:], plus_b_half_squared, equals_text, completed_square_math_text)
        self.wait(2)

        # Clean up Beat 1 for Beat 2
        self.play(
            FadeOut(plane, x_square, rect_b_half_x_top, rect_b_half_x_right, b_half_square_fill, 
                    x_label_bottom, x_label_left, b_over_2_label_horiz, b_over_2_label_vert),
            FadeOut(title1),
            FadeOut(current_equation_beat1)
        )
        self.wait(0.5)

        # --- BEAT 2: Applying to x^2 + bx + c = 0 ---
        title2 = Text("Normalizing & Completing", color=WHITE_TEXT, font_size=60).to_edge(UP)
        self.play(FadeIn(title2))

        # 1. Initial Equation: x^2 + bx + c = 0
        x_sq_beat2 = create_superscript("x", "2", base_color=BLUE_ACCENT)
        plus1_beat2 = Text("+", color=WHITE_TEXT)
        bx_beat2 = Text("bx", color=GOLD_ACCENT)
        plus2_beat2 = Text("+", color=WHITE_TEXT)
        c_beat2 = Text("c", color=BLUE_ACCENT)
        eq_beat2 = Text("=", color=WHITE_TEXT)
        zero_beat2 = Text("0", color=BLUE_ACCENT)

        initial_equation = VGroup(x_sq_beat2, plus1_beat2, bx_beat2, plus2_beat2, c_beat2, eq_beat2, zero_beat2).arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        
        self.play(Write(initial_equation), run_time=1.5)
        self.wait(0.5)

        # 2. Isolate x terms: x^2 + bx = -c
        minus_c_target = Text("-c", color=BLUE_ACCENT).next_to(eq_beat2, RIGHT, buff=0.2)
        
        self.play(
            FadeOut(plus2_beat2),
            Transform(c_beat2, minus_c_target),
            FadeOut(zero_beat2),
            initial_equation.animate.arrange(RIGHT, buff=0.2).move_to(UP*1.5), # Reposition existing parts
            run_time=1.5
        )
        current_equation_mobj = VGroup(x_sq_beat2, plus1_beat2, bx_beat2, eq_beat2, minus_c_target)
        self.wait(0.5)

        # 3. Complete the Square: Add (b/2)^2 to both sides
        b_over_2_text_gold = create_fraction(Text("b", color=GOLD_ACCENT), Text("2", color=GOLD_ACCENT))
        b_half_squared_term_gold = create_superscript(VGroup(Text("(", color=GOLD_ACCENT), b_over_2_text_gold, Text(")", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05), "2", base_color=GOLD_ACCENT)
        
        plus_b_half_sq_left = VGroup(Text("+", color=WHITE_TEXT), b_half_squared_term_gold.copy()).arrange(RIGHT, buff=0.1)
        plus_b_half_sq_right = VGroup(Text("+", color=WHITE_TEXT), b_half_squared_term_gold.copy()).arrange(RIGHT, buff=0.05)

        plus_b_half_sq_left.next_to(bx_beat2, RIGHT, buff=0.2)
        plus_b_half_sq_right.next_to(minus_c_target, RIGHT, buff=0.2)

        self.play(
            FadeIn(plus_b_half_sq_left, shift=UP*0.5), 
            FadeIn(plus_b_half_sq_right, shift=UP*0.5),
            run_time=1
        )
        current_equation_mobj = VGroup(x_sq_beat2, plus1_beat2, bx_beat2, plus_b_half_sq_left, eq_beat2, minus_c_target, plus_b_half_sq_right)
        self.wait(0.5)

        # 4. Factor Left Side: (x + b/2)^2 = -c + (b/2)^2
        factored_left_core = VGroup(
            Text("x", color=BLUE_ACCENT),
            Text("+", color=WHITE_TEXT),
            b_over_2_text_gold.copy()
        ).arrange(RIGHT, buff=0.1)
        
        factored_left_paren = VGroup(Text("(", color=BLUE_ACCENT), factored_left_core, Text(")", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
        factored_left_squared = create_superscript(factored_left_paren, "2", base_color=BLUE_ACCENT)
        factored_left_squared.move_to(VGroup(x_sq_beat2, plus1_beat2, bx_beat2, plus_b_half_sq_left).get_center())

        right_side_current = VGroup(minus_c_target, plus_b_half_sq_right)
        
        self.play(
            FadeTransform(VGroup(x_sq_beat2, plus1_beat2, bx_beat2, plus_b_half_sq_left), factored_left_squared),
            run_time=1.5
        )
        current_equation_mobj = VGroup(factored_left_squared, eq_beat2, right_side_current)
        self.wait(0.5)

        # 5. Take Square Root
        pm_symbol = Text("±", color=WHITE_TEXT).scale(0.9)
        
        right_side_for_sqrt = right_side_current.copy().arrange(RIGHT, buff=0.1)
        
        sqrt_of_right_side = create_sqrt_symbol(right_side_for_sqrt)
        
        left_side_no_square = factored_left_paren.copy().move_to(factored_left_squared.get_center())
        
        self.play(
            Transform(factored_left_squared, left_side_no_square),
            FadeIn(pm_symbol.next_to(eq_beat2, RIGHT, buff=0.1)),
            FadeTransform(right_side_current, sqrt_of_right_side),
            run_time=2
        )
        current_equation_mobj = VGroup(left_side_no_square, eq_beat2, pm_symbol, sqrt_of_right_side)
        self.wait(0.5)

        # 6. Isolate x
        minus_b_half_moved = VGroup(Text("-", color=WHITE_TEXT), b_over_2_text_gold.copy()).arrange(RIGHT, buff=0.1)
        
        x_only = Text("x", color=BLUE_ACCENT)
        equals_again = Text("=", color=WHITE_TEXT)

        # Animate moving b/2 to the right side
        self.play(
            FadeTransform(VGroup(left_side_no_square[0], left_side_no_square[2], left_side_no_square[3]), VGroup(x_only.copy().move_to(left_side_no_square[1].get_center()), equals_again.copy().next_to(x_only, RIGHT, buff=0.2))),
            Transform(left_side_no_square[1], x_only), # The 'x' part stays
            # eq_beat2 already positioned by pm_symbol
            pm_symbol.animate.next_to(minus_b_half_moved, RIGHT, buff=0.1),
            minus_b_half_moved.next_to(equals_again, RIGHT, buff=0.2),
            sqrt_of_right_side.animate.next_to(pm_symbol, RIGHT, buff=0.1),
            run_time=2
        )
        current_equation_mobj = VGroup(x_only, equals_again, minus_b_half_moved, pm_symbol, sqrt_of_right_side).center().to_edge(DOWN)
        self.wait(1)

        self.play(FadeOut(title2, current_equation_mobj))
        self.wait(0.5)
        
        # --- BEAT 3: Handling the 'a' coefficient ---
        title3 = Text("General Form: ax² + bx + c = 0", color=WHITE_TEXT, font_size=60).to_edge(UP)
        self.play(FadeIn(title3))

        # 1. General Equation: ax^2 + bx + c = 0
        a_beat3 = Text("a", color=GOLD_ACCENT)
        x_sq_beat3 = create_superscript("x", "2", base_color=BLUE_ACCENT)
        plus1_beat3 = Text("+", color=WHITE_TEXT)
        bx_beat3 = Text("bx", color=GOLD_ACCENT)
        plus2_beat3 = Text("+", color=WHITE_TEXT)
        c_beat3 = Text("c", color=BLUE_ACCENT)
        eq_beat3 = Text("=", color=WHITE_TEXT)
        zero_beat3 = Text("0", color=BLUE_ACCENT)
        
        initial_equation_general = VGroup(a_beat3, x_sq_beat3, plus1_beat3, bx_beat3, plus2_beat3, c_beat3, eq_beat3, zero_beat3).arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        
        self.play(Write(initial_equation_general), run_time=1.5)
        self.wait(0.5)

        # 2. Divide by 'a'
        divide_by_a_label = Text("Divide by 'a'", color=GREY_TEXT).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(divide_by_a_label))

        # Create new terms after division
        x_sq_div_a = create_superscript("x", "2", base_color=BLUE_ACCENT) # a/a = 1
        b_over_a_x = VGroup(create_fraction(Text("b", color=GOLD_ACCENT), Text("a", color=GOLD_ACCENT)), Text("x", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
        c_over_a = create_fraction(Text("c", color=BLUE_ACCENT), Text("a", color=GOLD_ACCENT))

        new_equation_div_a = VGroup(x_sq_div_a, plus1_beat3.copy(), b_over_a_x, plus2_beat3.copy(), c_over_a, eq_beat3.copy(), zero_beat3.copy()).arrange(RIGHT, buff=0.2).move_to(initial_equation_general.get_center())
        
        self.play(
            ReplacementTransform(initial_equation_general, new_equation_div_a),
            FadeOut(divide_by_a_label)
        )
        current_eq_mobj_beat3 = new_equation_div_a
        self.wait(1)

        # 3. Isolate x terms: x^2 + (b/a)x = -c/a
        minus_c_over_a = VGroup(Text("-", color=WHITE_TEXT), c_over_a.copy()).arrange(RIGHT, buff=0.05)
        
        isolated_x_eq = VGroup(x_sq_div_a.copy(), plus1_beat3.copy(), b_over_a_x.copy(), eq_beat3.copy(), minus_c_over_a).arrange(RIGHT, buff=0.2).move_to(current_eq_mobj_beat3.get_center())

        self.play(
            FadeTransform(current_eq_mobj_beat3, isolated_x_eq)
        )
        current_eq_mobj_beat3 = isolated_x_eq
        self.wait(1)

        # 4. Identify new b and add (b/(2a))^2 to both sides
        b_over_2a_frac = create_fraction(Text("b", color=GOLD_ACCENT), VGroup(Text("2", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05))
        b_over_2a_paren = VGroup(Text("(", color=GOLD_ACCENT), b_over_2a_frac, Text(")", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        b_over_2a_squared = create_superscript(b_over_2a_paren, "2", base_color=GOLD_ACCENT, super_color=GOLD_ACCENT)
        
        plus_b_over_2a_sq_left = VGroup(Text("+", color=WHITE_TEXT), b_over_2a_squared.copy()).arrange(RIGHT, buff=0.05)
        plus_b_over_2a_sq_right = VGroup(Text("+", color=WHITE_TEXT), b_over_2a_squared.copy()).arrange(RIGHT, buff=0.05)

        plus_b_over_2a_sq_left.next_to(b_over_a_x, RIGHT, buff=0.2)
        plus_b_over_2a_sq_right.next_to(minus_c_over_a, RIGHT, buff=0.2)
        
        self.play(
            FadeIn(plus_b_over_2a_sq_left, shift=UP*0.5),
            FadeIn(plus_b_over_2a_sq_right, shift=UP*0.5),
        )
        current_eq_mobj_beat3 = VGroup(x_sq_div_a, plus1_beat3, b_over_a_x, plus_b_over_2a_sq_left, eq_beat3, minus_c_over_a, plus_b_over_2a_sq_right)
        self.wait(1)

        # 5. Complete the Square: (x + b/(2a))^2 = -c/a + (b/(2a))^2
        factored_left_general_core = VGroup(
            Text("x", color=BLUE_ACCENT),
            Text("+", color=WHITE_TEXT),
            b_over_2a_frac.copy()
        ).arrange(RIGHT, buff=0.1)
        
        factored_left_general_paren = VGroup(Text("(", color=BLUE_ACCENT), factored_left_general_core, Text(")", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
        factored_left_general_squared = create_superscript(factored_left_general_paren, "2", base_color=BLUE_ACCENT)
        factored_left_general_squared.move_to(VGroup(x_sq_div_a, plus1_beat3, b_over_a_x, plus_b_over_2a_sq_left).get_center())

        right_side_current_beat3 = VGroup(minus_c_over_a, plus_b_over_2a_sq_right)
        
        self.play(
            FadeTransform(VGroup(x_sq_div_a, plus1_beat3, b_over_a_x, plus_b_over_2a_sq_left), factored_left_general_squared),
            current_eq_mobj_beat3.animate.shift(LEFT * 0.5)
        )
        current_eq_mobj_beat3 = VGroup(factored_left_general_squared, eq_beat3, right_side_current_beat3)
        self.wait(1)

        self.play(FadeOut(title3, current_eq_mobj_beat3))
        self.wait(0.5)

        # --- BEAT 4: Finalizing the Quadratic Formula ---
        title4 = Text("Deriving the Formula", color=WHITE_TEXT, font_size=60).to_edge(UP)
        self.play(FadeIn(title4))

        # Start with the result from Beat 3
        # (x + b/(2a))^2 = -c/a + (b/(2a))^2
        factored_left_general_squared_final = factored_left_general_squared.copy().to_edge(LEFT).shift(UP*1.5)
        eq_final = eq_beat3.copy().next_to(factored_left_general_squared_final, RIGHT, buff=0.2)
        
        minus_c_over_a_final = minus_c_over_a.copy()
        plus_b_over_2a_sq_right_final = plus_b_over_2a_sq_right.copy()
        
        right_side_final_initial = VGroup(minus_c_over_a_final, plus_b_over_2a_sq_right_final).arrange(RIGHT, buff=0.1).next_to(eq_final, RIGHT, buff=0.2)
        
        self.play(FadeIn(factored_left_general_squared_final), FadeIn(eq_final), FadeIn(right_side_final_initial))
        current_equation_final_step = VGroup(factored_left_general_squared_final, eq_final, right_side_final_initial)
        self.wait(1)

        # 2a. Expand (b/(2a))^2 to b^2 / (4a^2)
        b_sq_over_4a_sq_expanded = create_fraction(
            create_superscript("b", "2", base_color=GOLD_ACCENT),
            VGroup(Text("4", color=WHITE_TEXT), create_superscript("a", "2", base_color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        )
        plus_b_sq_over_4a_sq = VGroup(Text("+", color=WHITE_TEXT), b_sq_over_4a_sq_expanded).arrange(RIGHT, buff=0.05)
        plus_b_sq_over_4a_sq.move_to(plus_b_over_2a_sq_right_final.get_center())

        self.play(Transform(plus_b_over_2a_sq_right_final, plus_b_sq_over_4a_sq), run_time=1)
        right_side_expanded = VGroup(minus_c_over_a_final, plus_b_sq_over_4a_sq)
        current_equation_final_step = VGroup(factored_left_general_squared_final, eq_final, right_side_expanded)
        self.wait(0.5)

        # 2b. Get common denominator for -c/a
        four_a_text = VGroup(Text("4", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        minus_4ac_over_4a_sq = create_fraction(
            VGroup(Text("-", color=WHITE_TEXT), four_a_text.copy(), Text("c", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05),
            VGroup(Text("4", color=WHITE_TEXT), create_superscript("a", "2", base_color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        )
        minus_4ac_over_4a_sq.move_to(minus_c_over_a_final.get_center())

        self.play(Transform(minus_c_over_a_final, minus_4ac_over_4a_sq), run_time=1)
        right_side_common_denom = VGroup(minus_4ac_over_4a_sq, plus_b_sq_over_4a_sq)
        current_equation_final_step = VGroup(factored_left_general_squared_final, eq_final, right_side_common_denom)
        self.wait(0.5)

        # 2c. Combine numerators
        combined_num_mobj = VGroup(
            create_superscript("b", "2", base_color=GOLD_ACCENT),
            Text("-", color=WHITE_TEXT),
            VGroup(Text("4", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT), Text("c", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
        ).arrange(RIGHT, buff=0.1)
        
        final_right_frac_combined = create_fraction(
            combined_num_mobj,
            VGroup(Text("4", color=WHITE_TEXT), create_superscript("a", "2", base_color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        )
        final_right_frac_combined.move_to(right_side_common_denom.get_center())

        self.play(Transform(right_side_common_denom, final_right_frac_combined), run_time=1.5)
        simplified_right_side_frac = final_right_frac_combined
        current_equation_final_step = VGroup(factored_left_general_squared_final, eq_final, simplified_right_side_frac)
        self.wait(0.5)

        # 3. Take Square Root
        left_no_square_final = factored_left_general_paren.copy().move_to(factored_left_general_squared_final.get_center())
        
        pm_final = Text("±", color=WHITE_TEXT).next_to(eq_final, RIGHT, buff=0.2)

        sqrt_right_content_copy = simplified_right_side_frac.copy()
        sqrt_right_final = create_sqrt_symbol(sqrt_right_content_copy).next_to(pm_final, RIGHT, buff=0.1)

        self.play(
            Transform(factored_left_general_squared_final, left_no_square_final),
            FadeIn(pm_final),
            FadeTransform(simplified_right_side_frac, sqrt_right_final),
            run_time=1.5
        )
        current_equation_final_step = VGroup(left_no_square_final, eq_final, pm_final, sqrt_right_final)
        self.wait(1)

        # 4. Simplify Root: √(4a^2) = 2a
        sqrt_num_content = VGroup(
            create_superscript("b", "2", base_color=GOLD_ACCENT), 
            Text("-", color=WHITE_TEXT), 
            VGroup(Text("4", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT), Text("c", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
        ).arrange(RIGHT, buff=0.1)
        sqrt_num = create_sqrt_symbol(sqrt_num_content)
        
        denom_2a = VGroup(Text("2", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        simplified_sqrt_right_side_final = create_fraction(sqrt_num, denom_2a)
        simplified_sqrt_right_side_final.next_to(pm_final, RIGHT, buff=0.1)

        self.play(ReplacementTransform(sqrt_right_final, simplified_sqrt_right_side_final), run_time=1.5)
        current_equation_final_step = VGroup(left_no_square_final, eq_final, pm_final, simplified_sqrt_right_side_final)
        self.wait(1)

        # 5. Isolate x (by moving -b/2a to the right)
        x_final = Text("x", color=BLUE_ACCENT)
        equals_final = Text("=", color=WHITE_TEXT)
        minus_b_over_2a_final = VGroup(Text("-", color=WHITE_TEXT), b_over_2a_frac.copy()).arrange(RIGHT, buff=0.05)
        
        pm_final_moved = pm_final.copy()
        sqrt_right_final_moved = simplified_sqrt_right_side_final.copy()

        self.play(
            Transform(left_no_square_final, x_final.copy().move_to(left_no_square_final.get_center())),
            eq_final.animate.next_to(x_final, RIGHT, buff=0.2),
            Transform(VGroup(left_no_square_final[0], left_no_square_final[2]), minus_b_over_2a_final.copy().next_to(equals_final, RIGHT, buff=0.2)),
            pm_final_moved.next_to(minus_b_over_2a_final, RIGHT, buff=0.2),
            sqrt_right_final_moved.next_to(pm_final_moved, RIGHT, buff=0.1),
            run_time=2
        )
        
        quadratic_formula_almost = VGroup(
            x_final, equals_final, minus_b_over_2a_final, pm_final_moved, sqrt_right_final_moved
        ).arrange(RIGHT, buff=0.2).center()
        
        self.play(Transform(VGroup(x_final, equals_final, minus_b_over_2a_final, pm_final_moved, sqrt_right_final_moved), quadratic_formula_almost))
        self.wait(1)

        # 6. Combine: x = (-b ± √(b^2 - 4ac)) / (2a)
        numerator_final = VGroup(
            Text("-", color=WHITE_TEXT),
            Text("b", color=GOLD_ACCENT),
            Text(" ± ", color=WHITE_TEXT),
            create_sqrt_symbol(VGroup(
                create_superscript("b", "2", base_color=GOLD_ACCENT), 
                Text("-", color=WHITE_TEXT), 
                VGroup(Text("4", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT), Text("c", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
            ).arrange(RIGHT, buff=0.1))
        ).arrange(RIGHT, buff=0.1)
        
        denominator_final = VGroup(Text("2", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        
        final_quadratic_formula_rhs = create_fraction(numerator_final, denominator_final)
        final_quadratic_formula_rhs.next_to(equals_final, RIGHT, buff=0.2)

        final_quadratic_formula = VGroup(x_final.copy(), equals_final.copy(), final_quadratic_formula_rhs).arrange(RIGHT, buff=0.2).center()

        self.play(
            Transform(quadratic_formula_almost, final_quadratic_formula),
            run_time=2
        )
        final_quadratic_formula_mobj = final_quadratic_formula
        self.wait(2)

        self.play(FadeOut(title4, final_quadratic_formula_mobj))
        self.wait(0.5)

        # --- BEAT 5: Recap Card ---
        recap_title = Text("Recap: The Quadratic Formula", color=GOLD_ACCENT, font_size=50).to_edge(UP)
        
        # Re-create the final formula for the recap card
        recap_formula_x = Text("x", color=BLUE_ACCENT)
        recap_formula_equals = Text("=", color=WHITE_TEXT)
        recap_formula_numerator = VGroup(
            Text("-", color=WHITE_TEXT),
            Text("b", color=GOLD_ACCENT),
            Text(" ± ", color=WHITE_TEXT),
            create_sqrt_symbol(VGroup(
                create_superscript("b", "2", base_color=GOLD_ACCENT), 
                Text("-", color=WHITE_TEXT), 
                VGroup(Text("4", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT), Text("c", color=BLUE_ACCENT)).arrange(RIGHT, buff=0.05)
            ).arrange(RIGHT, buff=0.1))
        ).arrange(RIGHT, buff=0.1)
        recap_formula_denominator = VGroup(Text("2", color=WHITE_TEXT), Text("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        
        recap_formula_rhs = create_fraction(recap_formula_numerator, recap_formula_denominator)
        
        final_quadratic_formula_recap = VGroup(recap_formula_x, recap_formula_equals, recap_formula_rhs).arrange(RIGHT, buff=0.2).scale(1.2).center().shift(UP*0.5)
        
        recap_text1 = Text("Derived from completing the square!", color=WHITE_TEXT, font_size=36).next_to(final_quadratic_formula_recap, DOWN, buff=1)
        recap_text2 = Text("Understanding 'why' makes it stick!", color=BLUE_ACCENT, font_size=36).next_to(recap_text1, DOWN, buff=0.5)

        self.play(FadeIn(recap_title), Write(final_quadratic_formula_recap), run_time=1.5)
        self.play(Write(recap_text1), run_time=1)
        self.play(Write(recap_text2), run_time=1)
        self.wait(3)
        self.play(FadeOut(recap_title, final_quadratic_formula_recap, recap_text1, recap_text2))
        self.wait(1)