from manim import *

class DeriveQuadraticFormula(Scene):
    def construct(self):
        self.camera.background_color = "#1A1A1A" # Dark background

        # --- Helper functions for creating text expressions without Tex ---
        # Manages creating fractions from Mobject components
        def create_fraction(numerator_mobject, denominator_mobject, color=WHITE):
            # Ensure inputs are Mobjects, not just strings
            if isinstance(numerator_mobject, str):
                numerator_mobject = Text(numerator_mobject, font_size=40, color=color)
            if isinstance(denominator_mobject, str):
                denominator_mobject = Text(denominator_mobject, font_size=40, color=color)

            line = Line(LEFT * 0.5, RIGHT * 0.5, color=color, stroke_width=2)
            
            # Adjust line length based on wider of num/den
            line.set_width(max(numerator_mobject.get_width(), denominator_mobject.get_width()) * 1.2)
            
            numerator_mobject.next_to(line, UP, buff=0.1)
            denominator_mobject.next_to(line, DOWN, buff=0.1)
            
            fraction_group = VGroup(numerator_mobject, line, denominator_mobject)
            return fraction_group

        # Manages creating exponents from Mobject components
        def create_exponent(base_mobject, exponent_mobject, base_color=WHITE, exp_color=WHITE):
            if isinstance(base_mobject, str):
                base = Text(base_mobject, font_size=40, color=base_color)
            else:
                base = base_mobject # Assume it's already a VGroup/Mobject
            
            if isinstance(exponent_mobject, str):
                exponent = Text(exponent_mobject, font_size=20, color=exp_color)
            else:
                exponent = exponent_mobject # Assume it's already a VGroup/Mobject
            
            exponent.next_to(base, UP + RIGHT, buff=0.05).scale(0.7).align_to(base, UP) # Smaller, superscript, aligned to top of base
            return VGroup(base, exponent)

        # Manages creating a simplified square root symbol from Mobject components
        def create_sqrt(expression_mobject, color=WHITE):
            # A simplified square root symbol composed of lines
            v_stem = Line(ORIGIN, DOWN * 0.2, color=color, stroke_width=3)
            hook = Line(v_stem.get_end(), v_stem.get_end() + UP * 0.4 + RIGHT * 0.15, color=color, stroke_width=3)
            top_line = Line(hook.get_end(), hook.get_end() + RIGHT * (expression_mobject.get_width() * 1.1 + 0.2), color=color, stroke_width=3)

            sqrt_symbol_group = VGroup(v_stem, hook, top_line)
            
            # Scale and position the symbol relative to the expression
            sqrt_symbol_group.scale_to_fit_height(expression_mobject.get_height() * 1.2)
            sqrt_symbol_group.next_to(expression_mobject, LEFT, buff=0.1)
            
            # Adjust alignment for better visual appearance
            top_line.align_to(expression_mobject, UP)
            hook.put_start_and_end_on(v_stem.get_end(), top_line.get_start())
            
            # Reposition the stem relative to the hook's start and top line
            # This is a bit of a manual hack to make it look decent without Tex
            stem_start_point = top_line.get_start() + LEFT * 0.2 + DOWN * 0.6
            stem_end_point = top_line.get_start() + LEFT * 0.1
            v_stem.put_start_and_end_on(stem_start_point, stem_end_point)

            return VGroup(sqrt_symbol_group, expression_mobject)

        # --- Beat 1: Introduction / Visual Hook & General Form ---
        title = Text("Deriving the Quadratic Formula", font_size=60, color=GOLD).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Visual Hook: A dynamically changing parabola
        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            x_length=10, y_length=10,
            axis_config={"color": BLUE_D, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-4, 4]},
            y_axis_config={"numbers_to_include": [-4, 4]},
        ).scale(0.6).to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(0)
        c_tracker = ValueTracker(0)

        parabola_func = lambda x: a_tracker.get_value() * x**2 + b_tracker.get_value() * x + c_tracker.get_value()
        parabola = always_redraw(lambda: axes.get_graph(parabola_func, color=BLUE).set_stroke(width=4))

        self.play(Create(axes), Create(labels), Create(parabola))
        self.wait(0.5)

        self.play(a_tracker.animate.set_value(0.5), b_tracker.animate.set_value(2), c_tracker.animate.set_value(1), run_time=1.5)
        self.wait(0.5)
        self.play(a_tracker.animate.set_value(-0.8), b_tracker.animate.set_value(-1), c_tracker.animate.set_value(3), run_time=1.5)
        self.wait(0.5)

        self.play(FadeOut(parabola, axes, labels, a_tracker, b_tracker, c_tracker), run_time=1)
        self.play(FadeOut(title))

        # Introduce the general form of the quadratic equation
        eq1_a = Text("a", color=BLUE, font_size=48)
        eq1_x2 = create_exponent("x", "2") # Using helper function
        eq1_plus1 = Text(" + ", font_size=48)
        eq1_b = Text("b", color=BLUE, font_size=48)
        eq1_x = Text("x", font_size=48)
        eq1_plus2 = Text(" + ", font_size=48)
        eq1_c = Text("c", color=BLUE, font_size=48)
        eq1_eq0 = Text(" = 0", font_size=48)

        equation1 = VGroup(eq1_a, eq1_x2, eq1_plus1, eq1_b, eq1_x, eq1_plus2, eq1_c, eq1_eq0).arrange(RIGHT, buff=0.1).center()
        
        self.play(Write(equation1), run_time=1.5)
        self.wait(1)

        goal_text = Text("Our Goal: Solve for 'x'", font_size=40, color=GOLD).next_to(equation1, DOWN, buff=0.8)
        self.play(Write(goal_text))
        self.wait(1)

        # --- Beat 2: Normalize 'a' and Move 'c' ---
        self.play(FadeOut(goal_text))
        
        # Step 1: Divide by 'a'
        divide_by_a_text = Text("Step 1: Divide by 'a'", font_size=32, color=BLUE_A).to_corner(UL)
        self.play(Write(divide_by_a_text))

        # New equation after dividing by 'a'
        eq2_x2 = create_exponent("x", "2")
        eq2_plus1 = Text(" + ", font_size=48)
        eq2_b_over_a = create_fraction("b", "a", color=WHITE)
        eq2_x = Text("x", font_size=48)
        eq2_plus2 = Text(" + ", font_size=48)
        eq2_c_over_a = create_fraction("c", "a", color=WHITE)
        eq2_eq0 = Text(" = 0", font_size=48)

        equation2 = VGroup(eq2_x2, eq2_plus1, eq2_b_over_a, eq2_x, eq2_plus2, eq2_c_over_a, eq2_eq0).arrange(RIGHT, buff=0.1).center()

        self.play(
            FadeOut(equation1, shift=UP), # Fade out old equation
            Write(equation2) # Write new equation
        )
        self.wait(1)

        # Step 2: Move 'c/a' to the right side
        move_c_text = Text("Step 2: Move 'c/a' to right", font_size=32, color=BLUE_A).next_to(divide_by_a_text, DOWN, buff=0.5, align_to=divide_by_a_text)
        self.play(Write(move_c_text))

        # Create the next equation's components
        eq3_x2 = eq2_x2.copy()
        eq3_plus1 = eq2_plus1.copy()
        eq3_b_over_a = eq2_b_over_a.copy()
        eq3_x = eq2_x.copy()
        eq3_eq = Text(" = ", font_size=48)
        eq3_minus = Text("-", font_size=48)
        eq3_c_over_a = eq2_c_over_a.copy()

        equation3 = VGroup(eq3_x2, eq3_plus1, eq3_b_over_a, eq3_x, eq3_eq, eq3_minus, eq3_c_over_a).arrange(RIGHT, buff=0.1).center()

        # Animate moving c/a. Replace old `+ c/a = 0` with new `= -c/a`.
        old_left_side = VGroup(eq2_x2, eq2_plus1, eq2_b_over_a, eq2_x)
        old_right_side = VGroup(eq2_plus2, eq2_c_over_a, eq2_eq0)
        new_left_side = VGroup(eq3_x2, eq3_plus1, eq3_b_over_a, eq3_x)
        new_right_side = VGroup(eq3_eq, eq3_minus, eq3_c_over_a)
        
        self.play(
            ReplacementTransform(old_left_side, new_left_side),
            FadeOut(old_right_side, shift=RIGHT),
            Write(new_right_side),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 3: Completing the Square - Intuition (Geometric) ---
        self.play(FadeOut(divide_by_a_text, move_c_text), FadeOut(equation3, shift=UP))

        title_comp_sq = Text("Step 3: Completing the Square (Visual)", font_size=50, color=GOLD).to_edge(UP)
        self.play(Write(title_comp_sq))

        # Geometric representation of x^2 + (b/a)x
        # x^2 square
        side_x_length = 2.0
        square_x = Square(side_length=side_x_length, color=BLUE_C, fill_opacity=0.7).move_to(LEFT * 3 + UP * 1)
        x_label_left = Text("x", font_size=35, color=WHITE).next_to(square_x, LEFT, buff=0.1)
        x_label_top = Text("x", font_size=35, color=WHITE).next_to(square_x, UP, buff=0.1)
        x_area_label = create_exponent("x", "2", color=WHITE).move_to(square_x.get_center())

        self.play(Create(square_x), Write(x_label_left), Write(x_label_top), Write(x_area_label))
        self.wait(0.5)

        # (b/a)x split into two (b/2a)x rectangles
        rect_width_val = side_x_length / 2 # Represents b/2a for visual scale

        rect1 = Rectangle(width=rect_width_val, height=side_x_length, color=GOLD_C, fill_opacity=0.7).next_to(square_x, RIGHT, buff=0).align_to(square_x, UP)
        rect2 = Rectangle(width=side_x_length, height=rect_width_val, color=GOLD_C, fill_opacity=0.7).next_to(square_x, DOWN, buff=0).align_to(square_x, LEFT)
        
        # Area labels for these rectangles
        area_bx_2a_text = VGroup(create_fraction("b", "2a", color=WHITE).scale(0.7), Text("x", font_size=35)).arrange(RIGHT, buff=0.05)
        area_bx_2a_label1 = area_bx_2a_text.copy().move_to(rect1.get_center())
        area_bx_2a_label2 = area_bx_2a_text.copy().move_to(rect2.get_center())
        
        self.play(
            Create(rect1), Create(rect2),
            Write(area_bx_2a_label1), Write(area_bx_2a_label2)
        )
        self.wait(1)

        # Complete the square by adding the missing corner
        missing_square_side = rect_width_val
        missing_square = Square(side_length=missing_square_side, color=BLUE_E, fill_opacity=0.9).next_to(rect1, DOWN, buff=0).align_to(rect2, RIGHT)
        
        missing_area_term = create_exponent(create_fraction("b", "2a"), "2").arrange(RIGHT, buff=0.05).scale(0.7)
        missing_area_label = missing_area_term.copy().move_to(missing_square.get_center())

        self.play(Create(missing_square), Write(missing_area_label))
        self.wait(1)

        # Show the full square (x + b/2a)^2
        full_side_label_content = VGroup(Text("x + ", font_size=35), create_fraction("b", "2a").scale(0.7)).arrange(RIGHT, buff=0.05)
        full_side_top = full_side_label_content.copy().next_to(square_x.get_corner(UP+LEFT), UP, buff=0.1).align_to(square_x.get_corner(UP+LEFT), LEFT)
        full_side_right = full_side_label_content.copy().rotate(PI/2).next_to(square_x.get_corner(UP+RIGHT), RIGHT, buff=0.1).align_to(square_x.get_corner(UP+RIGHT), UP)

        self.play(
            FadeOut(x_label_left, x_label_top, x_area_label, area_bx_2a_label1, area_bx_2a_label2),
            Write(full_side_top),
            Write(full_side_right),
            run_time=1.5
        )
        self.wait(1)
        
        # Animate the concept of (x + b/2a)^2
        full_geometric_group = VGroup(square_x, rect1, rect2, missing_square)
        self.play(full_geometric_group.animate.shift(LEFT * 2.5), FadeOut(full_side_top, full_side_right), run_time=1.5)

        formal_comp_square = VGroup(
            Text("(", font_size=48), Text("x + ", font_size=48), create_fraction("b", "2a", color=WHITE),
            Text(")", font_size=48), create_exponent("", "2", color=WHITE)
        ).arrange(RIGHT, buff=0.1)
        
        # The expansion of (x + b/2a)^2 for reference
        formal_comp_square_expansion = VGroup(
            create_exponent("x", "2"),
            Text(" + ", font_size=48),
            create_fraction("b", "a"),
            Text("x", font_size=48),
            Text(" + ", font_size=48),
            create_exponent(create_fraction("b", "2a"), "2")
        ).arrange(RIGHT, buff=0.1)

        formal_comp_square_full_expr = VGroup(
            formal_comp_square,
            Text(" = ", font_size=48),
            formal_comp_square_expansion
        ).arrange(RIGHT, buff=0.1).next_to(full_geometric_group, RIGHT, buff=1.5).align_to(full_geometric_group, UP)
        
        self.play(Write(formal_comp_square_full_expr), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(full_geometric_group, formal_comp_square_full_expr, missing_area_label),
            FadeOut(title_comp_sq)
        )

        # --- Beat 4: Completing the Square - Algebraic Application ---
        algebraic_title = Text("Step 4: Algebraic Application", font_size=50, color=GOLD).to_edge(UP)
        self.play(Write(algebraic_title))

        # Re-create eq3 (from Beat 2) for proper Mobject management
        eq_current_x2 = create_exponent("x", "2")
        eq_current_b_over_a_x = VGroup(create_fraction("b", "a", color=WHITE), Text("x", font_size=48)).arrange(RIGHT, buff=0.05)
        eq_current_c_over_a = create_fraction("c", "a", color=WHITE)
        
        eq_current = VGroup(
            eq_current_x2, Text(" + ", font_size=48), eq_current_b_over_a_x,
            Text(" = ", font_size=48), Text("-", font_size=48), eq_current_c_over_a
        ).arrange(RIGHT, buff=0.1).center()
        
        self.play(Write(eq_current))
        self.wait(1)

        # Add (b/2a)^2 to both sides
        add_term_expression = create_exponent(create_fraction("b", "2a", color=GOLD), "2")
        add_term_left_plus = Text(" + ", font_size=48)
        add_term_right_plus = Text(" + ", font_size=48)

        # Position them
        add_term_left_group = VGroup(add_term_left_plus, add_term_expression.copy()).arrange(RIGHT, buff=0.1).next_to(eq_current[2], RIGHT, buff=0.1) # After 'b/a x' on left
        add_term_right_group = VGroup(add_term_right_plus, add_term_expression.copy()).arrange(RIGHT, buff=0.1).next_to(eq_current[5], RIGHT, buff=0.1) # After '-c/a' on right

        self.play(Write(add_term_left_group), Write(add_term_right_group))
        self.wait(1)

        # Factor left side, simplify right side
        eq4_left = create_exponent(
            VGroup(Text("(", font_size=48), Text("x + ", font_size=48), create_fraction("b", "2a", color=WHITE), Text(")", font_size=48)).arrange(RIGHT, buff=0.1),
            "2"
        )
        
        eq4_eq = Text(" = ", font_size=48)

        # Right side: (b^2 / 4a^2) - (c/a) = (b^2 - 4ac) / (4a^2)
        b_sq = create_exponent("b", "2", color=WHITE)
        four_a_sq = VGroup(Text("4", font_size=40), create_exponent("a", "2")).arrange(RIGHT, buff=0.05)
        numerator_rhs = VGroup(b_sq.copy(), Text(" - ", font_size=40), Text("4ac", font_size=40, color=BLUE)).arrange(RIGHT, buff=0.05)
        eq4_rhs = create_fraction(numerator_rhs, four_a_sq.copy(), color=WHITE)
        
        equation4 = VGroup(eq4_left, eq4_eq, eq4_rhs).arrange(RIGHT, buff=0.1).center()
        
        self.play(
            FadeOut(eq_current, add_term_left_group, add_term_right_group, shift=UP),
            Write(equation4),
            run_time=2
        )
        self.wait(1.5)

        # --- Beat 5: Solve for 'x' ---
        self.play(FadeOut(algebraic_title, shift=UP))
        solve_title = Text("Step 5: Solve for 'x'", font_size=50, color=GOLD).to_edge(UP)
        self.play(Write(solve_title))
        
        # Take square root of both sides
        take_sqrt_text = Text("Take square root of both sides", font_size=32, color=BLUE_A).to_corner(UL)
        self.play(Write(take_sqrt_text))

        eq5_left = VGroup(Text("x + ", font_size=48), create_fraction("b", "2a", color=WHITE)).arrange(RIGHT, buff=0.1)
        eq5_eq = Text(" = ", font_size=48)
        eq5_plus_minus = Text("±", font_size=48)

        # Right side: sqrt((b^2 - 4ac) / (4a^2))
        eq5_rhs_fraction_num = numerator_rhs.copy()
        eq5_rhs_fraction_den = four_a_sq.copy()
        eq5_rhs_fraction_content = create_fraction(eq5_rhs_fraction_num, eq5_rhs_fraction_den)
        
        eq5_rhs = create_sqrt(eq5_rhs_fraction_content, color=WHITE)
        
        equation5 = VGroup(eq5_left, eq5_eq, eq5_plus_minus, eq5_rhs).arrange(RIGHT, buff=0.1).center()

        self.play(
            FadeOut(equation4, shift=UP),
            Write(equation5),
            run_time=2
        )
        self.wait(1.5)

        # Simplify right side: sqrt(numerator) / sqrt(denominator)
        simplify_sqrt_text = Text("Simplify the square root", font_size=32, color=BLUE_A).next_to(take_sqrt_text, DOWN, buff=0.5, align_to=take_sqrt_text)
        self.play(Write(simplify_sqrt_text))

        # New right side: sqrt(b^2 - 4ac) / (2a)
        final_numerator_rhs_term = create_sqrt(numerator_rhs.copy(), color=WHITE)
        final_denominator_rhs_term = VGroup(Text("2", font_size=40), Text("a", font_size=40)).arrange(RIGHT, buff=0.05)
        
        eq6_rhs = create_fraction(final_numerator_rhs_term, final_denominator_rhs_term, color=WHITE)
        
        equation6 = VGroup(eq5_left.copy(), eq5_eq.copy(), eq5_plus_minus.copy(), eq6_rhs).arrange(RIGHT, buff=0.1).center()

        self.play(
            ReplacementTransform(equation5, equation6),
            run_time=1.5
        )
        self.wait(1.5)

        # Isolate x
        isolate_x_text = Text("Isolate 'x'", font_size=32, color=BLUE_A).next_to(simplify_sqrt_text, DOWN, buff=0.5, align_to=simplify_sqrt_text)
        self.play(Write(isolate_x_text))

        # x = -b/2a ± sqrt(...) / 2a
        eq7_x = Text("x", font_size=48)
        eq7_eq = Text(" = ", font_size=48)
        eq7_minus_b_over_2a = VGroup(Text("-", font_size=48), create_fraction("b", "2a", color=WHITE)).arrange(RIGHT, buff=0.1)
        eq7_plus_minus = Text("±", font_size=48)
        eq7_rhs_fraction = eq6_rhs.copy()

        equation7 = VGroup(eq7_x, eq7_eq, eq7_minus_b_over_2a, eq7_plus_minus, eq7_rhs_fraction).arrange(RIGHT, buff=0.1).center()
        
        self.play(
            ReplacementTransform(equation6, equation7),
            run_time=1.5
        )
        self.wait(1.5)

        # Combine into single fraction
        combine_fraction_text = Text("Combine fractions", font_size=32, color=BLUE_A).next_to(isolate_x_text, DOWN, buff=0.5, align_to=isolate_x_text)
        self.play(Write(combine_fraction_text))
        
        # Final expression
        final_numerator_content = VGroup(
            Text("-b", font_size=40, color=BLUE), Text(" ± ", font_size=40),
            create_sqrt(VGroup(create_exponent("b", "2"), Text(" - ", font_size=40), Text("4ac", font_size=40, color=BLUE)).arrange(RIGHT, buff=0.05))
        ).arrange(RIGHT, buff=0.1)
        final_denominator_content = VGroup(Text("2", font_size=40), Text("a", font_size=40, color=BLUE)).arrange(RIGHT, buff=0.05)
        
        final_rhs_fraction = create_fraction(final_numerator_content, final_denominator_content, color=WHITE)
        
        final_formula = VGroup(Text("x", font_size=48, color=GOLD), Text(" = ", font_size=48), final_rhs_fraction).arrange(RIGHT, buff=0.1).center()

        self.play(
            ReplacementTransform(equation7, final_formula.set_color(GOLD)), # Set the whole formula to GOLD
            FadeOut(take_sqrt_text, simplify_sqrt_text, isolate_x_text, combine_fraction_text, solve_title),
            run_time=3
        )
        self.wait(3)

        # --- Beat 6: Recap Card ---
        self.play(FadeOut(final_formula))
        
        recap_title = Text("Recap: Quadratic Formula Derivation", font_size=60, color=GOLD).to_edge(UP)
        self.play(Write(recap_title))

        recap_steps = VGroup(
            Text("1. Start with ax² + bx + c = 0", font_size=35, color=WHITE),
            Text("2. Normalize by 'a', move 'c'", font_size=35, color=WHITE),
            Text("3. Complete the square (geometric intuition)", font_size=35, color=WHITE),
            Text("4. Apply completion algebraically", font_size=35, color=WHITE),
            Text("5. Solve for 'x' by taking square root", font_size=35, color=WHITE),
            Text("6. Simplify and combine terms", font_size=35, color=WHITE)
        ).arrange(DOWN, buff=0.4, align_vert=LEFT).center().shift(UP*0.5)

        self.play(LaggedStart(*[Write(step) for step in recap_steps], lag_ratio=0.5))
        self.wait(3)

        # Final formula on recap card
        final_numerator_recap_content = VGroup(
            Text("-b", font_size=48, color=BLUE), Text(" ± ", font_size=48),
            create_sqrt(VGroup(create_exponent("b", "2"), Text(" - ", font_size=48), Text("4ac", font_size=48, color=BLUE)).arrange(RIGHT, buff=0.05))
        ).arrange(RIGHT, buff=0.1)
        final_denominator_recap_content = VGroup(Text("2", font_size=48), Text("a", font_size=48, color=BLUE)).arrange(RIGHT, buff=0.05)
        
        final_formula_recap_display = VGroup(
            Text("x", font_size=55, color=GOLD), Text(" = ", font_size=55),
            create_fraction(final_numerator_recap_content, final_denominator_recap_content, color=WHITE)
        ).arrange(RIGHT, buff=0.2).next_to(recap_steps, DOWN, buff=1)

        self.play(Write(final_formula_recap_display, run_time=2))
        self.wait(5)