from manim import *

class QuadraticEquations(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = '#6DAFF7' # Lighter blue for contrast on dark backgrounds
        GOLD_ACCENT = '#FFD700' # Standard gold

        # --- Beat 1: Visual Hook - The Path of a Ball ---
        title = Text("Understanding Quadratic Equations", font_size=50, color=BLUE_ACCENT)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7), run_time=1)

        # Setup NumberPlane
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-2, 8, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": BLUE_ACCENT, "stroke_width": 2},
            background_line_style={"stroke_color": BLUE_ACCENT, "stroke_opacity": 0.2, "stroke_width": 1}
        ).add_coordinates().shift(DOWN*0.5)

        # A specific quadratic for the ball path: y = -0.5x^2 + 2x + 4.5
        parabola_func = lambda x: -0.5 * x**2 + 2 * x + 4.5
        parabola_mobj = plane.get_graph(parabola_func, x_range=[-2, 6], color=GOLD_ACCENT, stroke_width=4)

        ball = Dot(point=plane.coords_to_point(-2, parabola_func(-2)), color=GOLD_ACCENT, radius=0.15)
        question_text = Text("Where does it land?", color=BLUE_ACCENT, font_size=30).next_to(plane, DOWN, buff=0.7)

        self.play(Create(plane, run_time=1.5), FadeIn(parabola_mobj, shift=UP*0.5, run_time=1.5))
        self.play(MoveAlongPath(ball, parabola_mobj), run_time=3, rate_func=linear)
        self.play(FadeIn(question_text, shift=UP), run_time=1)
        self.wait(1)
        
        # Move everything off-screen left to clear for next beat
        self.play(FadeOut(ball, parabola_mobj, question_text))
        self.play(plane.animate.shift(LEFT * config.frame_width), run_time=1) 

        # --- Beat 2: Introducing the Equation: y = ax^2 + bx + c ---
        general_form_y = MathTex("y = ax^2 + bx + c", color=BLUE_ACCENT, font_size=60)
        self.play(Transform(title, general_form_y), run_time=1) # Transform title into the equation
        
        # Explain coefficients
        a_text = MathTex("a \\text{: Controls opening (up/down) and width}", color=BLUE_ACCENT, font_size=35).next_to(general_form_y, DOWN, buff=0.7).align_to(general_form_y, LEFT)
        c_text = MathTex("c \\text{: Is the y-intercept}", color=BLUE_ACCENT, font_size=35).next_to(a_text, DOWN, buff=0.3).align_to(general_form_y, LEFT)
        
        # Highlight 'a' and 'c' in the equation
        a_highlight = MathTex("y = \\textbf{a}x^2 + bx + c", color=BLUE_ACCENT, font_size=60).move_to(general_form_y.get_center())
        c_highlight = MathTex("y = ax^2 + bx + \\textbf{c}", color=BLUE_ACCENT, font_size=60).move_to(general_form_y.get_center())

        self.play(Write(a_text), run_time=1)
        self.play(ReplacementTransform(general_form_y, a_highlight), run_time=0.7)
        self.wait(0.5)
        self.play(Transform(a_highlight, c_highlight), run_time=0.7)
        self.play(Write(c_text), run_time=1)
        self.wait(1)

        # Introduce the 'solving for 0' concept
        solve_for_zero_text = Text("We often want to find 'x' when y = 0", color=BLUE_ACCENT, font_size=35).next_to(c_text, DOWN, buff=0.7)
        quadratic_equation = MathTex("ax^2 + bx + c = 0", color=BLUE_ACCENT, font_size=60)
        quadratic_equation.move_to(general_form_y.get_center())

        self.play(Write(solve_for_zero_text), run_time=1)
        self.play(FadeOut(a_text, c_highlight, c_text), Transform(solve_for_zero_text, quadratic_equation), run_time=1.5)
        self.wait(1)

        # --- Beat 3: The Roots: Where it Crosses Zero ---
        self.play(FadeOut(quadratic_equation), run_time=0.5)
        
        # Reset plane position off-screen to the right and slide it in
        plane.shift(config.frame_width * 2 * RIGHT) # Place it far right
        self.play(plane.animate.shift(LEFT * config.frame_width), run_time=1.5) # Slide it to the center

        # Re-plot a generic parabola for root demonstration
        parabola_base_func = lambda x: 0.5 * x**2 - 2 * x + 1.5
        parabola_roots = plane.get_graph(parabola_base_func, x_range=[-1, 5], color=GOLD_ACCENT, stroke_width=4)
        root1_coords = plane.coords_to_point(1, 0)
        root2_coords = plane.coords_to_point(3, 0)
        root1_dot = Dot(root1_coords, color=GOLD_ACCENT, radius=0.15)
        root2_dot = Dot(root2_coords, color=GOLD_ACCENT, radius=0.15)

        roots_label = Text("These are the 'roots' or 'solutions'", color=BLUE_ACCENT, font_size=35).to_edge(UP)

        self.play(Create(parabola_roots), run_time=1)
        self.play(FadeIn(root1_dot, root2_dot, shift=UP), Write(roots_label), run_time=1.5)
        self.wait(1)

        # Demonstrate 0, 1, 2 roots by shifting the parabola
        parabola_no_roots = plane.get_graph(lambda x: 0.5 * x**2 - 2 * x + 4.5, x_range=[-1, 5], color=GOLD_ACCENT, stroke_width=4)
        parabola_one_root = plane.get_graph(lambda x: 0.5 * x**2 - 2 * x + 2, x_range=[-1, 5], color=GOLD_ACCENT, stroke_width=4)
        one_root_dot = Dot(plane.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.15)

        self.play(FadeOut(roots_label, root1_dot, root2_dot), run_time=0.5)
        num_roots_text = Text("0, 1, or 2 Real Roots", color=BLUE_ACCENT, font_size=40).to_edge(UP)
        self.play(FadeIn(num_roots_text), run_time=1)
        
        roots_count = Text("0 Real Roots", color=BLUE_ACCENT, font_size=30).next_to(plane, DOWN, buff=0.7)
        self.play(Transform(parabola_roots, parabola_no_roots), Write(roots_count), run_time=1.5)
        self.wait(0.7)

        self.play(Transform(parabola_roots, parabola_one_root), Transform(roots_count, Text("1 Real Root", color=BLUE_ACCENT, font_size=30).next_to(plane, DOWN, buff=0.7)), FadeIn(one_root_dot), run_time=1.5)
        self.wait(0.7)

        self.play(Transform(parabola_roots, plane.get_graph(parabola_base_func, x_range=[-1, 5], color=GOLD_ACCENT, stroke_width=4)),
                  Transform(roots_count, Text("2 Real Roots", color=BLUE_ACCENT, font_size=30).next_to(plane, DOWN, buff=0.7)),
                  FadeIn(root1_dot, root2_dot), FadeOut(one_root_dot), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(parabola_roots, root1_dot, root2_dot, roots_count, num_roots_text), run_time=1)
        self.play(plane.animate.shift(LEFT * config.frame_width), run_time=1) # Move plane off-screen left

        # --- Beat 4: The Quadratic Formula: The Key ---
        equation_context = MathTex("ax^2 + bx + c = 0", color=BLUE_ACCENT, font_size=50).to_edge(UP)
        self.play(FadeIn(equation_context, shift=UP), run_time=1)

        quadratic_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=GOLD_ACCENT,
            font_size=70
        ).move_to(ORIGIN)

        formula_label = Text("The Quadratic Formula", color=BLUE_ACCENT, font_size=40).next_to(quadratic_formula, UP, buff=0.7)
        
        self.play(Write(formula_label), run_time=1)
        self.play(LaggedStart(
            FadeIn(quadratic_formula[0][0:2]), # x =
            FadeIn(quadratic_formula[0][2:]), # rest of formula
            lag_ratio=0.3,
            run_time=2.5
        ))
        self.wait(1)

        # Briefly highlight 'a', 'b', 'c' mapping
        a_map = Arrow(equation_context[0][0].get_center(), quadratic_formula[0][11].get_center(), buff=0.1, color=BLUE_ACCENT, stroke_width=3, max_stroke_width_to_length_ratio=3)
        b_map = Arrow(equation_context[0][4].get_center(), quadratic_formula[0][3].get_center(), buff=0.1, color=BLUE_ACCENT, stroke_width=3, max_stroke_width_to_length_ratio=3)
        c_map = Arrow(equation_context[0][8].get_center(), quadratic_formula[0][10].get_center(), buff=0.1, color=BLUE_ACCENT, stroke_width=3, max_stroke_width_to_length_ratio=3)
        
        self.play(Create(a_map), Create(b_map), Create(c_map), run_time=1.5)
        self.wait(0.7)
        self.play(FadeOut(a_map, b_map, c_map), run_time=0.7)

        # --- Beat 5: A Simple Example: Finding the Roots ---
        self.play(FadeOut(formula_label), run_time=0.5)
        example_eq_text = Text("Example: x² - 2x - 3 = 0", color=BLUE_ACCENT, font_size=45).to_edge(UP).shift(LEFT*1.5)
        self.play(Transform(equation_context, example_eq_text), run_time=1) # Transform the previous equation text

        abc_values = MathTex("a=1, b=-2, c=-3", color=BLUE_ACCENT, font_size=40).next_to(example_eq_text, RIGHT, buff=0.5)
        self.play(Write(abc_values), run_time=1)
        self.wait(0.5)

        # Substitute and solve (display simplified steps/result) - quick transitions for brevity
        solution_step1 = MathTex("x = \\frac{-(-2) \\pm \\sqrt{(-2)^2 - 4(1)(-3)}}{2(1)}", color=GOLD_ACCENT, font_size=50).move_to(quadratic_formula.get_center())
        solution_step2 = MathTex("x = \\frac{2 \\pm \\sqrt{4 + 12}}{2}", color=GOLD_ACCENT, font_size=50).move_to(quadratic_formula.get_center())
        solution_step3 = MathTex("x = \\frac{2 \\pm \\sqrt{16}}{2}", color=GOLD_ACCENT, font_size=50).move_to(quadratic_formula.get_center())
        solution_step4 = MathTex("x = \\frac{2 \\pm 4}{2}", color=GOLD_ACCENT, font_size=50).move_to(quadratic_formula.get_center())
        
        self.play(Transform(quadratic_formula, solution_step1), run_time=0.8)
        self.play(Transform(quadratic_formula, solution_step2), run_time=0.8)
        self.play(Transform(quadratic_formula, solution_step3), run_time=0.8)
        self.play(Transform(quadratic_formula, solution_step4), run_time=0.8)
        self.wait(0.5)

        final_solutions = MathTex("x_1 = 3, \\quad x_2 = -1", color=GOLD_ACCENT, font_size=55).move_to(quadratic_formula.get_center())
        self.play(Transform(quadratic_formula, final_solutions), run_time=1)
        self.wait(1)
        
        # Plot and confirm
        self.play(FadeOut(example_eq_text, abc_values), run_time=0.5)
        plane.shift(config.frame_width * 2 * RIGHT) # Place plane far right
        self.play(plane.animate.shift(LEFT * config.frame_width), run_time=1.5) # Slide plane to the left

        example_parabola_func = lambda x: x**2 - 2 * x - 3
        example_parabola = plane.get_graph(example_parabola_func, x_range=[-2, 4], color=GOLD_ACCENT, stroke_width=4)
        root_dot_1 = Dot(plane.coords_to_point(3, 0), color=GOLD_ACCENT, radius=0.15)
        root_dot_2 = Dot(plane.coords_to_point(-1, 0), color=GOLD_ACCENT, radius=0.15)
        
        self.play(Create(example_parabola), FadeIn(root_dot_1, root_dot_2), run_time=1.5)
        self.play(final_solutions.animate.to_edge(UP).shift(RIGHT*2), run_time=1)
        self.wait(2)

        self.play(FadeOut(final_solutions, example_parabola, root_dot_1, root_dot_2), run_time=1)
        self.play(plane.animate.shift(RIGHT * config.frame_width), run_time=1.5) # Slide plane off-screen right


        # --- Recap Card ---
        recap_title = Text("Recap: Quadratic Equations", font_size=50, color=BLUE_ACCENT).to_edge(UP)
        
        recap_p1_text = Text("Form:", font_size=35, color=BLUE_ACCENT)
        recap_p1_eq = MathTex("ax^2 + bx + c = 0", color=GOLD_ACCENT, font_size=35)
        recap_p1 = VGroup(recap_p1_text, recap_p1_eq).arrange(RIGHT, buff=0.2)

        recap_p2 = Text("Solutions are 'roots' / x-intercepts.", font_size=35, color=BLUE_ACCENT).align_to(recap_p1, LEFT)
        recap_p3 = Text("Found using the Quadratic Formula.", font_size=35, color=BLUE_ACCENT).align_to(recap_p1, LEFT)

        recap_points = VGroup(recap_p1, recap_p2, recap_p3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(recap_title, DOWN, buff=1)
        
        self.play(Write(recap_title), run_time=1)
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.5) for p in recap_points], lag_ratio=0.3, run_time=3))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_points), run_time=1)

        # End screen / outro
        thanks = Text("Thanks for watching!", font_size=40, color=BLUE_ACCENT)
        self.play(Write(thanks), run_time=1)
        self.wait(2)