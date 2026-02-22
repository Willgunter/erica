from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # 1. Configuration: Dark background, high-contrast colors
        self.camera.background_color = BLACK
        BLUE_ACCENT = '#32C1FF' # A vibrant blue
        GOLD_ACCENT = '#FFD700' # A bright gold
        TEXT_COLOR = WHITE

        # --- Visual Hook (Opening) ---
        title = Text("Unlocking the Quadratic Formula", font_size=50, color=GOLD_ACCENT).to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)

        # Show the final formula as the grand goal
        final_formula_big = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=BLUE_ACCENT
        ).scale(1.8).shift(DOWN*0.5)

        self.play(Write(final_formula_big))
        self.wait(1.5)
        
        # Shrink and move the formula to a corner as a persistent reminder
        final_formula_small = final_formula_big.copy().scale(0.5).to_corner(UR, buff=0.3).set_color(TEXT_COLOR)
        self.play(
            ReplacementTransform(final_formula_big, final_formula_small),
            FadeOut(title)
        )
        self.wait(0.5)

        # Introduce the starting point for derivation
        intro_text = Text(
            "We begin with the standard quadratic equation:",
            font_size=32, color=TEXT_COLOR
        ).to_edge(LEFT, buff=0.5).shift(UP*1.5)
        self.play(FadeIn(intro_text, shift=RIGHT))
        self.wait(0.5)

        current_equation_str = "ax^2 + bx + c = 0"
        equation = MathTex(current_equation_str, color=GOLD_ACCENT).next_to(intro_text, DOWN, buff=0.6).align_to(intro_text, LEFT)
        self.play(Write(equation))
        self.wait(1)

        self.play(FadeOut(intro_text)) # Remove intro text to make space

        # --- Beat 1: Isolate constant term and divide by 'a' ---
        step1_title = Text("Step 1: Isolate & Normalize", font_size=30, color=BLUE_ACCENT).to_corner(UL, buff=0.3)
        self.play(FadeIn(step1_title))
        self.wait(0.3)

        # Subtract c from both sides
        eq1_1 = MathTex("ax^2 + bx", "= -c", color=GOLD_ACCENT).move_to(equation)
        minus_c = MathTex("-c", color=TEXT_COLOR).next_to(equation[0][5], RIGHT, buff=0.2)
        arrow_c = Arrow(equation[0][5].get_center(), minus_c.get_center(), buff=0.1, color=TEXT_COLOR).set_stroke(width=2)
        
        self.play(
            TransformMatchingTex(equation, eq1_1, transform_mobject=True),
            FadeOut(equation[0][5]) # Fade out the 'c' from original
        )
        self.wait(0.7)

        # Divide by a
        eq1_2 = MathTex("x^2 + \\frac{b}{a}x", "= -\\frac{c}{a}", color=GOLD_ACCENT).move_to(eq1_1)
        divide_a = Text("/a", font_size=25, color=TEXT_COLOR).next_to(eq1_1.get_right(), RIGHT, buff=0.2)
        self.play(
            ReplacementTransform(eq1_1, eq1_2),
            FadeIn(divide_a),
            run_time=1
        )
        self.play(FadeOut(divide_a))
        self.wait(1)

        current_equation = eq1_2 # Keep track for next transform

        # --- Beat 2: Completing the Square - Intuition and adding term ---
        self.play(FadeOut(step1_title))
        step2_title = Text("Step 2: Complete the Square", font_size=30, color=BLUE_ACCENT).to_corner(UL, buff=0.3)
        self.play(FadeIn(step2_title))
        self.wait(0.3)

        # Focus on the bx/a term and its transformation
        b_over_a_term = MathTex("\\frac{b}{a}", color=GOLD_ACCENT).scale(1.2).next_to(current_equation, RIGHT, buff=1.5).shift(UP*0.5)
        self.play(FadeIn(b_over_a_term))
        self.wait(0.5)

        # Visualizing the (b/2a)^2 addition
        half_b_over_a = MathTex("\\frac{b}{2a}", color=BLUE_ACCENT).next_to(b_over_a_term, DOWN, buff=0.6)
        arrow_half = Arrow(b_over_a_term.get_bottom(), half_b_over_a.get_top(), buff=0.1, color=TEXT_COLOR)
        label_half = Text("Half it", font_size=20, color=TEXT_COLOR).next_to(arrow_half, RIGHT, buff=0.1)
        self.play(GrowArrow(arrow_half), Write(label_half), FadeIn(half_b_over_a))
        self.wait(0.7)

        square_half_term = MathTex("(\\frac{b}{2a})^2", color=GOLD_ACCENT).next_to(half_b_over_a, DOWN, buff=0.6)
        arrow_square = Arrow(half_b_over_a.get_bottom(), square_half_term.get_top(), buff=0.1, color=TEXT_COLOR)
        label_square = Text("Square it", font_size=20, color=TEXT_COLOR).next_to(arrow_square, RIGHT, buff=0.1)
        self.play(GrowArrow(arrow_square), Write(label_square), FadeIn(square_half_term))
        self.wait(1)

        # Add (b/2a)^2 to both sides of the main equation
        self.play(FadeOut(b_over_a_term, half_b_over_a, arrow_half, label_half, arrow_square, label_square))
        
        eq2_1 = MathTex(
            "x^2 + \\frac{b}{a}x + (\\frac{b}{2a})^2",
            " = -\\frac{c}{a} + (\\frac{b}{2a})^2",
            color=GOLD_ACCENT
        ).move_to(current_equation)
        self.play(TransformMatchingTex(current_equation, eq2_1))
        self.wait(1)

        current_equation = eq2_1

        # --- Beat 3: Factor LHS and simplify RHS ---
        self.play(FadeOut(step2_title))
        step3_title = Text("Step 3: Factor & Simplify", font_size=30, color=BLUE_ACCENT).to_corner(UL, buff=0.3)
        self.play(FadeIn(step3_title))
        self.wait(0.3)

        # Factor LHS
        eq3_1 = MathTex("(x + \\frac{b}{2a})^2", "= -\\frac{c}{a} + \\frac{b^2}{4a^2}", color=GOLD_ACCENT).move_to(current_equation)
        self.play(TransformMatchingTex(current_equation, eq3_1))
        self.wait(1)

        # Simplify RHS by finding a common denominator
        eq3_2 = MathTex("(x + \\frac{b}{2a})^2", "= \\frac{b^2}{4a^2} - \\frac{4ac}{4a^2}", color=GOLD_ACCENT).move_to(eq3_1)
        self.play(TransformMatchingTex(eq3_1, eq3_2, key_map={"\\frac{b^2}{4a^2}": "\\frac{b^2}{4a^2}", "-\\frac{c}{a}": "-\\frac{4ac}{4a^2}"}))
        self.wait(0.7)

        eq3_3 = MathTex("(x + \\frac{b}{2a})^2", "= \\frac{b^2 - 4ac}{4a^2}", color=GOLD_ACCENT).move_to(eq3_2)
        self.play(TransformMatchingTex(eq3_2, eq3_3))
        self.wait(1)

        current_equation = eq3_3

        # --- Beat 4: Take square root of both sides ---
        self.play(FadeOut(step3_title))
        step4_title = Text("Step 4: Take Square Root", font_size=30, color=BLUE_ACCENT).to_corner(UL, buff=0.3)
        self.play(FadeIn(step4_title))
        self.wait(0.3)

        # Take square root
        eq4_1 = MathTex("x + \\frac{b}{2a}", "= \\pm\\sqrt{\\frac{b^2 - 4ac}{4a^2}}", color=GOLD_ACCENT).move_to(current_equation)
        self.play(TransformMatchingTex(current_equation, eq4_1))
        self.wait(1)

        # Simplify denominator of sqrt (sqrt(4a^2) = 2a)
        eq4_2 = MathTex("x + \\frac{b}{2a}", "= \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT).move_to(eq4_1)
        self.play(TransformMatchingTex(eq4_1, eq4_2, key_map={"\\sqrt{\\frac{b^2 - 4ac}{4a^2}}": "\\frac{\\sqrt{b^2 - 4ac}}{2a}"}))
        self.wait(1)

        current_equation = eq4_2

        # --- Beat 5: Isolate x ---
        self.play(FadeOut(step4_title))
        step5_title = Text("Step 5: Isolate x", font_size=30, color=BLUE_ACCENT).to_corner(UL, buff=0.3)
        self.play(FadeIn(step5_title))
        self.wait(0.3)

        # Subtract b/2a from both sides
        eq5_1 = MathTex("x", "= -\\frac{b}{2a} \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT).move_to(current_equation)
        self.play(TransformMatchingTex(current_equation, eq5_1))
        self.wait(1)

        # Combine terms under a single fraction
        final_derivation = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", color=BLUE_ACCENT).scale(1.2).move_to(eq5_1)
        self.play(TransformMatchingTex(eq5_1, final_derivation))
        self.wait(2)

        self.play(FadeOut(step5_title), FadeOut(final_formula_small)) # Fade out the persistent reminder and current formula

        # --- Recap Card ---
        recap_card = Rectangle(width=10, height=6, color=GOLD_ACCENT, fill_opacity=0.1, stroke_width=3).center()
        recap_title = Text("Recap: Formula Derivation Steps", font_size=40, color=GOLD_ACCENT).move_to(recap_card.get_top() + UP*0.5)
        
        recap_points_text = [
            "1. Standard Form $\\rightarrow ax^2 + bx + c = 0$",
            "2. Isolate constant, divide by '$a$'.",
            "3. Complete the square: add $(b/2a)^2$ to both sides.",
            "4. Factor LHS, simplify RHS (common denominator).",
            "5. Take the square root of both sides (remember $\\pm$!).",
            "6. Isolate '$x$' to reveal the Quadratic Formula!"
        ]
        recap_points = VGroup(*[
            MathTex(point, color=TEXT_COLOR, font_size=30).align_to(recap_card.get_left(), LEFT).shift(RIGHT*0.5)
            for point in recap_points_text
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(recap_title, DOWN, buff=0.5)

        self.play(Create(recap_card), FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.7, run_time=5))
        self.wait(3)

        self.play(FadeOut(recap_card, recap_title, recap_points, final_derivation)) # Fade out the recap card and also the derived formula from the last step if it was still there.
        self.wait(1)