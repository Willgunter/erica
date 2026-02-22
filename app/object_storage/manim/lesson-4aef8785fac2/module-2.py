from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # Configuration for colors
        self.camera.background_color = BLACK
        BLUE = BLUE_E
        GOLD = GOLD_E
        WHITE = WHITE
        GRAY_TEXT = GRAY_A

        # --- Beat 0: Visual Hook ---
        # Adjust camera for initial view, focusing on the right for the parabola
        self.play(self.camera.animate.move_to(RIGHT * 2), run_time=0.01) # Instant camera move

        # Parabola and axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY_TEXT, "include_numbers": False}
        ).scale(0.8).to_edge(RIGHT, buff=0.5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y").set_color(GRAY_TEXT).scale(0.8)
        
        parabola = axes.plot(lambda x: x**2 - 2, color=BLUE)
        
        # Roots
        root1_val = -np.sqrt(2)
        root2_val = np.sqrt(2)
        dot1 = Dot(axes.c2p(root1_val, 0), color=GOLD)
        dot2 = Dot(axes.c2p(root2_val, 0), color=GOLD)
        
        intro_text = Text("Finding X", font_size=60, color=GOLD).to_edge(LEFT, buff=1)
        
        self.play(Create(axes), Create(axes_labels), run_time=0.8)
        self.play(Create(parabola), run_time=1.2)
        self.play(Create(dot1), Create(dot2), FadeIn(intro_text), run_time=0.8)
        self.wait(1.0)
        
        self.play(
            FadeOut(parabola), FadeOut(dot1), FadeOut(dot2),
            FadeOut(axes), FadeOut(axes_labels), FadeOut(intro_text),
            self.camera.animate.move_to(ORIGIN), # Reset camera position
            run_time=1.0
        )

        # --- Beat 1: Introduce General Quadratic Equation (ax^2 + bx + c = 0) ---
        title = Text("Deriving the Quadratic Formula", font_size=48, color=BLUE).to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        a_text_1 = Text("a", color=GOLD, font_size=40)
        x2_text_1 = Text("x²", color=BLUE, font_size=40)
        plus_b_text_1 = Text("+ b", color=GOLD, font_size=40)
        x_text_1 = Text("x", color=BLUE, font_size=40)
        plus_c_text_1 = Text("+ c", color=GOLD, font_size=40)
        equals_0_text_1 = Text("= 0", color=WHITE, font_size=40)

        # Group initial equation parts
        eq1_left_main = VGroup(a_text_1, x2_text_1, plus_b_text_1, x_text_1).arrange(RIGHT, buff=0.1)
        eq1_right_main = VGroup(plus_c_text_1, equals_0_text_1).arrange(RIGHT, buff=0.1)
        eq1_overall = VGroup(eq1_left_main, eq1_right_main).arrange(RIGHT, buff=0.1).center().shift(UP*0.5)

        goal_text = Text("Goal: Find 'x'", font_size=32, color=WHITE).next_to(eq1_overall, DOWN, buff=0.5)

        self.play(LaggedStart(*[Write(m) for m in eq1_overall], lag_ratio=0.1), FadeIn(goal_text))
        self.wait(1.2)

        # --- Beat 2: Isolate x terms and normalize (x^2 + (b/a)x = -c/a) ---
        # Move +c to the right side
        minus_c_text_2 = Text("= -c", color=WHITE, font_size=40).move_to(equals_0_text_1.get_center())
        
        self.play(
            FadeOut(plus_c_text_1),
            ReplacementTransform(equals_0_text_1, minus_c_text_2),
            FadeOut(goal_text)
        )
        self.wait(0.5)
        
        current_eq_for_div = VGroup(a_text_1, x2_text_1, plus_b_text_1, x_text_1, minus_c_text_2).arrange(RIGHT, buff=0.1).center().shift(UP*0.5)
        
        # Divide by 'a'
        div_a_note = Text("Divide by 'a'", font_size=28, color=GRAY_TEXT).next_to(current_eq_for_div, DOWN, buff=0.3)
        self.play(FadeIn(div_a_note))

        # New equation parts for x^2 + (b/a)x = -c/a
        x2_final = Text("x²", color=BLUE, font_size=40).move_to(x2_text_1.get_center())
        plus_final = Text("+", color=WHITE, font_size=40).move_to(plus_b_text_1.get_center())
        b_over_a_final = Text("b/a", color=GOLD, font_size=40).next_to(plus_final, RIGHT, buff=0.1)
        x_final = Text("x", color=BLUE, font_size=40).next_to(b_over_a_final, RIGHT, buff=0.1)
        equals_final = Text("=", color=WHITE, font_size=40).move_to(minus_c_text_2.get_left() + LEFT*0.2) 
        minus_c_over_a_final = Text("-c/a", color=WHITE, font_size=40).next_to(equals_final, RIGHT, buff=0.1)

        self.play(
            FadeOut(a_text_1),
            ReplacementTransform(x2_text_1, x2_final),
            ReplacementTransform(plus_b_text_1, plus_final),
            Create(b_over_a_final), 
            ReplacementTransform(x_text_1, x_final),
            ReplacementTransform(minus_c_text_2, VGroup(equals_final, minus_c_over_a_final).arrange(RIGHT, buff=0.1)),
            FadeOut(div_a_note)
        )
        current_eq_group_alg = VGroup(x2_final, plus_final, b_over_a_final, x_final, equals_final, minus_c_over_a_final).center().shift(UP*0.5)
        self.wait(1.0)

        # --- Beat 3: Geometric Completing the Square (Intuition) ---
        self.play(FadeOut(current_eq_group_alg), FadeOut(title.copy()))
        title_cs = Text("Completing the Square", font_size=48, color=BLUE).to_edge(UP, buff=0.5)
        self.play(FadeIn(title_cs))

        x_dim = 3.0
        b_over_a_dim = 1.2 

        square_x = Square(side_length=x_dim, color=BLUE, fill_opacity=0.7).shift(LEFT*2.5 + DOWN*0.5)
        rect_bx = Rectangle(width=b_over_a_dim, height=x_dim, color=GOLD, fill_opacity=0.7).next_to(square_x, RIGHT, buff=0)
        
        x_label_sq_left = Text("x", font_size=30, color=WHITE).next_to(square_x, LEFT, buff=0.1)
        x_label_sq_top = Text("x", font_size=30, color=WHITE).next_to(square_x, UP, buff=0.1)
        b_over_a_label_rect_top = Text("b/a", font_size=30, color=WHITE).next_to(rect_bx, UP, buff=0.1)
        
        self.play(Create(square_x), Write(x_label_sq_left), Write(x_label_sq_top), run_time=0.8)
        self.play(Create(rect_bx), Write(b_over_a_label_rect_top), run_time=0.8)
        self.wait(0.5)

        # Split rect_bx into two (b/2a)x rectangles
        half_b_over_a_dim = b_over_a_dim / 2
        
        rect_bx_half_1_new_pos = Rectangle(width=half_b_over_a_dim, height=x_dim, color=GOLD, fill_opacity=0.7).next_to(square_x, RIGHT, buff=0)
        rect_bx_half_2_new_pos = Rectangle(width=x_dim, height=half_b_over_a_dim, color=GOLD, fill_opacity=0.7).next_to(square_x, DOWN, buff=0)

        self.play(
            ReplacementTransform(rect_bx, rect_bx_half_1_new_pos),
            FadeOut(b_over_a_label_rect_top), run_time=0.8
        )
        self.play(
            Create(rect_bx_half_2_new_pos), run_time=0.8
        )

        b_over_2a_label_top = Text("b/2a", font_size=25, color=WHITE).next_to(rect_bx_half_1_new_pos, UP, buff=0.1)
        b_over_2a_label_left = Text("b/2a", font_size=25, color=WHITE).next_to(rect_bx_half_2_new_pos, LEFT, buff=0.1)
        
        self.play(
            FadeIn(b_over_2a_label_top), FadeIn(b_over_2a_label_left), run_time=0.8
        )
        self.wait(0.5)

        # Add the missing square
        missing_square = Square(side_length=half_b_over_a_dim, color=BLUE, fill_opacity=0.7)
        missing_square.next_to(rect_bx_half_1_new_pos, DOWN, buff=0).align_to(rect_bx_half_2_new_pos, RIGHT)
        missing_square_label = Text("(b/2a)²", font_size=25, color=WHITE).move_to(missing_square.get_center())

        self.play(Create(missing_square), FadeIn(missing_square_label), run_time=1.0)
        self.wait(1.0)
        
        geometric_mobjects = VGroup(
            square_x, rect_bx_half_1_new_pos, rect_bx_half_2_new_pos, missing_square,
            x_label_sq_left, x_label_sq_top, b_over_2a_label_top, b_over_2a_label_left,
            missing_square_label
        )
        
        self.play(
            FadeOut(geometric_mobjects),
            FadeOut(title_cs), run_time=1.0
        )
        
        # --- Beat 4: Completing the Square Algebraically (x + b/2a)^2 = (b^2 - 4ac) / 4a^2 ---
        self.play(FadeIn(title)) 
        
        # Bring back eq3 (x^2 + (b/a)x = -c/a)
        current_eq_group_alg.center().shift(UP*1.5)
        self.play(FadeIn(current_eq_group_alg), run_time=0.8)
        self.wait(0.5)

        # Add (b/2a)^2 to both sides
        add_b_over_2a_sq_note = Text("Add (b/2a)² to both sides", font_size=28, color=GRAY_TEXT).next_to(current_eq_group_alg, DOWN, buff=0.3)
        self.play(FadeIn(add_b_over_2a_sq_note), run_time=0.8)

        b_over_2a_sq_text_left = Text(" + (b/2a)²", color=GOLD, font_size=40).next_to(x_final, RIGHT, buff=0.1)
        b_over_2a_sq_text_right = Text(" + (b/2a)²", color=GOLD, font_size=40).next_to(minus_c_over_a_final, RIGHT, buff=0.1)

        self.play(
            FadeIn(b_over_2a_sq_text_left),
            FadeIn(b_over_2a_sq_text_right), run_time=1.0
        )
        self.wait(0.5)

        # Factor left side: (x + b/2a)^2
        factored_left_parts = [
            Text("(", color=BLUE, font_size=40),
            Text("x", color=BLUE, font_size=40),
            Text("+", color=WHITE, font_size=40),
            Text("b/2a", color=GOLD, font_size=40),
            Text(")", color=BLUE, font_size=40),
            Text("²", color=BLUE, font_size=40)
        ]
        factored_left_group = VGroup(*factored_left_parts).arrange(RIGHT, buff=0.05).align_to(x2_final, LEFT)
        
        self.play(
            FadeOut(add_b_over_2a_sq_note),
            Transform(VGroup(x2_final, plus_final, b_over_a_final, x_final, b_over_2a_sq_text_left), factored_left_group), run_time=1.0
        )
        self.wait(0.5)

        # Simplify right side: (b^2 - 4ac) / 4a^2
        combined_right_final_parts = [
            equals_final.copy(),
            Text(" (b² - 4ac)", color=WHITE, font_size=40),
            Text(" / ", color=WHITE, font_size=40),
            Text("4a²", color=BLUE, font_size=40)
        ]
        combined_right_final_group = VGroup(*combined_right_final_parts).arrange(RIGHT, buff=0.05).align_to(minus_c_over_a_final, LEFT).shift(RIGHT*0.3)
        
        self.play(
            Transform(VGroup(equals_final, minus_c_over_a_final, b_over_2a_sq_text_right), combined_right_final_group), run_time=1.2
        )
        current_eq_step4 = VGroup(factored_left_group, combined_right_final_group).arrange(RIGHT, buff=0.1).center().shift(UP*0.5)
        self.wait(1.5)

        # --- Beat 5: Isolate x and Final Formula ---
        # Take square root of both sides
        sqrt_note = Text("Take square root of both sides", font_size=28, color=GRAY_TEXT).next_to(current_eq_step4, DOWN, buff=0.3)
        self.play(FadeIn(sqrt_note), run_time=0.8)

        # Left side after sqrt: x + b/2a
        x_plus_b_div_2a_final = VGroup(
            factored_left_parts[1].copy(), # x
            factored_left_parts[2].copy(), # +
            factored_left_parts[3].copy()  # b/2a
        ).arrange(RIGHT, buff=0.05).align_to(factored_left_group, LEFT)
        
        # Right side after sqrt: ± √(b² - 4ac) / 2a
        plus_minus_sqrt_numerator = VGroup(
            Text("± ", color=GOLD, font_size=40),
            Text("√(b² - 4ac)", color=GOLD, font_size=40)
        ).arrange(RIGHT, buff=0.05)
        
        fraction_bar_sqrt = Text(" / ", color=WHITE, font_size=40)
        denominator_sqrt = Text("2a", color=BLUE, font_size=40)
        
        combined_right_group_sqrt = VGroup(
            combined_right_final_parts[0].copy(), # =
            plus_minus_sqrt_numerator,
            fraction_bar_sqrt,
            denominator_sqrt
        ).arrange(RIGHT, buff=0.05).align_to(combined_right_final_group, LEFT)
        
        self.play(
            FadeOut(sqrt_note),
            ReplacementTransform(factored_left_group, x_plus_b_div_2a_final),
            ReplacementTransform(combined_right_final_group, combined_right_group_sqrt), run_time=1.2
        )
        current_eq_step5 = VGroup(x_plus_b_div_2a_final, combined_right_group_sqrt).arrange(RIGHT, buff=0.1).center().shift(UP*0.5)
        self.wait(1.0)

        # Isolate x to get final formula
        # Due to "no Tex" constraint, a clean fade out/in is used for the final complex grouping.
        final_formula_display = VGroup(
            Text("x = ", color=WHITE, font_size=50),
            Text("(-b ± √(b² - 4ac))", color=GOLD, font_size=50),
            Text(" / ", color=WHITE, font_size=50),
            Text("2a", color=BLUE, font_size=50)
        ).arrange(RIGHT, buff=0.1).center().shift(DOWN*0.5)
        
        self.play(
            FadeOut(current_eq_step5),
            FadeIn(final_formula_display), run_time=1.5
        )
        self.wait(2.0)

        # --- Beat 6: Recap Card ---
        self.play(
            FadeOut(final_formula_display),
            FadeOut(title), run_time=1.0
        )

        recap_title = Text("The Quadratic Formula", font_size=50, color=BLUE).to_edge(UP, buff=0.5)
        recap_formula = VGroup(
            Text("x = ", color=WHITE, font_size=50),
            Text("(-b ± √(b² - 4ac))", color=GOLD, font_size=50),
            Text(" / ", color=WHITE, font_size=50),
            Text("2a", color=BLUE, font_size=50)
        ).arrange(RIGHT, buff=0.1).center().shift(UP*0.5)
        
        recap_message = Text(
            "Solves for x in ax² + bx + c = 0", 
            font_size=32, color=GRAY_TEXT
        ).next_to(recap_formula, DOWN, buff=0.5)

        self.play(FadeIn(recap_title), Create(recap_formula), FadeIn(recap_message), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(self.mobjects), run_time=1.0)