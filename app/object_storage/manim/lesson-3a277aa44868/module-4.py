from manim import *

class UnderstandingTheDiscriminant(Scene):
    def construct(self):
        # --- Configuration: Colors and Styles ---
        self.camera.background_color = "#212121" # Dark background
        blue_accent = BLUE_E # For highlights, roots, key elements
        gold_accent = GOLD_C # For the discriminant itself
        white_text = WHITE # For general text and main equations

        # --- Beat 1: The Quadratic Formula and the "Mystery Part" ---
        # Module title
        module_title = Tex("Understanding the Discriminant", color=white_text).scale(1.2)
        self.play(Write(module_title))
        self.wait(0.5)
        self.play(FadeOut(module_title, shift=UP))

        # Strong visual hook: Quadratic formula appears, then highlights the discriminant
        quadratic_formula_str = r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"
        quadratic_formula = MathTex(quadratic_formula_str, color=white_text).scale(1.5)
        self.play(Write(quadratic_formula))
        self.wait(1)

        # Highlight the discriminant part within the formula
        discriminant_part_in_formula = quadratic_formula.copy().set_color(gold_accent).get_part_by_tex(r"b^2 - 4ac")
        mystery_label = Tex("The Heart of the Formula", color=gold_accent).next_to(discriminant_part_in_formula, DOWN, buff=0.7)

        self.play(
            discriminant_part_in_formula.animate.scale(1.2).shift(UP*0.5), # Make it pop out
            FadeIn(mystery_label, shift=UP)
        )
        self.wait(1.5)

        # Extract the discriminant and introduce its formal name
        discriminant_eq = MathTex(r"\Delta = b^2 - 4ac", color=gold_accent).scale(1.8).move_to(ORIGIN)
        self.play(
            ReplacementTransform(discriminant_part_in_formula, discriminant_eq.get_part_by_tex(r"b^2 - 4ac")),
            FadeOut(quadratic_formula, shift=UP),
            FadeOut(mystery_label, shift=UP),
            Write(discriminant_eq.get_part_by_tex(r"\Delta = "))
        )
        self.wait(1)

        name_text = Tex("This is the \\textbf{Discriminant}", color=white_text).next_to(discriminant_eq, DOWN, buff=0.8)
        self.play(Write(name_text))
        self.wait(1)

        self.play(FadeOut(name_text), FadeOut(discriminant_eq))
        self.wait(0.5)

        # --- Setup for beats 2-4: Axes and General Quadratic Equation ---
        # NumberPlane for graphing parabolas
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": GREY_B, "include_numbers": False},
        ).add_coordinates().shift(LEFT*2.5) # Shift left to make space for text
        
        y_label = plane.get_y_axis_label("y", edge=UP, direction=LEFT, buff=0.1)
        x_label = plane.get_x_axis_label("x", edge=RIGHT, direction=DOWN, buff=0.1)
        
        general_quadratic_eq_display = MathTex("ax^2 + bx + c = 0", color=white_text).scale(0.8).to_corner(UL)
        
        self.play(Create(plane), Create(y_label), Create(x_label))
        self.play(Write(general_quadratic_eq_display))
        self.wait(0.5)

        # --- Beat 2: Positive Discriminant (Two Real Roots) ---
        # Example: x^2 - 4 = 0 (a=1, b=0, c=-4) -> Delta = 0^2 - 4(1)(-4) = 16
        eq1_str = r"x^2 - 4 = 0"
        eq1_display = MathTex(eq1_str, color=white_text).next_to(general_quadratic_eq_display, DOWN).align_to(general_quadratic_eq_display, LEFT)
        
        discriminant_val1 = MathTex(r"\Delta = 16 > 0", color=gold_accent).next_to(eq1_display, DOWN).align_to(eq1_display, LEFT)
        
        parabola1 = plane.get_graph(lambda x: x**2 - 4, x_range=[-3, 3], color=blue_accent)
        roots1 = VGroup(
            Dot(plane.coords_to_point(-2, 0), color=blue_accent, radius=0.1),
            Dot(plane.coords_to_point(2, 0), color=blue_accent, radius=0.1)
        )
        
        explanation1 = Tex("Two Real Roots", color=white_text).next_to(discriminant_val1, DOWN).align_to(discriminant_val1, LEFT)
        
        self.play(
            Write(eq1_display),
            Create(parabola1),
            Write(discriminant_val1)
        )
        self.play(
            LaggedStart(
                FadeIn(roots1[0]),
                FadeIn(roots1[1]),
                lag_ratio=0.5
            ),
            Write(explanation1)
        )
        self.wait(2)

        # --- Beat 3: Zero Discriminant (One Real Root) ---
        # Example: x^2 = 0 (a=1, b=0, c=0) -> Delta = 0^2 - 4(1)(0) = 0
        eq2_str = r"x^2 = 0"
        eq2_display = MathTex(eq2_str, color=white_text).next_to(general_quadratic_eq_display, DOWN).align_to(general_quadratic_eq_display, LEFT)
        
        discriminant_val2 = MathTex(r"\Delta = 0", color=gold_accent).next_to(eq2_display, DOWN).align_to(eq2_display, LEFT)
        
        parabola2 = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=blue_accent)
        root2 = Dot(plane.coords_to_point(0, 0), color=blue_accent, radius=0.1) # One point for the single root
        
        explanation2 = Tex("One Real Root (Repeated)", color=white_text).next_to(discriminant_val2, DOWN).align_to(discriminant_val2, LEFT)
        
        self.play(
            TransformMatchingTex(eq1_display, eq2_display), # Change equation text
            Transform(parabola1, parabola2),                # Animate parabola transformation
            FadeOut(roots1),                                # Remove old roots
            TransformMatchingTex(discriminant_val1, discriminant_val2), # Change discriminant value
            TransformMatchingTex(explanation1, explanation2),   # Change explanation
            FadeIn(root2)                                   # Show new single root
        )
        self.wait(2)

        # --- Beat 4: Negative Discriminant (No Real Roots) ---
        # Example: x^2 + 4 = 0 (a=1, b=0, c=4) -> Delta = 0^2 - 4(1)(4) = -16
        eq3_str = r"x^2 + 4 = 0"
        eq3_display = MathTex(eq3_str, color=white_text).next_to(general_quadratic_eq_display, DOWN).align_to(general_quadratic_eq_display, LEFT)
        
        discriminant_val3 = MathTex(r"\Delta = -16 < 0", color=gold_accent).next_to(eq3_display, DOWN).align_to(eq3_display, LEFT)
        
        parabola3 = plane.get_graph(lambda x: x**2 + 4, x_range=[-3, 3], color=blue_accent)
        
        explanation3 = Tex("No Real Roots", color=white_text).next_to(discriminant_val3, DOWN).align_to(discriminant_val3, LEFT)
        
        self.play(
            TransformMatchingTex(eq2_display, eq3_display),
            Transform(parabola2, parabola3),
            FadeOut(root2),
            TransformMatchingTex(discriminant_val2, discriminant_val3),
            TransformMatchingTex(explanation2, explanation3)
        )
        self.wait(2)

        # Clear the graph and related text
        self.play(
            FadeOut(eq3_display),
            FadeOut(discriminant_val3),
            FadeOut(explanation3),
            FadeOut(parabola3),
            FadeOut(plane),
            FadeOut(y_label),
            FadeOut(x_label),
            FadeOut(general_quadratic_eq_display)
        )
        self.wait(0.5)

        # --- Beat 5: Formal Definition & Recap ---
        # Re-introduce the discriminant formula and summarize its conditions
        final_discriminant_eq = MathTex(r"\Delta = b^2 - 4ac", color=gold_accent).scale(1.8)
        self.play(Write(final_discriminant_eq))
        self.wait(1)

        summary_points = VGroup(
            Tex(r"If $\Delta > 0$, Two Real Roots", color=white_text),
            Tex(r"If $\Delta = 0$, One Real Root", color=white_text),
            Tex(r"If $\Delta < 0$, No Real Roots", color=white_text)
        ).arrange(DOWN, buff=0.8).scale(0.9).next_to(final_discriminant_eq, DOWN, buff=1.2)

        self.play(LaggedStart(*[Write(point) for point in summary_points], lag_ratio=0.7))
        self.wait(3)

        # --- Recap Card ---
        self.play(
            FadeOut(final_discriminant_eq, shift=UP),
            FadeOut(summary_points, shift=UP)
        )

        recap_title = Tex("Recap: The Discriminant", color=blue_accent).scale(1.5).to_edge(UP)
        recap_points = VGroup(
            Tex(r"$\Delta = b^2 - 4ac$ (from the quadratic formula)", color=white_text),
            Tex(r"Determines the \\textbf{number of real roots}", color=white_text),
            Tex(r"$\Delta > 0 \Rightarrow$ 2 roots", color=gold_accent),
            Tex(r"$\Delta = 0 \Rightarrow$ 1 root", color=gold_accent),
            Tex(r"$\Delta < 0 \Rightarrow$ 0 roots", color=gold_accent),
            Tex("Essential for solving quadratic equations!", color=white_text)
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).scale(0.9).next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[FadeIn(point, shift=RIGHT) for point in recap_points], lag_ratio=0.3))
        self.wait(4)
        self.play(FadeOut(recap_title, shift=UP), FadeOut(recap_points, shift=UP))
        self.wait(0.5)