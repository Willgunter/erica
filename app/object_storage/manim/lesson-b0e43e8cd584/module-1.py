from manim import *

class QuadraticEquationAnimation(Scene):
    def construct(self):
        # 1. Setup: Clean dark background, high-contrast blue and gold
        self.camera.background_color = BLACK

        # --- Beat 1: The Parabola - Visual Hook & Introduction ---
        # 1.1 Strong visual hook: A parabola being drawn
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": BLUE_E, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-2, 0, 2]},
            y_axis_config={"numbers_to_include": [0, 2, 4]},
        ).add_coordinates()
        axes.to_edge(DOWN)

        # A specific parabola: y = x^2
        parabola_func = lambda x: x**2
        parabola = axes.get_graph(parabola_func, color=GOLD, x_range=[-2.5, 2.5])
        
        # Initial text for the hook
        intro_text_1 = Text("What shape is this?", font_size=40, color=WHITE).to_edge(UP)
        intro_text_2 = Text("A Parabola!", font_size=48, color=BLUE).next_to(intro_text_1, DOWN)

        self.play(
            LaggedStart(
                Create(axes),
                Create(parabola),
                Write(intro_text_1),
                lag_ratio=0.7,
                run_time=2.5
            )
        )
        self.wait(0.5)
        self.play(Write(intro_text_2))
        self.wait(1)

        intro_text_3 = Text("From Quadratic Equations", font_size=36, color=WHITE).next_to(intro_text_2, DOWN)
        self.play(FadeIn(intro_text_3, shift=DOWN))
        self.wait(1.5)

        # Clean up for next beat
        self.play(
            FadeOut(intro_text_1),
            FadeOut(intro_text_2),
            FadeOut(intro_text_3),
            parabola.animate.scale(0.8).to_corner(UL), # Shrink and move for continuity
            axes.animate.scale(0.8).to_corner(UL),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 2: Roots/Zeros - Where it crosses ---
        # A new parabola with visible roots: y = x^2 - 4
        axes_roots = Axes(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": BLUE_E, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-2, 0, 2]},
            y_axis_config={"numbers_to_include": [-4, 0, 4]},
        ).add_coordinates()
        axes_roots.shift(RIGHT * 2.5) # Position to the right

        parabola_roots_func = lambda x: x**2 - 4
        parabola_roots = axes_roots.get_graph(parabola_roots_func, color=GOLD, x_range=[-2.5, 2.5])

        root_label_1 = Text("Roots (or Zeros)", font_size=36, color=WHITE).to_edge(UP).shift(LEFT * 2)
        root_label_2 = Text("Where y = 0", font_size=30, color=BLUE).next_to(root_label_1, DOWN)

        root_dot_1 = Dot(point=axes_roots.coords_to_point(-2, 0), color=RED_C, radius=0.1)
        root_dot_2 = Dot(point=axes_roots.coords_to_point(2, 0), color=RED_C, radius=0.1)
        
        root_arrow_1 = Arrow(start=root_label_1.get_bottom(), end=root_dot_1.get_center(), buff=0.1, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        root_arrow_2 = Arrow(start=root_label_1.get_bottom(), end=root_dot_2.get_center(), buff=0.1, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.1)

        self.play(
            Create(axes_roots),
            Create(parabola_roots),
            FadeIn(root_label_1, shift=UP)
        )
        self.wait(0.5)
        self.play(
            FadeIn(root_label_2, shift=UP),
            Create(root_dot_1),
            Create(root_dot_2)
        )
        self.wait(0.5)
        self.play(
            GrowArrow(root_arrow_1),
            GrowArrow(root_arrow_2)
        )
        self.wait(2)

        # Fade everything out except for the axes_roots and parabola_roots for next beat, centered
        self.play(
            FadeOut(root_label_1),
            FadeOut(root_label_2),
            FadeOut(root_dot_1),
            FadeOut(root_dot_2),
            FadeOut(root_arrow_1),
            FadeOut(root_arrow_2),
            axes.animate.fade(1), # Fade out the old axes/parabola
            parabola.animate.fade(1),
            axes_roots.animate.move_to(ORIGIN), # Center the new one
            parabola_roots.animate.move_to(ORIGIN)
        )
        self.wait(0.5)

        # --- Beat 3: The General Form ---
        eq_a = Text("a", font_size=60, color=BLUE).shift(LEFT * 4 + UP * 0.5)
        eq_x2 = Text("x", font_size=60, color=WHITE).next_to(eq_a, RIGHT * 0.5)
        eq_2_exp = Text("2", font_size=30, color=WHITE).next_to(eq_x2, UP * 0.5).scale(0.8)
        eq_plus1 = Text("+", font_size=60, color=WHITE).next_to(eq_x2, RIGHT * 0.5)
        eq_b = Text("b", font_size=60, color=BLUE).next_to(eq_plus1, RIGHT * 0.5)
        eq_x = Text("x", font_size=60, color=WHITE).next_to(eq_b, RIGHT * 0.5)
        eq_plus2 = Text("+", font_size=60, color=WHITE).next_to(eq_x, RIGHT * 0.5)
        eq_c = Text("c", font_size=60, color=BLUE).next_to(eq_plus2, RIGHT * 0.5)
        eq_eq = Text("=", font_size=60, color=WHITE).next_to(eq_c, RIGHT * 0.5)
        eq_0 = Text("0", font_size=60, color=WHITE).next_to(eq_eq, RIGHT * 0.5)

        quadratic_equation_group = VGroup(
            eq_a, eq_x2, eq_2_exp, eq_plus1, eq_b, eq_x, eq_plus2, eq_c, eq_eq, eq_0
        ).move_to(UP * 2.5) # Position above the parabola

        title_general = Text("General Form:", font_size=40, color=WHITE).to_edge(UP).shift(LEFT * 4.5)

        self.play(
            FadeIn(title_general, shift=UP),
            LaggedStart(
                FadeIn(eq_a, shift=LEFT),
                FadeIn(eq_x2, shift=LEFT),
                FadeIn(eq_2_exp, shift=LEFT),
                FadeIn(eq_plus1, shift=LEFT),
                FadeIn(eq_b, shift=LEFT),
                FadeIn(eq_x, shift=LEFT),
                FadeIn(eq_plus2, shift=LEFT),
                FadeIn(eq_c, shift=LEFT),
                FadeIn(eq_eq, shift=LEFT),
                FadeIn(eq_0, shift=LEFT),
                lag_ratio=0.1,
                run_time=3
            )
        )
        self.wait(2)

        a_expl = Text("Controls opening & width", font_size=28, color=GOLD).next_to(eq_a, DOWN)
        c_expl = Text("Y-intercept", font_size=28, color=GOLD).next_to(eq_c, DOWN)

        self.play(FadeIn(a_expl, shift=UP), FadeIn(c_expl, shift=UP))
        self.wait(2)

        self.play(
            FadeOut(title_general),
            FadeOut(a_expl),
            FadeOut(c_expl),
            FadeOut(quadratic_equation_group),
            axes_roots.animate.fade(1), # Fade out parabola as well
            parabola_roots.animate.fade(1)
        )
        self.wait(0.5)

        # --- Beat 4: The Quadratic Formula ---
        # Build the quadratic formula using Text objects, manually positioning
        title_formula = Text("The Quadratic Formula", font_size=48, color=BLUE).to_edge(UP)

        x_eq = Text("x =", font_size=70, color=WHITE)
        
        minus_b = Text("-b", font_size=70, color=BLUE)
        pm_sym = Text("±", font_size=70, color=WHITE)
        sqrt_paren = Text("(", font_size=70, color=WHITE)
        b2_minus_4ac = Text("b", font_size=70, color=BLUE)
        exp_2 = Text("2", font_size=35, color=WHITE).next_to(b2_minus_4ac, UP * 0.5).scale(0.8)
        minus_4ac = Text("- 4ac", font_size=70, color=WHITE).next_to(b2_minus_4ac, RIGHT * 0.5)
        sqrt_paren_close = Text(")", font_size=70, color=WHITE).next_to(minus_4ac, RIGHT * 0.5)

        # Manually create a horizontal line for the fraction
        frac_line = Line(start=LEFT * 3, end=RIGHT * 3, stroke_width=4, color=WHITE)
        
        two_a = Text("2a", font_size=70, color=BLUE)

        # Group components for alignment
        numerator_components = VGroup(minus_b, pm_sym, sqrt_paren, b2_minus_4ac, exp_2, minus_4ac, sqrt_paren_close)
        
        # Position numerator relative to each other
        pm_sym.next_to(minus_b, RIGHT * 0.5)
        sqrt_paren.next_to(pm_sym, RIGHT * 0.5)
        b2_minus_4ac.next_to(sqrt_paren, RIGHT * 0.5)
        minus_4ac.next_to(b2_minus_4ac, RIGHT * 0.5)
        sqrt_paren_close.next_to(minus_4ac, RIGHT * 0.5)
        
        # Make the square root symbol look somewhat like a sqrt. This is a manual approximation
        # A 'tick' and a 'top line' for the square root
        sqrt_tick = Line(start=b2_minus_4ac.get_top() + LEFT * 0.2, end=b2_minus_4ac.get_center(), stroke_width=4, color=WHITE)
        sqrt_top_line = Line(start=sqrt_tick.get_start(), end=sqrt_paren_close.get_right() + UP * 0.2, stroke_width=4, color=WHITE)
        sqrt_line_group = VGroup(sqrt_tick, sqrt_top_line)
        sqrt_line_group.move_to(b2_minus_4ac.get_center() + UP * 0.5) # Adjust position
        
        # Group everything for the formula
        numerator = VGroup(minus_b, pm_sym, sqrt_paren, b2_minus_4ac, exp_2, minus_4ac, sqrt_paren_close, sqrt_line_group)
        denominator = VGroup(two_a)

        # Now, arrange the full formula
        frac_line.set_width(numerator.width * 1.2) # Adjust width based on numerator
        
        # Center numerator and denominator around the fraction line
        numerator.next_to(frac_line, UP * 0.5)
        denominator.next_to(frac_line, DOWN * 0.5)
        
        # Combine into a group for easier positioning
        formula_fraction = VGroup(numerator, frac_line, denominator)
        
        # Position x = next to the fraction
        x_eq.next_to(formula_fraction, LEFT * 0.5)
        
        full_formula = VGroup(x_eq, formula_fraction).center()
        
        finds_roots_text = Text("Finds the Roots!", font_size=36, color=GOLD).next_to(full_formula, DOWN, buff=0.7)

        self.play(FadeIn(title_formula, shift=UP))
        self.play(
            LaggedStart(
                FadeIn(x_eq, shift=LEFT),
                FadeIn(minus_b, shift=LEFT),
                FadeIn(pm_sym, shift=LEFT),
                FadeIn(sqrt_paren, shift=LEFT),
                FadeIn(b2_minus_4ac, shift=LEFT),
                FadeIn(exp_2, shift=LEFT),
                FadeIn(minus_4ac, shift=LEFT),
                FadeIn(sqrt_paren_close, shift=LEFT),
                Create(sqrt_line_group),
                Create(frac_line, scale=0), # Scale from zero
                FadeIn(two_a, shift=DOWN),
                lag_ratio=0.07,
                run_time=4
            )
        )
        self.wait(1)
        self.play(FadeIn(finds_roots_text, shift=UP))
        self.wait(2.5)

        # --- Beat 5: Application Example (Conceptual) ---
        self.play(
            full_formula.animate.scale(0.6).to_corner(UL),
            finds_roots_text.animate.next_to(full_formula, DOWN).scale(0.8),
            FadeOut(title_formula)
        )

        # Re-introduce a parabola with roots, centered
        axes_example = Axes(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": BLUE_E, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-2, 0, 2]},
            y_axis_config={"numbers_to_include": [-4, 0, 4]},
        ).add_coordinates().shift(RIGHT * 2.5) # Position to the right

        parabola_example_func = lambda x: x**2 - 4
        parabola_example = axes_example.get_graph(parabola_example_func, color=GOLD, x_range=[-2.5, 2.5])

        example_root_dot_1 = Dot(point=axes_example.coords_to_point(-2, 0), color=RED_C, radius=0.15)
        example_root_dot_2 = Dot(point=axes_example.coords_to_point(2, 0), color=RED_C, radius=0.15)
        
        example_text = Text("Use the formula to find these points!", font_size=32, color=WHITE).next_to(full_formula, DOWN, buff=1).shift(RIGHT*1.5)

        self.play(
            Create(axes_example),
            Create(parabola_example),
            FadeIn(example_root_dot_1),
            FadeIn(example_root_dot_2)
        )
        self.wait(0.5)
        self.play(FadeIn(example_text, shift=DOWN))
        
        # Animate "x =" moving towards the roots
        x_equals_copy = x_eq.copy()
        self.play(
            x_equals_copy.animate.move_to(example_root_dot_1.get_center() + LEFT * 0.5),
            run_time=1
        )
        x_equals_copy_2 = x_eq.copy()
        self.play(
            x_equals_copy_2.animate.move_to(example_root_dot_2.get_center() + LEFT * 0.5),
            run_time=1
        )
        self.wait(2)

        # --- Recap Card ---
        self.play(
            FadeOut(full_formula),
            FadeOut(finds_roots_text),
            FadeOut(x_equals_copy),
            FadeOut(x_equals_copy_2),
            FadeOut(example_text),
            FadeOut(axes_example),
            FadeOut(parabola_example),
        )

        recap_title = Text("Recap: Quadratic Equations", font_size=48, color=BLUE).to_edge(UP)
        
        recap_point_1 = Text("- Parabola is the graph shape", font_size=36, color=WHITE).shift(UP * 1.5)
        recap_point_2 = Text("- Roots are x-intercepts (where y=0)", font_size=36, color=WHITE).next_to(recap_point_1, DOWN)
        recap_point_3 = Text("- General Form: ax^2 + bx + c = 0", font_size=36, color=WHITE).next_to(recap_point_2, DOWN)
        recap_point_4 = Text("- Formula finds the roots", font_size=36, color=WHITE).next_to(recap_point_3, DOWN)

        recap_points = VGroup(recap_title, recap_point_1, recap_point_2, recap_point_3, recap_point_4)
        recap_points.center() # Recenter the group

        self.play(
            FadeIn(recap_title, shift=UP),
            LaggedStart(
                FadeIn(recap_point_1, shift=LEFT),
                FadeIn(recap_point_2, shift=LEFT),
                FadeIn(recap_point_3, shift=LEFT),
                FadeIn(recap_point_4, shift=LEFT),
                lag_ratio=0.5,
                run_time=3
            )
        )
        self.wait(3)

        self.play(FadeOut(recap_points))
        self.wait(0.5)