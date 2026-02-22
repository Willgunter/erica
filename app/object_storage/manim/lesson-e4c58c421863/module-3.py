from manim import *

class DiscriminantParabola(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#1a1a1a" # Dark background
        BLUE_ACCENT = "#5E9BE6" # A vibrant blue
        GOLD_ACCENT = "#FFD700" # Gold
        GREY_TEXT = "#CCCCCC"
        TITLE_FONT_SIZE = 72
        SUBTITLE_FONT_SIZE = 48
        NORMAL_TEXT_SIZE = 36
        FORMULA_TEXT_SIZE = 48
        SMALL_TEXT_SIZE = 28

        # --- Helper for custom quadratic formula & discriminant (no MathTex) ---
        def create_discriminant_text(color=GOLD_ACCENT, font_size=FORMULA_TEXT_SIZE):
            b_text = Text("b", color=color, font_size=font_size)
            exponent_2 = Text("2", color=color, font_size=font_size * 0.6).next_to(b_text, UP + RIGHT * 0.2, buff=0.05)
            minus_4ac = Text("- 4ac", color=color, font_size=font_size).next_to(b_text, RIGHT, buff=0.1)
            discriminant_group = VGroup(b_text, exponent_2, minus_4ac)
            discriminant_group.arrange(RIGHT, center=False, buff=0.1).shift(LEFT * 0.5) # Manual adjustment
            return discriminant_group

        def create_quadratic_formula_text():
            x_eq = Text("x =", font_size=FORMULA_TEXT_SIZE, color=GREY_TEXT)
            
            minus_b = Text("-b", font_size=FORMULA_TEXT_SIZE, color=BLUE_ACCENT)
            plus_minus = Text(" ± ", font_size=FORMULA_TEXT_SIZE, color=GREY_TEXT)
            sqrt_start = Text("sqrt(", font_size=FORMULA_TEXT_SIZE, color=GREY_TEXT)
            b_sq = Text("b", font_size=FORMULA_TEXT_SIZE, color=GOLD_ACCENT)
            exp_2 = Text("2", font_size=FORMULA_TEXT_SIZE * 0.6).next_to(b_sq, UP + RIGHT * 0.2, buff=0.05)
            minus_4ac_part = Text(" - 4ac", font_size=FORMULA_TEXT_SIZE, color=GOLD_ACCENT)
            sqrt_end = Text(")", font_size=FORMULA_TEXT_SIZE, color=GREY_TEXT)

            discriminant_part = VGroup(b_sq, exp_2, minus_4ac_part).arrange(RIGHT, buff=0.05, center=False)
            
            numerator_parts = VGroup(minus_b, plus_minus, sqrt_start, discriminant_part, sqrt_end).arrange(RIGHT, buff=0.05)
            
            denominator_text = Text("2a", font_size=FORMULA_TEXT_SIZE, color=BLUE_ACCENT)
            
            # Create a fraction bar
            fraction_bar = Line(LEFT, RIGHT, color=GREY_TEXT).set_length(numerator_parts.width * 1.1)

            # Position elements
            numerator_parts.move_to(ORIGIN)
            denominator_text.next_to(numerator_parts, DOWN, buff=0.8)
            fraction_bar.move_to(VGroup(numerator_parts, denominator_text).get_center_and_shift(DOWN*0.1)) # Adjust bar position

            # Group for final formula
            formula_components = VGroup(numerator_parts, fraction_bar, denominator_text)
            
            # Position x =
            x_eq.next_to(formula_components, LEFT, buff=0.2)
            
            full_formula = VGroup(x_eq, formula_components).arrange(RIGHT, buff=0.1)
            return full_formula.scale(0.8) # Scale down slightly for better fit

        # --- Beat 1: Hook - Intercepts Mystery ---
        title = Text("Discriminant & Parabola Intercepts", font_size=TITLE_FONT_SIZE, color=GOLD_ACCENT)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": GREY_B, "include_numbers": False},
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.6}
        ).add_coordinates()
        
        self.play(Create(plane))

        # Parabola 1: y = x^2 - 4 (2 intercepts)
        parabola1 = plane.get_graph(lambda x: x**2 - 4, color=BLUE_ACCENT, x_range=[-3, 3])
        intercept_points1 = VGroup(
            Dot(plane.coords_to_point(-2, 0), color=GOLD_ACCENT),
            Dot(plane.coords_to_point(2, 0), color=GOLD_ACCENT)
        )
        
        question1 = Text("How many times does this graph cross the x-axis?", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT).to_edge(UP)
        
        self.play(Create(parabola1), Write(question1))
        self.play(FadeIn(intercept_points1, scale=0.8))
        self.wait(1.5)

        # Parabola 2: y = x^2 (1 intercept)
        parabola2 = plane.get_graph(lambda x: x**2, color=BLUE_ACCENT, x_range=[-3, 3])
        intercept_points2 = Dot(plane.coords_to_point(0, 0), color=GOLD_ACCENT)
        
        self.play(
            ReplacementTransform(parabola1, parabola2),
            Transform(intercept_points1, intercept_points2)
        )
        self.wait(1.5)

        # Parabola 3: y = x^2 + 4 (0 intercepts)
        parabola3 = plane.get_graph(lambda x: x**2 + 4, color=BLUE_ACCENT, x_range=[-3, 3])
        
        self.play(
            ReplacementTransform(parabola2, parabola3),
            FadeOut(intercept_points1) # points were transformed to intercept_points2, then parabola3 has no intercepts
        )
        mystery_text = Text("The number of intercepts changes...", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT).to_edge(UP)
        mystery_why = Text("...but why?", font_size=SUBTITLE_FONT_SIZE, color=GOLD_ACCENT).next_to(mystery_text, DOWN)
        self.play(FadeTransform(question1, mystery_text))
        self.play(Write(mystery_why))
        self.wait(2)
        self.play(FadeOut(parabola3, mystery_text, mystery_why))

        # --- Beat 2: The Core Idea - Shifting Parabolas ---
        subtitle_core = Text("It's all about how high or low the parabola 'sits'!", font_size=SUBTITLE_FONT_SIZE, color=GREY_TEXT).to_edge(UP)
        self.play(FadeIn(subtitle_core))

        parabola_base = plane.get_graph(lambda x: x**2, color=BLUE_ACCENT, x_range=[-3, 3])
        self.play(Create(parabola_base))

        # Animate shifting up and down
        parabola_shifted_down = plane.get_graph(lambda x: x**2 - 2, color=BLUE_ACCENT, x_range=[-3, 3])
        parabola_shifted_up = plane.get_graph(lambda x: x**2 + 2, color=BLUE_ACCENT, x_range=[-3, 3])

        text_2_intercepts = Text("2 Intercepts", font_size=SMALL_TEXT_SIZE, color=GOLD_ACCENT).next_to(parabola_shifted_down, DOWN, buff=0.5)
        text_1_intercept = Text("1 Intercept", font_size=SMALL_TEXT_SIZE, color=GOLD_ACCENT).next_to(parabola_base, DOWN, buff=0.5)
        text_0_intercepts = Text("0 Intercepts", font_size=SMALL_TEXT_SIZE, color=GOLD_ACCENT).next_to(parabola_shifted_up, DOWN, buff=0.5)

        intercepts_down = VGroup(Dot(plane.coords_to_point(-1.41, 0), color=GOLD_ACCENT), Dot(plane.coords_to_point(1.41, 0), color=GOLD_ACCENT))
        intercept_origin = Dot(plane.coords_to_point(0,0), color=GOLD_ACCENT)

        self.play(
            ReplacementTransform(parabola_base, parabola_shifted_down),
            FadeIn(intercepts_down, scale=0.8),
            Write(text_2_intercepts)
        )
        self.wait(1)

        self.play(
            ReplacementTransform(parabola_shifted_down, parabola_base),
            ReplacementTransform(intercepts_down, intercept_origin),
            FadeTransform(text_2_intercepts, text_1_intercept)
        )
        self.wait(1)

        self.play(
            ReplacementTransform(parabola_base, parabola_shifted_up),
            FadeOut(intercept_origin),
            FadeTransform(text_1_intercept, text_0_intercepts)
        )
        self.wait(1.5)

        self.play(FadeOut(parabola_shifted_up, text_0_intercepts, subtitle_core, plane))

        # --- Beat 3: Introducing the Discriminant ---
        subtitle_discriminant = Text("The Quadratic Formula holds the key!", font_size=SUBTITLE_FONT_SIZE, color=GREY_TEXT).to_edge(UP)
        self.play(Write(subtitle_discriminant))

        quadratic_formula = create_quadratic_formula_text().move_to(ORIGIN)
        self.play(Write(quadratic_formula))
        self.wait(1)

        # Highlight the discriminant part
        disc_highlight = SurroundingRectangle(quadratic_formula[1][3], color=GOLD_ACCENT, fill_opacity=0.2, buff=0.1)
        self.play(Create(disc_highlight))

        discriminant_label = Text("This special part...", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT).next_to(quadratic_formula, DOWN, buff=1)
        self.play(Write(discriminant_label))
        self.wait(0.5)

        discriminant_name = Text("is called the DISCRIMINANT!", font_size=SUBTITLE_FONT_SIZE, color=GOLD_ACCENT).next_to(discriminant_label, DOWN, buff=0.3)
        self.play(Write(discriminant_name))
        self.wait(1.5)

        # Intuition about the square root
        sqrt_intuition = Text("It's inside a square root...", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT).to_edge(DOWN)
        self.play(Write(sqrt_intuition))
        self.wait(1)

        self.play(FadeOut(quadratic_formula, disc_highlight, discriminant_label, discriminant_name, sqrt_intuition, subtitle_discriminant))

        # --- Beat 4: Discriminant Cases (Visuals to Formula) ---
        subtitle_cases = Text("The Discriminant (b² - 4ac) tells the story:", font_size=SUBTITLE_FONT_SIZE, color=GREY_TEXT).to_edge(UP)
        self.play(Write(subtitle_cases))

        # Setup 3 sub-planes
        plane_left = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4, y_length=4,
            axis_config={"color": GREY_B, "include_numbers": False},
            background_line_style={"stroke_color": GREY_D, "stroke_width": 0.5, "stroke_opacity": 0.3}
        ).shift(LEFT * 4).scale(0.8)
        plane_center = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4, y_length=4,
            axis_config={"color": GREY_B, "include_numbers": False},
            background_line_style={"stroke_color": GREY_D, "stroke_width": 0.5, "stroke_opacity": 0.3}
        ).scale(0.8)
        plane_right = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4, y_length=4,
            axis_config={"color": GREY_B, "include_numbers": False},
            background_line_style={"stroke_color": GREY_D, "stroke_width": 0.5, "stroke_opacity": 0.3}
        ).shift(RIGHT * 4).scale(0.8)

        self.play(Create(VGroup(plane_left, plane_center, plane_right)))

        # Case 1: b^2 - 4ac > 0 (2 intercepts)
        parabola_case1 = plane_left.get_graph(lambda x: x**2 - 2, color=BLUE_ACCENT, x_range=[-2, 2])
        intercepts_case1 = VGroup(Dot(plane_left.coords_to_point(-1.41, 0), color=GOLD_ACCENT), Dot(plane_left.coords_to_point(1.41, 0), color=GOLD_ACCENT))
        discriminant_pos_text = create_discriminant_text().set_color(GOLD_ACCENT).next_to(plane_left, DOWN, buff=0.5).scale(0.7)
        greater_than_zero = Text("> 0", font_size=FORMULA_TEXT_SIZE * 0.7, color=GREY_TEXT).next_to(discriminant_pos_text, RIGHT, buff=0.1)
        two_intercepts_text = Text("2 Intercepts", font_size=SMALL_TEXT_SIZE, color=GOLD_ACCENT).next_to(discriminant_pos_text, DOWN, buff=0.2)
        
        self.play(Create(parabola_case1), FadeIn(intercepts_case1))
        self.play(Write(discriminant_pos_text), Write(greater_than_zero))
        self.play(Write(two_intercepts_text))
        self.wait(1)

        # Case 2: b^2 - 4ac = 0 (1 intercept)
        parabola_case2 = plane_center.get_graph(lambda x: x**2, color=BLUE_ACCENT, x_range=[-2, 2])
        intercept_case2 = Dot(plane_center.coords_to_point(0, 0), color=GOLD_ACCENT)
        discriminant_zero_text = create_discriminant_text().set_color(GOLD_ACCENT).next_to(plane_center, DOWN, buff=0.5).scale(0.7)
        equal_zero = Text("= 0", font_size=FORMULA_TEXT_SIZE * 0.7, color=GREY_TEXT).next_to(discriminant_zero_text, RIGHT, buff=0.1)
        one_intercept_text = Text("1 Intercept", font_size=SMALL_TEXT_SIZE, color=GOLD_ACCENT).next_to(discriminant_zero_text, DOWN, buff=0.2)

        self.play(Create(parabola_case2), FadeIn(intercept_case2))
        self.play(Write(discriminant_zero_text), Write(equal_zero))
        self.play(Write(one_intercept_text))
        self.wait(1)

        # Case 3: b^2 - 4ac < 0 (0 intercepts)
        parabola_case3 = plane_right.get_graph(lambda x: x**2 + 2, color=BLUE_ACCENT, x_range=[-2, 2])
        discriminant_neg_text = create_discriminant_text().set_color(GOLD_ACCENT).next_to(plane_right, DOWN, buff=0.5).scale(0.7)
        less_than_zero = Text("< 0", font_size=FORMULA_TEXT_SIZE * 0.7, color=GREY_TEXT).next_to(discriminant_neg_text, RIGHT, buff=0.1)
        zero_intercepts_text = Text("0 Intercepts", font_size=SMALL_TEXT_SIZE, color=GOLD_ACCENT).next_to(discriminant_neg_text, DOWN, buff=0.2)

        self.play(Create(parabola_case3))
        self.play(Write(discriminant_neg_text), Write(less_than_zero))
        self.play(Write(zero_intercepts_text))
        self.wait(2)

        self.play(FadeOut(VGroup(
            plane_left, plane_center, plane_right,
            parabola_case1, intercepts_case1, discriminant_pos_text, greater_than_zero, two_intercepts_text,
            parabola_case2, intercept_case2, discriminant_zero_text, equal_zero, one_intercept_text,
            parabola_case3, discriminant_neg_text, less_than_zero, zero_intercepts_text, subtitle_cases
        )))

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: The Discriminant", font_size=TITLE_FONT_SIZE, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(recap_title))

        # Recreate discriminant for the recap
        discriminant_recap = create_discriminant_text(color=GOLD_ACCENT, font_size=SUBTITLE_FONT_SIZE)
        
        point1 = Text("1.  The Discriminant is: ", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT)
        point1_formula = VGroup(point1, discriminant_recap).arrange(RIGHT, buff=0.1).to_edge(LEFT).shift(UP*1.5)

        point2 = Text("2.  If it's POSITIVE ( > 0 ) :  TWO real intercepts", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT).next_to(point1_formula, DOWN, buff=0.5).align_to(point1, LEFT)
        point3 = Text("3.  If it's ZERO ( = 0 )   :  ONE real intercept", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT).next_to(point2, DOWN, buff=0.3).align_to(point1, LEFT)
        point4 = Text("4.  If it's NEGATIVE ( < 0 ) : ZERO real intercepts", font_size=NORMAL_TEXT_SIZE, color=GREY_TEXT).next_to(point3, DOWN, buff=0.3).align_to(point1, LEFT)

        recap_card = VGroup(point1_formula, point2, point3, point4)

        self.play(LaggedStart(
            FadeIn(point1_formula, shift=UP),
            FadeIn(point2, shift=UP),
            FadeIn(point3, shift=UP),
            FadeIn(point4, shift=UP),
            lag_ratio=0.5
        ))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_card)))

        # End Scene
        thanks = Text("Thanks for watching!", font_size=TITLE_FONT_SIZE, color=GOLD_ACCENT)
        self.play(Write(thanks))
        self.wait(1)
        self.play(FadeOut(thanks))