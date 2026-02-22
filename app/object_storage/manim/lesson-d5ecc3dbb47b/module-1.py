from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C
        WHITE_TEXT = WHITE

        # --- Beat 1: Strong Visual Hook & Introduction (Curved Motion) ---
        title = Text("Quadratic Equations & Formula", font_size=50).to_edge(UP).set_color(WHITE_TEXT)
        self.play(FadeIn(title))

        # Projectile motion visual hook
        path_color = BLUE_ACCENT
        dot_color = GOLD_ACCENT

        # Define a quadratic function for the path
        def parabola_func(x):
            return -0.5 * (x - 0.5)**2 + 2 # Adjust parameters for a nice arc

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 3, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": GRAY_A},
            tips=False
        ).to_edge(DOWN).shift(LEFT * 0.5)

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        parabola = axes.get_graph(parabola_func, x_range=[0, 3], color=path_color)
        
        # A dot moving along the parabola
        dot = Dot(point=axes.c2p(0, parabola_func(0)), color=dot_color, radius=0.1)

        intro_text = Text("Modeling Curved Motion", font_size=30).next_to(axes, UP, buff=0.5).set_color(WHITE_TEXT)
        
        self.play(
            LaggedStart(
                Create(axes),
                Create(labels),
                FadeIn(intro_text),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.play(Create(parabola), run_time=1.5)
        self.play(MoveAlongPath(dot, parabola), run_time=2.5, rate_func=linear)
        self.remove(dot) # Remove the dot after it finishes

        quadratic_eq_general = MathTex(
            "ax^2 + bx + c = 0",
            font_size=60,
            color=WHITE_TEXT
        )
        
        self.play(
            FadeOut(intro_text),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(parabola),
            Transform(title, Text("The Quadratic Formula", font_size=50).to_edge(UP).set_color(WHITE_TEXT)),
            FadeIn(quadratic_eq_general.move_to(ORIGIN).shift(UP*0.5)), # Bring eq into view
            run_time=1
        )
        self.wait(0.5)

        # --- Beat 2: Intuition - Completing the Square Visual ---
        # Focus on x^2 + bx as areas
        sq_x = Square(side_length=2, color=BLUE_ACCENT, fill_opacity=0.7)
        rect_b_whole = Rectangle(width=0.8, height=2, color=GOLD_ACCENT, fill_opacity=0.7).next_to(sq_x, RIGHT, buff=0)
        
        area_group = VGroup(sq_x, rect_b_whole).shift(LEFT * 2)

        x_label_sq = MathTex("x^2", font_size=35, color=WHITE_TEXT).move_to(sq_x)
        b_label_rect = MathTex("bx", font_size=35, color=WHITE_TEXT).move_to(rect_b_whole)

        equation_part_1_tex = MathTex("x^2 + bx", font_size=50, color=WHITE_TEXT).to_edge(RIGHT).shift(UP*1.5)

        self.play(
            FadeIn(area_group),
            FadeIn(x_label_sq),
            FadeIn(b_label_rect),
            FadeIn(equation_part_1_tex),
            run_time=1.5
        )
        self.wait(0.5)

        # Reshape rect_b for completing the square
        rect_b_split_1 = Rectangle(width=2, height=0.4, color=GOLD_ACCENT, fill_opacity=0.7)
        rect_b_split_2 = rect_b_split_1.copy()

        # Target positions for completing the square (forming a larger square)
        # This is a visual representation for (x + b/2)^2
        target_group = VGroup(sq_x, rect_b_split_1, rect_b_split_2)
        target_group[1].next_to(sq_x, DOWN, buff=0) # Place one piece below x^2
        target_group[2].rotate(PI/2).next_to(sq_x, RIGHT, buff=0) # Rotate and place the other piece to the right
        
        target_group.move_to(LEFT * 2 + DOWN * 0.5)

        self.play(
            FadeOut(x_label_sq),
            FadeOut(b_label_rect),
            FadeOut(rect_b_whole),
            Transform(sq_x, target_group[0]), # x^2
            Create(target_group[1]), # b/2 * x
            Create(target_group[2]), # b/2 * x
            run_time=1.5
        )

        # Add the missing piece (b/2)^2
        missing_sq = Square(side_length=target_group[1].get_width(), color=RED_C, fill_opacity=0.7).next_to(target_group[1], RIGHT, buff=0)
        missing_label = MathTex("(\\frac{b}{2})^2", font_size=35, color=WHITE_TEXT).move_to(missing_sq)

        intuitive_form_text = MathTex(
            "(x + \\frac{b}{2})^2 - (\\frac{b}{2})^2",
            font_size=40,
            color=WHITE_TEXT
        ).next_to(equation_part_1_tex, DOWN, buff=0.5)

        self.play(
            FadeIn(missing_sq),
            FadeIn(missing_label),
            TransformMatchingTex(equation_part_1_tex, intuitive_form_text), # Show how x^2+bx becomes (x+b/2)^2 - (b/2)^2
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 3: Formal Notation - The Quadratic Formula ---
        # Combine with + c = 0
        eq_with_c = MathTex(
            "(x + \\frac{b}{2})^2 - (\\frac{b}{2})^2 + c = 0",
            font_size=50,
            color=WHITE_TEXT
        ).move_to(intuitive_form_text.get_center())

        self.play(
            FadeOut(VGroup(sq_x, target_group[1], target_group[2])),
            FadeOut(missing_sq),
            FadeOut(missing_label),
            FadeOut(quadratic_eq_general),
            ReplacementTransform(intuitive_form_text, eq_with_c)
        )
        self.wait(0.5)

        # Derivation steps (simplified) leading to the formula
        step1 = MathTex(
            "(x + \\frac{b}{2})^2 = (\\frac{b}{2})^2 - c",
            font_size=50,
            color=WHITE_TEXT
        ).move_to(eq_with_c.get_center())
        self.play(TransformMatchingTex(eq_with_c, step1), run_time=1)
        self.wait(0.5)

        step2 = MathTex(
            "x + \\frac{b}{2} = \\pm\\sqrt{(\\frac{b}{2})^2 - c}",
            font_size=50,
            color=WHITE_TEXT
        ).move_to(step1.get_center())
        self.play(TransformMatchingTex(step1, step2), run_time=1)
        self.wait(0.5)

        quadratic_formula_final = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=60,
            color=GOLD_ACCENT # Highlight the formula itself
        ).move_to(ORIGIN).shift(DOWN*0.5)
        
        formula_label = Text("The Quadratic Formula:", font_size=30, color=WHITE_TEXT).next_to(quadratic_formula_final, UP, buff=0.5)

        self.play(
            FadeOut(step2),
            LaggedStart(
                FadeIn(formula_label),
                Create(quadratic_formula_final),
                lag_ratio=0.5
            )
        )
        self.wait(1)

        # --- Beat 4: Applications & Roots ---
        self.play(FadeOut(formula_label))
        self.play(quadratic_formula_final.animate.to_edge(UP + RIGHT).scale(0.7), FadeOut(title))

        app_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY_A},
            tips=False
        ).shift(LEFT * 2)

        app_labels = app_axes.get_axis_labels(x_label="x", y_label="y")

        # Example quadratic: x^2 - 2x - 3 = 0, roots at x = -1, x = 3
        def example_parabola_func(x):
            return x**2 - 2*x - 3

        example_parabola = app_axes.get_graph(example_parabola_func, x_range=[-2, 4], color=BLUE_ACCENT)
        root1_dot = Dot(point=app_axes.c2p(-1, 0), color=RED_E, radius=0.1)
        root2_dot = Dot(point=app_axes.c2p(3, 0), color=RED_E, radius=0.1)

        roots_text = Text("Roots (x-intercepts)", font_size=30).next_to(app_axes, UP, buff=0.5).set_color(WHITE_TEXT)

        self.play(
            Create(app_axes),
            Create(app_labels),
            FadeIn(roots_text)
        )
        self.play(Create(example_parabola), run_time=2)
        self.play(GrowFromCenter(root1_dot), GrowFromCenter(root2_dot))
        self.wait(1)

        # Text for applications
        applications_title = Text("Applications:", font_size=35).to_edge(RIGHT).shift(UP*1.5).set_color(WHITE_TEXT)
        app_list = VGroup(
            Text("• Projectile Motion", font_size=25, color=WHITE_TEXT),
            Text("• Area Calculations", font_size=25, color=WHITE_TEXT),
            Text("• Optimization", font_size=25, color=WHITE_TEXT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(applications_title, DOWN, buff=0.5).align_to(applications_title, LEFT)

        self.play(
            FadeIn(applications_title),
            LaggedStart(*[FadeIn(app) for app in app_list], lag_ratio=0.3)
        )
        self.wait(1.5)

        # --- Beat 5: Call to Action / Next Steps & Recap ---
        self.play(
            FadeOut(app_axes),
            FadeOut(app_labels),
            FadeOut(example_parabola),
            FadeOut(root1_dot),
            FadeOut(root2_dot),
            FadeOut(roots_text),
            FadeOut(applications_title),
            FadeOut(app_list),
            FadeOut(quadratic_formula_final)
        )

        recap_title = Text("Recap & Next Steps", font_size=50).to_edge(UP).set_color(WHITE_TEXT)
        self.play(FadeIn(recap_title))

        flashcard_text = Text("Guided Practice: Flashcards", font_size=35, color=BLUE_ACCENT)
        ai_spar_text = Text("AI Spar: Test Your Knowledge with Erica", font_size=35, color=GOLD_ACCENT)

        flashcard_rect = Rectangle(width=6, height=1.5, color=BLUE_ACCENT, fill_opacity=0.1).next_to(recap_title, DOWN, buff=1)
        ai_spar_rect = Rectangle(width=7, height=1.5, color=GOLD_ACCENT, fill_opacity=0.1).next_to(flashcard_rect, DOWN, buff=0.7)

        flashcard_group = VGroup(flashcard_rect, flashcard_text.move_to(flashcard_rect))
        ai_spar_group = VGroup(ai_spar_rect, ai_spar_text.move_to(ai_spar_rect))

        self.play(
            FadeIn(flashcard_group, shift=UP),
            FadeIn(ai_spar_group, shift=UP),
            lag_ratio=0.5
        )
        self.wait(2)

        # Final Recap Card (Summary)
        final_recap_card = Rectangle(width=8, height=5, color=WHITE, fill_opacity=0.05).center()
        
        recap_points = VGroup(
            Text("• Quadratics describe curves.", font_size=30, color=WHITE_TEXT),
            Text("• Formula derived from completing the square.", font_size=30, color=WHITE_TEXT),
            Text("• Solves for x-intercepts/roots (x when y=0).", font_size=30, color=WHITE_TEXT),
            Text("• Essential for physics, engineering, graphics.", font_size=30, color=WHITE_TEXT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(final_recap_card.get_center()).shift(UP*0.5)

        formula_recap = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=40,
            color=GOLD_ACCENT
        ).next_to(recap_points, DOWN, buff=0.5)


        self.play(
            FadeOut(flashcard_group),
            FadeOut(ai_spar_group),
            FadeOut(recap_title),
            FadeIn(final_recap_card)
        )
        self.play(
            LaggedStart(
                *[FadeIn(point, shift=UP) for point in recap_points],
                Create(formula_recap),
                lag_ratio=0.3
            )
        )
        self.wait(3)

        self.play(FadeOut(final_recap_card), FadeOut(recap_points), FadeOut(formula_recap))
        self.wait(1)