from manim import *

class DefiningQuadraticEquations(Scene):
    def construct(self):
        # --- Configuration & Colors (3Blue1Brown Inspired) ---
        config.background_color = BLACK
        BLUE_COLOR = "#87CEEB"  # Sky Blue for primary curve
        GOLD_COLOR = "#FFD700"  # Gold for main equations/titles
        GREEN_COLOR = "#7CFC00" # Lawn Green for positive/coefficients
        RED_COLOR = "#FF6347"   # Tomato for constraints/negative

        # --- Beat 1: The Visual Hook & Intuition - What is a Parabola? ---
        # Module Title
        title = Text("Defining Quadratic Equations & Formula", font_size=48, color=GOLD_COLOR)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7), run_time=0.8)
        self.wait(0.5)

        # Create a NumberPlane
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": GREY_B},
            background_line_style={"stroke_opacity": 0.4}
        ).add_coordinates()
        plane.shift(DOWN * 0.5) # Shift slightly down to make room for title

        # The basic parabola y = x^2
        parabola_func = lambda x: x**2
        initial_parabola = plane.plot(parabola_func, x_range=[-2.5, 2.5], color=BLUE_COLOR)
        parabola_label_y_x2 = MathTex("y = x^2", color=BLUE_COLOR).next_to(initial_parabola, RIGHT, buff=0.5).shift(UP*0.5)

        # Introduction text
        intro_text = Text("This is a Parabola.", font_size=36, color=GOLD_COLOR).next_to(plane, DOWN, buff=1)
        intro_desc = Text("A special curve, often seen in nature.", font_size=28, color=WHITE).next_to(intro_text, DOWN)

        self.play(Create(plane, run_time=1))
        self.play(Create(initial_parabola), Write(parabola_label_y_x2), run_time=1.5)
        self.play(FadeIn(intro_text, shift=UP), FadeIn(intro_desc, shift=UP), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(intro_text, shift=DOWN), FadeOut(intro_desc, shift=DOWN), run_time=0.8)

        # --- Beat 2: Introducing the Quadratic Equation (Intuitive Form) ---
        # General form: y = ax^2 + bx + c
        y_eq_abc = MathTex("y = ax^2 + bx + c", color=GOLD_COLOR).move_to(parabola_label_y_x2.get_center())
        y_eq_abc.align_to(title, LEFT) # Keep alignment consistent

        self.play(
            ReplacementTransform(parabola_label_y_x2, y_eq_abc, run_time=1)
        )
        self.wait(0.5)

        # ValueTrackers for a, b, c
        a_val = ValueTracker(1)
        b_val = ValueTracker(0)
        c_val = ValueTracker(0)

        # Function to update the parabola based on a, b, c trackers
        def update_full_parabola(mob):
            current_a = a_val.get_value()
            current_b = b_val.get_value()
            current_c = c_val.get_value()
            new_parabola = plane.plot(lambda x: current_a * x**2 + current_b * x + current_c, x_range=[-3, 3], color=BLUE_COLOR)
            mob.become(new_parabola)

        parabola_full_dynamic = initial_parabola.copy()
        parabola_full_dynamic.add_updater(update_full_parabola)
        self.remove(initial_parabola) # Remove initial static parabola
        self.add(parabola_full_dynamic) # Add dynamic one

        # Animate 'a' changes (width and orientation)
        a_label = MathTex(f"a = {a_val.get_value():.1f}", color=GREEN_COLOR).next_to(y_eq_abc, RIGHT, buff=1.5).shift(LEFT*0.5)
        a_label.add_updater(lambda m: m.become(MathTex(f"a = {a_val.get_value():.1f}", color=GREEN_COLOR).next_to(y_eq_abc, RIGHT, buff=1.5).shift(LEFT*0.5)))
        self.add(a_label)
        self.play(a_val.animate.set_value(0.4), run_time=0.8) # Wider
        self.play(a_val.animate.set_value(-1.5), run_time=0.8) # Flips and narrows
        self.play(a_val.animate.set_value(1), run_time=0.8) # Back to original 'a'
        self.remove(a_label)

        # Animate 'b' changes (horizontal shift)
        b_label = MathTex(f"b = {b_val.get_value():.1f}", color=GREEN_COLOR).next_to(y_eq_abc, RIGHT, buff=1.5).shift(LEFT*0.5)
        b_label.add_updater(lambda m: m.become(MathTex(f"b = {b_val.get_value():.1f}", color=GREEN_COLOR).next_to(y_eq_abc, RIGHT, buff=1.5).shift(LEFT*0.5)))
        self.add(b_label)
        self.play(b_val.animate.set_value(2), run_time=0.8) # Shift left
        self.play(b_val.animate.set_value(0), run_time=0.8) # Back to original 'b'
        self.remove(b_label)

        # Animate 'c' changes (vertical shift)
        c_label = MathTex(f"c = {c_val.get_value():.1f}", color=GREEN_COLOR).next_to(y_eq_abc, RIGHT, buff=1.5).shift(LEFT*0.5)
        c_label.add_updater(lambda m: m.become(MathTex(f"c = {c_val.get_value():.1f}", color=GREEN_COLOR).next_to(y_eq_abc, RIGHT, buff=1.5).shift(LEFT*0.5)))
        self.add(c_label)
        self.play(c_val.animate.set_value(2), run_time=0.8) # Shift up
        self.play(c_val.animate.set_value(0), run_time=0.8) # Back to original 'c'
        self.remove(c_label)

        parabola_full_dynamic.remove_updater(update_full_parabola) # Stop updating

        # Restore parabola to y=x^2 state (a=1, b=0, c=0) for continuity
        final_parabola_state = plane.plot(lambda x: 1 * x**2, x_range=[-3, 3], color=BLUE_COLOR)
        self.play(ReplacementTransform(parabola_full_dynamic, final_parabola_state))
        self.wait(0.5)
        self.play(FadeOut(y_eq_abc, shift=UP), run_time=0.8)

        # --- Beat 3: Formal Definition - The Standard Form ---
        # The formal definition ax^2 + bx + c = 0
        quad_eq_formal = MathTex("ax^2 + bx + c = 0", color=GOLD_COLOR, font_size=50).move_to(y_eq_abc.get_center())

        self.play(Write(quad_eq_formal, run_time=1))

        # Explain 'a', 'b', 'c' and a != 0
        a_not_zero = MathTex("a \\neq 0", color=RED_COLOR, font_size=36).next_to(quad_eq_formal, RIGHT, buff=1)
        a_b_c_note = VGroup(
            MathTex("a, b, c", color=GOLD_COLOR),
            Text("are constant coefficients", color=WHITE, font_size=28)
        ).arrange(RIGHT, buff=0.2).next_to(a_not_zero, DOWN, buff=0.5).shift(LEFT*0.5)

        self.play(Write(a_not_zero, run_time=0.8))
        self.play(LaggedStart(*[FadeIn(mob, shift=UP) for mob in a_b_c_note], lag_ratio=0.2), run_time=1.2)
        self.wait(1)

        # Highlight a, b, c in the equation
        a_box = SurroundingRectangle(quad_eq_formal[0][0], color=GREEN_COLOR, buff=0.1) # 'a'
        b_box = SurroundingRectangle(quad_eq_formal[0][3], color=GREEN_COLOR, buff=0.1) # 'b'
        c_box = SurroundingRectangle(quad_eq_formal[0][6], color=GREEN_COLOR, buff=0.1) # 'c'

        self.play(Create(a_box, run_time=0.5))
        self.wait(0.3)
        self.play(ReplacementTransform(a_box, b_box, run_time=0.5))
        self.wait(0.3)
        self.play(ReplacementTransform(b_box, c_box, run_time=0.5))
        self.wait(0.3)
        self.play(FadeOut(c_box, run_time=0.5))

        self.play(FadeOut(a_not_zero, run_time=0.8), FadeOut(a_b_c_note, run_time=0.8))
        self.wait(0.5)

        # --- Beat 4: Why are Quadratics Important? (Brief Bio Connection) ---
        self.play(FadeOut(final_parabola_state, plane, run_time=1))
        self.play(quad_eq_formal.animate.scale(0.8).to_edge(UP, buff=1), run_time=0.8)

        importance_text = VGroup(
            Text("Why are they important?", font_size=40, color=GOLD_COLOR),
            Text("1. Describe natural phenomena (e.g., population growth curves, enzyme activity trends).", font_size=28, color=WHITE),
            Text("2. Predict future states (e.g., trajectories, peak concentrations).", font_size=28, color=WHITE),
            Text("3. Optimize processes (e.g., finding maximum yield or minimum cost).", font_size=28, color=WHITE)
        ).arrange(DOWN, buff=0.5, align_to_edge=LEFT).next_to(quad_eq_formal, DOWN, buff=1)

        self.play(LaggedStart(*[FadeIn(mob, shift=LEFT) for mob in importance_text], lag_ratio=0.2), run_time=2)
        self.wait(3)

        self.play(FadeOut(importance_text, shift=RIGHT), run_time=1)
        self.wait(0.5)

        # --- Recap Card ---
        self.play(FadeOut(quad_eq_formal, shift=UP), run_time=0.8)

        recap_title = Text("Key Takeaways", font_size=48, color=GOLD_COLOR)
        self.play(Write(recap_title), run_time=0.8)
        self.wait(0.5)
        self.play(recap_title.animate.to_edge(UP).scale(0.7), run_time=0.8)

        recap_points = VGroup(
            Text("1. Parabola: The unique U-shaped curve.", font_size=36, color=BLUE_COLOR),
            MathTex("2. Quadratic Equation: ax^2 + bx + c = 0", font_size=36, color=GOLD_COLOR),
            Text("3. 'a' cannot be zero (a \\neq 0).", font_size=36, color=RED_COLOR),
            Text("4. Used to model curves, predict, and optimize.", font_size=36, color=WHITE)
        ).arrange(DOWN, buff=0.7, align_to_edge=LEFT).next_to(recap_title, DOWN, buff=1)

        self.play(LaggedStart(*[FadeIn(mob, shift=UP) for mob in recap_points], lag_ratio=0.3), run_time=2)
        self.wait(3)
        self.play(FadeOut(recap_points, shift=DOWN), FadeOut(recap_title, shift=UP), run_time=1)
        self.wait(1)