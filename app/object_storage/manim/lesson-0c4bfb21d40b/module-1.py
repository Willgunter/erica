from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = "#121212" # Dark background
        
        # --- Colors ---
        BLUE_ACCENT = "#87CEEB" # Sky Blue
        GOLD_ACCENT = "#FFD700" # Gold
        WHITE = "#FFFFFF"
        LIGHT_GRAY = "#CCCCCC"

        # --- Beat 0: Visual Hook & Introduction ---
        title = Text("Quadratic Formula Derivation", font_size=50, color=BLUE_ACCENT)
        subtitle = Text("Completing the Square", font_size=36, color=LIGHT_GRAY).next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(0.5)
        self.play(FadeOut(VGroup(title, subtitle)))

        # General quadratic equation
        eq_general = MathTex("ax^2 + bx + c = 0", color=WHITE)
        self.play(Write(eq_general))
        self.wait(0.5)
        
        goal_text = Text("Our Goal: Find x!", font_size=30, color=GOLD_ACCENT).to_edge(UP).shift(LEFT*3)
        self.play(Write(goal_text))
        self.wait(1)
        
        # --- Beat 1: Isolate x^2 term and coefficient 'a' ---
        # Divide by 'a'
        divide_by_a_text = Text("1. Divide by a (a ≠ 0)", font_size=28, color=LIGHT_GRAY).next_to(goal_text, DOWN, buff=0.5).align_to(goal_text, LEFT)
        self.play(Write(divide_by_a_text))
        self.wait(0.5)

        eq_div_a = MathTex(r"\frac{ax^2}{a} + \frac{bx}{a} + \frac{c}{a} = \frac{0}{a}", color=WHITE).move_to(eq_general)
        self.play(TransformMatchingTex(eq_general, eq_div_a))
        self.wait(0.5)

        eq1 = MathTex("x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0", color=WHITE).move_to(eq_div_a)
        self.play(TransformMatchingTex(eq_div_a, eq1))
        self.wait(0.5)

        # Move c/a to the right side
        move_c_text = Text("2. Move c/a to the right side", font_size=28, color=LIGHT_GRAY).next_to(divide_by_a_text, DOWN, buff=0.5).align_to(divide_by_a_text, LEFT)
        self.play(Write(move_c_text))
        self.wait(0.5)

        eq2 = MathTex("x^2 + \\frac{b}{a}x = -\\frac{c}{a}", color=WHITE).move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1)

        # --- Beat 2: Completing the Square - Geometric Intuition and Algebraic Step ---
        self.play(FadeOut(VGroup(divide_by_a_text, move_c_text, goal_text)))
        
        complete_square_text = Text("3. Complete the Square", font_size=28, color=LIGHT_GRAY).to_edge(UP).shift(LEFT*3)
        self.play(Write(complete_square_text))
        
        # Geometric representation
        x_side_length = 2
        b_over_2a_length = 0.5 # Visual placeholder length
        
        square_x2 = Square(side_length=x_side_length, color=BLUE_ACCENT, fill_opacity=0.7).shift(LEFT * 2 + DOWN * 0.5)
        label_x_left = MathTex("x", color=WHITE).next_to(square_x2.get_left(), LEFT).shift(UP*0.3)
        label_x_bottom = MathTex("x", color=WHITE).next_to(square_x2.get_bottom(), DOWN).shift(LEFT*0.3)
        label_x2_area = MathTex("x^2", color=WHITE).move_to(square_x2.get_center())

        rect_bx_half1 = Rectangle(width=x_side_length, height=b_over_2a_length, color=GOLD_ACCENT, fill_opacity=0.7).next_to(square_x2, UP, buff=0, aligned_edge=LEFT)
        rect_bx_half2 = Rectangle(width=b_over_2a_length, height=x_side_length, color=GOLD_ACCENT, fill_opacity=0.7).next_to(square_x2, RIGHT, buff=0, aligned_edge=UP)
        
        label_b_2a_top = MathTex(r"\frac{b}{2a}", color=WHITE).next_to(rect_bx_half1.get_center(), UP*0.5)
        label_b_2a_right = MathTex(r"\frac{b}{2a}", color=WHITE).next_to(rect_bx_half2.get_center(), RIGHT*0.5)
        
        # Initial visual group before adding the missing square
        initial_geometric_group = VGroup(
            square_x2, label_x_left, label_x_bottom, label_x2_area,
            rect_bx_half1, rect_bx_half2, label_b_2a_top, label_b_2a_right
        )

        self.play(eq2.animate.scale(0.7).to_edge(UP, buff=1).shift(RIGHT*3))
        
        self.play(
            Create(square_x2), 
            Write(label_x_left), 
            Write(label_x_bottom), 
            Write(label_x2_area)
        )
        self.wait(0.5)
        self.play(
            Create(rect_bx_half1), 
            Create(rect_bx_half2), 
            Write(label_b_2a_top), 
            Write(label_b_2a_right)
        )
        self.wait(1)

        missing_square_side = b_over_2a_length
        missing_square = Square(side_length=missing_square_side, color=BLUE_ACCENT, fill_opacity=0.5).next_to(rect_bx_half1, RIGHT, buff=0).next_to(rect_bx_half2, UP, buff=0)
        label_b_2a_squared = MathTex(r"\left(\frac{b}{2a}\right)^2", color=WHITE).move_to(missing_square.get_center())
        
        self.play(Create(missing_square), Write(label_b_2a_squared))
        self.wait(1)
        
        # Combine all geometric elements for animation
        full_geometric_group = VGroup(
            initial_geometric_group, missing_square, label_b_2a_squared
        )
        self.play(
            full_geometric_group.animate.scale(0.7).shift(LEFT*2 + DOWN*1.5), 
            FadeOut(label_x_left, label_x_bottom, label_x2_area, label_b_2a_top, label_b_2a_right, label_b_2a_squared)
        )
        
        # Add (b/2a)^2 to both sides of the equation
        eq3 = MathTex(r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \left(\frac{b}{2a}\right)^2", color=WHITE).move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1)

        # Left side becomes a perfect square
        eq4 = MathTex(r"\left(x + \frac{b}{2a}\right)^2 = -\frac{c}{a} + \frac{b^2}{4a^2}", color=WHITE).move_to(eq3)
        self.play(ReplacementTransform(eq3, eq4))
        self.wait(1)

        # --- Beat 3: Simplify Right Side & Square Root ---
        self.play(FadeOut(full_geometric_group, complete_square_text))
        
        simplify_right_text = Text("4. Simplify the right side", font_size=28, color=LIGHT_GRAY).to_edge(UP).shift(LEFT*3)
        self.play(Write(simplify_right_text))

        eq5 = MathTex(r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}", color=WHITE).move_to(eq4)
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(1)

        # Take square root of both sides
        sqrt_text = Text("5. Take the square root of both sides", font_size=28, color=LIGHT_GRAY).next_to(simplify_right_text, DOWN, buff=0.5).align_to(simplify_right_text, LEFT)
        self.play(Write(sqrt_text))
        
        eq6 = MathTex(r"x + \frac{b}{2a} = \pm\sqrt{\frac{b^2 - 4ac}{4a^2}}", color=WHITE).move_to(eq5)
        self.play(TransformMatchingTex(eq5, eq6))
        self.wait(1)

        # Simplify the square root
        eq7 = MathTex(r"x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2a}", color=WHITE).move_to(eq6)
        self.play(TransformMatchingTex(eq6, eq7))
        self.wait(1)

        # --- Beat 4: Final Isolation of x ---
        self.play(FadeOut(VGroup(simplify_right_text, sqrt_text)))
        
        isolate_x_text = Text("6. Isolate x", font_size=28, color=LIGHT_GRAY).to_edge(UP).shift(LEFT*3)
        self.play(Write(isolate_x_text))

        eq8 = MathTex(r"x = -\frac{b}{2a} \pm\frac{\sqrt{b^2 - 4ac}}{2a}", color=WHITE).move_to(eq7)
        self.play(TransformMatchingTex(eq7, eq8))
        self.wait(1)

        # Combine into final formula
        final_formula = MathTex(r"x = \frac{-b \pm\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT, font_size=50).move_to(eq8)
        self.play(ReplacementTransform(eq8, final_formula))
        self.wait(2)

        # --- Recap Card ---
        self.play(FadeOut(final_formula, isolate_x_text))
        
        recap_title = Text("Recap: Steps to Derive Quadratic Formula", font_size=40, color=BLUE_ACCENT)
        self.play(Write(recap_title))
        self.wait(0.5)
        
        recap_steps = VGroup(
            MathTex(r"\text{1. } ax^2 + bx + c = 0 \quad \xrightarrow{\div a} \quad x^2 + \frac{b}{a}x + \frac{c}{a} = 0"),
            MathTex(r"\text{2. } x^2 + \frac{b}{a}x = -\frac{c}{a}"),
            MathTex(r"\text{3. } x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \left(\frac{b}{2a}\right)^2"),
            MathTex(r"\text{4. } \left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}"),
            MathTex(r"\text{5. } x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2a}"),
            MathTex(r"\text{6. } x = \frac{-b \pm\sqrt{b^2 - 4ac}}{2a}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.7).next_to(recap_title, DOWN, buff=0.8)
        
        for i, step in enumerate(recap_steps):
            self.play(Write(step), run_time=1)
            
        final_highlight = SurroundingRectangle(recap_steps[-1], color=GOLD_ACCENT, buff=0.2)
        self.play(Create(final_highlight))
        
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_steps, final_highlight)))
        self.wait(0.5)