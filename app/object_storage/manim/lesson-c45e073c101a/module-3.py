from manim import *
import numpy as np # For np.array

class ParabolaXInterceptsDiscriminant(Scene):
    def construct(self):
        # Configuration
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C
        TEXT_COLOR = WHITE

        # --- Utility Functions for Text Expressions (since no Tex/MathTex) ---
        def create_discriminant_expression_only():
            """Creates a VGroup representing 'b^2 - 4ac' using Text objects."""
            b_base = Text("b", color=BLUE_ACCENT).scale(0.8)
            pow2 = Text("^2", color=TEXT_COLOR).scale(0.5).next_to(b_base, UP+RIGHT, buff=0.02)
            b2_group = VGroup(b_base, pow2)
            minus4ac = Text("- 4ac", color=TEXT_COLOR).scale(0.8)
            return VGroup(b2_group, minus4ac).arrange(RIGHT, buff=0.05)

        def create_quadratic_formula_text():
            """Creates a VGroup representing the quadratic formula using Text objects."""
            x_eq = Text("x =", color=TEXT_COLOR).scale(0.8)
            
            # Numerator parts
            num_b = Text("-b", color=BLUE_ACCENT).scale(0.8)
            pm_sym = Text(" ± ", color=TEXT_COLOR).scale(0.8)
            sqrt_text = Text("sqrt(", color=TEXT_COLOR).scale(0.8)

            discriminant_content_group = create_discriminant_expression_only()
            
            sqrt_full_group = VGroup(sqrt_text, discriminant_content_group, Text(")", color=TEXT_COLOR).scale(0.8)).arrange(RIGHT, buff=0.05)
            
            numerator_group = VGroup(num_b, pm_sym, sqrt_full_group).arrange(RIGHT, buff=0.1)

            # Denominator
            denominator_val = Text("2a", color=BLUE_ACCENT).scale(0.8)
            
            # Fraction line
            line_width = max(numerator_group.width, denominator_val.width) * 1.1
            fraction_line = Line(LEFT * line_width / 2, RIGHT * line_width / 2, color=TEXT_COLOR)
            
            # Position elements relative to a common center for horizontal alignment
            # This is a manual way to achieve what MathTex does automatically.
            fraction_line.move_to(ORIGIN) 
            
            # Position numerator above, denominator below, then re-center them horizontally
            # based on the fraction line's x-coordinate.
            numerator_group.next_to(fraction_line, UP, buff=0.1)
            denominator_val.next_to(fraction_line, DOWN, buff=0.1)
            
            numerator_group.move_to(np.array([fraction_line.get_center()[0], numerator_group.get_center()[1], 0]))
            denominator_val.move_to(np.array([fraction_line.get_center()[0], denominator_val.get_center()[1], 0]))

            full_fraction = VGroup(numerator_group, fraction_line, denominator_val)
            
            final_formula = VGroup(x_eq, full_fraction).arrange(RIGHT, buff=0.2)
            
            return final_formula, discriminant_content_group

        # --- Scene Setup ---
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 10, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": WHITE},
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 0.5,
                "stroke_opacity": 0.4,
            }
        ).add_coordinates()
        plane.axes.set_color(WHITE)
        
        # Adjust coordinate labels color for better contrast
        for coord_label in plane.coordinate_labels:
            coord_label.set_color(GREY_A)

        # --- Beat 1: Introduction - What are X-Intercepts? ---
        title = Text("Parabola X-Intercepts", color=TEXT_COLOR).scale(1.2).to_edge(UP)
        
        definition = Text("Where the parabola crosses the x-axis.", color=TEXT_COLOR).scale(0.7)
        definition.next_to(title, DOWN, buff=0.5)

        parabola_1 = plane.get_graph(lambda x: x**2 - 4, x_range=[-3, 3], color=BLUE_ACCENT)
        intercept_1a = Dot(plane.coords_to_point(-2, 0), color=GOLD_ACCENT, radius=0.12)
        intercept_1b = Dot(plane.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.12)
        intercept_label = Text("X-Intercepts", color=GOLD_ACCENT).scale(0.6).next_to(intercept_1b, DR, buff=0.2)

        self.add(plane)
        self.play(
            FadeIn(title, shift=UP),
            FadeIn(definition, shift=UP),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            Create(parabola_1, run_time=2),
            LaggedStart(
                GrowFromCenter(intercept_1a),
                GrowFromCenter(intercept_1b),
                lag_ratio=0.5, run_time=1
            )
        )
        self.play(Write(intercept_label))
        self.wait(1.5)
        self.play(FadeOut(definition, intercept_label))


        # --- Beat 2: Three Cases - Visualizing the Possibilities ---
        cases_title = Text("Three Possibilities:", color=TEXT_COLOR).scale(0.9).next_to(title, DOWN, buff=0.5)
        self.play(ReplacementTransform(title, title), FadeIn(cases_title, shift=UP))
        
        # Case 1: Two Intercepts
        parabola_current = parabola_1 
        intercepts_current = VGroup(intercept_1a, intercept_1b)
        label_current = Text("Two Intercepts", color=GOLD_ACCENT).scale(0.7).next_to(cases_title, DOWN, buff=0.8)

        self.play(FadeIn(label_current))
        self.play(FadeIn(intercepts_current))
        self.wait(1)
        
        # Case 2: One Intercept
        parabola_one_intercept = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=BLUE_ACCENT)
        intercept_one = Dot(plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.12)
        label_one = Text("One Intercept", color=GOLD_ACCENT).scale(0.7).move_to(label_current.get_center())

        self.play(
            Transform(parabola_current, parabola_one_intercept),
            FadeOut(intercepts_current),
            Transform(label_current, label_one)
        )
        intercepts_current = VGroup(intercept_one) 
        self.play(GrowFromCenter(intercepts_current))
        self.wait(1)

        # Case 3: No Intercepts
        parabola_no_intercepts = plane.get_graph(lambda x: x**2 + 4, x_range=[-3, 3], color=BLUE_ACCENT)
        label_none = Text("No Intercepts", color=GOLD_ACCENT).scale(0.7).move_to(label_current.get_center())

        self.play(
            Transform(parabola_current, parabola_no_intercepts),
            FadeOut(intercepts_current),
            Transform(label_current, label_none)
        )
        intercepts_current = VGroup() 
        self.wait(1)

        self.play(
            FadeOut(parabola_current, label_current, cases_title),
            title.animate.center().to_edge(UP)
        )

        # --- Beat 3: Connecting to the Quadratic Formula (Intuition First) ---
        quadratic_equation_text = Text("y = ax^2 + bx + c", color=TEXT_COLOR).scale(0.9)
        quadratic_equation_text.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(quadratic_equation_text, shift=UP))
        self.wait(0.5)

        y_is_zero_text = Text("At x-intercepts, y = 0", color=TEXT_COLOR).scale(0.7).next_to(quadratic_equation_text, DOWN, buff=0.3)
        self.play(FadeIn(y_is_zero_text, shift=UP))
        self.wait(0.5)

        zero_eq = Text("ax^2 + bx + c = 0", color=TEXT_COLOR).scale(0.9)
        zero_eq.move_to(y_is_zero_text.get_center())
        self.play(Transform(y_is_zero_text, zero_eq))
        self.wait(1)

        formula_label = Text("Solutions come from the Quadratic Formula:", color=TEXT_COLOR).scale(0.7).next_to(y_is_zero_text, DOWN, buff=0.5)
        self.play(FadeIn(formula_label, shift=UP))
        self.wait(0.5)
        
        quadratic_formula_group, discriminant_part_in_formula = create_quadratic_formula_text()
        quadratic_formula_group.next_to(formula_label, DOWN, buff=0.5)
        
        self.play(FadeIn(quadratic_formula_group, shift=UP))
        self.wait(1)

        discriminant_highlight = SurroundingRectangle(discriminant_part_in_formula, color=GOLD_ACCENT, buff=0.1)
        discriminant_name = Text("The Discriminant", color=GOLD_ACCENT).scale(0.7).next_to(discriminant_highlight, DOWN, buff=0.3)
        
        self.play(Create(discriminant_highlight))
        self.play(Write(discriminant_name))
        self.wait(2)
        
        self.play(
            FadeOut(formula_label, quadratic_formula_group, discriminant_highlight, quadratic_equation_text, y_is_zero_text, discriminant_name),
            title.animate.center().to_edge(UP)
        )

        # --- Beat 4: Formalizing the Discriminant's Role ---
        discriminant_label = Text("Discriminant: D =", color=TEXT_COLOR).scale(0.9)
        discriminant_expression = create_discriminant_expression_only()
        discriminant_expression.set_color(GOLD_ACCENT) 
        
        initial_discriminant_display = VGroup(discriminant_label, discriminant_expression).arrange(RIGHT, buff=0.1).next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(initial_discriminant_display, shift=UP))
        self.wait(1)
        
        parabola_active = plane.get_graph(lambda x: x**2 - 2, x_range=[-3, 3], color=BLUE_ACCENT)
        self.play(Create(parabola_active))
        self.wait(0.5)

        # Case D > 0
        d_val_greater_zero = Text("> 0", color=GOLD_ACCENT).scale(1.1)
        d_greater_zero_display = VGroup(initial_discriminant_display.copy(), d_val_greater_zero).arrange(RIGHT, buff=0.1).next_to(title, DOWN, buff=0.5)
        
        outcome_two_intercepts = Text("Two X-Intercepts", color=GOLD_ACCENT).scale(0.7).next_to(d_greater_zero_display, DOWN, buff=0.3)
        
        self.play(
            Transform(initial_discriminant_display, d_greater_zero_display), 
            FadeIn(outcome_two_intercepts, shift=UP),
            FadeOut(parabola_active)
        )
        parabola_greater_zero = plane.get_graph(lambda x: x**2 - 4, x_range=[-3, 3], color=BLUE_ACCENT)
        intercept_g1 = Dot(plane.coords_to_point(-2, 0), color=GOLD_ACCENT, radius=0.12)
        intercept_g2 = Dot(plane.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.12)
        self.play(
            Create(parabola_greater_zero),
            LaggedStart(GrowFromCenter(intercept_g1), GrowFromCenter(intercept_g2), lag_ratio=0.5)
        )
        self.wait(1.5)

        # Case D = 0
        d_val_equals_zero = Text("= 0", color=GOLD_ACCENT).scale(1.1)
        d_equals_zero_display = VGroup(d_greater_zero_display[0].copy(), d_val_equals_zero).arrange(RIGHT, buff=0.1).next_to(title, DOWN, buff=0.5)
        outcome_one_intercept = Text("One X-Intercept", color=GOLD_ACCENT).scale(0.7).move_to(outcome_two_intercepts.get_center())

        self.play(
            Transform(d_greater_zero_display, d_equals_zero_display),
            Transform(outcome_two_intercepts, outcome_one_intercept),
            Transform(parabola_greater_zero, plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=BLUE_ACCENT)),
            FadeOut(intercept_g1, intercept_g2)
        )
        intercept_e1 = Dot(plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.12)
        self.play(GrowFromCenter(intercept_e1))
        self.wait(1.5)

        # Case D < 0
        d_val_less_zero = Text("< 0", color=GOLD_ACCENT).scale(1.1)
        d_less_zero_display = VGroup(d_equals_zero_display[0].copy(), d_val_less_zero).arrange(RIGHT, buff=0.1).next_to(title, DOWN, buff=0.5)
        outcome_no_intercepts = Text("No X-Intercepts", color=GOLD_ACCENT).scale(0.7).move_to(outcome_two_intercepts.get_center())
        
        self.play(
            Transform(d_greater_zero_display, d_less_zero_display), 
            Transform(outcome_two_intercepts, outcome_no_intercepts),
            Transform(parabola_greater_zero, plane.get_graph(lambda x: x**2 + 4, x_range=[-3, 3], color=BLUE_ACCENT)),
            FadeOut(intercept_e1)
        )
        self.wait(1.5)

        self.play(
            FadeOut(parabola_greater_zero, d_greater_zero_display, outcome_two_intercepts)
        )

        # --- Beat 5: Recap Card ---
        self.play(FadeOut(plane))
        recap_title = Text("Recap: The Discriminant", color=TEXT_COLOR).scale(1.2).to_edge(UP)

        recap_d_label = Text("D =", color=TEXT_COLOR).scale(0.8)
        recap_d_expression = create_discriminant_expression_only().set_color(GOLD_ACCENT)
        recap_d_formula = VGroup(recap_d_label, recap_d_expression).arrange(RIGHT, buff=0.1)
        recap_d_formula.next_to(recap_title, DOWN, buff=0.8)

        # Create recap bullets with explicit Text objects for value and description
        bullet1_value = Text("> 0", color=GOLD_ACCENT).scale(0.8)
        bullet1_desc = Text(" : Two X-Intercepts", color=TEXT_COLOR).scale(0.8)
        recap_bullet1 = VGroup(bullet1_value, bullet1_desc).arrange(RIGHT, buff=0.1)
        
        bullet2_value = Text("= 0", color=GOLD_ACCENT).scale(0.8)
        bullet2_desc = Text(" : One X-Intercept", color=TEXT_COLOR).scale(0.8)
        recap_bullet2 = VGroup(bullet2_value, bullet2_desc).arrange(RIGHT, buff=0.1)

        bullet3_value = Text("< 0", color=GOLD_ACCENT).scale(0.8)
        bullet3_desc = Text(" : No X-Intercepts", color=TEXT_COLOR).scale(0.8)
        recap_bullet3 = VGroup(bullet3_value, bullet3_desc).arrange(RIGHT, buff=0.1)

        recap_list = VGroup(recap_bullet1, recap_bullet2, recap_bullet3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        recap_list.next_to(recap_d_formula, DOWN, buff=0.8).align_to(recap_d_formula, LEFT)

        self.play(
            FadeOut(title),
            FadeIn(recap_title, shift=UP)
        )
        self.wait(0.5)
        self.play(Write(recap_d_formula))
        self.play(
            LaggedStart(
                Write(recap_bullet1),
                Write(recap_bullet2),
                Write(recap_bullet3),
                lag_ratio=0.7, run_time=3
            )
        )
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_d_formula, recap_list)))
        self.wait(1)