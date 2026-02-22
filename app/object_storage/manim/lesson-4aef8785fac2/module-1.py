from manim import *

# Custom colors for 3Blue1Brown style
BLUE_ACCENT = "#50d8ed"  # Lighter blue
GOLD_ACCENT = "#ffd700"  # Gold
DARK_BACKGROUND = "#1a1a1a" # Very dark grey

class QuadraticEquationsAnimation(Scene):
    def construct(self):
        # Set dark background
        self.camera.background_color = DARK_BACKGROUND

        # --- Beat 1: Visual Hook - The Parabola Shape ---
        # A dynamic path that reveals a parabola
        intro_title = Text("Understanding Quadratic Equations", font_size=50, color=BLUE_ACCENT)
        self.play(FadeIn(intro_title))
        self.wait(1)
        self.play(intro_title.animate.to_edge(UP).scale(0.7), run_time=1.5)

        # Create a simple parabola function
        def func_parabola_initial(x):
            return 0.5 * x**2

        axes_hook = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 2},
            x_axis_config={"numbers_to_exclude": [0]},
            y_axis_config={"numbers_to_exclude": [0]},
        ).to_edge(DOWN).shift(UP*0.5)
        
        parabola_curve_initial = axes_hook.plot(func_parabola_initial, color=GOLD_ACCENT, stroke_width=4)
        parabola_label = Text("Parabola", color=GOLD_ACCENT, font_size=30).next_to(parabola_curve_initial, UP+RIGHT, buff=0.2)

        real_world_concept = Text("Curves are everywhere!", color=BLUE_ACCENT, font_size=35).next_to(intro_title, DOWN, buff=1)
        
        self.play(FadeIn(real_world_concept), run_time=1)
        self.play(
            Create(axes_hook),
            Create(parabola_curve_initial, run_time=2, rate_func=ease_out_sine),
        )
        self.play(Write(parabola_label))
        self.wait(1)

        # --- Beat 2: Connecting to Coordinates (x and y) ---
        self.play(
            FadeOut(real_world_concept),
            FadeOut(parabola_label),
            intro_title.animate.to_edge(UP).shift(LEFT*2.5),
            axes_hook.animate.scale(0.8).move_to(ORIGIN).shift(RIGHT*2),
            parabola_curve_initial.animate.scale(0.8).move_to(ORIGIN).shift(RIGHT*2)
        )
        
        # Adjust axes range for better focus on point plotting
        axes_focus = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 2},
            x_axis_config={"numbers_to_exclude": [0]},
            y_axis_config={"numbers_to_exclude": [0]},
        ).move_to(axes_hook.get_center())

        parabola_curve_focus = axes_focus.plot(func_parabola_initial, color=GOLD_ACCENT, stroke_width=4)
        
        self.play(
            ReplacementTransform(axes_hook, axes_focus),
            ReplacementTransform(parabola_curve_initial, parabola_curve_focus),
            run_time=1.5
        )

        coord_text = Text("Points on a curve have (x, y) coordinates.", color=BLUE_ACCENT, font_size=30).next_to(intro_title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Write(coord_text))

        # Show points being plotted
        points_to_plot = [(-2, func_parabola_initial(-2)), (-1, func_parabola_initial(-1)), (0, func_parabola_initial(0)), (1, func_parabola_initial(1)), (2, func_parabola_initial(2))]
        dots = VGroup()
        coord_labels = VGroup()

        for x_val, y_val in points_to_plot:
            dot = Dot(axes_focus.coords_to_point(x_val, y_val), color=BLUE_ACCENT, radius=0.08)
            label = Text(f"({x_val}, {y_val:.1f})", font_size=20, color=GOLD_ACCENT).next_to(dot, UP, buff=0.1)
            dots.add(dot)
            coord_labels.add(label)

        self.play(LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(label) for label in coord_labels], lag_ratio=0.3))
        self.wait(1.5)

        # --- Beat 3: Intuition of the Equation (y = x^2) ---
        self.play(
            FadeOut(dots),
            FadeOut(coord_labels),
            FadeOut(coord_text),
            parabola_curve_focus.animate.set_color(BLUE_ACCENT),
            axes_focus.animate.shift(LEFT * 2) # Move axes to center-left
        )
        
        # Create y = x^2 using Text objects
        y_label_sq = Text("y", font_size=40, color=GOLD_ACCENT)
        eq_label_sq = Text("=", font_size=40, color=BLUE_ACCENT)
        x_label_sq = Text("x", font_size=40, color=GOLD_ACCENT)
        exp_label_sq = Text("2", font_size=25, color=GOLD_ACCENT) # Small '2' for exponent
        exp_label_sq.next_to(x_label_sq, UP+RIGHT, buff=0.05).shift(RIGHT*0.05).scale(0.6) # Manually position
        
        x_squared_group = VGroup(y_label_sq, eq_label_sq, x_label_sq, exp_label_sq).arrange(RIGHT, buff=0.1)
        x_squared_group.next_to(axes_focus, RIGHT, buff=1)

        equation_concept_text = Text("The relationship is often 'x squared'.", color=BLUE_ACCENT, font_size=30).to_edge(UP).shift(LEFT*2.5)
        self.play(ReplacementTransform(intro_title, equation_concept_text))

        self.play(Write(x_squared_group))
        self.wait(0.5)

        # Plot points of y=x line
        line_x = axes_focus.plot(lambda x: x, color=BLUE_ACCENT, stroke_width=2)
        line_x_label = Text("y = x", font_size=20, color=BLUE_ACCENT).next_to(line_x, UL, buff=0.1)

        self.play(Create(line_x), Write(line_x_label))
        self.wait(0.5)

        # Transform line y=x to parabola y=x^2
        transform_label = Text("Squaring x values makes this curve!", color=BLUE_ACCENT, font_size=25).next_to(equation_concept_text, DOWN, buff=0.5)
        self.play(Write(transform_label))
        
        parabola_for_transform = axes_focus.plot(lambda x: x**2, color=GOLD_ACCENT, stroke_width=4)
        self.play(
            ReplacementTransform(line_x, parabola_for_transform),
            FadeOut(line_x_label),
            run_time=2
        )
        self.wait(1)
        self.play(FadeOut(transform_label))
        parabola_curve_focus = parabola_for_transform # Update the reference

        # --- Beat 4: Generalizing the Form (a, b, c) ---
        self.play(
            x_squared_group.animate.to_edge(UP).shift(RIGHT*1.5),
            equation_concept_text.animate.to_edge(UP).shift(LEFT*2.5),
            axes_focus.animate.scale(0.8).move_to(ORIGIN).shift(LEFT*2),
            parabola_curve_focus.animate.scale(0.8).move_to(ORIGIN).shift(LEFT*2),
            run_time=1.5
        )

        general_form_label = Text("The general form:", color=BLUE_ACCENT, font_size=30).to_edge(LEFT, buff=0.5).next_to(equation_concept_text, DOWN, buff=0.5)
        self.play(Write(general_form_label))

        # Create general quadratic equation: y = ax^2 + bx + c using Text objects
        y_label_gen = Text("y", font_size=40, color=GOLD_ACCENT)
        eq_label_gen = Text("=", font_size=40, color=BLUE_ACCENT)
        a_label = Text("a", font_size=40, color=GOLD_ACCENT)
        x1_label = Text("x", font_size=40, color=GOLD_ACCENT)
        exp_label_gen = Text("2", font_size=25, color=GOLD_ACCENT) # Small '2' for exponent

        # Position exponent relative to x1_label, then group
        exp_label_gen.next_to(x1_label, UP+RIGHT, buff=0.05).shift(RIGHT*0.05).scale(0.6) 
        ax2_part_final = VGroup(a_label, x1_label, exp_label_gen).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)

        plus1_label = Text("+", font_size=40, color=BLUE_ACCENT)
        b_label = Text("b", font_size=40, color=GOLD_ACCENT)
        x2_label = Text("x", font_size=40, color=GOLD_ACCENT)
        bx_part_final = VGroup(b_label, x2_label).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)

        plus2_label = Text("+", font_size=40, color=BLUE_ACCENT)
        c_label = Text("c", font_size=40, color=GOLD_ACCENT)

        general_eq_group = VGroup(
            y_label_gen, eq_label_gen,
            ax2_part_final,
            plus1_label,
            bx_part_final,
            plus2_label,
            c_label
        ).arrange(RIGHT, buff=0.15, aligned_edge=DOWN) # Use aligned_edge=DOWN to keep base of text aligned.
        general_eq_group.next_to(general_form_label, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(x_squared_group, general_eq_group),
            FadeOut(equation_concept_text)
        )
        self.wait(0.5)

        # Animate the effect of a, b, c
        def get_parabola(a, b, c):
            return axes_focus.plot(lambda x: a*x**2 + b*x + c, color=GOLD_ACCENT, stroke_width=4)
        
        # Initial parabola for 'a=1, b=0, c=0' (from Beat 3)
        current_parabola = parabola_curve_focus

        # Effect of 'a'
        a_value_text = Text("a changes width and direction", font_size=25, color=BLUE_ACCENT).next_to(general_eq_group, DOWN, buff=0.5)
        self.play(Write(a_value_text))
        
        parabola_a_1 = get_parabola(2, 0, 0) # Narrower
        parabola_a_2 = get_parabola(0.5, 0, 0) # Wider
        parabola_a_3 = get_parabola(-1, 0, 0) # Opens down
        
        self.play(ReplacementTransform(current_parabola, parabola_a_1))
        self.wait(0.5)
        self.play(ReplacementTransform(parabola_a_1, parabola_a_2))
        self.wait(0.5)
        self.play(ReplacementTransform(parabola_a_2, parabola_a_3))
        self.wait(0.5)
        current_parabola = parabola_a_3

        self.play(FadeOut(a_value_text))

        # Effect of 'c'
        c_value_text = Text("c shifts it up or down", font_size=25, color=BLUE_ACCENT).next_to(general_eq_group, DOWN, buff=0.5)
        self.play(Write(c_value_text))

        parabola_c_1 = get_parabola(-1, 0, 2) # Shift up
        parabola_c_2 = get_parabola(-1, 0, -1) # Shift down
        
        self.play(ReplacementTransform(current_parabola, parabola_c_1))
        self.wait(0.5)
        self.play(ReplacementTransform(parabola_c_1, parabola_c_2))
        self.wait(0.5)
        current_parabola = parabola_c_2

        self.play(FadeOut(c_value_text))

        # Effect of 'b' (simplified)
        b_value_text = Text("b moves the vertex sideways", font_size=25, color=BLUE_ACCENT).next_to(general_eq_group, DOWN, buff=0.5)
        self.play(Write(b_value_text))

        parabola_b_1 = get_parabola(-1, 2, -1) # Shift vertex
        parabola_b_2 = get_parabola(-1, -3, -1) # Shift vertex other way
        
        self.play(ReplacementTransform(current_parabola, parabola_b_1))
        self.wait(0.5)
        self.play(ReplacementTransform(parabola_b_1, parabola_b_2))
        self.wait(0.5)
        current_parabola = parabola_b_2

        self.play(FadeOut(b_value_text))

        self.wait(1)
        self.play(FadeOut(general_form_label), FadeOut(general_eq_group))
        
        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(axes_focus),
            FadeOut(current_parabola),
        )

        recap_title = Text("Recap:", font_size=45, color=GOLD_ACCENT).to_edge(UP)
        
        bullet1 = Text("• Quadratic equations create parabolas (U-shapes).", font_size=30, color=BLUE_ACCENT).next_to(recap_title, DOWN, buff=0.8).align_to(recap_title, LEFT)
        bullet2 = Text("• They model real-world curves.", font_size=30, color=BLUE_ACCENT).next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet3 = Text("• Basic form: y = x^2", font_size=30, color=BLUE_ACCENT).next_to(bullet2, DOWN, buff=0.5).align_to(bullet2, LEFT)
        bullet4 = Text("• General form: y = ax^2 + bx + c", font_size=30, color=BLUE_ACCENT).next_to(bullet3, DOWN, buff=0.5).align_to(bullet3, LEFT)
        bullet5 = Text("• a, b, c change the parabola's shape and position.", font_size=30, color=BLUE_ACCENT).next_to(bullet4, DOWN, buff=0.5).align_to(bullet4, LEFT)
        
        recap_group = VGroup(recap_title, bullet1, bullet2, bullet3, bullet4, bullet5).center()
        
        self.play(FadeIn(recap_title))
        self.play(Write(bullet1), run_time=1)
        self.play(Write(bullet2), run_time=1)
        self.play(Write(bullet3), run_time=1)
        self.play(Write(bullet4), run_time=1)
        self.play(Write(bullet5), run_time=1)
        self.wait(3)
        self.play(FadeOut(recap_group))
        self.wait(1)