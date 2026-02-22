from manim import *

class ParabolaInterceptsDiscriminant(Scene):
    def construct(self):
        # --- Configuration ---
        _PARABOLA_COLOR = BLUE
        _HIGHLIGHT_COLOR = GOLD
        _TEXT_COLOR = WHITE
        _AXES_COLOR = GRAY_B
        _DISCRIMINANT_COLOR = GOLD
        self.camera.background_color = BLACK

        # --- Beat 1: Visual Hook & Introduction ---
        # 1. NumberPlane and Axes
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": _AXES_COLOR, "stroke_width": 2},
            background_line_style={"stroke_color": GRAY_D, "stroke_width": 1, "stroke_opacity": 0.6}
        ).add_coordinates()
        axes = plane.get_axes()

        self.play(Create(plane, run_time=1.5))

        # 2. Initial Parabola (y = x^2 - 4)
        def func_parabola1(x):
            return x**2 - 4
        parabola1 = plane.get_graph(func_parabola1, color=_PARABOLA_COLOR, x_range=[-3, 3])
        
        # Get intercepts for parabola1
        intercept1_left_coords = plane.c2p(-2, 0)
        intercept1_right_coords = plane.c2p(2, 0)
        
        dot1_left = Dot(intercept1_left_coords, color=_HIGHLIGHT_COLOR, radius=0.1)
        dot1_right = Dot(intercept1_right_coords, color=_HIGHLIGHT_COLOR, radius=0.1)
        
        self.play(
            Create(parabola1, run_time=2),
            LaggedStart(
                FadeIn(dot1_left, scale=0.5),
                FadeIn(dot1_right, scale=0.5),
                lag_ratio=0.5, run_time=1
            )
        )

        # 3. Module Title
        title_text = Text("Parabola Intercepts and the Discriminant", font_size=48, color=_TEXT_COLOR)
        title_text.to_edge(UP, buff=0.75)
        
        self.play(Write(title_text))
        self.wait(1.5)
        self.play(FadeOut(title_text))

        # --- Beat 2: The x-intercepts and their meaning ---
        question_text = Text("Where does the parabola cross the x-axis?", font_size=36, color=_TEXT_COLOR)
        question_text.to_edge(UP)

        self.play(FadeIn(question_text, shift=UP))
        self.play(Indicate(axes[0], scale_factor=1.1, color=_HIGHLIGHT_COLOR)) # Highlight x-axis

        intercept_label_left = Text("(-2, 0)", font_size=24, color=_HIGHLIGHT_COLOR).next_to(dot1_left, DOWN + LEFT, buff=0.1)
        intercept_label_right = Text("(2, 0)", font_size=24, color=_HIGHLIGHT_COLOR).next_to(dot1_right, DOWN + RIGHT, buff=0.1)

        self.play(FadeIn(intercept_label_left), FadeIn(intercept_label_right))
        self.wait(1)

        solution_text = Text("These are the solutions when y = 0.", font_size=32, color=_TEXT_COLOR)
        solution_text.next_to(question_text, DOWN, buff=0.5)
        
        general_form_text = Text("General form: ax² + bx + c = 0", font_size=32, color=_TEXT_COLOR)
        general_form_text.next_to(solution_text, DOWN, buff=0.5)

        self.play(FadeIn(solution_text), FadeIn(general_form_text))
        self.wait(2)

        self.play(
            FadeOut(question_text),
            FadeOut(solution_text),
            FadeOut(general_form_text),
            FadeOut(intercept_label_left),
            FadeOut(intercept_label_right)
        )

        # --- Beat 3: Varying the Parabola - One Intercept, No Intercepts ---
        # 1. One Intercept (y = x^2)
        def func_parabola2(x):
            return x**2
        parabola2 = plane.get_graph(func_parabola2, color=_PARABOLA_COLOR, x_range=[-3, 3])
        dot2 = Dot(plane.c2p(0, 0), color=_HIGHLIGHT_COLOR, radius=0.1)
        
        one_solution_text = Text("One solution", font_size=32, color=_TEXT_COLOR).to_edge(UP)

        self.play(
            ReplacementTransform(parabola1, parabola2, run_time=1.5),
            Transform(VGroup(dot1_left, dot1_right), dot2, run_time=1.5), # Transform two dots into one
        )
        self.play(FadeIn(one_solution_text, shift=UP))
        self.wait(1)
        self.play(FadeOut(one_solution_text, shift=UP))

        # 2. No Intercepts (y = x^2 + 2)
        def func_parabola3(x):
            return x**2 + 2
        parabola3 = plane.get_graph(func_parabola3, color=_PARABOLA_COLOR, x_range=[-3, 3])
        
        no_real_solutions_text = Text("No real solutions", font_size=32, color=_TEXT_COLOR).to_edge(UP)

        self.play(
            ReplacementTransform(parabola2, parabola3, run_time=1.5),
            FadeOut(dot2) # The dot disappears
        )
        self.play(FadeIn(no_real_solutions_text, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(no_real_solutions_text, shift=UP))

        # Return to original parabola for context
        self.play(ReplacementTransform(parabola3, parabola1, run_time=1), FadeIn(dot1_left), FadeIn(dot1_right))
        
        # --- Beat 4: The Discriminant - Intuition ---
        context_text = Text("The number of solutions depends on one special part...", font_size=36, color=_TEXT_COLOR)
        context_text.to_edge(UP)
        self.play(FadeIn(context_text, shift=UP))
        self.wait(1)

        quadratic_formula_intro = Text("The Quadratic Formula:", font_size=32, color=_TEXT_COLOR)
        quadratic_formula_intro.next_to(context_text, DOWN, buff=0.5)
        self.play(FadeIn(quadratic_formula_intro))
        self.wait(0.5)

        # Build quadratic formula using Text objects (no MathTex)
        x_equals = Text("x = ", font_size=36, color=_TEXT_COLOR)
        minus_b = Text("-b ", font_size=36, color=_TEXT_COLOR)
        plus_minus = Text("± ", font_size=36, color=_TEXT_COLOR)
        
        sqrt_open = Text("sqrt(", font_size=36, color=_TEXT_COLOR)
        discriminant_val_text = Text("b² - 4ac", font_size=36, color=_DISCRIMINANT_COLOR)
        sqrt_close = Text(")", font_size=36, color=_TEXT_COLOR)

        numerator_group = VGroup(minus_b, plus_minus, sqrt_open, discriminant_val_text, sqrt_close).arrange(RIGHT, buff=0.05)
        
        line_numerator = Line(LEFT, RIGHT).set_width(numerator_group.get_width() + 0.2).set_stroke(width=2, color=_TEXT_COLOR)
        line_numerator.next_to(numerator_group, DOWN, buff=0.1)

        two_a = Text("2a", font_size=36, color=_TEXT_COLOR)
        
        # Position the '2a' below the line, centered
        two_a.next_to(line_numerator, DOWN, buff=0.1)

        # Group formula parts
        formula_group = VGroup(
            x_equals,
            numerator_group.copy().move_to(ORIGIN), # Create copy to use for relative positioning
            line_numerator.copy().move_to(ORIGIN),
            two_a.copy().move_to(ORIGIN)
        )

        # Repositioning elements manually for a pseudo-fraction layout
        # This is a simplified visual representation, not a true fraction bar for the full length.
        # Given "Do not use Tex/MathTex", this is the most practical way to represent it.
        # The goal is to draw attention to the discriminant part.
        
        # Adjust vertical spacing for the formula parts
        x_equals.next_to(quadratic_formula_intro, DOWN, buff=0.5).align_to(numerator_group, LEFT)
        numerator_group.next_to(x_equals, RIGHT, buff=0.1).shift(0.2*UP) # Shift up to make space for the line
        line_numerator.set_width(numerator_group.get_width() + 0.2).next_to(numerator_group, DOWN, buff=0.1).align_to(numerator_group, LEFT)
        two_a.next_to(line_numerator, DOWN, buff=0.1).align_to(line_numerator, LEFT) # Align to the start of the line

        # Final assemble the formula
        quadratic_formula_elements = VGroup(x_equals, numerator_group, line_numerator, two_a)
        quadratic_formula_elements.move_to(ORIGIN)
        quadratic_formula_elements.next_to(quadratic_formula_intro, DOWN, buff=0.75)


        self.play(LaggedStart(
            FadeIn(x_equals, shift=LEFT),
            FadeIn(minus_b, shift=LEFT),
            FadeIn(plus_minus, shift=LEFT),
            FadeIn(sqrt_open, shift=LEFT),
            FadeIn(discriminant_val_text, shift=LEFT),
            FadeIn(sqrt_close, shift=LEFT),
            FadeIn(line_numerator, shift=LEFT),
            FadeIn(two_a, shift=LEFT),
            lag_ratio=0.1,
            group=VGroup(quadratic_formula_elements),
            run_time=3
        ))
        
        self.wait(1)

        key_part_text = Text("This part determines how many answers we get!", font_size=32, color=_TEXT_COLOR)
        key_part_text.next_to(quadratic_formula_elements, DOWN, buff=0.75)
        
        self.play(FadeIn(key_part_text, shift=DOWN))
        self.play(Indicate(discriminant_val_text, scale_factor=1.2, color=_HIGHLIGHT_COLOR, run_time=1.5))
        self.wait(1.5)

        self.play(
            FadeOut(context_text),
            FadeOut(quadratic_formula_intro),
            FadeOut(quadratic_formula_elements),
            FadeOut(key_part_text)
        )

        # --- Beat 5: Formalizing the Discriminant ---
        discriminant_isolated = Text("b² - 4ac", font_size=60, color=_DISCRIMINANT_COLOR)
        discriminant_isolated_label = Text("The DISCRIMINANT", font_size=36, color=_TEXT_COLOR).next_to(discriminant_isolated, UP, buff=0.75)
        
        self.play(FadeIn(discriminant_isolated))
        self.play(FadeIn(discriminant_isolated_label))
        self.wait(1)

        # 1. Case > 0 (2 solutions)
        case1_text = Text("When b² - 4ac > 0:", font_size=32, color=_HIGHLIGHT_COLOR).next_to(discriminant_isolated_label, UP, buff=0.75).align_to(LEFT, about_edge=True)
        case1_result = Text("2 Solutions", font_size=32, color=_TEXT_COLOR).next_to(case1_text, RIGHT, buff=0.5)
        case1_group = VGroup(case1_text, case1_result).to_edge(UP)

        self.play(FadeIn(case1_group))
        
        # Ensure parabola1 is visible
        if not parabola1.is_shown():
            self.add(parabola1, dot1_left, dot1_right)
        
        self.play(
            parabola1.animate.set_color(_PARABOLA_COLOR), # Reset color if it changed
            FadeIn(dot1_left), FadeIn(dot1_right)
        )
        self.wait(1.5)

        # 2. Case = 0 (1 solution)
        case2_text = Text("When b² - 4ac = 0:", font_size=32, color=_HIGHLIGHT_COLOR).next_to(case1_group, DOWN, buff=0.5).align_to(case1_group, LEFT)
        case2_result = Text("1 Solution", font_size=32, color=_TEXT_COLOR).next_to(case2_text, RIGHT, buff=0.5)
        case2_group = VGroup(case2_text, case2_result)

        self.play(FadeIn(case2_group))

        parabola2_re_create = plane.get_graph(func_parabola2, color=_PARABOLA_COLOR, x_range=[-3, 3]) # Re-create if it got transformed
        dot2_re_create = Dot(plane.c2p(0, 0), color=_HIGHLIGHT_COLOR, radius=0.1)

        self.play(
            Transform(parabola1, parabola2_re_create),
            Transform(VGroup(dot1_left, dot1_right), dot2_re_create)
        )
        self.wait(1.5)

        # 3. Case < 0 (0 real solutions)
        case3_text = Text("When b² - 4ac < 0:", font_size=32, color=_HIGHLIGHT_COLOR).next_to(case2_group, DOWN, buff=0.5).align_to(case2_group, LEFT)
        case3_result = Text("0 Real Solutions", font_size=32, color=_TEXT_COLOR).next_to(case3_text, RIGHT, buff=0.5)
        case3_group = VGroup(case3_text, case3_result)
        
        self.play(FadeIn(case3_group))

        parabola3_re_create = plane.get_graph(func_parabola3, color=_PARABOLA_COLOR, x_range=[-3, 3])
        
        self.play(
            Transform(parabola2_re_create, parabola3_re_create), # Use the parabola2_re_create as the current state
            FadeOut(dot2_re_create)
        )
        self.wait(2)

        self.play(
            FadeOut(VGroup(case1_group, case2_group, case3_group, discriminant_isolated, discriminant_isolated_label)),
            FadeOut(parabola3_re_create)
        )
        
        # --- Beat 6: Recap Card ---
        recap_title = Text("Recap: Parabola Intercepts", font_size=44, color=_HIGHLIGHT_COLOR).to_edge(UP, buff=0.75)
        
        bullet1 = Text("• Solutions to ax² + bx + c = 0 are x-intercepts.", font_size=30, color=_TEXT_COLOR)
        bullet2 = Text("• The Discriminant (b² - 4ac) determines the number of solutions.", font_size=30, color=_TEXT_COLOR)
        bullet3 = Text("• b² - 4ac > 0: Two distinct real solutions.", font_size=30, color=_TEXT_COLOR)
        bullet4 = Text("• b² - 4ac = 0: One real solution (repeated).", font_size=30, color=_TEXT_COLOR)
        bullet5 = Text("• b² - 4ac < 0: No real solutions.", font_size=30, color=_TEXT_COLOR)

        recap_bullets = VGroup(bullet1, bullet2, bullet3, bullet4, bullet5).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        recap_bullets.next_to(recap_title, DOWN, buff=0.75)
        recap_bullets.align_to(recap_title, LEFT)
        recap_bullets.shift(LEFT * 0.5) # Shift slightly left for better alignment visually

        self.play(FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN) for b in recap_bullets], lag_ratio=0.3, run_time=3))
        self.wait(3)

        self.play(FadeOut(recap_title), FadeOut(recap_bullets), FadeOut(plane)) # Fade out everything at the end