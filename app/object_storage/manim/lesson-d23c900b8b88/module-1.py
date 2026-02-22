from manim import *

class UnderstandingQuadraticEquations(Scene):
    def construct(self):
        # --- Configuration and Colors ---
        # Dark background (default, but explicitly set for clarity)
        self.camera.background_color = BLACK

        # Custom high-contrast colors inspired by 3Blue1Brown
        BLUE_ACCENT = "#87CEEB"  # Light blue for main elements (e.g., graph lines)
        GOLD_ACCENT = "#FFD700"  # Gold for highlights, important text, or points
        TEXT_COLOR = WHITE         # Standard text color
        COORDINATE_COLOR = GREY_B  # For axes and grid lines

        # --- Beat 1: The Parabolic Shape (Visual Hook) ---
        title = Text("Understanding Quadratic Equations", font_size=48, color=BLUE_ACCENT)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7))

        intro_text = Text("The Shape of Change", font_size=36, color=GOLD_ACCENT)
        intro_text.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(intro_text, shift=UP))
        self.wait(0.5)

        # Create a NumberPlane for graphing
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-2, 8, 1],
            x_length=10,
            y_length=7,
            background_line_style={
                "stroke_color": COORDINATE_COLOR,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            }
        ).shift(DOWN * 0.5)
        
        # Add simple text labels for axes
        x_axis_label = Text("x", font_size=24, color=COORDINATE_COLOR).next_to(plane.x_axis.get_end(), RIGHT * 0.5)
        y_axis_label = Text("y", font_size=24, color=COORDINATE_COLOR).next_to(plane.y_axis.get_end(), UP * 0.5)

        self.play(Create(plane), FadeIn(x_axis_label, y_axis_label))
        self.wait(0.2)

        # Draw a generic parabola (y = 0.5x^2)
        parabola_func = lambda x: 0.5 * x**2
        parabola = plane.get_graph(parabola_func, x_range=[-4, 4], color=BLUE_ACCENT, stroke_width=4)

        # Animate dots moving to form the parabola, then fading into the continuous line
        dots = VGroup(*[Dot(plane.coords_to_point(x, 0), radius=0.05, color=GOLD_ACCENT) for x in np.linspace(-4, 4, 20)])
        
        self.play(
            LaggedStart(
                *[ApplyMethod(dot.animate.move_to, plane.coords_to_point(x, parabola_func(x)))
                  for x, dot in zip(np.linspace(-4, 4, 20), dots)],
                lag_ratio=0.05,
                run_time=2
            ),
            Create(parabola),
        )
        self.play(FadeOut(dots))
        self.wait(1)
        self.play(FadeOut(intro_text))

        # --- Beat 2: The Meaning of "Squared" (Intuition) ---
        concept_text_1 = Text("What 'x squared' truly means", font_size=36, color=GOLD_ACCENT)
        concept_text_1.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(concept_text_1, shift=UP))
        self.wait(0.5)

        # Illustrate x squared with a square whose area changes
        square = Square(side_length=1, color=BLUE_ACCENT, fill_opacity=0.3).move_to(LEFT*3.5 + DOWN*1)
        side_x_label = Text("x", color=TEXT_COLOR, font_size=28).next_to(square.get_bottom(), DOWN*0.5)
        side_x_label_2 = Text("x", color=TEXT_COLOR, font_size=28).next_to(square.get_left(), LEFT*0.5)
        area_label = Text("Area = x²", color=TEXT_COLOR, font_size=32).next_to(square, UP*1.5)

        self.play(Create(square), Write(side_x_label), Write(side_x_label_2))
        self.wait(0.5)
        self.play(Write(area_label))
        self.wait(0.5)

        # Use ValueTracker to animate the side length 'x'
        x_val_tracker = ValueTracker(1)
        
        # Updaters for the square and its labels
        def update_square_size(mobject):
            x_val = x_val_tracker.get_value()
            mobject.set(width=x_val, height=x_val)
            mobject.move_to(square.get_center()) # Keep center fixed during scaling
        
        def update_side_x_label_text(mobject):
            x_val = x_val_tracker.get_value()
            mobject.become(Text(f"x = {x_val:.1f}", color=TEXT_COLOR, font_size=28).next_to(square.get_bottom(), DOWN*0.5))
        
        def update_area_label_text(mobject):
            x_val = x_val_tracker.get_value()
            mobject.become(Text(f"Area = {x_val**2:.1f}", color=TEXT_COLOR, font_size=32).next_to(square, UP*1.5))
        
        square.add_updater(update_square_size)
        side_x_label.add_updater(update_side_x_label_text)
        area_label.add_updater(update_area_label_text)

        self.play(x_val_tracker.animate.set_value(2.5), run_time=2)
        self.wait(0.5)
        self.play(x_val_tracker.animate.set_value(1.5), run_time=1.5)
        self.wait(0.5)

        # Remove updaters to prevent further implicit updates
        square.clear_updaters()
        side_x_label.clear_updaters()
        area_label.clear_updaters()

        self.play(
            FadeOut(square, shift=RIGHT),
            FadeOut(side_x_label, shift=RIGHT),
            FadeOut(side_x_label_2, shift=RIGHT),
            FadeOut(area_label, shift=RIGHT),
            FadeOut(concept_text_1)
        )
        self.wait(0.5)

        # --- Beat 3: Building the General Form (Formal Notation - NO Tex/MathTex) ---
        concept_text_2 = Text("The General Quadratic Form", font_size=36, color=GOLD_ACCENT)
        concept_text_2.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(concept_text_2, shift=UP))
        self.wait(0.5)

        # Transform current parabola to y = x^2 (the basic form)
        initial_parabola_func = lambda x: x**2
        initial_parabola = plane.get_graph(initial_parabola_func, x_range=[-2.5, 2.5], color=TEXT_COLOR, stroke_width=3)
        initial_label = Text("y = x²", font_size=28, color=TEXT_COLOR).next_to(initial_parabola, RIGHT + UP*0.5)

        self.play(
            Transform(parabola, initial_parabola),
            FadeIn(initial_label)
        )
        self.wait(1)
        self.play(FadeOut(initial_label))

        # Construct the equation ax^2 + bx + c = 0 using individual Text Mobjects
        a_m = Text("a", color=GOLD_ACCENT, font_size=40)
        x_sq_m = Text("x", color=BLUE_ACCENT, font_size=40)
        exp_2_m = Text("2", font_size=20, color=BLUE_ACCENT)
        plus_1_m = Text("+", color=TEXT_COLOR, font_size=40)
        b_m = Text("b", color=GOLD_ACCENT, font_size=40)
        x_m = Text("x", color=BLUE_ACCENT, font_size=40)
        plus_2_m = Text("+", color=TEXT_COLOR, font_size=40)
        c_m = Text("c", color=GOLD_ACCENT, font_size=40)
        eq_m = Text("=", color=TEXT_COLOR, font_size=40)
        zero_m = Text("0", color=TEXT_COLOR, font_size=40)

        # Arrange the parts for a*x^2
        ax2 = VGroup(a_m, x_sq_m).arrange(RIGHT, buff=0.05)
        exp_2_m.move_to(x_sq_m.get_corner(UP + RIGHT) + UL * 0.1) # Position '2' as superscript
        ax2_group = VGroup(ax2, exp_2_m) # Group a, x, and 2

        # Arrange the parts for b*x
        bx_group = VGroup(b_m, x_m).arrange(RIGHT, buff=0.05)
        
        # Combine all elements into the full equation
        equation_mobject = VGroup(
            ax2_group, plus_1_m, bx_group, plus_2_m, c_m, eq_m, zero_m
        ).arrange(RIGHT, buff=0.2)
        equation_mobject.next_to(plane, DOWN*1.5)

        # Animate transformations of the parabola with a, b, c
        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(0)
        c_tracker = ValueTracker(0)

        # Updater for the parabola graph
        def update_general_parabola(mobject):
            a_val = a_tracker.get_value()
            b_val = b_tracker.get_value()
            c_val = c_tracker.get_value()
            new_graph = plane.get_graph(lambda x: a_val * x**2 + b_val * x + c_val, x_range=[-4, 4], color=BLUE_ACCENT, stroke_width=4)
            mobject.become(new_graph)
        
        parabola.add_updater(update_general_parabola)

        # Animate 'a' (stretch/compress/flip)
        temp_a_label = Text("a", color=GOLD_ACCENT, font_size=30).next_to(a_m, LEFT, buff=0.2).set_opacity(0)
        self.play(FadeIn(temp_a_label.set_opacity(1)))
        self.play(a_tracker.animate.set_value(2), run_time=1) # Thinner
        self.play(a_tracker.animate.set_value(0.5), run_time=1) # Wider
        self.play(a_tracker.animate.set_value(-1), run_time=1) # Flipped
        self.play(a_tracker.animate.set_value(1), run_time=1) # Back to default
        self.play(FadeOut(temp_a_label))

        # Animate 'c' (vertical shift)
        temp_c_label = Text("c", color=GOLD_ACCENT, font_size=30).next_to(c_m, LEFT, buff=0.2).set_opacity(0)
        self.play(FadeIn(temp_c_label.set_opacity(1)))
        self.play(c_tracker.animate.set_value(2), run_time=1) # Shift up
        self.play(c_tracker.animate.set_value(-1), run_time=1) # Shift down
        self.play(c_tracker.animate.set_value(0), run_time=1) # Back to default
        self.play(FadeOut(temp_c_label))

        # Animate 'b' (horizontal shift + vertex change)
        temp_b_label = Text("b", color=GOLD_ACCENT, font_size=30).next_to(b_m, LEFT, buff=0.2).set_opacity(0)
        self.play(FadeIn(temp_b_label.set_opacity(1)))
        self.play(b_tracker.animate.set_value(2), run_time=1) # Shift left
        self.play(b_tracker.animate.set_value(-2), run_time=1) # Shift right
        self.play(b_tracker.animate.set_value(0), run_time=1) # Back to default
        self.play(FadeOut(temp_b_label))

        parabola.clear_updaters() # Stop automatic updates
        
        # Display the full equation
        self.play(Write(equation_mobject))
        self.wait(1)
        self.play(FadeOut(concept_text_2))

        # --- Beat 4: Understanding Solutions (Interpreting the Equation) ---
        concept_text_3 = Text("Finding the Solutions (Roots)", font_size=36, color=GOLD_ACCENT)
        concept_text_3.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(concept_text_3, shift=UP))
        self.wait(0.5)

        # Highlight the '= 0' part of the equation
        self.play(
            equation_mobject[5].animate.set_color(GOLD_ACCENT), # =
            equation_mobject[6].animate.set_color(GOLD_ACCENT)  # 0
        )
        self.wait(0.5)
        
        # Explain what y=0 means graphically: crossing the x-axis
        y_equals_zero_text = Text("When y = 0...", color=TEXT_COLOR, font_size=30).next_to(plane.y_axis.get_origin(), RIGHT, buff=0.5).shift(UP)
        x_axis_highlight = Line(plane.x_axis.get_start(), plane.x_axis.get_end(), stroke_color=GOLD_ACCENT, stroke_width=4)
        self.play(Write(y_equals_zero_text), Create(x_axis_highlight))
        self.wait(1)

        # Show different solution scenarios
        # Scenario 1: Two real roots (e.g., y = x^2 - 2)
        current_parabola_func = lambda x: x**2 - 2
        new_parabola = plane.get_graph(current_parabola_func, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=4)
        self.play(Transform(parabola, new_parabola))
        
        root1_coords = np.sqrt(2)
        root2_coords = -np.sqrt(2)
        root1 = Dot(plane.coords_to_point(root1_coords, 0), color=GOLD_ACCENT, radius=0.1)
        root2 = Dot(plane.coords_to_point(root2_coords, 0), color=GOLD_ACCENT, radius=0.1)
        self.play(FadeIn(root1, root2))
        solutions_text_2 = Text("Two Real Solutions", font_size=28, color=TEXT_COLOR).next_to(parabola, UP + RIGHT, buff=0.5)
        self.play(Write(solutions_text_2))
        self.wait(1)
        self.play(FadeOut(root1, root2, solutions_text_2))

        # Scenario 2: One real root (e.g., y = 0.5x^2)
        current_parabola_func = lambda x: 0.5 * x**2
        new_parabola = plane.get_graph(current_parabola_func, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=4)
        self.play(Transform(parabola, new_parabola))
        root_one = Dot(plane.coords_to_point(0, 0), color=GOLD_ACCENT, radius=0.1)
        self.play(FadeIn(root_one))
        solutions_text_1 = Text("One Real Solution", font_size=28, color=TEXT_COLOR).next_to(parabola, UP + RIGHT, buff=0.5)
        self.play(Write(solutions_text_1))
        self.wait(1)
        self.play(FadeOut(root_one, solutions_text_1))

        # Scenario 3: No real roots (e.g., y = 0.5x^2 + 2)
        current_parabola_func = lambda x: 0.5 * x**2 + 2
        new_parabola = plane.get_graph(current_parabola_func, x_range=[-3, 3], color=BLUE_ACCENT, stroke_width=4)
        self.play(Transform(parabola, new_parabola))
        solutions_text_0 = Text("No Real Solutions", font_size=28, color=TEXT_COLOR).next_to(parabola, UP + RIGHT, buff=0.5)
        self.play(Write(solutions_text_0))
        self.wait(1)
        self.play(FadeOut(solutions_text_0))

        self.play(
            FadeOut(y_equals_zero_text),
            FadeOut(x_axis_highlight),
            FadeOut(concept_text_3)
        )
        self.wait(0.5)

        # --- Final cleanup before recap ---
        self.play(
            FadeOut(title),
            FadeOut(plane),
            FadeOut(x_axis_label),
            FadeOut(y_axis_label),
            FadeOut(parabola),
            FadeOut(equation_mobject)
        )

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Quadratic Equations", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        
        bullet1 = Text("• Second-degree polynomial", font_size=36, color=TEXT_COLOR)
        bullet2 = Text("• Creates parabola shapes", font_size=36, color=TEXT_COLOR)
        
        # Manually construct the equation for recap using Text Mobjects
        a_m_rec = Text("a", color=GOLD_ACCENT, font_size=36)
        x_sq_m_rec = Text("x", color=BLUE_ACCENT, font_size=36)
        exp_2_m_rec = Text("2", font_size=18, color=BLUE_ACCENT)
        plus_1_m_rec = Text("+", color=TEXT_COLOR, font_size=36)
        b_m_rec = Text("b", color=GOLD_ACCENT, font_size=36)
        x_m_rec = Text("x", color=BLUE_ACCENT, font_size=36)
        plus_2_m_rec = Text("+", color=TEXT_COLOR, font_size=36)
        c_m_rec = Text("c", color=GOLD_ACCENT, font_size=36)
        eq_m_rec = Text("=", color=TEXT_COLOR, font_size=36)
        zero_m_rec = Text("0", color=TEXT_COLOR, font_size=36)

        ax2_rec = VGroup(a_m_rec, x_sq_m_rec).arrange(RIGHT, buff=0.05)
        exp_2_m_rec.move_to(x_sq_m_rec.get_corner(UP + RIGHT) + UL * 0.1)
        ax2_group_rec = VGroup(ax2_rec, exp_2_m_rec)

        bx_group_rec = VGroup(b_m_rec, x_m_rec).arrange(RIGHT, buff=0.05)
        
        recap_equation_mobject = VGroup(
            ax2_group_rec, plus_1_m_rec, bx_group_rec, plus_2_m_rec, c_m_rec, eq_m_rec, zero_m_rec
        ).arrange(RIGHT, buff=0.15)
        
        # Combine "Form: " text with the equation mobject
        bullet3_prefix = Text("• Form: ", font_size=36, color=TEXT_COLOR)
        bullet3 = VGroup(bullet3_prefix, recap_equation_mobject).arrange(RIGHT, buff=0.2)
        
        bullet4 = Text("• Solutions are x-intercepts", font_size=36, color=TEXT_COLOR)

        recap_items = VGroup(bullet1, bullet2, bullet3, bullet4).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        recap_items.next_to(recap_title, DOWN, buff=1)
        recap_items.to_edge(LEFT, buff=1)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[FadeIn(item, shift=UP) for item in recap_items], lag_ratio=0.3))
        self.wait(3)