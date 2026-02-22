from manim import *

# Define custom colors for a 3Blue1Brown-inspired look
BLUE_ACCENT = "#87CEEB"  # Bright Sky Blue
GOLD_ACCENT = "#FFD700"  # Classic Gold
DARK_BACKGROUND = "#1A1A2E" # A deep, slightly desaturated purple-blue

class QuadraticFormulaTrick(Scene):
    def construct(self):
        # Set background color for the entire scene
        self.camera.background_color = DARK_BACKGROUND

        # --- Beat 1: The Visual Hook - Parabola Symmetry (approx. 8-10s) ---
        title = Text("Quadratic Formula: An Intuitive Trick", font_size=48).to_edge(UP).set_color(GOLD_ACCENT)
        self.play(Write(title))
        self.wait(0.5)

        # Setup axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 6, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": GRAY, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-4, -2, 0, 2, 4]},
            y_axis_config={"numbers_to_include": [-2, 0, 2, 4]},
        ).shift(DOWN * 0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Create(labels), run_time=1.5)

        # Start with a simple symmetric parabola: y = x^2 - 4
        parabola_simple = axes.get_graph(lambda x: x**2 - 4, x_range=[-3, 3], color=BLUE_ACCENT)
        root1_simple_dot = Dot(axes.coords_to_point(-2, 0), color=GOLD_ACCENT, radius=0.1)
        root2_simple_dot = Dot(axes.coords_to_point(2, 0), color=GOLD_ACCENT, radius=0.1)
        
        self.play(Create(parabola_simple), FadeIn(root1_simple_dot, root2_simple_dot), run_time=1.5)
        self.wait(0.5)

        center_line_simple = axes.get_vertical_line(axes.coords_to_point(0, 0), color=GRAY_A, stroke_width=2)
        center_label_simple = MathTex("x=0", color=GRAY_A).next_to(center_line_simple, UP, buff=0.2)
        self.play(Create(center_line_simple), FadeIn(center_label_simple))
        self.wait(1)

        # Introduce a general quadratic equation
        eq_general = MathTex("ax^2 + bx + c = 0", color=BLUE_ACCENT).next_to(title, DOWN)
        self.play(
            FadeOut(parabola_simple, root1_simple_dot, root2_simple_dot, center_line_simple, center_label_simple),
            ReplacementTransform(title, eq_general),
            run_time=1.2
        )
        self.wait(0.5)

        # --- Beat 2: The Center of Symmetry (approx. 8-10s) ---
        # Show a more complex parabola (example: y = x^2 + 2x - 3)
        # Vertex at (-1, -4), roots at (-3, 0) and (1, 0)
        parabola_shifted = axes.get_graph(lambda x: x**2 + 2*x - 3, x_range=[-4.5, 2.5], color=BLUE_ACCENT)
        root1_shifted_dot = Dot(axes.coords_to_point(-3, 0), color=GOLD_ACCENT, radius=0.1)
        root2_shifted_dot = Dot(axes.coords_to_point(1, 0), color=GOLD_ACCENT, radius=0.1)
        
        self.play(Create(parabola_shifted), FadeIn(root1_shifted_dot, root2_shifted_dot), run_time=1.5)
        self.wait(0.5)

        # Reveal the center line of this parabola
        center_x_val = -1 # for y = x^2 + 2x - 3
        center_line_shifted = axes.get_vertical_line(axes.coords_to_point(center_x_val, 0), color=GOLD_ACCENT, stroke_width=3)
        center_label_val = MathTex("x = -1", color=GOLD_ACCENT).next_to(center_line_shifted, UP, buff=0.2)

        self.play(Create(center_line_shifted), Write(center_label_val))
        self.wait(1)

        # Introduce the formula for the center of symmetry
        center_formula_tex = MathTex("x_{\\text{center}} = -\\frac{b}{2a}", color=GOLD_ACCENT).next_to(eq_general, DOWN, buff=0.5)
        self.play(
            Write(center_formula_tex), 
            FadeOut(center_label_val), 
            center_line_shifted.animate.set_color(BLUE_ACCENT).set_stroke_width(2)
        )
        self.wait(1)

        # --- Beat 3: The Distance from Center 'd' (approx. 10-12s) ---
        # Show the roots as the center plus/minus a distance 'd'
        arrow_left = Arrow(start=center_line_shifted.get_top(), end=root1_shifted_dot.get_center(), buff=0.1, color=BLUE_ACCENT)
        arrow_right = Arrow(start=center_line_shifted.get_top(), end=root2_shifted_dot.get_center(), buff=0.1, color=BLUE_ACCENT)
        distance_label_d = MathTex("d", color=BLUE_ACCENT).next_to(arrow_right, UP, buff=0.1)
        
        self.play(Create(arrow_left), Create(arrow_right), Write(distance_label_d))
        self.wait(1)

        # Express roots generically: x = x_center +/- d
        roots_sym_tex = MathTex("x = x_{\\text{center}} \\pm d", color=BLUE_ACCENT).next_to(center_formula_tex, DOWN, buff=0.5)
        self.play(Write(roots_sym_tex))
        self.wait(1)

        # Fade out specific parabola and dots, keep axes, general eq, center formula, and roots_sym_tex
        self.play(FadeOut(parabola_shifted, root1_shifted_dot, root2_shifted_dot, 
                          arrow_left, arrow_right, distance_label_d, center_line_shifted))

        # The "trick" is recognizing how 'd' relates to the discriminant
        # Show the discriminant part
        discriminant_tex = MathTex("\\Delta = b^2 - 4ac", color=GOLD_ACCENT).next_to(roots_sym_tex, DOWN, buff=0.5)
        self.play(Write(discriminant_tex))
        self.wait(1)
        
        # Directly reveal the formula for d, implying the algebraic steps
        d_formula_tex = MathTex("d = \\frac{\\sqrt{\\Delta}}{2a}", color=BLUE_ACCENT).next_to(discriminant_tex, DOWN, buff=0.5)
        self.play(Write(d_formula_tex))
        self.wait(1.5)
        
        # --- Beat 4: Combining for the Full Formula (approx. 8-10s) ---
        # Position the pieces to combine
        self.play(
            LaggedStart(
                center_formula_tex.animate.next_to(eq_general, DOWN, buff=0.5).to_edge(LEFT),
                d_formula_tex.animate.next_to(center_formula_tex, RIGHT, buff=0.7),
                FadeOut(roots_sym_tex, discriminant_tex)
            )
        )
        self.wait(0.5)

        # Combine x_center and d
        combined_qf_parts = MathTex("x = -\\frac{b}{2a} \\pm \\frac{\\sqrt{\\Delta}}{2a}", color=BLUE_ACCENT).next_to(eq_general, DOWN, buff=0.5).center()
        self.play(ReplacementTransform(VGroup(center_formula_tex, d_formula_tex), combined_qf_parts))
        self.wait(1.5)

        # Substitute Delta back in
        final_qf = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT).next_to(combined_qf_parts, DOWN, buff=0.7)
        self.play(ReplacementTransform(combined_qf_parts, final_qf))
        self.wait(2)

        # --- Beat 5: Recap Card (approx. 5-7s) ---
        self.play(FadeOut(eq_general, axes, labels)) # Clear previous objects

        recap_card_title = Text("Recap: The Quadratic Formula Trick", font_size=40).set_color(GOLD_ACCENT).to_edge(UP)
        
        # Split the formula to highlight components
        recap_formula = MathTex(
            "x = \\underbrace{\\frac{-b}{2a}}_{\\text{Center of Symmetry}} \\pm \\underbrace{\\frac{\\sqrt{b^2 - 4ac}}{2a}}_{\\text{Distance from Center}}",
            substrings_to_isolate=["{-b}/{2a}", "{\\sqrt{b^2 - 4ac}}/{2a}", "Center of Symmetry", "Distance from Center"]
        ).set_color_by_tex_to_color_map({
            "{-b}/{2a}": BLUE_ACCENT,
            "{\\sqrt{b^2 - 4ac}}/{2a}": GOLD_ACCENT,
            "Center of Symmetry": BLUE_ACCENT,
            "Distance from Center": GOLD_ACCENT
        }).scale(1.2).center()

        # Initial render of just the formula part, then add underbraces and labels
        initial_recap_formula_tex = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", color=GOLD_ACCENT).scale(1.2).center()

        self.play(
            ReplacementTransform(final_qf, initial_recap_formula_tex),
            Write(recap_card_title)
        )
        self.wait(1)
        
        self.play(
            TransformMatchingTex(initial_recap_formula_tex, recap_formula)
        )
        
        self.wait(3)

        self.play(FadeOut(recap_card_title, recap_formula))
        self.wait(1)