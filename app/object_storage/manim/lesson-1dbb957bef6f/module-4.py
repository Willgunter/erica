from manim import *

class PredictingSolutionTypes(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE = '#5DADE2'
        GOLD = '#F1C40F'
        LIGHT_GRAY = '#CCCCCC'

        # --- Beat 1: Visual Hook & Introduction ---
        # 1. Visual Hook: Parabola intersecting X-axis, showing roots
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=7,
            y_length=7,
            tips=False
        ).to_edge(LEFT, buff=1)
        axes.add_coordinates()
        
        # Parabola y = x^2 - 1
        parabola_initial = axes.get_graph(lambda x: x**2 - 1, x_range=[-2, 2], color=BLUE)
        root1_initial = Dot(axes.c2p(-1, 0), color=GOLD, radius=0.08)
        root2_initial = Dot(axes.c2p(1, 0), color=GOLD, radius=0.08)
        
        title = Text("Predicting Solution Types", font_size=48, color=LIGHT_GRAY).to_edge(UP, buff=0.5)
        with_discriminant = Text("with the Discriminant", font_size=36, color=GOLD).next_to(title, DOWN, buff=0.1)

        self.play(
            LaggedStart(
                Create(axes),
                Create(parabola_initial),
                FadeIn(root1_initial, shift=UP),
                FadeIn(root2_initial, shift=UP),
                lag_ratio=0.7
            ),
            Write(title),
            Write(with_discriminant),
            run_time=2
        )
        self.wait(0.5)

        # Shift parabola to show 1 root (tangent)
        parabola_one_root = axes.get_graph(lambda x: x**2, x_range=[-2, 2], color=BLUE)
        root_one = Dot(axes.c2p(0, 0), color=GOLD, radius=0.08)

        self.play(
            Transform(parabola_initial, parabola_one_root),
            Transform(root1_initial, root_one), # Re-purpose root1_initial for the single root
            FadeOut(root2_initial),
            run_time=1
        )
        self.wait(0.5)
        
        # Shift parabola to show 0 roots
        parabola_no_roots = axes.get_graph(lambda x: x**2 + 1, x_range=[-2, 2], color=BLUE)
        self.play(
            Transform(parabola_initial, parabola_no_roots),
            FadeOut(root1_initial), # The single root fades out as there are no real roots
            run_time=1
        )
        self.wait(0.5)

        # Introduce quadratic equation
        quadratic_eq_text = MathTex("ax^2 + bx + c = 0", color=LIGHT_GRAY, font_size=40).move_to(title.get_center())
        quadratic_eq_text.shift(DOWN*1.5)

        self.play(
            FadeOut(title, shift=UP),
            FadeOut(with_discriminant, shift=UP),
            Write(quadratic_eq_text),
            parabola_initial.animate.scale(0.8).next_to(quadratic_eq_text, DOWN, buff=0.8).fade(0.5), # Make the parabola less prominent
            FadeOut(axes),
            run_time=1.5
        )
        self.wait(0.5)


        # --- Beat 2: Parabolas & Solutions (Visual Intuition) ---
        self.play(FadeOut(parabola_initial))
        
        solutions_title = Text("How many times does it cross?", color=LIGHT_GRAY, font_size=36).to_edge(UP, buff=0.5)
        self.play(Transform(quadratic_eq_text, solutions_title)) # Re-purpose text for title

        axes_group = VGroup()
        parabolas_group = VGroup()
        labels_group = VGroup()

        # Parabola 1: Two Real Solutions
        axes1 = Axes(x_range=[-2.5, 2.5, 1], y_range=[-1.5, 2.5, 1], x_length=3, y_length=3).shift(LEFT*4 + UP*0.5)
        graph1 = axes1.get_graph(lambda x: x**2 - 1, x_range=[-1.5, 1.5], color=BLUE)
        label1 = MathTex("\\text{2 Real Solutions}", color=GOLD).next_to(axes1, DOWN, buff=0.2)
        root_dot1a = Dot(axes1.c2p(-1,0), color=GOLD, radius=0.05)
        root_dot1b = Dot(axes1.c2p(1,0), color=GOLD, radius=0.05)
        
        self.play(
            Create(axes1),
            Create(graph1),
            FadeIn(root_dot1a, root_dot1b),
            Write(label1),
            run_time=1.5
        )
        self.wait(0.5)

        # Parabola 2: One Real Solution
        axes2 = Axes(x_range=[-2.5, 2.5, 1], y_range=[-1.5, 2.5, 1], x_length=3, y_length=3).shift(UP*0.5)
        graph2 = axes2.get_graph(lambda x: x**2, x_range=[-1.5, 1.5], color=BLUE)
        label2 = MathTex("\\text{1 Real Solution}", color=GOLD).next_to(axes2, DOWN, buff=0.2)
        root_dot2 = Dot(axes2.c2p(0,0), color=GOLD, radius=0.05)

        self.play(
            Create(axes2),
            Create(graph2),
            FadeIn(root_dot2),
            Write(label2),
            run_time=1.5
        )
        self.wait(0.5)

        # Parabola 3: Zero Real Solutions
        axes3 = Axes(x_range=[-2.5, 2.5, 1], y_range=[-1.5, 2.5, 1], x_length=3, y_length=3).shift(RIGHT*4 + UP*0.5)
        graph3 = axes3.get_graph(lambda x: x**2 + 1, x_range=[-1.5, 1.5], color=BLUE)
        label3 = MathTex("\\text{0 Real Solutions}", color=GOLD).next_to(axes3, DOWN, buff=0.2)

        self.play(
            Create(axes3),
            Create(graph3),
            Write(label3),
            run_time=1.5
        )
        self.wait(1)
        
        self.play(
            FadeOut(axes1, axes2, axes3),
            FadeOut(graph1, graph2, graph3),
            FadeOut(label1, label2, label3),
            FadeOut(root_dot1a, root_dot1b, root_dot2),
            FadeOut(solutions_title),
            run_time=1.5
        )


        # --- Beat 3: Introducing the Discriminant ---
        quadratic_formula = MathTex(
            "x = {-b \\pm \\sqrt{b^2 - 4ac} \\over 2a}",
            substrings_to_isolate=["b^2 - 4ac"],
            color=LIGHT_GRAY,
            font_size=48
        ).center()

        self.play(Write(quadratic_formula), run_time=2)
        self.wait(1)

        discriminant_part = quadratic_formula.get_parts_by_tex("b^2 - 4ac")
        discriminant_label = Text("The Discriminant", color=GOLD, font_size=36).next_to(discriminant_part, UP, buff=0.5)
        discriminant_box = SurroundingRectangle(discriminant_part, color=GOLD, buff=0.1)

        self.play(
            Create(discriminant_box),
            Write(discriminant_label),
            run_time=1.5
        )
        self.wait(1)

        intuition_text = Text(
            "This part determines the nature of the solutions!",
            color=BLUE, font_size=28
        ).next_to(discriminant_label, UP, buff=0.5) # Position slightly higher
        
        arrow = Arrow(intuition_text.get_bottom(), discriminant_label.get_top(), buff=0.2, color=BLUE)
        
        self.play(
            FadeIn(intuition_text, shift=UP),
            GrowArrow(arrow),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(quadratic_formula, shift=UP),
            FadeOut(discriminant_box, shift=UP),
            FadeOut(discriminant_label, shift=UP),
            FadeOut(intuition_text, shift=UP),
            FadeOut(arrow, shift=UP),
            run_time=1.5
        )


        # --- Beat 4: Discriminant Values & Solution Types ---
        discriminant_symbol = MathTex("\\Delta = b^2 - 4ac", color=LIGHT_GRAY, font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(discriminant_symbol), run_time=1)
        self.wait(0.5)

        # Condition 1: Delta > 0
        cond1_math = MathTex("\\Delta > 0", color=GOLD).shift(LEFT*4 + UP*0.5)
        cond1_result = MathTex("\\Rightarrow \\text{2 Real Solutions}", color=BLUE).next_to(cond1_math, RIGHT, buff=0.5)
        
        # Small parabola icon for 2 solutions
        mini_axes1 = Axes(x_range=[-1.5, 1.5], y_range=[-0.5, 1.5], x_length=1.5, y_length=1.5).scale(0.5).next_to(cond1_result, RIGHT, buff=0.5)
        mini_graph1 = mini_axes1.get_graph(lambda x: x**2 - 0.2, x_range=[-0.8, 0.8], color=BLUE)
        mini_dots1 = VGroup(Dot(mini_axes1.c2p(-0.45,0), color=GOLD, radius=0.03), Dot(mini_axes1.c2p(0.45,0), color=GOLD, radius=0.03))
        mini_vis1 = VGroup(mini_axes1, mini_graph1, mini_dots1)

        self.play(
            Write(cond1_math),
            Write(cond1_result),
            FadeIn(mini_vis1),
            run_time=1.5
        )
        self.wait(1)

        # Condition 2: Delta = 0
        cond2_math = MathTex("\\Delta = 0", color=GOLD).next_to(cond1_math, DOWN, buff=0.8)
        cond2_result = MathTex("\\Rightarrow \\text{1 Real Solution}", color=BLUE).next_to(cond2_math, RIGHT, buff=0.5)
        
        # Small parabola icon for 1 solution
        mini_axes2 = Axes(x_range=[-1.5, 1.5], y_range=[-0.5, 1.5], x_length=1.5, y_length=1.5).scale(0.5).next_to(cond2_result, RIGHT, buff=0.5)
        mini_graph2 = mini_axes2.get_graph(lambda x: x**2, x_range=[-0.8, 0.8], color=BLUE)
        mini_dots2 = Dot(mini_axes2.c2p(0,0), color=GOLD, radius=0.03)
        mini_vis2 = VGroup(mini_axes2, mini_graph2, mini_dots2)

        self.play(
            Write(cond2_math),
            Write(cond2_result),
            FadeIn(mini_vis2),
            run_time=1.5
        )
        self.wait(1)

        # Condition 3: Delta < 0
        cond3_math = MathTex("\\Delta < 0", color=GOLD).next_to(cond2_math, DOWN, buff=0.8)
        cond3_result = MathTex("\\Rightarrow \\text{0 Real Solutions}", color=BLUE).next_to(cond3_math, RIGHT, buff=0.5)
        
        # Small parabola icon for 0 solutions
        mini_axes3 = Axes(x_range=[-1.5, 1.5], y_range=[-0.5, 1.5], x_length=1.5, y_length=1.5).scale(0.5).next_to(cond3_result, RIGHT, buff=0.5)
        mini_graph3 = mini_axes3.get_graph(lambda x: x**2 + 0.2, x_range=[-0.8, 0.8], color=BLUE)
        mini_vis3 = VGroup(mini_axes3, mini_graph3)

        self.play(
            Write(cond3_math),
            Write(cond3_result),
            FadeIn(mini_vis3),
            run_time=1.5
        )
        self.wait(2)


        # --- Beat 5: Recap Card ---
        recap_card_title = Text("Recap: The Discriminant (Δ)", color=GOLD, font_size=40).to_edge(UP, buff=0.8)
        
        recap_text1 = MathTex("\\Delta > 0 \\Rightarrow \\text{2 Real Solutions}", color=LIGHT_GRAY).next_to(recap_card_title, DOWN, buff=0.8)
        recap_text2 = MathTex("\\Delta = 0 \\Rightarrow \\text{1 Real Solution}", color=LIGHT_GRAY).next_to(recap_text1, DOWN, buff=0.4)
        recap_text3 = MathTex("\\Delta < 0 \\Rightarrow \\text{0 Real Solutions}", color=LIGHT_GRAY).next_to(recap_text2, DOWN, buff=0.4)

        recap_group = VGroup(recap_card_title, recap_text1, recap_text2, recap_text3)
        recap_group.center() # Center the whole group

        self.play(
            FadeOut(discriminant_symbol, shift=UP),
            FadeOut(cond1_math, cond1_result, mini_vis1, shift=UP),
            FadeOut(cond2_math, cond2_result, mini_vis2, shift=UP),
            FadeOut(cond3_math, cond3_result, mini_vis3, shift=UP),
            FadeIn(recap_group),
            run_time=1.5
        )
        self.wait(3)

        # Optional: AI Spar prompt
        ai_spar_text = Text(
            "Ready to test your understanding with Erica?",
            color=BLUE, font_size=32
        ).next_to(recap_text3, DOWN, buff=1.0)
        
        ai_spar_button = Rectangle(
            width=3.0, height=0.8, color=GOLD, fill_opacity=0.2
        ).next_to(ai_spar_text, DOWN, buff=0.3)
        
        button_text = Text("Start AI Spar", color=GOLD, font_size=28).move_to(ai_spar_button)
        
        self.play(
            FadeIn(ai_spar_text, shift=UP),
            Create(ai_spar_button),
            Write(button_text),
            run_time=1
        )
        self.wait(2)
        
        self.play(
            FadeOut(recap_group, shift=UP),
            FadeOut(ai_spar_text, shift=UP),
            FadeOut(ai_spar_button, shift=UP),
            FadeOut(button_text, shift=UP),
            run_time=1
        )
        self.wait(1)