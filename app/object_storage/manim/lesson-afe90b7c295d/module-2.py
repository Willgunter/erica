from manim import *

class DerivationCompletingTheSquare(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_C = '#58C4DD' # 3B1B inspired light blue
        GOLD_C = '#FFD700' # 3B1B inspired gold
        RED_C = '#E07A5F'  # For error/difference or key point
        
        # --- Beat 1: The Hook - The Mystery of the Quadratic Formula ---
        title = Tex("Derivation by Completing the Square", font_size=50, color=GOLD_C).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        initial_equation = MathTex("ax^2 + bx + c = 0", color=BLUE_C, font_size=48)
        self.play(FadeIn(initial_equation, shift=DOWN))
        self.wait(1)

        quadratic_formula = MathTex(
            "x = ", "{{-b \\pm \\sqrt{b^2 - 4ac}}}", "/", "{{2a}}",
            font_size=60, color=BLUE_C
        ).next_to(initial_equation, DOWN, buff=0.8)
        
        question_mark = Text("?", font_size=96, color=RED_C).next_to(quadratic_formula, RIGHT, buff=0.5)
        
        self.play(initial_equation.animate.shift(UP*1.5).scale(0.8), run_time=1.5)
        self.play(
            LaggedStart(
                Write(quadratic_formula[0]), # x =
                ReplacementTransform(initial_equation.copy(), quadratic_formula[1]), # -b...
                ReplacementTransform(initial_equation.copy(), quadratic_formula[2]), # /
                ReplacementTransform(initial_equation.copy(), quadratic_formula[3]), # 2a
                lag_ratio=0.5,
                run_time=2.5
            )
        )
        self.play(GrowFromCenter(question_mark))
        self.wait(1.5)

        explanation = Tex("Where does this come from?", font_size=40, color=GOLD_C).next_to(question_mark, DOWN)
        self.play(FadeIn(explanation, shift=UP))
        self.wait(1)
        self.play(FadeOut(question_mark, explanation, initial_equation, quadratic_formula))
        self.wait(0.5)

        # --- Beat 2: Geometric Intuition of Completing the Square ---
        self.play(title.animate.to_edge(UP).scale(0.8).set_color(BLUE_C))
        
        # Visualizing x^2 + bx
        x_val = 2.5
        b_val = 2

        square_x = Square(side_length=x_val, color=BLUE_C, fill_opacity=0.7).shift(LEFT * (b_val/2 + x_val/2))
        x_label = MathTex("x^2", color=BLACK).move_to(square_x)
        x_label_dim_x = MathTex("x", color=GOLD_C).next_to(square_x.get_top(), UP, buff=0.1)
        x_label_dim_y = MathTex("x", color=GOLD_C).next_to(square_x.get_left(), LEFT, buff=0.1)

        self.play(Create(square_x), Write(x_label_dim_x), Write(x_label_dim_y), FadeIn(x_label))
        self.wait(0.5)

        rect_h_base = Rectangle(width=x_val, height=b_val/2, color=GOLD_C, fill_opacity=0.7).next_to(square_x, UP, buff=0)
        rect_v_base = Rectangle(width=b_val/2, height=x_val + b_val/2, color=GOLD_C, fill_opacity=0.7).next_to(square_x.get_right(), RIGHT, buff=0)

        # We want to represent x^2 + bx. Split b into two halves for symmetry.
        rect_1 = Rectangle(width=x_val, height=b_val/2, color=GOLD_C, fill_opacity=0.7).next_to(square_x, RIGHT, buff=0)
        rect_2 = Rectangle(width=b_val/2, height=x_val, color=GOLD_C, fill_opacity=0.7).next_to(square_x, UP, buff=0) # This isn't right for b/2 * x + b/2 * x

        # Correct geometric representation for x^2 + bx.
        # One large rectangle of area bx, or two smaller rectangles of area (b/2)x each.
        # Let's use two (b/2)x rectangles to naturally lead to completing the square.
        
        rect_side_length = x_val # for consistency
        half_b_length = b_val / 2 

        rect_1 = Rectangle(width=rect_side_length, height=half_b_length, color=GOLD_C, fill_opacity=0.7).align_to(square_x.get_top(), LEFT).shift(UP * half_b_length)
        rect_2 = Rectangle(width=half_b_length, height=rect_side_length, color=GOLD_C, fill_opacity=0.7).align_to(square_x.get_right(), UP).shift(RIGHT * half_b_length)
        
        area_labels_group = VGroup(
            MathTex("x", color=GOLD_C).next_to(rect_1.get_top(), UP, buff=0.1),
            MathTex("\\frac{b}{2}", color=GOLD_C).next_to(rect_1.get_left(), LEFT, buff=0.1),
            MathTex("\\frac{b}{2}", color=GOLD_C).next_to(rect_2.get_bottom(), DOWN, buff=0.1),
            MathTex("x", color=GOLD_C).next_to(rect_2.get_right(), RIGHT, buff=0.1)
        ).fade(1) # initially faded

        rect_1_label = MathTex("x \\cdot \\frac{b}{2}", font_size=30, color=BLACK).move_to(rect_1)
        rect_2_label = MathTex("x \\cdot \\frac{b}{2}", font_size=30, color=BLACK).move_to(rect_2)

        shapes_group = VGroup(square_x, rect_1, rect_2)
        labels_group = VGroup(x_label, rect_1_label, rect_2_label, x_label_dim_x, x_label_dim_y)
        
        self.play(
            Create(rect_1), Create(rect_2),
            LaggedStart(FadeIn(rect_1_label), FadeIn(rect_2_label)),
            FadeIn(area_labels_group)
        )
        self.wait(1)
        
        current_eq_geom = MathTex("x^2 + 2 \\left(x \\cdot \\frac{b}{2}\\right) ", "=", " x^2 + bx", font_size=40, color=BLUE_C).next_to(shapes_group, DOWN, buff=1)
        self.play(Write(current_eq_geom))
        self.wait(1)

        # The missing piece
        missing_square = Square(side_length=half_b_length, color=RED_C, fill_opacity=0.7).next_to(rect_1, RIGHT, buff=0).next_to(rect_2, UP, buff=0)
        missing_label = MathTex("\\left(\\frac{b}{2}\\right)^2", font_size=30, color=BLACK).move_to(missing_square)
        missing_dim_x = MathTex("\\frac{b}{2}", color=GOLD_C).next_to(missing_square.get_right(), RIGHT, buff=0.1)
        missing_dim_y = MathTex("\\frac{b}{2}", color=GOLD_C).next_to(missing_square.get_top(), UP, buff=0.1)

        self.play(
            Create(missing_square),
            FadeIn(missing_label),
            FadeIn(missing_dim_x),
            FadeIn(missing_dim_y)
        )
        self.wait(1)

        # Show the complete square
        complete_square_group = VGroup(square_x, rect_1, rect_2, missing_square)
        complete_square_area_label = MathTex(
            "\\left(x + \\frac{b}{2}\\right)^2",
            font_size=40, color=BLUE_C
        ).move_to(complete_square_group.get_center() + RIGHT*3 + UP*0.5)

        brace_x_plus_b_2_x = Brace(complete_square_group, LEFT, buff=0.1)
        brace_x_plus_b_2_y = Brace(complete_square_group, DOWN, buff=0.1)
        brace_text_x = brace_x_plus_b_2_x.get_text("$x + b/2$", color=GOLD_C)
        brace_text_y = brace_x_plus_b_2_y.get_text("$x + b/2$", color=GOLD_C)

        self.play(
            FadeOut(x_label, rect_1_label, rect_2_label, missing_label),
            FadeOut(area_labels_group, x_label_dim_x, x_label_dim_y, missing_dim_x, missing_dim_y),
            GrowFromCenter(brace_x_plus_b_2_x),
            GrowFromCenter(brace_x_plus_b_2_y),
            Write(brace_text_x),
            Write(brace_text_y)
        )
        self.wait(0.5)
        
        final_eq_geom = MathTex(
            "x^2 + bx + ", "\\left(\\frac{b}{2}\\right)^2 ", "=", " \\left(x + \\frac{b}{2}\\right)^2",
            font_size=40, color=BLUE_C
        ).next_to(current_eq_geom, DOWN, buff=0.5)

        self.play(TransformMatchingTex(current_eq_geom, final_eq_geom[0]), Write(final_eq_geom[1:]))
        self.wait(2)
        
        self.play(FadeOut(complete_square_group, brace_x_plus_b_2_x, brace_text_x, brace_x_plus_b_2_y, brace_text_y, final_eq_geom))
        self.wait(0.5)

        # --- Beat 3: Algebraic Derivation (Step 1 - Isolate and Normalize) ---
        beat_3_title = Tex("Step 1: Normalize and Isolate", font_size=45, color=GOLD_C).to_edge(UP).shift(DOWN*0.5)
        self.play(Transform(title, beat_3_title))
        self.wait(0.5)

        eq1 = MathTex("ax^2 + bx + c = 0", color=BLUE_C).center().shift(UP*0.5)
        self.play(Write(eq1))
        self.wait(1)

        divide_a = MathTex("\\div a", color=GOLD_C).next_to(eq1, LEFT, buff=1)
        eq2 = MathTex(
            "\\frac{ax^2}{a} + \\frac{bx}{a} + \\frac{c}{a} = \\frac{0}{a}",
            color=BLUE_C
        ).next_to(eq1, DOWN, buff=0.8)
        self.play(Write(divide_a), TransformMatchingTex(eq1.copy(), eq2))
        self.wait(1)
        self.play(FadeOut(divide_a))

        eq3 = MathTex("x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0", color=BLUE_C).next_to(eq2, DOWN, buff=0.8)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1)
        
        # Move c/a to the right side
        arrow_move_c = Arrow(eq3[0][8].get_center(), eq3.get_right() + RIGHT*0.5, color=GOLD_C, buff=0.2)
        move_c_text = MathTex("{- \\frac{c}{a}}", color=GOLD_C).next_to(arrow_move_c, UP, buff=0.1)
        self.play(GrowArrow(arrow_move_c), Write(move_c_text))

        eq4 = MathTex("x^2 + \\frac{b}{a}x = -\\frac{c}{a}", color=BLUE_C).next_to(eq3, DOWN, buff=0.8)
        self.play(TransformMatchingTex(eq3, eq4))
        self.play(FadeOut(arrow_move_c, move_c_text))
        self.wait(1.5)
        
        self.play(FadeOut(eq4), title.animate.to_edge(UP).shift(DOWN*0.5).set_color(GOLD_C))

        # --- Beat 4: Algebraic Derivation (Step 2 - Completing the Square) ---
        beat_4_title = Tex("Step 2: Complete the Square", font_size=45, color=GOLD_C).to_edge(UP).shift(DOWN*0.5)
        self.play(Transform(title, beat_4_title))
        self.wait(0.5)

        eq_current = MathTex("x^2 + \\frac{b}{a}x = -\\frac{c}{a}", color=BLUE_C).center().shift(UP*0.5)
        self.play(Write(eq_current))
        self.wait(1)

        # Identify the term to add: ( (b/a) / 2 )^2 = (b / 2a)^2
        b_over_a_term = SurroundingRectangle(eq_current[0][4:8], color=GOLD_C, buff=0.1)
        self.play(Create(b_over_a_term))
        self.wait(0.5)

        term_to_add_tex = MathTex(
            "\\left(\\frac{1}{2} \\cdot \\frac{b}{a}\\right)^2",
            "=",
            "\\left(\\frac{b}{2a}\\right)^2",
            color=GOLD_C
        ).next_to(b_over_a_term, DOWN, buff=0.5)
        self.play(Write(term_to_add_tex))
        self.play(FadeOut(b_over_a_term))
        self.wait(1)
        
        # Add the term to both sides
        add_term_left = MathTex(" + \\left(\\frac{b}{2a}\\right)^2", color=RED_C).next_to(eq_current[0][9], RIGHT, buff=0)
        add_term_right = MathTex(" + \\left(\\frac{b}{2a}\\right)^2", color=RED_C).next_to(eq_current[0][12], RIGHT, buff=0)

        self.play(Write(add_term_left), Write(add_term_right), FadeOut(term_to_add_tex))
        self.wait(1)

        eq_added_terms = MathTex(
            "x^2 + \\frac{b}{a}x + \\left(\\frac{b}{2a}\\right)^2 = -\\frac{c}{a} + \\left(\\frac{b}{2a}\\right)^2",
            color=BLUE_C
        ).next_to(eq_current, DOWN, buff=0.8)
        self.play(TransformMatchingTex(VGroup(eq_current, add_term_left, add_term_right), eq_added_terms))
        self.wait(1)

        # Factor the left side
        left_side_factor = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2",
            color=BLUE_C
        ).align_to(eq_added_terms[0][:9], LEFT)

        self.play(
            ReplacementTransform(eq_added_terms[0][:9], left_side_factor),
            eq_added_terms[0][9:].animate.shift(LEFT * (left_side_factor.width - eq_added_terms[0][:9].width)) # shift remaining part
        )
        eq_factored_left = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2 = -\\frac{c}{a} + \\left(\\frac{b}{2a}\\right)^2",
            color=BLUE_C
        ).next_to(eq_added_terms, DOWN, buff=0.8)
        self.play(TransformMatchingTex(eq_added_terms, eq_factored_left))
        self.wait(1.5)

        self.play(FadeOut(eq_factored_left), title.animate.to_edge(UP).shift(DOWN*0.5).set_color(GOLD_C))
        
        # --- Beat 5: Algebraic Derivation (Step 3 - Solve for x) ---
        beat_5_title = Tex("Step 3: Isolate x", font_size=45, color=GOLD_C).to_edge(UP).shift(DOWN*0.5)
        self.play(Transform(title, beat_5_title))
        self.wait(0.5)

        eq_start_solve = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2 = -\\frac{c}{a} + \\frac{b^2}{4a^2}",
            color=BLUE_C
        ).center().shift(UP*0.5)
        self.play(Write(eq_start_solve))
        self.wait(1)
        
        # Simplify the right side
        common_denom = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2 = -\\frac{4ac}{4a^2} + \\frac{b^2}{4a^2}",
            color=BLUE_C
        ).next_to(eq_start_solve, DOWN, buff=0.8)
        self.play(TransformMatchingTex(eq_start_solve, common_denom))
        self.wait(1)

        combined_right = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2 = \\frac{b^2 - 4ac}{4a^2}",
            color=BLUE_C
        ).next_to(common_denom, DOWN, buff=0.8)
        self.play(TransformMatchingTex(common_denom, combined_right))
        self.wait(1.5)

        # Take square root of both sides
        sqrt_text = MathTex("\\sqrt{\\phantom{x}}", color=GOLD_C).next_to(combined_right, LEFT, buff=0.5)
        sqrt_text_copy = sqrt_text.copy().next_to(combined_right, RIGHT, buff=0.5)
        self.play(GrowFromCenter(sqrt_text), GrowFromCenter(sqrt_text_copy))
        self.wait(0.5)

        eq_sqrt = MathTex(
            "x + \\frac{b}{2a} = \\pm\\sqrt{\\frac{b^2 - 4ac}{4a^2}}",
            color=BLUE_C
        ).next_to(combined_right, DOWN, buff=0.8)
        self.play(TransformMatchingTex(combined_right, eq_sqrt), FadeOut(sqrt_text, sqrt_text_copy))
        self.wait(1)

        # Simplify the square root
        eq_sqrt_simplified = MathTex(
            "x + \\frac{b}{2a} = \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}",
            color=BLUE_C
        ).next_to(eq_sqrt, DOWN, buff=0.8)
        self.play(TransformMatchingTex(eq_sqrt, eq_sqrt_simplified))
        self.wait(1)

        # Isolate x
        move_b_2a_text = MathTex("{- \\frac{b}{2a}}", color=GOLD_C).next_to(eq_sqrt_simplified[0][4], UP, buff=0.5)
        arrow_move_b_2a = Arrow(eq_sqrt_simplified[0][4].get_center(), eq_sqrt_simplified[0][8].get_center() + RIGHT*0.5, color=GOLD_C, buff=0.2)
        
        self.play(GrowArrow(arrow_move_b_2a), Write(move_b_2a_text))
        
        eq_x_isolated = MathTex(
            "x = -\\frac{b}{2a} \\pm \\frac{\\sqrt{b^2 - 4ac}}{2a}",
            color=BLUE_C
        ).next_to(eq_sqrt_simplified, DOWN, buff=0.8)
        self.play(TransformMatchingTex(eq_sqrt_simplified, eq_x_isolated), FadeOut(arrow_move_b_2a, move_b_2a_text))
        self.wait(1)

        # Final form
        final_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=BLUE_C, font_size=60
        ).next_to(eq_x_isolated, DOWN, buff=1.0)
        final_formula.set_color_by_tex_to_color_map({
            "-b": GOLD_C,
            "\\pm": GOLD_C,
            "\\sqrt{b^2 - 4ac}": GOLD_C,
            "2a": GOLD_C
        })
        self.play(TransformMatchingTex(eq_x_isolated, final_formula))
        self.wait(2)
        
        self.play(FadeOut(title))
        self.wait(0.5)

        # --- Recap Card ---
        recap_title = Tex("Recap: Completing the Square", font_size=50, color=GOLD_C).to_edge(UP)
        
        step1 = Tex("1. Normalize: Divide by $a$", font_size=36, color=BLUE_C).shift(UP*1.5)
        step2 = Tex("2. Isolate: Move constant term to RHS", font_size=36, color=BLUE_C).next_to(step1, DOWN, buff=0.5)
        step3 = Tex("3. Complete: Add $(b/2a)^2$ to both sides", font_size=36, color=BLUE_C).next_to(step2, DOWN, buff=0.5)
        step4 = Tex("4. Factor: Left side becomes $(x + b/2a)^2$", font_size=36, color=BLUE_C).next_to(step3, DOWN, buff=0.5)
        step5 = Tex("5. Solve: Take square root & isolate $x$", font_size=36, color=BLUE_C).next_to(step4, DOWN, buff=0.5)
        
        recap_group = VGroup(recap_title, step1, step2, step3, step4, step5)

        self.play(
            FadeOut(final_formula),
            Write(recap_title)
        )
        self.wait(0.5)
        self.play(LaggedStart(
            Write(step1),
            Write(step2),
            Write(step3),
            Write(step4),
            Write(step5),
            lag_ratio=0.7,
            run_time=4
        ))
        self.wait(3)
        self.play(FadeOut(recap_group))
        self.wait(1)