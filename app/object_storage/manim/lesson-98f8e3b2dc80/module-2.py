from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Beat 0: The Problem - Roots of a Parabola (Visual Hook) ---
        title = Text("Formula Works Every Quadratic", font_size=50, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": GRAY_D},
        ).to_edge(DOWN)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        parabola_func = lambda x: x**2 - 4
        parabola = axes.get_graph(parabola_func, color=BLUE)
        
        roots_coords = [axes.coords_to_point(-2, 0), axes.coords_to_point(2, 0)]
        roots = VGroup(*[Dot(coord, color=GOLD, radius=0.1) for coord in roots_coords])

        question = Text("How do we ALWAYS find these points?", font_size=30, color=WHITE).next_to(parabola, UP, buff=0.7)

        self.play(
            Create(axes),
            Write(labels),
            Create(parabola),
            run_time=1.5
        )
        self.play(LaggedStart(*[FadeIn(root, shift=UP) for root in roots]), run_time=1)
        self.play(Write(question))
        self.wait(1.5)
        self.play(
            FadeOut(question, shift=DOWN),
            Uncreate(roots),
            Uncreate(parabola),
            FadeOut(labels),
            FadeOut(axes),
            run_time=1.5
        )
        self.play(FadeOut(title, shift=UP)) # Fade out the title as we transition to formal def

        # --- Beat 1: The Standard Form and The Condition ---
        quadratic_eq = MathTex("ax^2 + bx + c = 0", font_size=60, color=WHITE)
        
        self.play(Write(quadratic_eq))
        self.wait(1)

        a_term = quadratic_eq.get_parts_by_tex("a")[0] # Get 'a' from ax^2
        condition = MathTex("a \\neq 0", font_size=40, color=GOLD).next_to(quadratic_eq, DOWN, buff=0.5)

        self.play(
            Indicate(a_term, color=BLUE),
            Write(condition)
        )
        
        brief_explanation = Text("If a=0, it's a line, not a parabola.", font_size=24, color=GRAY).next_to(condition, DOWN)
        self.play(FadeIn(brief_explanation, shift=UP))
        self.wait(2)
        self.play(
            FadeOut(brief_explanation),
            FadeOut(condition),
            FadeOut(quadratic_eq, shift=UP)
        )

        # --- Beat 2: Roots are X-intercepts on the Graph ---
        axes_beat2 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": GRAY_D},
        ).to_edge(DOWN)
        labels_beat2 = axes_beat2.get_axis_labels(x_label="x", y_label="y")

        parabola_func_2 = lambda x: -0.5 * x**2 + x + 4 # Example parabola
        parabola_2 = axes_beat2.get_graph(parabola_func_2, color=BLUE)

        roots_coords_2 = [
            axes_beat2.coords_to_point(-2, 0), # Root 1
            axes_beat2.coords_to_point(4, 0)   # Root 2
        ]
        
        roots_beat2 = VGroup(*[Dot(coord, color=GOLD, radius=0.1) for coord in roots_coords_2])

        explanation_roots = Text("The 'roots' are where y = 0", font_size=30, color=WHITE).to_edge(UP)
        x_values_text = MathTex("x_1, x_2", font_size=40, color=GOLD).next_to(roots_beat2, RIGHT, buff=0.5)

        self.play(
            Create(axes_beat2),
            Write(labels_beat2),
            Create(parabola_2),
            FadeIn(explanation_roots, shift=UP)
        )
        self.play(
            LaggedStart(*[FadeIn(root, shift=UP) for root in roots_beat2]),
            Write(x_values_text),
            run_time=2
        )
        self.wait(2)
        self.play(
            FadeOut(explanation_roots),
            FadeOut(x_values_text),
            Uncreate(roots_beat2)
        )

        # --- Beat 3: The Axis of Symmetry ---
        # Keep parabola_2, axes_beat2, labels_beat2
        axis_of_sym_x = 1 # For parabola_func_2: x = -b/(2a) = -1/(2*-0.5) = 1
        
        axis_line = axes_beat2.get_vertical_line(axes_beat2.coords_to_point(axis_of_sym_x, 0), color=BLUE, line_arg_dict={"stroke_dash_offset": 0.5, "dashed_ratio": 0.1})
        
        center_text = Text("The center point:", font_size=30, color=WHITE).to_edge(UP)
        formula_center = MathTex("x = -\\frac{b}{2a}", font_size=45, color=BLUE).next_to(axis_line, RIGHT, buff=0.7)
        
        self.play(FadeIn(center_text, shift=UP))
        self.play(Create(axis_line))
        self.play(Write(formula_center))
        self.wait(2)
        self.play(FadeOut(center_text))

        # --- Beat 4: The Offset from the Center ---
        # Keep parabola_2, axes_beat2, labels_beat2, axis_line
        offset_text = Text("And a symmetric distance:", font_size=30, color=WHITE).to_edge(UP)

        root1_point = axes_beat2.coords_to_point(-2, 0)
        root2_point = axes_beat2.coords_to_point(4, 0)
        center_point_on_x_axis = axes_beat2.coords_to_point(axis_of_sym_x, 0)

        arrow1 = Arrow(center_point_on_x_axis, root1_point, color=GOLD, buff=0.1)
        arrow2 = Arrow(center_point_on_x_axis, root2_point, color=GOLD, buff=0.1)
        
        formula_offset = MathTex("\\pm \\frac{\\sqrt{b^2 - 4ac}}{2a}", font_size=45, color=GOLD).next_to(arrow2, UP, buff=0.5)

        self.play(FadeIn(offset_text, shift=UP))
        self.play(
            Create(arrow1),
            Create(arrow2)
        )
        self.play(Write(formula_offset))
        self.wait(2)
        self.play(FadeOut(offset_text))
        
        # --- Beat 5: The Quadratic Formula! ---
        self.play(
            FadeOut(parabola_2),
            FadeOut(labels_beat2),
            FadeOut(axes_beat2),
            FadeOut(arrow1),
            FadeOut(arrow2),
            run_time=1
        )

        # Move formula_center and formula_offset to prepare for combination
        self.play(
            formula_center.animate.center().shift(LEFT*2.5),
            formula_offset.animate.center().shift(RIGHT*2.5)
        )
        
        plus_minus = MathTex("\\pm", font_size=45, color=WHITE).move_to(ORIGIN)

        self.play(
            ReplacementTransform(axis_line, plus_minus) # axis_line becomes the plus_minus sign.
        ) 

        full_formula_parts_group = VGroup(formula_center, plus_minus, formula_offset)
        self.play(
            FadeOut(full_formula_parts_group),
            rate_func=lambda t: smooth(1-t) # Make the fadeout slightly slower at the end for clean look
        )

        final_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=80,
            color=WHITE
        ).to_edge(UP, buff=0.5)

        self.play(Write(final_formula))
        self.wait(2)

        # Highlight components: -b/(2a) as center, sqrt part as offset
        # Note: MathTex.get_parts_by_tex_to_isolate is for specific sub-expressions.
        # We can construct VGroups for visual highlighting.
        center_highlight_b = final_formula.get_parts_by_tex("-b")[0].set_color(BLUE)
        center_highlight_2a = final_formula.get_parts_by_tex("2a")[0].set_color(BLUE)
        
        offset_highlight_sqrt = final_formula.get_parts_by_tex("\\sqrt{b^2 - 4ac}")[0].set_color(GOLD)

        self.play(
            Indicate(center_highlight_b, scale_factor=1.1, color=BLUE),
            Indicate(center_highlight_2a, scale_factor=1.1, color=BLUE),
            run_time=1
        )
        self.play(
            Indicate(offset_highlight_sqrt, scale_factor=1.1, color=GOLD),
            run_time=1
        )
        self.wait(2)

        self.play(FadeOut(final_formula, shift=DOWN))


        # --- Beat 6: Recap Card ---
        recap_card = Rectangle(
            width=8, height=4.5,
            fill_opacity=0.9, color=GRAY_A, fill_color=BLACK
        ).center()

        recap_title = Text("Recap: Formula Works Every Quadratic", font_size=35, color=WHITE).to_edge(UP, buff=0.7)
        recap_eq = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", font_size=55, color=WHITE).move_to(recap_card.get_center()).shift(UP*0.5)
        
        # Using VGroup of Text/MathTex for bullet points for better control
        bp1_text = Text("- Valid for ", font_size=28, color=WHITE)
        bp1_eq1 = MathTex("ax^2 + bx + c = 0", font_size=28, color=WHITE)
        bp1_text2 = Text(" where ", font_size=28, color=WHITE)
        bp1_eq2 = MathTex("a \\neq 0", font_size=28, color=GOLD)
        bullet_point_1 = VGroup(bp1_text, bp1_eq1, bp1_text2, bp1_eq2).arrange(RIGHT, buff=0.1)

        bp2_text = Text("- Finds ", font_size=28, color=WHITE)
        bp2_highlight = Text("x-intercepts", font_size=28, color=GOLD)
        bp2_text2 = Text(" of a parabola.", font_size=28, color=WHITE)
        bullet_point_2 = VGroup(bp2_text, bp2_highlight, bp2_text2).arrange(RIGHT, buff=0.1)

        bp3_text = Text("- Center: ", font_size=28, color=WHITE)
        bp3_eq = MathTex("-\\frac{b}{2a}", font_size=28, color=BLUE)
        bullet_point_3 = VGroup(bp3_text, bp3_eq).arrange(RIGHT, buff=0.1)

        bp4_text = Text("- Offset: ", font_size=28, color=WHITE)
        bp4_eq = MathTex("\\pm \\frac{\\sqrt{b^2 - 4ac}}{2a}", font_size=28, color=GOLD)
        bullet_point_4 = VGroup(bp4_text, bp4_eq).arrange(RIGHT, buff=0.1)

        bullet_points = VGroup(
            bullet_point_1,
            bullet_point_2,
            bullet_point_3,
            bullet_point_4
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(recap_eq, DOWN, buff=0.5).to_edge(LEFT, buff=1)

        for bp in bullet_points:
            bp.shift(RIGHT * 0.5) # Adjust position to fit within card better

        self.play(FadeIn(recap_card, scale=0.8))
        self.play(
            Write(recap_title),
            Write(recap_eq),
            LaggedStart(*[FadeIn(bp, shift=LEFT) for bp in bullet_points], lag_ratio=0.3)
        )
        self.wait(4)
        self.play(
            FadeOut(recap_card),
            FadeOut(recap_title),
            FadeOut(recap_eq),
            FadeOut(bullet_points)
        )