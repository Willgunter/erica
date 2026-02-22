from manim import *

# Configuration for a clean dark background with high-contrast accents
config.background_color = "#1A1A1A"  # Dark background
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

# Define custom colors
ACCENT_BLUE = "#58CCED"  # Bright blue for primary elements
ACCENT_GOLD = "#FFD700"  # Gold for highlights and important points
LIGHT_GREY = "#AAAAAA"  # For grid lines and secondary elements
WHITE = "#FFFFFF"       # For general text

class QuadraticGeometricMeaning(Scene):
    def construct(self):
        self.camera.background_color = config.background_color # Ensure background is set

        # --- Beat 0: Visual Hook - A dynamic path ---
        hook_text = Text("A path.", color=WHITE).scale(0.9).to_edge(UP)
        
        # Define a simple parabola function for the hook
        def hook_parabola_func(x):
            return 0.5 * x**2 - 2

        # Create a tracker for the x-coordinate of the moving dot
        x_tracker = ValueTracker(-4)

        # Create the dot that will trace the path
        moving_dot = Dot(color=ACCENT_GOLD, radius=0.08)
        
        # Update the dot's position based on the x_tracker
        moving_dot.add_updater(lambda m: m.move_to([x_tracker.get_value(), hook_parabola_func(x_tracker.get_value()), 0]))

        # Create a "path" as the trace of the dot
        path_trace = TracedPath(moving_dot.get_center, stroke_color=ACCENT_BLUE, stroke_width=4)

        self.add(path_trace, moving_dot) # Add trace and dot to the scene
        self.play(Write(hook_text), run_time=1)
        self.wait(0.5)
        
        # Animate the dot moving along the path
        self.play(
            x_tracker.animate.set_value(4),
            run_time=3.5,
            rate_func=linear # Linear rate func for smooth path drawing
        )
        moving_dot.clear_updaters() # Stop updating the dot after animation
        
        # Create the full parabola object that matches the traced path
        hook_parabola = self.get_graph(hook_parabola_func, x_range=[-4, 4], color=ACCENT_BLUE, stroke_width=4)
        
        self.play(
            FadeOut(moving_dot), # Fade out the tracing dot
            ReplacementTransform(path_trace, hook_parabola), # Transform the traced path into the clean parabola
            FadeOut(hook_text),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 1: Introducing the Axes and Function Form ---
        axes = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": LIGHT_GREY},
            background_line_style={"stroke_color": LIGHT_GREY, "stroke_width": 1, "stroke_opacity": 0.5}
        ).add_coordinates() # Adds coordinate labels and axis arrows
        
        # Define the parabola function for this beat
        parabola_func_1 = lambda x: 0.5 * x**2 - 2.5 # Slightly lower for clearer x-intercepts
        parabola_1 = self.get_graph(parabola_func_1, x_range=[-4.5, 4.5], color=ACCENT_BLUE, stroke_width=4)
        
        # Equation text - using Unicode superscript for '2'
        equation_text = Text("y = ax² + bx + c", color=ACCENT_BLUE).scale(0.8).to_edge(UP)
        
        self.play(
            FadeIn(axes),
            Transform(hook_parabola, parabola_1), # Transform the previous parabola to the new one
            Write(equation_text),
            run_time=2
        )
        self.wait(0.5)

        # Visually explain x and y coordinates on the parabola
        x_val_tracker = ValueTracker(2.5)
        
        point_on_parabola = Dot(color=ACCENT_GOLD, radius=0.08)
        point_on_parabola.add_updater(lambda m: m.move_to(axes.coords_to_point(x_val_tracker.get_value(), parabola_func_1(x_val_tracker.get_value()))))

        x_proj_line = always_redraw(
            lambda: axes.get_vertical_line(point_on_parabola.get_center(), color=LIGHT_GREY, stroke_width=2, stroke_opacity=0.7)
        )
        y_proj_line = always_redraw(
            lambda: axes.get_horizontal_line(point_on_parabola.get_center(), color=LIGHT_GREY, stroke_width=2, stroke_opacity=0.7)
        )
        
        x_label = always_redraw(lambda: Text(f"x = {x_val_tracker.get_value():.1f}", color=WHITE).scale(0.6).next_to(x_proj_line.get_end(), DOWN, buff=0.2))
        y_label = always_redraw(lambda: Text(f"y = {parabola_func_1(x_val_tracker.get_value()):.1f}", color=WHITE).scale(0.6).next_to(y_proj_line.get_end(), LEFT, buff=0.2))

        self.play(
            LaggedStart(
                FadeIn(point_on_parabola),
                FadeIn(x_proj_line),
                FadeIn(y_proj_line),
                FadeIn(x_label),
                FadeIn(y_label),
                lag_ratio=0.5
            )
        )
        
        explanation_text_1 = Text("Every point (x, y) on this path follows an equation.", color=WHITE).scale(0.7).next_to(equation_text, DOWN, buff=0.5)
        self.play(Write(explanation_text_1))

        self.play(x_val_tracker.animate.set_value(-2.5), run_time=3, rate_func=linear)
        self.play(x_val_tracker.animate.set_value(0), run_time=2, rate_func=linear)

        self.play(
            FadeOut(point_on_parabola),
            FadeOut(x_proj_line),
            FadeOut(y_proj_line),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(explanation_text_1),
            run_time=1
        )
        self.wait(0.5)
        
        # --- Beat 2: Solutions as X-Intercepts ---
        question_text = Text("When is y = 0?", color=WHITE).scale(0.8).next_to(equation_text, DOWN, buff=0.5)
        self.play(Write(question_text))
        self.wait(0.5)

        # Highlight the x-axis (where y = 0)
        x_axis_highlight = Line(axes.coords_to_point(-6, 0), axes.coords_to_point(6, 0), color=ACCENT_GOLD, stroke_width=6)
        
        self.play(Create(x_axis_highlight), run_time=1.5)
        self.wait(0.5)

        # Calculate and mark the intersection points (solutions)
        x_sol_mag = np.sqrt(2.5 / 0.5) # From 0.5x^2 - 2.5 = 0 => x^2 = 5
        x_sol1 = x_sol_mag
        x_sol2 = -x_sol_mag
        
        solution_dot_1 = Dot(axes.coords_to_point(x_sol1, 0), color=ACCENT_GOLD, radius=0.1)
        solution_dot_2 = Dot(axes.coords_to_point(x_sol2, 0), color=ACCENT_GOLD, radius=0.1)
        
        # Using Unicode subscripts for solution labels
        sol_label_1 = Text(f"x₁ = {x_sol1:.2f}", color=ACCENT_GOLD).scale(0.6).next_to(solution_dot_1.get_center(), DOWN + RIGHT * 0.5, buff=0.1)
        sol_label_2 = Text(f"x₂ = {x_sol2:.2f}", color=ACCENT_GOLD).scale(0.6).next_to(solution_dot_2.get_center(), DOWN + LEFT * 0.5, buff=0.1)

        self.play(
            LaggedStart(
                FadeIn(solution_dot_1),
                FadeIn(solution_dot_2),
                Write(sol_label_1),
                Write(sol_label_2),
                lag_ratio=0.5
            )
        )
        
        solutions_text = Text("These are the solutions to the equation.", color=WHITE).scale(0.7).next_to(question_text, DOWN, buff=0.3)
        self.play(ReplacementTransform(question_text, solutions_text))
        self.wait(1.5)

        # --- Beat 3: Different Cases (0, 1, or 2 Solutions) ---
        self.play(
            FadeOut(sol_label_1),
            FadeOut(sol_label_2),
            FadeOut(solutions_text),
            FadeOut(solution_dot_1),
            FadeOut(solution_dot_2),
            # Keep x_axis_highlight
            run_time=1
        )
        
        # Case 1: Two distinct solutions (current parabola already shown)
        case_text_2_sols = Text("Two distinct solutions.", color=WHITE).scale(0.7).next_to(equation_text, DOWN, buff=0.5)
        
        # Re-add dots for 2 solutions as part of the new text group
        sol_dot_1_case = Dot(axes.coords_to_point(x_sol1, 0), color=ACCENT_GOLD, radius=0.1)
        sol_dot_2_case = Dot(axes.coords_to_point(x_sol2, 0), color=ACCENT_GOLD, radius=0.1)
        
        self.play(
            Write(case_text_2_sols),
            FadeIn(sol_dot_1_case),
            FadeIn(sol_dot_2_case)
        )
        self.wait(2)

        # Case 2: One repeated solution (vertex on x-axis)
        parabola_func_2 = lambda x: 0.5 * x**2
        parabola_2 = self.get_graph(parabola_func_2, x_range=[-4.5, 4.5], color=ACCENT_BLUE, stroke_width=4)
        
        case_text_1_sol = Text("One repeated solution.", color=WHITE).scale(0.7).next_to(equation_text, DOWN, buff=0.5)
        sol_dot_vertex = Dot(axes.coords_to_point(0, 0), color=ACCENT_GOLD, radius=0.1) # Vertex at (0,0)

        self.play(
            ReplacementTransform(parabola_1, parabola_2),
            ReplacementTransform(case_text_2_sols, case_text_1_sol),
            FadeOut(sol_dot_1_case),
            FadeOut(sol_dot_2_case),
            FadeIn(sol_dot_vertex) # Add the single solution dot
        )
        self.wait(2)

        # Case 3: No real solutions (parabola above x-axis)
        parabola_func_3 = lambda x: 0.5 * x**2 + 2
        parabola_3 = self.get_graph(parabola_func_3, x_range=[-4.5, 4.5], color=ACCENT_BLUE, stroke_width=4)
        
        case_text_0_sols = Text("No real solutions.", color=WHITE).scale(0.7).next_to(equation_text, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(parabola_2, parabola_3),
            ReplacementTransform(case_text_1_sol, case_text_0_sols),
            FadeOut(sol_dot_vertex) # Fade out the solution dot
        )
        self.wait(2.5)

        # --- Beat 4: Recap Card ---
        self.play(
            FadeOut(parabola_3),
            FadeOut(axes),
            FadeOut(equation_text),
            FadeOut(case_text_0_sols),
            FadeOut(x_axis_highlight),
            run_time=1.5
        )
        self.wait(0.5)

        recap_title = Text("Recap: Geometric Meaning of Quadratic Solutions", color=ACCENT_GOLD).scale(1.1)
        
        bullet_1 = Text("Solutions are the x-intercepts of the parabola", color=WHITE).scale(0.8).next_to(recap_title, DOWN, buff=0.8).align_to(recap_title, LEFT)
        equation_for_bullet = Text("y = ax² + bx + c", color=ACCENT_BLUE).scale(0.7).next_to(bullet_1, DOWN, buff=0.2).align_to(bullet_1, LEFT)

        bullet_2 = Text("A quadratic equation can have 0, 1, or 2 real solutions.", color=WHITE).scale(0.8).next_to(equation_for_bullet, DOWN, buff=0.8).align_to(bullet_1, LEFT)

        recap_group = VGroup(recap_title, bullet_1, equation_for_bullet, bullet_2).center()

        self.play(
            LaggedStart(
                FadeIn(recap_title, shift=UP),
                FadeIn(bullet_1, shift=LEFT),
                FadeIn(equation_for_bullet, shift=LEFT),
                FadeIn(bullet_2, shift=LEFT),
                lag_ratio=0.5,
                run_time=4
            )
        )
        self.wait(3)

        self.play(FadeOut(recap_group))
        self.wait(1)