from manim import *

# Set up custom colors for 3b1b style
BLUE_ACCENT = BLUE_E
GOLD_ACCENT = GOLD_E
TEXT_COLOR = WHITE

class QuadraticFormulaWorks(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Beat 1: The "Every Quadratic" Hook & Intuition (y = x^2 and transformations)
        self.beat_1_hook()

        # Beat 2: Introducing the General Form and a != 0
        self.beat_2_general_form()

        # Beat 3: The Quadratic Formula Itself
        self.beat_3_formula()

        # Beat 4: Geometric Interpretation
        self.beat_4_geometric_intuition()

        # Beat 5: Recap
        self.beat_5_recap()

    def beat_1_hook(self):
        title = Text("Formula Works Every Quadratic", font_size=50, color=TEXT_COLOR)
        self.play(Write(title))
        self.wait(0.5)

        self.play(title.animate.to_edge(UP).set_color(BLUE_ACCENT), run_time=0.8)

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": GREY_A, "stroke_width": 2},
            background_line_style={"stroke_opacity": 0.4}
        ).shift(DOWN * 0.5)
        self.play(Create(plane), run_time=1.5)

        # y = x^2 parabola
        parabola_eq = MathTex(r"y = x^2", color=BLUE_ACCENT).to_corner(UL).shift(RIGHT*2)
        parabola = plane.plot(lambda x: x**2, color=GOLD_ACCENT, stroke_width=4)
        self.play(Create(parabola), Write(parabola_eq), run_time=1.5)
        self.wait(0.5)

        # Show transformations: shift, scale, then shift again
        self.play(parabola.animate.shift(LEFT*1 + DOWN*0.5), run_time=0.8)
        self.play(parabola.animate.scale_y(0.5, about_point=parabola.get_center()), run_time=0.8)
        self.play(parabola.animate.shift(RIGHT*2 + UP*1.5), run_time=1)

        transform_text = Text("All Parabolas are 'the same shape'", color=TEXT_COLOR, font_size=30).next_to(parabola_eq, DOWN, buff=0.5)
        self.play(Write(transform_text), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(parabola_eq, transform_text))
        self.current_parabola = parabola
        self.current_plane = plane

    def beat_2_general_form(self):
        # General form: ax^2 + bx + c = 0
        general_form_tex = MathTex(
            r"ax^2 + bx + c = 0",
            color=BLUE_ACCENT
        ).to_corner(UL).shift(RIGHT*2)
        self.play(Write(general_form_tex), run_time=1.5)
        self.wait(0.5)

        # Emphasize 'a != 0'
        a_not_zero = MathTex(r"\text{where } a \neq 0", color=TEXT_COLOR, font_size=30).next_to(general_form_tex, DOWN, buff=0.5)
        self.play(Write(a_not_zero))

        # Illustrate a -> 0: parabola flattens into a line
        current_parabola_copy = self.current_parabola.copy()
        
        a_equals_zero_text = Text("If a = 0, it's a line!", color=GOLD_ACCENT, font_size=35).to_edge(DR).shift(LEFT*0.5)
        line_a0 = self.current_plane.plot(lambda x: 0.5*x + 1, color=GOLD_ACCENT, stroke_width=4) # Example line

        self.play(
            ReplacementTransform(current_parabola_copy, line_a0),
            Write(a_equals_zero_text),
            run_time=2
        )
        self.wait(1)

        self.play(
            FadeOut(a_equals_zero_text, line_a0),
            general_form_tex.animate.next_to(self.current_plane, UP, buff=0.5).set_x(0),
            FadeOut(a_not_zero),
            FadeOut(self.current_parabola) 
        )
        self.wait(0.5)

        # A new generic parabola for general form with real roots
        # Example: x^2 + 2x - 3 = 0, roots at x = -3, x = 1. Vertex at x=-1, y=-4
        parabola_general = self.current_plane.plot(lambda x: x**2 + 2*x - 3, color=GOLD_ACCENT, stroke_width=4)
        self.play(Create(parabola_general), run_time=1.5)
        self.current_parabola = parabola_general
        self.current_general_form_tex = general_form_tex
        self.play(general_form_tex.animate.set_value(r"x^2 + 2x - 3 = 0")) # Set specific equation for this parabola
        self.wait(0.5)


    def beat_3_formula(self):
        # The Quadratic Formula itself
        quadratic_formula_lhs = MathTex(r"x = ", color=BLUE_ACCENT)
        quadratic_formula_rhs = MathTex(
            r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            color=GOLD_ACCENT
        )
        quadratic_formula = VGroup(quadratic_formula_lhs, quadratic_formula_rhs).arrange(RIGHT, buff=0.1)
        quadratic_formula.next_to(self.current_general_form_tex, DOWN, buff=0.8).shift(RIGHT*0.5) 

        self.play(Write(quadratic_formula), run_time=2)
        self.wait(1)

        # Show roots on the parabola
        root_point_1 = Dot(self.current_plane.coords_to_point(-3, 0), color=BLUE_ACCENT, radius=0.1)
        root_point_2 = Dot(self.current_plane.coords_to_point(1, 0), color=BLUE_ACCENT, radius=0.1)
        
        root_label_1 = MathTex(r"x_1", color=BLUE_ACCENT, font_size=30).next_to(root_point_1, DOWN, buff=0.1)
        root_label_2 = MathTex(r"x_2", color=BLUE_ACCENT, font_size=30).next_to(root_point_2, DOWN, buff=0.1)

        self.play(
            GrowSmallestToLargest(root_point_1), GrowSmallestToLargest(root_point_2),
            Write(root_label_1), Write(root_label_2),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            FadeOut(root_point_1, root_point_2, root_label_1, root_label_2),
            quadratic_formula.animate.to_corner(UL).shift(RIGHT*2),
            FadeOut(self.current_general_form_tex)
        )
        self.current_formula = quadratic_formula

    def beat_4_geometric_intuition(self):
        # Use a new generic parabola for clarity with roots x=-1 and x=3 (a=0.5, b=-1, c=-1.5)
        self.play(FadeOut(self.current_parabola))

        # Re-center the plane for better visual on symmetry
        self.play(self.current_plane.animate.shift(LEFT * 0.5)) 

        parabola_for_geo = self.current_plane.plot(lambda x: 0.5*(x-1)**2 - 2, color=GOLD_ACCENT, stroke_width=4)
        self.play(Create(parabola_for_geo), run_time=1.5)

        # Axis of symmetry: x = -b/(2a) -> x = -(-1)/(2*0.5) = 1
        axis_of_sym_x = 1 
        axis_line = self.current_plane.get_vertical_line(self.current_plane.coords_to_point(axis_of_sym_x, 0), color=BLUE_ACCENT, stroke_dash_arg=[0.1, 0.1])
        axis_label = MathTex(r"x = -\frac{b}{2a}", color=BLUE_ACCENT).next_to(axis_line, UP, buff=0.1).shift(LEFT*0.5)

        self.play(Create(axis_line), Write(axis_label), run_time=1.5)
        self.wait(0.5)

        # Roots for this parabola are at x = -1 and x = 3
        root_1_coords = self.current_plane.coords_to_point(-1, 0)
        root_2_coords = self.current_plane.coords_to_point(3, 0)

        root_dot_1 = Dot(root_1_coords, color=GOLD_ACCENT, radius=0.08)
        root_dot_2 = Dot(root_2_coords, color=GOLD_ACCENT, radius=0.08)

        self.play(GrowSmallestToLargest(root_dot_1), GrowSmallestToLargest(root_dot_2))

        # Show distance from axis of symmetry to roots: +/- sqrt(b^2 - 4ac) / (2a)
        distance_arrow_1 = Arrow(
            self.current_plane.coords_to_point(axis_of_sym_x, 0),
            root_1_coords,
            buff=0.05,
            stroke_width=3,
            max_stroke_width_to_length_ratio=3,
            max_tip_length_to_length_ratio=0.25,
            color=GOLD_ACCENT
        )
        distance_arrow_2 = Arrow(
            self.current_plane.coords_to_point(axis_of_sym_x, 0),
            root_2_coords,
            buff=0.05,
            stroke_width=3,
            max_stroke_width_to_length_ratio=3,
            max_tip_length_to_length_ratio=0.25,
            color=GOLD_ACCENT
        )
        distance_label = MathTex(r"\pm \frac{\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT, font_size=35).next_to(distance_arrow_2, UP, buff=0.1).shift(LEFT*0.5)

        self.play(
            GrowArrow(distance_arrow_1), GrowArrow(distance_arrow_2),
            Write(distance_label),
            run_time=2
        )
        self.wait(1.5)

        self.play(
            FadeOut(parabola_for_geo, axis_line, axis_label, root_dot_1, root_dot_2,
                    distance_arrow_1, distance_arrow_2, distance_label, self.current_formula, self.current_plane)
        )

    def beat_5_recap(self):
        recap_title = Text("Recap:", color=BLUE_ACCENT, font_size=40).to_edge(UL).shift(RIGHT*1)
        recap_points = VGroup(
            Tex("- Every parabola is a transformation of $y=x^2$.", color=TEXT_COLOR),
            Tex("- Quadratic Formula solves $ax^2+bx+c=0$ (where $a \\neq 0$).", color=TEXT_COLOR),
            Tex("- Geometric components: axis of symmetry ($x = -b/(2a)$) and distance to roots ($\pm \\frac{\sqrt{\\Delta}}{2a}$).", color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.7, run_time=5))
        self.wait(2)

        final_title = Text("Formula Works Every Quadratic", font_size=50, color=BLUE_ACCENT).center()
        self.play(Transform(recap_title, final_title), FadeOut(recap_points))
        self.wait(1.5)
        self.play(FadeOut(recap_title))
        self.wait(0.5)