from manim import *

class UnderstandingQuadraticStructure(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        self.camera.background_color = BLACK # Ensure scene background is black
        BLUE_ACCENT = BLUE_A
        GOLD_ACCENT = GOLD_A
        RED_ACCENT = RED_D # For emphasizing flips (negative 'a')
        
        # --- Beat 1: The Visual Hook & Introduction ---
        title = Text("Understanding Quadratic Equations' Structure", font_size=48, color=WHITE)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7))

        # Visual hook: A point drawing a parabola, suggesting motion/path
        path_arc = FunctionGraph(lambda x: 0.5 * x**2 - 1, x_range=[-3, 3], color=BLUE_ACCENT)
        dot = Dot(color=GOLD_ACCENT).move_to(path_arc.points[0])
        
        intro_text1 = Text("This elegant curve appears everywhere...", font_size=32, color=WHITE).next_to(path_arc, DOWN, buff=1)
        intro_text2 = Text("...from the flight of a bird to optimal enzyme activity.", font_size=32, color=WHITE).next_to(intro_text1, DOWN)
        
        self.play(Create(path_arc), run_time=1.5, rate_func=linear)
        self.add(dot)
        self.play(MoveAlongPath(dot, path_arc), run_time=2, rate_func=linear)
        self.wait(0.5)
        self.play(Write(intro_text1), run_time=1.5)
        self.play(Write(intro_text2), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(intro_text1, intro_text2, dot, path_arc))
        
        # --- Beat 2: The Core: x² and 'a' ---
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 8, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": GRAY, "stroke_width": 1},
            tips=False
        ).add_coordinates()
        
        # Axis labels (biological context)
        x_label = axes.get_x_axis_label(MathTex(r"\text{Input (e.g., Time, Temp.)}").scale(0.7), edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label(MathTex(r"\text{Output (e.g., Pop., Rate)}").scale(0.7).rotate(90 * DEGREES), edge=LEFT, direction=LEFT)
        axes_labels = VGroup(x_label, y_label)

        self.play(Create(axes), Create(axes_labels), FadeOut(title))
        self.wait(0.5)

        # Initial equation: y = x^2
        eq_x2 = MathTex(r"y = x^2", color=WHITE).to_corner(UL)
        eq_x2.set_color_by_tex("x^2", BLUE_ACCENT)
        self.play(Write(eq_x2))

        graph_x2 = axes.get_graph(lambda x: x**2, color=BLUE_ACCENT, x_range=[-3.5, 3.5])
        self.play(Create(graph_x2))
        self.wait(1)

        # Introduce 'a'
        a_tracker = ValueTracker(1)
        
        # Graph always depends on a_tracker (and later b_tracker, c_tracker)
        graph_ax2 = always_redraw(lambda: axes.get_graph(lambda x: a_tracker.get_value() * x**2, color=BLUE_ACCENT, x_range=[-3.5, 3.5]))
        self.add(graph_ax2) # Add the dynamically updated graph
        self.remove(graph_x2) # Remove static graph_x2

        eq_ax2 = MathTex(r"y = ax^2", color=WHITE).to_corner(UL)
        eq_ax2.set_color_by_tex("a", GOLD_ACCENT)
        eq_ax2.set_color_by_tex("x^2", BLUE_ACCENT)
        
        self.play(ReplacementTransform(eq_x2, eq_ax2)) # Transform equation

        a_expl_label = Text("'a': shape, stretch, flip", font_size=28, color=GOLD_ACCENT).next_to(eq_ax2, DOWN, buff=0.5).align_to(eq_ax2, LEFT)
        self.play(Write(a_expl_label))
        
        # Animate 'a' changes
        self.play(a_tracker.animate.set_value(2), run_time=1.5, rate_func=smooth)
        self.play(a_tracker.animate.set_value(0.5), run_time=1.5, rate_func=smooth)
        self.play(a_tracker.animate.set_value(-1), run_time=2, rate_func=smooth, 
                  eq_ax2.animate.set_color_by_tex("a", RED_ACCENT)) # Change 'a' color in text
        self.play(a_tracker.animate.set_value(1), run_time=2, rate_func=smooth,
                  eq_ax2.animate.set_color_by_tex("a", GOLD_ACCENT)) # Back to gold
        self.wait(1)
        self.play(FadeOut(a_expl_label))


        # --- Beat 3: Adding Complexity (Shifting Horizontally: bx) ---
        b_tracker = ValueTracker(0)
        
        # Graph now depends on 'a' and 'b'
        graph_ax2_bx = always_redraw(lambda: axes.get_graph(lambda x: a_tracker.get_value() * x**2 + b_tracker.get_value() * x, color=BLUE_ACCENT, x_range=[-3.5, 3.5]))
        self.add(graph_ax2_bx) 
        self.remove(graph_ax2) # Remove previous graph_ax2

        eq_ax2_bx = MathTex(r"y = ax^2 + bx", color=WHITE).to_corner(UL)
        eq_ax2_bx.set_color_by_tex("a", GOLD_ACCENT)
        eq_ax2_bx.set_color_by_tex("x^2", BLUE_ACCENT)
        eq_ax2_bx.set_color_by_tex("b", GOLD_ACCENT)

        self.play(TransformMatchingTex(eq_ax2, eq_ax2_bx))

        b_expl_label = Text("'b': horizontal shift", font_size=28, color=GOLD_ACCENT).next_to(eq_ax2_bx, DOWN, buff=0.5).align_to(eq_ax2_bx, LEFT)
        self.play(Write(b_expl_label))

        # Animate 'b' changes
        self.play(b_tracker.animate.set_value(2), run_time=2)
        self.play(b_tracker.animate.set_value(-2), run_time=2)
        self.play(b_tracker.animate.set_value(0), run_time=2)
        self.wait(1)
        self.play(FadeOut(b_expl_label))


        # --- Beat 4: Shifting Vertically: c ---
        c_tracker = ValueTracker(0)
        
        # Graph now depends on 'a', 'b', and 'c'
        graph_ax2_bx_c = always_redraw(lambda: axes.get_graph(lambda x: a_tracker.get_value() * x**2 + b_tracker.get_value() * x + c_tracker.get_value(), color=BLUE_ACCENT, x_range=[-3.5, 3.5]))
        self.add(graph_ax2_bx_c) 
        self.remove(graph_ax2_bx) # Remove previous graph_ax2_bx

        eq_ax2_bx_c = MathTex(r"y = ax^2 + bx + c", color=WHITE).to_corner(UL)
        eq_ax2_bx_c.set_color_by_tex("a", GOLD_ACCENT)
        eq_ax2_bx_c.set_color_by_tex("x^2", BLUE_ACCENT)
        eq_ax2_bx_c.set_color_by_tex("b", GOLD_ACCENT)
        eq_ax2_bx_c.set_color_by_tex("c", GOLD_ACCENT)

        self.play(TransformMatchingTex(eq_ax2_bx, eq_ax2_bx_c))

        c_expl_label = Text("'c': vertical shift (y-intercept)", font_size=28, color=GOLD_ACCENT).next_to(eq_ax2_bx_c, DOWN, buff=0.5).align_to(eq_ax2_bx_c, LEFT)
        self.play(Write(c_expl_label))

        # Animate 'c' changes
        self.play(c_tracker.animate.set_value(2), run_time=1.5)
        self.play(c_tracker.animate.set_value(-1), run_time=1.5)
        self.play(c_tracker.animate.set_value(0), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(c_expl_label))
        
        self.remove(graph_ax2_bx_c) # Remove the final dynamic graph


        # --- Beat 5: The General Form & Recap ---
        self.play(FadeOut(axes, axes_labels)) # Clear the graph

        final_quad_eq_zero = MathTex(r"ax^2 + bx + c = 0", color=WHITE).scale(1.2).move_to(ORIGIN)
        final_quad_eq_zero.set_color_by_tex("a", GOLD_ACCENT)
        final_quad_eq_zero.set_color_by_tex("x^2", BLUE_ACCENT)
        final_quad_eq_zero.set_color_by_tex("b", GOLD_ACCENT)
        final_quad_eq_zero.set_color_by_tex("c", GOLD_ACCENT)
        
        self.play(ReplacementTransform(eq_ax2_bx_c, final_quad_eq_zero)) # Transform the final 'y=' equation to the '=0' form
        
        general_form_text = Text("This is the general form of a quadratic equation.", font_size=32, color=WHITE).next_to(final_quad_eq_zero, UP, buff=0.8)
        self.play(Write(general_form_text))
        self.wait(1)

        # Highlight coefficients and their roles
        a_role = Text("'a': Shape, Stretch, Flip", font_size=28, color=GOLD_ACCENT).next_to(final_quad_eq_zero, DOWN, buff=0.5).align_to(final_quad_eq_zero.get_part_by_tex("a"), LEFT)
        b_role = Text("'b': Horizontal Shift", font_size=28, color=GOLD_ACCENT).next_to(a_role, DOWN, buff=0.2).align_to(final_quad_eq_zero.get_part_by_tex("b"), LEFT)
        c_role = Text("'c': Vertical Shift (Y-intercept)", font_size=28, color=GOLD_ACCENT).next_to(b_role, DOWN, buff=0.2).align_to(final_quad_eq_zero.get_part_by_tex("c"), LEFT)

        # Arrows to connect roles to coefficients
        arrow_a = Arrow(a_role.get_part_by_tex("a").get_left(), final_quad_eq_zero.get_part_by_tex("a").get_center(), buff=0.1, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1)
        arrow_b = Arrow(b_role.get_part_by_tex("b").get_left(), final_quad_eq_zero.get_part_by_tex("b").get_center(), buff=0.1, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1)
        arrow_c = Arrow(c_role.get_part_by_tex("c").get_left(), final_quad_eq_zero.get_part_by_tex("c").get_center(), buff=0.1, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1)
        
        self.play(FadeOut(general_form_text))
        self.play(
            LaggedStart(
                Write(a_role), Create(arrow_a),
                Write(b_role), Create(arrow_b),
                Write(c_role), Create(arrow_c),
                lag_ratio=0.5, run_time=5
            )
        )
        self.wait(2)

        # --- Recap Card ---
        self.play(FadeOut(final_quad_eq_zero, a_role, b_role, c_role, arrow_a, arrow_b, arrow_c))
        
        recap_box = Rectangle(width=9, height=6, color=BLUE_ACCENT, fill_opacity=0.1).to_center()
        recap_title = Text("Recap: Quadratic Structure", font_size=40, color=GOLD_ACCENT).move_to(recap_box.get_top() + DOWN*0.6)
        
        recap_eq = MathTex(r"ax^2 + bx + c = 0", color=WHITE).scale(1.1).move_to(recap_title.get_bottom() + DOWN*0.6)
        recap_eq.set_color_by_tex("a", GOLD_ACCENT)
        recap_eq.set_color_by_tex("x^2", BLUE_ACCENT)
        recap_eq.set_color_by_tex("b", GOLD_ACCENT)
        recap_eq.set_color_by_tex("c", GOLD_ACCENT)

        recap_a = Text("• 'a': Shape, Stretch, Flip", font_size=28, color=WHITE).next_to(recap_eq, DOWN, buff=0.5).align_to(recap_eq, LEFT)
        recap_b = Text("• 'b': Horizontal Shift", font_size=28, color=WHITE).next_to(recap_a, DOWN, buff=0.2).align_to(recap_a, LEFT)
        recap_c = Text("• 'c': Vertical Shift (Y-intercept)", font_size=28, color=WHITE).next_to(recap_b, DOWN, buff=0.2).align_to(recap_a, LEFT)

        self.play(Create(recap_box), Write(recap_title))
        self.play(Write(recap_eq))
        self.play(LaggedStart(
            Write(recap_a),
            Write(recap_b),
            Write(recap_c),
            lag_ratio=0.3, run_time=3
        ))
        self.wait(3)
        self.play(FadeOut(recap_box, recap_title, recap_eq, recap_a, recap_b, recap_c))