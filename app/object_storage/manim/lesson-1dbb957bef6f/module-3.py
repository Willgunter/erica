from manim import *

class ParabolicGeometryOfSolutions(Scene):
    def construct(self):
        # 1. Configuration: Colors and general setup
        self.camera.background_color = BLACK
        ACCENT_BLUE = "#5DA0EE"  # A vibrant, slightly softer blue
        ACCENT_GOLD = "#F7C351"  # A rich, warm gold

        # Module Title
        title = Text(
            "Parabolic Geometry of Solutions", 
            font_size=48, 
            color=ACCENT_BLUE,
            weight=BOLD
        ).to_edge(UP, buff=0.7)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Beat 1: The Visual Hook - Parabola and its roots
        # Set up Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": GRAY_D, "stroke_width": 1},
            tips=False
        ).add_coordinates()
        
        x_label = axes.get_x_axis_label("x").set_color(WHITE)
        y_label = axes.get_y_axis_label("y").set_color(WHITE)
        
        self.play(
            Create(axes),
            FadeIn(x_label, y_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Define an initial parabola: y = x^2 - 1
        parabola_func_initial = lambda x: x**2 - 1
        parabola_initial = axes.get_graph(parabola_func_initial, color=ACCENT_BLUE, stroke_width=4)

        # Calculate roots for y = x^2 - 1
        root1_val = -1
        root2_val = 1
        root1_dot = Dot(axes.c2p(root1_val, 0), color=ACCENT_GOLD, radius=0.08)
        root2_dot = Dot(axes.c2p(root2_val, 0), color=ACCENT_GOLD, radius=0.08)

        # Text indicating solutions
        solutions_text = Text(
            "Solutions (x-intercepts)", 
            font_size=28, 
            color=ACCENT_GOLD
        ).next_to(root2_dot, RIGHT, buff=0.5).shift(UP*0.5)
        
        arrow_to_roots = Arrow(solutions_text.get_left(), root2_dot.get_center(), buff=0.1, color=ACCENT_GOLD, max_stroke_width_to_length_ratio=4)

        self.play(
            Create(parabola_initial),
            FadeIn(root1_dot, root2_dot),
            Write(solutions_text),
            GrowArrow(arrow_to_roots),
            run_time=2
        )
        self.wait(1.5)

        # 3. Beat 2: Connecting the Equation to the Graph
        # Fade out initial root indicators and text
        self.play(
            FadeOut(solutions_text, arrow_to_roots, root1_dot, root2_dot),
            parabola_initial.animate.set_color(GRAY), # Dim the parabola briefly
            run_time=1
        )
        self.wait(0.5)

        # Quadratic equation
        quad_eq_tex = MathTex("ax^2 + bx + c = 0", color=ACCENT_GOLD)
        quad_eq_tex.scale(0.8).next_to(title, DOWN, buff=0.8).align_to(title, LEFT)

        # Graph equation
        graph_eq_tex = MathTex("y = ax^2 + bx + c", color=ACCENT_BLUE)
        graph_eq_tex.scale(0.8).move_to(quad_eq_tex)

        # Explanation text
        explanation = Text(
            "When y=0, we find where the graph crosses the x-axis.",
            font_size=24, color=WHITE
        ).next_to(graph_eq_tex, DOWN, buff=0.5).to_edge(LEFT)
        
        # Show equation, then transform to y=f(x) form
        self.play(
            Write(quad_eq_tex),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            ReplacementTransform(quad_eq_tex, graph_eq_tex),
            Write(explanation),
            run_time=2
        )
        self.play(parabola_initial.animate.set_color(ACCENT_BLUE)) # Restore parabola color
        self.wait(2)

        # 4. Beat 3: The Discriminant - Number of Solutions
        self.play(FadeOut(explanation))
        
        # Discriminant formula
        discriminant_formula = MathTex(
            "D = b^2 - 4ac", color=ACCENT_GOLD
        ).scale(0.8).next_to(graph_eq_tex, DOWN, buff=0.8).align_to(graph_eq_tex, LEFT)
        self.play(Write(discriminant_formula))
        self.wait(0.5)

        # Text for discriminant cases
        disc_text_gt_0 = Text("D > 0: Two real solutions", font_size=22, color=WHITE).next_to(discriminant_formula, DOWN, buff=0.4).align_to(discriminant_formula, LEFT)
        disc_text_eq_0 = Text("D = 0: One real solution", font_size=22, color=WHITE).next_to(disc_text_gt_0, DOWN, buff=0.2).align_to(discriminant_formula, LEFT)
        disc_text_lt_0 = Text("D < 0: No real solutions", font_size=22, color=WHITE).next_to(disc_text_eq_0, DOWN, buff=0.2).align_to(discriminant_formula, LEFT)

        # Scenario 1: Two real roots (D > 0)
        # We use the existing parabola_initial (y = x^2 - 1)
        current_parabola = parabola_initial
        root1 = Dot(axes.c2p(-1, 0), color=ACCENT_GOLD, radius=0.08)
        root2 = Dot(axes.c2p(1, 0), color=ACCENT_GOLD, radius=0.08)
        
        self.play(
            FadeIn(root1, root2),
            Write(disc_text_gt_0),
            run_time=1.5
        )
        self.wait(1)

        # Scenario 2: One real root (D = 0) -> y = x^2
        parabola_eq_0_func = lambda x: x**2
        parabola_eq_0 = axes.get_graph(parabola_eq_0_func, color=ACCENT_BLUE, stroke_width=4)
        root_eq_0 = Dot(axes.c2p(0, 0), color=ACCENT_GOLD, radius=0.08)
        
        self.play(
            Transform(current_parabola, parabola_eq_0),
            FadeOut(root1, root2),
            FadeIn(root_eq_0),
            Write(disc_text_eq_0),
            run_time=2
        )
        self.wait(1)

        # Scenario 3: No real roots (D < 0) -> y = x^2 + 1
        parabola_lt_0_func = lambda x: x**2 + 1
        parabola_lt_0 = axes.get_graph(parabola_lt_0_func, color=ACCENT_BLUE, stroke_width=4)

        self.play(
            Transform(current_parabola, parabola_lt_0),
            FadeOut(root_eq_0),
            Write(disc_text_lt_0),
            run_time=2
        )
        self.wait(2)
        
        # Clear discriminant texts and current parabola
        self.play(
            FadeOut(disc_text_gt_0, disc_text_eq_0, disc_text_lt_0, discriminant_formula, graph_eq_tex, current_parabola)
        )

        # 5. Beat 4: Shifting the Parabola (Effect of 'c')
        c_explanation = Text(
            "How changing 'c' shifts the parabola and its roots:",
            font_size=28, color=WHITE
        ).next_to(title, DOWN, buff=0.8).align_to(title, LEFT)

        # Initialize parabola with y = x^2 + c, where c is controlled by a ValueTracker
        c_value_tracker = ValueTracker(2) # Start with c=2 (no roots)
        
        # MathTex for the equation, updating with c's value
        c_eq_tex = MathTex("y = x^2 + {}", "c", color=ACCENT_BLUE)
        c_eq_tex.scale(0.8).next_to(c_explanation, DOWN, buff=0.5).align_to(c_explanation, LEFT)
        
        c_value_tex = MathTex(f"{c_value_tracker.get_value():.1f}", color=ACCENT_GOLD)
        c_value_tex.move_to(c_eq_tex[1]) # Position over 'c'
        
        c_eq_group = VGroup(c_eq_tex[0], c_value_tex)

        def update_parabola_c(mob):
            c_val = c_value_tracker.get_value()
            new_parabola_func = lambda x: x**2 + c_val
            new_parabola = axes.get_graph(new_parabola_func, color=ACCENT_BLUE, stroke_width=4)
            mob.become(new_parabola)
            c_value_tex.set_value(c_val) # Update c value in text

        # Initial parabola for c=2
        parabola_c_anim = axes.get_graph(lambda x: x**2 + c_value_tracker.get_value(), color=ACCENT_BLUE, stroke_width=4)
        
        self.play(
            Write(c_explanation),
            Create(parabola_c_anim),
            FadeIn(c_eq_group),
            run_time=1.5
        )
        self.wait(1)

        # Animate c decreasing from 2 to -2
        # Roots will appear/disappear based on the c value
        self.play(c_value_tracker.animate.set_value(0), UpdateFromFunc(parabola_c_anim, update_parabola_c), run_time=3)
        # At c=0, one root
        root_c_0 = Dot(axes.c2p(0, 0), color=ACCENT_GOLD, radius=0.08)
        self.play(FadeIn(root_c_0), run_time=0.5)
        self.wait(1)

        self.play(c_value_tracker.animate.set_value(-2), UpdateFromFunc(parabola_c_anim, update_parabola_c), FadeOut(root_c_0), run_time=3)
        # At c=-2, two roots
        root_c_neg2_1 = Dot(axes.c2p(-np.sqrt(2), 0), color=ACCENT_GOLD, radius=0.08)
        root_c_neg2_2 = Dot(axes.c2p(np.sqrt(2), 0), color=ACCENT_GOLD, radius=0.08)
        self.play(FadeIn(root_c_neg2_1, root_c_neg2_2), run_time=0.5)
        self.wait(1.5)

        # 6. Beat 5: Recap Card
        self.play(
            FadeOut(parabola_c_anim, c_explanation, c_eq_group, root_c_neg2_1, root_c_neg2_2,
                    axes, x_label, y_label, title)
        )

        recap_title = Text("Recap: Parabolic Geometry", font_size=40, color=ACCENT_BLUE).to_edge(UP, buff=0.8)
        
        recap_point1 = BulletedList(
            "Quadratic solutions are X-intercepts (where y=0).",
            font_size=28, color=WHITE
        ).next_to(recap_title, DOWN, buff=0.6).align_to(recap_title, LEFT)

        recap_point2 = BulletedList(
            "The Discriminant (D=b²-4ac) determines the # of real solutions.",
            font_size=28, color=WHITE
        ).next_to(recap_point1, DOWN, buff=0.3).align_to(recap_title, LEFT)
        
        recap_point3 = BulletedList(
            "Visualize solution changes by shifting the parabola!",
            font_size=28, color=WHITE
        ).next_to(recap_point2, DOWN, buff=0.3).align_to(recap_title, LEFT)
        
        self.play(Write(recap_title))
        self.play(LaggedStart(
            *[Write(item) for item in recap_point1],
            run_time=1.5, lag_ratio=0.5
        ))
        self.play(LaggedStart(
            *[Write(item) for item in recap_point2],
            run_time=1.5, lag_ratio=0.5
        ))
        self.play(LaggedStart(
            *[Write(item) for item in recap_point3],
            run_time=1.5, lag_ratio=0.5
        ))
        self.wait(3)

        self.play(FadeOut(recap_title, recap_point1, recap_point2, recap_point3))
        self.wait(1)