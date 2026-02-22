from manim import *

class SolvingQuadraticEquationsAlgebraically(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        # Custom colors for high contrast
        MY_BLUE = BLUE_C 
        MY_GOLD = GOLD_C 
        
        # --- Beat 1: Title Card & Visual Hook ---
        # Module Title
        title = MathTex("\\text{Solving Quadratic Equations Algebraically}", font_size=58, color=WHITE)
        objective = Text("Understand and apply algebraic methods to find roots", font_size=36, color=LIGHT_GRAY).next_to(title, DOWN, buff=0.8)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(objective, shift=DOWN), run_time=1)
        self.wait(1)
        
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(objective, shift=UP),
            run_time=0.8
        )
        self.wait(0.2)

        # Visual Hook: Dynamic Parabola Drawing
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            background_line_style={"stroke_color": DARK_GRAY, "stroke_width": 1, "stroke_opacity": 0.6}
        ).add_coordinates().to_edge(RIGHT, buff=1.0)
        
        func = lambda x: x**2 - 4
        graph = plane.get_graph(func, x_range=[-2.5, 2.5], color=MY_BLUE)
        
        # Text for definition of quadratic equation
        intro_text_1 = Text("What is a Quadratic Equation?", font_size=40, color=WHITE).to_edge(LEFT, buff=0.8).shift(UP*1.5)
        general_form_tex = MathTex("ax^2 + bx + c = 0", color=MY_GOLD).next_to(intro_text_1, DOWN, buff=0.7).align_to(intro_text_1, LEFT)
        intro_text_2 = Text("where 'a' must not be zero.", font_size=32, color=LIGHT_GRAY).next_to(general_form_tex, DOWN, buff=0.3).align_to(general_form_tex, LEFT)
        
        self.play(FadeIn(plane, shift=LEFT))
        # Create graph dynamically as a visual hook
        self.play(
            LaggedStart(
                Write(intro_text_1, run_time=1),
                Create(graph, run_time=2, rate_func=rate_functions.ease_out_sine),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)
        self.play(Write(general_form_tex))
        self.play(Write(intro_text_2))
        self.wait(1)

        # --- Beat 2: The Roots/Zeros ---
        self.play(
            FadeOut(intro_text_1, shift=UP),
            FadeOut(intro_text_2, shift=UP),
            general_form_tex.animate.move_to(LEFT * 3 + UP * 2) # Move general form up to make space
        )

        roots_text = Text("The 'Roots' or 'Zeros'", font_size=40, color=WHITE).next_to(general_form_tex, DOWN, buff=0.7).align_to(general_form_tex, LEFT)
        roots_definition = Text("Values of 'x' where the graph crosses the x-axis (y=0)", font_size=32, color=LIGHT_GRAY).next_to(roots_text, DOWN, buff=0.3).align_to(roots_text, LEFT)
        
        self.play(Write(roots_text))
        self.play(Write(roots_definition))
        self.wait(0.5)

        # Highlight roots on the graph with dots and labels
        root_1_coord = [-2, 0, 0]
        root_2_coord = [2, 0, 0]
        
        dot_1 = Dot(plane.c2p(*root_1_coord), color=MY_GOLD, radius=0.1)
        dot_2 = Dot(plane.c2p(*root_2_coord), color=MY_GOLD, radius=0.1)

        root_label_1 = MathTex("x_1 = -2", color=MY_GOLD).next_to(dot_1, DOWN + LEFT, buff=0.2)
        root_label_2 = MathTex("x_2 = 2", color=MY_GOLD).next_to(dot_2, DOWN + RIGHT, buff=0.2)

        self.play(FadeIn(dot_1, dot_2, scale=0.5))
        self.play(Write(root_label_1), Write(root_label_2))
        self.wait(1)

        # Show the algebraic connection to f(x)=0
        equation_at_roots = MathTex("f(x) = ax^2 + bx + c = 0", color=WHITE).next_to(roots_definition, DOWN, buff=0.5).align_to(roots_definition, LEFT)
        self.play(Write(equation_at_roots))
        self.wait(1.5)

        # --- Beat 3: Algebraic Methods Idea ---
        self.play(
            FadeOut(roots_text, shift=UP),
            FadeOut(roots_definition, shift=UP),
            FadeOut(equation_at_roots, shift=UP),
            FadeOut(dot_1, dot_2, root_label_1, root_label_2)
        )
        
        algebraic_text = Text("Common Algebraic Approaches", font_size=40, color=WHITE).next_to(general_form_tex, DOWN, buff=0.7).align_to(general_form_tex, LEFT)
        
        methods_list = VGroup(
            MathTex("\\bullet \\text{ Factoring}", color=MY_BLUE),
            MathTex("\\bullet \\text{ Completing the Square}", color=MY_BLUE),
            MathTex("\\bullet \\text{ Quadratic Formula}", color=MY_BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(algebraic_text, DOWN, buff=0.5).align_to(algebraic_text, LEFT)

        self.play(Write(algebraic_text))
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN) for m in methods_list], lag_ratio=0.2))
        self.wait(0.5)
        
        # Briefly show the quadratic formula as the general solution
        quadratic_formula_tex = MathTex(
            "x = {-b \\pm \\sqrt{b^2 - 4ac} \\over 2a}",
            color=MY_GOLD
        ).scale(0.8).next_to(methods_list, DOWN, buff=0.7).align_to(methods_list, LEFT)
        
        formula_arrow = Arrow(
            methods_list[-1].get_bottom(), 
            quadratic_formula_tex.get_top(), 
            buff=0.1, 
            color=WHITE
        )

        self.play(FadeIn(formula_arrow, shift=UP), Write(quadratic_formula_tex))
        self.wait(1.5)

        # --- Beat 4: Simple Example Walkthrough (x^2 - 4 = 0) ---
        self.play(
            FadeOut(algebraic_text, shift=UP),
            FadeOut(methods_list, shift=UP),
            FadeOut(formula_arrow, shift=UP),
            FadeOut(quadratic_formula_tex, shift=UP),
            general_form_tex.animate.move_to(LEFT * 3 + UP * 2) # Keep it in place
        )
        
        example_title = Text("Example: Solving ", font_size=40, color=WHITE).next_to(general_form_tex, DOWN, buff=0.7).align_to(general_form_tex, LEFT)
        example_eq = MathTex("x^2 - 4 = 0", color=MY_GOLD).next_to(example_title, RIGHT, buff=0.2)
        example_group = VGroup(example_title, example_eq)
        
        self.play(Write(example_group))
        self.wait(0.5)
        
        # Algebraic steps
        step_1 = MathTex("x^2 = 4", color=WHITE).next_to(example_group, DOWN, buff=0.5).align_to(example_group, LEFT)
        step_2 = MathTex("x = \\pm \\sqrt{4}", color=WHITE).next_to(step_1, DOWN, buff=0.3).align_to(step_1, LEFT)
        step_3 = MathTex("x = \\pm 2", color=MY_BLUE).next_to(step_2, DOWN, buff=0.3).align_to(step_2, LEFT)
        
        solution_group = VGroup(step_1, step_2, step_3)

        self.play(Write(step_1))
        self.play(Write(step_2))
        self.play(Write(step_3))
        self.wait(1)
        
        # Connect algebraic solutions back to the graph visually
        final_dot_1 = Dot(plane.c2p(-2, 0, 0), color=MY_GOLD, radius=0.15)
        final_dot_2 = Dot(plane.c2p(2, 0, 0), color=MY_GOLD, radius=0.15)

        self.play(
            FadeOut(example_group, shift=UP),
            FadeOut(general_form_tex, shift=UP),
            solution_group.animate.move_to(LEFT * 3 + UP * 1) # Keep solutions on screen
        )

        final_roots_label = MathTex("\\text{The roots are } x_1 = -2, x_2 = 2", color=MY_GOLD).next_to(solution_group, DOWN, buff=0.7).align_to(solution_group, LEFT)
        
        self.play(
            FadeIn(final_dot_1, final_dot_2, scale=2),
            ShowPassingFlash(final_dot_1.copy().set_color(MY_BLUE).scale(1.5)), # Visual pulse
            ShowPassingFlash(final_dot_2.copy().set_color(MY_BLUE).scale(1.5)),
            Write(final_roots_label)
        )
        self.wait(2)

        # --- Recap Card ---
        self.play(
            FadeOut(plane, shift=LEFT),
            FadeOut(graph, shift=LEFT),
            FadeOut(final_dot_1, shift=LEFT),
            FadeOut(final_dot_2, shift=LEFT),
            FadeOut(solution_group, shift=LEFT),
            FadeOut(final_roots_label, shift=LEFT),
        )
        self.wait(0.5)

        recap_title = Text("Recap: Solving Quadratic Equations", font_size=48, color=WHITE).to_edge(UP, buff=1)
        
        recap_points = VGroup(
            MathTex("\\bullet \\text{ Form: } ax^2 + bx + c = 0 \\quad (a \\neq 0)", color=MY_BLUE),
            MathTex("\\bullet \\text{ Goal: Find } x \\text{ when } y=0 \\text{ (the roots/zeros)}", color=MY_BLUE),
            MathTex("\\bullet \\text{ A quadratic equation can have up to two real solutions}", color=MY_BLUE),
            MathTex("\\bullet \\text{ Key Algebraic Methods: Factoring, Completing the Square, Quadratic Formula}", color=MY_BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT) for p in recap_points], lag_ratio=0.2, run_time=3))
        self.wait(3)
        self.play(FadeOut(recap_title, shift=UP), FadeOut(recap_points, shift=UP))
        self.wait(1)