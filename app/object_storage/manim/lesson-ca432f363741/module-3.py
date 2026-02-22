from manim import *

# Define custom colors for the theme
MY_BLUE = BLUE_E
MY_GOLD = GOLD_E
MY_WHITE = WHITE

class QuadraticFormulaGeometricMeaning(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#1A1A1A" # A very dark gray, close to black

        # --- Beat 1: Visual Hook & Introduction ---
        self.beat_1_hook_and_intro()

        # --- Beat 2: The Axis of Symmetry ---
        self.beat_2_axis_of_symmetry()

        # --- Beat 3: Distance from Symmetry ---
        self.beat_3_distance_from_symmetry()

        # --- Beat 4: Bringing it Together - The Quadratic Formula ---
        self.beat_4_the_formula()

        # --- Beat 5: Recap ---
        self.beat_5_recap()

    def create_quadratic_expression_text(self, a_val, b_val, c_val):
        # Helper to create y = ax^2 + bx + c as a VGroup of Text objects
        parts = []
        
        # y = 
        y_equals = Text("y = ", color=MY_WHITE)
        parts.append(y_equals)

        # ax^2 term
        if a_val != 0:
            if a_val == 1:
                x_sq_text = VGroup(
                    Text("x", color=MY_GOLD),
                    Text("2", color=MY_GOLD).scale(0.5).shift(0.1*UP + 0.05*RIGHT)
                ).arrange(RIGHT, buff=0)
                parts.append(x_sq_text)
            elif a_val == -1:
                x_sq_text = VGroup(
                    Text("-x", color=MY_GOLD),
                    Text("2", color=MY_GOLD).scale(0.5).shift(0.1*UP + 0.05*RIGHT)
                ).arrange(RIGHT, buff=0)
                parts.append(x_sq_text)
            else:
                a_text = Text(str(a_val), color=MY_GOLD)
                x_sq_text = VGroup(
                    Text("x", color=MY_GOLD),
                    Text("2", color=MY_GOLD).scale(0.5).shift(0.1*UP + 0.05*RIGHT)
                ).arrange(RIGHT, buff=0)
                parts.append(VGroup(a_text, x_sq_text).arrange(RIGHT, buff=0.05))
        
        # bx term
        if b_val != 0:
            sign = "+" if b_val > 0 else "-"
            parts.append(Text(f" {sign} ", color=MY_WHITE))
            
            if abs(b_val) == 1:
                x_text = Text("x", color=MY_GOLD)
                parts.append(x_text)
            else:
                b_text = Text(str(abs(b_val)), color=MY_GOLD)
                x_text = Text("x", color=MY_GOLD)
                parts.append(VGroup(b_text, x_text).arrange(RIGHT, buff=0.05))

        # c term
        if c_val != 0:
            sign = "+" if c_val > 0 else "-"
            parts.append(Text(f" {sign} ", color=MY_WHITE))
            c_text = Text(str(abs(c_val)), color=MY_GOLD)
            parts.append(c_text)

        full_expression = VGroup(*parts).arrange(RIGHT, buff=0.05)
        return full_expression

    def beat_1_hook_and_intro(self):
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": MY_WHITE, "stroke_opacity": 0.5},
            background_line_style={"stroke_color": MY_WHITE, "stroke_opacity": 0.2, "stroke_width": 1}
        ).add_coordinates()
        
        axes_labels = VGroup(
            plane.get_x_axis_label("x", direction=UP).set_color(MY_WHITE),
            plane.get_y_axis_label("y").set_color(MY_WHITE)
        )

        self.play(Create(plane), Create(axes_labels), run_time=1.5)
        self.wait(0.5)

        # Parabola y = x^2 - 4
        func = lambda x: x**2 - 4
        parabola = plane.get_graph(func, color=MY_BLUE, stroke_width=4)

        x_intercept_1 = plane.coords_to_point(-2, 0)
        x_intercept_2 = plane.coords_to_point(2, 0)

        dot1 = Dot(x_intercept_1, color=MY_GOLD, radius=0.15)
        dot2 = Dot(x_intercept_2, color=MY_GOLD, radius=0.15)
        
        label_intercepts = Text("X-intercepts", font_size=30, color=MY_WHITE).next_to(dot1, UL).shift(0.5*RIGHT)
        arrow1 = Arrow(label_intercepts.get_bottom(), dot1.get_top(), buff=0.1, color=MY_WHITE)
        arrow2 = Arrow(label_intercepts.get_bottom(), dot2.get_top(), buff=0.1, color=MY_WHITE)
        
        self.play(Create(parabola), run_time=2)
        self.play(
            LaggedStart(
                GrowFromCenter(dot1),
                GrowFromCenter(dot2),
                Write(label_intercepts),
                GrowArrow(arrow1),
                GrowArrow(arrow2),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.wait(1)

        intro_text = Text("Quadratic equations...").scale(0.8).to_edge(UP, buff=0.75).set_color(MY_WHITE)
        intro_text_2 = Text("...form parabolas.").scale(0.8).next_to(intro_text, DOWN).set_color(MY_WHITE)

        self.play(Write(intro_text))
        self.play(Write(intro_text_2))
        self.wait(1)
        
        equation_text = self.create_quadratic_expression_text(1, 0, -4).scale(0.7).to_corner(UL)
        
        self.play(FadeOut(label_intercepts, arrow1, arrow2, intro_text, intro_text_2))
        self.play(Write(equation_text))
        self.wait(1)

        roots_text = Text("These X-intercepts are the 'solutions' or 'roots'!", color=MY_GOLD).scale(0.7).to_edge(UP, buff=0.75)
        self.play(FadeTransform(equation_text, roots_text))
        self.wait(1.5)
        
        self.play(FadeOut(roots_text, dot1, dot2))
        self.wait(0.5)

        self.plane = plane
        self.parabola = parabola

    def beat_2_axis_of_symmetry(self):
        # Focus on a more general parabola y = x^2 - 2x - 3 (roots at -1, 3)
        func_2 = lambda x: x**2 - 2*x - 3
        new_parabola = self.plane.get_graph(func_2, color=MY_BLUE, stroke_width=4)
        
        equation_text = self.create_quadratic_expression_text(1, -2, -3).scale(0.7).to_corner(UL)
        
        self.play(
            ReplacementTransform(self.parabola, new_parabola),
            Create(equation_text)
        )
        self.wait(1)

        sym_text = Text("Parabolas are SYMMETRIC.", color=MY_WHITE).scale(0.7).to_edge(UP, buff=0.75)
        self.play(Write(sym_text))
        self.wait(1)

        # Axis of symmetry x = -b/(2a) for x^2 - 2x - 3 => x = -(-2)/(2*1) = 1
        axis_x_coord = 1
        axis_of_symmetry = DashedLine(
            self.plane.coords_to_point(axis_x_coord, self.plane.y_range[0]),
            self.plane.coords_to_point(axis_x_coord, self.plane.y_range[1]),
            color=MY_GOLD
        )
        
        # Manually constructing x = -b/2a using Text and Line
        x_label = Text("x", color=MY_GOLD).scale(0.6)
        equals = Text(" = ", color=MY_WHITE).scale(0.6)
        
        numerator = Text("-b", color=MY_BLUE).scale(0.6)
        denominator = Text("2a", color=MY_BLUE).scale(0.6)
        fraction_line = Line(LEFT*0.3, RIGHT*0.3, color=MY_WHITE, stroke_width=2)
        fraction_line.move_to(VGroup(numerator, denominator).get_center()) # Center the line between terms
        
        neg_b_over_2a_vg = VGroup(numerator, fraction_line, denominator).arrange(DOWN, center=True, buff=0.1)
        
        axis_label = VGroup(x_label, equals, neg_b_over_2a_vg).arrange(RIGHT, buff=0.1).move_to(axis_of_symmetry.get_bottom()).shift(0.5*DOWN)
        
        self.play(Create(axis_of_symmetry), run_time=1.5)
        self.play(Write(axis_label))
        self.wait(1)

        roots = [-1, 3] # for x^2 - 2x - 3
        root_dots = VGroup(
            Dot(self.plane.coords_to_point(roots[0], 0), color=MY_GOLD, radius=0.15),
            Dot(self.plane.coords_to_point(roots[1], 0), color=MY_GOLD, radius=0.15)
        )
        
        self.play(GrowFromCenter(root_dots))
        self.wait(0.5)

        # Show symmetry with arrows
        arrow_left = Arrow(axis_of_symmetry.get_center() + 0.5*LEFT, root_dots[0].get_center(), buff=0.1, color=MY_GOLD, max_stroke_width_to_length_ratio=0.1)
        arrow_right = Arrow(axis_of_symmetry.get_center() + 0.5*RIGHT, root_dots[1].get_center(), buff=0.1, color=MY_GOLD, max_stroke_width_to_length_ratio=0.1)

        self.play(GrowArrow(arrow_left), GrowArrow(arrow_right))
        self.wait(1)

        self.play(FadeOut(sym_text, arrow_left, arrow_right))
        self.wait(0.5)

        self.parabola = new_parabola
        self.equation_text = equation_text
        self.axis_of_symmetry = axis_of_symmetry
        self.axis_label = axis_label
        self.root_dots = root_dots
        self.axis_x_coord = axis_x_coord

    def beat_3_distance_from_symmetry(self):
        distance_text = Text("The roots are equidistant from this axis.", color=MY_WHITE).scale(0.7).to_edge(UP, buff=0.75)
        self.play(Write(distance_text))
        self.wait(1)

        # Highlight the distance segments
        distance_line_left = Line(
            self.plane.coords_to_point(self.axis_x_coord, 0),
            self.root_dots[0].get_center(),
            color=MY_BLUE, stroke_width=4
        )
        distance_line_right = Line(
            self.plane.coords_to_point(self.axis_x_coord, 0),
            self.root_dots[1].get_center(),
            color=MY_BLUE, stroke_width=4
        )

        self.play(Create(distance_line_left), Create(distance_line_right))
        self.wait(1)

        # Label the distance
        dist_label = Text("distance", color=MY_BLUE).scale(0.5).next_to(distance_line_right, UP, buff=0.1)
        self.play(Write(dist_label))
        self.wait(1)

        # Introduce the idea that this distance depends on a, b, c
        depend_text = Text("This distance depends on 'a', 'b', and 'c'.", color=MY_WHITE).scale(0.7).to_edge(UP, buff=0.75)
        self.play(ReplacementTransform(distance_text, depend_text))
        self.wait(1.5)

        self.play(FadeOut(depend_text, distance_line_left, distance_line_right, dist_label))
        self.wait(0.5)

    def beat_4_the_formula(self):
        # Bring back the axis of symmetry and the roots
        self.play(
            FadeIn(self.root_dots),
            FadeIn(self.axis_of_symmetry),
            FadeIn(self.axis_label)
        )
        self.wait(0.5)

        x_equals = Text("x = ", color=MY_WHITE).scale(0.8)
        
        # Reuse neg_b_2a_vg from axis_label and scale it
        neg_b_2a_part = self.axis_label[2].copy().scale(0.8/0.6) # Scale from 0.6 back to 0.8
        
        plus_minus = Text(" ± ", color=MY_WHITE).scale(0.8)

        # Manually constructing sqrt(b^2 - 4ac) / 2a
        sqrt_b2_4ac_numerator_parts = VGroup(
            Text("sqrt(", color=MY_GOLD),
            Text("b", color=MY_GOLD),
            Text("2", color=MY_GOLD).scale(0.5).shift(0.1*UP+0.05*RIGHT),
            Text(" - 4ac", color=MY_GOLD),
            Text(")", color=MY_GOLD)
        ).arrange(RIGHT, buff=0.05)
        
        denominator_2a = Text("2a", color=MY_BLUE).scale(0.8)
        
        # Create a line long enough for the numerator
        line_fraction = Line(LEFT, RIGHT, color=MY_WHITE, stroke_width=3) 
        line_fraction.set_width(sqrt_b2_4ac_numerator_parts.get_width() + 0.2) # Make line wider than numerator
        
        sqrt_fraction = VGroup(sqrt_b2_4ac_numerator_parts, line_fraction, denominator_2a).arrange(DOWN, center=True, buff=0.1)
        
        # Adjust vertical position of line_fraction
        line_fraction.move_to(VGroup(sqrt_b2_4ac_numerator_parts, denominator_2a).get_center())

        # First part of the formula: x = -b/2a
        formula_part_1 = VGroup(x_equals, neg_b_2a_part).arrange(RIGHT, buff=0.1).to_edge(UL, buff=1)
        self.play(ReplacementTransform(self.axis_label, formula_part_1))
        self.wait(1)

        # Second part of the formula: ± sqrt(...)
        formula_part_2 = VGroup(plus_minus, sqrt_fraction).arrange(RIGHT, buff=0.1)
        
        # Position formula_part_2 relative to formula_part_1
        full_formula_obj = VGroup(formula_part_1, formula_part_2).arrange(RIGHT, buff=0.1).to_edge(UL, buff=1)
        
        self.play(Write(formula_part_2, run_time=2))
        self.wait(1)

        quad_formula_text = Text("The Quadratic Formula!", color=MY_GOLD).scale(0.7).next_to(full_formula_obj, DOWN, buff=0.75)
        
        self.play(FadeOut(self.equation_text))
        self.play(Write(quad_formula_text))
        self.wait(2)

        # Show the roots as x1 and x2
        x1_label = Text("x₁", color=MY_GOLD).scale(0.6).next_to(self.root_dots[0], DOWN, buff=0.1)
        x2_label = Text("x₂", color=MY_GOLD).scale(0.6).next_to(self.root_dots[1], DOWN, buff=0.1)
        
        self.play(Write(x1_label), Write(x2_label))
        self.wait(1)
        
        self.play(
            FadeOut(self.parabola, self.axis_of_symmetry, self.root_dots, x1_label, x2_label),
            FadeOut(quad_formula_text)
        )
        self.wait(0.5)

        self.full_formula_obj = full_formula_obj

    def beat_5_recap(self):
        # Fade out everything except the formula and bring it to center for emphasis
        self.play(
            FadeOut(self.plane),
            self.full_formula_obj.animate.to_center(),
            run_time=1.5
        )
        self.wait(0.5)

        recap_title = Text("Geometric Meaning Recap", color=MY_GOLD).scale(0.9).to_edge(UP, buff=0.75)
        self.play(Write(recap_title))
        self.wait(1)

        recap_points = VGroup(
            Text("1. Quadratic equations form parabolas.", color=MY_WHITE),
            Text("2. Solutions (roots) are X-intercepts.", color=MY_BLUE),
            Text("3. Axis of symmetry: x = -b/(2a).", color=MY_GOLD),
            Text("4. Roots are equidistant from the axis.", color=MY_BLUE),
            Text("5. The formula is: symmetry ± distance.", color=MY_WHITE)
        ).scale(0.6).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(recap_title, DOWN, buff=0.75)

        self.play(
            LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.75),
            run_time=4
        )
        self.wait(3)
        self.play(
            FadeOut(recap_title, recap_points, self.full_formula_obj)
        )