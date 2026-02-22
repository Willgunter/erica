from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_C = BLUE_E  # High contrast blue
        GOLD_C = GOLD_E  # High contrast gold
        WHITE_C = WHITE

        # --- Beat 1: The Goal ---
        title = Text("Deriving the Quadratic Formula", font_size=45, color=WHITE_C).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        initial_equation = MathTex(
            "ax^2 + bx + c = 0",
            color=WHITE_C
        ).next_to(title, DOWN, buff=1.0).scale(1.2)

        question_mark = Text("x = ?", font_size=40, color=GOLD_C).next_to(initial_equation, DOWN, buff=0.8)

        self.play(FadeIn(initial_equation, shift=UP))
        self.play(Write(question_mark))
        self.wait(1.5)
        self.play(FadeOut(question_mark, shift=DOWN), FadeOut(title, shift=UP))
        self.wait(0.5)

        # --- Beat 2: Normalize the leading coefficient ---
        # ax^2 + bx + c = 0
        # Divide by a
        # x^2 + (b/a)x + (c/a) = 0
        eq1 = initial_equation
        self.play(eq1.animate.center().scale(1.0)) # Bring it to center for the first step

        divide_a_text = Text("Divide by a", font_size=30, color=BLUE_C).next_to(eq1, UP, buff=0.5)
        self.play(Write(divide_a_text))
        self.wait(0.5)

        # Prepare the target equation after division
        eq2 = MathTex(
            "x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0",
            color=WHITE_C
        ).center()

        # Animate the division visually
        div_anims = []
        for term_idx in [0, 1, 2]: # For ax^2, bx, c
            term = eq1[0][term_idx] # Access the term in MathTex
            div_line = Line(term.get_corner(DOWN + LEFT), term.get_corner(UP + RIGHT), stroke_width=2, color=GOLD_C)
            div_a = MathTex("a", color=GOLD_C).next_to(div_line, DOWN, buff=0.05).scale(0.7)
            div_anims.append(FadeIn(VGroup(div_line, div_a)))
        
        div_anims.append(FadeOut(divide_a_text))
        self.play(*div_anims)
        self.wait(0.5)

        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1.5)

        # --- Beat 3: Isolate x terms for completing the square ---
        # x^2 + (b/a)x = -c/a
        eq3 = eq2 # Continue from eq2
        
        move_c_text = Text("Move c/a to right side", font_size=30, color=BLUE_C).next_to(eq3, UP, buff=0.5)
        self.play(Write(move_c_text))
        self.wait(0.5)

        eq4 = MathTex(
            "x^2 + \\frac{b}{a}x = -\\frac{c}{a}",
            color=WHITE_C
        ).center()
        
        # Animate c/a moving and changing sign
        c_a_term = eq3.get_part_by_tex("+\\frac{c}{a}")
        minus_c_a_target = eq4.get_part_by_tex("-\\frac{c}{a}")

        self.play(
            FadeOut(c_a_term, target_position=minus_c_a_target.get_center(), shift=LEFT*2), # Simulate move
            TransformMatchingTex(eq3, eq4, transform_mobject=False) # Match the rest
        )
        self.play(FadeOut(move_c_text))
        self.wait(1.5)

        # --- Beat 4: Completing the Square ---
        # x^2 + (b/a)x + (b/2a)^2 = -c/a + (b/2a)^2
        # (x + b/2a)^2 = (b^2 - 4ac) / 4a^2
        eq5_init = eq4
        
        middle_coeff = MathTex("\\frac{b}{a}", color=GOLD_C).scale(1.2).next_to(eq5_init, UP, buff=0.8)
        self.play(FadeIn(middle_coeff, shift=UP))
        self.wait(0.5)

        half_coeff = MathTex(
            "\\left( \\frac{1}{2} \\cdot \\frac{b}{a} \\right)^2 = \\left( \\frac{b}{2a} \\right)^2",
            color=BLUE_C
        ).next_to(middle_coeff, DOWN, buff=0.3)
        self.play(Write(half_coeff))
        self.wait(0.7)

        add_to_sides_text = Text("Add this to both sides:", font_size=30, color=GOLD_C).next_to(eq5_init, UP, buff=0.5)
        self.play(FadeTransform(VGroup(middle_coeff, half_coeff), add_to_sides_text))
        self.wait(0.5)

        eq5 = MathTex(
            "x^2 + \\frac{b}{a}x + \\left(\\frac{b}{2a}\\right)^2 = -\\frac{c}{a} + \\left(\\frac{b}{2a}\\right)^2",
            color=WHITE_C
        ).center().scale(1.0)
        
        eq5.get_parts_by_tex("(\\frac{b}{2a})^2")[0].set_color(BLUE_C)
        eq5.get_parts_by_tex("(\\frac{b}{2a})^2")[1].set_color(BLUE_C)
        
        self.play(TransformMatchingTex(eq5_init, eq5))
        self.play(FadeOut(add_to_sides_text))
        self.wait(1.5)

        factor_text = Text("Factor & Simplify:", font_size=30, color=GOLD_C).next_to(eq5, UP, buff=0.5)
        self.play(Write(factor_text))
        self.wait(0.5)

        eq6 = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2 = \\frac{b^2 - 4ac}{4a^2}",
            color=WHITE_C
        ).center().scale(1.0)
        
        self.play(TransformMatchingTex(eq5, eq6))
        self.play(FadeOut(factor_text))
        self.wait(1.5)

        # --- Beat 5: Solve for x ---
        # Take square root, isolate x
        eq7_init = eq6
        self.play(eq7_init.animate.center().scale(1.2))
        self.wait(0.5)

        sqrt_text = Text("Take square root:", font_size=30, color=BLUE_C).next_to(eq7_init, UP, buff=0.5)
        self.play(Write(sqrt_text))
        self.wait(0.5)

        eq7 = MathTex(
            "x + \\frac{b}{2a} = \\pm\\sqrt{\\frac{b^2 - 4ac}{4a^2}}",
            color=WHITE_C
        ).center().scale(1.2)
        eq7.get_part_by_tex("\\pm").set_color(GOLD_C)

        self.play(TransformMatchingTex(eq7_init, eq7))
        self.wait(1.0)

        eq8 = MathTex(
            "x + \\frac{b}{2a} = \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}",
            color=WHITE_C
        ).center().scale(1.2)
        eq8.get_part_by_tex("\\pm").set_color(GOLD_C)

        self.play(TransformMatchingTex(eq7, eq8))
        self.play(FadeOut(sqrt_text)) # Fade out old text

        isolate_text = Text("Isolate x:", font_size=30, color=BLUE_C).next_to(eq8, UP, buff=0.5)
        self.play(Write(isolate_text))
        self.wait(0.5)

        eq9 = MathTex(
            "x = -\\frac{b}{2a} \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}",
            color=WHITE_C
        ).center().scale(1.2)
        eq9.get_part_by_tex("\\pm").set_color(GOLD_C)
        eq9.get_part_by_tex("-\\frac{b}{2a}").set_color(BLUE_C)

        self.play(TransformMatchingTex(eq8, eq9))
        self.wait(1.0)

        eq10 = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=WHITE_C
        ).center().scale(1.2)
        eq10.get_part_by_tex("\\pm").set_color(GOLD_C)

        self.play(TransformMatchingTex(eq9, eq10))
        self.play(FadeOut(isolate_text))
        self.wait(2.0)

        # --- Recap Card ---
        self.play(FadeOut(eq10, shift=UP))
        
        recap_title = Text("The Quadratic Formula", font_size=50, color=WHITE_C).to_edge(UP)
        self.play(Write(recap_title))

        final_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=GOLD_C,
            font_size=80
        ).center()
        
        self.play(FadeIn(final_formula, shift=DOWN))
        self.wait(3)
        self.play(FadeOut(recap_title, final_formula))
        self.wait(0.5)