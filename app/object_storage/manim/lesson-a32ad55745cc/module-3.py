from manim import *

class QuadraticFormulaTrick(Scene):
    def construct(self):
        # 0. Configuration and Colors
        config.background_color = "#1A1A1A" # Dark grey/black
        BLUE_ACCENT = BLUE_E # Darker blue for accents
        GOLD_ACCENT = GOLD_E # Darker gold for accents
        WHITE_TEXT = WHITE # For general text

        self.camera.background_color = config.background_color # Ensure background color is set for the scene

        # Title for the whole animation
        title = Text("Quadratic Formula: The Algebraic Trick", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Beat 1: The Parabola and its Symmetry (Visual Hook + Intuition)
        # ------------------------------------------------------------------
        beat1_text = Text("Understanding the roots' symmetry.", font_size=36, color=WHITE_TEXT).next_to(title, DOWN, buff=0.8)
        self.play(Write(beat1_text))
        self.wait(0.5)

        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2.5, 8, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": GREY_B, "include_numbers": False},
        ).scale(0.8).to_edge(DOWN)
        labels = axes.get_axis_labels(x_label="x", y_label="y").set_color(GREY_B)

        # Sample parabola: y = 0.5 * (x - 1.5)^2 - 2
        # Vertex at (1.5, -2)
        # Roots: 0.5 * (x - 1.5)^2 = 2 => (x - 1.5)^2 = 4 => x - 1.5 = +/- 2
        # Roots at x = -0.5 and x = 3.5
        parabola_func = lambda x: 0.5 * (x - 1.5)**2 - 2
        parabola = axes.get_graph(parabola_func, x_range=[-3, 6], color=BLUE_ACCENT)

        root1_val, root2_val = -0.5, 3.5
        dot_root1 = Dot(axes.coords_to_point(root1_val, 0), color=GOLD_ACCENT, radius=0.1)
        dot_root2 = Dot(axes.coords_to_point(root2_val, 0), color=GOLD_ACCENT, radius=0.1)
        dot_vertex = Dot(axes.coords_to_point(1.5, parabola_func(1.5)), color=WHITE_TEXT, radius=0.1)
        
        self.play(
            Create(axes),
            Write(labels),
            Create(parabola),
            FadeIn(dot_root1, dot_root2, dot_vertex),
            run_time=2
        )
        self.wait(1)

        # Axis of Symmetry (midpoint between roots, or x-coord of vertex)
        axis_sym_val = 1.5
        axis_of_sym = DashedLine(
            axes.coords_to_point(axis_sym_val, axes.y_range[0]),
            axes.coords_to_point(axis_sym_val, axes.y_range[1]),
            color=GOLD_ACCENT
        )
        sym_label = MathTex("x = p", color=GOLD_ACCENT, font_size=32).next_to(axis_of_sym, RIGHT, buff=0.2)
        
        self.play(Create(axis_of_sym), Write(sym_label))
        self.wait(0.5)

        # Highlight equidistant roots
        arrow1 = Arrow(axes.coords_to_point(axis_sym_val, 0), dot_root1.get_center(), buff=0.1, color=WHITE_TEXT, max_stroke_width_to_length_ratio=0.08)
        arrow2 = Arrow(axes.coords_to_point(axis_sym_val, 0), dot_root2.get_center(), buff=0.1, color=WHITE_TEXT, max_stroke_width_to_length_ratio=0.08)
        d_label = MathTex("d", color=WHITE_TEXT, font_size=30).next_to(arrow2, UP, buff=0.1)
        
        self.play(Create(arrow1), Create(arrow2), Write(d_label))
        self.wait(1)

        roots_concept = MathTex(
            "\\text{Roots: } x = p \\pm d",
            color=WHITE_TEXT,
            font_size=40
        ).next_to(sym_label, RIGHT, buff=1.0)
        self.play(Write(roots_concept))
        self.wait(2)

        # Clean up for next beat
        self.play(
            FadeOut(axes, labels, parabola, dot_root1, dot_root2, dot_vertex, axis_of_sym, sym_label, arrow1, arrow2, d_label, roots_concept, beat1_text),
            title.animate.to_corner(UL).scale(0.7)
        )
        self.wait(0.5)

        # Beat 2: Setting up the "Trick" (Deriving from (x - (p+d))(x - (p-d)) = 0)
        # --------------------------------------------------------------------------
        beat2_text = Text("Algebraically, this means:", color=WHITE_TEXT).next_to(title, DOWN, buff=0.8)
        self.play(Write(beat2_text))
        self.wait(0.5)

        eq1 = MathTex(
            "(x - (p+d))(x - (p-d)) = 0",
            color=WHITE_TEXT
        ).next_to(beat2_text, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1)

        eq2 = MathTex(
            "(x - p - d)(x - p + d) = 0",
            color=WHITE_TEXT
        ).next_to(eq1, DOWN)
        self.play(ReplacementTransform(eq1, eq2))
        self.wait(1)

        eq3_diff_sq = MathTex(
            "(x-p)^2 - d^2 = 0", # Use (A-B)(A+B) = A^2 - B^2 where A=(x-p), B=d
            color=WHITE_TEXT
        ).next_to(eq2, DOWN)
        self.play(ReplacementTransform(eq2, eq3_diff_sq))
        self.wait(1)

        eq4_expanded = MathTex(
            "x^2 - 2px + p^2 - d^2 = 0",
            color=WHITE_TEXT
        ).next_to(eq3_diff_sq, DOWN)
        self.play(ReplacementTransform(eq3_diff_sq, eq4_expanded))
        self.wait(2)

        # Clean up for next beat
        self.play(FadeOut(beat2_text))
        self.wait(0.5)

        # Beat 3: Connecting to the General Formula (ax^2 + bx + c = 0)
        # --------------------------------------------------------------
        beat3_text = Text("Compare with the general quadratic form:", color=WHITE_TEXT).next_to(title, DOWN, buff=0.8)
        self.play(Write(beat3_text))
        self.wait(1)

        general_quadratic = MathTex(
            "ax^2 + bx + c = 0",
            color=BLUE_ACCENT
        ).next_to(beat3_text, DOWN, buff=0.5)
        self.play(Write(general_quadratic))
        self.wait(1)

        divide_a_text = Text("Divide by 'a':", color=WHITE_TEXT, font_size=30).next_to(general_quadratic, RIGHT, buff=0.5)
        normalized_quadratic = MathTex(
            "x^2 + {b \\over a}x + {c \\over a} = 0",
            color=BLUE_ACCENT
        ).next_to(general_quadratic, DOWN, buff=0.5).align_to(general_quadratic, LEFT)
        
        self.play(
            Write(divide_a_text),
            run_time=0.5
        )
        self.play(
            ReplacementTransform(general_quadratic, normalized_quadratic),
            FadeOut(divide_a_text)
        )
        self.wait(1)

        # Align our expanded form and the normalized form for comparison
        self.play(
            eq4_expanded.animate.next_to(normalized_quadratic, DOWN, buff=0.5).align_to(normalized_quadratic, LEFT)
        )
        self.wait(1)

        # Identify 'p'
        identify_p_text = Text("Identify 'p' (axis of symmetry):", color=WHITE_TEXT, font_size=30).next_to(normalized_quadratic, RIGHT, buff=1.5).align_to(normalized_quadratic, UP)
        self.play(Write(identify_p_text))

        highlight_2p = SurroundingRectangle(eq4_expanded.get_part_by_tex("-2px"), color=GOLD_ACCENT, buff=0.1)
        highlight_b_over_a = SurroundingRectangle(normalized_quadratic.get_part_by_tex("{b \\over a}x"), color=GOLD_ACCENT, buff=0.1)
        self.play(Create(highlight_2p), Create(highlight_b_over_a))
        self.wait(1)

        p_relation = MathTex(
            "-2p = {b \\over a}",
            color=GOLD_ACCENT
        ).next_to(identify_p_text, DOWN, buff=0.5)
        self.play(Write(p_relation))
        self.wait(0.5)

        p_result = MathTex(
            "p = -{b \\over {2a}}",
            color=GOLD_ACCENT
        ).next_to(p_relation, DOWN, buff=0.5)
        self.play(TransformMatchingTex(p_relation, p_result))
        self.wait(1.5)
        self.play(FadeOut(highlight_2p, highlight_b_over_a))

        # Identify 'd'
        identify_d_text = Text("Identify 'd' (distance to roots):", color=WHITE_TEXT, font_size=30).next_to(p_result, RIGHT, buff=1.5).align_to(p_result, UP)
        self.play(Write(identify_d_text))
        
        highlight_c_over_a = SurroundingRectangle(normalized_quadratic.get_part_by_tex("{c \\over a}"), color=BLUE_ACCENT, buff=0.1)
        highlight_p_sq_d_sq = SurroundingRectangle(eq4_expanded.get_part_by_tex("p^2 - d^2"), color=BLUE_ACCENT, buff=0.1)
        self.play(Create(highlight_c_over_a), Create(highlight_p_sq_d_sq))
        self.wait(1)

        d_relation = MathTex(
            "p^2 - d^2 = {c \\over a}",
            color=BLUE_ACCENT
        ).next_to(identify_d_text, DOWN, buff=0.5)
        self.play(Write(d_relation))
        self.wait(1)

        solve_d_sq = MathTex(
            "d^2 = p^2 - {c \\over a}",
            color=BLUE_ACCENT
        ).next_to(d_relation, DOWN, buff=0.5)
        self.play(TransformMatchingTex(d_relation, solve_d_sq))
        self.wait(1)

        sub_p_text = Text("Substitute p:", font_size=30, color=WHITE_TEXT).next_to(solve_d_sq, RIGHT, buff=0.5)
        self.play(Write(sub_p_text))
        
        d_sq_sub_p = MathTex(
            "d^2 = \\left(-{b \\over {2a}}\\right)^2 - {c \\over a}",
            color=BLUE_ACCENT
        ).next_to(solve_d_sq, DOWN, buff=0.5).align_to(solve_d_sq, LEFT)
        self.play(TransformMatchingTex(solve_d_sq, d_sq_sub_p))
        self.wait(1)

        d_sq_simplify1 = MathTex(
            "d^2 = {b^2 \\over {4a^2}} - {4ac \\over {4a^2}}", # Common denominator
            color=BLUE_ACCENT
        ).next_to(d_sq_sub_p, DOWN, buff=0.5).align_to(d_sq_sub_p, LEFT)
        self.play(TransformMatchingTex(d_sq_sub_p, d_sq_simplify1))
        self.wait(1)

        d_sq_simplify2 = MathTex(
            "d^2 = {b^2 - 4ac \\over {4a^2}}",
            color=BLUE_ACCENT
        ).next_to(d_sq_simplify1, DOWN, buff=0.5).align_to(d_sq_simplify1, LEFT)
        self.play(TransformMatchingTex(d_sq_simplify1, d_sq_simplify2))
        self.wait(1.5)

        d_result = MathTex(
            "d = \\pm {\\sqrt{b^2 - 4ac} \\over {2a}}",
            color=BLUE_ACCENT
        ).next_to(d_sq_simplify2, DOWN, buff=0.5).align_to(d_sq_simplify2, LEFT)
        self.play(TransformMatchingTex(d_sq_simplify2, d_result))
        self.wait(2)

        # Clean up for next beat
        self.play(
            FadeOut(beat3_text, normalized_quadratic, eq4_expanded,
                    identify_p_text, identify_d_text, highlight_c_over_a, highlight_p_sq_d_sq,
                    sub_p_text)
        )
        self.wait(0.5)

        # Beat 4: The Full Formula and its Intuition
        # ------------------------------------------
        beat4_text = Text("Putting it all together: $x = p \\pm d$", color=WHITE_TEXT).next_to(title, DOWN, buff=0.8)
        self.play(Write(beat4_text))
        self.wait(1)

        self.play(
            VGroup(p_result, d_result).animate.center().arrange(RIGHT, buff=1.5).shift(UP*1.5)
        )
        self.wait(1)

        # Show the substitution into x = p +/- d
        final_formula_plugged = MathTex(
            "x = ", 
            "{-b \\over {2a}}",  # Placeholder for p_result
            " \\pm ", 
            "{\\sqrt{b^2 - 4ac} \\over {2a}}", # Placeholder for d_result
            substrings_to_isolate=["{-b \\over {2a}}", "{\\sqrt{b^2 - 4ac} \\over {2a}}"],
            color=GOLD_ACCENT, font_size=64
        ).next_to(VGroup(p_result, d_result), DOWN, buff=1.0)
        
        # Transform p_result and d_result into their respective positions
        self.play(
            Transform(p_result, final_formula_plugged.get_part_by_tex("{-b \\over {2a}}")),
            Transform(d_result, final_formula_plugged.get_part_by_tex("{\\sqrt{b^2 - 4ac} \\over {2a}}")),
            Write(final_formula_plugged.get_part_by_tex("x = ")),
            Write(final_formula_plugged.get_part_by_tex("\\pm")),
            run_time=2
        )
        self.wait(1)

        # Combine into a single fraction
        final_formula_grouped = MathTex(
            "x = { -b \\pm \\sqrt{b^2 - 4ac} \\over 2a }",
            color=GOLD_ACCENT, font_size=64
        ).move_to(final_formula_plugged)

        self.play(TransformMatchingTex(final_formula_plugged, final_formula_grouped))
        self.wait(2)

        # Re-emphasize intuition
        intuition_p_label = Text("Axis of Symmetry", color=GOLD_ACCENT, font_size=36).next_to(final_formula_grouped, UP, buff=1.0).shift(LEFT*2.5)
        intuition_d_label = Text("Distance to Roots", color=BLUE_ACCENT, font_size=36).next_to(final_formula_grouped, UP, buff=1.0).shift(RIGHT*2.5)
        
        arrow_p = CurvedArrow(intuition_p_label.get_bottom(), final_formula_grouped.get_part_by_tex("-b")[0].get_top(), color=GOLD_ACCENT)
        arrow_d = CurvedArrow(intuition_d_label.get_bottom(), final_formula_grouped.get_part_by_tex("\\sqrt{b^2 - 4ac}")[0].get_top(), color=BLUE_ACCENT)

        self.play(
            FadeOut(beat4_text),
            Write(intuition_p_label),
            Write(intuition_d_label),
            Create(arrow_p),
            Create(arrow_d)
        )
        self.wait(3)

        # Clean up for recap
        self.play(FadeOut(final_formula_grouped, intuition_p_label, intuition_d_label, arrow_p, arrow_d, p_result, d_result))
        self.wait(0.5)

        # Beat 5: Recap Card
        # -------------------
        self.play(title.animate.center().set_color(WHITE_TEXT).scale(1/0.7)) # Restore title to original size and center

        recap_title = Text("Recap: The Quadratic Formula Trick", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(Transform(title, recap_title)) # Transform original title into recap title

        recap_formula = MathTex(
            "x = { -b \\over 2a } \\pm { \\sqrt{b^2 - 4ac} \\over 2a }",
            font_size=60, color=WHITE_TEXT
        ).next_to(recap_title, DOWN, buff=1.0)
        self.play(Write(recap_formula))

        recap_point1 = Text(
            "1. Roots are symmetric about an axis.",
            font_size=36, color=WHITE_TEXT
        ).next_to(recap_formula, DOWN, buff=0.8).align_to(recap_formula, LEFT)
        recap_point2 = MathTex(
            "2. \\text{Axis of Symmetry: } p = -{b \\over 2a}",
            font_size=36, color=GOLD_ACCENT
        ).next_to(recap_point1, DOWN, buff=0.3).align_to(recap_formula, LEFT)
        recap_point3 = MathTex(
            "3. \\text{Distance to Roots: } d = {\\sqrt{b^2 - 4ac} \\over 2a}",
            font_size=36, color=BLUE_ACCENT
        ).next_to(recap_point2, DOWN, buff=0.3).align_to(recap_formula, LEFT)

        self.play(LaggedStart(
            FadeIn(recap_point1, shift=UP*0.5),
            FadeIn(recap_point2, shift=UP*0.5),
            FadeIn(recap_point3, shift=UP*0.5),
            lag_ratio=0.5
        ))
        self.wait(4)

        self.play(FadeOut(title, recap_formula, recap_point1, recap_point2, recap_point3))
        self.wait(1)