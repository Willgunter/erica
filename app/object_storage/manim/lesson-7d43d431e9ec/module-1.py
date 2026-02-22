from manim import *

class IntroToQuadraticEquations(Scene):
    def construct(self):
        # --- 0. Scene Setup ---
        self.camera.background_color = BLACK
        blue_accent = BLUE_C
        gold_accent = GOLD_C
        line_color = BLUE_D # For axes and initial path

        # --- 1. Strong Visual Hook: The Parabolic Path ---
        # Title Card
        title = Text("Introduction to Quadratic Equations", font_size=50, color=gold_accent)
        title.shift(UP*2.5)
        subtitle = Text("Describing Curved Paths, Areas, & More", font_size=30, color=blue_accent)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Ball tracing a parabola (representing motion, e.g., a thrown object)
        axes_hook = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-1, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": line_color, "include_numbers": False},
        ).shift(DOWN*0.5)

        # Plot a simple parabola for the ball path
        parabola_func_hook = lambda x: -0.5 * (x - 0.5)**2 + 4.2
        path_hook = axes_hook.plot(parabola_func_hook, color=gold_accent, x_range=[-2.5, 3.5])

        ball = Dot(color=blue_accent, radius=0.1).move_to(axes_hook.coords_to_point(-2.5, parabola_func_hook(-2.5)))

        self.play(Create(axes_hook), run_time=1)
        self.add(ball)
        self.play(MoveAlongPath(ball, path_hook), Create(path_hook, run_time=2.5, lag_ratio=0.1), rate_func=linear) # rate_func for path drawing
        self.play(FadeOut(ball))

        # Text: "This curve is everywhere!"
        curve_text = Text("This curve describes so much!", font_size=36, color=gold_accent).next_to(path_hook, UP*0.5)
        self.play(Write(curve_text), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(curve_text))

        # --- 2. Intuition: The Power of x² ---
        # Transform the initial path into a canonical y=x^2 graph
        # Create new, simpler axes for y=x^2 centered
        axes_centered = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": line_color, "include_numbers": True},
        ).to_edge(LEFT, buff=1) # Move to left to make space for explanation

        graph_x2 = axes_centered.plot(lambda x: x**2, color=gold_accent)
        label_x2 = axes_centered.get_graph_label(graph_x2, label=r"x^2", x_val=2.5, direction=UP+RIGHT*0.2)

        eq_y_x2 = MathTex(r"y = x^2", color=blue_accent, font_size=48).shift(RIGHT*3 + UP*2)

        self.play(
            Transform(path_hook, graph_x2), # Transform the previous path object
            FadeOut(axes_hook), # Fade out old axes
            Create(axes_centered), # Create new axes
            Write(eq_y_x2),
            run_time=1.5
        )
        self.play(Write(label_x2))
        self.wait(0.5)

        # Explanation of x^2 effect
        exp_text1 = Text("The 'x²' term creates this signature parabola.", font_size=28, color=gold_accent).next_to(eq_y_x2, DOWN*2, alignment=LEFT)
        exp_text2 = Text("It makes values grow rapidly in both directions.", font_size=28, color=gold_accent).next_to(exp_text1, DOWN*0.5, alignment=LEFT)

        self.play(Write(exp_text1))
        self.wait(0.5)
        self.play(Write(exp_text2))
        self.wait(1)

        # Example points for y=x^2
        points_val = [-2, -1, 0, 1, 2]
        points_graph = VGroup()
        for x_val in points_val:
            dot = Dot(axes_centered.coords_to_point(x_val, x_val**2), color=blue_accent, radius=0.08)
            points_graph.add(dot)
        self.play(FadeIn(points_graph, scale=0.5))
        self.wait(0.5)
        self.play(FadeOut(points_graph, exp_text1, exp_text2, label_x2))


        # --- 3. The General Form: ax² + bx + c ---
        # Transition to the general form equation
        eq_general_form = MathTex(r"y = ax^2 + bx + c", color=blue_accent, font_size=48).move_to(eq_y_x2)
        self.play(TransformMatchingTex(eq_y_x2, eq_general_form))
        self.wait(0.5)

        # Explain 'c' (vertical shift)
        c_term_tex = eq_general_form.get_part_by_tex("c") # Get the 'c' part of the MathTex object
        c_effect_text = Text("+ c: Moves the curve UP or DOWN.", font_size=28, color=gold_accent).next_to(eq_general_form, DOWN*2, alignment=LEFT)

        graph_x2_plus_c = axes_centered.plot(lambda x: x**2 + 2, color=blue_accent)
        self.play(c_term_tex.animate.set_color(gold_accent), Write(c_effect_text))
        self.play(Transform(graph_x2, graph_x2_plus_c), run_time=1.5) # x^2 -> x^2 + 2
        self.wait(0.5)
        self.play(c_term_tex.animate.set_color(blue_accent), FadeOut(c_effect_text))

        # Explain 'a' (stretch/compress/flip)
        a_term_tex = eq_general_form.get_part_by_tex("a")
        a_effect_text = Text("a: Stretches, compresses, or flips the curve.", font_size=28, color=gold_accent).next_to(eq_general_form, DOWN*2, alignment=LEFT)

        graph_ax2 = axes_centered.plot(lambda x: -0.5*x**2 + 2, color=gold_accent) # a = -0.5, flipped and wider
        self.play(a_term_tex.animate.set_color(gold_accent), Write(a_effect_text))
        self.play(Transform(graph_x2_plus_c, graph_ax2), run_time=1.5)
        self.wait(0.5)
        self.play(a_term_tex.animate.set_color(blue_accent), FadeOut(a_effect_text))

        # Briefly mention 'bx'
        b_term_tex = eq_general_form.get_part_by_tex("bx")
        b_effect_text = Text("+ bx: Shifts the curve horizontally (and tilts).", font_size=28, color=gold_accent).next_to(eq_general_form, DOWN*2, alignment=LEFT)
        self.play(b_term_tex.animate.set_color(gold_accent), Write(b_effect_text))
        self.wait(1)
        self.play(b_term_tex.animate.set_color(blue_accent), FadeOut(b_effect_text))


        # --- 4. Finding Solutions: ax² + bx + c = 0 ---
        # Transform y = ... to ... = 0
        eq_zero_form = MathTex(r"ax^2 + bx + c = 0", color=blue_accent, font_size=48).move_to(eq_general_form)
        self.play(ReplacementTransform(eq_general_form, eq_zero_form))
        self.wait(0.5)

        # Explanation of what = 0 means
        zero_meaning = Text("Finding 'x' when y = 0.", font_size=36, color=gold_accent).next_to(eq_zero_form, DOWN*2)
        self.play(Write(zero_meaning))
        self.wait(0.5)

        # Show x-intercepts on the graph
        # Let's use the graph_ax2 we had, which was -0.5x^2 + 2. Roots are x = +-2
        root1_dot = Dot(axes_centered.coords_to_point(-2, 0), color=RED_C, radius=0.12)
        root2_dot = Dot(axes_centered.coords_to_point(2, 0), color=RED_C, radius=0.12)

        root_label1 = MathTex(r"x_1", color=RED_C).next_to(root1_dot, DOWN)
        root_label2 = MathTex(r"x_2", color=RED_C).next_to(root2_dot, DOWN)

        self.play(FadeIn(root1_dot, scale=1.5), FadeIn(root2_dot, scale=1.5))
        self.play(Write(root_label1), Write(root_label2))
        self.wait(1)

        roots_text = Text("These are the 'roots' or 'solutions'.", font_size=32, color=gold_accent).next_to(zero_meaning, DOWN)
        self.play(Write(roots_text))
        self.wait(1)

        self.play(FadeOut(axes_centered, graph_ax2, root1_dot, root2_dot, root_label1, root_label2, zero_meaning, roots_text, eq_zero_form))

        # --- 5. Recap Card ---
        recap_title = Text("Recap: Quadratic Equations", font_size=45, color=gold_accent).shift(UP*2.5)
        recap_bullets = BulletedList(
            "Describe curved paths & shapes.",
            "General form:  $ax^2 + bx + c = 0$",
            "Solving means finding where the curve crosses the x-axis (roots).",
            font_size=32, color=blue_accent, buff=0.7
        ).next_to(recap_title, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        recap_bullets.set_color_by_tex_to_color_map({
            "ax^2 + bx + c = 0": GOLD_C
        })

        self.play(Write(recap_title), LaggedStart(*[FadeIn(bullet, shift=UP*0.5) for bullet in recap_bullets]), run_time=3)
        self.wait(3)
        self.play(FadeOut(recap_title, recap_bullets))
        self.wait(0.5)