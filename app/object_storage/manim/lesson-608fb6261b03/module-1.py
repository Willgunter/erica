from manim import *

class QuadraticEquationFundamentals(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#1a1a1a" # Dark background
        blue_color = "#5DADE2" # Light blue
        gold_color = "#F4D03F" # Gold
        white_color = "#F8F8F8" # Off-white for general text

        # Helper to create equation parts (due to no Tex/MathTex constraint)
        # Handles parts like: "y", "=", "2", ("x", "2"), "+", "c"
        def create_text_equation_group(parts_list, color=white_color, scale=0.9):
            mobjects = []
            for part in parts_list:
                if isinstance(part, tuple) and len(part) == 2 and part[1] == "2": # Special handling for ("x", "2")
                    base = Text(part[0], color=color).scale(scale)
                    exponent = Text("2", font_size=30, color=color).next_to(base, UP + RIGHT, buff=0.05).scale(scale * 0.7)
                    mobjects.append(VGroup(base, exponent))
                else: # Regular text or numbers
                    mobjects.append(Text(str(part), color=color).scale(scale))
            
            group = VGroup(*mobjects).arrange(RIGHT, buff=0.1)
            return group

        # Helper for ax^2 + bx + c form explicitly
        # This one handles display logic for 1x^2, -1x^2, +0, etc.
        def get_general_form_equation(a_val, b_val, c_val, color=white_color, scale=0.9):
            parts = []
            parts.append("y")
            parts.append("=")

            # Handle 'a' part
            if a_val == -1:
                parts.append("-")
            elif a_val != 1 and a_val != 0:
                parts.append(str(a_val))
            
            if a_val != 0:
                parts.append(("x", "2"))

            # Handle 'b' part
            if b_val > 0:
                if a_val != 0: parts.append("+")
                if b_val != 1: parts.append(str(b_val))
                parts.append("x")
            elif b_val < 0:
                parts.append("-")
                if b_val != -1: parts.append(str(abs(b_val)))
                parts.append("x")
            
            # Handle 'c' part
            if c_val > 0:
                if a_val != 0 or b_val != 0: parts.append("+")
                parts.append(str(c_val))
            elif c_val < 0:
                parts.append("-")
                parts.append(str(abs(c_val)))
            
            # If all coefficients are zero, show y = 0
            if not parts or (len(parts) == 2 and parts[0] == "y" and parts[1] == "="):
                return create_text_equation_group(["y", "=", "0"], color=color, scale=scale)

            return create_text_equation_group(parts, color=color, scale=scale)


        # --- Beat 1: The Hook & Introduction (Intuition) ---
        title = Text("Quadratic Equations", color=gold_color).scale(1.3).to_edge(UP)
        
        hook_text = Text(
            "Modeling curved motion...", 
            color=blue_color
        ).scale(0.8)
        
        # Simulate a projectile path
        path_function = lambda t: np.array([t, -0.5 * t**2 + 2, 0])
        path = ParametricFunction(path_function, t_range=[-2.5, 2.5], color=gold_color, stroke_width=6)
        path.move_to(ORIGIN).shift(DOWN*0.5 + LEFT*0.5)

        self.play(Write(title), run_time=1.5)
        self.play(Create(path), Write(hook_text.next_to(path, DOWN, buff=0.5)), run_time=2)
        self.wait(1)

        intro_text = Text(
            "Describe curves like this parabola.", 
            color=white_color
        ).scale(0.7).next_to(hook_text, DOWN)
        self.play(Write(intro_text), FadeOut(hook_text), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(path), FadeOut(intro_text), run_time=1)
        
        # --- Beat 2: Visualizing y = x^2 ---
        number_plane = NumberPlane(
            x_range=[-5, 5, 1], 
            y_range=[-5, 5, 1], 
            x_length=10, 
            y_length=10,
            axis_config={"color": "#606060"}, # Darker grey for axes
            background_line_style={"stroke_color": "#404040", "stroke_width": 1, "stroke_opacity": 0.6}
        ).shift(DOWN * 0.5)

        x_label = Text("x", color=white_color).next_to(number_plane.x_axis, RIGHT, buff=0.1)
        y_label = Text("y", color=white_color).next_to(number_plane.y_axis, UP, buff=0.1)

        self.play(Create(number_plane), Write(x_label), Write(y_label), run_time=2)

        # Plot y = x^2
        def func_x_squared(x):
            return x**2
        
        parabola_curve = number_plane.get_graph(func_x_squared, color=blue_color, stroke_width=5)
        
        # Equation y = x^2 without Tex
        eq_y_x_squared = create_text_equation_group(["y", "=", ("x", "2")], color=blue_color)
        eq_y_x_squared.to_edge(UP).shift(RIGHT*3)
        
        parabola_text = Text("This is a parabola.", color=white_color).scale(0.8).next_to(number_plane, UP, buff=0.5).shift(LEFT*2)

        self.play(
            Create(parabola_curve),
            Write(parabola_text),
            Write(eq_y_x_squared),
            run_time=2
        )
        self.wait(1.5)

        # Show points on the curve (x, y)
        points = []
        labels = []
        x_vals = [-2, -1, 0, 1, 2]
        for x_val in x_vals:
            y_val = func_x_squared(x_val)
            point_dot = Dot(number_plane.coords_to_point(x_val, y_val), color=gold_color)
            label_text = Text(f"({x_val}, {y_val})", color=gold_color).scale(0.6).next_to(point_dot, UR, buff=0.1)
            points.append(point_dot)
            labels.append(label_text)

        self.play(LaggedStart(*[FadeIn(p) for p in points], lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.2), run_time=1.5)
        self.wait(1)
        
        self.play(
            *[FadeOut(m) for m in points + labels + [parabola_text]],
            FadeOut(eq_y_x_squared),
            run_time=1
        )

        # --- Beat 3: Introducing a and c (Transformations) ---
        general_form_label_text = Text("General form: y = ax² + bx + c", color=gold_color).scale(0.9)
        general_form_label_text.next_to(title, DOWN, buff=0.5).shift(LEFT*0.5)

        # Re-introduce current curve y=x^2 (a=1, b=0, c=0)
        current_a = 1
        current_b = 0
        current_c = 0
        
        current_equation_text = get_general_form_equation(current_a, current_b, current_c, color=blue_color)
        current_equation_text.to_edge(UP).shift(RIGHT*3)
        
        self.play(Create(current_equation_text), run_time=0.5)

        # Effect of 'a'
        a_effect_text = Text("Coefficient 'a' changes width & direction:", color=white_color).scale(0.7).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(a_effect_text))
        self.wait(0.5)

        # Animate 'a'
        a_values = [2, 0.5, -1] # Keep b=0, c=0
        for a_val in a_values:
            new_curve = number_plane.get_graph(lambda x: a_val * x**2 + current_b * x + current_c, color=blue_color, stroke_width=5)
            new_equation_text = get_general_form_equation(a_val, current_b, current_c, color=blue_color)
            new_equation_text.move_to(current_equation_text.get_center()) # Ensure it replaces at the same spot
            
            self.play(
                Transform(parabola_curve, new_curve),
                ReplacementTransform(current_equation_text, new_equation_text),
                run_time=1.5
            )
            current_equation_text = new_equation_text
            current_a = a_val
            self.wait(0.5)

        # Reset to a=1 for 'c' explanation
        if current_a != 1:
            new_curve = number_plane.get_graph(lambda x: 1 * x**2 + current_b * x + current_c, color=blue_color, stroke_width=5)
            new_equation_text = get_general_form_equation(1, current_b, current_c, color=blue_color)
            new_equation_text.move_to(current_equation_text.get_center())
            self.play(
                Transform(parabola_curve, new_curve),
                ReplacementTransform(current_equation_text, new_equation_text),
                run_time=1.5
            )
            current_equation_text = new_equation_text
            current_a = 1
            self.wait(0.5)

        self.play(FadeOut(a_effect_text))
        c_effect_text = Text("Constant 'c' shifts curve vertically:", color=white_color).scale(0.7).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(c_effect_text))
        self.wait(0.5)

        # Animate 'c'
        c_values = [2, -2] # Keep a=1, b=0
        for c_val in c_values:
            new_curve = number_plane.get_graph(lambda x: current_a * x**2 + current_b * x + c_val, color=blue_color, stroke_width=5)
            new_equation_text = get_general_form_equation(current_a, current_b, c_val, color=blue_color)
            new_equation_text.move_to(current_equation_text.get_center())
            
            self.play(
                Transform(parabola_curve, new_curve),
                ReplacementTransform(current_equation_text, new_equation_text),
                run_time=1.5
            )
            current_equation_text = new_equation_text
            current_c = c_val
            self.wait(0.5)

        self.play(FadeOut(c_effect_text))
        self.wait(1)
        self.play(FadeOut(current_equation_text)) # Hide equation to simplify next beat

        # --- Beat 4: Finding Roots/Zeros ---
        roots_title = Text("Roots (or Zeros): Where y = 0", color=gold_color).scale(0.9)
        roots_title.next_to(title, DOWN, buff=0.5).shift(LEFT*0.5) # Position under the main title
        self.play(ReplacementTransform(title, roots_title)) # Transform main title into roots title

        # Cases for roots
        def get_roots_function_and_curve(a_val, b_val, c_val):
            def func(x):
                return a_val * x**2 + b_val * x + c_val
            return func, number_plane.get_graph(func, color=blue_color, stroke_width=5)

        # Case 1: Two roots (y = x^2 - 1)
        func1, curve1 = get_roots_function_and_curve(1, 0, -1)
        self.play(Transform(parabola_curve, curve1), run_time=1.5)
        
        root_points1 = []
        root_arrows1 = []
        x_intercepts1 = [-1, 1]
        for x_val in x_intercepts1:
            point_coords = number_plane.coords_to_point(x_val, 0)
            root_points1.append(Dot(point_coords, color=gold_color, radius=0.12))
            arrow = Arrow(start=point_coords + UP*0.8, end=point_coords + UP*0.2, buff=0, color=gold_color, tip_length=0.2)
            root_arrows1.append(arrow)
        
        roots_text1 = Text("Two Real Roots", color=white_color).scale(0.7).next_to(number_plane.x_axis, UP, buff=0.8).align_to(number_plane.x_axis, RIGHT).shift(LEFT*1.5)
        self.play(Create(VGroup(*root_points1, *root_arrows1)), Write(roots_text1), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(VGroup(*root_points1, *root_arrows1, roots_text1)), run_time=1)

        # Case 2: One root (y = x^2)
        func2, curve2 = get_roots_function_and_curve(1, 0, 0)
        self.play(Transform(parabola_curve, curve2), run_time=1.5)
        
        point_coords2 = number_plane.coords_to_point(0, 0)
        root_points2 = [Dot(point_coords2, color=gold_color, radius=0.12)]
        root_arrows2 = [Arrow(start=point_coords2 + UP*0.8, end=point_coords2 + UP*0.2, buff=0, color=gold_color, tip_length=0.2)]
        
        roots_text2 = Text("One Real Root (repeated)", color=white_color).scale(0.7).next_to(number_plane.x_axis, UP, buff=0.8).align_to(number_plane.x_axis, RIGHT).shift(LEFT*1.5)
        self.play(Create(VGroup(*root_points2, *root_arrows2)), Write(roots_text2), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(VGroup(*root_points2, *root_arrows2, roots_text2)), run_time=1)

        # Case 3: No real roots (y = x^2 + 1)
        func3, curve3 = get_roots_function_and_curve(1, 0, 1)
        self.play(Transform(parabola_curve, curve3), run_time=1.5)
        
        roots_text3 = Text("No Real Roots", color=white_color).scale(0.7).next_to(number_plane.x_axis, UP, buff=0.8).align_to(number_plane.x_axis, RIGHT).shift(LEFT*1.5)
        self.play(Write(roots_text3), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(roots_text3), run_time=1)

        self.play(FadeOut(parabola_curve), FadeOut(number_plane), FadeOut(x_label), FadeOut(y_label), run_time=1.5)
        self.play(FadeOut(roots_title), run_time=0.5)

        # --- Beat 5: Recap Card ---
        recap_title = Text("Quadratic Equations: Recap", color=gold_color).scale(1.2).to_edge(UP)
        
        bullet1 = Text("• Model curved motion (parabolas)", color=blue_color).scale(0.8)
        
        bullet2_text = Text("• General form:", color=blue_color).scale(0.8)
        # Re-create general form equation string
        bullet2_eq = get_general_form_equation(1, 1, 1, color=white_color).scale(0.9) # Placeholder values to show full form

        bullet3 = Text("• 'a' controls width & direction", color=blue_color).scale(0.8)
        bullet4 = Text("• 'c' controls vertical shift", color=blue_color).scale(0.8)
        bullet5 = Text("• Roots = x-intercepts (where y = 0)", color=blue_color).scale(0.8)

        # Arrange bullet points
        # Position bullet1, then position subsequent bullets relative to the previous ones
        bullet1.move_to(ORIGIN).shift(UP*1.8 + LEFT*2.5) # Initial position
        bullet2_text.next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet2_eq.next_to(bullet2_text, RIGHT, buff=0.1)
        bullet3.next_to(bullet2_text, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet4.next_to(bullet3, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet5.next_to(bullet4, DOWN, buff=0.5).align_to(bullet1, LEFT)

        # Group all recap elements for a single FadeOut
        recap_elements = VGroup(recap_title, bullet1, bullet2_text, bullet2_eq, bullet3, bullet4, bullet5)

        self.play(Write(recap_title), run_time=1)
        self.play(
            LaggedStart(
                Write(bullet1),
                Write(bullet2_text),
                Create(bullet2_eq),
                Write(bullet3),
                Write(bullet4),
                Write(bullet5),
                lag_ratio=0.5,
                run_time=5
            )
        )
        self.wait(3)
        self.play(FadeOut(recap_elements))
        self.wait(1)