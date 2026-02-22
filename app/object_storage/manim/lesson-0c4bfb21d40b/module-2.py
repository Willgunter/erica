from manim import *

class QuadraticParabolaIntercepts(Scene):
    def construct(self):
        # --- Configuration & Custom Colors ---
        self.camera.background_color = BLACK
        BLUE_ACCENT = "#58CCED"  # Light blue for functions/parabolas
        GOLD_ACCENT = "#FFD700"  # Gold for equations/solutions/intercepts
        RED_ACCENT = "#FF6347"   # Tomato red for emphasis on no solutions

        # --- Beat 1: Visual Hook & Core Concept Introduction ---
        # 1. Setup Axes
        axes = Axes(
            x_range=[-4.5, 4.5, 1],
            y_range=[-4.5, 4.5, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY_A, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
            y_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
        ).add_coordinates()
        
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Create(labels), run_time=1.5)
        self.wait(0.5)

        # 2. Draw a generic parabola and highlight its intercepts
        parabola_func_initial = lambda x: 0.5 * x**2 - 2
        parabola_initial = axes.get_graph(parabola_func_initial, color=BLUE_ACCENT)
        
        # Calculate intercepts for initial parabola (0.5x^2 - 2 = 0 => x^2 = 4 => x = +/- 2)
        initial_intercept_coords = [-2, 2]
        initial_intercept_dots = VGroup(*[
            Dot(axes.c2p(x, 0), color=GOLD_ACCENT, radius=0.08) for x in initial_intercept_coords
        ])

        self.play(Create(parabola_initial), run_time=1.5)
        self.play(FadeIn(initial_intercept_dots, scale=0.8), run_time=0.8)
        self.wait(0.5)

        # 3. Introduce the module title
        title = Text("Quadratic Solutions as Parabola Intercepts", font_size=40, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # 4. Introduce the core concept text
        core_concept_p1 = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT).shift(UP*2.5 + LEFT*3.5)
        core_concept_arrow = MathTex("\\iff", color=GRAY_A).next_to(core_concept_p1, RIGHT, buff=0.3)
        core_concept_p2 = MathTex("y = ax^2 + bx + c", color=BLUE_ACCENT).next_to(core_concept_arrow, RIGHT, buff=0.3)
        core_concept_line2 = Text("Solutions are x-intercepts (where y=0)", font_size=28, color=WHITE).next_to(core_concept_p1, DOWN, buff=0.7).align_to(core_concept_p1, LEFT)
        
        self.play(
            FadeOut(title), # Fade out main title to make room
            FadeOut(initial_intercept_dots, parabola_initial), # Fade out initial elements for clean slate
            LaggedStart(
                Write(core_concept_p1),
                Write(core_concept_arrow),
                Write(core_concept_p2),
                lag_ratio=0.5,
                run_time=2
            )
        )
        self.play(Write(core_concept_line2))
        self.wait(1)

        # Move the concept explanation to the top-left to make room for the graph
        concept_group = VGroup(core_concept_p1, core_concept_arrow, core_concept_p2, core_concept_line2)
        self.play(
            concept_group.animate.to_corner(UL).scale(0.7),
            axes.animate.shift(RIGHT*2) # Shift axes to the right
        )
        self.wait(0.5)

        # --- Beat 2: Specific Example - Two Real Solutions ---
        # 1. Introduce specific equation and function
        current_quadratic_eq_tex = MathTex("x^2 - 4 = 0", color=GOLD_ACCENT).next_to(concept_group, DOWN, buff=1.0).align_to(concept_group, LEFT)
        current_function_tex = MathTex("y = x^2 - 4", color=BLUE_ACCENT).next_to(current_quadratic_eq_tex, DOWN).align_to(current_quadratic_eq_tex, LEFT)

        self.play(Write(current_quadratic_eq_tex))
        self.wait(0.5)
        self.play(Write(current_function_tex))
        self.wait(0.5)

        # 2. Draw graph for y = x^2 - 4 and show intercepts
        parabola_func_two_sols = lambda x: x**2 - 4
        parabola_two_sols = axes.get_graph(parabola_func_two_sols, color=BLUE_ACCENT)
        
        two_sols_intercept_coords = [-2, 2]
        two_sols_intercept_dots = VGroup(*[
            Dot(axes.c2p(x, 0), color=GOLD_ACCENT, radius=0.08) for x in two_sols_intercept_coords
        ])

        self.play(Create(parabola_two_sols))
        self.play(FadeIn(two_sols_intercept_dots, scale=0.8))
        self.wait(0.5)

        # 3. Show the solutions explicitly
        solutions_tex_two = MathTex("x = \\pm 2", color=GOLD_ACCENT).next_to(two_sols_intercept_dots, DOWN, buff=0.5)
        self.play(Write(solutions_tex_two))
        self.wait(1.5)

        # --- Beat 3: Exploring Number of Solutions (One, Zero) ---
        # Transition to One Solution (x^2 = 0)
        self.play(FadeOut(solutions_tex_two))
        self.wait(0.5)

        parabola_func_one_sol = lambda x: x**2
        one_sol_intercept_dot = Dot(axes.c2p(0, 0), color=GOLD_ACCENT, radius=0.08) # Only one intercept at x=0
        
        new_quadratic_eq_tex_one = MathTex("x^2 = 0", color=GOLD_ACCENT).copy().next_to(current_quadratic_eq_tex, DOWN, buff=1.0).align_to(current_quadratic_eq_tex, LEFT)
        new_function_tex_one = MathTex("y = x^2", color=BLUE_ACCENT).copy().next_to(new_quadratic_eq_tex_one, DOWN).align_to(new_quadratic_eq_tex_one, LEFT)

        self.play(
            Transform(parabola_two_sols, axes.get_graph(parabola_func_one_sol, color=BLUE_ACCENT)),
            TransformMatchingTex(current_quadratic_eq_tex, new_quadratic_eq_tex_one),
            TransformMatchingTex(current_function_tex, new_function_tex_one),
            Transform(two_sols_intercept_dots, one_sol_intercept_dot), # Transform two dots into one
            run_time=2
        )
        current_quadratic_eq_tex = new_quadratic_eq_tex_one # Update reference for next transform
        current_function_tex = new_function_tex_one
        self.wait(0.5)

        solutions_tex_one = MathTex("x = 0", color=GOLD_ACCENT).next_to(one_sol_intercept_dot, DOWN, buff=0.5)
        self.play(Write(solutions_tex_one))
        self.wait(1.5)

        # Transition to No Real Solutions (x^2 + 4 = 0)
        self.play(FadeOut(solutions_tex_one))
        self.wait(0.5)

        parabola_func_no_sols = lambda x: x**2 + 4
        
        new_quadratic_eq_tex_no = MathTex("x^2 + 4 = 0", color=GOLD_ACCENT).copy().next_to(current_quadratic_eq_tex, DOWN, buff=1.0).align_to(current_quadratic_eq_tex, LEFT)
        new_function_tex_no = MathTex("y = x^2 + 4", color=BLUE_ACCENT).copy().next_to(new_quadratic_eq_tex_no, DOWN).align_to(new_quadratic_eq_tex_no, LEFT)

        no_sols_text = Text("No Real Solutions", font_size=32, color=RED_ACCENT).next_to(one_sol_intercept_dot, DOWN, buff=0.5) # Position where solutions would be
        
        self.play(
            Transform(parabola_two_sols, axes.get_graph(parabola_func_no_sols, color=BLUE_ACCENT)),
            TransformMatchingTex(current_quadratic_eq_tex, new_quadratic_eq_tex_no),
            TransformMatchingTex(current_function_tex, new_function_tex_no),
            FadeOut(one_sol_intercept_dot), # Intercept dot disappears
            run_time=2
        )
        self.play(Write(no_sols_text))
        self.wait(2)

        # --- Beat 4: Recap Card ---
        self.play(
            FadeOut(parabola_two_sols),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(no_sols_text),
            FadeOut(concept_group),
            FadeOut(new_quadratic_eq_tex_no),
            FadeOut(new_function_tex_no),
        )

        recap_title = Text("Recap: Quadratic Solutions", font_size=45, color=WHITE).to_edge(UP, buff=1.0)
        
        recap_point1 = MathTex("1.", " \quad ax^2 + bx + c = 0", color=GOLD_ACCENT).next_to(recap_title, DOWN, buff=1.0).align_to(recap_title, LEFT).shift(RIGHT)
        recap_point2 = MathTex("2.", " \quad y = ax^2 + bx + c", color=BLUE_ACCENT).next_to(recap_point1, DOWN, buff=0.5).align_to(recap_point1, LEFT)
        recap_point3 = Text("3. Solutions are x-intercepts (where y=0)", font_size=32, color=WHITE).next_to(recap_point2, DOWN, buff=0.5).align_to(recap_point2, LEFT)
        recap_point4 = Text("4. A quadratic can have 2, 1, or 0 real solutions.", font_size=32, color=WHITE).next_to(recap_point3, DOWN, buff=0.5).align_to(recap_point3, LEFT)
        
        recap_group = VGroup(recap_point1, recap_point2, recap_point3, recap_point4)

        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(
            LaggedStart(
                Write(recap_point1),
                Write(recap_point2),
                Write(recap_point3),
                Write(recap_point4),
                lag_ratio=0.7,
                run_time=4
            )
        )
        self.wait(3)

        self.play(FadeOut(recap_title, recap_group))
        self.wait(1)