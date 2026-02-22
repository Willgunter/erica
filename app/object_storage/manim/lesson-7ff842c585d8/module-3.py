from manim import *

class UnderstandingDiscriminant(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#202020" # Clean dark background
        blue_accent = BLUE_E # High-contrast blue
        gold_accent = GOLD # High-contrast gold
        white_text = WHITE # For general text and formulas

        # --- Beat 1: Visual Hook & Introduction to Quadratic Roots (Intuition) ---
        # Title appears first
        title = Text("Understanding the Discriminant", font_size=50, color=white_text).to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)

        # Set up Axes for plotting parabolas
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": blue_accent, "font_size": 24},
            tips=False # Remove arrow tips for a cleaner look
        ).to_edge(LEFT).shift(RIGHT*0.5) # Position on left side
        
        # Labels for axes
        x_label = axes.get_x_axis_label("x", edge=DR, direction=DR, color=blue_accent)
        y_label = axes.get_y_axis_label("y", edge=UL, direction=UL, color=blue_accent)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Initial parabola (y = x^2 - 1) showing two real roots
        def func_two_roots(x):
            return x**2 - 1
        parabola_two_roots = axes.plot(func_two_roots, color=gold_accent)
        
        # Dots for roots
        root1_two = Dot(axes.c2p(-1, 0), color=RED, radius=0.08)
        root2_two = Dot(axes.c2p(1, 0), color=RED, radius=0.08)
        roots_group_two = VGroup(root1_two, root2_two)

        self.play(Create(parabola_two_roots), FadeIn(roots_group_two))
        self.wait(1)

        # Question text introduces the concept
        roots_text = Text("How many real 'x' solutions?", font_size=30, color=white_text).next_to(axes, RIGHT, buff=1)
        self.play(Write(roots_text))
        self.wait(0.5)
        
        # Animate the parabola shifting up/down to illustrate changing number of roots
        # Parabola for one root (y = x^2)
        def func_one_root(x):
            return x**2
        parabola_one_root = axes.plot(func_one_root, color=gold_accent)
        root_one = Dot(axes.c2p(0, 0), color=RED, radius=0.08) # Single root dot

        self.play(
            ReplacementTransform(parabola_two_roots, parabola_one_root), # Smoothly transform parabola
            Transform(roots_group_two, root_one), # Roots merge into one
            roots_text.animate.set_color(blue_accent), # Change text color for emphasis
            run_time=1.5
        )
        self.wait(0.7)

        # Parabola for zero real roots (y = x^2 + 1)
        def func_zero_roots(x):
            return x**2 + 1
        parabola_zero_roots = axes.plot(func_zero_roots, color=gold_accent)

        self.play(
            ReplacementTransform(parabola_one_root, parabola_zero_roots), # Transform parabola again
            FadeOut(roots_group_two), # Roots disappear
            roots_text.animate.set_color(gold_accent), # Change text color
            run_time=1.5
        )
        self.wait(1)
        
        # Clean up for the next beat
        self.play(
            FadeOut(parabola_zero_roots, roots_text, axes, x_label, y_label)
        )

        # --- Beat 2: Zooming into the Quadratic Formula & Isolating the Discriminant (Formal Notation) ---
        # Display the full quadratic formula
        quadratic_formula_full = MathTex(
            "x", "=", "{ -b", "\\pm", "\\sqrt{", "b^2 - 4ac", "}", "}", "\\over", "2a}", # Breaking it down for easy targeting
            color=white_text, font_size=45
        ).shift(UP*0.5)

        self.play(Write(quadratic_formula_full))
        self.wait(1)

        # Highlight the discriminant part (index 5 corresponds to "b^2 - 4ac")
        discriminant_part = quadratic_formula_full[5] 
        
        # Add a brace and label for the discriminant
        brace = Brace(discriminant_part, DOWN, color=blue_accent)
        discriminant_label = MathTex("\\Delta", "=", "b^2 - 4ac", color=blue_accent, font_size=40).next_to(brace, DOWN)

        self.play(
            GrowFromCenter(brace), # Grow the brace
            Write(discriminant_label), # Write the label
            discriminant_part.animate.set_color(gold_accent) # Color the discriminant
        )
        self.wait(1.5)

        # Explain the purpose of the discriminant
        concept_text = Text(
            "The Discriminant (Δ) reveals the number of real solutions!", 
            font_size=30, color=white_text
        ).next_to(discriminant_label, DOWN, buff=0.8)
        self.play(Write(concept_text))
        self.wait(1.5)

        # Prepare for the next beats: keep discriminant formula on screen
        self.play(
            FadeOut(quadratic_formula_full, brace),
            FadeOut(concept_text)
        )
        # Transform the main title into the discriminant formula and move it to the corner
        discriminant_label_corner = MathTex("\\Delta = b^2 - 4ac", color=blue_accent, font_size=45)
        self.play(ReplacementTransform(title, discriminant_label_corner)) 
        
        discriminant_label_corner.to_corner(UL).shift(RIGHT*0.5)
        self.play(discriminant_label_corner.animate.to_corner(UL).shift(RIGHT*0.5))


        # --- Beat 3: Case 1: Discriminant > 0 (Two Real Roots) ---
        case1_text = Text("Case 1: Δ > 0", font_size=35, color=GREEN).next_to(discriminant_label_corner, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(case1_text))
        
        # Re-introduce axes for visual context on the right side
        axes_case1 = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": blue_accent, "font_size": 24},
            tips=False
        ).to_edge(RIGHT).shift(LEFT*0.5)
        self.play(Create(axes_case1))

        # Example parabola with two roots (e.g., x^2 - 2x - 3), where Δ = 16 > 0
        def func_pos_disc(x):
            return x**2 - 2*x - 3
        parabola_pos_disc = axes_case1.plot(func_pos_disc, color=gold_accent)
        root1_pos = Dot(axes_case1.c2p(-1, 0), color=GREEN, radius=0.08)
        root2_pos = Dot(axes_case1.c2p(3, 0), color=GREEN, radius=0.08)
        
        self.play(
            Create(parabola_pos_disc),
            Create(root1_pos),
            Create(root2_pos)
        )
        
        # Show the part of the quadratic formula with Δ for explanation
        solutions_text_pos = MathTex("x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}", color=white_text, font_size=35).next_to(case1_text, DOWN, buff=0.5, aligned_edge=LEFT)
        solutions_text_pos[2].set_color(GREEN) # Highlight Δ in green
        
        result_text_pos = Text("Two Real Solutions", font_size=30, color=GREEN).next_to(solutions_text_pos, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(solutions_text_pos))
        self.play(Write(result_text_pos))
        self.wait(1.5)

        self.play(
            FadeOut(parabola_pos_disc, root1_pos, root2_pos, solutions_text_pos, result_text_pos, axes_case1, case1_text)
        )

        # --- Beat 4: Case 2: Discriminant = 0 (One Real Root) ---
        case2_text = Text("Case 2: Δ = 0", font_size=35, color=YELLOW).next_to(discriminant_label_corner, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(case2_text))

        axes_case2 = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": blue_accent, "font_size": 24},
            tips=False
        ).to_edge(RIGHT).shift(LEFT*0.5)
        self.play(Create(axes_case2))

        # Example parabola with one root (e.g., x^2 - 4x + 4), where Δ = 0
        def func_zero_disc(x):
            return x**2 - 4*x + 4
        parabola_zero_disc = axes_case2.plot(func_zero_disc, color=gold_accent)
        root_zero = Dot(axes_case2.c2p(2, 0), color=YELLOW, radius=0.08)
        
        self.play(
            Create(parabola_zero_disc),
            Create(root_zero)
        )

        # Show how sqrt(0) simplifies the formula
        solutions_text_zero = MathTex("x = \\frac{-b \\pm \\sqrt{0}}{2a} = \\frac{-b}{2a}", color=white_text, font_size=35).next_to(case2_text, DOWN, buff=0.5, aligned_edge=LEFT)
        solutions_text_zero[2].set_color(YELLOW) # Highlight 0
        
        result_text_zero = Text("One Real Solution (Repeated)", font_size=30, color=YELLOW).next_to(solutions_text_zero, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(solutions_text_zero))
        self.play(Write(result_text_zero))
        self.wait(1.5)

        self.play(
            FadeOut(parabola_zero_disc, root_zero, solutions_text_zero, result_text_zero, axes_case2, case2_text)
        )

        # --- Beat 5: Case 3: Discriminant < 0 (Zero Real Roots) ---
        case3_text = Text("Case 3: Δ < 0", font_size=35, color=RED).next_to(discriminant_label_corner, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(case3_text))

        axes_case3 = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": blue_accent, "font_size": 24},
            tips=False
        ).to_edge(RIGHT).shift(LEFT*0.5)
        self.play(Create(axes_case3))

        # Example parabola with zero real roots (e.g., x^2 + 1), where Δ = -4 < 0
        def func_neg_disc(x):
            return x**2 + 1
        parabola_neg_disc = axes_case3.plot(func_neg_disc, color=gold_accent)
        
        self.play(Create(parabola_neg_disc))

        # Explain why negative discriminant means no real roots
        solutions_text_neg = MathTex("x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}", color=white_text, font_size=35).next_to(case3_text, DOWN, buff=0.5, aligned_edge=LEFT)
        solutions_text_neg[2].set_color(RED) # Highlight Δ
        
        sqrt_neg_text = Text("√ (negative number) is not a real number", font_size=28, color=RED).next_to(solutions_text_neg, DOWN, buff=0.2, aligned_edge=LEFT)
        result_text_neg = Text("Zero Real Solutions (Complex Solutions)", font_size=30, color=RED).next_to(sqrt_neg_text, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(solutions_text_neg))
        self.play(Write(sqrt_neg_text))
        self.play(Write(result_text_neg))
        self.wait(2)

        self.play(
            FadeOut(parabola_neg_disc, solutions_text_neg, sqrt_neg_text, result_text_neg, axes_case3, case3_text)
        )
        
        # --- Recap Card ---
        self.play(FadeOut(discriminant_label_corner)) # Fade out the discriminant at top left

        recap_title = Text("Recap: The Discriminant", font_size=45, color=white_text).to_edge(UP)
        self.play(Write(recap_title))

        # Create a VGroup for the recap card for easy arrangement and animation
        recap_card = VGroup(
            MathTex("\\Delta = b^2 - 4ac", color=blue_accent, font_size=40).shift(UP*1.5),
            Tex("Determines the nature of quadratic roots:", color=white_text, font_size=30).shift(UP*0.5),
            VGroup( # Group the bullet points
                Text("• Δ > 0: Two Real Solutions", color=GREEN, font_size=28),
                Text("• Δ = 0: One Real Solution", color=YELLOW, font_size=28),
                Text("• Δ < 0: Zero Real Solutions", color=RED, font_size=28)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*1.2) # Arrange bullet points
        )

        # Use LaggedStart for a staggered reveal of recap points
        self.play(LaggedStart(*[FadeIn(mob, shift=UP) for mob in recap_card], lag_ratio=0.1))
        self.wait(3)

        self.play(FadeOut(recap_title, recap_card))
        self.wait(0.5)