from manim import *

class QuadraticEquationsAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_MAIN = BLUE_E
        GOLD_ACCENT = GOLD_E
        TEXT_COLOR = WHITE

        # Helper function to create the ax^2 + bx + c = 0 expression without Tex
        def create_quadratic_text_expression(include_equals_zero=True, color=TEXT_COLOR):
            a_label = Text("a", color=color)
            x_label1 = Text("x", color=color).next_to(a_label, RIGHT, buff=0.1)
            # Manual positioning for the superscript '2'
            power_2 = Text("2", color=color, font_size=a_label.font_size * 0.6)
            power_2.align_to(x_label1, UP) # Align top edge with 'x'
            power_2.shift(RIGHT * 0.08) # Small shift to the right to place it over 'x'

            plus1_label = Text("+", color=color).next_to(power_2, RIGHT, buff=0.15)
            b_label = Text("b", color=color).next_to(plus1_label, RIGHT, buff=0.15)
            x_label2 = Text("x", color=color).next_to(b_label, RIGHT, buff=0.1)

            plus2_label = Text("+", color=color).next_to(x_label2, RIGHT, buff=0.15)
            c_label = Text("c", color=color).next_to(plus2_label, RIGHT, buff=0.15)

            expression_parts = [a_label, x_label1, power_2, plus1_label, b_label, x_label2, plus2_label, c_label]
            
            if include_equals_zero:
                equals_label = Text("=", color=color).next_to(c_label, RIGHT, buff=0.15)
                zero_label = Text("0", color=color).next_to(equals_label, RIGHT, buff=0.15)
                expression_parts.extend([equals_label, zero_label])
            
            return VGroup(*expression_parts)

        # --- Beat 1: The Parabola's Shape (Visual Hook) ---
        title = Text("Understanding Quadratic Equations", color=GOLD_ACCENT).to_corner(UL).scale(0.8)
        self.play(FadeIn(title, shift=UP), run_time=0.8)

        # Setup NumberPlane and Axes
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": BLUE_MAIN},
            background_line_style={"stroke_color": BLUE_A, "stroke_width": 1, "stroke_opacity": 0.5}
        ).add_coordinates(font_size=24, color=BLUE_MAIN)
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": BLUE_MAIN},
        ).add_coordinates(font_size=24, color=BLUE_MAIN)

        self.play(Create(axes), Create(plane), run_time=1.2)

        # Define a simple parabola function
        def parabola_func(x):
            return 0.5 * x**2 - 2

        parabola = axes.plot(parabola_func, color=GOLD_ACCENT)
        parabola_label = Text("The Parabola Shape", color=TEXT_COLOR, font_size=32).next_to(parabola, UP, buff=0.5).shift(LEFT * 2)

        self.play(
            Create(parabola),
            FadeIn(parabola_label, shift=UP),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 2: Roots/Solutions ---
        solutions_title = Text("Solutions are X-Intercepts", color=GOLD_ACCENT, font_size=32).to_corner(UR)
        self.play(Transform(parabola_label, solutions_title), run_time=0.8)

        # Find roots (where y=0) for y = 0.5x^2 - 2  => x = -2, 2
        root1 = Dot(axes.c2p(-2, 0), color=BLUE_MAIN)
        root2 = Dot(axes.c2p(2, 0), color=BLUE_MAIN)

        arrow1 = Arrow(start=root1.get_center() + DOWN * 0.5, end=root1.get_center(), color=BLUE_MAIN)
        arrow2 = Arrow(start=root2.get_center() + DOWN * 0.5, end=root2.get_center(), color=BLUE_MAIN)
        
        root_explanation = Text("These are the 'roots'", color=TEXT_COLOR, font_size=28).next_to(root2, RIGHT, buff=0.5).shift(UP*0.5)

        self.play(
            FadeIn(root1, scale=0.5),
            FadeIn(root2, scale=0.5),
            Create(arrow1),
            Create(arrow2),
            FadeIn(root_explanation, shift=UP),
            run_time=1.8
        )
        self.wait(0.5)

        # --- Beat 3: General Form Intuition (Coefficients a, c) ---
        
        # Fade out root specific elements
        self.play(FadeOut(root1, root2, arrow1, arrow2, root_explanation), run_time=0.8)

        # Coefficient 'a'
        coeff_title_a = Text("Coefficient 'a'", color=GOLD_ACCENT, font_size=32).to_corner(UR)
        self.play(Transform(parabola_label, coeff_title_a), run_time=0.8)

        parabola_original = parabola.copy()
        parabola_up_wide = axes.plot(lambda x: 0.2 * x**2 - 2, color=GOLD_ACCENT) # Wider
        parabola_down = axes.plot(lambda x: -0.5 * x**2 + 2, color=BLUE_MAIN) # Opens down

        text_a_positive = Text("a > 0 (opens up)", color=GOLD_ACCENT, font_size=28).next_to(coeff_title_a, DOWN, buff=0.2)
        text_a_negative = Text("a < 0 (opens down)", color=BLUE_MAIN, font_size=28).next_to(coeff_title_a, DOWN, buff=0.2)

        self.play(Transform(parabola, parabola_up_wide), FadeIn(text_a_positive, shift=LEFT), run_time=1.2)
        self.wait(0.3)
        self.play(Transform(parabola, parabola_down), ReplacementTransform(text_a_positive, text_a_negative), run_time=1.2)
        self.wait(0.3)

        # Coefficient 'c'
        self.play(Transform(parabola, parabola_original), FadeOut(text_a_negative), run_time=0.8)

        coeff_title_c = Text("Constant 'c'", color=GOLD_ACCENT, font_size=32).to_corner(UR)
        self.play(Transform(parabola_label, coeff_title_c), run_time=0.8)

        parabola_shifted_up = axes.plot(lambda x: 0.5 * x**2 + 1, color=BLUE_MAIN)
        parabola_shifted_down = axes.plot(lambda x: 0.5 * x**2 - 3, color=GOLD_ACCENT)

        text_c_up = Text("c > 0 (shifts up)", color=BLUE_MAIN, font_size=28).next_to(coeff_title_c, DOWN, buff=0.2)
        text_c_down = Text("c < 0 (shifts down)", color=GOLD_ACCENT, font_size=28).next_to(coeff_title_c, DOWN, buff=0.2)

        self.play(Transform(parabola, parabola_shifted_up), FadeIn(text_c_up, shift=LEFT), run_time=1.2)
        self.wait(0.3)
        self.play(Transform(parabola, parabola_shifted_down), ReplacementTransform(text_c_up, text_c_down), run_time=1.2)
        self.wait(0.5)

        self.play(FadeOut(text_c_down), run_time=0.5)

        # --- Beat 4: Formal Notation & Solving ---
        general_form_title = Text("The General Form", color=GOLD_ACCENT, font_size=32).to_corner(UR)
        self.play(Transform(parabola_label, general_form_title), run_time=0.8)

        # Revert parabola to a standard one
        parabola_final = axes.plot(parabola_func, color=GOLD_ACCENT)
        self.play(Transform(parabola, parabola_final), run_time=1)

        # Create the quadratic equation text using the helper
        quadratic_equation_text = create_quadratic_text_expression(include_equals_zero=True, color=TEXT_COLOR)
        quadratic_equation_text.next_to(plane, DOWN, buff=0.8).scale(1.1)
        
        solving_text = Text("Find 'x' when y = 0", color=BLUE_MAIN, font_size=32).next_to(quadratic_equation_text, DOWN, buff=0.5)

        self.play(
            FadeIn(quadratic_equation_text, shift=UP),
            FadeIn(solving_text, shift=UP),
            run_time=1.8
        )
        self.wait(1.5)

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(plane, axes, parabola, quadratic_equation_text, solving_text, parabola_label),
            FadeOut(title),
            run_time=1.2
        )

        recap_title = Text("Quadratic Equations: Recap", color=GOLD_ACCENT).to_edge(UP, buff=1)
        
        point1 = Text("• Feature an x^2 term.", color=TEXT_COLOR, font_size=36).next_to(recap_title, DOWN, buff=0.7).align_to(recap_title, LEFT)
        point2 = Text("• Graph is a Parabola.", color=TEXT_COLOR, font_size=36).next_to(point1, DOWN, buff=0.4).align_to(point1, LEFT)
        point3 = Text("• Solutions = X-intercepts.", color=TEXT_COLOR, font_size=36).next_to(point2, DOWN, buff=0.4).align_to(point2, LEFT)
        
        # Create the general form text for the recap
        point4_expr = create_quadratic_text_expression(include_equals_zero=True, color=TEXT_COLOR).scale(0.8)
        point4_prefix = Text("• General form: ", color=TEXT_COLOR, font_size=36)
        point4_group = VGroup(point4_prefix, point4_expr).arrange(RIGHT, buff=0.1).next_to(point3, DOWN, buff=0.4).align_to(point3, LEFT)

        recap_points = VGroup(recap_title, point1, point2, point3, point4_group)
        recap_points.center() # Center the entire group

        self.play(LaggedStart(
            FadeIn(recap_title, shift=UP),
            FadeIn(point1, shift=LEFT),
            FadeIn(point2, shift=LEFT),
            FadeIn(point3, shift=LEFT),
            FadeIn(point4_group, shift=LEFT),
            lag_ratio=0.2
        ), run_time=3.5)
        self.wait(2)