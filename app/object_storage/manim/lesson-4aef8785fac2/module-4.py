from manim import *

class DiscriminantAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#1A1A2E" # Dark Blue-Purple
        BLUE_ACCENT = "#4287f5" # Bright Blue
        GOLD_ACCENT = "#FFD700" # Gold
        TEXT_COLOR = WHITE

        # --- Beat 1: Visual Hook & Introducing Quadratic Formula ---
        # Strong visual hook: A parabola and its roots
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-2, 8, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": LIGHT_GRAY},
            background_line_style={"stroke_opacity": 0.3}
        ).shift(DOWN*0.5) # Shift plane down to make room for title
        
        # Example: y = (x-1)(x-3) = x^2 - 4x + 3 (Discriminant = 4 > 0)
        parabola_curve_initial = plane.get_graph(
            lambda x: (x-1)*(x-3),
            x_range=[-1, 5],
            color=BLUE_ACCENT
        )
        x_intercept_1 = Dot(plane.c2p(1, 0), color=GOLD_ACCENT, radius=0.1)
        x_intercept_2 = Dot(plane.c2p(3, 0), color=GOLD_ACCENT, radius=0.1)
        
        # Initial title for the whole animation
        title = Text("Analyzing Solutions with the Discriminant", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.play(
            Create(plane),
            Create(parabola_curve_initial),
            FadeIn(x_intercept_1, x_intercept_2)
        )
        self.wait(1.5)

        # Introduce the quadratic formula (using Text only, no MathTex/Tex)
        quadratic_formula_label = Text("Quadratic Formula", font_size=36, color=TEXT_COLOR).next_to(parabola_curve_initial, UP, buff=0.8)
        
        x_eq = Text("x = ", color=TEXT_COLOR).scale(0.7)
        minus_b = Text("-b", color=TEXT_COLOR).scale(0.7)
        plus_minus_sqrt = Text("±√", color=TEXT_COLOR).scale(0.7) # Combined Unicode symbols
        b_sq_minus_4ac = Text("b² - 4ac", color=TEXT_COLOR).scale(0.7) # Discriminant part
        two_a = Text("2a", color=TEXT_COLOR).scale(0.7)

        # Arrange numerator parts horizontally
        numerator_elements = VGroup(minus_b, plus_minus_sqrt, b_sq_minus_4ac).arrange(RIGHT, buff=0.1)
        
        # Create fraction bar based on numerator width
        fraction_bar_width = numerator_elements.width * 1.1
        fraction_bar = Line(LEFT, RIGHT).set_color(TEXT_COLOR).set_length(fraction_bar_width)
        
        # Arrange numerator, fraction bar, and denominator vertically
        # Use a temporary VGroup to calculate overall height for placement
        fractional_part_temp = VGroup(numerator_elements, fraction_bar, two_a).arrange(DOWN, buff=0.2)
        
        # Combine 'x = ' and the fractional part
        quadratic_formula_group = VGroup(x_eq, fractional_part_temp).arrange(RIGHT, buff=0.1).move_to(BOTTOM).shift(UP*1.5)
        
        self.play(
            FadeOut(parabola_curve_initial, x_intercept_1, x_intercept_2),
            plane.animate.shift(LEFT*3), # Shift plane to the left to make room
            Write(quadratic_formula_label),
            FadeIn(quadratic_formula_group)
        )
        self.wait(1.5)
        
        # Highlight the discriminant part
        discriminant_highlight = SurroundingRectangle(b_sq_minus_4ac, color=GOLD_ACCENT, buff=0.1)
        
        self.play(Create(discriminant_highlight, run_time=1))
        self.wait(1)
        
        # --- Beat 2: Isolating the Discriminant & its Role (Intuition) ---
        discriminant_expression = b_sq_minus_4ac.copy().scale(1.2).move_to(RIGHT*3.5 + UP*1.5)
        discriminant_label = Text("The Discriminant (D)", color=GOLD_ACCENT).next_to(discriminant_expression, UP, buff=0.5)
        discriminant_function_text = Text("Determines the number and type of solutions", font_size=30, color=TEXT_COLOR).next_to(discriminant_expression, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(b_sq_minus_4ac, discriminant_expression),
            FadeOut(quadratic_formula_group, quadratic_formula_label, discriminant_highlight),
            Write(discriminant_label),
            Write(discriminant_function_text),
        )
        self.wait(1)
        
        # Show cases intuitively
        cases_text_d = VGroup(
            Text("If D > 0:", color=TEXT_COLOR),
            Text("If D = 0:", color=TEXT_COLOR),
            Text("If D < 0:", color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.8).next_to(discriminant_function_text, DOWN, buff=1.0).align_to(discriminant_function_text, LEFT)
        
        results_text_d = VGroup(
            Text("√ (positive) = Real numbers", color=BLUE_ACCENT),
            Text("√ (zero) = Zero", color=BLUE_ACCENT),
            Text("√ (negative) = Not Real numbers", color=BLUE_ACCENT)
        ).arrange(DOWN, buff=0.8).next_to(cases_text_d, RIGHT, buff=0.8, aligned_edge=UP)
        
        self.play(
            LaggedStart(*[Write(t) for t in cases_text_d], lag_ratio=0.5),
            LaggedStart(*[Write(r) for r in results_text_d], lag_ratio=0.5),
            run_time=3
        )
        self.wait(2)
        
        self.play(
            FadeOut(discriminant_expression, discriminant_label, discriminant_function_text, cases_text_d, results_text_d)
        )

        # Reposition title and plane for case descriptions
        self.play(
            Transform(title, Text("D > 0: Two Real Solutions", color=GOLD_ACCENT, font_size=48).to_edge(UP)),
            plane.animate.center() # Animate the existing plane back to center
        )
        
        # --- Beat 3: Case 1: D > 0 (Two Real Solutions) ---
        parabola_curve_two_roots = plane.get_graph(
            lambda x: (x-1)*(x-3), # y = x^2 - 4x + 3
            x_range=[-1, 5],
            color=BLUE_ACCENT
        )
        dot1 = Dot(plane.c2p(1, 0), color=GOLD_ACCENT, radius=0.1)
        dot2 = Dot(plane.c2p(3, 0), color=GOLD_ACCENT, radius=0.1)
        
        self.play(
            Create(parabola_curve_two_roots),
            FadeIn(dot1, dot2)
        )
        self.wait(2)
        
        # --- Beat 4: Case 2: D = 0 (One Real Solution) ---
        self.play(
            Transform(title, Text("D = 0: One Real Solution", color=GOLD_ACCENT, font_size=48).to_edge(UP)),
            FadeOut(parabola_curve_two_roots, dot1, dot2)
        )
        
        # y = (x-2)^2 = x^2 - 4x + 4 (Discriminant = 0)
        parabola_curve_one_root = plane.get_graph(
            lambda x: (x-2)**2,
            x_range=[-0.5, 4.5],
            color=BLUE_ACCENT
        )
        dot_single = Dot(plane.c2p(2, 0), color=GOLD_ACCENT, radius=0.1)
        
        self.play(
            Create(parabola_curve_one_root),
            FadeIn(dot_single)
        )
        self.wait(2)
        
        # --- Beat 5: Case 3: D < 0 (No Real Solutions) ---
        self.play(
            Transform(title, Text("D < 0: No Real Solutions", color=GOLD_ACCENT, font_size=48).to_edge(UP)),
            FadeOut(parabola_curve_one_root, dot_single)
        )
        
        # y = x^2 - 4x + 5 = (x-2)^2 + 1 (Discriminant = -4 < 0)
        parabola_curve_no_roots = plane.get_graph(
            lambda x: (x-2)**2 + 1,
            x_range=[-0.5, 4.5],
            color=BLUE_ACCENT
        )
        
        self.play(
            Create(parabola_curve_no_roots)
        )
        
        no_intersection_arrow = Arrow(
            start=plane.c2p(2, 1.5),
            end=plane.c2p(2, 0.5),
            buff=0,
            color=GOLD_ACCENT
        )
        no_intersection_text = Text("Does not cross X-axis", font_size=30, color=TEXT_COLOR).next_to(no_intersection_arrow, DOWN)
        
        self.play(
            FadeIn(no_intersection_arrow, shift=DOWN),
            Write(no_intersection_text)
        )
        self.wait(2.5) # A bit longer for explanation
        
        self.play(
            FadeOut(parabola_curve_no_roots, no_intersection_arrow, no_intersection_text, plane, title)
        )

        # --- Recap Card ---
        recap_title = Text("Recap: The Discriminant", color=GOLD_ACCENT, font_size=48).to_edge(UP)
        
        recap_d_gt_0 = Text("D > 0: Two Real Solutions", color=TEXT_COLOR).scale(0.9)
        recap_d_eq_0 = Text("D = 0: One Real Solution", color=TEXT_COLOR).scale(0.9)
        recap_d_lt_0 = Text("D < 0: No Real Solutions", color=TEXT_COLOR).scale(0.9)
        
        recap_group = VGroup(
            recap_d_gt_0,
            recap_d_eq_0,
            recap_d_lt_0
        ).arrange(DOWN, buff=0.7).center()
        
        self.play(
            FadeIn(recap_title, shift=UP),
            LaggedStart(*[Write(text, run_time=1) for text in recap_group], lag_ratio=0.5)
        )
        self.wait(3)
        self.play(FadeOut(recap_title, recap_group))