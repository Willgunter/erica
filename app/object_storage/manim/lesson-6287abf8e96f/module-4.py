from manim import *

# Custom 3B1B-inspired colors
BLUE_3B1B = ManimColor("#1C75BC")
GOLD_3B1B = ManimColor("#FFD700")
DARK_BACKGROUND = ManimColor("#1A1A1A")
TEXT_COLOR = WHITE

class ParabolaInterceptsAndDiscriminant(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = DARK_BACKGROUND
        self.add_sound("assets/Manim_Sound_Effect_Open.mp3") # Placeholder for a sound effect

        # --- Beat 1: The Mystery of the X-Intercepts (Opening Hook) ---
        title = Text("Parabola Intercepts & Discriminant Meaning", font_size=42, color=GOLD_3B1B).to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            x_length=10, y_length=10,
            axis_config={"color": GREY_A, "stroke_width": 2},
            background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.4}
        ).add_coordinates().shift(DOWN * 0.5)
        self.play(Create(plane, run_time=1.5))

        # Initial parabola: y = x^2 - 4 (two intercepts)
        def func_parabola_initial(x):
            return x**2 - 4
        
        parabola_initial = FunctionGraph(func_parabola_initial, color=BLUE_3B1B, x_range=[-3, 3])
        x_intercept_1 = Dot(plane.c2p(-2, 0), color=GOLD_3B1B)
        x_intercept_2 = Dot(plane.c2p(2, 0), color=GOLD_3B1B)

        question_text = Text("How many x-intercepts?", font_size=32, color=TEXT_COLOR).next_to(plane, UP, buff=0.5)
        
        self.play(
            Create(parabola_initial),
            FadeIn(question_text),
            run_time=2
        )
        self.play(
            FadeIn(x_intercept_1, shift=UP),
            FadeIn(x_intercept_2, shift=UP),
            Flash(x_intercept_1, flash_radius=0.3, color=GOLD_3B1B),
            Flash(x_intercept_2, flash_radius=0.3, color=GOLD_3B1B),
            run_time=1.5
        )
        self.wait(1)

        general_eq_text = MathTex(
            r"y = ax^2 + bx + c",
            font_size=40, color=BLUE_3B1B
        ).next_to(question_text, DOWN, buff=0.2).align_to(question_text, LEFT)
        self.play(
            ReplacementTransform(question_text, general_eq_text),
            run_time=1
        )
        self.wait(0.5)
        self.play(FadeOut(x_intercept_1, x_intercept_2))

        # --- Beat 2: The Discriminant - Three Cases Intuition ---
        discriminant_tex = MathTex(
            r"\text{Discriminant} = b^2 - 4ac",
            font_size=40, color=GOLD_3B1B
        ).next_to(general_eq_text, DOWN, buff=0.5).align_to(general_eq_text, LEFT)
        self.play(Write(discriminant_tex, run_time=1.5))
        self.wait(0.5)

        # ValueTracker for 'c' to smoothly change parabola and discriminant (a=1, b=0 assumed for simplicity)
        c_tracker = ValueTracker(-4) 

        def func_parabola_dynamic(x):
            return x**2 + 0*x + c_tracker.get_value()
        
        dynamic_parabola = always_redraw(
            lambda: FunctionGraph(func_parabola_dynamic, color=BLUE_3B1B, x_range=[-4, 4])
        )

        discriminant_value_text = always_redraw(
            lambda: MathTex(
                r"D = 0^2 - 4(1)(" + f"{c_tracker.get_value():.1f}" + r") = " + f"{-4 * c_tracker.get_value():.1f}",
                font_size=30, color=TEXT_COLOR
            ).next_to(discriminant_tex, DOWN, buff=0.2).align_to(discriminant_tex, LEFT)
        )

        num_intercepts_status = always_redraw(
            lambda: Text(
                self.get_intercept_status_text(c_tracker.get_value()),
                font_size=28, color=TEXT_COLOR
            ).next_to(discriminant_value_text, DOWN, buff=0.2).align_to(discriminant_value_text, LEFT)
        )

        self.play(
            ReplacementTransform(parabola_initial, dynamic_parabola),
            FadeIn(discriminant_value_text),
            FadeIn(num_intercepts_status),
            run_time=1.5
        )
        self.wait(0.5)

        # Case 1: D > 0 (2 intercepts)
        self.play(c_tracker.animate.set_value(-1), run_time=2)
        label_greater_0 = MathTex(r"D > 0 \implies \text{2 Intercepts}", font_size=32, color=GOLD_3B1B).next_to(num_intercepts_status, RIGHT, buff=0.5)
        self.play(FadeIn(label_greater_0, shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(label_greater_0))

        # Case 2: D = 0 (1 intercept)
        self.play(c_tracker.animate.set_value(0), run_time=2)
        label_equal_0 = MathTex(r"D = 0 \implies \text{1 Intercept}", font_size=32, color=GOLD_3B1B).next_to(num_intercepts_status, RIGHT, buff=0.5)
        self.play(FadeIn(label_equal_0, shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(label_equal_0))

        # Case 3: D < 0 (0 intercepts)
        self.play(c_tracker.animate.set_value(1), run_time=2)
        label_less_0 = MathTex(r"D < 0 \implies \text{0 Intercepts}", font_size=32, color=GOLD_3B1B).next_to(num_intercepts_status, RIGHT, buff=0.5)
        self.play(FadeIn(label_less_0, shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(label_less_0))
        
        self.play(FadeOut(discriminant_value_text, num_intercepts_status))
        self.wait(0.5)

        # --- Beat 3: Formalizing the Connection (Quadratic Formula) ---
        quadratic_formula = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=40, color=BLUE_3B1B
        ).to_edge(UP).shift(DOWN*1.5)

        self.play(
            TransformMatchingTex(general_eq_text, quadratic_formula),
            FadeOut(discriminant_tex),
            run_time=1.5
        )
        self.wait(0.5)

        # Highlight the discriminant part
        discriminant_in_formula = quadratic_formula.get_parts_by_tex(r"b^2 - 4ac")[0]
        self.play(
            Flash(discriminant_in_formula, color=GOLD_3B1B, line_length=0.2, num_lines=5, flash_radius=0.5),
            run_time=1
        )
        self.play(
            discriminant_in_formula.animate.set_color(GOLD_3B1B).scale(1.2),
            run_time=0.8
        )
        self.play(
            discriminant_in_formula.animate.set_color(BLUE_3B1B).scale(1/1.2),
            run_time=0.8
        )
        self.wait(0.5)

        # Explain the three cases again with the formula
        d_greater_0_tex = MathTex(r"\sqrt{D} \text{ is real (two values)}", font_size=30, color=TEXT_COLOR).next_to(quadratic_formula, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        d_equal_0_tex = MathTex(r"\sqrt{D} = 0 \text{ (one value)}", font_size=30, color=TEXT_COLOR).next_to(d_greater_0_tex, DOWN, buff=0.3).align_to(d_greater_0_tex, LEFT)
        d_less_0_tex = MathTex(r"\sqrt{D} \text{ is imaginary (no real values)}", font_size=30, color=TEXT_COLOR).next_to(d_equal_0_tex, DOWN, buff=0.3).align_to(d_equal_0_tex, LEFT)

        self.play(
            LaggedStart(
                Write(d_greater_0_tex),
                Write(d_equal_0_tex),
                Write(d_less_0_tex),
                lag_ratio=0.7,
                run_time=3
            )
        )
        self.wait(1)
        self.play(FadeOut(d_greater_0_tex, d_equal_0_tex, d_less_0_tex))
        
        # --- Beat 4: Visualizing 'a's Role (Briefly) ---
        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(0) 
        c_tracker.set_value(0) 

        def func_parabola_a_dynamic(x):
            return a_tracker.get_value() * x**2 + b_tracker.get_value() * x + c_tracker.get_value()
        
        parabola_a_dynamic = always_redraw(
            lambda: FunctionGraph(func_parabola_a_dynamic, color=BLUE_3B1B, x_range=[-4, 4])
        )

        a_coeff_text = always_redraw(
            lambda: MathTex(
                r"a = " + f"{a_tracker.get_value():.1f}",
                font_size=30, color=TEXT_COLOR
            ).to_edge(UL).shift(RIGHT*1.5)
        )
        a_role_desc = Text("Controls opening direction & width", font_size=24, color=TEXT_COLOR).next_to(a_coeff_text, RIGHT, buff=0.3).shift(UP*0.1)

        self.play(
            ReplacementTransform(dynamic_parabola, parabola_a_dynamic),
            FadeIn(a_coeff_text),
            FadeIn(a_role_desc),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(a_tracker.animate.set_value(0.5), run_time=1.5) # Wider
        self.play(a_tracker.animate.set_value(2), run_time=1.5)   # Narrower
        self.play(a_tracker.animate.set_value(-1), run_time=1.5)  # Opens down
        self.wait(1)
        
        self.play(
            FadeOut(parabola_a_dynamic, a_coeff_text, a_role_desc),
            FadeOut(quadratic_formula),
            run_time=1
        )

        # --- Beat 5: Application Example + Final Recap Card ---
        # Example: x^2 + 2x + 1 = 0
        example_eq_tex = MathTex(
            r"x^2 + 2x + 1 = 0",
            font_size=40, color=BLUE_3B1B
        ).to_edge(UL).shift(DOWN*1.5)
        
        discriminant_calc_tex = MathTex(
            r"D = b^2 - 4ac",
            r" = (2)^2 - 4(1)(1)",
            r" = 4 - 4",
            r" = 0",
            font_size=36, color=GOLD_3B1B
        ).next_to(example_eq_tex, DOWN, buff=0.5).align_to(example_eq_tex, LEFT)

        self.play(Write(example_eq_tex), run_time=1)
        self.wait(0.5)
        self.play(
            Write(discriminant_calc_tex[0]),
            run_time=0.5
        )
        self.play(
            TransformMatchingTex(discriminant_calc_tex[0], discriminant_calc_tex[1]),
            run_time=1
        )
        self.play(
            TransformMatchingTex(discriminant_calc_tex[1], discriminant_calc_tex[2]),
            run_time=0.7
        )
        self.play(
            TransformMatchingTex(discriminant_calc_tex[2], discriminant_calc_tex[3]),
            run_time=0.7
        )
        self.wait(1)

        result_text = Text("D = 0 implies 1 real x-intercept", font_size=32, color=TEXT_COLOR).next_to(discriminant_calc_tex, DOWN, buff=0.5).align_to(discriminant_calc_tex, LEFT)
        self.play(Write(result_text))
        self.wait(1)

        def func_example_parabola(x):
            return x**2 + 2*x + 1

        example_parabola = FunctionGraph(func_example_parabola, color=BLUE_3B1B, x_range=[-3, 1])
        x_intercept_example = Dot(plane.c2p(-1, 0), color=GOLD_3B1B)

        self.play(
            Create(example_parabola),
            FadeIn(x_intercept_example, shift=UP),
            Flash(x_intercept_example, flash_radius=0.3, color=GOLD_3B1B),
            run_time=2
        )
        self.wait(2)

        self.play(
            FadeOut(example_eq_tex, discriminant_calc_tex, result_text, example_parabola, x_intercept_example),
            FadeOut(plane),
            FadeOut(title),
            run_time=1.5
        )

        # Final Recap Card
        recap_title = Text("Recap: Discriminant (D)", font_size=48, color=GOLD_3B1B).to_edge(UP)
        
        recap_content = VGroup(
            MathTex(r"D = b^2 - 4ac", font_size=40, color=BLUE_3B1B),
            MathTex(r"\text{If } D > 0 \implies \text{2 real x-intercepts}", font_size=36, color=TEXT_COLOR),
            MathTex(r"\text{If } D = 0 \implies \text{1 real x-intercept}", font_size=36, color=TEXT_COLOR),
            MathTex(r"\text{If } D < 0 \implies \text{0 real x-intercepts}", font_size=36, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.7).center()

        self.play(FadeIn(recap_title))
        self.play(LaggedStart(*[Write(item) for item in recap_content], lag_ratio=0.5, run_time=4))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_content))

    def get_intercept_status_text(self, c_val):
        # For y = x^2 + c, a=1, b=0. D = 0^2 - 4(1)(c) = -4c
        discriminant_val = -4 * c_val
        if discriminant_val > 0.05: # Using a small epsilon for robust comparison
            return "2 real intercepts"
        elif abs(discriminant_val) < 0.05:
            return "1 real intercept"
        else: # discriminant_val < -0.05
            return "0 real intercepts"