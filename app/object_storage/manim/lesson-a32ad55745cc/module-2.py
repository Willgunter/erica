from manim import *

class FormulaWorksEveryQuadratic(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        ACCENT_BLUE = BLUE_E
        ACCENT_GOLD = GOLD_E

        # --- Beat 1: Visual Hook & Introduction to Quadratic Form ---
        self.camera.background_color = config.background_color

        # Visual hook: A dynamic parabola forming
        title = Tex("Formula Works Every Quadratic", color=ACCENT_GOLD).scale(1.2)
        self.play(Write(title))
        self.wait(0.5)

        # Set up axes for the demonstration
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 5, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": GRAY_B},
            tips=False
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # A generic parabola function for initial display
        def func_quadratic_initial(x):
            return 0.5 * x**2 + 1.5 * x + 1.5

        parabola_initial = axes.get_graph(func_quadratic_initial, color=ACCENT_BLUE, x_range=[-4, 4])

        self.play(
            FadeOut(title),
            Create(axes),
            Write(axes_labels),
            Create(parabola_initial),
            run_time=1.5
        )
        self.wait(0.5)

        # Introduce the general form
        quadratic_form_equation = MathTex(
            "ax^2 + bx + c = 0",
            color=ACCENT_GOLD
        ).to_edge(UP).shift(LEFT * 2.5)
        
        a_not_zero_early = MathTex("a \\neq 0", color=ACCENT_BLUE).next_to(quadratic_form_equation, DOWN)

        self.play(Write(quadratic_form_equation), Write(a_not_zero_early))
        self.wait(1)

        # --- Beat 2: Understanding ax^2 + bx + c - Geometric Intuition ---
        # Show 'c' (y-intercept)
        c_label = MathTex("c", color=ACCENT_GOLD).next_to(quadratic_form_equation, DOWN, buff=0.8).align_to(quadratic_form_equation, LEFT)
        c_effect_text = Tex("controls y-intercept", color=GRAY_A).next_to(c_label, RIGHT)

        parabola_c_shift_down = axes.get_graph(lambda x: 0.5 * x**2 + 1.5 * x + 0.5, color=ACCENT_BLUE)
        parabola_c_shift_up = axes.get_graph(lambda x: 0.5 * x**2 + 1.5 * x + 2.5, color=ACCENT_BLUE)

        # Highlight 'c' in the formula
        c_in_form = quadratic_form_equation.get_parts_by_tex("c")
        self.play(
            FadeTransform(a_not_zero_early, c_label),
            Write(c_effect_text),
            c_in_form.animate.set_color(ACCENT_GOLD),
        )
        self.play(
            ReplacementTransform(parabola_initial, parabola_c_shift_down),
            run_time=0.8
        )
        self.play(
            ReplacementTransform(parabola_c_shift_down, parabola_c_shift_up),
            run_time=0.8
        )
        self.play(
            ReplacementTransform(parabola_c_shift_up, parabola_initial), # Back to original
            FadeOut(c_label, c_effect_text),
            c_in_form.animate.set_color(ACCENT_GOLD) # Reset color
        )
        self.wait(0.5)

        # Show 'a' (concavity/width)
        a_label = MathTex("a", color=ACCENT_GOLD).next_to(quadratic_form_equation, DOWN, buff=0.8).align_to(quadratic_form_equation, LEFT)
        a_effect_text = Tex("controls concavity & width", color=GRAY_A).next_to(a_label, RIGHT)
        
        parabola_a_narrow = axes.get_graph(lambda x: 1.0 * x**2 + 1.5 * x + 1.5, color=ACCENT_BLUE) # Narrower, opens up
        parabola_a_inverted = axes.get_graph(lambda x: -0.5 * x**2 + 1.5 * x + 1.5, color=ACCENT_BLUE) # Opens down

        # Highlight 'a' in the formula
        a_in_form = quadratic_form_equation.get_parts_by_tex("ax^2")
        self.play(
            Write(a_label),
            Write(a_effect_text),
            a_in_form.animate.set_color(ACCENT_GOLD),
        )
        self.play(
            ReplacementTransform(parabola_initial, parabola_a_narrow),
            run_time=0.8
        )
        self.play(
            ReplacementTransform(parabola_a_narrow, parabola_a_inverted),
            run_time=0.8
        )
        self.play(
            ReplacementTransform(parabola_a_inverted, parabola_initial), # Back to original
            FadeOut(a_label, a_effect_text),
            a_in_form.animate.set_color(ACCENT_GOLD) # Reset color
        )
        self.wait(0.5)

        # --- Beat 3: The Vertex - The Key Idea ---
        # Re-introduce `a != 0`
        a_not_zero_reiterate = MathTex("a \\neq 0", color=ACCENT_BLUE).next_to(quadratic_form_equation, DOWN)
        self.play(FadeIn(a_not_zero_reiterate))

        # Focus on the vertex and axis of symmetry
        # (Vertex for original parabola: x = -1.5, y = 0.5*(1.5)^2 - 1.5*1.5 + 1.5 = 0.375)
        vertex_coords_orig = (-1.5, func_quadratic_initial(-1.5))
        vertex_dot = Dot(axes.c2p(*vertex_coords_orig), color=ACCENT_GOLD)
        vertex_text = Tex("Vertex", color=ACCENT_GOLD).next_to(vertex_dot, UP + LEFT, buff=0.1)

        axis_of_symmetry_line = axes.get_vertical_line(axes.c2p(vertex_coords_orig[0], 0), color=ACCENT_GOLD, stroke_width=2)
        axis_of_symmetry_label = MathTex("x = -{b \\over 2a}", color=ACCENT_GOLD).next_to(axis_of_symmetry_line, RIGHT, buff=0.1)

        self.play(
            FadeOut(quadratic_form_equation, a_not_zero_reiterate),
            Create(vertex_dot),
            Write(vertex_text),
            run_time=1
        )
        self.wait(0.5)

        self.play(
            Create(axis_of_symmetry_line),
            Write(axis_of_symmetry_label),
            run_time=1
        )
        self.wait(1)

        # --- Beat 4: Deriving the Roots - Completing the Square Intuition ---
        # Show roots (x-intercepts for func_quadratic_initial)
        # Using the quadratic formula for 0.5x^2 + 1.5x + 1.5 = 0
        # Discriminant: 1.5^2 - 4*0.5*1.5 = 2.25 - 3 = -0.75 (no real roots for initial parabola)
        # Adjust parabola to have real roots for demonstration
        parabola_with_roots_func = lambda x: 0.5 * x**2 + 1.5 * x + 0.5
        parabola_with_roots = axes.get_graph(parabola_with_roots_func, color=ACCENT_BLUE, x_range=[-4, 4])
        
        # New vertex for parabola_with_roots: x = -1.5, y = 0.5*(-1.5)^2 + 1.5*(-1.5) + 0.5 = 1.125 - 2.25 + 0.5 = -0.625
        vertex_coords_roots = (-1.5, parabola_with_roots_func(-1.5))
        new_vertex_dot = Dot(axes.c2p(*vertex_coords_roots), color=ACCENT_GOLD)
        new_axis_of_symmetry_line = axes.get_vertical_line(axes.c2p(vertex_coords_roots[0], 0), color=ACCENT_GOLD, stroke_width=2)

        # Calculate roots for 0.5x^2 + 1.5x + 0.5 = 0
        # x = [-1.5 ± sqrt(1.5^2 - 4*0.5*0.5)] / (2*0.5)
        # x = [-1.5 ± sqrt(2.25 - 1)] / 1
        # x = -1.5 ± sqrt(1.25) = -1.5 ± 1.118
        root1_val = -1.5 - 1.118
        root2_val = -1.5 + 1.118
        
        root1_dot = Dot(axes.c2p(root1_val, 0), color=ACCENT_BLUE)
        root2_dot = Dot(axes.c2p(root2_val, 0), color=ACCENT_BLUE)

        roots_text = Tex("Roots ($y=0$)", color=ACCENT_BLUE).next_to(root2_dot, DOWN+RIGHT, buff=0.1)

        self.play(
            Transform(parabola_initial, parabola_with_roots),
            Transform(vertex_dot, new_vertex_dot),
            Transform(axis_of_symmetry_line, new_axis_of_symmetry_line),
            FadeOut(vertex_text)
        )
        self.play(
            Create(root1_dot),
            Create(root2_dot),
            Write(roots_text)
        )
        self.wait(1)

        # Illustrate symmetry with distance
        dist_offset_y = -1.0 # To show arrows below x-axis
        dist_arrow1 = Arrow(axes.c2p(vertex_coords_roots[0], dist_offset_y), axes.c2p(root1_val, dist_offset_y), buff=0, color=ACCENT_BLUE, max_stroke_width_to_length_ratio=0.08)
        dist_arrow2 = Arrow(axes.c2p(vertex_coords_roots[0], dist_offset_y), axes.c2p(root2_val, dist_offset_y), buff=0, color=ACCENT_BLUE, max_stroke_width_to_length_ratio=0.08)
        
        delta_x_label = MathTex("\\pm \\delta", color=ACCENT_BLUE).next_to(dist_arrow1, DOWN)

        self.play(
            Create(dist_arrow1),
            Create(dist_arrow2),
            FadeIn(delta_x_label)
        )
        self.wait(1)

        # Build the quadratic formula step-by-step
        # Part 1: Axis of symmetry
        formula_part1 = MathTex("x = -{b \\over 2a}", color=ACCENT_GOLD).move_to(axis_of_symmetry_label.get_center()).shift(UP)
        self.play(
            FadeOut(axis_of_symmetry_label),
            FadeOut(vertex_dot),
            FadeOut(roots_text),
            Transform(axis_of_symmetry_line, formula_part1)
        )
        self.wait(0.5)

        # Part 2: Plus/minus distance
        formula_part2 = MathTex("x = -{b \\over 2a} \\pm \\sqrt{\\dots}", color=ACCENT_GOLD).move_to(formula_part1)
        self.play(
            TransformMatchingTex(formula_part1, formula_part2),
            FadeOut(dist_arrow1, dist_arrow2, delta_x_label),
            parabola_with_roots.animate.set_color(GRAY_C), # Dim parabola
            root1_dot.animate.set_color(GRAY_C),
            root2_dot.animate.set_color(GRAY_C)
        )
        self.wait(1)

        # Part 3: The discriminant - the full quadratic formula
        quadratic_formula_final = MathTex(
            "x = {-b \\pm \\sqrt{b^2 - 4ac} \\over 2a}",
            color=ACCENT_GOLD
        ).scale(1.2).shift(UP * 2)

        self.play(
            FadeOut(axes, axes_labels, parabola_with_roots, root1_dot, root2_dot),
            TransformMatchingTex(formula_part2, quadratic_formula_final),
            run_time=2
        )
        self.wait(1)

        # --- Beat 5: The Full Formula & a ≠ 0 ---
        # Emphasize a != 0 again
        a_not_zero_final = MathTex("\\text{for } ax^2 + bx + c = 0 \\text{ where } a \\neq 0", color=ACCENT_BLUE).next_to(quadratic_formula_final, DOWN, buff=0.7)
        self.play(Write(a_not_zero_final))
        self.wait(1.5)

        # Briefly show why a=0 is different
        linear_case_text = Tex("If $a=0$, it's a linear equation:", color=GRAY_A).next_to(a_not_zero_final, DOWN, buff=0.5)
        linear_equation = MathTex("bx + c = 0", color=GRAY_A).next_to(linear_case_text, DOWN)
        linear_solution = MathTex("x = -{c \\over b}", color=GRAY_A).next_to(linear_equation, DOWN)
        
        self.play(
            FadeIn(linear_case_text),
            FadeIn(linear_equation),
            FadeIn(linear_solution)
        )
        self.wait(2)
        self.play(FadeOut(linear_case_text, linear_equation, linear_solution))
        self.wait(0.5)


        # --- Recap Card ---
        self.play(
            FadeOut(quadratic_formula_final, a_not_zero_final),
            run_time=1
        )

        recap_title = Tex("Recap: Quadratic Formula", color=ACCENT_GOLD).scale(1.2)
        recap_formula = MathTex(
            "x = {-b \\pm \\sqrt{b^2 - 4ac} \\over 2a}",
            color=ACCENT_BLUE
        ).scale(1.5).next_to(recap_title, DOWN, buff=0.8)
        recap_condition = Tex(
            "Applies to ALL $ax^2 + bx + c = 0$", 
            " (as long as $a \\neq 0$!)", 
            color=GRAY_A
        ).next_to(recap_formula, DOWN)
        recap_condition[0].set_color(ACCENT_GOLD)
        recap_condition[1].set_color(ACCENT_BLUE)

        self.play(
            Write(recap_title),
            FadeIn(recap_formula),
            LaggedStart(
                Write(recap_condition[0]),
                Write(recap_condition[1]),
                lag_ratio=0.5,
                run_time=2
            )
        )
        self.wait(3)
        self.play(FadeOut(recap_title, recap_formula, recap_condition))
        self.wait(1)