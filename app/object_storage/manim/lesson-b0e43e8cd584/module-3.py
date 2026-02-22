from manim import *

class ParabolaSolutionsDiscriminant(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#202020" # Dark background
        blue_color = "#5DADE2" # High-contrast blue
        gold_color = "#FFD700" # High-contrast gold
        text_color = WHITE

        # --- Beat 1: Visual Hook & Introduction ---
        # Title appears
        title = Text("Parabola Solutions & Discriminant", font_size=48, color=gold_color).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create a number plane
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": blue_color, "stroke_width": 2},
            background_line_style={"stroke_opacity": 0.3}
        ).shift(DOWN * 0.5)
        
        # Add X and Y axis labels using Text
        x_label = Text("X", font_size=24, color=blue_color).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1)
        y_label = Text("Y", font_size=24, color=blue_color).next_to(plane.y_axis.get_end(), UP, buff=0.1)

        self.play(Create(plane), FadeIn(x_label, y_label))
        self.wait(0.5)

        # Manually create the quadratic equation Text with superscript
        quadratic_equation_base = Text("y = ax + bx + c", font_size=36, color=text_color).next_to(title, DOWN, buff=1.0)
        # Position '2' carefully for 'x^2'
        quadratic_equation_superscript = Text("2", font_size=20, color=text_color).next_to(
            quadratic_equation_base.get_parts_by_text("x")[0], UP + RIGHT * 0.2, buff=0.05
        ).shift(RIGHT * 0.05)
        
        quadratic_equation_full = VGroup(quadratic_equation_base, quadratic_equation_superscript)
        
        self.play(Write(quadratic_equation_full))
        self.wait(1)

        # Define an initial parabola with 2 solutions
        def func1(x):
            return 0.5 * x**2 - 2 
        parabola1 = plane.get_graph(func1, color=gold_color, stroke_width=4)
        
        self.play(
            Create(parabola1),
            quadratic_equation_full.animate.shift(LEFT * 3) # Move the label aside
        )
        self.wait(1)

        description1 = Text("This shape is a Parabola.", font_size=30, color=text_color).next_to(quadratic_equation_full, RIGHT, buff=0.5)
        self.play(Write(description1))
        self.wait(1.5)
        
        # --- Beat 2: Solutions (Roots) ---
        description2_text = Text("Solutions are where y = 0", font_size=30, color=text_color).move_to(description1.get_center())
        
        # Points of intersection for parabola1
        solution_points1_coords = [(-2, 0), (2, 0)]
        solution_dots1 = VGroup(*[Dot(plane.coords_to_point(x, y), color=blue_color, radius=0.15) for x, y in solution_points1_coords])
        
        self.play(
            FadeOut(description1),
            Transform(quadratic_equation_full, quadratic_equation_full.copy().shift(UP * 0.5)), # Keep the equation, shift slightly
            FadeIn(solution_dots1),
            Write(description2_text)
        )
        self.wait(1.5)

        # Case 2: One solution (touches x-axis)
        def func2(x):
            return 0.5 * x**2 
        parabola2 = plane.get_graph(func2, color=gold_color, stroke_width=4)
        solution_points2_coords = [(0, 0)]
        solution_dots2 = VGroup(*[Dot(plane.coords_to_point(x, y), color=blue_color, radius=0.15) for x, y in solution_points2_coords])
        
        self.play(
            ReplacementTransform(parabola1, parabola2),
            ReplacementTransform(solution_dots1, solution_dots2),
            FadeOut(description2_text)
        )
        self.wait(1)

        # Case 3: Zero solutions (above x-axis)
        def func3(x):
            return 0.5 * x**2 + 2 
        parabola3 = plane.get_graph(func3, color=gold_color, stroke_width=4)
        
        no_solutions_text = Text("No solutions here.", font_size=30, color=text_color).next_to(quadratic_equation_full, RIGHT, buff=0.5)

        self.play(
            ReplacementTransform(parabola2, parabola3),
            FadeOut(solution_dots2), # Solutions disappear
            Write(no_solutions_text)
        )
        self.wait(1.5)
        
        # --- Beat 3: The Discriminant - Predicting Solutions ---
        # Introduce the concept of discriminant without formula yet
        discriminant_concept = Text("How do we know?", font_size=36, color=gold_color).move_to(no_solutions_text.get_center())
        
        self.play(
            FadeOut(no_solutions_text),
            Write(discriminant_concept)
        )
        self.wait(1)
        
        # Introduce the discriminant part (b^2 - 4ac) using Text
        discriminant_formula_base = Text("b - 4ac", font_size=36, color=text_color)
        discriminant_formula_superscript = Text("2", font_size=20, color=text_color).next_to(
            discriminant_formula_base.get_parts_by_text("b")[0], UP + RIGHT * 0.2, buff=0.05
        ).shift(RIGHT * 0.05)
        discriminant_formula_label = VGroup(discriminant_formula_base, discriminant_formula_superscript)
        
        discriminant_formula_label.next_to(quadratic_equation_full, DOWN, buff=0.5).align_to(quadratic_equation_full, LEFT)

        self.play(
            FadeOut(discriminant_concept),
            FadeIn(discriminant_formula_label)
        )
        self.wait(1.5)

        # Cases for discriminant with animations
        # Case 1: > 0 (two solutions)
        delta_gt_0_text = Text(" > 0  (2 solutions)", font_size=30, color=blue_color).next_to(discriminant_formula_label, RIGHT, buff=0.5)
        
        self.play(
            FadeIn(delta_gt_0_text),
            Transform(parabola3, parabola1) # Back to 2 solutions
        )
        self.wait(1.5)

        # Add the dots for the 2 solutions
        solution_dots_reappear = VGroup(*[Dot(plane.coords_to_point(x, y), color=blue_color, radius=0.15) for x, y in solution_points1_coords])
        self.play(FadeIn(solution_dots_reappear))
        self.wait(0.5)

        # Case 2: = 0 (one solution)
        delta_eq_0_text = Text(" = 0  (1 solution)", font_size=30, color=gold_color).move_to(delta_gt_0_text.get_center())
        self.play(
            ReplacementTransform(delta_gt_0_text, delta_eq_0_text),
            Transform(parabola1, parabola2), # To 1 solution
            ReplacementTransform(solution_dots_reappear, solution_dots2) # To 1 dot
        )
        self.wait(1.5)

        # Case 3: < 0 (zero solutions)
        delta_lt_0_text = Text(" < 0  (No solutions)", font_size=30, color=text_color).move_to(delta_eq_0_text.get_center())
        self.play(
            ReplacementTransform(delta_eq_0_text, delta_lt_0_text),
            Transform(parabola2, parabola3), # To 0 solutions
            FadeOut(solution_dots2) # Dots disappear
        )
        self.wait(1.5)

        # --- Beat 4: Formalizing the Discriminant ---
        # Introduce Delta symbol
        delta_symbol = Text("Δ", font_size=48, color=gold_color)
        discriminant_label_formal_base = Text(" = b - 4ac", font_size=36, color=text_color).next_to(delta_symbol, RIGHT, buff=0.1)
        discriminant_label_formal_superscript = Text("2", font_size=20, color=text_color).next_to(
            discriminant_label_formal_base.get_parts_by_text("b")[0], UP + RIGHT * 0.2, buff=0.05
        ).shift(RIGHT * 0.05)
        
        discriminant_label_formal = VGroup(delta_symbol, discriminant_label_formal_base, discriminant_label_formal_superscript)
        
        discriminant_label_formal.move_to(discriminant_formula_label.get_center()).shift(LEFT * 0.5)

        self.play(
            FadeOut(discriminant_formula_label),
            FadeIn(delta_symbol),
            FadeIn(discriminant_label_formal_base),
            FadeIn(discriminant_label_formal_superscript),
            FadeOut(delta_lt_0_text) 
        )
        self.wait(1)

        # Reiterate cases with Delta
        summary_cases = VGroup(
            Text("Δ > 0 :  2 Solutions", font_size=28, color=blue_color),
            Text("Δ = 0 :  1 Solution", font_size=28, color=gold_color),
            Text("Δ < 0 :  0 Solutions", font_size=28, color=text_color)
        ).arrange(DOWN, buff=0.4).next_to(discriminant_label_formal, DOWN, buff=1.0).align_to(discriminant_label_formal, LEFT)

        self.play(
            LaggedStart(*[FadeIn(case) for case in summary_cases]),
            parabola3.animate.set_opacity(0.5) # Dim the parabola slightly for text focus
        )
        self.wait(2)

        # Animate the parabola through the three states while emphasizing text
        self.play(parabola3.animate.set_opacity(1)) 
        
        temp_dots1 = VGroup(*[Dot(plane.coords_to_point(x, y), color=blue_color, radius=0.15) for x, y in solution_points1_coords])
        self.play(
            Transform(parabola3, plane.get_graph(func1, color=gold_color, stroke_width=4)), # Two solutions
            FadeIn(temp_dots1),
            FadeIn(summary_cases[0].copy().scale(1.2).set_color(blue_color).shift(UP*0.1)), # Emphasize first case
            run_time=1.5
        )
        self.wait(0.5)
        
        temp_dots2 = VGroup(*[Dot(plane.coords_to_point(x, y), color=blue_color, radius=0.15) for x, y in solution_points2_coords])
        self.play(
            Transform(parabola3, plane.get_graph(func2, color=gold_color, stroke_width=4)), # One solution
            ReplacementTransform(temp_dots1, temp_dots2),
            FadeOut(self.mobjects[-1]), # Remove previous highlight copy
            FadeIn(summary_cases[1].copy().scale(1.2).set_color(gold_color).shift(UP*0.1)), # Emphasize second case
            run_time=1.5
        )
        self.wait(0.5)
        
        self.play(
            Transform(parabola3, plane.get_graph(func3, color=gold_color, stroke_width=4)), # Zero solutions
            FadeOut(temp_dots2),
            FadeOut(self.mobjects[-1]), # Remove previous highlight copy
            FadeIn(summary_cases[2].copy().scale(1.2).set_color(text_color).shift(UP*0.1)), # Emphasize third case
            run_time=1.5
        )
        self.wait(2)

        # --- Recap Card ---
        self.play(
            FadeOut(plane),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(title),
            FadeOut(quadratic_equation_full),
            FadeOut(parabola3),
            FadeOut(discriminant_label_formal),
            FadeOut(summary_cases),
            FadeOut(self.mobjects[-1]), # Remove last emphasis
        )

        recap_title = Text("Recap:", font_size=48, color=gold_color).to_edge(UP)
        
        # Create all recap text objects
        recap_points_base = [
            Text("Parabola: y = ax + bx + c", font_size=36, color=text_color),
            Text("2", font_size=20, color=text_color), # Superscript for x^2
            Text("Solutions are where it crosses X-axis (y=0)", font_size=36, color=text_color),
            Text("Discriminant: Δ = b - 4ac", font_size=36, color=text_color),
            Text("2", font_size=20, color=text_color), # Superscript for b^2
            Text("Δ > 0 : 2 Solutions", font_size=36, color=blue_color),
            Text("Δ = 0 : 1 Solution", font_size=36, color=gold_color),
            Text("Δ < 0 : 0 Solutions", font_size=36, color=text_color)
        ]
        
        # Assemble quadratic equation
        recap_eq_parabola_parts = [recap_points_base[0].get_parts_by_text("y = ax")[0], recap_points_base[1], recap_points_base[0].get_parts_by_text("+ bx + c")[0]]
        recap_eq_parabola = VGroup(*recap_eq_parabola_parts).arrange(RIGHT, buff=0.05, aligned_edge=DOWN).next_to(recap_title, DOWN, buff=1.0)
        recap_points_base[1].next_to(recap_points_base[0].get_parts_by_text("x")[0], UP + RIGHT * 0.2, buff=0.05).shift(RIGHT * 0.05)
        
        recap_solutions = recap_points_base[2].next_to(recap_eq_parabola, DOWN, buff=0.8)

        # Assemble discriminant formula
        recap_eq_discriminant_parts = [recap_points_base[3].get_parts_by_text("Δ = b")[0], recap_points_base[4], recap_points_base[3].get_parts_by_text("- 4ac")[0]]
        recap_eq_discriminant = VGroup(*recap_eq_discriminant_parts).arrange(RIGHT, buff=0.05, aligned_edge=DOWN).next_to(recap_solutions, DOWN, buff=0.8)
        recap_points_base[4].next_to(recap_points_base[3].get_parts_by_text("b")[0], UP + RIGHT * 0.2, buff=0.05).shift(RIGHT * 0.05)

        recap_cases = VGroup(recap_points_base[5], recap_points_base[6], recap_points_base[7]).arrange(DOWN, buff=0.4).next_to(recap_eq_discriminant, DOWN, buff=0.8)
        
        all_recap_items = VGroup(recap_title, recap_eq_parabola, recap_solutions, recap_eq_discriminant, recap_cases)
        all_recap_items.scale(0.8).center()

        self.play(
            FadeIn(recap_title),
            LaggedStart(
                FadeIn(recap_eq_parabola),
                FadeIn(recap_solutions),
                FadeIn(recap_eq_discriminant),
                FadeIn(recap_cases),
                lag_ratio=0.5
            )
        )
        self.wait(3)