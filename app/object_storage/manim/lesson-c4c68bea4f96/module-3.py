from manim import *

class QuadraticGeometricMeaning(Scene):
    def construct(self):
        # --- Configuration ---
        DARK_BACKGROUND = '#1A1A1A'
        BLUE = '#58C4ED' # High-contrast blue
        GOLD = '#F7D75E' # High-contrast gold
        WHITE = '#FFFFFF'

        self.camera.background_color = DARK_BACKGROUND

        # --- Scene Setup: Axes ---
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={
                "numbers_to_include": [-4, -2, 2, 4],
                "font_size": 24,
                "color": GOLD
            },
            y_axis_config={
                "numbers_to_include": [-3, -1, 1, 3],
                "font_size": 24,
                "color": BLUE
            },
        ).to_edge(DOWN)
        
        # Add a clear label for the x-axis
        x_axis_label_text = Text("X-axis (y=0)", font_size=24, color=GOLD).next_to(axes.x_axis, DOWN, buff=0.2)
        
        self.play(Create(axes, run_time=1.5), Write(x_axis_label_text))
        self.wait(0.5)

        # --- Beat 1: Visual Hook - A Parabola and its Intersections ---
        # y = 0.5x^2 - 2
        initial_parabola = FunctionGraph(
            lambda x: 0.5 * x**2 - 2,
            x_range=[-4, 4],
            color=BLUE,
            stroke_width=5
        )

        intersection_points_coords = [axes.c2p(-2, 0), axes.c2p(2, 0)]
        intersection_dots = VGroup(*[Dot(point, color=GOLD, radius=0.12) for point in intersection_points_coords])

        hook_question = Text("Where does this curve cross the line?", font_size=32, color=WHITE).to_edge(UP)

        self.play(
            Create(initial_parabola),
            Write(hook_question),
            run_time=2
        )
        self.play(
            FadeIn(intersection_dots, scale=0.8),
            run_time=1
        )
        self.wait(1.5)

        # --- Beat 2: The Idea of 'Roots' as X-intercepts ---
        self.play(FadeOut(hook_question))

        solutions_label = Text("These points are the 'solutions'!", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(solutions_label))

        # Vertical lines from dots to x-axis (already on x-axis, just for emphasis)
        v_lines = VGroup()
        x_labels = VGroup()

        for i, dot in enumerate(intersection_dots):
            x_coord_value = round(axes.point_to_coords(dot.get_center())[0])
            v_line = DashedLine(
                dot.get_center() + UP * 0.5, # Start slightly above for visual effect
                dot.get_center(),
                color=GOLD,
                stroke_width=3
            )
            x_label = Text(str(x_coord_value), font_size=28, color=GOLD).next_to(dot, DOWN, buff=0.2)
            v_lines.add(v_line)
            x_labels.add(x_label)
        
        self.play(
            Create(v_lines),
            FadeIn(x_labels, shift=DOWN),
            run_time=1.5
        )

        x_intercepts_clarification = Text("They are the X-intercepts.", font_size=28, color=GOLD).next_to(solutions_label, DOWN)
        self.play(Write(x_intercepts_clarification))
        self.wait(2)
        
        # --- Beat 3: Varying the Parabola - Number of Solutions ---
        self.play(
            FadeOut(solutions_label, x_intercepts_clarification, v_lines, x_labels)
        )

        how_many_solutions_title = Text("How many solutions can there be?", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(how_many_solutions_title))

        # Case 1: Two solutions (current state is already this, just label it)
        two_sol_text = Text("Two Real Solutions", font_size=28, color=BLUE).next_to(how_many_solutions_title, DOWN)
        self.play(FadeIn(two_sol_text))
        self.wait(1.5)

        # Case 2: One solution (tangent to x-axis)
        one_sol_parabola = FunctionGraph(
            lambda x: 0.25 * x**2, # Vertex at (0,0)
            x_range=[-4, 4],
            color=BLUE,
            stroke_width=5
        )
        one_sol_dot = Dot(axes.c2p(0, 0), color=GOLD, radius=0.12)
        one_sol_text = Text("One Real Solution", font_size=28, color=BLUE).next_to(how_many_solutions_title, DOWN)
        
        self.play(
            Transform(initial_parabola, one_sol_parabola),
            ReplacementTransform(intersection_dots, VGroup(one_sol_dot)),
            ReplacementTransform(two_sol_text, one_sol_text),
            run_time=2
        )
        self.wait(1.5)

        # Case 3: No solutions (above x-axis)
        no_sol_parabola = FunctionGraph(
            lambda x: 0.25 * x**2 + 1.5, # Vertex at (0, 1.5)
            x_range=[-4, 4],
            color=BLUE,
            stroke_width=5
        )
        no_sol_text = Text("No Real Solutions", font_size=28, color=BLUE).next_to(how_many_solutions_title, DOWN)
        
        self.play(
            Transform(initial_parabola, no_sol_parabola),
            FadeOut(one_sol_dot, scale=0.5), # No intersection dots
            ReplacementTransform(one_sol_text, no_sol_text),
            run_time=2
        )
        self.wait(2)

        # --- Beat 4: Formal Notation - y = ax^2 + bx + c ---
        self.play(
            FadeOut(how_many_solutions_title, no_sol_text)
        )

        equation_intro = Text("This is a quadratic function:", font_size=32, color=WHITE).to_edge(UP)
        quadratic_equation_text = Text("y = ax² + bx + c", font_size=48, color=BLUE).next_to(equation_intro, DOWN, buff=0.7)
        
        self.play(Write(equation_intro), Write(quadratic_equation_text))

        # Briefly bring back a two-solution parabola to reinforce
        final_parabola = FunctionGraph(lambda x: 0.5 * x**2 - 2, x_range=[-4, 4], color=BLUE, stroke_width=5)
        final_dots = VGroup(*[Dot(axes.c2p(-2, 0), color=GOLD, radius=0.12), Dot(axes.c2p(2, 0), color=GOLD, radius=0.12)])
        
        self.play(
            Transform(initial_parabola, final_parabola),
            FadeIn(final_dots)
        )

        explanation_line1 = Text("Finding the 'solutions' means finding", font_size=28, color=GOLD).next_to(quadratic_equation_text, DOWN, buff=0.5)
        explanation_line2 = Text("the x-values where y = 0.", font_size=28, color=GOLD).next_to(explanation_line1, DOWN)

        self.play(
            Write(explanation_line1),
            Write(explanation_line2),
            run_time=2
        )
        self.wait(2.5)

        # --- Recap Card ---
        self.play(
            FadeOut(axes, initial_parabola, final_dots, x_axis_label_text,
                    equation_intro, quadratic_equation_text, explanation_line1, explanation_line2)
        )

        recap_title = Text("Recap: Quadratic Solutions", font_size=48, color=BLUE).to_edge(UP, buff=1)
        
        recap_bullet1 = Text("Solutions are the X-intercepts", font_size=36, color=WHITE).next_to(recap_title, DOWN, buff=0.8)
        recap_bullet2 = Text("of the parabola y = ax² + bx + c.", font_size=36, color=WHITE).next_to(recap_bullet1, DOWN)

        # Small illustrative parabola for recap
        mini_axes = Axes(x_range=[-2, 2, 1], y_range=[-1, 1, 1], x_length=4, y_length=2,
                         axis_config={"color": DARK_BACKGROUND},
                         x_axis_config={"color": WHITE, "numbers_to_include": []},
                         y_axis_config={"color": DARK_BACKGROUND, "numbers_to_include": []}
                         ).scale(0.8).to_edge(DOWN, buff=0.5).shift(RIGHT*0.5)
        
        mini_parabola = FunctionGraph(
            lambda x: 0.5 * x**2 - 0.5,
            x_range=[-1.5, 1.5],
            color=BLUE,
            stroke_width=4
        ).move_to(mini_axes.get_center())

        # Manually calculate and adjust dots for mini_parabola on mini_axes for clarity
        mini_dot1 = Dot(mini_axes.c2p(-1, 0), color=GOLD, radius=0.08)
        mini_dot2 = Dot(mini_axes.c2p(1, 0), color=GOLD, radius=0.08)
        
        self.play(
            Write(recap_title)
        )
        self.play(
            LaggedStart(
                Write(recap_bullet1),
                Write(recap_bullet2),
                lag_ratio=0.7,
                run_time=2
            )
        )
        self.play(
            Create(mini_axes.x_axis), # Only show x-axis for context
            Create(mini_parabola),
            FadeIn(VGroup(mini_dot1, mini_dot2)),
            run_time=1.5
        )
        self.wait(3)