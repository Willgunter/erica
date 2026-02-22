from manim import *

# Define custom colors for consistency, inspired by 3Blue1Brown
BLUE_ACCENT = '#87CEEB'  # Light blue
GOLD_ACCENT = '#FFD700'  # Gold
BACKGROUND_COLOR = BLACK # Dark background

class GeometricDiscriminant(Scene):
    def construct(self):
        # Set background color for the entire scene
        self.camera.background_color = BACKGROUND_COLOR

        # --- Visual Hook and Initial Setup ---
        # Introduce the module title and objective
        title = Text("Geometric Interpretation and the Discriminant", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        objective = Text("Unveiling the number of solutions for quadratic equations.", font_size=30, color=BLUE_ACCENT).next_to(title, DOWN, buff=0.5)

        self.play(
            FadeIn(title, shift=UP),
            FadeIn(objective, shift=UP),
            run_time=1.5
        )
        self.wait(1)

        # Create the main coordinate axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
            y_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
        ).to_edge(LEFT, buff=1.0).shift(RIGHT * 0.5) # Position to make space for text
        
        # Labels for the x and y axes
        x_label = Text("x", color=BLUE_ACCENT, font_size=24).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("y", color=BLUE_ACCENT, font_size=24).next_to(axes.y_axis.get_end(), UP)
        
        axes_group = VGroup(axes, x_label, y_label)

        # Fade out intro text and bring in axes
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(objective, shift=UP),
            Create(axes_group),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 1: Two Distinct Real Roots (Discriminant > 0) ---
        beat1_header = Text("Case 1: Two Distinct Real Roots", font_size=36, color=GOLD_ACCENT).to_corner(UP + RIGHT)
        self.play(FadeIn(beat1_header))
        self.wait(0.5)

        # Define the first parabola function: y = x^2 - 4
        def parabola_func_two_roots(x):
            return x**2 - 4

        graph_two_roots = axes.get_graph(parabola_func_two_roots, color=BLUE_ACCENT)
        # Position label near the graph, using axes.c2p for coordinate conversion
        graph_label_two_roots = Text("y = x^2 - 4", font_size=28, color=BLUE_ACCENT).next_to(axes.c2p(3.5, parabola_func_two_roots(3.5)), UP)

        self.play(Create(graph_two_roots), FadeIn(graph_label_two_roots, shift=LEFT), run_time=2)
        self.wait(0.5)

        # Mark the x-intercepts (roots) with dots and labels
        x_intercept_1_val = -2
        x_intercept_2_val = 2
        
        root_dot_1 = Dot(axes.c2p(x_intercept_1_val, 0), color=GOLD_ACCENT)
        root_dot_2 = Dot(axes.c2p(x_intercept_2_val, 0), color=GOLD_ACCENT)

        root_label_1 = Text("Root 1", font_size=24, color=GOLD_ACCENT).next_to(root_dot_1, DOWN)
        root_label_2 = Text("Root 2", font_size=24, color=GOLD_ACCENT).next_to(root_dot_2, DOWN)

        self.play(
            FadeIn(root_dot_1, scale_factor=0.5),
            FadeIn(root_dot_2, scale_factor=0.5),
            Write(root_label_1),
            Write(root_label_2)
        )
        self.wait(1)

        # Introduce the discriminant condition for this case
        discriminant_text_1 = Text("Discriminant > 0", font_size=32, color=GOLD_ACCENT).next_to(beat1_header, DOWN, buff=0.8)
        self.play(FadeIn(discriminant_text_1, shift=UP))
        self.wait(2)

        # --- Beat 2: One Real Root (Repeated Root, Discriminant = 0) ---
        # Clear previous beat's specific elements
        self.play(
            FadeOut(beat1_header, shift=UP),
            FadeOut(discriminant_text_1, shift=UP),
            FadeOut(root_label_1),
            FadeOut(root_label_2)
        )

        beat2_header = Text("Case 2: One Real Root (Repeated)", font_size=36, color=GOLD_ACCENT).to_corner(UP + RIGHT)
        self.play(FadeIn(beat2_header))
        self.wait(0.5)

        # Define the second parabola function: y = x^2
        def parabola_func_one_root(x):
            return x**2

        graph_one_root = axes.get_graph(parabola_func_one_root, color=BLUE_ACCENT)
        graph_label_one_root = Text("y = x^2", font_size=28, color=BLUE_ACCENT).next_to(axes.c2p(3.5, parabola_func_one_root(3.5)), UL)

        # Transform the first parabola and its label into the second
        # Dots merge to represent a single root
        self.play(
            Transform(graph_two_roots, graph_one_root),
            Transform(graph_label_two_roots, graph_label_one_root),
            Transform(root_dot_1, Dot(axes.c2p(0, 0), color=GOLD_ACCENT)),
            FadeOut(root_dot_2), # One dot fades out, the other becomes the single root
            run_time=2
        )
        self.wait(0.5)

        single_root_label = Text("Single Root", font_size=24, color=GOLD_ACCENT).next_to(root_dot_1, DOWN)
        self.play(Write(single_root_label))
        self.wait(1)

        # Introduce the discriminant condition for this case
        discriminant_text_2 = Text("Discriminant = 0", font_size=32, color=GOLD_ACCENT).next_to(beat2_header, DOWN, buff=0.8)
        self.play(FadeIn(discriminant_text_2, shift=UP))
        self.wait(2)

        # --- Beat 3: No Real Roots (Discriminant < 0) ---
        # Clear previous beat's specific elements
        self.play(
            FadeOut(beat2_header, shift=UP),
            FadeOut(discriminant_text_2, shift=UP),
            FadeOut(single_root_label),
        )

        beat3_header = Text("Case 3: No Real Roots", font_size=36, color=GOLD_ACCENT).to_corner(UP + RIGHT)
        self.play(FadeIn(beat3_header))
        self.wait(0.5)

        # Define the third parabola function: y = x^2 + 1
        def parabola_func_no_roots(x):
            return x**2 + 1

        graph_no_roots = axes.get_graph(parabola_func_no_roots, color=BLUE_ACCENT)
        graph_label_no_roots = Text("y = x^2 + 1", font_size=28, color=BLUE_ACCENT).next_to(axes.c2p(3.5, parabola_func_no_roots(3.5)), UL)

        # Transform the current parabola and its label into the third
        # The single root dot fades out as there are no x-intercepts
        self.play(
            Transform(graph_two_roots, graph_no_roots),
            Transform(graph_label_two_roots, graph_label_no_roots),
            FadeOut(root_dot_1),
            run_time=2
        )
        self.wait(0.5)

        no_roots_info = Text("Does Not Intersect x-axis", font_size=24, color=GOLD_ACCENT).next_to(graph_no_roots, DOWN)
        self.play(Write(no_roots_info))
        self.wait(1)

        # Introduce the discriminant condition for this case
        discriminant_text_3 = Text("Discriminant < 0", font_size=32, color=GOLD_ACCENT).next_to(beat3_header, DOWN, buff=0.8)
        self.play(FadeIn(discriminant_text_3, shift=UP))
        self.wait(2)

        # --- Beat 4: Summary of Discriminant (Visual Connection) ---
        # Clear the screen from the previous beat
        self.play(
            FadeOut(beat3_header, shift=UP),
            FadeOut(discriminant_text_3, shift=UP),
            FadeOut(no_roots_info),
            FadeOut(graph_two_roots), 
            FadeOut(graph_label_two_roots),
            FadeOut(axes_group)
        )
        self.wait(0.5)

        summary_header = Text("The Discriminant Reveals The Roots!", font_size=42, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(summary_header, shift=UP))
        self.wait(1)

        # --- Section 1: Two Roots Summary ---
        axes_sum_1 = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 1},
            x_axis_config={"numbers_to_include": [-1, 1]},
            y_axis_config={"numbers_to_include": [-1, 1]},
        ).scale(0.8)
        graph_sum_two_actual = axes_sum_1.get_graph(lambda x: x**2 - 1, color=BLUE_ACCENT)
        dot_sum_two_1 = Dot(axes_sum_1.c2p(-1, 0), color=GOLD_ACCENT)
        dot_sum_two_2 = Dot(axes_sum_1.c2p(1, 0), color=GOLD_ACCENT)
        
        # Group graph and dots for consistent positioning
        graph_and_dots_1 = VGroup(axes_sum_1, graph_sum_two_actual, dot_sum_two_1, dot_sum_two_2)
        
        text_two_roots = Text("2 Real Roots", color=GOLD_ACCENT, font_size=28)
        disc_two_roots = Text("Discriminant > 0", color=BLUE_ACCENT, font_size=24)
        
        # Position texts relative to the graph group
        text_two_roots.next_to(graph_and_dots_1, DOWN, buff=0.5)
        disc_two_roots.next_to(text_two_roots, DOWN, buff=0.2)
        section_1 = VGroup(graph_and_dots_1, text_two_roots, disc_two_roots)

        # --- Section 2: One Root Summary ---
        axes_sum_2 = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 1},
            x_axis_config={"numbers_to_include": [-1, 1]},
            y_axis_config={"numbers_to_include": [-1, 1]},
        ).scale(0.8)
        graph_sum_one_actual = axes_sum_2.get_graph(lambda x: x**2, color=BLUE_ACCENT)
        dot_sum_one = Dot(axes_sum_2.c2p(0, 0), color=GOLD_ACCENT)
        
        graph_and_dots_2 = VGroup(axes_sum_2, graph_sum_one_actual, dot_sum_one)

        text_one_root = Text("1 Real Root", color=GOLD_ACCENT, font_size=28)
        disc_one_root = Text("Discriminant = 0", color=BLUE_ACCENT, font_size=24)
        
        text_one_root.next_to(graph_and_dots_2, DOWN, buff=0.5)
        disc_one_root.next_to(text_one_root, DOWN, buff=0.2)
        section_2 = VGroup(graph_and_dots_2, text_one_root, disc_one_root)

        # --- Section 3: Zero Roots Summary ---
        axes_sum_3 = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 1},
            x_axis_config={"numbers_to_include": [-1, 1]},
            y_axis_config={"numbers_to_include": [-1, 1]},
        ).scale(0.8)
        graph_sum_zero_actual = axes_sum_3.get_graph(lambda x: x**2 + 0.5, color=BLUE_ACCENT)

        graph_and_dots_3 = VGroup(axes_sum_3, graph_sum_zero_actual)

        text_zero_roots = Text("0 Real Roots", color=GOLD_ACCENT, font_size=28)
        disc_zero_roots = Text("Discriminant < 0", color=BLUE_ACCENT, font_size=24)
        
        text_zero_roots.next_to(graph_and_dots_3, DOWN, buff=0.5)
        disc_zero_roots.next_to(text_zero_roots, DOWN, buff=0.2)
        section_3 = VGroup(graph_and_dots_3, text_zero_roots, disc_zero_roots)
        
        # Arrange the three complete sections horizontally
        all_sections = VGroup(section_1, section_2, section_3).arrange(RIGHT, buff=1.0).next_to(summary_header, DOWN, buff=1.0)

        # Animate the sections appearing using LaggedStart for a staggered effect
        self.play(
            LaggedStart(
                FadeIn(all_sections[0], shift=UP),
                FadeIn(all_sections[1], shift=UP),
                FadeIn(all_sections[2], shift=UP),
                lag_ratio=0.5, # Stagger the start times of the animations
                run_time=3
            )
        )
        self.wait(3)

        # --- Beat 5: Recap Card ---
        # Fade out the summary elements
        self.play(
            FadeOut(summary_header, shift=UP),
            FadeOut(all_sections)
        )
        self.wait(0.5)

        recap_title = Text("Recap: Discriminant and Roots", font_size=44, color=GOLD_ACCENT).to_edge(UP)
        
        recap_text_1 = Text("1. Discriminant > 0: Two distinct real roots.", font_size=32, color=BLUE_ACCENT)
        recap_text_2 = Text("2. Discriminant = 0: One real (repeated) root.", font_size=32, color=BLUE_ACCENT)
        recap_text_3 = Text("3. Discriminant < 0: No real roots.", font_size=32, color=BLUE_ACCENT)

        # Arrange recap points vertically and left-aligned
        recap_group = VGroup(recap_text_1, recap_text_2, recap_text_3).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        recap_group.next_to(recap_title, DOWN, buff=1.0)
        
        self.play(FadeIn(recap_title, shift=UP))
        self.wait(0.5)
        self.play(Write(recap_group[0]), run_time=1.5)
        self.wait(0.5)
        self.play(Write(recap_group[1]), run_time=1.5)
        self.wait(0.5)
        self.play(Write(recap_group[2]), run_time=1.5)
        self.wait(2)

        final_message = Text("Keep Exploring Quadratic Equations!", font_size=36, color=GOLD_ACCENT).to_edge(DOWN)
        self.play(FadeIn(final_message, shift=UP))
        self.wait(2)