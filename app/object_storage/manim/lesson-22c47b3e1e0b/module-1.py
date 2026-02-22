from manim import *

class QuadraticEquationsAnimation(Scene):
    def construct(self):
        # Set up general scene properties
        self.camera.background_color = BLACK
        blue_color = BLUE_D
        gold_color = GOLD
        white_color = WHITE

        # --- Helper function for custom text equations (NO Tex/MathTex) ---
        # This function aims to create math-like expressions using individual Text objects.
        # It primarily handles basic characters and simple superscripts by positioning them manually.
        def create_math_text_group(math_string, color=white_color, font_size=40):
            group = VGroup()
            temp_group = VGroup() # To build parts before grouping and centering

            i = 0
            while i < len(math_string):
                char = math_string[i]
                
                if char == '^' and i + 1 < len(math_string):
                    # Handle superscript: 'X^2' -> 'X' + small '2'
                    superscript_char = math_string[i+1]
                    t = Text(superscript_char, color=color, font_size=font_size * 0.7)
                    if temp_group:
                        # Position relative to the previous character (base of the superscript)
                        t.move_to(temp_group[-1].get_corner(UP + RIGHT) + RIGHT * 0.05 + UP * 0.05)
                    temp_group.add(t)
                    i += 2 # Skip '^' and the superscript character
                else:
                    t = Text(char, color=color, font_size=font_size)
                    if temp_group:
                        t.next_to(temp_group[-1], RIGHT, buff=0.1)
                    temp_group.add(t)
                    i += 1
            
            if temp_group:
                group.add(*temp_group)
                group.move_to(ORIGIN) # Center the resulting group
            return group

        # --- Beat 0: Visual Hook & Title ---
        title = Text("Understanding Quadratic Equations & Formula", color=gold_color, font_size=60)
        objective = Text("Unlocking the power of parabolas!", color=blue_color, font_size=30)
        objective.next_to(title, DOWN, buff=0.5)

        # Visual hook: A dynamic parabola
        plane_hook = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 5, 1],
            x_length=6, y_length=7,
            axis_config={"color": white_color, "stroke_width": 1},
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.4}
        ).shift(DOWN*0.5)
        
        # A simple parabola to form: y = x^2 - 1
        parabola_func_hook = lambda x: x**2 - 1
        graph_path_hook = plane_hook.get_graph(parabola_func_hook, x_range=[-2.5, 2.5], color=blue_color, stroke_width=4)

        self.play(
            LaggedStart(
                DrawBorderThenFill(plane_hook.axes),
                Create(plane_hook.background_lines),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.play(Create(graph_path_hook, run_time=1.5, rate_func=ease_out_sine))
        self.play(
            Write(title),
            FadeIn(objective, shift=UP),
            graph_path_hook.animate.scale(0.8).shift(LEFT*3),
            plane_hook.animate.scale(0.8).shift(LEFT*3),
            run_time=2
        )
        self.wait(1)
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(objective, shift=UP),
            FadeOut(graph_path_hook),
            FadeOut(plane_hook),
            run_time=1.5
        )

        # --- Beat 1: What is a Quadratic Equation? - The Parabola ---
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-4, 6, 1],
            x_length=10, y_length=8,
            axis_config={"color": white_color, "stroke_width": 1},
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.4}
        ).to_edge(LEFT, buff=0.5).scale(0.9)

        intro_text = Text("The Parabola: A special curve", color=gold_color, font_size=45).to_corner(UP + RIGHT).shift(LEFT * 0.5)

        # Manually create "y = x^2" using the helper
        y_eq_x_sq = create_math_text_group("y = x^2", font_size=40).to_corner(UP + RIGHT).shift(LEFT * 0.5 + DOWN * 0.8)

        self.play(
            LaggedStart(
                DrawBorderThenFill(plane.axes),
                Create(plane.background_lines),
                lag_ratio=0.5
            ),
            run_time=1.5
        )
        self.play(FadeIn(intro_text, shift=UP))
        self.wait(0.5)

        graph_x_squared = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=blue_color, stroke_width=4)
        self.play(Create(graph_x_squared))
        self.play(FadeIn(y_eq_x_sq))
        self.wait(1)

        # Real-world connection: illustrate a projectile path
        ball_path_text = Text("Think of a thrown ball...", color=white_color, font_size=30).next_to(y_eq_x_sq, DOWN, buff=0.5)
        self.play(Write(ball_path_text))
        
        ball = Circle(radius=0.1, color=gold_color, fill_opacity=1)
        # Create a VMobject path from the graph for MoveAlongPath
        graph_path = plane.get_graph(lambda x: x**2, x_range=[-2.5, 2.5])
        
        self.play(
            FadeIn(ball.move_to(plane.c2p(-2.5, (-2.5)**2))),
            MoveAlongPath(ball, graph_path, run_time=2.5)
        )
        self.play(FadeOut(ball), FadeOut(ball_path_text))
        self.wait(0.5)
        self.play(
            FadeOut(intro_text),
            FadeOut(y_eq_x_sq)
        )

        # --- Beat 2: The Coefficients a, b, c - Building the Equation ---
        general_form_label = Text("The General Form:", color=gold_color, font_size=45).to_corner(UP + RIGHT).shift(LEFT * 0.5)
        
        # Manually assemble ax^2 + bx + c = 0
        general_form_elements = create_math_text_group("ax^2 + bx + c = 0", font_size=40)
        general_form_elements.move_to(general_form_label.get_center() + DOWN * 1.5)

        self.play(FadeIn(general_form_label, shift=UP))
        self.play(Write(general_form_elements))
        self.wait(1)

        # Isolate 'a' for animation
        a_char = general_form_elements.submobjects[0] # 'a' in 'ax^2'
        
        a_value_display = DecimalNumber(1, num_decimal_places=1, color=gold_color, font_size=35).next_to(a_char, DOWN, buff=0.3)
        a_desc = Text(" (shape & direction)", color=white_color, font_size=25).next_to(a_value_display, RIGHT, buff=0.2)
        
        self.play(FadeIn(a_value_display), FadeIn(a_desc))

        graph_a_start = graph_x_squared.copy() # Current graph is y=x^2
        
        self.play(Transform(graph_a_start, plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=blue_color, stroke_width=4))) # Ensure it's the current state
        self.wait(0.5)
        
        # a = 0.5
        new_graph_a_0_5 = plane.get_graph(lambda x: 0.5*x**2, x_range=[-4, 4], color=BLUE_E, stroke_width=4)
        self.play(a_value_display.animate.set_value(0.5), Transform(graph_a_start, new_graph_a_0_5))
        self.wait(0.5)

        # a = -1
        new_graph_a_neg_1 = plane.get_graph(lambda x: -x**2, x_range=[-3, 3], color=GOLD, stroke_width=4)
        self.play(a_value_display.animate.set_value(-1.0), Transform(graph_a_start, new_graph_a_neg_1))
        self.wait(0.5)
        
        self.play(FadeOut(a_value_display), FadeOut(a_desc))
        self.wait(0.5)

        # Demonstrate 'c' coefficient (vertical shift)
        c_char = general_form_elements.submobjects[-2] # 'c' in 'c = 0'
        c_value_display = DecimalNumber(0, num_decimal_places=0, color=gold_color, font_size=35).next_to(c_char, DOWN, buff=0.3)
        c_desc = Text(" (vertical shift)", color=white_color, font_size=25).next_to(c_value_display, RIGHT, buff=0.2)
        
        self.play(FadeIn(c_value_display), FadeIn(c_desc))
        
        # Reset graph to y = x^2
        graph_c_start = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=blue_color, stroke_width=4)
        self.play(ReplacementTransform(graph_a_start, graph_c_start))
        
        self.wait(0.5)
        new_graph_c_2 = plane.get_graph(lambda x: x**2 + 2, x_range=[-3, 3], color=BLUE_E, stroke_width=4)
        self.play(c_value_display.animate.set_value(2), Transform(graph_c_start, new_graph_c_2))
        self.wait(0.5)
        
        new_graph_c_neg_1 = plane.get_graph(lambda x: x**2 - 1, x_range=[-3, 3], color=GOLD, stroke_width=4)
        self.play(c_value_display.animate.set_value(-1), Transform(graph_c_start, new_graph_c_neg_1))
        self.wait(0.5)
        
        self.play(FadeOut(c_value_display), FadeOut(c_desc))
        self.wait(0.5)

        # Demonstrate 'b' coefficient (horizontal shift/vertex position)
        b_char = general_form_elements.submobjects[3] # 'b' in 'bx'
        b_value_display = DecimalNumber(0, num_decimal_places=0, color=gold_color, font_size=35).next_to(b_char, DOWN, buff=0.3)
        b_desc = Text(" (vertex position)", color=white_color, font_size=25).next_to(b_value_display, RIGHT, buff=0.2)
        
        self.play(FadeIn(b_value_display), FadeIn(b_desc))

        # Reset graph to y = x^2
        graph_b_start = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=blue_color, stroke_width=4)
        self.play(ReplacementTransform(graph_c_start, graph_b_start))
        
        self.wait(0.5)
        new_graph_b_2 = plane.get_graph(lambda x: x**2 + 2*x, x_range=[-4, 2], color=BLUE_E, stroke_width=4)
        self.play(b_value_display.animate.set_value(2), Transform(graph_b_start, new_graph_b_2))
        self.wait(0.5)
        
        new_graph_b_neg_4 = plane.get_graph(lambda x: x**2 - 4*x, x_range=[0, 4], color=GOLD, stroke_width=4)
        self.play(b_value_display.animate.set_value(-4), Transform(graph_b_start, new_graph_b_neg_4))
        self.wait(0.5)
        
        self.play(FadeOut(b_value_display), FadeOut(b_desc))
        
        self.play(
            FadeOut(general_form_label),
            FadeOut(general_form_elements),
            FadeOut(graph_b_start) # Clear the graph
        )
        self.wait(0.5)

        # --- Beat 3: Finding the Roots - Where it Crosses Zero ---
        roots_title = Text("Finding the Roots (x-intercepts)", color=gold_color, font_size=45).to_corner(UP + RIGHT).shift(LEFT * 0.5)
        self.play(FadeIn(roots_title, shift=UP))

        # Re-introduce a parabola (with two roots)
        parabola_two_roots = plane.get_graph(lambda x: x**2 - 2*x - 3, x_range=[-2, 4], color=blue_color, stroke_width=4) # (x-3)(x+1) -> roots at 3, -1
        self.play(Create(parabola_two_roots))
        
        # Highlight roots
        root1_dot = Dot(plane.c2p(-1, 0), color=gold_color, radius=0.15)
        root2_dot = Dot(plane.c2p(3, 0), color=gold_color, radius=0.15)
        root1_label = create_math_text_group("x = -1", font_size=30).next_to(root1_dot, DOWN, buff=0.2)
        root2_label = create_math_text_group("x = 3", font_size=30).next_to(root2_dot, DOWN, buff=0.2)

        self.play(FadeIn(root1_dot, scale=0.5), FadeIn(root2_dot, scale=0.5))
        self.play(Write(root1_label), Write(root2_label))
        self.wait(1)

        # One root (tangent)
        parabola_one_root = plane.get_graph(lambda x: (x-1)**2, x_range=[-1, 3], color=BLUE_E, stroke_width=4) # Vertex at (1,0)
        one_root_dot = Dot(plane.c2p(1, 0), color=gold_color, radius=0.15)
        one_root_label = create_math_text_group("x = 1 (repeated)", font_size=30).next_to(one_root_dot, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(parabola_two_roots, parabola_one_root),
            FadeOut(root1_dot), FadeOut(root2_dot),
            FadeOut(root1_label), FadeOut(root2_label)
        )
        self.play(FadeIn(one_root_dot, scale=0.5), Write(one_root_label))
        self.wait(1)

        # No real roots
        parabola_no_roots = plane.get_graph(lambda x: x**2 + 1, x_range=[-2, 2], color=blue_color, stroke_width=4) # Vertex at (0,1)

        self.play(
            ReplacementTransform(parabola_one_root, parabola_no_roots),
            FadeOut(one_root_dot),
            FadeOut(one_root_label)
        )
        no_roots_text = Text("No real roots!", color=gold_color, font_size=35).next_to(parabola_no_roots, UP, buff=0.5)
        self.play(Write(no_roots_text))
        self.wait(1)
        
        self.play(
            FadeOut(roots_title),
            FadeOut(parabola_no_roots),
            FadeOut(no_roots_text)
        )
        self.wait(0.5)

        # --- Beat 4: The Quadratic Formula (Visual Introduction) ---
        formula_title = Text("The Quadratic Formula", color=gold_color, font_size=45).to_corner(UP + RIGHT).shift(LEFT * 0.5)
        self.play(FadeIn(formula_title, shift=UP))
        
        # Build the quadratic formula using create_math_text_group and manual positioning for robustness
        # x = (-b +- sqrt(b^2 - 4ac)) / 2a
        
        x_eq_label = create_math_text_group("x =", font_size=50)
        
        # Numerator: -b +/- sqrt(b^2 - 4ac)
        minus_b_label = create_math_text_group("-b", font_size=50)
        plus_minus_label = create_math_text_group("±", font_size=50)
        
        # Discriminant content: b^2 - 4ac
        b_sq_label = create_math_text_group("b^2", font_size=50)
        minus_4ac_label = create_math_text_group("-4ac", font_size=50)
        discriminant_content_group = VGroup(b_sq_label, minus_4ac_label).arrange(RIGHT, buff=0.1)
        
        # Square root symbol and bar
        sqrt_symbol_label = Text("√", font_size=90, color=white_color)
        sqrt_symbol_label.stretch_to_fit_height(discriminant_content_group.get_height() * 1.2) # Make it taller than content
        
        # Position sqrt symbol relative to content
        sqrt_symbol_label.next_to(discriminant_content_group, LEFT, buff=0.05).align_to(discriminant_content_group, DOWN)
        
        # Create the horizontal bar over the sqrt expression
        # Calculate width needed to cover both symbol and content
        effective_sqrt_content_width = (discriminant_content_group.get_right()[0] - sqrt_symbol_label.get_left()[0])
        sqrt_bar = Line(ORIGIN, RIGHT*effective_sqrt_content_width*1.05, color=white_color, stroke_width=2)
        sqrt_bar.move_to(sqrt_symbol_label.get_right() + UP*0.05) # Start near top right of sqrt symbol
        sqrt_bar.set_x(sqrt_symbol_label.get_x() + (sqrt_bar.get_width()/2)) # Center the bar over the expression more broadly
        sqrt_bar.next_to(VGroup(sqrt_symbol_label, discriminant_content_group), UP, buff=0.05)
        sqrt_bar.align_to(sqrt_symbol_label, LEFT)

        # Group square root expression
        sqrt_expression_group = VGroup(sqrt_symbol_label, discriminant_content_group, sqrt_bar)
        
        # Arrange numerator parts: -b, ±, sqrt_expression
        numerator_group = VGroup(minus_b_label, plus_minus_label, sqrt_expression_group).arrange(RIGHT, buff=0.2)
        
        # Denominator: 2a
        two_a_label = create_math_text_group("2a", font_size=50)
        
        # Fraction line
        fraction_line = Line(LEFT, RIGHT, color=white_color, stroke_width=2)
        fraction_line.set_width(numerator_group.get_width() * 1.1)
        
        # Arrange the full fraction (numerator, line, denominator)
        full_fraction_group = VGroup(numerator_group, fraction_line, two_a_label).arrange(DOWN, buff=0.2)
        fraction_line.set_width(numerator_group.get_width() * 1.1) # Re-adjust width after arranging
        
        # Center denominator under the fraction line
        two_a_label.move_to(fraction_line.get_center() + DOWN * (fraction_line.get_height()/2 + two_a_label.get_height()/2 + 0.2))

        # Assemble x= and the fraction
        quadratic_formula_display = VGroup(x_eq_label, full_fraction_group).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        quadratic_formula_display.move_to(ORIGIN)
        quadratic_formula_display.scale(0.7).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)

        self.play(Write(quadratic_formula_display))
        formula_purpose = Text("Finds 'x' (the roots) for any quadratic!", color=blue_color, font_size=35).next_to(quadratic_formula_display, UP, buff=0.5)
        self.play(Write(formula_purpose))
        self.wait(2)

        # Briefly connect parts of the formula (visual indicators, not detailed explanation)
        minus_b_box = SurroundingRectangle(minus_b_label, color=gold_color, buff=0.1)
        discriminant_box = SurroundingRectangle(discriminant_content_group, color=gold_color, buff=0.1)
        two_a_box = SurroundingRectangle(two_a_label, color=gold_color, buff=0.1)
        
        self.play(Create(minus_b_box))
        self.wait(0.5)
        self.play(FadeOut(minus_b_box), Create(discriminant_box))
        self.wait(0.5)
        self.play(FadeOut(discriminant_box), Create(two_a_box))
        self.wait(0.5)
        self.play(FadeOut(two_a_box))
        
        self.play(
            FadeOut(formula_title),
            FadeOut(formula_purpose),
            FadeOut(quadratic_formula_display),
            FadeOut(plane) # Fade out the plane from the left side
        )
        self.wait(0.5)

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Quadratic Equations", color=gold_color, font_size=55)
        
        bullet1 = Text("• Parabola: The unique curve (y = ax^2 + bx + c)", color=white_color, font_size=35)
        bullet2 = Text("• Coefficients (a, b, c): Shape, position, and shift", color=white_color, font_size=35)
        bullet3 = Text("• Roots: Where the parabola crosses the x-axis", color=white_color, font_size=35)
        
        # Simplified formula for recap - manual assembly for no Tex
        x_eq_recap = create_math_text_group("x =", font_size=35)
        numerator_recap = create_math_text_group("(-b ± √(b^2 - 4ac))", font_size=35)
        denominator_recap = create_math_text_group("2a", font_size=35)
        fraction_line_recap = Line(ORIGIN, RIGHT, color=white_color, stroke_width=2).set_width(numerator_recap.get_width() * 1.1)
        
        recap_formula_fraction = VGroup(numerator_recap, fraction_line_recap, denominator_recap).arrange(DOWN, buff=0.15)
        recap_formula_fraction.align_to(numerator_recap, LEFT) # Align to the left of the numerator for the line
        denominator_recap.move_to(fraction_line_recap.get_center() + DOWN * (fraction_line_recap.get_height()/2 + denominator_recap.get_height()/2 + 0.15))
        
        formula_recap_display = VGroup(x_eq_recap, recap_formula_fraction).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        
        bullet4 = Text("• Quadratic Formula: Finds the roots!", color=white_color, font_size=35)
        
        # Arrange all recap elements
        recap_group = VGroup(recap_title, bullet1, bullet2, bullet3, formula_recap_display, bullet4)
        recap_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        recap_group.center()
        
        # Fine-tune vertical positioning
        recap_title.to_edge(UP, buff=1)
        bullet1.next_to(recap_title, DOWN, buff=0.8)
        bullet2.next_to(bullet1, DOWN, buff=0.5, aligned_edge=LEFT)
        bullet3.next_to(bullet2, DOWN, buff=0.5, aligned_edge=LEFT)
        formula_recap_display.next_to(bullet3, DOWN, buff=0.5, aligned_edge=LEFT)
        bullet4.next_to(formula_recap_display, DOWN, buff=0.5, aligned_edge=LEFT)


        self.play(Write(recap_title))
        self.play(LaggedStart(
            FadeIn(bullet1, shift=UP),
            FadeIn(bullet2, shift=UP),
            FadeIn(bullet3, shift=UP),
            FadeIn(formula_recap_display, shift=UP),
            FadeIn(bullet4, shift=UP),
            lag_ratio=0.3
        ))
        self.wait(3)
        self.play(FadeOut(recap_group))
        self.wait(1)