from manim import *

class ApplyingQuadraticFormula(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        blue_color = BLUE_C
        gold_color = GOLD_C
        white_color = WHITE
        
        # --- Beat 1: Visual Hook & Problem Statement ---
        # 1.1 Axes and Parabola
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-6, 6, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": blue_color, "stroke_opacity": 0.5},
            tips=False
        ).add_coordinates()
        
        # Example parabola: y = x^2 - 2x - 3, roots at x=-1, x=3
        quadratic_function = lambda x: x**2 - 2*x - 3
        parabola = axes.plot(quadratic_function, color=gold_color, stroke_width=4)
        
        # Highlight roots
        root1_dot = Dot(axes.c2p(-1, 0), color=white_color, radius=0.08)
        root2_dot = Dot(axes.c2p(3, 0), color=white_color, radius=0.08)
        
        # Text
        title = Text("Applying the Quadratic Formula", color=white_color).to_edge(UP)
        problem_statement1 = Text("Finding where a curve crosses the x-axis...", color=white_color).scale(0.8)
        problem_statement2 = Text("...can be tricky!", color=white_color).scale(0.8)
        
        self.play(FadeIn(title, shift=UP), run_time=0.8)
        self.play(Create(axes), Create(parabola), run_time=2)
        self.play(FadeIn(root1_dot, scale_factor=0.5), FadeIn(root2_dot, scale_factor=0.5), run_time=1)
        self.play(Write(problem_statement1.next_to(parabola, UP, buff=0.8)), run_time=1.5)
        self.play(Transform(problem_statement1, problem_statement2.next_to(parabola, UP, buff=0.8)), run_time=1)
        
        self.play(
            FadeOut(root1_dot), FadeOut(root2_dot), 
            FadeOut(problem_statement1), 
            parabola.animate.set_stroke(opacity=0.3), 
            axes.animate.set_opacity(0.3),
            run_time=1.5
        )

        # --- Beat 2: Standard Form & The Formula Introduction ---
        # Standard Form
        std_form_text = MathTex("ax^2 + bx + c = 0", color=gold_color).scale(1.2)
        std_form_label = Text("Standard Quadratic Form", color=white_color).next_to(std_form_text, DOWN)
        
        self.play(Write(std_form_text), run_time=1.5)
        self.play(Write(std_form_label), run_time=1)
        
        # Quadratic Formula
        quad_formula_text = MathTex(
            "x = ", 
            "{-b \\pm \\sqrt{b^2 - 4ac}}", 
            "\\over {2a}", 
            color=blue_color
        ).scale(1.2).shift(DOWN*1.5)
        
        formula_label = Text("The Quadratic Formula", color=white_color).next_to(quad_formula_text, DOWN)
        
        self.play(
            FadeOut(std_form_label, shift=DOWN),
            std_form_text.animate.to_corner(UL).scale(0.8),
            Write(quad_formula_text),
            run_time=2.5
        )
        self.play(Write(formula_label), run_time=1)
        self.play(FadeOut(formula_label), run_time=0.8)

        # --- Beat 3: Identifying a, b, c from an Example ---
        example_eq = MathTex("2x^2 + 5x - 3 = 0", color=white_color).scale(1.2)
        example_eq.move_to(quad_formula_text.get_center())

        self.play(ReplacementTransform(quad_formula_text, example_eq), run_time=1)
        
        a_val = MathTex("a = 2", color=gold_color).next_to(example_eq, DOWN, buff=0.5).shift(LEFT*2)
        b_val = MathTex("b = 5", color=gold_color).next_to(example_eq, DOWN, buff=0.5)
        c_val = MathTex("c = -3", color=gold_color).next_to(example_eq, DOWN, buff=0.5).shift(RIGHT*2)
        
        # Highlight a, b, c in the example equation
        a_highlight = SurroundingRectangle(example_eq[0:2], color=gold_color, buff=0.1) # 2x^2
        b_highlight = SurroundingRectangle(example_eq[3:5], color=gold_color, buff=0.1) # + 5x
        c_highlight = SurroundingRectangle(example_eq[6:8], color=gold_color, buff=0.1) # - 3
        
        self.play(Create(a_highlight), run_time=0.8)
        self.play(Write(a_val), run_time=0.8)
        self.play(ReplacementTransform(a_highlight, b_highlight), run_time=0.8)
        self.play(Write(b_val), run_time=0.8)
        self.play(ReplacementTransform(b_highlight, c_highlight), run_time=0.8)
        self.play(Write(c_val), run_time=0.8)
        
        abc_values = VGroup(a_val, b_val, c_val) 
        
        self.play(FadeOut(example_eq, shift=UP), FadeOut(c_highlight), abc_values.animate.shift(UP*1.5), run_time=1.5)

        # --- Beat 4: Plugging In and Solving ---
        # Bring back the formula template
        quad_formula_template = MathTex(
            "x = ", 
            "{-b \\pm \\sqrt{b^2 - 4ac}}", 
            "\\over {2a}", 
            color=blue_color
        ).scale(1.2)
        self.play(Write(quad_formula_template), run_time=1)
        
        # Create 'placeholders' for the numbers to move into
        b_target1 = MathTex("5", color=gold_color).move_to(quad_formula_template[1][1]) # -b
        b_target2 = MathTex("5", color=gold_color).move_to(quad_formula_template[1][5]) # b^2
        a_target1 = MathTex("2", color=gold_color).move_to(quad_formula_template[2][2]) # 2a
        a_target2 = MathTex("2", color=gold_color).move_to(quad_formula_template[1][8]) # 4ac (a part)
        c_target = MathTex("-3", color=gold_color).move_to(quad_formula_template[1][9]) # 4ac (c part)
        
        # Animating the values 'dropping in'
        self.play(
            ReplacementTransform(a_val[0], a_target1), # a from 'a=2' to '2a'
            ReplacementTransform(a_val[0].copy(), a_target2), # a from 'a=2' to '4ac'
            ReplacementTransform(b_val[0], b_target1), # b from 'b=5' to '-b'
            ReplacementTransform(b_val[0].copy(), b_target2), # b from 'b=5' to 'b^2'
            ReplacementTransform(c_val[0], c_target), # c from 'c=-3' to '-4ac'
            FadeOut(abc_values, shift=DOWN), # Fade out a=2, b=5, c=-3 labels
            run_time=2.5
        )
        
        # Now, the full filled formula is ready to be transitioned to
        filled_formula = MathTex(
            "x = ", 
            "{-5 \\pm \\sqrt{(5)^2 - 4(2)(-3)}}", 
            "\\over {2(2)}", 
            color=blue_color
        ).scale(1.2)
        
        self.play(
            FadeOut(VGroup(b_target1, b_target2, a_target1, a_target2, c_target)), # Fade out temporary number mobjects
            TransformMatchingTex(quad_formula_template, filled_formula, path_arc=PI/2),
            run_time=1.5
        )

        # Calculate discriminant (b^2 - 4ac)
        discriminant_group = VGroup(filled_formula[1][5:15]) # (5)^2 - 4(2)(-3)
        discriminant_calc = MathTex("25 - (-24)", "= 49", color=white_color).scale(0.9)
        discriminant_calc.next_to(filled_formula, DOWN, buff=0.5)

        arrow_to_disc = Arrow(filled_formula[1][7].get_bottom(), discriminant_calc[0].get_top(), buff=0.2, color=gold_color)
        
        self.play(Create(arrow_to_disc), Write(discriminant_calc[0]), run_time=1.2)
        self.play(Write(discriminant_calc[1]), run_time=0.8)
        
        # Replace discriminant in formula
        simplified_formula = MathTex(
            "x = ", 
            "{-5 \\pm \\sqrt{49}}", 
            "\\over {4}", 
            color=blue_color
        ).scale(1.2)
        
        simplified_formula.move_to(filled_formula.get_center())

        self.play(
            FadeOut(arrow_to_disc, shift=UP), 
            FadeOut(discriminant_calc, shift=UP),
            TransformMatchingTex(filled_formula, simplified_formula),
            run_time=1.5
        )
        
        # Calculate sqrt(49)
        sqrt_simplified_formula = MathTex(
            "x = ", 
            "{-5 \\pm 7}", 
            "\\over {4}", 
            color=blue_color
        ).scale(1.2)

        self.play(TransformMatchingTex(simplified_formula, sqrt_simplified_formula), run_time=1)
        
        # Split into x1 and x2
        x1_eq = MathTex("x_1 = {(-5 + 7)} / {4}", "= {2} / {4}", "= 0.5", color=gold_color).scale(1)
        x2_eq = MathTex("x_2 = {(-5 - 7)} / {4}", "= {-12} / {4}", "= -3", color=gold_color).scale(1)
        
        x1_eq.next_to(sqrt_simplified_formula, LEFT, buff=1.5).shift(DOWN*0.5)
        x2_eq.next_to(sqrt_simplified_formula, RIGHT, buff=1.5).shift(DOWN*0.5)
        
        self.play(FadeTransform(sqrt_simplified_formula.copy(), x1_eq[0]), FadeTransform(sqrt_simplified_formula.copy(), x2_eq[0]), run_time=1)
        self.play(Write(x1_eq[1:]), Write(x2_eq[1:]), run_time=1.5)
        
        # Clean up equations for next beat
        self.play(
            FadeOut(sqrt_simplified_formula, shift=UP),
            x1_eq.animate.to_corner(UL).scale(0.8),
            x2_eq.animate.to_corner(UR).scale(0.8),
            run_time=1
        )

        # --- Beat 5: Visualizing the Solutions ---
        # Set up a new graph for the example equation 2x^2 + 5x - 3 = 0
        # Roots are at x = 0.5 and x = -3
        new_axes = Axes(
            x_range=[-4, 1, 1],
            y_range=[-7, 1, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": blue_color, "stroke_opacity": 0.5},
            tips=False
        ).add_coordinates()
        
        example_quadratic_function = lambda x: 2*x**2 + 5*x - 3
        example_parabola = new_axes.plot(example_quadratic_function, color=gold_color, stroke_width=4)
        
        # Dots for the roots
        root1_calc_dot = Dot(new_axes.c2p(0.5, 0), color=white_color, radius=0.08)
        root2_calc_dot = Dot(new_axes.c2p(-3, 0), color=white_color, radius=0.08)
        
        root1_label = MathTex("x_1 = 0.5", color=white_color).scale(0.7).next_to(root1_calc_dot, UP, buff=0.2)
        root2_label = MathTex("x_2 = -3", color=white_color).scale(0.7).next_to(root2_calc_dot, UP, buff=0.2)
        
        self.play(Create(new_axes), Create(example_parabola), run_time=2)
        
        self.play(
            FadeIn(root1_calc_dot, scale_factor=0.5), 
            Write(root1_label),
            FadeOut(x1_eq, shift=DOWN), # Fade out the old x1_eq from the corner
            run_time=1.5
        )
        self.play(
            FadeIn(root2_calc_dot, scale_factor=0.5), 
            Write(root2_label),
            FadeOut(x2_eq, shift=DOWN), # Fade out the old x2_eq from the corner
            run_time=1.5
        )
        
        # --- Recap Card ---
        self.play(
            FadeOut(new_axes), 
            FadeOut(example_parabola), 
            FadeOut(root1_calc_dot), 
            FadeOut(root2_calc_dot), 
            FadeOut(root1_label), 
            FadeOut(root2_label),
            FadeOut(std_form_text), # Fade out the standard form from the corner
            run_time=2
        )
        
        recap_title = Text("Recap: How to Apply", color=white_color).to_edge(UP)
        
        step1 = Text("1. Standard Form: ax² + bx + c = 0", color=white_color).shift(UP*1.5 + LEFT*0.5)
        step2 = Text("2. Identify a, b, c", color=white_color).next_to(step1, DOWN)
        step3 = Text("3. Plug into Formula:", color=white_color).next_to(step2, DOWN)
        step4 = MathTex("x = {-b \\pm \\sqrt{b^2 - 4ac}} / {2a}", color=blue_color).scale(1).next_to(step3, DOWN, buff=0.2)
        step5 = Text("4. Calculate and Simplify for x", color=white_color).next_to(step4, DOWN, buff=0.5)
        
        recap_group = VGroup(recap_title, step1, step2, step3, step4, step5)
        recap_group.arrange(DOWN, aligned_edge=LEFT, buff=0.5).center()
        
        self.play(FadeIn(recap_title, shift=UP), run_time=1)
        self.play(LaggedStart(
            Write(step1),
            Write(step2),
            Write(step3),
            Write(step4),
            Write(step5),
            lag_ratio=0.5
        ), run_time=4)
        self.play(FadeOut(recap_group), run_time=1)