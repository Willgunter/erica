from manim import *

class GeometricInterpretationDiscriminant(Scene):
    def construct(self):
        # --- Configuration and Colors ---
        # Using a dark background is Manim's default for Scene.
        BLUE_ACCENT = BLUE_B
        GOLD_ACCENT = GOLD_C
        LIGHT_TEXT = WHITE

        # --- Beat 1: The X-Intercept Question (Visual Hook) ---
        title = Text("Geometric Interpretation and the Discriminant", font_size=48, color=LIGHT_TEXT)
        title.move_to(UP * 3.5)
        self.play(Write(title))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"color": LIGHT_TEXT, "stroke_width": 2},
        ).add_coordinates()
        plane.to_edge(LEFT, buff=1)

        question_text = Text("How many times does it cross the x-axis?",
                             font_size=30, color=LIGHT_TEXT)
        question_text.next_to(plane, RIGHT, buff=1).align_to(title, DOWN)

        self.play(Create(plane, run_time=1.5), Write(question_text))
        self.wait(0.5)

        # Parabola 1: Two solutions (y = x^2 - 4)
        parabola1 = plane.plot(lambda x: x**2 - 4, color=BLUE_ACCENT)
        dot1_a = Dot(plane.coords_to_point(-2, 0), color=GOLD_ACCENT, radius=0.1)
        dot1_b = Dot(plane.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.1)
        group1 = VGroup(parabola1, dot1_a, dot1_b)

        self.play(Create(parabola1), GrowAlongPath(dot1_a), GrowAlongPath(dot1_b))
        self.wait(1.5)

        # Parabola 2: One solution (y = x^2)
        parabola2 = plane.plot(lambda x: x**2, color=BLUE_ACCENT)
        dot2 = Dot(plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.1)
        group2 = VGroup(parabola2, dot2)

        self.play(
            Transform(parabola1, parabola2),
            FadeOut(dot1_a, target_position=dot2.get_center()),
            FadeOut(dot1_b, target_position=dot2.get_center()),
            GrowAlongPath(dot2)
        )
        self.wait(1.5)

        # Parabola 3: No solutions (y = x^2 + 2)
        parabola3 = plane.plot(lambda x: x**2 + 2, color=BLUE_ACCENT)
        group3 = VGroup(parabola3)

        self.play(
            Transform(parabola1, parabola3),
            FadeOut(dot2)
        )
        self.wait(1.5)

        # --- Beat 2: Introducing the Discriminant ---
        self.play(
            FadeOut(parabola1),
            FadeOut(plane),
            FadeOut(question_text),
            FadeOut(title)
        )

        quad_formula_intro = Text("The Quadratic Formula helps find x-intercepts.",
                                  font_size=36, color=LIGHT_TEXT)
        quad_formula_intro.to_edge(UP, buff=1)
        self.play(Write(quad_formula_intro))
        self.wait(0.5)

        discriminant_expr = Text("b^2 - 4ac", font_size=60, color=GOLD_ACCENT, weight=BOLD)
        discriminant_expr.move_to(ORIGIN)
        self.play(Write(discriminant_expr))
        self.wait(1)

        discriminant_name = Text("This is the Discriminant", font_size=36, color=LIGHT_TEXT)
        discriminant_name.next_to(discriminant_expr, DOWN, buff=0.5)
        arrow_to_name = Arrow(discriminant_expr.get_bottom(), discriminant_name.get_top(), buff=0.2, color=BLUE_ACCENT)

        self.play(GrowArrow(arrow_to_name), Write(discriminant_name))
        self.wait(1.5)

        self.play(FadeOut(arrow_to_name), FadeOut(quad_formula_intro))

        # --- Beat 3: Case 1 - Discriminant > 0 (Two Solutions) ---
        self.play(
            discriminant_expr.animate.scale(0.8).move_to(UP * 2.5),
            discriminant_name.animate.scale(0.8).next_to(discriminant_expr, DOWN, buff=0.2)
        )

        plane.to_edge(RIGHT, buff=1)
        self.play(Create(plane))

        parabola_case1 = plane.plot(lambda x: x**2 - 4, color=BLUE_ACCENT)
        dot_c1_a = Dot(plane.coords_to_point(-2, 0), color=GOLD_ACCENT, radius=0.1)
        dot_c1_b = Dot(plane.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.1)
        self.play(Create(parabola_case1), GrowAlongPath(dot_c1_a), GrowAlongPath(dot_c1_b))
        self.wait(0.5)

        case1_label_expr = Text("b^2 - 4ac > 0", font_size=40, color=GOLD_ACCENT)
        case1_label_expr.move_to(UP * 1.5).align_to(discriminant_expr, LEFT)

        case1_label_sol = Text("Two Real Solutions", font_size=36, color=BLUE_ACCENT)
        case1_label_sol.next_to(case1_label_expr, DOWN, buff=0.3).align_to(discriminant_expr, LEFT)

        arrow_to_graph1 = Arrow(
            case1_label_sol.get_right(),
            plane.get_center_of_mass() + RIGHT * 0.5,
            color=BLUE_ACCENT,
            tip_length=0.2
        )

        self.play(
            ReplacementTransform(discriminant_expr, case1_label_expr),
            FadeOut(discriminant_name),
            Write(case1_label_sol),
            GrowArrow(arrow_to_graph1)
        )
        self.wait(2)

        # --- Beat 4: Case 2 - Discriminant = 0 (One Solution) ---
        parabola_case2 = plane.plot(lambda x: x**2, color=BLUE_ACCENT)
        dot_c2 = Dot(plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.1)

        case2_label_expr = Text("b^2 - 4ac = 0", font_size=40, color=GOLD_ACCENT)
        case2_label_expr.move_to(case1_label_expr.get_center())

        case2_label_sol = Text("One Real Solution", font_size=36, color=BLUE_ACCENT)
        case2_label_sol.move_to(case1_label_sol.get_center())

        self.play(
            Transform(parabola_case1, parabola_case2),
            FadeOut(dot_c1_a, target_position=dot_c2.get_center()),
            FadeOut(dot_c1_b, target_position=dot_c2.get_center()),
            GrowAlongPath(dot_c2),
            Transform(case1_label_expr, case2_label_expr),
            Transform(case1_label_sol, case2_label_sol),
            arrow_to_graph1.animate.shift(LEFT*0.3) # Adjust arrow slightly
        )
        self.wait(2)

        # --- Beat 5: Case 3 - Discriminant < 0 (No Solutions) ---
        parabola_case3 = plane.plot(lambda x: x**2 + 2, color=BLUE_ACCENT)

        case3_label_expr = Text("b^2 - 4ac < 0", font_size=40, color=GOLD_ACCENT)
        case3_label_expr.move_to(case1_label_expr.get_center())

        case3_label_sol = Text("No Real Solutions", font_size=36, color=BLUE_ACCENT)
        case3_label_sol.move_to(case1_label_sol.get_center())

        self.play(
            Transform(parabola_case1, parabola_case3),
            FadeOut(dot_c2),
            Transform(case1_label_expr, case3_label_expr),
            Transform(case1_label_sol, case3_label_sol),
            arrow_to_graph1.animate.shift(LEFT*0.3) # Adjust arrow slightly
        )
        self.wait(2)

        # --- Short Recap Card ---
        self.play(
            FadeOut(plane),
            FadeOut(parabola_case1),
            FadeOut(case1_label_expr),
            FadeOut(case1_label_sol),
            FadeOut(arrow_to_graph1)
        )

        recap_title = Text("Discriminant (b^2 - 4ac) tells us:",
                           font_size=42, color=LIGHT_TEXT)
        recap_title.to_edge(UP, buff=1)

        recap_point1 = Text("> 0 : Two x-intercepts", font_size=36, color=GOLD_ACCENT)
        recap_point2 = Text("= 0 : One x-intercept", font_size=36, color=GOLD_ACCENT)
        recap_point3 = Text("< 0 : No x-intercepts", font_size=36, color=GOLD_ACCENT)

        recap_list = VGroup(recap_point1, recap_point2, recap_point3).arrange(DOWN, buff=0.5)
        recap_list.next_to(recap_title, DOWN, buff=1)

        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(LaggedStart(
            Write(recap_point1),
            Write(recap_point2),
            Write(recap_point3),
            lag_ratio=0.7
        ))
        self.wait(3)

        self.play(FadeOut(VGroup(recap_title, recap_list)))
        final_message = Text("Keep exploring with Erica!", font_size=48, color=BLUE_ACCENT)
        self.play(Write(final_message))
        self.wait(2)