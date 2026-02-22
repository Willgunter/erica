from manim import *

class GeometricInterpretationDiscriminant(Scene):
    def construct(self):
        # 0. Configuration and Initial Setup
        self.camera.background_color = "#1A1A1A"  # Clean dark grey background
        default_color_blue = BLUE_C # High-contrast blue
        default_color_gold = GOLD_A # High-contrast gold

        # Title Card
        title = Text("Geometric Interpretation: The Discriminant", font_size=52, color=default_color_gold)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title, shift=UP))

        # Graph Setup
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY, "stroke_width": 2},
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(
            x_label=Text("x", color=GRAY).scale(0.7),
            y_label=Text("y", color=GRAY).scale(0.7)
        )
        graph_group = VGroup(axes, axes_labels)
        self.play(Create(graph_group), run_time=1.5)

        # Visual Hook & Beat 1: Quadratic Equation = Parabola
        # Start with a parabola that clearly crosses the x-axis
        initial_parabola = axes.plot(lambda x: x**2 - 2, color=default_color_blue)
        equation_label = Text("y = ax² + bx + c", color=default_color_gold, font_size=32).to_edge(UP).shift(LEFT*2)
        equation_intro = Text("Quadratic Equation:", color=GRAY, font_size=24).next_to(equation_label, LEFT, buff=0.2)

        self.play(Create(initial_parabola), run_time=1)
        self.play(Write(equation_intro), Write(equation_label))

        parabola_text_desc = Text("...always forms a PARABOLA!", color=default_color_gold, font_size=30).next_to(equation_label, DOWN, buff=0.5)
        self.play(Write(parabola_text_desc))
        self.wait(1)

        # Demonstrate 'c' changing
        temp_equation = Text("y = x² - 2", color=default_color_gold, font_size=32).move_to(equation_label.get_center())
        self.play(ReplacementTransform(equation_label, temp_equation))
        self.wait(0.5)
        
        # Move parabola up
        self.play(
            initial_parabola.animate.shift(UP * 2),
            temp_equation.animate.become(Text("y = x²", color=default_color_gold, font_size=32).move_to(temp_equation.get_center())),
            run_time=1
        )
        self.wait(0.5)
        # Move parabola down
        self.play(
            initial_parabola.animate.shift(DOWN * 4),
            temp_equation.animate.become(Text("y = x² - 4", color=default_color_gold, font_size=32).move_to(temp_equation.get_center())),
            run_time=1
        )
        self.wait(0.5)
        self.play(FadeOut(parabola_text_desc))


        # Beat 2: Two Distinct Real Roots (Parabola crosses x-axis twice)
        current_parabola = axes.plot(lambda x: x**2 - 2*x - 3, color=default_color_blue) # Roots at -1, 3
        equation_2_roots = Text("y = x² - 2x - 3", color=default_color_gold, font_size=32).move_to(temp_equation.get_center())

        roots_header = Text("The 'Roots' are X-intercepts", color=default_color_gold, font_size=38).to_edge(UP).shift(LEFT)
        self.play(
            ReplacementTransform(initial_parabola, current_parabola),
            ReplacementTransform(temp_equation, equation_2_roots),
            FadeOut(equation_intro),
            Write(roots_header)
        )
        self.wait(0.5)

        root1_dot = Dot(axes.c2p(-1, 0), color=GOLD)
        root2_dot = Dot(axes.c2p(3, 0), color=GOLD)
        root1_label = Text("x = -1", color=GOLD, font_size=24).next_to(root1_dot, DOWN, buff=0.1)
        root2_label = Text("x = 3", color=GOLD, font_size=24).next_to(root2_dot, DOWN, buff=0.1)

        self.play(Create(root1_dot), Create(root2_dot), run_time=1)
        self.play(Write(root1_label), Write(root2_label), run_time=1)
        
        desc_2_roots = Text("2 Distinct Real Roots", color=default_color_blue, font_size=30).next_to(roots_header, DOWN, buff=0.5)
        self.play(Write(desc_2_roots))
        self.wait(1.5)


        # Beat 3: One Real Root (Parabola touches x-axis once)
        parabola_1_root = axes.plot(lambda x: x**2 - 4*x + 4, color=default_color_blue) # Root at 2
        equation_1_root = Text("y = x² - 4x + 4", color=default_color_gold, font_size=32).move_to(equation_2_roots.get_center())

        self.play(
            FadeOut(root1_dot, target_position=root2_dot.get_center()), # Fade and move towards the new root
            FadeOut(root1_label, target_position=root2_label.get_center()),
            FadeOut(root2_label),
            FadeOut(desc_2_roots),
            Transform(current_parabola, parabola_1_root),
            ReplacementTransform(equation_2_roots, equation_1_root),
            run_time=1.5
        )
        self.wait(0.5)

        root_single_dot = Dot(axes.c2p(2, 0), color=GOLD)
        root_single_label = Text("x = 2", color=GOLD, font_size=24).next_to(root_single_dot, DOWN, buff=0.1)

        self.play(Create(root_single_dot), Write(root_single_label), run_time=1)
        
        desc_1_root = Text("1 Real Root (repeated)", color=default_color_blue, font_size=30).next_to(roots_header, DOWN, buff=0.5)
        self.play(Write(desc_1_root))
        self.wait(1.5)


        # Beat 4: Zero Real Roots (Parabola does not cross x-axis)
        parabola_0_roots = axes.plot(lambda x: x**2 + 1, color=default_color_blue) # No real roots
        equation_0_roots = Text("y = x² + 1", color=default_color_gold, font_size=32).move_to(equation_1_root.get_center())

        self.play(
            FadeOut(root_single_dot), FadeOut(root_single_label),
            FadeOut(desc_1_root),
            Transform(current_parabola, parabola_0_roots),
            ReplacementTransform(equation_1_root, equation_0_roots),
            run_time=1.5
        )
        self.wait(1)

        desc_0_roots = Text("0 Real Roots (2 Complex Roots)", color=default_color_blue, font_size=30).next_to(roots_header, DOWN, buff=0.5)
        self.play(Write(desc_0_roots))
        self.wait(1.5)


        # Beat 5: Introducing The Discriminant
        self.play(
            FadeOut(roots_header), FadeOut(desc_0_roots),
            FadeOut(equation_0_roots), # Fade out the current equation
            FadeOut(current_parabola), # current_parabola is now parabola_0_roots
            FadeOut(graph_group), # Fade out axes and labels
            run_time=1.5
        )

        discriminant_title = Text("The Discriminant (Δ)", color=default_color_gold, font_size=48).to_edge(UP)
        self.play(Write(discriminant_title))

        general_quad_eq = Text("For: ax² + bx + c = 0", color=default_color_blue, font_size=36).next_to(discriminant_title, DOWN, buff=0.6)
        discriminant_formula = Text("Δ = b² - 4ac", color=default_color_gold, font_size=56).next_to(general_quad_eq, DOWN, buff=0.7)

        self.play(Write(general_quad_eq))
        self.play(Write(discriminant_formula))
        self.wait(1)

        # Cases for discriminant
        case1_text = Text("If Δ > 0", color=GOLD, font_size=32).shift(LEFT*3.5 + DOWN*0.5)
        case1_result = Text("➞ 2 Distinct Real Roots", color=default_color_blue, font_size=30).next_to(case1_text, RIGHT, buff=0.5)

        case2_text = Text("If Δ = 0", color=GOLD, font_size=32).shift(LEFT*3.5 + DOWN*1.7)
        case2_result = Text("➞ 1 Real Root (repeated)", color=default_color_blue, font_size=30).next_to(case2_text, RIGHT, buff=0.5)

        case3_text = Text("If Δ < 0", color=GOLD, font_size=32).shift(LEFT*3.5 + DOWN*2.9)
        case3_result = Text("➞ 0 Real Roots (2 Complex)", color=default_color_blue, font_size=30).next_to(case3_text, RIGHT, buff=0.5)

        cases_group = VGroup(
            VGroup(case1_text, case1_result),
            VGroup(case2_text, case2_result),
            VGroup(case3_text, case3_result)
        )

        self.play(LaggedStart(*[Write(mob) for mob in cases_group], lag_ratio=0.5), run_time=3)
        self.wait(2.5)

        # Recap Card
        self.play(
            FadeOut(general_quad_eq),
            FadeOut(discriminant_formula),
            FadeOut(cases_group),
            Transform(discriminant_title, Text("Recap: The Discriminant", color=default_color_gold, font_size=48).to_edge(UP))
        )

        recap_points = VGroup(
            Text("• Quadratic equations form parabolas.", color=default_color_blue, font_size=28),
            Text("• Roots are where the parabola crosses the x-axis.", color=default_color_blue, font_size=28),
            Text("• The Discriminant (Δ = b² - 4ac) tells us how many real roots!", color=default_color_gold, font_size=28),
            Text("  - Δ > 0 : Two distinct real roots.", color=default_color_blue, font_size=26),
            Text("  - Δ = 0 : One real root (parabola touches x-axis).", color=default_color_blue, font_size=26),
            Text("  - Δ < 0 : No real roots (parabola does not cross x-axis).", color=default_color_blue, font_size=26)
        ).arrange(DOWN, center=True, aligned_edge=LEFT, buff=0.4).shift(DOWN*0.2) # Use arrange, not arrange_in_grid

        self.play(LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.3), run_time=4)
        self.wait(3)
        self.play(FadeOut(VGroup(discriminant_title, recap_points)))
        self.wait(1)