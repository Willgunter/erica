from manim import *

class GeometricMeaningAndDiscriminant(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK

        # Define custom colors for 3Blue1Brown-inspired style
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C
        GREY_AXIS = GREY_D
        LIGHT_TEXT = WHITE
        HIGHLIGHT_RED = RED_C

        # --- Beat 1: Visual Hook & Introduction (Two Roots) ---
        title_text = Text("Geometric Meaning of Roots", font_size=48, color=LIGHT_TEXT)
        title_text.to_edge(UP, buff=0.7)
        self.play(FadeIn(title_text, shift=UP))
        self.wait(0.5)

        # Create Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GREY_AXIS, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-3, -1, 1, 3]},
            y_axis_config={"numbers_to_include": [-4, -2, 2, 4]}
        ).shift(DOWN * 0.5)
        self.play(Create(axes, run_time=1.5))

        # Define a default quadratic function (two real roots)
        def func_two_roots(x):
            return 0.5 * (x - 3) * (x + 1) # y = 0.5x^2 - x - 1.5

        parabola_two_roots = axes.plot(func_two_roots, color=BLUE_ACCENT, stroke_width=4)
        
        # Mark roots
        root_1_coord = axes.c2p(-1, 0)
        root_2_coord = axes.c2p(3, 0)
        
        root_point_1 = Dot(root_1_coord, color=GOLD_ACCENT, radius=0.1)
        root_point_2 = Dot(root_2_coord, color=GOLD_ACCENT, radius=0.1)

        root_line_1 = DashedLine(root_1_coord + UP * 0.5, root_1_coord + DOWN * 0.5, color=GOLD_ACCENT)
        root_line_2 = DashedLine(root_2_coord + UP * 0.5, root_2_coord + DOWN * 0.5, color=GOLD_ACCENT)

        parabola_desc = Text("Where the graph crosses the X-axis.", font_size=32, color=LIGHT_TEXT)
        parabola_desc.next_to(axes, DOWN, buff=0.7)

        self.play(
            Create(parabola_two_roots),
            FadeIn(root_point_1, scale=0.5),
            FadeIn(root_point_2, scale=0.5),
            Create(root_line_1),
            Create(root_line_2),
            run_time=2
        )
        self.play(Write(parabola_desc))
        self.wait(1.5)

        # --- Beat 2: Varying 'c' - Transition to different root scenarios ---
        self.play(FadeOut(parabola_desc), FadeOut(root_line_1), FadeOut(root_line_2), FadeOut(root_point_1), FadeOut(root_point_2))
        
        # Construct general quadratic equation using Text objects
        eq_a = Text("a", font_size=36, color=GOLD_ACCENT)
        eq_x2 = Text("x", font_size=36, color=LIGHT_TEXT)
        eq_sup2 = Text("2", font_size=24, color=LIGHT_TEXT)
        eq_plus_b = Text(" + b", font_size=36, color=LIGHT_TEXT)
        eq_x = Text("x", font_size=36, color=LIGHT_TEXT)
        eq_plus_c = Text(" + c", font_size=36, color=BLUE_ACCENT)
        eq_equals_0 = Text(" = 0", font_size=36, color=LIGHT_TEXT)

        # Manual arrangement to handle superscript
        eq_a.move_to(ORIGIN)
        eq_x2.next_to(eq_a, RIGHT, buff=0.05)
        eq_sup2.next_to(eq_x2, UP + RIGHT, buff=0.05).shift(RIGHT * 0.05)
        eq_plus_b.next_to(eq_x2, RIGHT, buff=0.15)
        eq_x.next_to(eq_plus_b, RIGHT, buff=0.15)
        eq_plus_c.next_to(eq_x, RIGHT, buff=0.15)
        eq_equals_0.next_to(eq_plus_c, RIGHT, buff=0.15)
        
        general_quadratic_eq = VGroup(eq_a, eq_x2, eq_sup2, eq_plus_b, eq_x, eq_plus_c, eq_equals_0)
        general_quadratic_eq.move_to(title_text.get_center())

        self.play(Transform(title_text, general_quadratic_eq), run_time=1.0)
        self.wait(0.5)

        c_label = Text("Changing 'c'", font_size=28, color=BLUE_ACCENT)
        c_label.next_to(general_quadratic_eq, DOWN, buff=0.5)
        c_arrow = Arrow(c_label.get_bottom(), eq_plus_c.get_top(), buff=0.1, color=BLUE_ACCENT)

        self.play(FadeIn(c_label, shift=UP), Create(c_arrow))
        self.wait(0.5)
        
        parabola_current = parabola_two_roots # Track the parabola being transformed
        
        # Case 1 (initial state, implicit two roots)
        # No transformation needed as it's the current state. Just wait.
        self.wait(0.5)

        # Case 2: One root (tangent) by changing 'c'
        def func_one_root(x):
            return 0.5 * (x - 1)**2  # y = 0.5x^2 - x + 0.5 (c=0.5)
        parabola_one_root = axes.plot(func_one_root, color=BLUE_ACCENT, stroke_width=4)
        root_point_one = Dot(axes.c2p(1, 0), color=GOLD_ACCENT, radius=0.1)

        self.play(
            Transform(parabola_current, parabola_one_root),
            FadeIn(root_point_one),
            run_time=1.5
        )
        self.wait(1)

        # Case 3: No real roots by changing 'c' further
        def func_no_roots(x):
            return 0.5 * (x - 1)**2 + 2 # y = 0.5x^2 - x + 2.5 (c=2.5)
        parabola_no_roots = axes.plot(func_no_roots, color=BLUE_ACCENT, stroke_width=4)

        self.play(
            Transform(parabola_current, parabola_no_roots),
            FadeOut(root_point_one),
            run_time=1.5
        )
        self.wait(1)
        
        self.play(FadeOut(c_label, c_arrow))

        # --- Beat 3: Introduce the Discriminant ---
        discriminant_expl = Text("This part tells us how many roots!", font_size=32, color=LIGHT_TEXT)
        discriminant_expl.next_to(axes, DOWN, buff=0.7)

        # Construct the quadratic formula using Text objects (no Tex/MathTex)
        qf_minus_b = Text("-b", font_size=32, color=LIGHT_TEXT)
        qf_pm = Text(" +/- ", font_size=32, color=LIGHT_TEXT)
        qf_sqrt_start = Text("sqrt(", font_size=32, color=LIGHT_TEXT) 
        qf_b2 = Text("b", font_size=32, color=GOLD_ACCENT)
        qf_b2_sup = Text("2", font_size=20, color=GOLD_ACCENT)
        qf_minus_4ac = Text(" - 4ac", font_size=32, color=GOLD_ACCENT)
        qf_sqrt_end = Text(")", font_size=32, color=LIGHT_TEXT) 
        qf_2a = Text("2a", font_size=32, color=LIGHT_TEXT)

        # Manual positioning for numerator elements
        qf_b2_sup.next_to(qf_b2, UP + RIGHT, buff=0.05).shift(RIGHT * 0.05)
        
        # Place elements explicitly to simulate alignment
        numerator_part_1 = VGroup(qf_minus_b, qf_pm, qf_sqrt_start)
        numerator_part_2 = VGroup(qf_b2, qf_b2_sup, qf_minus_4ac)
        numerator_part_3 = qf_sqrt_end

        numerator_part_1.arrange(RIGHT, buff=0.05)
        numerator_part_2.arrange(RIGHT, buff=0.05)
        
        qf_sqrt_start.next_to(numerator_part_1.get_right(), RIGHT, buff=0.05)
        numerator_part_2.next_to(qf_sqrt_start, RIGHT, buff=0.05)
        numerator_part_3.next_to(numerator_part_2, RIGHT, buff=0.05)

        # Combine all parts into a single VGroup for the numerator
        numerator = VGroup(numerator_part_1, numerator_part_2, numerator_part_3).arrange(RIGHT, buff=0)
        numerator.move_to(ORIGIN) # Center the entire numerator

        qf_line = Line(LEFT * (numerator.width / 2 + 0.2), RIGHT * (numerator.width / 2 + 0.2), color=LIGHT_TEXT, stroke_width=2)
        denominator = qf_2a
        
        # Arrange numerator, line, and denominator
        quadratic_formula_vg = VGroup(numerator, qf_line, denominator).arrange(DOWN, buff=0.1)
        
        qf_line.width = numerator.width * 1.1 
        qf_line.move_to(VGroup(numerator, denominator).get_center())
        qf_line.shift(DOWN * 0.15) 
        denominator.next_to(qf_line, DOWN, buff=0.1)

        quadratic_formula_vg.scale(0.8)
        quadratic_formula_vg.next_to(parabola_current, LEFT, buff=1.0).to_edge(LEFT, buff=0.5)

        # Move general equation to top-right
        self.play(
            general_quadratic_eq.animate.to_edge(UP).shift(RIGHT * 3),
            FadeIn(quadratic_formula_vg, shift=LEFT),
            run_time=1.5
        )
        self.wait(0.5)

        discriminant_group_elements = VGroup(qf_b2, qf_b2_sup, qf_minus_4ac)
        
        discriminant_label = Text("Discriminant", font_size=36, color=GOLD_ACCENT)
        discriminant_label.next_to(discriminant_group_elements, UP, buff=0.5)
        discriminant_arrow = Arrow(discriminant_label.get_bottom(), discriminant_group_elements.get_top(), buff=0.1, color=GOLD_ACCENT)

        self.play(
            LaggedStart(
                Indicate(discriminant_group_elements, scale_factor=1.2, color=GOLD_ACCENT),
                Write(discriminant_label),
                Create(discriminant_arrow),
                lag_ratio=0.5
            )
        )
        self.play(Write(discriminant_expl))
        self.wait(1.5)

        self.play(
            FadeOut(discriminant_expl),
            FadeOut(discriminant_arrow),
            FadeOut(discriminant_label),
            FadeOut(quadratic_formula_vg),
            FadeOut(general_quadratic_eq),
            FadeOut(parabola_current),
            FadeOut(axes),
            run_time=1.5
        )

        # --- Case display helper function ---
        # This will simplify creating the discriminant conditions and results
        def create_discriminant_expression(symbol_str):
            b_text = Text("b", font_size=40, color=GOLD_ACCENT)
            b_sup = Text("2", font_size=28, color=GOLD_ACCENT)
            minus_4ac_text = Text(" - 4ac", font_size=40, color=GOLD_ACCENT)
            symbol_text = Text(symbol_str, font_size=40, color=GOLD_ACCENT)

            b_sup.next_to(b_text, UP + RIGHT, buff=0.05).shift(RIGHT * 0.05)
            
            # Manual positioning within VGroup
            b_text.move_to(ORIGIN)
            minus_4ac_text.next_to(b_text, RIGHT, buff=0.15).shift(RIGHT * 0.6) 
            symbol_text.next_to(minus_4ac_text, RIGHT, buff=0.15)
            
            condition_group = VGroup(b_text, b_sup, minus_4ac_text, symbol_text)
            condition_group.move_to(ORIGIN) # Center the VGroup after individual adjustments
            
            return condition_group

        # --- Beat 4: Case 1: Discriminant > 0 (Two Real Roots) ---
        d_gt_0_condition = create_discriminant_expression("> 0")
        d_gt_0_condition.to_edge(UP, buff=0.7)
        d_gt_0_result = Text("Two distinct real roots", font_size=36, color=LIGHT_TEXT)
        d_gt_0_result.next_to(d_gt_0_condition, DOWN, buff=0.7)

        self.play(FadeIn(d_gt_0_condition, shift=UP))
        self.play(Write(d_gt_0_result))
        self.wait(0.5)

        # Re-create axes for the cases
        axes_case = Axes(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=8, y_length=4,
            axis_config={"color": GREY_AXIS, "stroke_width": 2}
        ).shift(DOWN * 0.5)
        parabola_case = axes_case.plot(func_two_roots, color=BLUE_ACCENT, stroke_width=4)
        
        root_point_1_case = Dot(axes_case.c2p(-1, 0), color=GOLD_ACCENT, radius=0.1)
        root_point_2_case = Dot(axes_case.c2p(3, 0), color=GOLD_ACCENT, radius=0.1)

        self.play(
            Create(axes_case),
            Create(parabola_case),
            FadeIn(root_point_1_case),
            FadeIn(root_point_2_case),
            run_time=2
        )
        self.wait(1.5)

        self.play(
            FadeOut(root_point_1_case), FadeOut(root_point_2_case)
        )

        # --- Beat 5: Case 2: Discriminant = 0 (One Real Root) ---
        d_eq_0_condition = create_discriminant_expression("= 0")
        d_eq_0_condition.to_edge(UP, buff=0.7)
        d_eq_0_result = Text("One repeated real root", font_size=36, color=LIGHT_TEXT)
        d_eq_0_result.next_to(d_eq_0_condition, DOWN, buff=0.7)

        self.play(
            ReplacementTransform(d_gt_0_condition, d_eq_0_condition),
            ReplacementTransform(d_gt_0_result, d_eq_0_result)
        )
        self.wait(0.5)

        parabola_case_one_root = axes_case.plot(func_one_root, color=BLUE_ACCENT, stroke_width=4)
        root_point_case_one = Dot(axes_case.c2p(1, 0), color=GOLD_ACCENT, radius=0.1)

        self.play(
            Transform(parabola_case, parabola_case_one_root),
            FadeIn(root_point_case_one),
            run_time=1.5
        )
        self.wait(1.5)

        self.play(
            FadeOut(root_point_case_one)
        )

        # --- Beat 6: Case 3: Discriminant < 0 (No Real Roots) ---
        d_lt_0_condition = create_discriminant_expression("< 0")
        d_lt_0_condition.to_edge(UP, buff=0.7)
        d_lt_0_result = Text("No real roots", font_size=36, color=LIGHT_TEXT)
        d_lt_0_result.next_to(d_lt_0_condition, DOWN, buff=0.7)

        self.play(
            ReplacementTransform(d_eq_0_condition, d_lt_0_condition),
            ReplacementTransform(d_eq_0_result, d_lt_0_result)
        )
        self.wait(0.5)

        parabola_case_no_roots = axes_case.plot(func_no_roots, color=BLUE_ACCENT, stroke_width=4)
        
        # Add a subtle "no intersection" visual
        no_roots_x_mark = VGroup(
            Line(axes_case.c2p(-1.5, 0.5), axes_case.c2p(1.5, -0.5), color=HIGHLIGHT_RED, stroke_width=4),
            Line(axes_case.c2p(-1.5, -0.5), axes_case.c2p(1.5, 0.5), color=HIGHLIGHT_RED, stroke_width=4)
        ).scale(0.8).next_to(parabola_case_no_roots, DOWN, buff=0.2).set_opacity(0.7)

        self.play(
            Transform(parabola_case, parabola_case_no_roots),
            FadeIn(no_roots_x_mark),
            run_time=1.5
        )
        self.wait(1.5)

        self.play(
            FadeOut(axes_case), FadeOut(parabola_case),
            FadeOut(no_roots_x_mark), FadeOut(d_lt_0_condition), FadeOut(d_lt_0_result)
        )

        # --- Beat 7: Recap Card ---
        recap_title = Text("Recap: The Discriminant", font_size=48, color=LIGHT_TEXT)
        recap_title.to_edge(UP, buff=0.7)
        self.play(FadeIn(recap_title, shift=UP))

        # Case 1 recap
        recap_d1_condition = create_discriminant_expression("> 0")
        recap_d1_result = Text("Two distinct real roots", font_size=32, color=BLUE_ACCENT)
        recap_d1 = VGroup(recap_d1_condition, recap_d1_result).arrange(RIGHT, buff=0.8)

        # Case 2 recap
        recap_d2_condition = create_discriminant_expression("= 0")
        recap_d2_result = Text("One repeated real root", font_size=32, color=BLUE_ACCENT)
        recap_d2 = VGroup(recap_d2_condition, recap_d2_result).arrange(RIGHT, buff=0.8)

        # Case 3 recap
        recap_d3_condition = create_discriminant_expression("< 0")
        recap_d3_result = Text("No real roots", font_size=32, color=BLUE_ACCENT)
        recap_d3 = VGroup(recap_d3_condition, recap_d3_result).arrange(RIGHT, buff=1.0)

        recap_group = VGroup(recap_d1, recap_d2, recap_d3).arrange(DOWN, buff=0.7)
        recap_group.next_to(recap_title, DOWN, buff=1.0)
        
        self.play(LaggedStart(
            FadeIn(recap_d1, shift=LEFT),
            FadeIn(recap_d2, shift=LEFT),
            FadeIn(recap_d3, shift=LEFT),
            lag_ratio=0.5
        ))
        self.wait(3)

        self.play(FadeOut(VGroup(recap_title, recap_group)))
        self.wait(0.5)