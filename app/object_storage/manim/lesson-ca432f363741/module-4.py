from manim import *

class DiscriminantAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        BACKGROUND_COLOR = '#1A1A1A'
        BLUE_ACCENT = '#58C4DD' # Light blue for graphs, accents
        GOLD_ACCENT = '#FFD700' # Bright gold for key elements
        WHITE_TEXT = WHITE
        
        self.camera.background_color = BACKGROUND_COLOR

        # Helper to create styled Text mobjects
        def create_text_mobject(text_str, font_size=45, color=WHITE_TEXT):
            return Text(text_str, font_size=font_size, color=color)

        # Helper to create and arrange VGroups of Mobjects/strings for math expressions (no Tex)
        def create_math_group(parts, font_size_base=45, buff=0.15):
            mobjects = VGroup()
            for part in parts:
                if isinstance(part, Mobject):
                    mobjects.add(part)
                else:
                    mobjects.add(create_text_mobject(str(part), font_size=font_size_base))
            mobjects.arrange(RIGHT, buff=buff)
            return mobjects

        # --- Beat 1: Visual Hook - Parabola & X-intercepts ---
        # Title appears early
        title = create_text_mobject("The Discriminant & Solution Types", font_size=55, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)
        
        number_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            background_line_style={"stroke_opacity": 0.2},
            faded_line_style={"stroke_opacity": 0.1},
            axes_color=BLUE_ACCENT
        ).scale(0.8).shift(DOWN * 0.5)
        
        x_axis_label = create_text_mobject("x", font_size=30, color=BLUE_ACCENT).next_to(number_plane.get_x_axis(), RIGHT, buff=0.1)
        y_axis_label = create_text_mobject("y", font_size=30, color=BLUE_ACCENT).next_to(number_plane.get_y_axis(), UP, buff=0.1)
        
        self.play(Create(number_plane), FadeIn(x_axis_label, y_axis_label))
        self.wait(0.5)

        # Parabola 1: Two real solutions (intersects x-axis twice)
        graph1 = number_plane.get_graph(lambda x: 0.5 * x**2 - 2, color=GOLD_ACCENT)
        x_intercept1_1 = Dot(number_plane.coords_to_point(-2, 0), color=GOLD_ACCENT, radius=0.08)
        x_intercept1_2 = Dot(number_plane.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.08)
        
        parabola_group1 = VGroup(graph1, x_intercept1_1, x_intercept1_2)
        self.play(Create(parabola_group1), run_time=1.5)
        self.wait(1)

        # Parabola 2: One real solution (tangent to x-axis)
        graph2 = number_plane.get_graph(lambda x: 0.5 * x**2, color=GOLD_ACCENT)
        x_intercept2 = Dot(number_plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.08)

        parabola_group2 = VGroup(graph2, x_intercept2)
        self.play(
            ReplacementTransform(parabola_group1, parabola_group2),
            run_time=1.5
        )
        self.wait(1)

        # Parabola 3: No real solutions (does not intersect x-axis)
        graph3 = number_plane.get_graph(lambda x: 0.5 * x**2 + 2, color=GOLD_ACCENT)
        
        parabola_group3 = VGroup(graph3)
        self.play(
            ReplacementTransform(parabola_group2, parabola_group3),
            run_time=1.5
        )
        self.wait(1)

        # Question text
        question_text = create_text_mobject("How many x-intercepts?", font_size=40, color=BLUE_ACCENT).next_to(number_plane, DOWN, buff=1)
        self.play(FadeIn(question_text), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(question_text))
        
        # Fade out parabolas and axes to prepare for next beat
        self.play(FadeOut(parabola_group3, x_axis_label, y_axis_label))
        
        # --- Beat 2: Quadratic Equation Form & The Core Idea ---
        # Construct: y = ax^2 + bx + c
        y_eq = create_text_mobject("y =")
        
        # ax^2 term
        a_term = create_text_mobject("a", color=GOLD_ACCENT)
        x_sq_base = create_text_mobject("x")
        exponent_2 = create_text_mobject("2", font_size=25).next_to(x_sq_base, UP + RIGHT, buff=0.05).shift(UL*0.05)
        ax_squared_group = VGroup(a_term, x_sq_base, exponent_2) 
        
        plus1 = create_text_mobject("+")
        
        # bx term
        b_term = create_text_mobject("b", color=BLUE_ACCENT)
        bx_group = VGroup(b_term, create_text_mobject("x"))
        
        plus2 = create_text_mobject("+")
        
        # c term
        c_term = create_text_mobject("c", color=GOLD_ACCENT)

        # Arrange all parts to form the full quadratic expression
        full_quadratic_expr = VGroup(
            ax_squared_group[0], # a
            ax_squared_group[1], # x
            ax_squared_group[2], # 2 (exponent)
            plus1,
            bx_group[0], # b
            bx_group[1], # x
            plus2,
            c_term
        ).arrange(RIGHT, buff=0.15)
        
        # The full equation
        quadratic_equation = VGroup(y_eq, full_quadratic_expr).arrange(RIGHT, buff=0.1).move_to(ORIGIN).scale(0.9).to_edge(UP, buff=1)

        self.play(FadeIn(quadratic_equation))
        self.wait(1.5)

        # Highlight y=0 for solutions
        zero_text_val = create_text_mobject("0", color=GOLD_ACCENT)
        zero_equation = VGroup(zero_text_val, create_text_mobject("="), full_quadratic_expr.copy()).arrange(RIGHT, buff=0.1).move_to(quadratic_equation.get_center())
        
        self.play(ReplacementTransform(quadratic_equation, zero_equation))
        self.wait(1)

        # Connect back to x-intercepts
        solutions_text = create_text_mobject("Solutions = x-intercepts", font_size=40, color=BLUE_ACCENT).next_to(zero_equation, DOWN, buff=1)
        self.play(FadeIn(solutions_text))
        self.wait(1.5)
        self.play(FadeOut(solutions_text))

        self.play(FadeOut(zero_equation)) # Fade out the equation for clarity
        self.wait(0.5)
        
        # --- Beat 3: The Discriminant - Unveiling b^2 - 4ac ---
        discriminant_label = create_text_mobject("The Discriminant:", font_size=45, color=WHITE_TEXT).to_edge(LEFT, buff=0.5).to_edge(UP, buff=1.5)
        self.play(FadeIn(discriminant_label))

        # Construct: b^2 - 4ac
        b_disc = create_text_mobject("b", color=BLUE_ACCENT, font_size=45)
        exp_2_disc = create_text_mobject("2", font_size=25).next_to(b_disc, UP + RIGHT, buff=0.05).shift(UL*0.05)
        b_squared_group = VGroup(b_disc, exp_2_disc)
        
        minus_text = create_text_mobject("-")
        four_text = create_text_mobject("4")
        a_disc = create_text_mobject("a", color=GOLD_ACCENT)
        c_disc = create_text_mobject("c", color=GOLD_ACCENT)
        
        four_ac_group = VGroup(four_text, a_disc, c_disc).arrange(RIGHT, buff=0.05)
        
        discriminant_expr = VGroup(b_squared_group, minus_text, four_ac_group).arrange(RIGHT, buff=0.15)
        discriminant_expr.next_to(discriminant_label, RIGHT, buff=0.5)
        
        self.play(FadeIn(discriminant_expr), run_time=1.5)
        self.wait(1)

        # Explain its location (inside square root)
        underline_expr = Rectangle(color=BLUE_ACCENT, stroke_width=2).surround(discriminant_expr, buff=0.15)
        
        # Approximate a square root symbol manually with line segments
        root_arc = Arc(radius=0.2, start_angle=PI/2, angle=-PI/2, color=BLUE_ACCENT, stroke_width=2).next_to(underline_expr, LEFT, buff=0.05).shift(DOWN*0.1)
        root_stem = Line(root_arc.get_bottom(), root_arc.get_bottom() + LEFT * 0.1, color=BLUE_ACCENT, stroke_width=2)
        root_top = Line(root_arc.get_top(), underline_expr.get_top() + LEFT * 0.05, color=BLUE_ACCENT, stroke_width=2)
        root_symbol_group = VGroup(root_arc, root_stem, root_top)

        inside_root_text = create_text_mobject("...is found inside the square root!", font_size=35, color=WHITE_TEXT).next_to(discriminant_expr, DOWN, buff=0.8).shift(RIGHT * 1.5)
        arrow = Arrow(inside_root_text.get_top(), discriminant_expr.get_bottom(), buff=0.1, color=BLUE_ACCENT)
        
        self.play(Create(underline_expr), Create(root_symbol_group), run_time=0.8)
        self.play(FadeIn(inside_root_text), GrowArrow(arrow))
        self.wait(2)
        
        self.play(FadeOut(underline_expr, root_symbol_group, inside_root_text, arrow))
        
        # Reposition discriminant for later beats
        self.play(discriminant_expr.animate.scale(0.8).to_edge(UP, buff=1.5).to_edge(LEFT, buff=0.5),
                  FadeOut(discriminant_label)) 
        
        # --- Prepare for Solution Type Visuals ---
        self.play(FadeIn(number_plane), FadeIn(x_axis_label, y_axis_label))
        self.wait(0.5)
        
        # --- Beat 4: Case 1: Discriminant > 0 (Two Solutions) ---
        disc_gt_0_text = create_math_group([">", "0"], font_size_base=45).next_to(discriminant_expr, RIGHT, buff=0.1)
        case_label = create_text_mobject("Case 1:", font_size=35, color=WHITE_TEXT).next_to(discriminant_expr, LEFT, buff=0.5).shift(LEFT*0.5)
        
        self.play(FadeIn(case_label), FadeIn(disc_gt_0_text))
        
        graph_case1 = number_plane.get_graph(lambda x: 0.5 * x**2 - 2, color=GOLD_ACCENT)
        dot_case1_1 = Dot(number_plane.coords_to_point(-2, 0), color=GOLD_ACCENT, radius=0.08)
        dot_case1_2 = Dot(number_plane.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.08)
        
        parabola_group_case1 = VGroup(graph_case1, dot_case1_1, dot_case1_2).shift(DOWN * 1) # Shift for better view
        self.play(Create(parabola_group_case1), run_time=1.5) 
        
        solutions_text_case1 = create_text_mobject("2 Real Solutions", font_size=40, color=WHITE_TEXT).next_to(number_plane, DOWN, buff=0.8)
        self.play(FadeIn(solutions_text_case1))
        self.wait(2)
        
        # --- Beat 5: Case 2: Discriminant = 0 (One Solution) ---
        disc_eq_0_text = create_math_group(["=", "0"], font_size_base=45).next_to(discriminant_expr, RIGHT, buff=0.1)
        self.play(ReplacementTransform(disc_gt_0_text, disc_eq_0_text))
        
        graph_case2 = number_plane.get_graph(lambda x: 0.5 * x**2, color=GOLD_ACCENT)
        dot_case2 = Dot(number_plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.08)
        
        parabola_group_case2 = VGroup(graph_case2, dot_case2).shift(DOWN * 1)
        self.play(
            ReplacementTransform(parabola_group_case1, parabola_group_case2),
            run_time=1.5
        )
        
        solutions_text_case2 = create_text_mobject("1 Real Solution", font_size=40, color=WHITE_TEXT).next_to(number_plane, DOWN, buff=0.8)
        self.play(ReplacementTransform(solutions_text_case1, solutions_text_case2))
        self.wait(2)
        
        # --- Beat 6: Case 3: Discriminant < 0 (No Real Solutions) ---
        disc_lt_0_text = create_math_group(["<", "0"], font_size_base=45).next_to(discriminant_expr, RIGHT, buff=0.1)
        self.play(ReplacementTransform(disc_eq_0_text, disc_lt_0_text))
        
        graph_case3 = number_plane.get_graph(lambda x: 0.5 * x**2 + 2, color=GOLD_ACCENT)
        
        parabola_group_case3 = VGroup(graph_case3).shift(DOWN * 1)
        self.play(
            ReplacementTransform(parabola_group_case2, parabola_group_case3),
            run_time=1.5
        )
        
        solutions_text_case3 = create_text_mobject("0 Real Solutions", font_size=40, color=WHITE_TEXT).next_to(number_plane, DOWN, buff=0.8)
        self.play(ReplacementTransform(solutions_text_case2, solutions_text_case3))
        self.wait(2)
        
        # --- Clean up for Recap ---
        self.play(
            FadeOut(parabola_group_case3, solutions_text_case3, number_plane, x_axis_label, y_axis_label, 
                    discriminant_expr, disc_lt_0_text, case_label, title)
        )
        self.wait(0.5)
        
        # --- Beat 7: Recap Card ---
        recap_title = create_text_mobject("Recap: The Discriminant", font_size=55, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(recap_title))

        # Recreate discriminant expression for recap, smaller font
        b_disc_recap = create_text_mobject("b", color=BLUE_ACCENT, font_size=35)
        exp_2_disc_recap = create_text_mobject("2", font_size=20).next_to(b_disc_recap, UP + RIGHT, buff=0.05).shift(UL*0.05)
        b_squared_group_recap = VGroup(b_disc_recap, exp_2_disc_recap)
        
        minus_text_recap = create_text_mobject("-", font_size=35)
        four_text_recap = create_text_mobject("4", font_size=35)
        a_disc_recap = create_text_mobject("a", color=GOLD_ACCENT, font_size=35)
        c_disc_recap = create_text_mobject("c", color=GOLD_ACCENT, font_size=35)
        
        four_ac_group_recap = VGroup(four_text_recap, a_disc_recap, c_disc_recap).arrange(RIGHT, buff=0.05)
        
        discriminant_expr_recap_base = VGroup(b_squared_group_recap, minus_text_recap, four_ac_group_recap).arrange(RIGHT, buff=0.15)

        # Create the three rows for recap
        row1_cond = create_math_group([discriminant_expr_recap_base.copy(), " > ", "0"], font_size_base=35, buff=0.1)
        row1 = VGroup(row1_cond, create_text_mobject("-> 2 Real Solutions", font_size=35, color=BLUE_ACCENT)).arrange(RIGHT, buff=0.5).move_to(LEFT * 0.5 + UP * 1.5)
        
        row2_cond = create_math_group([discriminant_expr_recap_base.copy(), " = ", "0"], font_size_base=35, buff=0.1)
        row2 = VGroup(row2_cond, create_text_mobject("-> 1 Real Solution", font_size=35, color=WHITE_TEXT)).arrange(RIGHT, buff=0.5).move_to(LEFT * 0.5)
        
        row3_cond = create_math_group([discriminant_expr_recap_base.copy(), " < ", "0"], font_size_base=35, buff=0.1)
        row3 = VGroup(row3_cond, create_text_mobject("-> 0 Real Solutions", font_size=35, color=GOLD_ACCENT)).arrange(RIGHT, buff=0.5).move_to(LEFT * 0.5 + DOWN * 1.5)

        self.play(FadeIn(row1))
        self.wait(1.5)
        self.play(FadeIn(row2))
        self.wait(1.5)
        self.play(FadeIn(row3))
        self.wait(2)

        final_message = create_text_mobject("Understand the Discriminant, Master Quadratics!", font_size=40, color=WHITE_TEXT).to_edge(DOWN)
        self.play(FadeIn(final_message))
        self.wait(3)