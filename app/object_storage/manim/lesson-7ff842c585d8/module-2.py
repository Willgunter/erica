from manim import *

class QuadraticSolutions(Scene):
    def construct(self):
        # 1. Configuration: Clean dark background with high-contrast accents
        self.camera.background_color = BLACK

        # Setup Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY_A, "include_numbers": True},
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # Initial animation of axes appearing
        self.play(Create(axes), Create(axes_labels), run_time=1.5)
        self.wait(0.5)

        # ValueTrackers for a, b, c parameters
        a_val = ValueTracker(1)
        b_val = ValueTracker(0)
        c_val = ValueTracker(0)

        # Helper function to get the parabola Mobject
        def get_parabola(a, b, c):
            return axes.get_graph(
                lambda x: a * x**2 + b * x + c, 
                color=BLUE_E, 
                x_range=[-3.5, 3.5]
            )

        # Always redraw the parabola based on tracker values
        parabola = always_redraw(lambda: get_parabola(
            a_val.get_value(), 
            b_val.get_value(), 
            c_val.get_value()
        ))
        
        # Helper to update roots dynamically
        def update_roots(parabola_mobject, a_tracker, b_tracker, c_tracker):
            a_cur = a_tracker.get_value()
            b_cur = b_tracker.get_value()
            c_cur = c_tracker.get_value()
            
            discriminant = b_cur**2 - 4 * a_cur * c_cur
            new_roots = VGroup()
            
            # Avoid division by zero if a_cur is very close to zero, or handle as linear
            if abs(a_cur) < 1e-9: # If 'a' is essentially 0, it's a linear equation
                if abs(b_cur) > 1e-9: # If 'b' is not 0, there's one root
                    x_root = -c_cur / b_cur
                    new_roots.add(Dot(axes.c2p(x_root, 0), color=GOLD, radius=0.12))
            elif discriminant >= 0:
                x1 = (-b_cur + discriminant**0.5) / (2 * a_cur)
                x2 = (-b_cur - discriminant**0.5) / (2 * a_cur)
                new_roots.add(Dot(axes.c2p(x1, 0), color=GOLD, radius=0.12))
                if discriminant > 1e-9: # If discriminant is strictly positive, two distinct roots
                    new_roots.add(Dot(axes.c2p(x2, 0), color=GOLD, radius=0.12))
            return new_roots

        dynamic_roots = always_redraw(lambda: update_roots(parabola, a_val, b_val, c_val))

        # Beat 1: Strong Visual Hook - The `y = x^2` parabola emerges
        equation_tex_initial = MathTex("y = x^2", color=BLUE_E).to_corner(UP_RIGHT).scale(0.9)
        
        self.play(Create(parabola), Write(equation_tex_initial), run_time=2.5)
        self.wait(1)

        # Beat 2: The Core Question - Where is y=0? (x-intercepts)
        x_axis_label = MathTex("y = 0 \\text{ (x-axis)}", color=GOLD).next_to(axes.x_axis, DOWN, buff=0.2)
        question_tex = MathTex("y = 0 \\implies x = ?", color=WHITE).to_corner(UP_LEFT).scale(0.8)

        self.add(dynamic_roots) # Add dynamic roots here for the first time
        self.play(
            FadeIn(x_axis_label),
            Write(question_tex),
            run_time=2
        )
        self.wait(1)

        # Beat 3: Parameter 'c' - Vertical Shift (y = x^2 + c)
        equation_c_tex = MathTex("y = x^2 + c", color=BLUE_E).to_corner(UP_RIGHT).scale(0.9)
        c_label = MathTex(r"c = {{%.2f}}" % c_val.get_value(), color=GOLD).next_to(equation_c_tex, DOWN)
        c_label.add_updater(lambda m: m.become(MathTex(r"c = {{%.2f}}" % c_val.get_value(), color=GOLD).next_to(equation_c_tex, DOWN)))
        
        self.play(
            ReplacementTransform(equation_tex_initial, equation_c_tex),
            FadeOut(question_tex),
            FadeIn(c_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Animate c changing, showing roots appearing/disappearing
        self.play(c_val.animate.set_value(-2), run_time=3) # Two roots
        self.play(c_val.animate.set_value(2), run_time=3)  # Zero roots
        self.play(c_val.animate.set_value(-0.5), run_time=2) # Settle at 2 roots
        self.wait(1)

        # Beat 4: Parameter 'b' - Horizontal Shift / Vertex Movement (y = x^2 + bx + c)
        fixed_c_val = c_val.get_value() 
        equation_b_tex = MathTex("y = x^2 + bx + ", f"{fixed_c_val:.2f}", color=BLUE_E).to_corner(UP_RIGHT).scale(0.9)
        b_label = MathTex(r"b = {{%.2f}}" % b_val.get_value(), color=GOLD).next_to(equation_b_tex, DOWN)
        b_label.add_updater(lambda m: m.become(MathTex(r"b = {{%.2f}}" % b_val.get_value(), color=GOLD).next_to(equation_b_tex, DOWN)))
        
        self.play(
            ReplacementTransform(equation_c_tex, equation_b_tex),
            Transform(c_label, b_label), 
            run_time=1.5
        )
        self.add(b_label) # Add b_label as updater before removing old
        self.remove(c_label)
        self.wait(0.5)

        # Animate b changing
        self.play(b_val.animate.set_value(3), run_time=3)
        self.play(b_val.animate.set_value(-3), run_time=3)
        self.play(b_val.animate.set_value(1), run_time=2) # Settle
        self.wait(1)

        # Beat 5: Parameter 'a' - Stretch/Compression/Reflection (y = ax^2 + bx + c)
        fixed_b_val = b_val.get_value() 
        equation_a_tex = MathTex("y = ax^2 + ", f"{fixed_b_val:.2f}", "x + ", f"{fixed_c_val:.2f}", color=BLUE_E).to_corner(UP_RIGHT).scale(0.9)
        a_label = MathTex(r"a = {{%.2f}}" % a_val.get_value(), color=GOLD).next_to(equation_a_tex, DOWN)
        a_label.add_updater(lambda m: m.become(MathTex(r"a = {{%.2f}}" % a_val.get_value(), color=GOLD).next_to(equation_a_tex, DOWN)))
        
        self.play(
            ReplacementTransform(equation_b_tex, equation_a_tex),
            Transform(b_label, a_label), 
            run_time=1.5
        )
        self.add(a_label) # Add a_label as updater before removing old
        self.remove(b_label)
        self.wait(0.5)

        # Animate a changing
        self.play(a_val.animate.set_value(0.5), run_time=2) # Wider
        self.play(a_val.animate.set_value(2), run_time=2)   # Narrower
        self.play(a_val.animate.set_value(-1), run_time=3)  # Reflects, opens downwards
        self.play(a_val.animate.set_value(1), run_time=2)   # Back to initial 'a'
        self.wait(1)

        # Beat 6: Recap Card
        self.play(
            FadeOut(parabola, equation_a_tex, a_label, dynamic_roots, x_axis_label, axes_labels),
            axes.animate.scale(0.8).shift(2*LEFT + 1.5*DOWN), # Keep axes for context, but smaller
            run_time=2
        )
        
        recap_title = Text("Recap: Visualizing Quadratic Solutions", color=BLUE_E).to_edge(UP).scale(0.9)
        eq_summary = MathTex("y = ax^2 + bx + c", color=WHITE).next_to(recap_title, DOWN, buff=0.5)
        
        a_effect = Text(" 'a' : Stretch / Compression, Reflection", font_size=36, color=WHITE).shift(UP*0.5)
        b_effect = Text(" 'b' : Horizontal Vertex Shift", font_size=36, color=WHITE)
        c_effect = Text(" 'c' : Vertical Parabola Shift", font_size=36, color=WHITE).shift(DOWN*0.5)

        summary_points = VGroup(a_effect, b_effect, c_effect).arrange(DOWN, buff=0.7)
        summary_points.next_to(eq_summary, DOWN, buff=0.8)

        self.play(
            FadeIn(recap_title),
            Write(eq_summary),
            LaggedStart(
                FadeIn(a_effect, shift=UP),
                FadeIn(b_effect, shift=UP),
                FadeIn(c_effect, shift=UP),
                lag_ratio=0.3,
                run_time=3
            )
        )
        self.wait(4)

        self.play(FadeOut(recap_title, eq_summary, summary_points, axes))
        self.wait(1)