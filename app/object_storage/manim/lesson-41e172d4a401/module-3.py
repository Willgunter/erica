from manim import *

class ParabolaIntercepts(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#202020" # Dark background
        blue_color = "#3399FF" # High-contrast blue
        gold_color = "#FFD700" # High-contrast gold
        red_color = "#FF6347" # For no solutions
        green_color = "#7CFC00" # For solutions

        # --- Beat 1: Visual Hook & Introduction to Parabola ---
        # Title
        title = Text("Parabola Intercepts & Solution Nature", font_size=48, color=gold_color)
        self.play(Write(title))
        self.wait(0.5)
        self.play(
            title.animate.to_corner(UP + LEFT).scale(0.7),
            run_time=0.8
        )

        # Number Plane and Axes
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": GRAY_A},
            background_line_style={"stroke_color": GRAY_D, "stroke_width": 1, "stroke_opacity": 0.6},
        ).add_coordinates()
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": GRAY_A},
        )
        x_axis_label = Text("X-axis", font_size=24, color=GRAY_A).next_to(axes.x_axis, DOWN)
        y_axis_label = Text("Y-axis", font_size=24, color=GRAY_A).next_to(axes.y_axis, LEFT)

        # Parabola function definition
        def parabola_func(x, a, b, c):
            return a * x**2 + b * x + c

        # Initial parabola (a=0.5, b=0, c=-2) for starting
        current_parabola = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, -2), color=blue_color, x_range=[-4, 4])
        parabola_label = Text("Parabola", font_size=30, color=blue_color).next_to(current_parabola, UP + RIGHT)

        # Hook: Dynamic drawing of the plane and parabola
        self.play(
            Create(plane),
            Create(axes),
            FadeIn(x_axis_label, y_axis_label)
        )
        self.wait(0.5)
        self.play(Create(current_parabola, run_time=2, rate_func=smooth))
        self.play(Write(parabola_label))
        self.wait(1)

        # What are intercepts?
        intercept_concept = Text("What are 'intercepts'?", font_size=36, color=gold_color).next_to(title, DOWN).align_to(title, LEFT)
        self.play(FadeIn(intercept_concept, shift=UP))
        self.wait(1)

        # Highlight x-axis for x-intercepts
        x_axis_highlight = Line(axes.x_axis.get_left(), axes.x_axis.get_right(), color=gold_color, stroke_width=4)
        x_intercept_text = Text("X-intercepts", font_size=30, color=gold_color).next_to(x_axis_highlight, DOWN*0.5)
        self.play(Create(x_axis_highlight), Write(x_intercept_text))
        self.wait(0.5)
        self.play(FadeOut(x_axis_highlight, x_intercept_text))

        # Highlight y-axis for y-intercepts
        y_axis_highlight = Line(axes.y_axis.get_bottom(), axes.y_axis.get_top(), color=blue_color, stroke_width=4)
        y_intercept_text = Text("Y-intercept", font_size=30, color=blue_color).next_to(y_axis_highlight, LEFT*0.5)
        self.play(Create(y_axis_highlight), Write(y_intercept_text))
        self.wait(0.5)
        self.play(FadeOut(y_axis_highlight, y_intercept_text))
        self.play(FadeOut(intercept_concept, parabola_label))
        self.wait(0.5)

        # --- Beat 2: Parabola's Interaction with the X-axis (Roots/Solutions) ---
        beat2_title = Text("Finding X-Intercepts", font_size=36, color=gold_color).next_to(title, DOWN).align_to(title, LEFT)
        self.play(FadeIn(beat2_title, shift=UP))
        self.wait(0.5)

        # Show the current parabola (a=0.5, b=0, c=-2) with its x-intercepts
        x_intercept_1 = Dot(axes.c2p(-2, 0), color=green_color, radius=0.15)
        x_intercept_2 = Dot(axes.c2p(2, 0), color=green_color, radius=0.15)

        intercept_label_1 = Text("x = -2", font_size=24, color=green_color).next_to(x_intercept_1, DOWN + LEFT)
        intercept_label_2 = Text("x = 2", font_size=24, color=green_color).next_to(x_intercept_2, DOWN + RIGHT)

        self.play(
            GrowFromCenter(x_intercept_1),
            GrowFromCenter(x_intercept_2),
            Write(intercept_label_1),
            Write(intercept_label_2)
        )
        self.wait(1)

        # Explain "solutions"
        solutions_text = Text("These are the 'solutions' or 'roots'", font_size=30, color=green_color).move_to(UP*2 + RIGHT*3)
        self.play(Write(solutions_text))
        self.play(
            Flash(x_intercept_1, flash_radius=0.3, line_length=0.3, color=green_color),
            Flash(x_intercept_2, flash_radius=0.3, line_length=0.3, color=green_color)
        )
        self.wait(1)

        # Concept: At x-intercepts, y = 0
        y_equals_0 = Text("At X-intercepts, Y = 0", font_size=30, color=blue_color).next_to(solutions_text, DOWN).align_to(solutions_text, LEFT)
        self.play(Write(y_equals_0))
        self.wait(1.5)
        
        # Fade out solutions text & labels, keep current_parabola for transition
        self.play(
            FadeOut(solutions_text, y_equals_0, intercept_label_1, intercept_label_2, x_intercept_1, x_intercept_2),
            FadeOut(beat2_title)
        )
        self.wait(0.5)

        # --- Beat 3: Different Cases of Intercepts ---
        beat3_title = Text("Nature of Solutions", font_size=36, color=gold_color).next_to(title, DOWN).align_to(title, LEFT)
        self.play(FadeIn(beat3_title, shift=UP))
        self.wait(0.5)

        # Case 1: Two Real Solutions (current_parabola already has 2)
        num_solutions_two = Text("Two Real Solutions", font_size=30, color=green_color).move_to(UP*2.5 + RIGHT*3)
        x_intercept_1_case1 = Dot(axes.c2p(-2, 0), color=green_color)
        x_intercept_2_case1 = Dot(axes.c2p(2, 0), color=green_color)
        
        self.play(
            Write(num_solutions_two),
            GrowFromCenter(x_intercept_1_case1),
            GrowFromCenter(x_intercept_2_case1)
        )
        self.wait(1.5)

        # Case 2: One Real Solution (tangent)
        parabola_one_root = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, 0), color=blue_color, x_range=[-4, 4])
        dot_one_root = Dot(axes.c2p(0, 0), color=blue_color)
        num_solutions_one = Text("One Real Solution", font_size=30, color=blue_color).move_to(num_solutions_two.get_center())

        self.play(
            Transform(current_parabola, parabola_one_root),
            ReplacementTransform(num_solutions_two, num_solutions_one), # Transform the text object
            FadeOut(x_intercept_1_case1, x_intercept_2_case1),
            GrowFromCenter(dot_one_root)
        )
        self.wait(1.5)

        # Case 3: No Real Solutions
        parabola_no_roots = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, 2), color=red_color, x_range=[-4, 4])
        num_solutions_none = Text("No Real Solutions", font_size=30, color=red_color).move_to(num_solutions_one.get_center())

        self.play(
            FadeOut(dot_one_root),
            Transform(current_parabola, parabola_no_roots),
            ReplacementTransform(num_solutions_one, num_solutions_none) # Transform the text object
        )
        self.wait(1.5)

        # Explain the movement visually
        arrow_up = Arrow(start=RIGHT*4 + UP*1.5, end=RIGHT*4 + UP*0.5, color=GRAY_A)
        explain_movement = Text("Parabola's position affects solutions!", font_size=28, color=gold_color).next_to(arrow_up, UP*0.5)

        self.play(FadeIn(explain_movement, arrow_up))
        
        # Animate parabola moving down to show 2 solutions again
        final_parabola_for_beat3 = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, -2), color=blue_color, x_range=[-4, 4])
        final_dot_1 = Dot(axes.c2p(-2, 0), color=green_color)
        final_dot_2 = Dot(axes.c2p(2, 0), color=green_color)

        self.play(
            Transform(current_parabola, final_parabola_for_beat3, run_time=1.5),
            FadeOut(num_solutions_none),
            LaggedStart(
                GrowFromCenter(final_dot_1),
                GrowFromCenter(final_dot_2),
                lag_ratio=0.5
            )
        )
        self.wait(1)
        self.play(FadeOut(explain_movement, arrow_up, beat3_title, final_dot_1, final_dot_2))
        self.wait(0.5)

        # --- Beat 4: Formal Notation (Connecting to y = ax^2 + bx + c) ---
        beat4_title = Text("The Equation: y = ax²+bx+c", font_size=36, color=gold_color).next_to(title, DOWN).align_to(title, LEFT)
        self.play(FadeIn(beat4_title, shift=UP))
        self.wait(0.5)

        # Building the equation using Text
        y_txt = Text("y", font_size=40, color=blue_color)
        equals_txt = Text("=", font_size=40, color=GRAY_B)
        a_txt = Text("a", font_size=40, color=gold_color)
        x_txt1 = Text("x", font_size=40, color=blue_color)
        exp_txt = Text("2", font_size=28, color=blue_color).scale(0.8).next_to(x_txt1, UP + RIGHT, buff=0.05) # superscript
        plus1_txt = Text("+", font_size=40, color=GRAY_B)
        b_txt = Text("b", font_size=40, color=gold_color)
        x_txt2 = Text("x", font_size=40, color=blue_color)
        plus2_txt = Text("+", font_size=40, color=GRAY_B)
        c_txt = Text("c", font_size=40, color=gold_color)

        # VGroup for the squared term
        ax_squared = VGroup(a_txt, x_txt1, exp_txt)
        
        equation_components = VGroup(
            y_txt, equals_txt, ax_squared, plus1_txt, b_txt, x_txt2, plus2_txt, c_txt
        ).arrange(RIGHT, buff=0.1)
        
        # Position the equation
        equation_components.move_to(UP*2.5 + RIGHT*3)

        self.play(Write(equation_components))
        self.wait(1)

        # Highlight 'a' and its effect
        a_param_text = Text("'a': Controls Opening Direction & Width", font_size=28, color=gold_color).next_to(equation_components, DOWN, buff=0.5).align_to(equation_components, LEFT)
        self.play(Indicate(a_txt, color=gold_color))
        self.play(Write(a_param_text))
        
        # Animate 'a' changing
        # current_parabola is already a=0.5, c=-2
        
        parabola_a_neg = axes.get_graph(lambda x: parabola_func(x, -0.5, 0, -2), color=blue_color, x_range=[-4, 4])
        self.play(Transform(current_parabola, parabola_a_neg), run_time=1) # a changes sign (opens down)
        self.wait(0.5)
        parabola_a_wide = axes.get_graph(lambda x: parabola_func(x, 0.1, 0, -2), color=blue_color, x_range=[-6, 6])
        self.play(Transform(current_parabola, parabola_a_wide), run_time=1) # |a| gets smaller (wider)
        self.wait(0.5)
        parabola_a_reset = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, -2), color=blue_color, x_range=[-4, 4])
        self.play(Transform(current_parabola, parabola_a_reset), FadeOut(a_param_text), run_time=1)
        self.wait(0.5)

        # Highlight 'c' and its effect (y-intercept)
        c_param_text = Text("'c': Controls Y-intercept (when x=0)", font_size=28, color=gold_color).next_to(equation_components, DOWN, buff=0.5).align_to(equation_components, LEFT)
        self.play(Indicate(c_txt, color=gold_color))
        self.play(Write(c_param_text))

        # Animate 'c' changing (vertical shift)
        dot_y_intercept = Dot(axes.c2p(0, -2), color=blue_color, radius=0.15)
        self.play(GrowFromCenter(dot_y_intercept))
        self.wait(0.5)

        parabola_c_zero = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, 0), color=blue_color, x_range=[-4, 4])
        dot_y_intercept_zero = Dot(axes.c2p(0, 0), color=blue_color, radius=0.15)
        self.play(
            Transform(current_parabola, parabola_c_zero),
            Transform(dot_y_intercept, dot_y_intercept_zero),
            run_time=1
        )
        self.wait(0.5)
        parabola_c_pos = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, 2), color=blue_color, x_range=[-4, 4])
        dot_y_intercept_pos = Dot(axes.c2p(0, 2), color=blue_color, radius=0.15)
        self.play(
            Transform(current_parabola, parabola_c_pos),
            Transform(dot_y_intercept, dot_y_intercept_pos),
            run_time=1
        )
        self.wait(0.5)
        
        # Reset parabola and fade out c explanation
        parabola_c_reset_final = axes.get_graph(lambda x: parabola_func(x, 0.5, 0, -2), color=blue_color, x_range=[-4, 4])
        self.play(
            Transform(current_parabola, parabola_c_reset_final),
            FadeOut(dot_y_intercept, c_param_text),
            run_time=1
        )

        self.play(
            FadeOut(current_parabola),
            FadeOut(beat4_title, equation_components),
            FadeOut(plane, axes, x_axis_label, y_axis_label) # Clear the plane for recap
        )
        self.wait(0.5)

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Parabola Intercepts", font_size=48, color=gold_color)
        
        # Create bullet points
        bullet1 = Text("1. X-intercepts are 'solutions' when y = 0.", font_size=36, color=blue_color)
        bullet2 = Text("2. A parabola can have 0, 1, or 2 X-intercepts.", font_size=36, color=blue_color)
        bullet3 = Text("3. 'a' controls direction/width; 'c' controls Y-intercept.", font_size=36, color=blue_color)

        recap_group = VGroup(
            recap_title,
            bullet1,
            bullet2,
            bullet3
        ).arrange(DOWN, center=True, buff=0.8)
        
        # Position the recap group
        recap_group.move_to(ORIGIN)

        self.play(
            FadeTransform(title, recap_title), # Transform the initial title to recap title
            LaggedStart(
                Write(bullet1),
                Write(bullet2),
                Write(bullet3),
                lag_ratio=0.5
            )
        )
        self.wait(3)
        self.play(FadeOut(recap_group))
        self.wait(0.5)