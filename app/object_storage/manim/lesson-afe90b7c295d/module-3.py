from manim import *

# Define custom colors for consistency
ACCENT_BLUE = BLUE_E
ACCENT_GOLD = GOLD_E
TEXT_COLOR = WHITE
AXES_COLOR = GREY_B

class ParabolaXInterceptsSolutions(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Beat 1: The Visual Hook & X-Intercepts Introduction ---
        # (Approx. 0-8 seconds)
        
        # 1. Setup the coordinate plane
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": AXES_COLOR},
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 0.5,
                "stroke_opacity": 0.6,
            }
        ).add_coordinates()
        
        x_axis_label = plane.get_x_axis_label(MathTex("x")).set_color(TEXT_COLOR)
        y_axis_label = plane.get_y_axis_label(MathTex("y"), edge=LEFT, direction=UP).set_color(TEXT_COLOR)
        axes_labels = VGroup(x_axis_label, y_axis_label)

        self.play(
            LaggedStart(
                Create(plane),
                Write(axes_labels),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.wait(0.5)

        # 2. Draw a standard parabola and highlight intercepts
        def func_parabola_1(x):
            return 0.5 * x**2 - 2
        
        parabola_1 = plane.get_graph(func_parabola_1, color=ACCENT_BLUE, x_range=[-4, 4])
        
        # Intercept points for parabola_1
        intercept_1_left = Dot(plane.coords_to_point(-2, 0), radius=0.12, color=ACCENT_GOLD)
        intercept_1_right = Dot(plane.coords_to_point(2, 0), radius=0.12, color=ACCENT_GOLD)
        intercept_points_1 = VGroup(intercept_1_left, intercept_1_right)

        intercept_label_1 = MathTex("\\text{X-Intercepts}", color=TEXT_COLOR).next_to(intercept_points_1, DOWN, buff=0.7)
        intercept_label_1.shift(RIGHT * 0.5) # Adjust position slightly

        self.play(
            Create(parabola_1),
            run_time=1.5
        )
        self.play(
            FadeIn(intercept_points_1, scale=0.8),
            Write(intercept_label_1),
            run_time=1.5
        )
        self.play(
            intercept_points_1.animate.set_opacity(0.4), # pulse effect
            run_time=0.4
        )
        self.play(
            intercept_points_1.animate.set_opacity(1),
            run_time=0.4
        )
        self.wait(1)

        # --- Beat 2: From Intercepts to Solutions ---
        # (Approx. 8-18 seconds)

        # 1. Introduce the functional form
        functional_form = MathTex("y = ax^2 + bx + c", color=TEXT_COLOR)
        functional_form.to_edge(UP, buff=0.7)
        self.play(
            Write(functional_form),
            FadeOut(intercept_label_1),
            run_time=1.5
        )
        self.wait(0.5)

        # 2. Show that x-intercepts occur when y=0
        text_y_is_zero = MathTex("\\text{At X-intercepts, } y = 0", color=TEXT_COLOR)
        text_y_is_zero.next_to(functional_form, DOWN, buff=0.5)
        self.play(Write(text_y_is_zero), run_time=1.5)
        self.wait(0.5)

        # 3. Transform to the equation form (solutions)
        solution_form = MathTex("ax^2 + bx + c = 0", color=TEXT_COLOR)
        solution_form.move_to(functional_form.get_center()) # Start at same position for smooth transform

        self.play(
            TransformMatchingTex(functional_form, solution_form),
            FadeOut(text_y_is_zero),
            run_time=1.5
        )
        self.wait(0.5)

        # 4. Relabel the points as "Solutions"
        solution_label = MathTex("\\text{Solutions (or Roots)}", color=TEXT_COLOR).next_to(intercept_points_1, DOWN, buff=0.7)
        solution_label.shift(RIGHT * 0.5)

        self.play(
            Write(solution_label),
            run_time=1.5
        )
        self.play(
            intercept_points_1.animate.scale(1.2).set_color(ACCENT_GOLD).set_opacity(0.8), # Emphasize solution dots
            run_time=0.6
        )
        self.play(
            intercept_points_1.animate.scale(1/1.2).set_opacity(1),
            run_time=0.6
        )
        self.wait(1)

        # --- Beat 3: Different Scenarios for X-Intercepts ---
        # (Approx. 18-32 seconds)

        # 1. Two intercepts (already shown)
        num_solutions_2 = MathTex("\\text{2 Real Solutions}", color=ACCENT_GOLD).next_to(solution_form, DOWN, buff=0.5)
        self.play(Write(num_solutions_2), run_time=1)
        self.wait(1)

        # 2. One intercept (tangent)
        def func_parabola_2(x):
            return 0.5 * x**2
        
        parabola_2 = plane.get_graph(func_parabola_2, color=ACCENT_BLUE, x_range=[-4, 4])
        intercept_2_middle = Dot(plane.coords_to_point(0, 0), radius=0.12, color=ACCENT_GOLD)
        intercept_points_2 = VGroup(intercept_2_middle)

        num_solutions_1 = MathTex("\\text{1 Real Solution}", color=ACCENT_GOLD).move_to(num_solutions_2)

        self.play(
            Transform(parabola_1, parabola_2),
            Transform(intercept_points_1, intercept_points_2), # Transform the two dots into one
            Transform(solution_label, MathTex("\\text{Tangent Point}", color=TEXT_COLOR).next_to(intercept_2_middle, DOWN, buff=0.7)), # Change label
            ReplacementTransform(num_solutions_2, num_solutions_1),
            run_time=2.5
        )
        self.wait(1)

        # 3. No intercepts
        def func_parabola_3(x):
            return 0.5 * x**2 + 2
        
        parabola_3 = plane.get_graph(func_parabola_3, color=ACCENT_BLUE, x_range=[-4, 4])
        
        num_solutions_0 = MathTex("\\text{0 Real Solutions}", color=ACCENT_GOLD).move_to(num_solutions_1)

        self.play(
            Transform(parabola_2, parabola_3),
            FadeOut(intercept_points_2, solution_label), # Fade out the single dot and label
            ReplacementTransform(num_solutions_1, num_solutions_0),
            run_time=2.5
        )
        self.wait(1.5)

        # --- Beat 4: Importance & Bio Context ---
        # (Approx. 32-42 seconds)
        self.play(
            FadeOut(parabola_3, num_solutions_0),
            solution_form.animate.move_to(ORIGIN).scale(1.2), # Center the equation
            FadeOut(plane, axes_labels),
            run_time=2
        )
        self.wait(0.5)
        
        context_text_1 = Text("These solutions are key!", color=ACCENT_GOLD).next_to(solution_form, DOWN, buff=1)
        context_text_2 = Text("They represent critical points, equilibrium states,", font_size=36, color=TEXT_COLOR).next_to(context_text_1, DOWN, buff=0.5)
        context_text_3 = Text("or moments of change in scientific models.", font_size=36, color=TEXT_COLOR).next_to(context_text_2, DOWN, buff=0.2)
        
        self.play(Write(context_text_1), run_time=1.5)
        self.play(Write(context_text_2), run_time=2)
        self.play(Write(context_text_3), run_time=2)
        self.wait(2)

        # --- Recap Card ---
        # (Approx. 42-50 seconds)
        self.play(
            FadeOut(solution_form, context_text_1, context_text_2, context_text_3),
            run_time=1.5
        )

        recap_title = Text("Recap: Parabola X-Intercepts & Solutions", color=ACCENT_GOLD).to_edge(UP)
        
        recap_points = BulletList(
            "X-intercepts are points where a parabola crosses the x-axis.",
            "They occur when the function's y-value is 0.",
            "These are the 'real solutions' or 'roots' of ax² + bx + c = 0.",
            "A parabola can have 0, 1, or 2 real x-intercepts/solutions.",
            font_size=36,
            color=TEXT_COLOR,
            buff=0.7
        )
        recap_points.next_to(recap_title, DOWN, buff=1)
        recap_points.align_to(self.camera.frame_width * LEFT / 2 + RIGHT * 0.5, LEFT) # Align to left edge

        self.play(
            Write(recap_title),
            LaggedStart(*[FadeIn(point, shift=UP*0.5) for point in recap_points], lag_ratio=0.7),
            run_time=4
        )
        self.wait(3)

        self.play(
            FadeOut(recap_title, recap_points),
            run_time=1
        )
        self.wait(0.5)