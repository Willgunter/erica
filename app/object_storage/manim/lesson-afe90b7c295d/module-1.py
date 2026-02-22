from manim import *

class QuadraticBasics(Scene):
    def construct(self):
        # 0. Setup - Colors and Initial Hook
        self.camera.background_color = "#202020"  # Dark background
        blue_accent = "#58CCED"  # Light blue for accents
        gold_accent = "#FFD700"  # Gold for other accents
        text_color = WHITE
        subtle_grey = GREY_A

        # Title and Objective Introduction
        title = Text("Basics of Quadratic Equations", font_size=50, color=text_color)
        objective = Text("Understand and apply quadratic equations", font_size=30, color=blue_accent).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), FadeIn(objective, shift=UP), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title, shift=UP), FadeOut(objective, shift=UP), run_time=0.8)

        # --- Beat 1: Intuition - Area & Growth (Visually representing x and x^2) ---
        beat1_title = Text("Quadratic relationships are everywhere!", color=gold_accent).to_edge(UP)
        self.play(FadeIn(beat1_title, shift=UP))

        # Dynamic Square to represent x and x^2
        x_val_tracker = ValueTracker(1.5)
        
        x_label = MathTex("x = ", color=blue_accent).to_corner(UL).shift(DOWN*0.5 + RIGHT*0.5)
        x_number = always_redraw(lambda: DecimalNumber(x_val_tracker.get_value(), num_decimal_places=1).next_to(x_label, RIGHT))
        
        x_squared_label = MathTex("x^2 = ", color=text_color).next_to(x_label, DOWN, alignment=LEFT, buff=0.8)
        x_squared_number = always_redraw(lambda: DecimalNumber(x_val_tracker.get_value()**2, num_decimal_places=1).next_to(x_squared_label, RIGHT))

        dynamic_square = always_redraw(lambda: Square(
            side_length=x_val_tracker.get_value(), 
            color=blue_accent, 
            fill_opacity=0.3
        ).move_to(ORIGIN + LEFT*2.5))
        
        area_math = always_redraw(lambda: MathTex(
            f"\\text{{Area}} = ({x_val_tracker.get_value():.1f})^2 = {x_val_tracker.get_value()**2:.1f}",
            color=text_color
        ).next_to(dynamic_square, RIGHT, buff=0.8).shift(UP*0.5))

        self.play(Create(dynamic_square), Write(x_label), Write(x_number), 
                  Write(x_squared_label), Write(x_squared_number), Write(area_math))
        self.play(x_val_tracker.animate.set_value(3), run_time=2)
        self.play(x_val_tracker.animate.set_value(0.8), run_time=1.5)
        self.play(x_val_tracker.animate.set_value(2), run_time=1)
        self.wait(0.5)

        bio_context_beat1 = Text(
            "Like growth of a bacterial colony, or spread on a surface.", 
            font_size=24, color=subtle_grey
        ).next_to(area_math, DOWN, buff=0.5).shift(RIGHT*0.5)
        self.play(FadeIn(bio_context_beat1, shift=DOWN))
        self.wait(1.5)

        self.play(FadeOut(VGroup(beat1_title, x_label, x_number, x_squared_label, x_squared_number, 
                                 dynamic_square, area_math, bio_context_beat1)))

        # --- Beat 2: Formal Definition ---
        beat2_title = Text("Defining the Quadratic Equation", color=gold_accent).to_edge(UP)
        self.play(FadeIn(beat2_title, shift=UP))

        quadratic_form = MathTex("ax^2 + bx + c = 0", color=blue_accent, font_size=60).move_to(ORIGIN + UP*0.5)
        
        self.play(Write(quadratic_form), run_time=1.5)
        self.wait(0.5)

        a_const = MathTex("a \\neq 0", color=gold_accent).next_to(quadratic_form, DOWN * 1.5, alignment=LEFT).shift(LEFT*1.5)
        a_desc = Text("Quadratic Term Coefficient", font_size=25, color=text_color).next_to(a_const, RIGHT, buff=0.5)
        b_desc = Text("Linear Term Coefficient", font_size=25, color=text_color).next_to(a_desc, DOWN, alignment=LEFT, buff=0.4)
        c_desc = Text("Constant Term", font_size=25, color=text_color).next_to(b_desc, DOWN, alignment=LEFT, buff=0.4)
        
        arrow_a = Arrow(start=a_desc.get_top() + LEFT*0.5, end=quadratic_form.get_parts_by_tex("a")[0].get_bottom() + UP*0.1, buff=0.2, color=subtle_grey)
        arrow_b = Arrow(start=b_desc.get_top(), end=quadratic_form.get_parts_by_tex("b")[0].get_bottom() + UP*0.1, buff=0.2, color=subtle_grey)
        arrow_c = Arrow(start=c_desc.get_top(), end=quadratic_form.get_parts_by_tex("c")[0].get_bottom() + UP*0.1, buff=0.2, color=subtle_grey)

        self.play(Write(a_const), FadeIn(a_desc), Create(arrow_a))
        self.play(FadeIn(b_desc), Create(arrow_b))
        self.play(FadeIn(c_desc), Create(arrow_c))
        self.wait(2)

        self.play(FadeOut(VGroup(beat2_title, quadratic_form, a_const, a_desc, b_desc, c_desc, arrow_a, arrow_b, arrow_c)))

        # --- Beat 3: The Parabola - Graphing y = ax^2 + bx + c ---
        beat3_title = Text("The Parabola: Visualizing Quadratic Functions", color=gold_accent).to_edge(UP)
        self.play(FadeIn(beat3_title, shift=UP))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 8, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": subtle_grey, "include_numbers": True},
            tips=False
        ).to_edge(DOWN).shift(UP*0.5)
        
        x_label_ax = axes.get_x_axis_label(MathTex("x", color=text_color)).shift(RIGHT*0.3)
        y_label_ax = axes.get_y_axis_label(MathTex("y", color=text_color)).shift(UP*0.3)
        
        self.play(Create(axes), Write(x_label_ax), Write(y_label_ax), run_time=1)
        
        # Plot y = x^2
        parabola_1 = axes.get_graph(lambda x: x**2, color=blue_accent, x_range=[-3, 3])
        eq_1_text = MathTex("y = x^2", color=blue_accent).next_to(parabola_1, UP + RIGHT, buff=0.2).shift(RIGHT*0.5)
        self.play(Create(parabola_1), Write(eq_1_text))
        self.wait(1)

        # Illustrate 'a' changing width/direction (y = 0.5x^2, y = -x^2)
        parabola_2 = axes.get_graph(lambda x: 0.5*x**2, color=gold_accent, x_range=[-3.5, 3.5])
        eq_2_text = MathTex("y = 0.5x^2", color=gold_accent).next_to(parabola_2, UP + LEFT, buff=0.2).shift(LEFT*0.5)
        
        self.play(ReplacementTransform(parabola_1, parabola_2), ReplacementTransform(eq_1_text, eq_2_text))
        self.wait(1)
        
        parabola_3 = axes.get_graph(lambda x: -0.8*x**2 + 5, color=text_color, x_range=[-3, 3])
        eq_3_text = MathTex("y = -0.8x^2 + 5", color=text_color).next_to(parabola_3, DOWN + LEFT, buff=0.2)
        
        self.play(ReplacementTransform(parabola_2, parabola_3), ReplacementTransform(eq_2_text, eq_3_text))
        
        bio_context_beat3 = Text(
            "Think of trajectories (like a jumping frog) or dose-response curves.", 
            font_size=24, color=subtle_grey
        ).to_corner(DR).shift(LEFT*0.5 + UP*0.5)
        self.play(FadeIn(bio_context_beat3, shift=DOWN))
        self.wait(2)

        self.play(FadeOut(VGroup(beat3_title, axes, x_label_ax, y_label_ax, parabola_3, eq_3_text, bio_context_beat3)))

        # --- Beat 4: Roots/Solutions (Where the Parabola Crosses the X-axis) ---
        beat4_title = Text("Finding the Roots: Where the function is zero", color=gold_accent).to_edge(UP)
        self.play(FadeIn(beat4_title, shift=UP))

        axes_roots = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": subtle_grey, "include_numbers": True},
            tips=False
        ).to_edge(DOWN).shift(UP*0.5)
        
        self.play(Create(axes_roots), run_time=0.8)
        
        # Parabola with 2 roots
        parabola_2_roots = axes_roots.get_graph(lambda x: x**2 - 2*x - 2, color=blue_accent, x_range=[-1.5, 3.5])
        eq_2_roots_text = MathTex("y = x^2 - 2x - 2", color=blue_accent).next_to(parabola_2_roots, UP + LEFT, buff=0.2)
        self.play(Create(parabola_2_roots), Write(eq_2_roots_text))
        
        root1_pos = axes_roots.c2p(1 - (3**0.5), 0) # Exact root for x^2 - 2x - 2
        root2_pos = axes_roots.c2p(1 + (3**0.5), 0)
        
        root1_dot = Dot(root1_pos, color=gold_accent, radius=0.1)
        root2_dot = Dot(root2_pos, color=gold_accent, radius=0.1)
        root1_label = MathTex("x_1", color=gold_accent).next_to(root1_dot, DOWN)
        root2_label = MathTex("x_2", color=gold_accent).next_to(root2_dot, DOWN)

        self.play(FadeIn(root1_dot, scale=0.5), FadeIn(root2_dot, scale=0.5))
        self.play(Write(root1_label), Write(root2_label))
        self.wait(1.5)

        # Parabola with 1 root
        parabola_1_root = axes_roots.get_graph(lambda x: 0.5*(x-1)**2, color=gold_accent, x_range=[-2, 4])
        eq_1_root_text = MathTex("y = 0.5(x-1)^2", color=gold_accent).next_to(parabola_1_root, UP + RIGHT, buff=0.2)
        
        self.play(ReplacementTransform(parabola_2_roots, parabola_1_root), 
                  ReplacementTransform(eq_2_roots_text, eq_1_root_text),
                  FadeOut(root1_dot, root2_dot, root1_label, root2_label))
        
        root_single_dot = Dot(axes_roots.c2p(1, 0), color=blue_accent, radius=0.1)
        root_single_label = MathTex("x_1 = x_2", color=blue_accent).next_to(root_single_dot, DOWN)
        self.play(FadeIn(root_single_dot, scale=0.5), Write(root_single_label))
        self.wait(1.5)

        # Parabola with 0 roots
        parabola_0_roots = axes_roots.get_graph(lambda x: 0.5*x**2 + 1, color=text_color, x_range=[-3, 3])
        eq_0_roots_text = MathTex("y = 0.5x^2 + 1", color=text_color).next_to(parabola_0_roots, UP + LEFT, buff=0.2)
        
        self.play(ReplacementTransform(parabola_1_root, parabola_0_roots), 
                  ReplacementTransform(eq_1_root_text, eq_0_roots_text),
                  FadeOut(root_single_dot, root_single_label))
        
        no_roots_text = Text("No real solutions", font_size=25, color=subtle_grey).next_to(eq_0_roots_text, DOWN, alignment=LEFT).shift(LEFT*0.2)
        self.play(Write(no_roots_text))
        self.wait(2)

        self.play(FadeOut(VGroup(beat4_title, axes_roots, parabola_0_roots, eq_0_roots_text, no_roots_text)))

        # --- Beat 5: Recap Card ---
        recap_card_outline = Rectangle(width=10, height=6, color=blue_accent, fill_opacity=0.1).center()
        
        recap_title_text = Text("Recap: Quadratic Equations", font_size=40, color=gold_accent).move_to(recap_card_outline.get_center() + UP*2.5)
        
        concept1 = MathTex("\\bullet \\text{ General form: } ax^2 + bx + c = 0 \\text{ (with } a \\neq 0 \\text{)}", font_size=28, color=text_color).next_to(recap_title_text, DOWN, buff=0.6).align_to(recap_card_outline.get_left(), LEFT).shift(RIGHT*0.7)
        concept2 = Text("• Graph is a parabola (U-shape)", font_size=28, color=text_color).next_to(concept1, DOWN, buff=0.4).align_to(concept1, LEFT)
        concept3 = Text("• Roots are x-intercepts (0, 1, or 2 real solutions)", font_size=28, color=text_color).next_to(concept2, DOWN, buff=0.4).align_to(concept1, LEFT)
        
        next_steps_title = Text("Next Steps:", font_size=32, color=blue_accent).next_to(concept3, DOWN, buff=0.8).align_to(concept1, LEFT).shift(LEFT*0.2)
        next_step_1 = Text("• Concept Walkthrough (Deep Dive)", font_size=24, color=subtle_grey).next_to(next_steps_title, DOWN, buff=0.3).align_to(concept1, LEFT).shift(RIGHT*0.7)
        next_step_2 = Text("• Guided Practice (Flashcards)", font_size=24, color=subtle_grey).next_to(next_step_1, DOWN, buff=0.2).align_to(concept1, LEFT).shift(RIGHT*0.7)
        next_step_3 = Text("• AI Spar with Erica (Test your knowledge)", font_size=24, color=subtle_grey).next_to(next_step_2, DOWN, buff=0.2).align_to(concept1, LEFT).shift(RIGHT*0.7)

        recap_group = VGroup(recap_card_outline, recap_title_text, concept1, concept2, concept3, next_steps_title, next_step_1, next_step_2, next_step_3)
        
        self.play(FadeIn(recap_card_outline), Write(recap_title_text))
        self.play(LaggedStart(
            Write(concept1),
            Write(concept2),
            Write(concept3),
            lag_ratio=0.7, run_time=3
        ))
        self.wait(0.5)
        self.play(Write(next_steps_title))
        self.play(LaggedStart(
            Write(next_step_1),
            Write(next_step_2),
            Write(next_step_3),
            lag_ratio=0.7, run_time=3
        ))
        self.wait(3)