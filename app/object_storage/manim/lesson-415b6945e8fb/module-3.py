from manim import *

class GraphingQuadratics(Scene):
    def construct(self):
        # --- Configuration & Helper Functions ---
        config.background_color = "#1A1A1A"  # Very dark gray, almost black
        BLUE_ACCENT = "#58C4DD" # Manim's BLUE_E is a bit dark, using a brighter blue
        GOLD_ACCENT = "#FFD700" # Manim's GOLD_E is a bit dark, using a brighter gold
        DARK_TEXT = "#CCCCCC"  # For general text that contrasts well
        LIGHT_TEXT = "#FFFFFF"  # For important highlights

        # Helper to create equation text without Tex
        def create_quadratic_text(a_val, b_val, c_val):
            y_eq_part = Text("y = ", color=DARK_TEXT, font_size=36)
            
            terms = []
            if a_val != 0:
                a_str = ""
                if a_val == 1: a_str = "x²"
                elif a_val == -1: a_str = "-x²"
                else: a_str = f"{a_val}x²"
                terms.append(Text(a_str, color=GOLD_ACCENT, font_size=36))
            
            if b_val != 0:
                b_str = ""
                if b_val > 0: b_str += " + "
                else: b_str += " - "
                if abs(b_val) == 1: b_str += "x"
                else: b_str += f"{abs(b_val)}x"
                terms.append(Text(b_str, color=BLUE_ACCENT, font_size=36))
            
            if c_val != 0:
                c_str = ""
                if c_val > 0: c_str += " + "
                else: c_str += " - "
                c_str += f"{abs(c_val)}"
                terms.append(Text(c_str, color=DARK_TEXT, font_size=36))

            if not terms: # Case y = 0
                return Text("y = 0", color=DARK_TEXT, font_size=36)

            equation = VGroup(y_eq_part)
            for term in terms:
                equation.add(term.next_to(equation[-1], RIGHT, buff=0.1))
            
            return equation

        # Helper for discriminant text
        def create_discriminant_text(b_val, a_val, c_val, sign_str=""):
            b_sq = Text(f"{b_val}²", color=BLUE_ACCENT, font_size=36)
            
            # Constructing - 4ac part
            op = Text(" - ", color=DARK_TEXT, font_size=36)
            four_ac = VGroup(
                Text("4", color=GOLD_ACCENT, font_size=36),
                Text("(", color=DARK_TEXT, font_size=36),
                Text(str(a_val), color=GOLD_ACCENT, font_size=36),
                Text(")", color=DARK_TEXT, font_size=36),
                Text("(", color=DARK_TEXT, font_size=36),
                Text(str(c_val), color=GOLD_ACCENT, font_size=36),
                Text(")", color=DARK_TEXT, font_size=36),
            ).arrange(RIGHT, buff=0.05)

            formula = VGroup(b_sq, op.next_to(b_sq, RIGHT, buff=0.1), four_ac.next_to(op, RIGHT, buff=0.1))
            
            if sign_str:
                sign = Text(f" {sign_str}", color=DARK_TEXT, font_size=36)
                formula.add(sign.next_to(formula[-1], RIGHT, buff=0.1))
            return formula

        # --- Scene Setup: Title and NumberPlane ---
        title = Text("Graphing Quadratics and the Discriminant", font_size=48, color=LIGHT_TEXT)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Main graphing area
        self.plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": "#444444"},
            background_line_style={"stroke_color": "#222222", "stroke_width": 1, "stroke_opacity": 0.8},
        ).add_coordinates(font_size=20, color="#666666") # Added coordinates for clarity
        self.plane.shift(DOWN * 0.5 + LEFT * 2) # Position the plane

        self.play(FadeIn(self.plane))
        self.wait(0.5)

        # --- Beat 1: Intro Hook - The basic Parabola y = x² ---
        intro_text = Text("Every quadratic equation corresponds to a parabola.", color=DARK_TEXT, font_size=36)
        intro_text.next_to(title, DOWN, buff=1)
        
        # A dynamic hook: a point tracing y=x^2
        dot = Dot(self.plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.08)
        path = VMobject(stroke_color=BLUE_ACCENT, stroke_width=4)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])

        def update_path(p):
            p.add_points_as_corners([dot.get_center()])

        initial_parabola_func = lambda x: x**2
        initial_parabola_graph = self.plane.get_graph(initial_parabola_func, color=BLUE_ACCENT, x_range=[-3, 3])

        self.play(
            FadeIn(intro_text),
            Create(dot)
        )
        self.wait(0.5)

        self.add(path)
        path.add_updater(update_path)
        
        self.play(
            FadeOut(intro_text),
            MoveAlongPath(dot, self.plane.get_graph(initial_parabola_func, x_range=[-3, 3]), run_time=2.5, rate_func=linear)
        )
        path.remove_updater(update_path)
        self.remove(dot) # Remove the dot, keep the path

        # Show initial equation y = x^2
        current_a, current_b, current_c = 1, 0, 0
        current_quadratic_text = create_quadratic_text(current_a, current_b, current_c)
        current_quadratic_text.to_edge(RIGHT).shift(UP * 2)

        self.play(
            ReplacementTransform(path, initial_parabola_graph),
            Write(current_quadratic_text)
        )
        self.wait(1)

        general_form_label = Text("General Form:", color=DARK_TEXT, font_size=32)
        general_form_label.next_to(current_quadratic_text, DOWN, buff=0.5).align_to(current_quadratic_text, LEFT)
        general_form_equation = Text("y = ax² + bx + c", color=LIGHT_TEXT, font_size=32)
        general_form_equation.next_to(general_form_label, RIGHT, buff=0.2)
        general_form_group = VGroup(general_form_label, general_form_equation)

        self.play(FadeIn(general_form_group, shift=UP))
        self.wait(1)
        self.play(FadeOut(general_form_group)) # Hide for now to declutter

        # --- Beat 2: The 'a' coefficient - Shape and Direction ---
        a_effect_text = Text("Coefficient 'a': Shape & Direction", color=GOLD_ACCENT, font_size=32)
        a_effect_text.move_to(current_quadratic_text).align_to(current_quadratic_text, LEFT)
        
        self.play(
            Transform(current_quadratic_text, a_effect_text)
        )
        self.wait(0.5)

        # Animate 'a' changing
        a_vals = [2, 0.5, -1] # Values to demonstrate
        for i, val in enumerate(a_vals):
            new_a = val
            new_graph = self.plane.get_graph(lambda x: new_a * x**2, color=BLUE_ACCENT, x_range=[-3.5, 3.5])
            new_a_text = create_quadratic_text(new_a, 0, 0)
            new_a_text.move_to(a_effect_text).align_to(a_effect_text, LEFT)

            self.play(
                Transform(initial_parabola_graph, new_graph),
                Transform(a_effect_text, new_a_text),
                run_time=1.5
            )
            current_a = new_a
            self.wait(0.5)
        
        # Reset to y = x^2 before next beat
        reset_graph = self.plane.get_graph(lambda x: 1 * x**2, color=BLUE_ACCENT, x_range=[-3.5, 3.5])
        reset_text = create_quadratic_text(1, 0, 0)
        reset_text.move_to(a_effect_text).align_to(a_effect_text, LEFT)
        self.play(
            Transform(initial_parabola_graph, reset_graph),
            Transform(a_effect_text, reset_text)
        )
        current_quadratic_text = reset_text # Update reference for next beat
        self.wait(0.5)

        # --- Beat 3: The 'c' coefficient - Vertical Shift ---
        c_effect_text = Text("Coefficient 'c': Vertical Shift", color=DARK_TEXT, font_size=32)
        c_effect_text.move_to(current_quadratic_text).align_to(current_quadratic_text, LEFT)
        
        current_quadratic_text_with_c = create_quadratic_text(current_a, 0, current_c)
        current_quadratic_text_with_c.move_to(current_quadratic_text).align_to(current_quadratic_text, LEFT)
        
        self.play(
            ReplacementTransform(a_effect_text, c_effect_text),
            Transform(current_quadratic_text, current_quadratic_text_with_c)
        )
        self.wait(0.5)

        # Animate 'c' changing
        c_vals = [2, -3, 0] # Values to demonstrate
        for i, val in enumerate(c_vals):
            new_c = val
            new_graph = self.plane.get_graph(lambda x: current_a * x**2 + new_c, color=BLUE_ACCENT, x_range=[-3.5, 3.5])
            new_c_text = create_quadratic_text(current_a, 0, new_c)
            new_c_text.move_to(c_effect_text).align_to(c_effect_text, LEFT)

            self.play(
                Transform(initial_parabola_graph, new_graph),
                Transform(current_quadratic_text, new_c_text),
                run_time=1.5
            )
            current_c = new_c
            self.wait(0.5)
        
        # Reset to y = x^2 before next beat
        reset_graph = self.plane.get_graph(lambda x: 1 * x**2, color=BLUE_ACCENT, x_range=[-3.5, 3.5])
        reset_text = create_quadratic_text(1, 0, 0)
        reset_text.move_to(c_effect_text).align_to(c_effect_text, LEFT)
        self.play(
            Transform(initial_parabola_graph, reset_graph),
            Transform(current_quadratic_text, reset_text)
        )
        current_a, current_b, current_c = 1, 0, 0 # Reset all
        self.wait(0.5)

        # --- Beat 4: The 'b' coefficient - Horizontal Shift of Vertex ---
        b_effect_text = Text("Coefficient 'b': Horizontal Vertex Shift", color=BLUE_ACCENT, font_size=32)
        b_effect_text.move_to(current_quadratic_text).align_to(current_quadratic_text, LEFT)
        
        current_quadratic_text_with_b = create_quadratic_text(current_a, current_b, current_c)
        current_quadratic_text_with_b.move_to(current_quadratic_text).align_to(current_quadratic_text, LEFT)

        self.play(
            ReplacementTransform(c_effect_text, b_effect_text),
            Transform(current_quadratic_text, current_quadratic_text_with_b)
        )
        self.wait(0.5)

        # Animate 'b' changing
        b_vals = [2, -4, 0] # Values to demonstrate (a=1, c=0 for simplicity)
        for i, val in enumerate(b_vals):
            new_b = val
            new_graph = self.plane.get_graph(lambda x: current_a * x**2 + new_b * x + current_c, color=BLUE_ACCENT, x_range=[-5, 5])
            new_b_text = create_quadratic_text(current_a, new_b, current_c)
            new_b_text.move_to(b_effect_text).align_to(b_effect_text, LEFT)

            self.play(
                Transform(initial_parabola_graph, new_graph),
                Transform(current_quadratic_text, new_b_text),
                run_time=1.5
            )
            current_b = new_b
            self.wait(0.5)

        # Final setup for discriminant section: y = x^2 - 2x - 3 (two roots)
        current_a, current_b, current_c = 1, -2, -3 
        final_graph = self.plane.get_graph(lambda x: current_a * x**2 + current_b * x + current_c, color=BLUE_ACCENT, x_range=[-5, 5])
        final_text = create_quadratic_text(current_a, current_b, current_c)
        final_text.move_to(b_effect_text).align_to(b_effect_text, LEFT)

        self.play(
            FadeOut(b_effect_text),
            Transform(initial_parabola_graph, final_graph),
            Transform(current_quadratic_text, final_text)
        )
        self.wait(1)

        # --- Beat 5: The Discriminant - Number of Roots ---
        discriminant_intro = Text("How many times does it cross the x-axis?", color=DARK_TEXT, font_size=30)
        discriminant_intro.next_to(self.plane, UP, buff=0.5)
        self.play(FadeIn(discriminant_intro))
        self.wait(1)

        # Move parabola to make space for discriminant explanation on the right
        self.play(self.plane.animate.shift(LEFT*2.5), initial_parabola_graph.animate.shift(LEFT*2.5))
        
        current_quadratic_text.animate.to_edge(UP).shift(LEFT * 0.5)
        self.play(current_quadratic_text.animate)
        self.wait(0.5)

        discriminant_formula_label = Text("Discriminant:", color=LIGHT_TEXT, font_size=32)
        discriminant_formula_label.move_to(title).align_to(title, LEFT).shift(RIGHT * 3.5) # Position next to current_quadratic_text

        discriminant_formula_initial = create_discriminant_text(current_b, current_a, current_c)
        discriminant_formula_initial.next_to(discriminant_formula_label, RIGHT, buff=0.2)
        
        self.play(
            FadeOut(discriminant_intro),
            Write(discriminant_formula_label),
            Write(discriminant_formula_initial)
        )
        self.wait(1)

        # Case 1: D > 0 (Two roots)
        case1_text = Text("> 0 (Two real roots)", color=GOLD_ACCENT, font_size=30)
        case1_text.next_to(discriminant_formula_label, DOWN, buff=0.5).align_to(discriminant_formula_label, LEFT)
        
        # Current example: y = x^2 - 2x - 3 (D = (-2)^2 - 4(1)(-3) = 4 + 12 = 16 > 0)
        x_intercepts = [Dot(self.plane.coords_to_point(-1, 0), color=GOLD_ACCENT), Dot(self.plane.coords_to_point(3, 0), color=GOLD_ACCENT)]
        
        arrow_group_1 = VGroup()
        for intercept in x_intercepts:
            arrow_group_1.add(Arrow(start=discriminant_formula_initial.get_center(), end=intercept.get_center(), buff=0.2, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1))

        self.play(
            Write(case1_text),
            LaggedStart(
                *[FadeIn(x_i) for x_i in x_intercepts],
                *[Create(arrow) for arrow in arrow_group_1],
                lag_ratio=0.5
            )
        )
        self.wait(1.5)

        self.play(
            FadeOut(arrow_group_1),
            *[FadeOut(x_i) for x_i in x_intercepts]
        )

        # Case 2: D = 0 (One root)
        new_a, new_b, new_c = 1, -4, 4 # Example: y = x^2 - 4x + 4 = (x-2)^2 (D = 0)
        new_graph_equal_roots = self.plane.get_graph(lambda x: new_a * x**2 + new_b * x + new_c, color=BLUE_ACCENT, x_range=[-5, 5])
        new_quadratic_text_equal_roots = create_quadratic_text(new_a, new_b, new_c)
        new_quadratic_text_equal_roots.to_edge(UP).shift(LEFT * 0.5)

        new_discriminant_formula_eq_0 = create_discriminant_text(new_b, new_a, new_c, sign_str="= 0")
        new_discriminant_formula_eq_0.next_to(discriminant_formula_label, RIGHT, buff=0.2)

        case2_text = Text("= 0 (One real root)", color=BLUE_ACCENT, font_size=30)
        case2_text.next_to(discriminant_formula_label, DOWN, buff=0.5).align_to(discriminant_formula_label, LEFT)

        x_intercept_equal = Dot(self.plane.coords_to_point(2, 0), color=BLUE_ACCENT)
        arrow_equal = Arrow(start=new_discriminant_formula_eq_0.get_center(), end=x_intercept_equal.get_center(), buff=0.2, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.1)
        
        self.play(
            Transform(initial_parabola_graph, new_graph_equal_roots),
            Transform(current_quadratic_text, new_quadratic_text_equal_roots),
            Transform(discriminant_formula_initial, new_discriminant_formula_eq_0),
            ReplacementTransform(case1_text, case2_text),
            FadeIn(x_intercept_equal),
            Create(arrow_equal)
        )
        self.wait(1.5)

        self.play(FadeOut(x_intercept_equal), FadeOut(arrow_equal))

        # Case 3: D < 0 (No real roots)
        new_a, new_b, new_c = 1, -2, 3 # Example: y = x^2 - 2x + 3 (D = -8 < 0)
        new_graph_no_roots = self.plane.get_graph(lambda x: new_a * x**2 + new_b * x + new_c, color=BLUE_ACCENT, x_range=[-5, 5])
        new_quadratic_text_no_roots = create_quadratic_text(new_a, new_b, new_c)
        new_quadratic_text_no_roots.to_edge(UP).shift(LEFT * 0.5)

        new_discriminant_formula_lt_0 = create_discriminant_text(new_b, new_a, new_c, sign_str="< 0")
        new_discriminant_formula_lt_0.next_to(discriminant_formula_label, RIGHT, buff=0.2)

        case3_text = Text("< 0 (No real roots)", color=RED_A, font_size=30)
        case3_text.next_to(discriminant_formula_label, DOWN, buff=0.5).align_to(discriminant_formula_label, LEFT)

        self.play(
            Transform(initial_parabola_graph, new_graph_no_roots),
            Transform(current_quadratic_text, new_quadratic_text_no_roots),
            Transform(discriminant_formula_initial, new_discriminant_formula_lt_0),
            ReplacementTransform(case2_text, case3_text)
        )
        self.wait(2)

        self.play(
            FadeOut(initial_parabola_graph),
            FadeOut(current_quadratic_text),
            FadeOut(self.plane),
            FadeOut(discriminant_formula_label),
            FadeOut(discriminant_formula_initial),
            FadeOut(case3_text),
            FadeOut(title)
        )
        self.wait(0.5)

        # --- Beat 6: Recap Card ---
        recap_title = Text("Recap: Graphing Quadratics", color=LIGHT_TEXT, font_size=40)
        recap_title.to_edge(UP, buff=1)

        recap_points = VGroup(
            Text("• 'a': parabola shape & direction", color=DARK_TEXT, font_size=30),
            Text("• 'c': vertical shift", color=DARK_TEXT, font_size=30),
            Text("• 'b': horizontal shift of vertex", color=DARK_TEXT, font_size=30),
            Text("• Discriminant (b² - 4ac): number of x-intercepts", color=GOLD_ACCENT, font_size=30),
            Text("  > 0 : Two real roots", color=GOLD_ACCENT, font_size=24),
            Text("  = 0 : One real root", color=BLUE_ACCENT, font_size=24),
            Text("  < 0 : No real roots", color=RED_A, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        recap_points.next_to(recap_title, DOWN, buff=0.8).shift(LEFT * 1.5)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.5) for p in recap_points], lag_ratio=0.2))
        self.wait(2)

        call_to_action = Text("Ready to test your understanding?", color=LIGHT_TEXT, font_size=36)
        call_to_action.next_to(recap_points, DOWN, buff=1)
        self.play(FadeIn(call_to_action, shift=DOWN))
        self.wait(2)