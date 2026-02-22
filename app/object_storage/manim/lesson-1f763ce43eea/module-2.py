from manim import *

class ApplyingQuadraticFormula(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        blue_color = BLUE_D
        gold_color = GOLD

        # --- Helper for creating the Quadratic Formula Mobject without Tex ---
        # x = (-b ± sqrt(b^2 - 4ac)) / (2a)
        def create_quadratic_formula_mobject(scale_factor=1.0):
            x_eq = Text("x =", color=gold_color, font_size=48 * scale_factor)
            
            # Numerator parts
            minus_b = Text("-b", color=blue_color, font_size=48 * scale_factor)
            plus_minus = Text("±", color=gold_color, font_size=48 * scale_factor)
            
            b_squared = Text("b^2", color=blue_color, font_size=48 * scale_factor)
            minus_4ac = Text("- 4ac", color=gold_color, font_size=48 * scale_factor)
            
            discriminant_group = VGroup(b_squared, minus_4ac).arrange(RIGHT, buff=0.1)
            
            # Custom "square root" visual: a line over the expression
            sqrt_line_width = discriminant_group.width + 0.2 * scale_factor
            sqrt_line = Line(LEFT * sqrt_line_width / 2, RIGHT * sqrt_line_width / 2, 
                             color=gold_color, stroke_width=3 * scale_factor)
            sqrt_line.move_to(discriminant_group.get_center() + UP * 0.45 * scale_factor)

            # Combine numerator terms
            numerator_vgroup = VGroup(minus_b, plus_minus, discriminant_group, sqrt_line)
            numerator_vgroup.arrange(RIGHT, buff=0.1) 
            # Re-position sqrt_line after final numerator arrangement
            sqrt_line.move_to(discriminant_group.get_center() + UP * 0.45 * scale_factor)
            
            # Denominator
            two_a = Text("2a", color=blue_color, font_size=48 * scale_factor)

            # Fraction line
            fraction_line_width = max(numerator_vgroup.width, two_a.width) * 1.1
            fraction_line = Line(LEFT * fraction_line_width / 2, RIGHT * fraction_line_width / 2, 
                                 color=gold_color, stroke_width=4 * scale_factor)

            # Assemble everything relative to the fraction line
            numerator_vgroup.next_to(fraction_line, UP, buff=0.2 * scale_factor)
            two_a.next_to(fraction_line, DOWN, buff=0.2 * scale_factor)
            
            rhs_formula = VGroup(numerator_vgroup, two_a, fraction_line)
            rhs_formula.arrange(DOWN, buff=0.1 * scale_factor, center=True) # This arranges vertically around fraction line
            
            # Combine x = and the RHS
            full_formula = VGroup(x_eq, rhs_formula).arrange(RIGHT, buff=0.2 * scale_factor)

            return full_formula, x_eq, minus_b, plus_minus, discriminant_group, sqrt_line, two_a, fraction_line


        # --- Beat 1: Visual Hook & Problem Introduction ---
        title = Text("Applying the Quadratic Formula", color=gold_color, font_size=60).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Set up Axes and a simple parabola
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-8, 8, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": BLUE_D},
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.4}
        ).shift(DOWN * 0.5)
        
        # Parabola: y = x^2 - x - 6. Roots at x=-2, x=3
        def parabola_func1(x):
            return x**2 - x - 6
        
        parabola1 = FunctionGraph(
            parabola_func1, 
            x_range=[-4, 4], 
            color=gold_color, 
            stroke_width=5
        )

        roots1_x = [-2, 3]
        roots1_dots = VGroup(*[Dot(plane.coords_to_point(x, 0), color=blue_color, radius=0.12) for x in roots1_x])

        question_text = Text("Where does it cross?", color=gold_color, font_size=40).next_to(parabola1, UP, buff=0.5)

        self.play(Create(plane), run_time=1.5)
        self.play(Create(parabola1))
        self.play(FadeIn(roots1_dots), Write(question_text))
        self.wait(1.5)
        self.play(FadeOut(question_text), FadeOut(roots1_dots))
        self.wait(0.5)

        # --- Beat 2: The General Form & Coefficients ---
        general_form_text = Text("ax² + bx + c = 0", color=gold_color, font_size=60)
        general_form_text.move_to(UP*2.5)

        example_eq_text = Text("2x² + 5x - 3 = 0", color=blue_color, font_size=60)
        example_eq_text.move_to(DOWN*0.5)

        a_val = Text("a = 2", color=gold_color, font_size=40).shift(LEFT * 4 + DOWN * 2.5)
        b_val = Text("b = 5", color=gold_color, font_size=40).shift(DOWN * 2.5)
        c_val = Text("c = -3", color=gold_color, font_size=40).shift(RIGHT * 4 + DOWN * 2.5)
        
        coefficients_group = VGroup(a_val, b_val, c_val).arrange(RIGHT, buff=1.5).next_to(example_eq_text, DOWN, buff=1)

        self.play(
            ReplacementTransform(parabola1, general_form_text),
            FadeOut(plane)
        )
        self.wait(0.5)
        self.play(Write(example_eq_text))
        self.wait(0.5)
        self.play(
            LaggedStart(
                Write(a_val),
                Write(b_val),
                Write(c_val),
                lag_ratio=0.5
            )
        )
        self.wait(1.5)

        # --- Beat 3: Introducing the Quadratic Formula (Visually Assembled) ---
        formula_parts = create_quadratic_formula_mobject(scale_factor=1.0)
        full_formula_mobject = formula_parts[0] # The VGroup containing the entire formula
        x_eq, minus_b, plus_minus, discriminant_group, sqrt_line, two_a, fraction_line = formula_parts[1:]
        
        # Position the formula to be central
        full_formula_mobject.move_to(ORIGIN)
        
        self.play(
            FadeOut(general_form_text),
            FadeOut(example_eq_text),
            FadeOut(coefficients_group),
            FadeOut(title) # Fade out the title to make room for the formula
        )
        
        # Re-introduce title, smaller, to top left
        small_title = Text("The Quadratic Formula", color=gold_color, font_size=40).to_edge(UP).to_edge(LEFT)
        self.play(FadeIn(small_title))

        # Animation of building the formula
        self.play(Write(x_eq))
        self.play(FadeIn(fraction_line))
        self.play(FadeIn(minus_b))
        self.play(FadeIn(plus_minus))
        self.play(FadeIn(discriminant_group))
        self.play(FadeIn(sqrt_line))
        self.play(FadeIn(two_a))
        self.wait(2)
        self.wait(1.5)

        # --- Beat 4: Applying the Formula (Example Calculation) ---
        self.play(full_formula_mobject.animate.scale(0.7).to_edge(UP).to_edge(LEFT))
        self.wait(0.5)

        # Re-display problem and coefficients
        example_eq_text_small = Text("2x² + 5x - 3 = 0", color=blue_color, font_size=40).next_to(full_formula_mobject, DOWN, buff=0.5, aligned_edge=LEFT)
        coefficients_group_small = VGroup(
            Text("a = 2", color=gold_color, font_size=32),
            Text("b = 5", color=gold_color, font_size=32),
            Text("c = -3", color=gold_color, font_size=32)
        ).arrange(RIGHT, buff=0.5).next_to(example_eq_text_small, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(FadeIn(example_eq_text_small), FadeIn(coefficients_group_small))
        self.wait(0.5)

        # Substitute values
        substitution_text = Text(
            "x = (-5 ± sqrt(5^2 - 4(2)(-3))) / (2(2))", 
            color=gold_color, font_size=40
        ).next_to(coefficients_group_small, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(substitution_text))
        self.wait(1)

        # Simplify discriminant
        discriminant_calc = Text(
            "5^2 - 4(2)(-3) = 25 - (-24) = 25 + 24 = 49", 
            color=blue_color, font_size=40
        ).next_to(substitution_text, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(discriminant_calc))
        self.wait(1)

        # Simplify further
        simplified_text = Text(
            "x = (-5 ± sqrt(49)) / 4", 
            color=gold_color, font_size=40
        ).next_to(discriminant_calc, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(simplified_text))
        self.wait(1)
        
        simplified_text2 = Text(
            "x = (-5 ± 7) / 4", 
            color=blue_color, font_size=40
        ).next_to(simplified_text, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(simplified_text2))
        self.wait(1)

        # Find x1 and x2
        x1_text = Text("x1 = (-5 + 7) / 4 = 2 / 4 = 0.5", color=gold_color, font_size=40).next_to(simplified_text2, DOWN, buff=0.5, aligned_edge=LEFT)
        x2_text = Text("x2 = (-5 - 7) / 4 = -12 / 4 = -3", color=gold_color, font_size=40).next_to(x1_text, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(x1_text))
        self.wait(0.5)
        self.play(Write(x2_text))
        self.wait(1.5)

        # Visual confirmation on graph (new parabola for the example)
        self.play(FadeOut(small_title), FadeOut(full_formula_mobject), FadeOut(example_eq_text_small),
                  FadeOut(coefficients_group_small), FadeOut(substitution_text), FadeOut(discriminant_calc),
                  FadeOut(simplified_text), FadeOut(simplified_text2), FadeOut(x1_text), FadeOut(x2_text))
        
        plane2 = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-8, 8, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": BLUE_D},
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.4}
        ).move_to(ORIGIN)

        def parabola_func2(x):
            return 2*x**2 + 5*x - 3
        
        parabola2 = FunctionGraph(
            parabola_func2, 
            x_range=[-3.5, 1], 
            color=gold_color, 
            stroke_width=5
        )

        roots2_x = [-3, 0.5]
        roots2_dots = VGroup(*[Dot(plane2.coords_to_point(x, 0), color=blue_color, radius=0.12) for x in roots2_x])

        self.play(Create(plane2))
        self.play(Create(parabola2))
        self.play(FadeIn(roots2_dots))
        self.wait(2)

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(plane2), 
            FadeOut(parabola2), 
            FadeOut(roots2_dots)
        )
        
        recap_title = Text("Recap:", color=gold_color, font_size=60).to_edge(UP)
        
        recap_bullets = VGroup(
            Text("1. Identify a, b, c from ax² + bx + c = 0", color=blue_color, font_size=40),
            Text("2. Substitute into the quadratic formula:", color=blue_color, font_size=40),
            Text("3. Simplify to find the roots (x-intercepts)", color=blue_color, font_size=40)
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).next_to(recap_title, DOWN, buff=1)

        # Re-create the formula for the recap card, possibly larger or more prominent
        recap_formula_components = create_quadratic_formula_mobject(scale_factor=0.9)
        recap_formula = recap_formula_components[0]
        recap_formula.next_to(recap_bullets[1], DOWN, buff=0.5, aligned_edge=LEFT)
        recap_formula.shift(RIGHT * 0.5) # Adjust position to align well

        self.play(Write(recap_title))
        self.play(LaggedStart(*[Write(bullet) for bullet in recap_bullets], lag_ratio=0.7))
        self.play(FadeIn(recap_formula))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_bullets, recap_formula)))
        self.wait(1)