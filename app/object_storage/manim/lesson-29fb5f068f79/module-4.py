from manim import *

class QuadraticSolutionsGeometric(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        TEXT_COLOR = WHITE
        BLUE_ACCENT_LIGHT = BLUE_C # Lighter blue for outlines/minor elements
        BLUE_ACCENT_DARK = BLUE_A  # Darker blue for primary elements
        GOLD_ACCENT_LIGHT = GOLD_C # Lighter gold
        GOLD_ACCENT_DARK = GOLD_A  # Darker gold

        # Helper for creating Text with superscript using Unicode
        def get_equation_text(text_str, color=TEXT_COLOR, font_size=40):
            # Replace common power notations with unicode superscripts for cleaner look
            text_str = text_str.replace("x^2", "x²").replace("x^3", "x³").replace("y^2", "y²")
            return Text(text_str, font_size=font_size, color=color)

        # --- Beat 1: The Core Question - Where do they cross? ---
        # Initial title, will transform into equations for continuity
        current_main_text = Text("Geometric Interpretation of Quadratic Solutions", font_size=50, color=GOLD_ACCENT_DARK)
        self.play(Write(current_main_text))
        self.wait(1)
        self.play(current_main_text.animate.to_corner(UL).scale(0.7))

        intro_question = get_equation_text("Where does y = ax² + bx + c cross the x-axis?", color=BLUE_ACCENT_LIGHT)
        intro_question.next_to(current_main_text, DOWN, buff=MED_LARGE_BUFF).align_to(current_main_text, LEFT)
        self.play(Write(intro_question))
        self.wait(1)

        # Set up Axes and a sample Parabola (y = x^2) with a horizontal line (y = c)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": BLUE_ACCENT_LIGHT, "font_size": 24},
            tips=False
        ).shift(DOWN * 0.5)
        
        labels = axes.get_axis_labels(x_label=Text("x", color=BLUE_ACCENT_LIGHT), y_label=Text("y", color=BLUE_ACCENT_LIGHT))

        parabola = axes.get_graph(lambda x: x**2, color=GOLD_ACCENT_DARK)
        line_c = axes.get_horizontal_line(axes.c2p(0, 2), color=BLUE_ACCENT_DARK, length=axes.x_length)
        c_label = get_equation_text("y = c", color=BLUE_ACCENT_DARK, font_size=30).next_to(line_c, RIGHT, buff=SMALL_BUFF)

        self.play(
            FadeOut(intro_question),
            Create(axes),
            Write(labels),
            run_time=1.5
        )
        self.play(Create(parabola), run_time=1.5)
        self.play(Create(line_c), Write(c_label))
        self.wait(0.5)

        # Show intersection points and their projection onto the x-axis (roots)
        intersection_points = VGroup()
        x_root_val = np.sqrt(2)
        
        dot1 = Dot(axes.c2p(-x_root_val, 2), color=WHITE)
        line_to_x_axis1 = DashedLine(dot1.get_center(), axes.c2p(-x_root_val, 0), color=WHITE)
        x_label1 = get_equation_text(f"x = -{x_root_val:.2f}", color=TEXT_COLOR, font_size=30).next_to(line_to_x_axis1.get_end(), DOWN)
        
        dot2 = Dot(axes.c2p(x_root_val, 2), color=WHITE)
        line_to_x_axis2 = DashedLine(dot2.get_center(), axes.c2p(x_root_val, 0), color=WHITE)
        x_label2 = get_equation_text(f"x = {x_root_val:.2f}", color=TEXT_COLOR, font_size=30).next_to(line_to_x_axis2.get_end(), DOWN)
        
        intersection_points.add(dot1, line_to_x_axis1, x_label1, dot2, line_to_x_axis2, x_label2)
        
        self.play(Create(intersection_points))
        self.wait(2)

        self.play(
            FadeOut(intersection_points),
            FadeOut(line_c),
            FadeOut(c_label),
            FadeOut(parabola),
            FadeOut(axes),
            FadeOut(labels)
        )
        self.wait(0.5)
        
        # --- Beat 2: Simple Case: x² = c - The Square ---
        eq_x_squared_c = get_equation_text("x² = c", color=GOLD_ACCENT_DARK).to_corner(UL).shift(UP*0.5)
        self.play(Transform(current_main_text, eq_x_squared_c)) # Transform the main text for continuity
        
        # Visualizing x^2 = c with squares
        square_x_side = 1.5
        square_x = Square(side_length=square_x_side, color=BLUE_ACCENT_DARK, fill_opacity=0.3)
        x_label_side1 = get_equation_text("x", color=BLUE_ACCENT_LIGHT, font_size=30).next_to(square_x.get_left(), LEFT, buff=SMALL_BUFF)
        x_label_side2 = get_equation_text("x", color=BLUE_ACCENT_LIGHT, font_size=30).next_to(square_x.get_bottom(), DOWN, buff=SMALL_BUFF)
        area_label_x = get_equation_text("Area = x²", color=GOLD_ACCENT_DARK, font_size=30).move_to(square_x.get_center())

        rect_c_height = square_x_side # Match one side for clear comparison
        rect_c_width = 2.0 
        rect_c = Rectangle(width=rect_c_width, height=rect_c_height, color=GOLD_ACCENT_DARK, fill_opacity=0.3)
        c_label_area = get_equation_text("Area = c", color=GOLD_ACCENT_DARK, font_size=30).move_to(rect_c.get_center())

        square_group = VGroup(square_x, x_label_side1, x_label_side2, area_label_x).to_edge(LEFT, buff=1).shift(DOWN*0.5)
        rect_group = VGroup(rect_c, c_label_area).to_edge(RIGHT, buff=1).shift(DOWN*0.5)

        self.play(
            Create(square_group),
            FadeIn(rect_group),
            run_time=2
        )
        
        arrow = Arrow(square_x.get_right(), rect_c.get_left(), buff=0.2, color=WHITE)
        equal_sign = get_equation_text("=", color=WHITE, font_size=40).move_to(arrow.get_center())
        self.play(GrowArrow(arrow), Write(equal_sign))
        self.wait(1)

        solution_text = get_equation_text("x = ±√c", color=BLUE_ACCENT_LIGHT, font_size=40).next_to(equal_sign, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(solution_text))
        self.wait(2)

        self.play(
            FadeOut(square_group),
            FadeOut(rect_group),
            FadeOut(arrow),
            FadeOut(equal_sign),
            FadeOut(solution_text),
        )
        self.wait(0.5)

        # --- Beat 3: Completing the Square: x² + bx = c ---
        eq_x_squared_bx_c = get_equation_text("x² + bx = c", color=GOLD_ACCENT_DARK).to_corner(UL).shift(UP*0.5)
        self.play(Transform(current_main_text, eq_x_squared_bx_c)) # Transform the main text placeholder

        # Visualizing completing the square with geometric shapes
        current_origin_for_square = ORIGIN + LEFT * 2.5 + DOWN * 0.5

        square_x_side = 2
        main_square = Square(side_length=square_x_side, color=BLUE_ACCENT_DARK, fill_opacity=0.3).move_to(current_origin_for_square)
        x_label_side_main = get_equation_text("x", color=BLUE_ACCENT_LIGHT, font_size=30).next_to(main_square.get_left(), LEFT)
        area_label_main = get_equation_text("x²", color=GOLD_ACCENT_DARK, font_size=30).move_to(main_square.get_center())
        
        self.play(Create(main_square), Write(x_label_side_main), Write(area_label_main))
        self.wait(0.5)

        # Add two rectangles for 'bx' terms (b/2 * x)
        b_over_2_val = 0.8
        rect1 = Rectangle(width=b_over_2_val, height=square_x_side, color=BLUE_ACCENT_DARK, fill_opacity=0.3)
        rect2 = Rectangle(width=square_x_side, height=b_over_2_val, color=BLUE_ACCENT_DARK, fill_opacity=0.3)

        rect1.move_to(main_square.get_right() + RIGHT * (b_over_2_val / 2))
        rect2.move_to(main_square.get_bottom() + DOWN * (b_over_2_val / 2))

        b_over_2_label_horiz = get_equation_text("b/2", color=BLUE_ACCENT_LIGHT, font_size=30).next_to(rect1.get_right(), RIGHT)
        b_over_2_label_vert = get_equation_text("b/2", color=BLUE_ACCENT_LIGHT, font_size=30).next_to(rect2.get_bottom(), DOWN)
        
        bx_label1 = get_equation_text("x(b/2)", color=GOLD_ACCENT_DARK, font_size=30).move_to(rect1.get_center())
        bx_label2 = get_equation_text("x(b/2)", color=GOLD_ACCENT_DARK, font_size=30).move_to(rect2.get_center())

        self.play(
            FadeIn(rect1), Write(b_over_2_label_horiz), Write(bx_label1)
        )
        self.play(
            FadeIn(rect2), Write(b_over_2_label_vert), Write(bx_label2)
        )
        self.wait(1)

        # Show the missing square to complete the larger square (b/2)^2
        missing_square = Square(side_length=b_over_2_val, color=GOLD_ACCENT_DARK, fill_opacity=0.5)
        missing_square.move_to(rect1.get_right() + RIGHT * (b_over_2_val / 2)).align_to(rect2.get_top(), UP)
        missing_label = get_equation_text("(b/2)²", color=WHITE, font_size=30).move_to(missing_square.get_center())

        self.play(Create(missing_square), Write(missing_label))
        self.wait(1)

        # Group everything and scale down, move aside
        completing_square_group = VGroup(
            main_square, x_label_side_main, area_label_main,
            rect1, b_over_2_label_horiz, bx_label1,
            rect2, b_over_2_label_vert, bx_label2,
            missing_square, missing_label
        )
        
        self.play(
            completing_square_group.animate.shift(RIGHT * 4).scale(0.5)
        )

        # Show the algebraic form of completing the square
        new_eq_title = get_equation_text("(x + b/2)² = c + (b/2)²", color=BLUE_ACCENT_LIGHT).next_to(current_main_text, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(new_eq_title))
        self.wait(2)

        self.play(
            FadeOut(new_eq_title),
            FadeOut(completing_square_group)
        )
        self.wait(0.5)
        
        # --- Beat 4: The General Form: ax² + bx + c = 0 ---
        # Reintroduce Axes for parabola visualization
        axes_general = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE_ACCENT_LIGHT, "font_size": 24},
            tips=False
        ).shift(DOWN * 0.5) 
        labels_general = axes_general.get_axis_labels(x_label=Text("x", color=BLUE_ACCENT_LIGHT), y_label=Text("y", color=BLUE_ACCENT_LIGHT))
        
        self.play(Create(axes_general), Write(labels_general))
        self.wait(0.5)

        general_eq_text = get_equation_text("ax² + bx + c = 0", color=GOLD_ACCENT_DARK).to_corner(UL).shift(UP*0.5)
        self.play(Transform(current_main_text, general_eq_text)) # Transform main text placeholder
        self.wait(1)
        
        # Parabola variations to show 2, 1, or 0 roots
        parabola_two_roots = axes_general.get_graph(lambda x: 0.5 * x**2 - 1, color=BLUE_ACCENT_DARK) # Example: Two roots
        parabola_one_root = axes_general.get_graph(lambda x: 0.5 * (x-1)**2, color=BLUE_ACCENT_DARK) # Example: One root (vertex on x-axis)
        parabola_zero_roots = axes_general.get_graph(lambda x: 0.5 * (x-1)**2 + 1, color=BLUE_ACCENT_DARK) # Example: Zero roots

        # Initial parabola with 2 roots
        self.play(Create(parabola_two_roots))
        roots_text_info = get_equation_text("2 Solutions", color=TEXT_COLOR, font_size=35).next_to(parabola_two_roots, UP).shift(UP*0.5)
        self.play(Write(roots_text_info))
        self.wait(1)

        # Animate to 1 root (parabola shifts to touch x-axis)
        self.play(
            Transform(parabola_two_roots, parabola_one_root),
            roots_text_info.animate.become(get_equation_text("1 Solution", color=TEXT_COLOR, font_size=35).next_to(parabola_one_root, UP).shift(UP*0.5)),
            run_time=1.5
        )
        self.wait(1)

        # Animate to 0 roots (parabola shifts above x-axis)
        self.play(
            Transform(parabola_two_roots, parabola_zero_roots),
            roots_text_info.animate.become(get_equation_text("0 Solutions", color=TEXT_COLOR, font_size=35).next_to(parabola_zero_roots, UP).shift(UP*0.5)),
            run_time=1.5
        )
        self.wait(2)

        self.play(
            FadeOut(parabola_two_roots),
            FadeOut(roots_text_info),
            FadeOut(current_main_text), # Fade out the last equation text
            FadeOut(axes_general),
            FadeOut(labels_general)
        )
        self.wait(0.5)

        # --- Beat 5: Recap ---
        recap_title = Text("Recap: Geometric Interpretation of Quadratic Solutions", font_size=45, color=GOLD_ACCENT_DARK).to_corner(UL)
        recap_point1 = get_equation_text("- Solving quadratics means finding x-intercepts of y = ax² + bx + c.", color=BLUE_ACCENT_LIGHT, font_size=35)
        recap_point2 = get_equation_text("- Visualizing the parabola explains 0, 1, or 2 solutions.", color=BLUE_ACCENT_LIGHT, font_size=35)
        
        recap_point1.next_to(recap_title, DOWN, buff=MED_LARGE_BUFF).align_to(recap_title, LEFT)
        recap_point2.next_to(recap_point1, DOWN, buff=MED_SMALL_BUFF).align_to(recap_point1, LEFT)

        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(FadeIn(recap_point1, shift=DOWN))
        self.wait(0.5)
        self.play(FadeIn(recap_point2, shift=DOWN))
        self.wait(3)

        self.play(FadeOut(recap_title), FadeOut(recap_point1), FadeOut(recap_point2))
        self.wait(1)