from manim import *

# Custom colors for 3Blue1Brown feel
ACCENT_BLUE = BLUE_B
ACCENT_GOLD = GOLD_C
DARK_GREY = "#202020" # A very dark grey, almost black
LIGHT_GREY = "#AAAAAA"
RED_ACCENT = RED_C

class QuadraticIntro(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = DARK_GREY

        # --- Beat 1: Visual Hook - Projectile Motion (Intuition) ---
        title = Text("Introduction to Quadratic Equations", font_size=50, color=ACCENT_GOLD)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7), run_time=1)

        intro_text = Text("Modeling curves in the real world.", font_size=36, color=LIGHT_GREY).next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(intro_text, shift=UP))

        axes_hook = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 5, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": LIGHT_GREY, "include_numbers": False},
        ).to_edge(DOWN).shift(LEFT*2)
        
        x_label_hook = Text("Time / Distance", font_size=24, color=LIGHT_GREY).next_to(axes_hook.x_axis, DOWN)
        y_label_hook = Text("Height", font_size=24, color=LIGHT_GREY).next_to(axes_hook.y_axis, LEFT)

        curve_func = lambda x: -0.5 * x**2 + 4 * x 
        graph_hook = axes_hook.plot(curve_func, x_range=[0, 8], color=ACCENT_BLUE)

        projectile_dot = Dot(point=axes_hook.coords_to_point(0, 0), color=ACCENT_GOLD, radius=0.15)
        
        self.play(
            LaggedStart(
                Create(axes_hook),
                Write(x_label_hook),
                Write(y_label_hook),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.play(Create(graph_hook), FadeIn(projectile_dot, shift=UP), run_time=1.5)
        
        self.play(
            MoveAlongPath(projectile_dot, graph_hook),
            run_time=4,
            rate_func=linear
        )
        self.wait(0.5)

        self.play(
            FadeOut(projectile_dot),
            FadeOut(graph_hook),
            FadeOut(axes_hook),
            FadeOut(x_label_hook),
            FadeOut(y_label_hook),
            FadeOut(intro_text),
            run_time=1.5
        )

        # --- Beat 2: What is a Parabola? (Shape & Name) ---
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-2, 8, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": LIGHT_GREY},
            background_line_style={"stroke_opacity": 0.4, "stroke_color": LIGHT_GREY}
        )
        self.play(Create(plane), run_time=1.5)

        parabola_func = lambda x: 0.5 * x**2 - 1
        parabola_graph = plane.plot(parabola_func, color=ACCENT_BLUE)
        
        self.play(Create(parabola_graph), run_time=1.5)

        parabola_text = Text("This shape is a PARABOLA.", font_size=40, color=ACCENT_GOLD).next_to(plane, UP, buff=0.7)
        quadratic_intro_text = Text("It's the graph of a QUADRATIC equation.", font_size=36, color=LIGHT_GREY).next_to(parabola_text, DOWN)
        
        self.play(Write(parabola_text), run_time=1.5)
        self.play(Write(quadratic_intro_text), run_time=2)
        self.wait(1)

        # --- Beat 3: The x^2 Term (Core concept) ---
        self.play(
            FadeOut(parabola_text),
            quadratic_intro_text.animate.next_to(title, DOWN, buff=0.7),
            plane.animate.to_edge(LEFT, buff=0.5).scale(0.7),
            parabola_graph.animate.scale(0.7).move_to(plane.get_center()), # Scale and reposition with the plane
            run_time=1.5
        )

        key_term_text = Text("The Key: an 'x squared' term.", font_size=36, color=ACCENT_GOLD).next_to(title, DOWN, buff=0.7).shift(RIGHT*2)
        self.play(ReplacementTransform(quadratic_intro_text, key_term_text), run_time=1)

        # Manually construct y = x^2 with Text
        y_label_eq = Text("y", color=WHITE, font_size=40)
        equals_label = Text("=", color=WHITE, font_size=40)
        x_base_eq = Text("x", color=ACCENT_BLUE, font_size=40)
        exponent_2_eq = Text("2", color=ACCENT_BLUE, font_size=20)
        exponent_2_eq.align_to(x_base_eq, UR).shift(LEFT * 0.15 + DOWN * 0.05) # Fine tune position
        x_squared_term = VGroup(x_base_eq, exponent_2_eq)
        
        x_squared_group = VGroup(y_label_eq, equals_label, x_squared_term)
        x_squared_group.arrange(RIGHT, buff=0.1)
        x_squared_group.next_to(key_term_text, DOWN, buff=1.0).shift(LEFT*0.5)
        
        # Show points for y=x^2
        points_to_show = [(-2,4), (-1,1), (0,0), (1,1), (2,4)]
        dots = VGroup()
        for x_val, y_val in points_to_show:
            dot = Dot(point=plane.coords_to_point(x_val, y_val), color=ACCENT_GOLD, radius=0.1)
            dots.add(dot)

        self.play(FadeIn(x_squared_group, shift=LEFT), run_time=1)
        self.play(FadeIn(dots, scale=0.5), run_time=1)
        
        # Transform graph to y=x^2
        new_parabola_func = lambda x: x**2
        new_parabola_graph = plane.plot(new_parabola_func, color=ACCENT_BLUE)
        self.play(Transform(parabola_graph, new_parabola_graph), run_time=1.5)
        self.wait(0.5)

        # Show variations: y = 2x^2, y = 0.5x^2, y = -x^2
        variations_text = Text("Changing 'a' in 'ax²' modifies the shape:", font_size=30, color=LIGHT_GREY).next_to(x_squared_group, DOWN, buff=0.5).shift(RIGHT*1)
        self.play(FadeIn(variations_text, shift=UP))

        # ax^2 representation
        ax_base = Text("x", color=WHITE, font_size=40)
        ax_exp = Text("2", color=WHITE, font_size=20)
        ax_exp.align_to(ax_base, UR).shift(LEFT * 0.15 + DOWN * 0.05)
        
        eq_a_x2 = VGroup(
            Text("a", color=RED_ACCENT, font_size=40),
            VGroup(ax_base, ax_exp)
        ).arrange(RIGHT, buff=0.1).next_to(variations_text, DOWN, buff=0.3)
        self.play(FadeIn(eq_a_x2, shift=LEFT))

        # Show a=2
        graph_2x2 = plane.plot(lambda x: 2 * x**2, color=ACCENT_BLUE)
        a_val_2 = Text("a=2", font_size=28, color=RED_ACCENT).next_to(eq_a_x2, DOWN, buff=0.2).align_to(eq_a_x2[0], LEFT)
        self.play(Transform(parabola_graph, graph_2x2), FadeIn(a_val_2), run_time=1)
        self.wait(0.3)

        # Show a=0.5
        graph_0_5x2 = plane.plot(lambda x: 0.5 * x**2, color=ACCENT_BLUE)
        a_val_0_5 = Text("a=0.5", font_size=28, color=RED_ACCENT).next_to(eq_a_x2, DOWN, buff=0.2).align_to(eq_a_x2[0], LEFT)
        self.play(Transform(parabola_graph, graph_0_5x2), ReplacementTransform(a_val_2, a_val_0_5), run_time=1)
        self.wait(0.3)

        # Show a=-1
        graph_neg_x2 = plane.plot(lambda x: -1 * x**2, color=ACCENT_BLUE)
        a_val_neg1 = Text("a=-1", font_size=28, color=RED_ACCENT).next_to(eq_a_x2, DOWN, buff=0.2).align_to(eq_a_x2[0], LEFT)
        self.play(Transform(parabola_graph, graph_neg_x2), ReplacementTransform(a_val_0_5, a_val_neg1), run_time=1)
        self.wait(0.5)

        self.play(
            FadeOut(a_val_neg1),
            FadeOut(eq_a_x2),
            FadeOut(variations_text),
            FadeOut(dots),
            FadeOut(x_squared_group),
            FadeOut(key_term_text),
            FadeOut(parabola_graph),
            FadeOut(plane),
            run_time=2
        )

        # --- Beat 4: Formal Notation - ax^2 + bx + c = 0 ---
        formal_text = Text("Standard Form of a Quadratic Equation:", font_size=38, color=ACCENT_GOLD).next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(formal_text, shift=UP), run_time=1)

        # Manually construct ax^2 + bx + c = 0 with Text
        a_coeff = Text("a", color=RED_ACCENT, font_size=50)
        
        # x^2 term
        x_base_formal = Text("x", color=WHITE, font_size=50)
        exponent_2_formal = Text("2", color=WHITE, font_size=25)
        exponent_2_formal.align_to(x_base_formal, UR).shift(LEFT * 0.15 + DOWN * 0.05) # Fine tune position
        x2_term_formal = VGroup(x_base_formal, exponent_2_formal)

        plus1_op = Text("+", color=WHITE, font_size=50)
        b_coeff = Text("b", color=ACCENT_BLUE, font_size=50)
        x_term = Text("x", color=WHITE, font_size=50)
        
        plus2_op = Text("+", color=WHITE, font_size=50)
        c_coeff = Text("c", color=ACCENT_GOLD, font_size=50)
        
        equals_zero = VGroup(
            Text("=", color=WHITE, font_size=50),
            Text("0", color=WHITE, font_size=50)
        ).arrange(RIGHT, buff=0.1)

        equation_parts = VGroup(
            a_coeff, x2_term_formal, plus1_op, b_coeff, x_term, plus2_op, c_coeff, equals_zero
        ).arrange(RIGHT, buff=0.1).next_to(formal_text, DOWN, buff=1.0)
        
        self.play(LaggedStart(*[FadeIn(part, shift=UP) for part in equation_parts], lag_ratio=0.1), run_time=3)
        self.wait(1)

        # Explain a, b, c
        a_desc = Text("a: controls width & direction", font_size=30, color=RED_ACCENT).next_to(a_coeff, DOWN, buff=0.5).align_to(a_coeff, LEFT)
        b_desc = Text("b: shifts horizontally", font_size=30, color=ACCENT_BLUE).next_to(b_coeff, DOWN, buff=0.5).align_to(b_coeff, LEFT)
        c_desc = Text("c: shifts vertically", font_size=30, color=ACCENT_GOLD).next_to(c_coeff, DOWN, buff=0.5).align_to(c_coeff, LEFT)

        self.play(FadeIn(a_desc, shift=UP), run_time=1)
        self.play(FadeIn(b_desc, shift=UP), run_time=1)
        self.play(FadeIn(c_desc, shift=UP), run_time=1)
        self.wait(1)

        self.play(
            FadeOut(a_desc),
            FadeOut(b_desc),
            FadeOut(c_desc),
            FadeOut(formal_text),
            run_time=1.5
        )

        # --- Beat 5: Solving Quadratic Equations (Meaning) ---
        solving_text = Text("What does it mean to 'solve'?", font_size=38, color=ACCENT_GOLD).next_to(title, DOWN, buff=0.7)
        self.play(ReplacementTransform(title, solving_text), run_time=1) # Transform title to new text

        equation_for_solving = equation_parts.copy().scale(0.8).next_to(solving_text, DOWN, buff=0.7).to_edge(LEFT, buff=0.5)
        self.play(Transform(equation_parts, equation_for_solving), run_time=1)
        
        # Re-introduce plane and a parabola
        plane_small = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": LIGHT_GREY},
            background_line_style={"stroke_opacity": 0.4, "stroke_color": LIGHT_GREY}
        ).next_to(equation_for_solving, RIGHT, buff=1.0).shift(UP*0.5)
        
        solving_parabola_func = lambda x: x**2 - 2*x - 1
        solving_parabola_graph = plane_small.plot(solving_parabola_func, color=ACCENT_BLUE)

        self.play(Create(plane_small), Create(solving_parabola_graph), run_time=2)

        x_axis_label = Text("x-axis (where y=0)", font_size=28, color=LIGHT_GREY).next_to(plane_small.x_axis, DOWN, buff=0.3)
        self.play(Write(x_axis_label), run_time=1)

        find_x_text = Text("Find x-values where y=0.", font_size=34, color=WHITE).next_to(equation_for_solving, DOWN, buff=0.7).align_to(equation_for_solving, LEFT)
        self.play(Write(find_x_text), run_time=1)

        intercept_1 = Dot(point=plane_small.coords_to_point(-0.414, 0), color=ACCENT_GOLD, radius=0.15)
        intercept_2 = Dot(point=plane_small.coords_to_point(2.414, 0), color=ACCENT_GOLD, radius=0.15)
        
        self.play(
            Indicate(plane_small.x_axis, scale_factor=1.1, color=ACCENT_GOLD),
            Create(intercept_1),
            Create(intercept_2),
            run_time=2
        )
        self.wait(1.5)

        self.play(
            FadeOut(equation_parts),
            FadeOut(solving_text),
            FadeOut(plane_small),
            FadeOut(solving_parabola_graph),
            FadeOut(x_axis_label),
            FadeOut(find_x_text),
            FadeOut(intercept_1),
            FadeOut(intercept_2),
            run_time=2
        )

        # --- Recap Card ---
        recap_title = Text("Recap: Quadratic Equations", font_size=50, color=ACCENT_GOLD).to_edge(UP, buff=1.0)
        self.play(FadeIn(recap_title, shift=UP), run_time=1)

        bullet1 = Text("1. Create PARABOLAS (U-shapes).", font_size=36, color=LIGHT_GREY).next_to(recap_title, DOWN, buff=0.8).align_to(recap_title, LEFT)
        
        # For bullet 2, assemble it with custom x^2
        bullet2_x_base = Text("x", font_size=36, color=LIGHT_GREY)
        bullet2_x_exp = Text("2", font_size=20, color=LIGHT_GREY)
        bullet2_x_exp.align_to(bullet2_x_base, UR).shift(LEFT * 0.15 + DOWN * 0.05)
        
        bullet2 = VGroup(
            Text("2. Always contain an '", font_size=36, color=LIGHT_GREY),
            VGroup(bullet2_x_base, bullet2_x_exp),
            Text("' term.", font_size=36, color=LIGHT_GREY)
        ).arrange(RIGHT, buff=0.02)
        bullet2.next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)

        # For bullet 3, assemble it with custom x^2
        bullet3_x_base = Text("x", font_size=36, color=LIGHT_GREY)
        bullet3_x_exp = Text("2", font_size=20, color=LIGHT_GREY)
        bullet3_x_exp.align_to(bullet3_x_base, UR).shift(LEFT * 0.15 + DOWN * 0.05)

        bullet3 = VGroup(
            Text("3. Standard form: ax", font_size=36, color=LIGHT_GREY),
            VGroup(bullet3_x_base, bullet3_x_exp),
            Text(" + bx + c = 0.", font_size=36, color=LIGHT_GREY)
        ).arrange(RIGHT, buff=0.02)
        bullet3.next_to(bullet2, DOWN, buff=0.5).align_to(bullet2, LEFT)
        
        bullet4 = Text("4. Solving means finding x-intercepts (where y=0).", font_size=36, color=LIGHT_GREY).next_to(bullet3, DOWN, buff=0.5).align_to(bullet3, LEFT)
        
        recap_bullets = VGroup(bullet1, bullet2, bullet3, bullet4)
        
        self.play(LaggedStart(*[FadeIn(bullet, shift=LEFT) for bullet in recap_bullets], lag_ratio=0.3), run_time=3)
        self.wait(3)

        self.play(FadeOut(recap_title, shift=UP), FadeOut(recap_bullets, shift=DOWN), run_time=1.5)
        self.wait(1)