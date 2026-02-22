from manim import *

class QuadraticEquationsIntro(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK

        blue_color = BLUE_C
        gold_color = GOLD_C
        white_color = WHITE
        grey_color = GREY_D

        # --- Beat 1: Visual Hook - The Growing Shapes (Intuition) ---
        self.camera.background_color = BLACK

        # Module Title & Subtitle
        title = Text("Quadratic Equations", font_size=50, color=white_color).to_corner(UL).shift(RIGHT*0.5)
        subtitle = Text("Form and Formula", font_size=30, color=gold_color).next_to(title, DOWN, aligned_edge=LEFT)
        self.play(Write(title), Write(subtitle), run_time=1.5)
        self.wait(0.5)

        # Initial square representing x^2
        x_label = Text("x", color=blue_color, font_size=36)
        square = Square(side_length=2, color=blue_color, fill_opacity=0.3).shift(LEFT * 2)
        x_label.next_to(square, DOWN)
        x_label_copy = x_label.copy().next_to(square, LEFT)

        area_text_x2 = Text("Area: x^2", color=white_color, font_size=30).next_to(square, RIGHT, buff=1.5)

        self.play(Create(square), Write(x_label), Write(x_label_copy), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(area_text_x2, shift=RIGHT))
        self.wait(1)

        # Add 'bx' part, forming a rectangle
        b_length = 1.5
        rectangle_b = Rectangle(width=b_length, height=2, color=gold_color, fill_opacity=0.3)
        rectangle_b.next_to(square, RIGHT, buff=0)

        b_label = Text("b", color=gold_color, font_size=36).next_to(rectangle_b, DOWN)
        area_text_bx = Text("+ bx", color=white_color, font_size=30).next_to(area_text_x2, RIGHT, buff=0.2)
        
        self.play(
            Create(rectangle_b),
            Write(b_label),
            area_text_x2.animate.shift(LEFT * (area_text_bx.width / 2 + 0.1)),
            FadeIn(area_text_bx, shift=RIGHT),
            run_time=1
        )
        self.wait(1)

        # Add 'c' part, forming a small square/rectangle
        c_val = 0.5
        square_c = Square(side_length=c_val, color=white_color, fill_opacity=0.3)
        square_c.next_to(rectangle_b, UP, buff=0.5).shift(LEFT * (b_length / 2 - c_val / 2)) 
        c_label = Text("c", color=white_color, font_size=36).next_to(square_c, UP)
        area_text_c = Text("+ c", color=white_color, font_size=30).next_to(area_text_bx, RIGHT, buff=0.2)
        
        self.play(
            Create(square_c),
            Write(c_label),
            area_text_bx.animate.shift(LEFT * (area_text_c.width / 2 + 0.1)),
            FadeIn(area_text_c, shift=RIGHT),
            run_time=1
        )
        self.wait(1.5)

        geometric_group = VGroup(square, x_label, x_label_copy, rectangle_b, b_label, square_c, c_label, area_text_x2, area_text_bx, area_text_c)
        self.play(FadeOut(geometric_group))
        self.wait(0.5)


        # --- Beat 2: The General Form ---
        
        # Manually construct "ax^2 + bx + c = 0" using Text objects
        a_text = Text("a", color=blue_color, font_size=50)
        x_text_1 = Text("x", color=white_color, font_size=50)
        exp_2 = Text("2", color=white_color, font_size=30) 
        
        plus_1 = Text("+", color=white_color, font_size=50)
        b_text = Text("b", color=gold_color, font_size=50)
        x_text_2 = Text("x", color=white_color, font_size=50)
        plus_2 = Text("+", color=white_color, font_size=50)
        c_text = Text("c", color=white_color, font_size=50)
        equals_0 = Text("= 0", color=white_color, font_size=50)

        # Position elements carefully for the equation
        x_text_1.next_to(a_text, RIGHT, buff=0.1)
        exp_2.next_to(x_text_1, UP, buff=0).align_to(x_text_1, RIGHT).shift(0.1*RIGHT + 0.1*UP)

        plus_1.next_to(x_text_1, RIGHT, buff=0.4)
        b_text.next_to(plus_1, RIGHT, buff=0.4)
        x_text_2.next_to(b_text, RIGHT, buff=0.1)
        plus_2.next_to(x_text_2, RIGHT, buff=0.4)
        c_text.next_to(plus_2, RIGHT, buff=0.4)
        equals_0.next_to(c_text, RIGHT, buff=0.4)

        general_form_group = VGroup(
            a_text, x_text_1, exp_2, plus_1, b_text, x_text_2, plus_2, c_text, equals_0
        ).move_to(ORIGIN)

        general_title_beat2 = Text("The General Form", font_size=40, color=white_color).next_to(general_form_group, UP, buff=0.8)
        
        self.play(FadeIn(general_title_beat2, shift=UP))
        self.play(
            LaggedStart(
                Write(a_text), Write(x_text_1), Write(exp_2),
                Write(plus_1),
                Write(b_text), Write(x_text_2),
                Write(plus_2),
                Write(c_text),
                Write(equals_0),
                lag_ratio=0.1,
                run_time=2
            )
        )
        self.wait(1)

        a_not_zero = Text("where a ≠ 0", color=gold_color, font_size=30).next_to(general_form_group, DOWN, buff=0.5)
        self.play(FadeIn(a_not_zero, shift=DOWN))
        self.wait(1)

        self.play(
            FadeOut(general_title_beat2),
            general_form_group.animate.to_edge(UP).shift(DOWN * 0.5),
            FadeOut(a_not_zero),
            FadeOut(title), FadeOut(subtitle) # Fade out initial title
        )
        self.wait(0.5)
        
        # --- Beat 3: Understanding a, b, c (Parabola Transformations) ---
        
        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            x_length=8, y_length=6,
            axis_config={"color": grey_color, "stroke_width": 2},
            tips=False
        ).shift(DOWN * 0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="y", font_size=28)
        
        self.play(Create(axes), Write(labels), run_time=1.5)
        self.wait(0.5)

        def get_parabola(a_val, b_val, c_val, color):
            return axes.plot(lambda x: a_val * x**2 + b_val * x + c_val, color=color)

        # Initial parabola (a=1, b=0, c=0)
        p1 = get_parabola(1, 0, 0, blue_color)
        p1_label_a = Text("a=1", color=blue_color, font_size=28).next_to(p1, RIGHT, buff=0.1).shift(UP * 0.5)
        self.play(Create(p1), Write(p1_label_a), run_time=0.8)
        self.wait(0.5)

        # Changing 'a' - wider
        p2 = get_parabola(0.5, 0, 0, gold_color)
        p2_label_a = Text("a=0.5 (Wider)", color=gold_color, font_size=28).next_to(p2, RIGHT, buff=0.1).shift(UP * 0.5)
        self.play(ReplacementTransform(p1, p2), ReplacementTransform(p1_label_a, p2_label_a), run_time=0.8)
        self.wait(0.5)

        # Changing 'a' - opens down
        p3 = get_parabola(-1, 0, 0, white_color)
        p3_label_a = Text("a=-1 (Opens Down)", color=white_color, font_size=28).next_to(p3, DOWN, buff=0.1).shift(LEFT * 0.5)
        self.play(ReplacementTransform(p2, p3), ReplacementTransform(p2_label_a, p3_label_a), run_time=0.8)
        self.wait(0.5)
        
        # Changing 'b' - shifts horizontally
        p_base_for_b = get_parabola(1, 0, 0, blue_color)
        p_base_label = Text("b=0", color=blue_color, font_size=28).next_to(p_base_for_b, RIGHT, buff=0.1).shift(UP * 0.5)
        self.play(ReplacementTransform(p3, p_base_for_b), ReplacementTransform(p3_label_a, p_base_label), run_time=0.8)
        self.wait(0.5)

        p_b_shift = get_parabola(1, 2, 0, gold_color) # Shifted left
        p_b_shift_label = Text("b=2 (Shifts Left)", color=gold_color, font_size=28).next_to(p_b_shift, RIGHT, buff=0.1).shift(UP * 0.5)
        self.play(ReplacementTransform(p_base_for_b, p_b_shift), ReplacementTransform(p_base_label, p_b_shift_label), run_time=0.8)
        self.wait(0.5)

        # Changing 'c' - shifts vertically
        p_base_for_c = get_parabola(1, 0, 0, blue_color)
        p_base_label_c = Text("c=0", color=blue_color, font_size=28).next_to(p_base_for_c, RIGHT, buff=0.1).shift(UP * 0.5)
        self.play(ReplacementTransform(p_b_shift, p_base_for_c), ReplacementTransform(p_b_shift_label, p_base_label_c), run_time=0.8)
        self.wait(0.5)

        p_c_shift = get_parabola(1, 0, 2, white_color) # Shifted up
        p_c_shift_label = Text("c=2 (Y-intercept)", color=white_color, font_size=28).next_to(p_c_shift, RIGHT, buff=0.1).shift(UP * 0.5)
        self.play(ReplacementTransform(p_base_for_c, p_c_shift), ReplacementTransform(p_base_label_c, p_c_shift_label), run_time=0.8)
        self.wait(1.5)

        self.play(
            FadeOut(p_c_shift), FadeOut(p_c_shift_label),
            FadeOut(axes), FadeOut(labels)
        )
        self.wait(0.5)

        # --- Beat 4: The Quadratic Formula ---
        
        formula_title = Text("The Quadratic Formula", font_size=40, color=white_color).move_to(general_form_group.get_center() + DOWN * 1.5)
        self.play(FadeIn(formula_title, shift=UP))

        # Manually construct the formula: x = (-b ± sqrt(b^2 - 4ac)) / 2a
        x_eq = Text("x =", color=white_color, font_size=45)

        minus_b = Text("-b", color=gold_color, font_size=45)
        pm_symbol = Text("±", color=white_color, font_size=45)
        
        sqrt_begin = Text("√", color=white_color, font_size=45).stretch_to_fit_height(0.6)

        b2 = Text("b", color=gold_color, font_size=35)
        exp_2_inner = Text("2", color=gold_color, font_size=20)
        minus_4ac = Text("- 4ac", color=blue_color, font_size=35)
        
        # Position numerator elements
        exp_2_inner.next_to(b2, UP, buff=0).align_to(b2, RIGHT).shift(0.1*RIGHT + 0.1*UP)
        b_squared_group = VGroup(b2, exp_2_inner)
        discriminant_elements = VGroup(b_squared_group, minus_4ac).arrange(RIGHT, buff=0.05)
        
        sqrt_begin.next_to(pm_symbol, RIGHT, buff=0.1).shift(LEFT * 0.05) # Adjust manually
        discriminant_elements.next_to(sqrt_begin, RIGHT, buff=0.1).shift(UP*0.05)

        numerator_elements = VGroup(minus_b, pm_symbol, sqrt_begin, discriminant_elements).arrange(RIGHT, buff=0.1).shift(UP * 0.2)

        line = Line(LEFT * 2.5, RIGHT * 2.5, color=white_color).next_to(numerator_elements, DOWN, buff=0.1)

        denominator = VGroup(Text("2", color=white_color, font_size=45), Text("a", color=blue_color, font_size=45)).arrange(RIGHT, buff=0.1).next_to(line, DOWN, buff=0.1)

        formula_group_right = VGroup(numerator_elements, line, denominator)
        formula_group = VGroup(x_eq, formula_group_right).arrange(RIGHT, buff=0.2).move_to(ORIGIN)

        self.play(FadeIn(x_eq, shift=LEFT))
        self.play(
            LaggedStart(
                Write(minus_b), Write(pm_symbol), Write(sqrt_begin),
                Write(b2), Write(exp_2_inner), Write(minus_4ac),
                Create(line),
                Write(denominator),
                lag_ratio=0.1,
                run_time=2.5
            )
        )
        self.wait(1.5)

        solution_expl = Text("Solves for 'x' when y = 0", color=white_color, font_size=30).next_to(formula_group, DOWN, buff=0.8)
        self.play(FadeIn(solution_expl, shift=DOWN))
        self.wait(1.5)

        self.play(FadeOut(formula_title), FadeOut(solution_expl), general_form_group.animate.shift(LEFT * 3))
        self.wait(0.5)

        self.play(
            formula_group.animate.to_edge(RIGHT).shift(LEFT * 1).shift(UP * 0.5)
        )
        self.wait(0.5)

        # --- Beat 5: Visualizing the Roots ---
        axes_roots = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 5, 1],
            x_length=8, y_length=5,
            axis_config={"color": grey_color, "stroke_width": 2},
            tips=False
        ).to_edge(LEFT).shift(RIGHT * 1).shift(DOWN * 0.5)
        labels_roots = axes_roots.get_axis_labels(x_label="x", y_label="y", font_size=28)

        self.play(Create(axes_roots), Write(labels_roots))
        self.wait(0.5)

        # Example parabola with two roots: x^2 - 4
        roots_parabola = axes_roots.plot(lambda x: x**2 - 4, color=blue_color)
        root1_coord = axes_roots.coords_to_point(-2, 0)
        root2_coord = axes_roots.coords_to_point(2, 0)

        root_dot1 = Dot(root1_coord, color=gold_color, radius=0.1)
        root_dot2 = Dot(root2_coord, color=gold_color, radius=0.1)

        root_text1 = Text("x₁", color=gold_color, font_size=30).next_to(root_dot1, DOWN, buff=0.2)
        root_text2 = Text("x₂", color=gold_color, font_size=30).next_to(root_dot2, DOWN, buff=0.2)
        
        expl_text_roots = Text("The 'x' values are the roots", font_size=35, color=white_color).next_to(axes_roots, UP, buff=0.8)

        self.play(Create(roots_parabola), FadeIn(expl_text_roots))
        self.wait(1)
        self.play(FadeIn(root_dot1, scale=0.8), FadeIn(root_text1), FadeIn(root_dot2, scale=0.8), FadeIn(root_text2), run_time=1.5)
        self.wait(2)

        self.play(
            FadeOut(expl_text_roots), FadeOut(roots_parabola),
            FadeOut(root_dot1), FadeOut(root_text1), FadeOut(root_dot2), FadeOut(root_text2),
            FadeOut(axes_roots), FadeOut(labels_roots),
            FadeOut(general_form_group),
            FadeOut(formula_group)
        )
        self.wait(0.5)

        # --- Recap Card ---
        recap_title = Text("Recap:", font_size=50, color=white_color).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(recap_title))

        # Re-create general form for recap
        recap_a = Text("a", color=blue_color, font_size=45)
        recap_x1 = Text("x", color=white_color, font_size=45)
        recap_exp2 = Text("2", color=white_color, font_size=25)
        recap_plus1 = Text("+", color=white_color, font_size=45)
        recap_b = Text("b", color=gold_color, font_size=45)
        recap_x2 = Text("x", color=white_color, font_size=45)
        recap_plus2 = Text("+", color=white_color, font_size=45)
        recap_c = Text("c", color=white_color, font_size=45)
        recap_equals0 = Text("= 0", color=white_color, font_size=45)

        recap_x1.next_to(recap_a, RIGHT, buff=0.1)
        recap_exp2.next_to(recap_x1, UP, buff=0).align_to(recap_x1, RIGHT).shift(0.1*RIGHT + 0.1*UP)
        recap_plus1.next_to(recap_x1, RIGHT, buff=0.4)
        recap_b.next_to(recap_plus1, RIGHT, buff=0.4)
        recap_x2.next_to(recap_b, RIGHT, buff=0.1)
        recap_plus2.next_to(recap_x2, RIGHT, buff=0.4)
        recap_c.next_to(recap_plus2, RIGHT, buff=0.4)
        recap_equals0.next_to(recap_c, RIGHT, buff=0.4)

        recap_general_form = VGroup(
            recap_a, recap_x1, recap_exp2, recap_plus1, recap_b, recap_x2, recap_plus2, recap_c, recap_equals0
        ).move_to(ORIGIN).shift(UP*1.5)
        
        self.play(FadeIn(recap_general_form, shift=LEFT))
        self.wait(1)

        # Re-create quadratic formula for recap
        recap_x_eq = Text("x =", color=white_color, font_size=40)
        recap_minus_b = Text("-b", color=gold_color, font_size=40)
        recap_pm_symbol = Text("±", color=white_color, font_size=40)
        recap_sqrt_begin = Text("√", color=white_color, font_size=40).stretch_to_fit_height(0.6)

        recap_b2 = Text("b", color=gold_color, font_size=30)
        recap_exp_2_inner = Text("2", color=gold_color, font_size=18)
        recap_minus_4ac = Text("- 4ac", color=blue_color, font_size=30)
        
        recap_exp_2_inner.next_to(recap_b2, UP, buff=0).align_to(recap_b2, RIGHT).shift(0.1*RIGHT + 0.1*UP)
        recap_b_squared_group = VGroup(recap_b2, recap_exp_2_inner)
        recap_discriminant_elements = VGroup(recap_b_squared_group, recap_minus_4ac).arrange(RIGHT, buff=0.05)
        
        recap_sqrt_begin.next_to(recap_pm_symbol, RIGHT, buff=0.1).shift(LEFT * 0.05)
        recap_discriminant_elements.next_to(recap_sqrt_begin, RIGHT, buff=0.1).shift(UP*0.05)

        recap_numerator_elements = VGroup(recap_minus_b, recap_pm_symbol, recap_sqrt_begin, recap_discriminant_elements).arrange(RIGHT, buff=0.1).shift(UP * 0.1)

        recap_line = Line(LEFT * 2.2, RIGHT * 2.2, color=white_color).next_to(recap_numerator_elements, DOWN, buff=0.1)
        recap_denominator = VGroup(Text("2", color=white_color, font_size=40), Text("a", color=blue_color, font_size=40)).arrange(RIGHT, buff=0.1).next_to(recap_line, DOWN, buff=0.1)

        recap_formula_group_right = VGroup(recap_numerator_elements, recap_line, recap_denominator)
        recap_quadratic_formula = VGroup(recap_x_eq, recap_formula_group_right).arrange(RIGHT, buff=0.2).move_to(ORIGIN).shift(DOWN*1.0)

        self.play(FadeIn(recap_quadratic_formula, shift=RIGHT))
        self.wait(3)

        self.play(FadeOut(VGroup(recap_title, recap_general_form, recap_quadratic_formula)))
        self.wait(1)