from manim import *

class QuadraticFormulaTrick(Scene):
    def construct(self):
        # --- Configuration for colors ---
        self.camera.background_color = BLACK
        TEXT_COLOR = WHITE
        HIGHLIGHT_COLOR_GOLD = GOLD_A 
        HIGHLIGHT_COLOR_BLUE = BLUE_C 
        AXES_COLOR = GREY_B
        PARABOLA_COLOR = BLUE_E

        # --- Beat 1: The Problem & Visual Hook (Roots of a Parabola) ---
        # Introduce axes and a generic parabola
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 4, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": AXES_COLOR, "include_numbers": False},
        ).to_edge(DOWN, buff=0.7)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        parabola_func = lambda x: 0.5 * x**2 + x - 1.5 # Roots at x=1, x=-3; Vertex at x=-1
        graph = axes.get_graph(parabola_func, x_range=[-4, 4], color=PARABOLA_COLOR)

        root1 = Dot(axes.c2p(1, 0), color=HIGHLIGHT_COLOR_BLUE)
        root2 = Dot(axes.c2p(-3, 0), color=HIGHLIGHT_COLOR_BLUE)
        
        # Title and opening question
        title = Text("Finding Quadratic Roots", font_size=50, color=TEXT_COLOR).to_edge(UP)
        question = Text("The 'how' behind finding x-intercepts", font_size=36, color=TEXT_COLOR).next_to(title, DOWN)

        self.play(Write(title))
        self.play(Create(axes), Create(labels), run_time=1.5)
        self.play(Create(graph), run_time=2)
        self.play(FadeIn(root1, root2))
        self.play(Write(question), run_time=1.5)
        self.wait(1.5)

        # Clear visual hook elements to prepare for algebraic manipulation
        self.play(FadeOut(question, title, labels, root1, root2, graph))
        
        # --- Beat 2: The Core Idea - Symmetry ---
        # Introduce the general quadratic equation
        equation_general = MathTex("ax^2 + bx + c = 0", color=TEXT_COLOR).to_edge(UP, buff=0.8)
        self.play(Write(equation_general))
        self.wait(0.5)

        # Re-introduce the parabola to highlight axis of symmetry
        graph_symmetry = axes.get_graph(parabola_func, x_range=[-4, 4], color=PARABOLA_COLOR)
        axis_of_symmetry_x = -1 
        axis_line = axes.get_vertical_line(axes.c2p(axis_of_symmetry_x, 0), color=HIGHLIGHT_COLOR_GOLD, stroke_width=4)
        axis_label = MathTex("x = -\\frac{b}{2a}", color=HIGHLIGHT_COLOR_GOLD).scale(0.8).next_to(axis_line, RIGHT, buff=0.1)
        
        symmetry_text = Text("Roots are symmetric around the vertex's x-value", font_size=28, color=TEXT_COLOR).next_to(axes, UP, buff=0.5)

        self.play(FadeIn(graph_symmetry), Create(axis_line))
        self.play(Write(axis_label))
        self.play(Write(symmetry_text))
        self.wait(1.5)
        
        # Expressing roots in terms of symmetry: x = -b/2a +/- u
        roots_symmetry_form = MathTex("x = -\\frac{b}{2a} \\pm u", color=HIGHLIGHT_COLOR_BLUE).next_to(equation_general, DOWN, buff=0.5)
        self.play(FadeOut(symmetry_text, graph_symmetry, axis_line, axis_label)) 
        self.play(Write(roots_symmetry_form), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(roots_symmetry_form)) # Fade out symmetry form, focus on derivation
        
        # Transform the general equation to its normalized form for algebraic manipulation
        equation_norm_start = MathTex("x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0", color=TEXT_COLOR).move_to(equation_general.get_center())
        self.play(ReplacementTransform(equation_general, equation_norm_start))
        self.wait(1)

        # --- Beat 3: Algebraic Manipulation (Completing the Square) ---
        # Step 1: Isolate the x terms
        equation_step1 = MathTex("x^2 + \\frac{b}{a}x = -\\frac{c}{a}", color=TEXT_COLOR).move_to(equation_norm_start.get_center())
        self.play(ReplacementTransform(equation_norm_start, equation_step1))
        self.wait(0.5)
        
        # Step 2: Add (b/2a)^2 to both sides to complete the square
        square_term_highlight = MathTex("\\left(\\frac{b}{2a}\\right)^2", color=HIGHLIGHT_COLOR_GOLD).scale(0.8)
        
        equation_step2 = VGroup(
            MathTex("x^2 + \\frac{b}{a}x + ", color=TEXT_COLOR),
            square_term_highlight.copy(),
            MathTex(" = -\\frac{c}{a} + ", color=TEXT_COLOR),
            square_term_highlight.copy()
        ).arrange(RIGHT, buff=0.1).move_to(equation_step1.get_center())

        self.play(TransformMatchingTex(equation_step1, equation_step2), run_time=2)
        self.wait(1)

        # Step 3: Factor the left side
        equation_step3 = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2",
            " = -\\frac{c}{a} + \\frac{b^2}{4a^2}",
            color=TEXT_COLOR
        ).move_to(equation_step1.get_center())
        self.play(TransformMatchingTex(equation_step2, equation_step3), run_time=2)
        self.wait(1)

        # Step 4: Combine terms on the right side
        equation_step4 = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2",
            " = \\frac{b^2 - 4ac}{4a^2}",
            color=TEXT_COLOR
        ).move_to(equation_step1.get_center())
        self.play(TransformMatchingTex(equation_step3, equation_step4), run_time=2)
        self.wait(1)

        # --- Beat 4: The Formula Emerges ---
        # Step 5: Take the square root of both sides
        equation_step5 = MathTex(
            "x + \\frac{b}{2a}",
            " = \\pm \\sqrt{\\frac{b^2 - 4ac}{4a^2}}",
            color=TEXT_COLOR
        ).move_to(equation_step1.get_center())
        self.play(TransformMatchingTex(equation_step4, equation_step5), run_time=1.5)
        self.wait(0.5)

        # Step 6: Simplify the square root
        equation_step6 = MathTex(
            "x + \\frac{b}{2a}",
            " = \\pm \\frac{\\sqrt{b^2 - 4ac}}{2a}",
            color=TEXT_COLOR
        ).move_to(equation_step1.get_center())
        self.play(TransformMatchingTex(equation_step5, equation_step6), run_time=1.5)
        self.wait(0.5)

        # Step 7: Isolate x
        equation_final = MathTex(
            "x = -\\frac{b}{2a} \\pm \\frac{\\sqrt{b^2 - 4ac}}{2a}",
            color=TEXT_COLOR
        ).move_to(equation_step1.get_center())
        self.play(TransformMatchingTex(equation_step6, equation_final), run_time=1.5)
        self.wait(0.5)

        # Final form of the quadratic formula
        quadratic_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=HIGHLIGHT_COLOR_GOLD
        ).scale(1.5).move_to(equation_step1.get_center())

        self.play(TransformMatchingTex(equation_final, quadratic_formula), run_time=2)
        self.wait(2)

        # --- Beat 5: Recap Card ---
        # Clear the formula, show a recap card
        self.play(FadeOut(quadratic_formula))

        recap_title = Text("Quadratic Formula: The Big Picture", font_size=50, color=TEXT_COLOR).to_edge(UP, buff=0.8)
        recap_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=HIGHLIGHT_COLOR_GOLD
        ).scale(1.8).move_to(ORIGIN)

        notes = VGroup(
            MathTex("\\bullet", "\\text{ Finds roots of } ax^2+bx+c=0", color=TEXT_COLOR),
            MathTex("\\bullet", "\\text{ Roots are symmetric about } x=-b/(2a)", color=TEXT_COLOR),
            MathTex("\\bullet", "\\text{ Derived by completing the square}", color=TEXT_COLOR)
        ).scale(0.8).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(recap_formula, DOWN, buff=1.0)
        
        # Highlight bullet points
        for note in notes:
            note[0].set_color(HIGHLIGHT_COLOR_BLUE)

        self.play(Write(recap_title))
        self.play(Create(recap_formula))
        self.play(LaggedStart(*[FadeIn(note) for note in notes], lag_ratio=0.7))
        self.wait(3)

        self.play(FadeOut(recap_title, recap_formula, notes, axes))
        self.wait(1)