from manim import *

class DiscriminantAnimation(Scene):
    def construct(self):
        # Custom Colors
        BLUE_ACCENT = "#87CEEB" # Sky Blue
        GOLD_ACCENT = "#FFD700" # Gold
        LIGHT_TEXT = WHITE
        DARK_BACKGROUND = BLACK # Manim's default background is dark

        # --- Helper for creating text for expressions without MathTex ---
        def create_expression_text(parts, color=LIGHT_TEXT):
            mobjects = []
            for part in parts:
                if isinstance(part, tuple): # For superscript like ("b", "2")
                    base, sup = part
                    m = VGroup(Text(base, color=color), Text(sup, color=color).scale(0.6).shift(UP * 0.3))
                    mobjects.append(m)
                else:
                    mobjects.append(Text(part, color=color))
            
            expression_vgroup = VGroup(*mobjects).arrange(RIGHT, buff=0.1)
            return expression_vgroup

        # --- Beat 1: Visual Hook & Introduction ---
        self.camera.background_color = DARK_BACKGROUND

        title = Text("The Discriminant: Nature of Solutions", color=GOLD_ACCENT).scale(1.2)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title, shift=UP))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": GRAY_D},
        ).add_coordinates()
        axes_label_x = axes.get_x_axis_label("x", edge=DOWN, direction=DOWN).set_color(GRAY)
        axes_label_y = axes.get_y_axis_label("y", edge=LEFT, direction=LEFT).set_color(GRAY)
        
        self.play(Create(axes), Create(axes_label_x), Create(axes_label_y), run_time=1.5)
        self.wait(0.5)

        intro_text = Text("How many times does it cross the x-axis?", color=LIGHT_TEXT).to_edge(UP).shift(RIGHT*1.5)
        self.play(FadeIn(intro_text, shift=UP))

        # Parabola 1: 2 solutions
        parabola1 = axes.plot(lambda x: 0.5 * x**2 - 2, x_range=[-3.5, 3.5], color=BLUE_ACCENT)
        dots1 = VGroup(Dot(axes.c2p(-2, 0), color=GOLD_ACCENT), Dot(axes.c2p(2, 0), color=GOLD_ACCENT))
        num_solutions1 = Text("2 Solutions", color=GOLD_ACCENT).next_to(parabola1, DOWN).shift(DOWN*0.5)
        
        self.play(Create(parabola1))
        self.play(Create(dots1), Write(num_solutions1))
        self.wait(1)

        # Parabola 2: 1 solution
        parabola2 = axes.plot(lambda x: 0.5 * x**2, x_range=[-3.5, 3.5], color=BLUE_ACCENT)
        dots2 = Dot(axes.c2p(0, 0), color=GOLD_ACCENT)
        num_solutions2 = Text("1 Solution", color=GOLD_ACCENT).next_to(parabola2, DOWN).shift(DOWN*0.5)

        self.play(ReplacementTransform(parabola1, parabola2), 
                  FadeOut(dots1), FadeOut(num_solutions1),
                  Create(dots2), Write(num_solutions2))
        self.wait(1)

        # Parabola 3: 0 solutions
        parabola3 = axes.plot(lambda x: 0.5 * x**2 + 2, x_range=[-3.5, 3.5], color=BLUE_ACCENT)
        num_solutions3 = Text("0 Solutions", color=GOLD_ACCENT).next_to(parabola3, DOWN).shift(DOWN*0.5)

        self.play(ReplacementTransform(parabola2, parabola3), 
                  FadeOut(dots2), FadeOut(num_solutions2),
                  Write(num_solutions3))
        self.wait(1)

        self.play(FadeOut(parabola3, shift=LEFT), FadeOut(num_solutions3, shift=RIGHT), FadeOut(intro_text, shift=UP))

        # --- Beat 2: Introducing the Discriminant ---
        question = Text("What tells us how many solutions?", color=LIGHT_TEXT).to_edge(UP)
        self.play(FadeIn(question, shift=UP))
        self.wait(0.5)

        # The general quadratic equation
        quadratic_equation_parts = [
            ("ax", "2"), "+", "bx", "+", "c", "=", "0"
        ]
        quadratic_equation = create_expression_text(quadratic_equation_parts).scale(0.9)
        quadratic_equation.move_to(ORIGIN)

        self.play(Write(quadratic_equation))
        self.wait(1)

        formula_snippet_text = Text("It's found inside the square root of the quadratic formula!", color=LIGHT_TEXT).next_to(quadratic_equation, UP, buff=1)
        self.play(Write(formula_snippet_text))
        self.wait(1)

        discriminant_concept_parts = [
            ("b", "2"), "-", "4ac"
        ]
        discriminant_concept = create_expression_text(discriminant_concept_parts, color=GOLD_ACCENT).scale(1.2).shift(DOWN*1.5)
        discriminant_label = Text("The Discriminant", color=BLUE_ACCENT).next_to(discriminant_concept, DOWN)

        self.play(FadeOut(quadratic_equation), FadeOut(formula_snippet_text, shift=UP)) 
        self.play(Write(discriminant_concept))
        self.play(FadeIn(discriminant_label, shift=UP))
        self.wait(1.5)

        self.play(FadeOut(discriminant_label, shift=DOWN), FadeOut(question, shift=UP))

        # --- Beat 3: Case 1 - Discriminant > 0 (Two Real Solutions) ---
        discriminant_gt_0_text = create_expression_text([("b", "2"), "-", "4ac", ">", "0"], color=GOLD_ACCENT).to_edge(UP)
        result_gt_0 = Text("Two Real Solutions", color=BLUE_ACCENT).next_to(discriminant_gt_0_text, DOWN, buff=0.5)

        self.play(Transform(discriminant_concept, discriminant_gt_0_text)) # Move and update text
        self.play(FadeIn(result_gt_0, shift=UP))
        self.wait(0.5)

        parabola_gt_0 = axes.plot(lambda x: 0.5 * x**2 - 2, x_range=[-3.5, 3.5], color=BLUE_ACCENT)
        dots_gt_0 = VGroup(Dot(axes.c2p(-2, 0), color=GOLD_ACCENT), Dot(axes.c2p(2, 0), color=GOLD_ACCENT))

        self.play(Create(parabola_gt_0))
        self.play(Create(dots_gt_0))
        self.wait(1.5)

        self.play(FadeOut(parabola_gt_0), FadeOut(dots_gt_0))

        # --- Beat 4: Case 2 - Discriminant = 0 (One Real Solution) ---
        discriminant_eq_0_text = create_expression_text([("b", "2"), "-", "4ac", "=", "0"], color=GOLD_ACCENT).to_edge(UP)
        result_eq_0 = Text("One Real Solution", color=BLUE_ACCENT).next_to(discriminant_eq_0_text, DOWN, buff=0.5)

        self.play(ReplacementTransform(discriminant_gt_0_text, discriminant_eq_0_text),
                  ReplacementTransform(result_gt_0, result_eq_0))
        self.wait(0.5)

        parabola_eq_0 = axes.plot(lambda x: 0.5 * x**2, x_range=[-3.5, 3.5], color=BLUE_ACCENT)
        dot_eq_0 = Dot(axes.c2p(0, 0), color=GOLD_ACCENT)

        self.play(Create(parabola_eq_0))
        self.play(Create(dot_eq_0))
        self.wait(1.5)

        self.play(FadeOut(parabola_eq_0), FadeOut(dot_eq_0))

        # --- Beat 5: Case 3 - Discriminant < 0 (No Real Solutions) ---
        discriminant_lt_0_text = create_expression_text([("b", "2"), "-", "4ac", "<", "0"], color=GOLD_ACCENT).to_edge(UP)
        result_lt_0 = Text("No Real Solutions", color=BLUE_ACCENT).next_to(discriminant_lt_0_text, DOWN, buff=0.5)

        self.play(ReplacementTransform(discriminant_eq_0_text, discriminant_lt_0_text),
                  ReplacementTransform(result_eq_0, result_lt_0))
        self.wait(0.5)

        parabola_lt_0 = axes.plot(lambda x: 0.5 * x**2 + 2, x_range=[-3.5, 3.5], color=BLUE_ACCENT)

        self.play(Create(parabola_lt_0))
        self.wait(1.5)

        self.play(FadeOut(parabola_lt_0), FadeOut(axes), FadeOut(axes_label_x), FadeOut(axes_label_y))

        # --- Recap Card ---
        self.play(FadeOut(discriminant_lt_0_text, shift=UP), FadeOut(result_lt_0, shift=UP))

        recap_title = Text("The Discriminant", color=GOLD_ACCENT).scale(1.2).to_edge(UP)
        
        recap_line1_disc = create_expression_text([("b", "2"), "-", "4ac"], color=LIGHT_TEXT)
        recap_line1_text = Text(" > 0 means Two Real Solutions", color=BLUE_ACCENT).next_to(recap_line1_disc, RIGHT)
        recap_line1 = VGroup(recap_line1_disc, recap_line1_text).arrange(RIGHT, buff=0.2).next_to(recap_title, DOWN, buff=0.8).shift(LEFT*1.5)

        recap_line2_disc = create_expression_text([("b", "2"), "-", "4ac"], color=LIGHT_TEXT)
        recap_line2_text = Text(" = 0 means One Real Solution", color=BLUE_ACCENT).next_to(recap_line2_disc, RIGHT)
        recap_line2 = VGroup(recap_line2_disc, recap_line2_text).arrange(RIGHT, buff=0.2).next_to(recap_line1, DOWN, buff=0.5).shift(LEFT*1.5)
        
        recap_line3_disc = create_expression_text([("b", "2"), "-", "4ac"], color=LIGHT_TEXT)
        recap_line3_text = Text(" < 0 means No Real Solutions", color=BLUE_ACCENT).next_to(recap_line3_disc, RIGHT)
        recap_line3 = VGroup(recap_line3_disc, recap_line3_text).arrange(RIGHT, buff=0.2).next_to(recap_line2, DOWN, buff=0.5).shift(LEFT*1.5)

        recap_vgroup = VGroup(recap_title, recap_line1, recap_line2, recap_line3)
        recap_vgroup.center()

        self.play(Write(recap_title))
        self.play(LaggedStart(
            Write(recap_line1),
            Write(recap_line2),
            Write(recap_line3),
            lag_ratio=0.7
        ))
        self.wait(3)
        self.play(FadeOut(recap_vgroup))