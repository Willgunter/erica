from manim import *

# Configuration
config.background_color = BLACK
config.frame_width = 16  # Standard 16:9 aspect ratio
config.frame_height = 9

class GeometricInterpretationDiscriminant(Scene):
    def construct(self):
        # Colors for consistency
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E
        TEXT_COLOR = WHITE

        # --- BEAT 1: Visual Hook & Intro to Parabola ---
        # 1. Visual Hook: Dynamic parabola
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=12,
            y_length=12,
            axis_config={"color": GRAY_A},
            background_line_style={"stroke_color": GRAY_B, "stroke_width": 1, "stroke_opacity": 0.6}
        ).add_coordinates()
        axes_labels = plane.get_axis_labels(x_label="X", y_label="Y")

        self.play(Create(plane), Create(axes_labels), run_time=1.5)
        self.wait(0.5)

        # Initial parabola for the hook
        initial_parabola_func = lambda x: 0.5 * x**2 - 1
        initial_parabola = plane.get_graph(initial_parabola_func, color=BLUE_ACCENT)
        self.play(Create(initial_parabola), run_time=1.5)
        self.wait(0.5)

        # Rapid transformation to another parabola to show dynamism
        parabola_a_hook = ValueTracker(0.5)
        parabola_b_hook = ValueTracker(0)
        parabola_c_hook = ValueTracker(-1)

        def get_parabola_mob(a, b, c, color=BLUE_ACCENT):
            return plane.get_graph(lambda x: a * x**2 + b * x + c, color=color)

        # Animate initial parabola to a different shape/position
        # This gives the "dynamic" feel
        new_parabola_mob = get_parabola_mob(1, 2, 1) # Example target
        self.play(
            Transform(initial_parabola, new_parabola_mob),
            parabola_a_hook.animate.set_value(1),
            parabola_b_hook.animate.set_value(2),
            parabola_c_hook.animate.set_value(1),
            run_time=2
        )
        self.wait(0.5)

        # Title and Equation Introduction (using Text)
        title = Text("Quadratic Equations", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title, shift=UP))

        # Equation y = ax^2 + bx + c (Constructed with Text)
        y_label = Text("y =", font_size=38, color=TEXT_COLOR)
        a_label = Text("a", font_size=38, color=GOLD_ACCENT)
        x2_label = Text("x²", font_size=38, color=TEXT_COLOR) # Using Unicode for superscript
        plus_b_label = Text("+ b", font_size=38, color=BLUE_ACCENT)
        x_label_single = Text("x", font_size=38, color=TEXT_COLOR)
        plus_c_label = Text("+ c", font_size=38, color=GOLD_ACCENT)

        quadratic_equation_text = VGroup(y_label, a_label, x2_label, plus_b_label, x_label_single, plus_c_label).arrange(RIGHT, buff=0.1)
        quadratic_equation_text.next_to(title, DOWN, buff=0.7)

        self.play(LaggedStart(*[FadeIn(part, shift=UP) for part in quadratic_equation_text], lag_ratio=0.1), run_time=2)
        self.wait(1)

        # --- BEAT 2: Role of 'a', 'b', 'c' ---
        # ValueTrackers for parabola coefficients
        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(2)
        c_tracker = ValueTracker(1)

        # Create an always_redraw parabola that responds to trackers
        parabola = always_redraw(lambda: plane.get_graph(
            lambda x: a_tracker.get_value() * x**2 + b_tracker.get_value() * x + c_tracker.get_value(),
            color=BLUE_ACCENT
        ))
        self.remove(initial_parabola) # Remove the old static/transformed parabola
        self.add(parabola) # Add the new dynamic parabola

        # Explanation of 'a'
        a_explanation = Text("Coefficient 'a': Controls width & direction", font_size=30, color=TEXT_COLOR).next_to(quadratic_equation_text, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(FadeIn(a_explanation))
        self.play(
            a_tracker.animate.set_value(0.1), # Wider
            run_time=1.5
        )
        self.play(
            a_tracker.animate.set_value(-0.5), # Downwards
            run_time=1.5
        )
        self.play(
            a_tracker.animate.set_value(2), # Narrower
            run_time=1.5
        )
        self.play(FadeOut(a_explanation))
        self.wait(0.5)

        # Explanation of 'b'
        b_explanation = Text("Coefficient 'b': Shifts the vertex horizontally", font_size=30, color=TEXT_COLOR).next_to(quadratic_equation_text, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(FadeIn(b_explanation))
        self.play(
            b_tracker.animate.set_value(-4), # Shift right
            run_time=2
        )
        self.play(
            b_tracker.animate.set_value(4), # Shift left
            run_time=2
        )
        self.play(FadeOut(b_explanation))
        self.wait(0.5)

        # Explanation of 'c'
        c_explanation = Text("Coefficient 'c': Shifts the parabola vertically (y-intercept)", font_size=30, color=TEXT_COLOR).next_to(quadratic_equation_text, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(FadeIn(c_explanation))
        self.play(
            c_tracker.animate.set_value(4), # Shift up
            run_time=1.5
        )
        self.play(
            c_tracker.animate.set_value(-3), # Shift down
            run_time=1.5
        )
        self.play(FadeOut(c_explanation))
        self.wait(0.5)

        # Reset parabola to a standard form with two roots for the next beat
        self.play(
            a_tracker.animate.set_value(1),
            b_tracker.animate.set_value(-2),
            c_tracker.animate.set_value(-3), # Parabola: y = x^2 - 2x - 3 (roots at x=3, x=-1)
            run_time=2
        )
        self.wait(1)

        # --- BEAT 3: Roots/X-intercepts ---
        # Focus on roots
        roots_title = Text("Roots: Where the parabola crosses the X-axis", font_size=40, color=GOLD_ACCENT).next_to(quadratic_equation_text, DOWN, buff=0.5)
        self.play(ReplacementTransform(quadratic_equation_text, roots_title)) # Replace equation with roots title

        # Highlight x-axis
        x_axis_highlight = Line(plane.x_range[0] * plane.x_unit_size, plane.x_range[1] * plane.x_unit_size, color=YELLOW, stroke_width=4).move_to(plane.c2p(0, 0))
        self.play(Create(x_axis_highlight))
        self.wait(0.5)

        # Display number of roots
        num_roots_label = Text("Number of Real Roots:", font_size=30, color=TEXT_COLOR).to_edge(DR).shift(LEFT*2)
        current_roots_text = Text("2", font_size=30, color=BLUE_ACCENT).next_to(num_roots_label, RIGHT)
        self.play(FadeIn(num_roots_label), FadeIn(current_roots_text))
        self.wait(1)

        # Transition to 1 root (touching the x-axis)
        # Parabola: y = x^2 - 2x + 1 (root at x=1)
        self.play(
            c_tracker.animate.set_value(1),
            Transform(current_roots_text, Text("1", font_size=30, color=GOLD_ACCENT).next_to(num_roots_label, RIGHT)),
            run_time=2
        )
        self.wait(1)

        # Transition to 0 roots (above/below x-axis)
        # Parabola: y = x^2 - 2x + 5 (no real roots)
        self.play(
            c_tracker.animate.set_value(5),
            Transform(current_roots_text, Text("0", font_size=30, color=RED).next_to(num_roots_label, RIGHT)),
            run_time=2
        )
        self.wait(1)
        self.play(FadeOut(num_roots_label), FadeOut(current_roots_text), FadeOut(roots_title))
        self.wait(0.5)

        # --- BEAT 4: The Discriminant (Intuition & Formula) ---
        # Re-introduce quadratic equation as context
        self.play(ReplacementTransform(x_axis_highlight, quadratic_equation_text.copy().move_to(roots_title.get_center())))
        self.wait(0.5)

        discriminant_intro = Text("How many roots? The Discriminant tells us!", font_size=40, color=GOLD_ACCENT).next_to(quadratic_equation_text, DOWN, buff=0.5)
        self.play(Transform(quadratic_equation_text, discriminant_intro)) # Replace equation text with discriminant intro
        self.wait(1)

        # Discriminant formula (Constructed with Text)
        delta_symbol = Text("Δ =", font_size=38, color=TEXT_COLOR)
        b2_term = Text("b²", font_size=38, color=BLUE_ACCENT)
        minus_4ac_term = Text(" - 4ac", font_size=38, color=GOLD_ACCENT)

        discriminant_formula = VGroup(delta_symbol, b2_term, minus_4ac_term).arrange(RIGHT, buff=0.1)
        discriminant_formula.next_to(discriminant_intro, DOWN, buff=0.7)

        self.play(LaggedStart(*[FadeIn(part, shift=UP) for part in discriminant_formula], lag_ratio=0.1), run_time=2)
        self.wait(1)

        # Remove previous explanations for a cleaner screen
        self.play(FadeOut(title), FadeOut(discriminant_intro))
        self.wait(0.5)

        # Move discriminant formula to top for continued use
        self.play(discriminant_formula.animate.to_edge(UP).shift(DOWN*0.5))
        self.wait(0.5)

        # --- BEAT 5: Discriminant Cases ---
        # Reset parabola to have 2 roots initially for D > 0
        self.play(
            a_tracker.animate.set_value(1),
            b_tracker.animate.set_value(-2),
            c_tracker.animate.set_value(-3), # D = (-2)^2 - 4(1)(-3) = 4 + 12 = 16 ( > 0)
            run_time=1.5
        )
        self.wait(0.5)

        # D > 0 case
        d_greater_0_text = Text("Δ > 0 : Two Real Roots", font_size=35, color=BLUE_ACCENT).next_to(discriminant_formula, DOWN, buff=0.7)
        d_value_label = Text("Δ = 16", font_size=30, color=BLUE_ACCENT).next_to(d_greater_0_text, RIGHT, buff=0.5)
        self.play(FadeIn(d_greater_0_text), FadeIn(d_value_label))
        self.wait(2)

        # D = 0 case
        # Update text for the new case and new discriminant value
        new_d_0_text = Text("Δ = 0 : One Real Root", font_size=35, color=GOLD_ACCENT).next_to(discriminant_formula, DOWN, buff=0.7)
        new_d_0_value_label = Text("Δ = 0", font_size=30, color=GOLD_ACCENT).next_to(new_d_0_text, RIGHT, buff=0.5)
        self.play(
            c_tracker.animate.set_value(1), # D = (-2)^2 - 4(1)(1) = 4 - 4 = 0
            ReplacementTransform(d_greater_0_text, new_d_0_text),
            Transform(d_value_label, new_d_0_value_label),
            run_time=2
        )
        self.wait(2)

        # D < 0 case
        # Update text for the new case and new discriminant value
        new_d_less_0_text = Text("Δ < 0 : No Real Roots", font_size=35, color=RED).next_to(discriminant_formula, DOWN, buff=0.7)
        new_d_less_0_value_label = Text("Δ = -16", font_size=30, color=RED).next_to(new_d_less_0_text, RIGHT, buff=0.5)
        self.play(
            c_tracker.animate.set_value(5), # D = (-2)^2 - 4(1)(5) = 4 - 20 = -16 ( < 0)
            ReplacementTransform(new_d_0_text, new_d_less_0_text),
            Transform(d_value_label, new_d_less_0_value_label),
            run_time=2
        )
        self.wait(2)

        self.play(FadeOut(new_d_less_0_text), FadeOut(d_value_label))

        # --- Recap Card ---
        self.play(FadeOut(plane), FadeOut(axes_labels), FadeOut(parabola), FadeOut(discriminant_formula))
        self.wait(1)

        recap_title = Text("Recap: Discriminant & Roots", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        
        # Manually arrange bullet points using `next_to` and `align_to`
        bullet1 = Text("• Parabola shape: y = ax² + bx + c", font_size=35, color=TEXT_COLOR)
        bullet2 = Text("• Roots: Where parabola crosses X-axis", font_size=35, color=TEXT_COLOR)
        bullet3 = Text("• Discriminant Δ = b² - 4ac", font_size=35, color=TEXT_COLOR)
        bullet4 = Text("• Δ > 0: 2 Real Roots", font_size=35, color=BLUE_ACCENT)
        bullet5 = Text("• Δ = 0: 1 Real Root", font_size=35, color=GOLD_ACCENT)
        bullet6 = Text("• Δ < 0: 0 Real Roots", font_size=35, color=RED)

        bullet1.next_to(recap_title, DOWN, buff=1)
        bullet2.next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet3.next_to(bullet2, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet4.next_to(bullet3, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet5.next_to(bullet4, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet6.next_to(bullet5, DOWN, buff=0.5).align_to(bullet1, LEFT)

        recap_group = VGroup(recap_title, bullet1, bullet2, bullet3, bullet4, bullet5, bullet6)
        
        self.play(FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(*[FadeIn(bullet, shift=LEFT) for bullet in recap_group[1:]], lag_ratio=0.15), run_time=3)
        self.wait(3)
        self.play(FadeOut(recap_group))
        self.wait(1)