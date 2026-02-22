from manim import *

class DiscriminantAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = ManimColor("#1A73E8")  # A vibrant blue
        GOLD_ACCENT = ManimColor("#F7CE46")  # A bright gold
        GRAY_TEXT = ManimColor("#AAAAAA")    # Subtle gray for less emphasis

        # --- Helper for creating Text objects in the desired style ---
        # Using Monospace font helps with character alignment for math-like text
        def create_math_text(text_str, color=BLUE_ACCENT, font_size=40):
            return Text(text_str, font="Monospace", font_size=font_size, color=color)

        # --- Beat 1: Visual Hook & Introduction ---
        # Module Title
        title_text = "The Discriminant and Solution Types"
        title = create_math_text(title_text, font_size=50).to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 1. Quadratic Equation Appearance
        # Manually assemble "ax^2 + bx + c = 0" using Text objects
        a_text = create_math_text("a", color=GOLD_ACCENT)
        x2_text = create_math_text("x^2", color=BLUE_ACCENT)
        plus1 = create_math_text(" + ", color=GRAY_TEXT)
        b_text = create_math_text("b", color=GOLD_ACCENT)
        x_text_eq = create_math_text("x", color=BLUE_ACCENT)
        plus2 = create_math_text(" + ", color=GRAY_TEXT)
        c_text = create_math_text("c", color=GOLD_ACCENT)
        eq0 = create_math_text(" = 0", color=GRAY_TEXT)

        ax2 = VGroup(a_text, x2_text).arrange(RIGHT, buff=0.05)
        bx = VGroup(b_text, x_text_eq).arrange(RIGHT, buff=0.05)

        quadratic_equation = VGroup(
            ax2, plus1, bx, plus2, c_text, eq0
        ).arrange(RIGHT, buff=0.1)
        quadratic_equation.scale(0.8).next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(quadratic_equation, shift=UP), run_time=1.5)
        self.wait(1)

        # 2. NumberPlane and Parabola
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10, y_length=8,
            axis_config={"color": GRAY_TEXT, "stroke_width": 1.5},
            background_line_style={"stroke_color": GRAY_TEXT, "stroke_opacity": 0.3}
        ).add_coordinates().scale(0.6).shift(DOWN * 0.5)

        x_axis_label = create_math_text("x", font_size=20, color=GRAY_TEXT).next_to(plane.get_x_axis(), RIGHT, buff=0.1)
        y_axis_label = create_math_text("y", font_size=20, color=GRAY_TEXT).next_to(plane.get_y_axis(), UP, buff=0.1)

        # Example parabola with two real roots
        def func1(x):
            return 0.5 * x**2 - 1.5 * x - 2

        parabola1 = plane.get_graph(func1, x_range=[-4, 5], color=BLUE_ACCENT, stroke_width=4)
        x_intercepts1 = [plane.coords_to_point(-1, 0), plane.coords_to_point(4, 0)]
        dots1 = VGroup(*[Dot(point, color=GOLD_ACCENT, radius=0.08) for point in x_intercepts1])
        
        question_text = create_math_text("How many times does it cross the x-axis?", font_size=40).move_to(quadratic_equation.get_center())

        self.play(
            FadeOut(quadratic_equation, shift=UP),
            Transform(title, create_math_text("Visualizing Solutions:", font_size=50).move_to(title.get_center())),
            Write(question_text),
            run_time=1.5
        )
        self.play(
            FadeIn(plane, x_axis_label, y_axis_label),
            Create(parabola1),
            FadeIn(dots1, scale=0.8),
            run_time=2
        )
        self.wait(1)

        # --- Beat 2: Three Scenarios for Solutions ---
        # Scenario 1: Two Real Solutions (already shown)
        two_sol_label = create_math_text("Two Real Solutions", color=GOLD_ACCENT, font_size=32).next_to(plane, DOWN, buff=0.5)
        self.play(ReplacementTransform(question_text, two_sol_label), run_time=0.8)
        self.wait(1)

        # Scenario 2: One Real Solution
        def func2(x):
            return 0.5 * x**2 - 2 * x + 2

        parabola2 = plane.get_graph(func2, x_range=[-1, 5], color=BLUE_ACCENT, stroke_width=4)
        x_intercept2 = plane.coords_to_point(2, 0)
        dot2 = Dot(x_intercept2, color=GOLD_ACCENT, radius=0.08)
        one_sol_label = create_math_text("One Real Solution", color=GOLD_ACCENT, font_size=32).move_to(two_sol_label.get_center())

        self.play(
            ReplacementTransform(parabola1, parabola2),
            FadeOut(dots1),
            FadeIn(dot2),
            Transform(two_sol_label, one_sol_label), # Reuse two_sol_label to avoid multiple mobjects
            run_time=1.5
        )
        self.wait(1)

        # Scenario 3: No Real Solutions
        def func3(x):
            return 0.5 * x**2 - 2 * x + 3

        parabola3 = plane.get_graph(func3, x_range=[-1, 5], color=BLUE_ACCENT, stroke_width=4)
        no_sol_label = create_math_text("No Real Solutions", color=GOLD_ACCENT, font_size=32).move_to(two_sol_label.get_center())

        self.play(
            ReplacementTransform(parabola2, parabola3),
            FadeOut(dot2),
            Transform(two_sol_label, no_sol_label), # Reuse label
            run_time=1.5
        )
        self.wait(1)

        self.play(
            FadeOut(plane, x_axis_label, y_axis_label, parabola3, two_sol_label, shift=DOWN),
            Transform(title, create_math_text("How do we predict this without graphing?", font_size=45).move_to(title.get_center()))
        )
        self.wait(0.5)

        # --- Beat 3: Introducing the Quadratic Formula & The Discriminant ---
        # Manually construct quadratic formula parts using Text
        x_eq = create_math_text("x =", font_size=45)
        neg_b = create_math_text("-b", font_size=45)
        plus_minus = create_math_text(" ± ", font_size=45)
        sqrt_sym_open = create_math_text("sqrt(", font_size=45)
        discriminant_content_str = "b^2 - 4ac"
        discriminant_content = create_math_text(discriminant_content_str, color=GOLD_ACCENT, font_size=45)
        sqrt_sym_close = create_math_text(")", font_size=45)

        numerator_parts = VGroup(neg_b, plus_minus, sqrt_sym_open, discriminant_content, sqrt_sym_close).arrange(RIGHT, buff=0.1)
        
        # Calculate line length based on numerator width
        line_length = numerator_parts.get_width() * 1.1 
        fraction_line = Line(LEFT, RIGHT, color=GRAY_TEXT).set_width(line_length)
        
        two_a_denom = create_math_text("2a", font_size=45)

        # Arrange formula elements
        x_eq.to_edge(LEFT, buff=1.5).shift(UP*0.5)
        numerator_parts.next_to(x_eq, RIGHT, buff=0.5).shift(RIGHT*0.1)
        fraction_line.next_to(numerator_parts, DOWN, buff=0.2).set_x(numerator_parts.get_x()) # Center line under numerator
        two_a_denom.next_to(fraction_line, DOWN, buff=0.2)

        quadratic_formula_vg = VGroup(x_eq, numerator_parts, fraction_line, two_a_denom).center().shift(UP*0.5)
        
        self.play(
            Transform(title, create_math_text("The Quadratic Formula holds the key:", font_size=45).move_to(title.get_center())),
            FadeIn(x_eq, shift=LEFT),
            FadeIn(neg_b, plus_minus, sqrt_sym_open, sqrt_sym_close, shift=UP),
            Create(fraction_line),
            FadeIn(two_a_denom, shift=DOWN),
            run_time=2
        )
        self.wait(0.5)
        self.play(FadeIn(discriminant_content, scale=0.8), run_time=1) # Introduce the discriminant content
        self.wait(1)

        discriminant_label = create_math_text("The Discriminant", color=GOLD_ACCENT, font_size=35).next_to(discriminant_content, UP, buff=0.5)
        discriminant_label_arrow = Arrow(discriminant_label.get_bottom(), discriminant_content.get_top(), buff=0.1, color=GOLD_ACCENT)
        
        self.play(
            Create(discriminant_label_arrow),
            FadeIn(discriminant_label, shift=UP),
            run_time=1
        )
        self.wait(1)

        discriminant_definition = create_math_text("D = b^2 - 4ac", color=GOLD_ACCENT, font_size=40).to_edge(LEFT, buff=0.5).shift(DOWN*2)
        
        # Animate the discriminant part flowing into its definition
        self.play(
            ReplacementTransform(VGroup(discriminant_label, discriminant_label_arrow, discriminant_content).copy(), discriminant_definition),
            FadeOut(quadratic_formula_vg, shift=UP), 
            Transform(title, create_math_text("Meet the Discriminant (D):", font_size=45).move_to(title.get_center())),
            run_time=2
        )
        self.wait(1)

        # --- Beat 4: Connecting Discriminant Value to Solution Types ---
        self.play(
            FadeOut(title, shift=UP),
            discriminant_definition.animate.to_edge(UP).scale(0.8), # Move D definition to top
            run_time=1
        )
        self.wait(0.5)

        # Re-introduce a smaller plane for visual context for each case
        plane_small = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=6,
            axis_config={"color": GRAY_TEXT, "stroke_width": 1},
            background_line_style={"stroke_color": GRAY_TEXT, "stroke_opacity": 0.3}
        ).add_coordinates().scale(0.5).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        x_axis_label_small = create_math_text("x", font_size=15, color=GRAY_TEXT).next_to(plane_small.get_x_axis(), RIGHT, buff=0.1)
        y_axis_label_small = create_math_text("y", font_size=15, color=GRAY_TEXT).next_to(plane_small.get_y_axis(), UP, buff=0.1)
        self.play(FadeIn(plane_small, x_axis_label_small, y_axis_label_small), run_time=1)
        
        cases_title = create_math_text("D determines the number of real solutions:", font_size=35).to_edge(LEFT, buff=0.5).shift(UP*1.5)
        self.play(Write(cases_title), run_time=1)

        # Case 1: D > 0 (Two Real Solutions)
        d_greater_0_text = create_math_text("1. If D > 0:", color=BLUE_ACCENT, font_size=35).next_to(cases_title, DOWN, buff=0.5).align_to(cases_title, LEFT)
        example_d1 = create_math_text("e.g. D = 25", color=GOLD_ACCENT, font_size=30).next_to(d_greater_0_text, DOWN, buff=0.2).align_to(d_greater_0_text, LEFT)
        sqrt_d1 = create_math_text("sqrt(D) = sqrt(25) = 5", color=BLUE_ACCENT, font_size=30).next_to(example_d1, DOWN, buff=0.2).align_to(d_greater_0_text, LEFT)
        result_d1 = create_math_text("Two distinct real solutions!", color=GOLD_ACCENT, font_size=30).next_to(sqrt_d1, DOWN, buff=0.2).align_to(d_greater_0_text, LEFT)

        def func_case1(x): return 0.5 * x**2 - 1.5 * x - 0.5 # Two roots
        parabola_case1 = plane_small.get_graph(func_case1, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=3)
        dots_case1 = VGroup(*[
            Dot(plane_small.coords_to_point(-0.29, 0), color=GOLD_ACCENT, radius=0.06), 
            Dot(plane_small.coords_to_point(3.29, 0), color=GOLD_ACCENT, radius=0.06)
        ])

        self.play(
            Write(d_greater_0_text),
            FadeIn(example_d1, shift=LEFT),
            Create(parabola_case1),
            FadeIn(dots_case1),
            run_time=1.5
        )
        self.play(Write(sqrt_d1), run_time=0.8)
        self.play(Write(result_d1), run_time=0.8)
        self.wait(1.5)

        # Case 2: D = 0 (One Real Solution)
        d_equal_0_text = create_math_text("2. If D = 0:", color=BLUE_ACCENT, font_size=35).move_to(d_greater_0_text.get_center()).align_to(cases_title, LEFT)
        example_d2 = create_math_text("e.g. D = 0", color=GOLD_ACCENT, font_size=30).move_to(example_d1.get_center()).align_to(d_equal_0_text, LEFT)
        sqrt_d2 = create_math_text("sqrt(D) = sqrt(0) = 0", color=BLUE_ACCENT, font_size=30).move_to(sqrt_d1.get_center()).align_to(d_equal_0_text, LEFT)
        result_d2 = create_math_text("One real solution!", color=GOLD_ACCENT, font_size=30).move_to(result_d1.get_center()).align_to(d_equal_0_text, LEFT)

        def func_case2(x): return 0.5 * x**2 - 1.5 * x + 1.125 # One root (vertex on x-axis)
        parabola_case2 = plane_small.get_graph(func_case2, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=3)
        dot_case2 = Dot(plane_small.coords_to_point(1.5, 0), color=GOLD_ACCENT, radius=0.06)

        self.play(
            FadeTransform(VGroup(d_greater_0_text, example_d1, sqrt_d1, result_d1, dots_case1), VGroup(d_equal_0_text, example_d2, sqrt_d2, result_d2)),
            Transform(parabola_case1, parabola_case2),
            FadeIn(dot_case2),
            run_time=2
        )
        self.wait(1.5)

        # Case 3: D < 0 (No Real Solutions)
        d_less_0_text = create_math_text("3. If D < 0:", color=BLUE_ACCENT, font_size=35).move_to(d_equal_0_text.get_center()).align_to(cases_title, LEFT)
        example_d3 = create_math_text("e.g. D = -4", color=GOLD_ACCENT, font_size=30).move_to(example_d2.get_center()).align_to(d_less_0_text, LEFT)
        sqrt_d3 = create_math_text("sqrt(D) = sqrt(-4) = Not Real", color=BLUE_ACCENT, font_size=30).move_to(sqrt_d2.get_center()).align_to(d_less_0_text, LEFT)
        result_d3 = create_math_text("No real solutions!", color=GOLD_ACCENT, font_size=30).move_to(result_d2.get_center()).align_to(d_less_0_text, LEFT)

        def func_case3(x): return 0.5 * x**2 - 1.5 * x + 2 # No roots
        parabola_case3 = plane_small.get_graph(func_case3, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=3)

        self.play(
            FadeTransform(VGroup(d_equal_0_text, example_d2, sqrt_d2, result_d2, dot_case2), VGroup(d_less_0_text, example_d3, sqrt_d3, result_d3)),
            Transform(parabola_case1, parabola_case3), # parabola_case1 is currently parabola_case2
            run_time=2
        )
        self.wait(1.5)

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(discriminant_definition, cases_title, d_less_0_text, example_d3, sqrt_d3, result_d3, parabola_case1,
                    plane_small, x_axis_label_small, y_axis_label_small, shift=DOWN),
            run_time=1.5
        )
        self.wait(0.5)

        recap_title = create_math_text("Recap: The Discriminant (D)", color=GOLD_ACCENT, font_size=45).to_edge(UP, buff=1)
        recap_d_def = create_math_text("D = b^2 - 4ac", color=BLUE_ACCENT, font_size=40).next_to(recap_title, DOWN, buff=0.5)

        # Using create_math_text for consistent styling, align to the left of the recap_d_def
        recap_item1 = create_math_text("• D > 0: Two Real Solutions", color=GOLD_ACCENT, font_size=35).next_to(recap_d_def, DOWN, buff=0.7).align_to(recap_d_def, LEFT)
        recap_item2 = create_math_text("• D = 0: One Real Solution", color=BLUE_ACCENT, font_size=35).next_to(recap_item1, DOWN, buff=0.4).align_to(recap_d_def, LEFT)
        recap_item3 = create_math_text("• D < 0: No Real Solutions", color=GOLD_ACCENT, font_size=35).next_to(recap_item2, DOWN, buff=0.4).align_to(recap_d_def, LEFT)

        self.play(Write(recap_title), run_time=1)
        self.play(Write(recap_d_def), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(recap_item1, shift=LEFT), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(recap_item2, shift=LEFT), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(recap_item3, shift=LEFT), run_time=0.8)
        self.wait(3)

        # Final fade out
        self.play(
            FadeOut(recap_title, shift=UP),
            FadeOut(recap_d_def, shift=UP),
            FadeOut(recap_item1, shift=UP),
            FadeOut(recap_item2, shift=UP),
            FadeOut(recap_item3, shift=UP)
        )
        self.wait(1)