from manim import *

class DiscriminantAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C

        # --- Title/Introduction (Quick Fade) ---
        title = Text("Understanding the Discriminant's Role", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        subtitle = Text("Predicting Quadratic Solutions", font_size=30, color=BLUE_ACCENT).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), FadeIn(subtitle, shift=UP), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # --- Beat 1: The Visual Hook - Parabola's Relationship with X-axis ---
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": GREY_BROWN},
            background_line_style={"stroke_opacity": 0.4}
        ).add_coordinates().shift(LEFT*2)
        
        # Labels for the axes
        axes_label_x = MathTex("x", color=GREY_BROWN).next_to(plane.x_axis, RIGHT).shift(UP*0.2)
        axes_label_y = MathTex("y", color=GREY_BROWN).next_to(plane.y_axis, UP)

        self.play(Create(plane), Create(axes_label_x), Create(axes_label_y), run_time=1)

        # Parabola definition: y = x^2 + c. 'c' is varied to move it vertically.
        parabola_offset = ValueTracker(-2) # Start with two solutions
        parabola_func = lambda x, c: x**2 + c
        
        parabola = always_redraw(
            lambda: FunctionGraph(
                lambda x: parabola_func(x, parabola_offset.get_value()),
                x_range=[-3, 3],
                color=BLUE_ACCENT,
                stroke_width=5
            )
        )
        
        question_text = Text(
            "How many times does this curve\ntouch the x-axis?", 
            font_size=30, 
            color=GOLD_ACCENT,
            line_spacing=0.8
        ).to_edge(RIGHT).shift(UP*1.5)

        self.play(Create(parabola), Write(question_text), run_time=1.5)
        self.wait(0.5)

        # Animate the parabola moving to show 2, 1, 0 intercepts
        self.play(parabola_offset.animate.set_value(0), run_time=1.5) # One solution
        self.wait(0.5)
        self.play(parabola_offset.animate.set_value(2), run_time=1.5) # No solutions
        self.wait(0.5)
        self.play(parabola_offset.animate.set_value(-2.5), run_time=1.5) # Two solutions again
        self.wait(1)

        # --- Beat 2: Connecting Intercepts to Solutions ---
        solution_text = Text(
            "Each touch point is a 'real solution'\n to the equation ax²+bx+c=0", 
            font_size=28, 
            color=BLUE_ACCENT,
            t2c={'real solution': GOLD_ACCENT, 'ax²+bx+c=0': GOLD_ACCENT},
            line_spacing=0.8
        ).move_to(question_text.get_center())

        quadratic_equation = MathTex(
            "ax^2 + bx + c = 0",
            color=GOLD_ACCENT,
            font_size=40
        ).next_to(solution_text, DOWN, buff=0.8)

        self.play(
            FadeTransform(question_text, solution_text),
            FadeIn(quadratic_equation, shift=UP),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 3: Introducing the "Predictor" - The Discriminant ---
        self.play(FadeOut(solution_text), FadeOut(plane), FadeOut(axes_label_x), 
                  FadeOut(axes_label_y), FadeOut(parabola), FadeOut(parabola_offset),
                  run_time=1)
        self.play(quadratic_equation.animate.center().shift(UP*2), run_time=0.8)

        # Introduce the Quadratic Formula
        intro_formula_text = Text("The Quadratic Formula finds these solutions.", font_size=28, color=BLUE_ACCENT).next_to(quadratic_equation, UP, buff=0.8)
        self.play(Write(intro_formula_text), run_time=1)

        q_formula_full = MathTex(
            "x = ", "{ -b \\pm \\sqrt{", "b^2 - 4ac", "} } \\over {2a} }", 
            color=BLUE_ACCENT
        ).next_to(quadratic_equation, DOWN, buff=0.8)
        q_formula_full[2].set_color(GOLD_ACCENT) # Highlight the discriminant part

        self.play(Write(q_formula_full), run_time=2)
        self.wait(1)
        
        # Point to and label the discriminant
        discriminant_label = MathTex(
            "\\text{This part (the Discriminant)}", 
            "\\Delta", 
            "= b^2 - 4ac", 
            font_size=40,
            color=GOLD_ACCENT,
            t2c={"\\Delta": BLUE_ACCENT}
        ).next_to(q_formula_full, DOWN, buff=1.0)
        
        arrow = Arrow(
            start=discriminant_label[0].get_edge_center(UP),
            end=q_formula_full[2].get_edge_center(DOWN),
            color=GOLD_ACCENT,
            max_stroke_width_to_length_ratio=0.08
        )
        
        self.play(
            FadeIn(discriminant_label[0], shift=UP*0.5),
            GrowArrow(arrow),
            run_time=1
        )
        self.play(
            Write(discriminant_label[1]),
            Write(discriminant_label[2]),
            run_time=1.5
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(intro_formula_text), 
            FadeOut(q_formula_full), 
            FadeOut(arrow),
            FadeOut(quadratic_equation),
            run_time=1
        )
        self.play(discriminant_label.animate.to_edge(UP).shift(DOWN*0.5), run_time=1)
        # Transform the detailed label into just the formula
        discriminant_formula = MathTex("\\Delta = b^2 - 4ac", color=GOLD_ACCENT, font_size=50).move_to(discriminant_label.get_center())
        self.play(TransformMatchingTex(discriminant_label, discriminant_formula), run_time=1)
        self.wait(1)

        # --- Beat 4: The Three Cases ---
        case_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 4, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": GREY_BROWN},
            background_line_style={"stroke_opacity": 0.4}
        ).add_coordinates().shift(LEFT*2)
        self.play(Create(case_plane), run_time=1)
        self.wait(0.5)

        # Case 1: Delta > 0 (Two Real Solutions)
        c1_val = ValueTracker(-2.5) # Parabola with two roots
        parabola1 = always_redraw(
            lambda: FunctionGraph(
                lambda x: x**2 + c1_val.get_value(),
                x_range=[-3, 3],
                color=BLUE_ACCENT,
                stroke_width=5
            )
        )
        
        case1_text = VGroup(
            MathTex("\\Delta > 0", color=GOLD_ACCENT, font_size=40),
            Text("Two Real Solutions", color=BLUE_ACCENT, font_size=30)
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT).shift(UP*0.8)
        
        self.play(Create(parabola1), FadeIn(case1_text[0], shift=UP*0.2), run_time=1)
        self.play(Write(case1_text[1]), run_time=1)
        self.wait(1.5)

        # Case 2: Delta = 0 (One Real Solution)
        c2_val = ValueTracker(0) # Parabola with one root (tangent)
        parabola2 = always_redraw(
            lambda: FunctionGraph(
                lambda x: x**2 + c2_val.get_value(),
                x_range=[-3, 3],
                color=BLUE_ACCENT,
                stroke_width=5
            )
        )
        
        case2_text = VGroup(
            MathTex("\\Delta = 0", color=GOLD_ACCENT, font_size=40),
            Text("One Real Solution", color=BLUE_ACCENT, font_size=30)
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT).shift(UP*0.8)

        self.play(
            ReplacementTransform(parabola1, parabola2),
            TransformMatchingTex(case1_text[0], case2_text[0]),
            FadeTransform(case1_text[1], case2_text[1]),
            run_time=2
        )
        self.wait(1.5)

        # Case 3: Delta < 0 (No Real Solutions)
        c3_val = ValueTracker(2.5) # Parabola with no roots
        parabola3 = always_redraw(
            lambda: FunctionGraph(
                lambda x: x**2 + c3_val.get_value(),
                x_range=[-3, 3],
                color=BLUE_ACCENT,
                stroke_width=5
            )
        )

        case3_text = VGroup(
            MathTex("\\Delta < 0", color=GOLD_ACCENT, font_size=40),
            Text("No Real Solutions", color=BLUE_ACCENT, font_size=30)
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT).shift(UP*0.8)

        self.play(
            ReplacementTransform(parabola2, parabola3),
            TransformMatchingTex(case2_text[0], case3_text[0]),
            FadeTransform(case2_text[1], case3_text[1]),
            run_time=2
        )
        self.wait(1.5)

        self.play(
            FadeOut(parabola3),
            FadeOut(case3_text),
            FadeOut(case_plane),
            FadeOut(discriminant_formula),
            run_time=1
        )
        
        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: The Discriminant (Δ)", color=GOLD_ACCENT, font_size=40).to_edge(UP)
        self.play(Write(recap_title), run_time=1)

        recap_formula = MathTex("\\Delta = b^2 - 4ac", color=GOLD_ACCENT, font_size=45).next_to(recap_title, DOWN, buff=0.6)
        self.play(Write(recap_formula), run_time=1)

        recap_points = VGroup(
            MathTex("\\Delta > 0 \\quad \\implies \\quad \\text{Two Real Solutions}", color=BLUE_ACCENT, font_size=35, t2c={"\\text{Two Real Solutions}": GOLD_ACCENT}),
            MathTex("\\Delta = 0 \\quad \\implies \\quad \\text{One Real Solution}", color=BLUE_ACCENT, font_size=35, t2c={"\\text{One Real Solution}": GOLD_ACCENT}),
            MathTex("\\Delta < 0 \\quad \\implies \\quad \\text{No Real Solutions}", color=BLUE_ACCENT, font_size=35, t2c={"\\text{No Real Solutions}": GOLD_ACCENT})
        ).arrange(DOWN, buff=0.7).next_to(recap_formula, DOWN, buff=0.8)

        self.play(LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.7), run_time=3)
        self.wait(3)

        self.play(FadeOut(recap_title), FadeOut(recap_formula), FadeOut(recap_points), run_time=1)
        self.wait(1)