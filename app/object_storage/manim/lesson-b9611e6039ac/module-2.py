from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # --- Configuration and Initial Setup ---
        self.camera.background_color = BLACK
        BLUE_A = "#58CCED" # Light blue
        GOLD_A = "#FFD700" # Gold
        RED_A = "#E07A5F" # A softer red for accents

        # --- Beat 1: Visual Hook - The Parabola and its Roots ---
        title = Text("Applying the Formula & Graphing Solutions", font_size=40, color=BLUE_A).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 8, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": GREY_A, "stroke_width": 2},
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1, "stroke_opacity": 0.6}
        ).shift(DOWN * 0.5)
        
        labels = plane.get_axis_labels(x_label="x", y_label="y").set_color(GREY_A)
        
        # A simple quadratic function for demonstration: y = x^2 - 2x - 3
        # Roots are at x = 3 and x = -1
        def func(x):
            return x**2 - 2*x - 3

        parabola = plane.get_graph(func, color=GOLD_A, stroke_width=5)
        
        self.play(
            LaggedStart(
                Create(plane),
                FadeIn(labels),
                run_time=2
            )
        )
        self.wait(0.5)

        self.play(Create(parabola, run_time=2))
        self.wait(0.5)

        root1_coords = plane.coords_to_point(-1, 0)
        root2_coords = plane.coords_to_point(3, 0)
        
        root1_dot = Dot(root1_coords, color=RED_A)
        root2_dot = Dot(root2_coords, color=RED_A)
        
        solutions_text = Text("Solutions (Roots)", font_size=35, color=BLUE_A).next_to(plane, UP*1.5)

        self.play(
            FadeIn(solutions_text),
            FadeIn(root1_dot),
            FadeIn(root2_dot)
        )
        self.wait(1.5)

        # --- Beat 2: The Need for the Formula (Quadratic Equation) ---
        self.play(FadeOut(root1_dot), FadeOut(root2_dot)) # Clear root dots

        quadratic_eq_title = Text("Quadratic Equation:", font_size=35, color=BLUE_A).next_to(solutions_text, DOWN, buff=0.5).align_to(solutions_text, LEFT)
        
        # Breakdown general form for individual part interaction
        a_gen = Text("a", font_size=50, color=GOLD_A)
        x2_gen = Text("x²", font_size=50, color=GOLD_A)
        plus1_gen = Text(" + ", font_size=50, color=GOLD_A)
        b_gen = Text("b", font_size=50, color=GOLD_A)
        x_gen = Text("x", font_size=50, color=GOLD_A)
        plus2_gen = Text(" + ", font_size=50, color=GOLD_A)
        c_gen = Text("c", font_size=50, color=GOLD_A)
        eq0_gen = Text(" = 0", font_size=50, color=GOLD_A)

        general_form_group = VGroup(
            a_gen, x2_gen, plus1_gen, b_gen, x_gen, plus2_gen, c_gen, eq0_gen
        ).arrange(RIGHT, buff=0.05).next_to(quadratic_eq_title, DOWN, buff=0.3).align_to(quadratic_eq_title, LEFT)
        
        self.play(
            FadeIn(quadratic_eq_title),
            LaggedStart(*[FadeIn(p) for p in general_form_group], lag_ratio=0.05, run_time=2)
        )
        self.wait(1)
        
        question_text = Text("How to find x?", font_size=40, color=BLUE_A).next_to(general_form_group, DOWN, buff=0.8)
        self.play(FadeIn(question_text), Flash(general_form_group, flash_radius=0.5, color=BLUE_A))
        self.wait(1)

        # --- Beat 3: Unveiling the Quadratic Formula ---
        self.play(
            FadeOut(solutions_text),
            FadeOut(quadratic_eq_title),
            FadeOut(question_text),
            general_form_group.animate.scale(0.8).move_to(LEFT * 3 + UP * 2.5) # Move general form aside
        )

        formula_intro = Text("The Quadratic Formula!", font_size=40, color=BLUE_A).next_to(general_form_group, RIGHT, buff=1.0).align_to(general_form_group, UP)
        self.play(FadeIn(formula_intro))

        # Constructing the formula without Tex/MathTex - Individual Mobjects for highlighting
        x_equals = Text("x =", font_size=60, color=BLUE_A)
        
        # Numerator parts
        paren_open_num = Text("(", font_size=60, color=GOLD_A)
        minus_b_form = Text("-b", font_size=60, color=GOLD_A)
        plus_minus_form = Text("±", font_size=60, color=GOLD_A)
        sqrt_sym_form = Text("√", font_size=60, color=GOLD_A) 
        b_squared_form = Text("b²", font_size=60, color=GOLD_A)
        minus_4_form = Text("-4", font_size=60, color=GOLD_A)
        a_form_disc = Text("a", font_size=60, color=GOLD_A)
        c_form_disc = Text("c", font_size=60, color=GOLD_A)
        paren_close_num = Text(")", font_size=60, color=GOLD_A)

        numerator_elements = VGroup(
            paren_open_num, minus_b_form, plus_minus_form, sqrt_sym_form, b_squared_form,
            minus_4_form, a_form_disc, c_form_disc, paren_close_num
        ).arrange(RIGHT, buff=0.05)

        # Denominator parts
        two_form = Text("2", font_size=60, color=GOLD_A)
        a_form_denom = Text("a", font_size=60, color=GOLD_A)
        denominator_elements = VGroup(two_form, a_form_denom).arrange(RIGHT, buff=0.05)

        # Group and position
        fraction_line = Line(LEFT, RIGHT, color=GOLD_A, stroke_width=4).set_width(numerator_elements.width * 1.1)
        
        formula_rhs = VGroup(numerator_elements, fraction_line, denominator_elements).arrange(DOWN, buff=0.2)
        formula_group = VGroup(x_equals, formula_rhs).arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        
        self.play(
            FadeIn(x_equals),
            LaggedStart(
                FadeIn(paren_open_num), FadeIn(minus_b_form), FadeIn(plus_minus_form),
                FadeIn(sqrt_sym_form), FadeIn(b_squared_form), FadeIn(minus_4_form),
                FadeIn(a_form_disc), FadeIn(c_form_disc), FadeIn(paren_close_num),
                Create(fraction_line),
                FadeIn(two_form), FadeIn(a_form_denom),
                lag_ratio=0.05,
                run_time=3.5
            )
        )
        self.wait(1.5)

        # Highlight connection between general form and formula using Transformations
        self.play(Flash(a_gen, color=RED_A), FadeOut(x2_gen, plus1_gen)) # Flash original to indicate it's being used
        self.play(
            Transform(a_gen.copy().set_color(RED_A), a_form_disc.copy().set_color(RED_A)),
            Transform(a_gen.copy().set_color(RED_A), a_form_denom.copy().set_color(RED_A))
        )
        self.wait(0.5)

        self.play(Flash(b_gen, color=BLUE_A), FadeOut(x_gen, plus2_gen))
        self.play(
            Transform(b_gen.copy().set_color(BLUE_A), minus_b_form.copy().set_color(BLUE_A)),
            Transform(b_gen.copy().set_color(BLUE_A), b_squared_form.copy().set_color(BLUE_A))
        )
        self.wait(0.5)

        self.play(Flash(c_gen, color=GOLD_A), FadeOut(eq0_gen))
        self.play(
            Transform(c_gen.copy().set_color(GOLD_A), c_form_disc.copy().set_color(GOLD_A))
        )
        self.wait(1.5)
        
        # --- Beat 4: Graphing the Solutions ---
        self.play(
            FadeOut(formula_intro),
            FadeOut(general_form_group), # Fade out the general form parts
            formula_group.animate.scale(0.7).to_edge(UP).shift(RIGHT*2)
        )

        plane.animate.scale(0.8).move_to(LEFT*2.5 + DOWN*0.5)
        parabola.animate.scale(0.8).move_to(LEFT*2.5 + DOWN*0.5)
        labels.animate.scale(0.8).next_to(plane, RIGHT).shift(RIGHT*0.5 + UP*0.5)
        self.play(
            plane.animate,
            parabola.animate,
            labels.animate,
            FadeIn(root1_dot), FadeIn(root2_dot), # Bring dots back
            run_time=1.5
        )
        self.wait(0.5)

        formula_app_text = Text("Formula gives x-intercepts!", font_size=35, color=BLUE_A).next_to(plane, UP*1.5)
        self.play(FadeIn(formula_app_text))

        # Label roots with generic x1, x2 and then their values
        root_label1_gen = Text("x₁", font_size=30, color=RED_A).next_to(root1_dot, DOWN, buff=0.2)
        root_label2_gen = Text("x₂", font_size=30, color=RED_A).next_to(root2_dot, DOWN, buff=0.2)
        self.play(FadeIn(root_label1_gen), FadeIn(root_label2_gen))

        arrow1 = Arrow(start=formula_group.get_center(), end=root1_dot.get_center(), buff=0.5, color=BLUE_A, tip_length=0.2)
        arrow2 = Arrow(start=formula_group.get_center(), end=root2_dot.get_center(), buff=0.5, color=BLUE_A, tip_length=0.2)

        self.play(Create(arrow1), Create(arrow2))
        self.wait(2)
        
        x1_val = Text("x₁ = -1", font_size=30, color=RED_A).next_to(root1_dot, DOWN, buff=0.2)
        x2_val = Text("x₂ = 3", font_size=30, color=RED_A).next_to(root2_dot, DOWN, buff=0.2)
        self.play(
            ReplacementTransform(root_label1_gen, x1_val),
            ReplacementTransform(root_label2_gen, x2_val)
        )
        self.wait(1.5)

        self.play(FadeOut(arrow1, arrow2, x1_val, x2_val, root1_dot, root2_dot, formula_app_text))


        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(plane, parabola, labels, title, formula_group),
        )

        recap_title = Text("Recap:", font_size=50, color=BLUE_A).to_edge(UP)
        
        bullet1 = Text("• Quadratic Formula finds 'x' solutions.", font_size=35, color=GOLD_A).next_to(recap_title, DOWN, buff=0.8).align_to(recap_title, LEFT)
        bullet2 = Text("• These solutions are the x-intercepts.", font_size=35, color=GOLD_A).next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet3 = Text("• Graphing confirms these points.", font_size=35, color=GOLD_A).next_to(bullet2, DOWN, buff=0.5).align_to(bullet2, LEFT)
        
        recap_group = VGroup(recap_title, bullet1, bullet2, bullet3).center()

        self.play(FadeIn(recap_title))
        self.play(
            LaggedStart(
                FadeIn(bullet1, shift=UP*0.5),
                FadeIn(bullet2, shift=UP*0.5),
                FadeIn(bullet3, shift=UP*0.5),
                lag_ratio=0.5,
                run_time=3
            )
        )
        self.wait(3)
        self.play(FadeOut(recap_group))