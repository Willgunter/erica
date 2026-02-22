from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_A # Lighter blue for general accents
        GOLD_ACCENT = GOLD_A # Lighter gold for general accents
        BLUE_HIGHLIGHT = BLUE_E # Deeper blue for emphasis
        GOLD_HIGHLIGHT = GOLD_E # Deeper gold for emphasis

        # --- Beat 1: Visual Hook & Introduction (~10s) ---
        # Title
        title = Tex("Quadratic Equations", font_size=72, color=GOLD_ACCENT).to_edge(UP)
        subtitle = Tex("Understanding the Quadratic Formula", font_size=48, color=BLUE_ACCENT).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Parabolic motion visual hook
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-2, 8, 1],
            x_length=10,
            y_length=7,
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"color": GRAY_C}
        ).to_edge(LEFT, buff=0.5).shift(RIGHT*1.5)
        plane.add_coordinates(font_size=20, color=GRAY_A)

        parabola_eq_func = MathTex(
            "f(x) = ax^2 + bx + c",
            font_size=40, color=WHITE
        ).to_edge(UP+RIGHT)

        parabola_motion = plane.get_graph(lambda x: 0.5 * x**2 - x + 1.5, x_range=[-2.5, 4.5], color=GOLD_ACCENT)
        dot_motion = Dot(color=BLUE_HIGHLIGHT).move_to(parabola_motion.points[0])

        motion_text = Tex("Modeling curved motion, areas...", font_size=36, color=BLUE_ACCENT).next_to(parabola_eq_func, DOWN, buff=0.5)

        self.play(Create(plane), Create(parabola_eq_func), Write(motion_text))
        self.play(Create(parabola_motion))
        self.add(dot_motion)
        self.play(MoveAlongPath(dot_motion, parabola_motion), run_time=2.5, rate_func=linear)
        self.play(FadeOut(dot_motion), FadeOut(motion_text))
        self.wait(0.5)

        # Introduce standard form
        std_form_eq = MathTex(
            "ax^2 + bx + c = 0",
            font_size=60, color=WHITE
        ).move_to(parabola_eq_func) 
        
        self.play(TransformMatchingTex(parabola_eq_func, std_form_eq))
        self.wait(1)

        # --- Beat 2: Standard Form and Roots (~10s) ---
        self.play(
            FadeOut(plane), FadeOut(parabola_motion),
            std_form_eq.animate.to_edge(UP)
        )
        
        # Re-create plane centered for better visual
        plane_centered = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 5, 1],
            x_length=10,
            y_length=8,
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"color": GRAY_C}
        ).add_coordinates(font_size=20, color=GRAY_A)
        self.play(Create(plane_centered))

        parabola_example = plane_centered.get_graph(lambda x: x**2 - 2*x - 3, x_range=[-2.5, 4.5], color=GOLD_ACCENT)
        
        # Mark the roots visually
        root1_coords = plane_centered.coords_to_point(-1, 0)
        root2_coords = plane_centered.coords_to_point(3, 0)
        
        root_dot1 = Dot(root1_coords, color=BLUE_HIGHLIGHT, radius=0.1)
        root_dot2 = Dot(root2_coords, color=BLUE_HIGHLIGHT, radius=0.1)
        
        roots_text = Tex("The 'roots' are where the parabola crosses the x-axis.", font_size=36, color=BLUE_ACCENT).next_to(std_form_eq, DOWN, buff=0.8)
        
        self.play(Create(parabola_example), Write(roots_text))
        self.play(Create(root_dot1), Create(root_dot2))
        self.wait(1)

        # Highlight a, b, c
        a_text = MathTex("a", color=GOLD_HIGHLIGHT).next_to(std_form_eq[0][0], UP, buff=0.2)
        b_text = MathTex("b", color=GOLD_HIGHLIGHT).next_to(std_form_eq[0][3], UP, buff=0.2)
        c_text = MathTex("c", color=GOLD_HIGHLIGHT).next_to(std_form_eq[0][6], UP, buff=0.2)
        
        self.play(Write(a_text), Write(b_text), Write(c_text))
        self.wait(1)
        self.play(FadeOut(a_text), FadeOut(b_text), FadeOut(c_text), FadeOut(roots_text))

        # --- Beat 3: The Challenge - Finding Roots Systematically (~8s) ---
        problem_text = Tex("How to find these 'roots' consistently for ANY quadratic equation?", font_size=40, color=BLUE_ACCENT).next_to(std_form_eq, DOWN, buff=1.0)
        
        arrow1 = Arrow(start=problem_text.get_bottom(), end=root_dot1.get_top(), color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.1)
        arrow2 = Arrow(start=problem_text.get_bottom(), end=root_dot2.get_top(), color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.1)

        self.play(Write(problem_text))
        self.play(Create(arrow1), Create(arrow2))
        self.wait(1.5)
        self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(problem_text))

        # --- Beat 4: Introducing the Quadratic Formula (~10s) ---
        solution_text = Tex("The Quadratic Formula provides the solution!", font_size=54, color=GOLD_HIGHLIGHT).next_to(std_form_eq, DOWN, buff=1.0)
        self.play(Write(solution_text))
        self.wait(0.5)

        # Quadratic Formula
        quad_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=72, color=BLUE_HIGHLIGHT
        ).shift(DOWN*1.5)

        self.play(Write(quad_formula))
        self.wait(1.5)

        # Link a, b, c from standard form to the formula
        # Need to be precise with indices for MathTex parts
        a_in_std = std_form_eq[0][0] # 'a' in 'ax^2'
        b_in_std = std_form_eq[0][3] # 'b' in '+ bx'
        c_in_std = std_form_eq[0][6] # 'c' in '+ c'

        a_in_formula1 = quad_formula.get_parts_by_tex("a")[0] # 'a' in '4ac'
        a_in_formula2 = quad_formula.get_parts_by_tex("a")[1] # 'a' in '2a'
        b_in_formula1 = quad_formula.get_parts_by_tex("b")[0] # 'b' in '-b'
        b_in_formula2 = quad_formula.get_parts_by_tex("b")[1] # 'b' in 'b^2'
        c_in_formula = quad_formula.get_parts_by_tex("c")[0] # 'c' in '4ac'

        a_connections = VGroup(
            Line(a_in_std.get_corner(DR), a_in_formula1.get_corner(UL), color=GOLD_ACCENT, stroke_width=2),
            Line(a_in_std.get_corner(DR), a_in_formula2.get_corner(UL), color=GOLD_ACCENT, stroke_width=2)
        )
        b_connections = VGroup(
            Line(b_in_std.get_corner(DR), b_in_formula1.get_corner(UL), color=GOLD_ACCENT, stroke_width=2),
            Line(b_in_std.get_corner(DR), b_in_formula2.get_corner(UL), color=GOLD_ACCENT, stroke_width=2)
        )
        c_connections = Line(c_in_std.get_corner(DR), c_in_formula.get_corner(UL), color=GOLD_ACCENT, stroke_width=2)

        self.play(
            LaggedStart(
                Create(a_connections),
                Create(b_connections),
                Create(c_connections),
                lag_ratio=0.5
            )
        )
        self.wait(2)
        self.play(FadeOut(a_connections), FadeOut(b_connections), FadeOut(c_connections), FadeOut(solution_text))


        # --- Beat 5: Formula in Action (Conceptual) (~10s) ---
        self.play(
            FadeOut(std_form_eq),
            quad_formula.animate.to_edge(UP)
        )

        example_equation = MathTex("x^2 - 2x - 3 = 0", font_size=54, color=GOLD_ACCENT).next_to(quad_formula, DOWN, buff=1.0)
        self.play(Write(example_equation))
        self.wait(0.5)

        # Identify a, b, c for the example
        a_val = MathTex("a=1", color=WHITE).next_to(example_equation, LEFT, buff=1.0)
        b_val = MathTex("b=-2", color=WHITE).next_to(a_val, DOWN)
        c_val = MathTex("c=-3", color=WHITE).next_to(b_val, DOWN)

        self.play(Write(a_val), Write(b_val), Write(c_val))
        self.wait(1)

        substitute_text = Tex("Substitute these values to find the roots...", font_size=36, color=BLUE_ACCENT).next_to(example_equation, DOWN, buff=1.5)
        self.play(Write(substitute_text))
        self.wait(1.5)
        
        # Show roots appear on graph
        self.play(FadeOut(a_val), FadeOut(b_val), FadeOut(c_val), FadeOut(substitute_text), FadeOut(example_equation))

        # Emphasize the roots on the existing parabola
        root1_text = MathTex("x_1 = -1", color=BLUE_HIGHLIGHT).next_to(plane_centered.coords_to_point(-1, 0), DOWN, buff=0.5)
        root2_text = MathTex("x_2 = 3", color=BLUE_HIGHLIGHT).next_to(plane_centered.coords_to_point(3, 0), DOWN, buff=0.5)
        
        self.play(
            root_dot1.animate.set_fill(BLUE_HIGHLIGHT, opacity=1).scale(1.5),
            root_dot2.animate.set_fill(BLUE_HIGHLIGHT, opacity=1).scale(1.5)
        )
        self.play(Write(root1_text), Write(root2_text))
        self.wait(2)
        
        self.play(FadeOut(root1_text), FadeOut(root2_text), FadeOut(root_dot1), FadeOut(root_dot2))


        # --- Beat 6: Recap Card (~8s) ---
        self.play(FadeOut(plane_centered), FadeOut(parabola_example), FadeOut(quad_formula))

        recap_title = Tex("Quadratic Formula Recap", font_size=60, color=GOLD_HIGHLIGHT).to_edge(UP)
        
        recap_std_form = MathTex("ax^2 + bx + c = 0", font_size=50, color=WHITE).shift(UP*1)
        recap_formula = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", font_size=60, color=BLUE_HIGHLIGHT).next_to(recap_std_form, DOWN, buff=1.0)
        
        key_idea = Tex("Used to find the 'roots' (x-intercepts) of any quadratic equation.", font_size=36, color=BLUE_ACCENT).next_to(recap_formula, DOWN, buff=1.0)

        self.play(Write(recap_title))
        self.play(Write(recap_std_form))
        self.play(Write(recap_formula))
        self.play(Write(key_idea))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_std_form, recap_formula, key_idea)))
        self.wait(1)