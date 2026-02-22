from manim import *

# Define custom colors for better contrast and theme
BLUE_ACCENT = '#5DADE2' # A slightly lighter blue
GOLD_ACCENT = '#FFD700' # Standard gold

class QuadraticDiscriminant(Scene):
    def construct(self):
        # 0. Setup: Dark background for high contrast
        self.camera.background_color = BLACK

        # Beat 1: The Parabola - A Visual Hook & Introduction
        # ----------------------------------------------------
        intro_text = Text("Quadratic Equations", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(intro_text))

        # A simple parabola function for the hook
        def func_parabola_hook(x):
            return 0.5 * x**2 - 2

        parabola_initial = ParametricFunction(
            lambda t: self.coords_to_point(t, func_parabola_hook(t)),
            t_range=[-4, 4],
            color=GOLD_ACCENT,
            stroke_width=6
        )
        
        self.play(Create(parabola_initial, run_time=2))
        self.wait(0.5)

        # Introduce the general form
        general_eq_tex = MathTex("ax^2 + bx + c = 0", color=WHITE, font_size=48)
        general_eq_tex.shift(DOWN * 1.5)
        self.play(Write(general_eq_tex))
        self.wait(1)
        
        self.play(
            FadeOut(parabola_initial),
            FadeOut(general_eq_tex),
            FadeOut(intro_text)
        )
        self.wait(0.5)


        # Beat 2: X-intercepts as Solutions
        # ---------------------------------
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-4, -2, 2, 4]},
            y_axis_config={"numbers_to_include": [-3, -1, 1, 3]}
        ).add_coordinates()
        axes.to_center()

        labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Write(labels))
        self.wait(0.5)

        # Example parabola with two roots
        def f_two_roots(x):
            return 0.5 * x**2 - 2

        parabola_two_roots = axes.get_graph(f_two_roots, color=GOLD_ACCENT, stroke_width=5)
        root1 = Dot(axes.c2p(-2, 0), color=BLUE_ACCENT, radius=0.15)
        root2 = Dot(axes.c2p(2, 0), color=BLUE_ACCENT, radius=0.15)
        
        eq_text_two_roots = MathTex("y = 0.5x^2 - 2", color=WHITE).to_edge(UP)
        solution_label = Text("Solutions (x-intercepts)", color=BLUE_ACCENT, font_size=30).next_to(root2, RIGHT, buff=0.5)
        solution_arrow = Arrow(solution_label.get_left(), root2.get_center(), buff=0.1, color=BLUE_ACCENT)

        self.play(Create(parabola_two_roots), Write(eq_text_two_roots))
        self.play(Create(root1), Create(root2))
        self.play(Write(solution_label), Create(solution_arrow))
        self.wait(1.5)
        self.play(FadeOut(solution_label), FadeOut(solution_arrow))


        # Beat 3: Varying 'c' and its Impact on Roots
        # --------------------------------------------
        # We vary 'c' in y = 0.5x^2 + c and observe the roots.
        self.remove(root1, root2) # Remove old roots directly

        c_tracker = ValueTracker(-2) # Initial value of c

        def get_dynamic_parabola():
            return axes.get_graph(lambda x: 0.5 * x**2 + c_tracker.get_value(), color=GOLD_ACCENT, stroke_width=5)
        
        # Equation for dynamic parabola
        eq_dynamic_tex = MathTex("y = 0.5x^2 + ", "c", color=WHITE).to_edge(UP)
        c_val_text = MathTex(f"{c_tracker.get_value():.1f}", color=GOLD_ACCENT).next_to(eq_dynamic_tex[0], RIGHT, buff=0.1)
        eq_group = VGroup(eq_dynamic_tex[0], c_val_text).to_edge(UP)

        dynamic_parabola = always_redraw(get_dynamic_parabola)

        self.play(
            FadeTransform(eq_text_two_roots, eq_dynamic_tex[0]),
            Write(c_val_text)
        )
        self.play(Create(dynamic_parabola))
        
        # Function to dynamically get x-intercepts
        def get_x_intercepts_dynamic():
            a = 0.5
            c = c_tracker.get_value()
            roots_list = []
            
            # Discriminant for y = ax^2 + c is b^2 - 4ac = 0^2 - 4(a)(c) = -4ac
            discriminant_val = -4 * a * c 
            epsilon = 0.05 # Tolerance for floating point comparisons to zero
            
            if discriminant_val > epsilon: # Two real roots
                x_val = np.sqrt(-c / a) 
                roots_list.append(Dot(axes.c2p(x_val, 0), color=BLUE_ACCENT, radius=0.15))
                roots_list.append(Dot(axes.c2p(-x_val, 0), color=BLUE_ACCENT, radius=0.15))
            elif abs(discriminant_val) <= epsilon: # One real root (tangent)
                roots_list.append(Dot(axes.c2p(0, 0), color=BLUE_ACCENT, radius=0.15))
            # If discriminant_val < -epsilon, no real roots (list remains empty)
            return roots_list

        current_roots = VGroup(*get_x_intercepts_dynamic())
        self.add(current_roots)

        def update_roots(mob):
            new_roots = get_x_intercepts_dynamic()
            mob.become(VGroup(*new_roots))

        current_roots.add_updater(update_roots)
        
        # Update c_val_text
        c_val_text.add_updater(lambda m: m.become(MathTex(f"{c_tracker.get_value():.1f}", color=GOLD_ACCENT).next_to(eq_dynamic_tex[0], RIGHT, buff=0.1)))

        # Text for number of roots
        num_roots_text = Text(f"Number of Real Roots: {len(get_x_intercepts_dynamic())}", font_size=30, color=WHITE).to_corner(DR)
        self.play(Write(num_roots_text))
        
        def update_num_roots_text(mob):
            num_roots = len(get_x_intercepts_dynamic())
            mob.become(Text(f"Number of Real Roots: {num_roots}", font_size=30, color=WHITE).to_corner(DR))
        
        num_roots_text.add_updater(update_num_roots_text)


        self.play(c_tracker.animate.set_value(0), run_time=2, rate_func=smooth) # Two roots -> One root (tangent)
        self.wait(1)
        self.play(c_tracker.animate.set_value(2), run_time=2, rate_func=smooth) # One root -> No roots
        self.wait(1.5)
        self.play(c_tracker.animate.set_value(-2), run_time=2, rate_func=smooth) # No roots -> Two roots
        self.wait(1)

        # Clear updaters and remove objects for next beat
        c_val_text.clear_updaters()
        current_roots.clear_updaters()
        num_roots_text.clear_updaters()
        self.remove(c_val_text, current_roots, num_roots_text) 


        # Beat 4: Introduce the Discriminant's Role Visually
        # ---------------------------------------------------
        discriminant_concept_text = Text("What determines the number of roots?", color=BLUE_ACCENT, font_size=36).to_edge(UP)
        self.play(FadeTransform(eq_group, discriminant_concept_text))

        # Introduce the crucial part of the quadratic formula
        quad_formula_part = MathTex("b^2 - 4ac", color=GOLD_ACCENT, font_size=48).move_to(ORIGIN)
        self.play(Write(quad_formula_part))
        self.wait(1)

        # Show cases
        case1_text = MathTex("b^2 - 4ac > 0", " \\implies ", "\\text{Two Real Roots}", color=WHITE)
        case2_text = MathTex("b^2 - 4ac = 0", " \\implies ", "\\text{One Real Root}", color=WHITE)
        case3_text = MathTex("b^2 - 4ac < 0", " \\implies ", "\\text{No Real Roots}", color=WHITE)

        cases = VGroup(case1_text, case2_text, case3_text).arrange(DOWN, buff=0.8).next_to(quad_formula_part, DOWN, buff=1)
        
        self.play(quad_formula_part.animate.scale(0.8).to_edge(UL, buff=1.0))
        self.play(LaggedStart(*[FadeIn(t) for t in cases], lag_ratio=0.5))
        self.wait(1)

        # Show small illustrative parabolas next to each case
        def get_mini_parabola(a, b, c, x_offset=0, y_offset=0):
            def func(x):
                return a * x**2 + b * x + c
            
            graph = ParametricFunction(
                lambda t: np.array([t, func(t), 0]),
                t_range=[-1.5, 1.5],
                color=GOLD_ACCENT,
                stroke_width=3
            ).scale(0.3).shift(x_offset*RIGHT + y_offset*UP)
            return graph

        # Case 1: Two roots (e.g., y = 0.5x^2 - 1) -> b^2 - 4ac = 0 - 4(0.5)(-1) = 2 > 0
        mini_parabola1 = get_mini_parabola(0.5, 0, -1).next_to(case1_text[2], RIGHT, buff=0.5)
        root1_mini1 = Dot(mini_parabola1.get_center() + LEFT*0.2, color=BLUE_ACCENT, radius=0.05)
        root2_mini1 = Dot(mini_parabola1.get_center() + RIGHT*0.2, color=BLUE_ACCENT, radius=0.05)
        
        # Case 2: One root (e.g., y = 0.5x^2) -> b^2 - 4ac = 0 - 4(0.5)(0) = 0
        mini_parabola2 = get_mini_parabola(0.5, 0, 0).next_to(case2_text[2], RIGHT, buff=0.5)
        root_mini2 = Dot(mini_parabola2.get_center(), color=BLUE_ACCENT, radius=0.05)

        # Case 3: No real roots (e.g., y = 0.5x^2 + 1) -> b^2 - 4ac = 0 - 4(0.5)(1) = -2 < 0
        mini_parabola3 = get_mini_parabola(0.5, 0, 1).next_to(case3_text[2], RIGHT, buff=0.5)

        self.play(
            Create(mini_parabola1), Create(root1_mini1), Create(root2_mini1),
            run_time=0.7
        )
        self.play(
            Create(mini_parabola2), Create(root_mini2),
            run_time=0.7
        )
        self.play(
            Create(mini_parabola3),
            run_time=0.7
        )
        self.wait(1.5)

        self.play(
            FadeOut(dynamic_parabola),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(discriminant_concept_text),
            FadeOut(mini_parabola1), FadeOut(root1_mini1), FadeOut(root2_mini1),
            FadeOut(mini_parabola2), FadeOut(root_mini2),
            FadeOut(mini_parabola3),
            *[FadeOut(t) for t in cases],
            quad_formula_part.animate.scale(1.2).move_to(ORIGIN)
        )
        self.wait(0.5)


        # Beat 5: Formalizing the Discriminant
        # ------------------------------------
        full_quad_formula = MathTex(
            "x = {-b \\pm \\sqrt{", "b^2 - 4ac", "}} \\over {2a}}", 
            color=WHITE
        ).scale(1.2).to_edge(UP)

        discriminant_label = MathTex("\\Delta = b^2 - 4ac", color=GOLD_ACCENT).next_to(full_quad_formula, DOWN, buff=1)
        discriminant_label.align_to(full_quad_formula[1], LEFT) 

        self.play(
            FadeTransform(quad_formula_part, full_quad_formula[1]),
            Write(full_quad_formula[0]),
            Write(full_quad_formula[2]),
            run_time=1.5
        )
        self.play(ReplacementTransform(full_quad_formula[1].copy(), discriminant_label))
        self.wait(1.5)

        final_cases = VGroup(
            MathTex("\\Delta > 0 \\implies ", "\\text{Two Real Roots}", color=WHITE),
            MathTex("\\Delta = 0 \\implies ", "\\text{One Real Root}", color=WHITE),
            MathTex("\\Delta < 0 \\implies ", "\\text{No Real Roots}", color=WHITE)
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).next_to(discriminant_label, DOWN, buff=1)
        
        final_cases.set_color_by_tex_to_color_map({
            "\\Delta > 0": BLUE_ACCENT,
            "\\Delta = 0": BLUE_ACCENT,
            "\\Delta < 0": BLUE_ACCENT,
            "Two Real Roots": GOLD_ACCENT,
            "One Real Root": GOLD_ACCENT,
            "No Real Roots": GOLD_ACCENT
        })
        
        self.play(LaggedStart(*[Write(t) for t in final_cases], lag_ratio=0.5))
        self.wait(2)


        # Recap Card
        # ----------
        self.play(
            FadeOut(full_quad_formula),
            FadeOut(discriminant_label),
            FadeOut(final_cases)
        )
        self.wait(0.5)

        recap_title = Text("Recap: The Discriminant (Δ)", font_size=48, color=BLUE_ACCENT).to_edge(UP, buff=0.8)
        recap_formula = MathTex("\\Delta = b^2 - 4ac", color=GOLD_ACCENT).next_to(recap_title, DOWN, buff=0.8)
        
        recap_points = VGroup(
            MathTex("\\Delta > 0:", "\\text{ Two Distinct Real Roots (Parabola crosses x-axis twice)}", color=WHITE),
            MathTex("\\Delta = 0:", "\\text{ One Real Root (Parabola is tangent to x-axis)}", color=WHITE),
            MathTex("\\Delta < 0:", "\\text{ No Real Roots (Parabola does not cross x-axis)}", color=WHITE)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(recap_formula, DOWN, buff=0.8)
        
        recap_points.set_color_by_tex_to_color_map({
            "\\Delta > 0:": BLUE_ACCENT,
            "\\Delta = 0:": BLUE_ACCENT,
            "\\Delta < 0:": BLUE_ACCENT,
            "Two Distinct Real Roots": GOLD_ACCENT,
            "One Real Root": GOLD_ACCENT,
            "No Real Roots": GOLD_ACCENT
        })
        
        self.play(Write(recap_title), Create(recap_formula))
        self.play(LaggedStart(*[Write(p) for p in recap_points], lag_ratio=0.5))
        self.wait(3)

        self.play(FadeOut(VGroup(recap_title, recap_formula, recap_points)))
        self.wait(1)