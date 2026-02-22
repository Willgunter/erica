from manim import *

class DiscriminantAnimation(Scene):
    def construct(self):
        # --- Colors ---
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_E 
        LIGHT_TEXT = WHITE
        HIGHLIGHT_BLUE = BLUE_E
        HIGHLIGHT_GOLD = GOLD_C

        # --- Helper for creating discriminant text (b^2 - 4ac) without Tex/MathTex ---
        def create_discriminant_expression(color=HIGHLIGHT_GOLD, font_size=50):
            b_char = Text("b", font_size=font_size, color=color)
            exp_char = Text("2", font_size=font_size * 0.6, color=color)
            
            # Position '2' as a superscript to 'b'
            exp_char.next_to(b_char, UP + RIGHT, buff=0.01).shift(0.05 * UP)
            
            # Group 'b' and '2'
            b_squared_group = VGroup(b_char, exp_char)
            
            # Create the rest of the expression
            minus_4ac_text = Text("- 4ac", font_size=font_size, color=color)
            
            # Arrange the full expression
            final_group = VGroup(b_squared_group, minus_4ac_text).arrange(RIGHT, buff=0.1)
            return final_group

        # --- Scene 0: Visual Hook & Title ---
        title = Text("Discriminant: Nature of Solutions", font_size=60, color=HIGHLIGHT_BLUE).move_to(UP*2.5)
        subtitle = Text("Inside the quadratic formula lies a critical expression:", font_size=30, color=LIGHT_TEXT).next_to(title, DOWN, buff=0.5)
        expression_label = create_discriminant_expression(color=HIGHLIGHT_GOLD, font_size=50).next_to(subtitle, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                Write(title),
                Write(subtitle),
                FadeIn(expression_label, shift=UP),
                lag_ratio=0.7
            ),
            run_time=3
        )
        self.wait(1)

        # Create a simple NumberPlane and Axes for background
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": GREY_B, "stroke_width": 1},
            background_line_style={"stroke_color": GREY_D, "stroke_width": 0.5, "stroke_opacity": 0.6}
        ).add_coordinates()
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": GREY_B, "stroke_width": 2},
            x_axis_config={"numbers_to_exclude": [0]},
            y_axis_config={"numbers_to_exclude": [0]}
        )

        x_axis_label = Text("x", font_size=30, color=LIGHT_TEXT).next_to(axes.x_axis.get_end(), RIGHT, buff=0.1)
        y_axis_label = Text("y", font_size=30, color=LIGHT_TEXT).next_to(axes.y_axis.get_end(), UP, buff=0.1)
        axes_labels = VGroup(x_axis_label, y_axis_label)

        self.play(
            FadeOut(title, shift=UP*0.5),
            FadeOut(subtitle, shift=UP*0.5),
            FadeOut(expression_label, shift=UP*0.5),
            Create(plane),
            Create(axes),
            Create(axes_labels),
            run_time=1.5
        )
        self.wait(0.5)

        # Initial parabola (visual hook sequence)
        def func_parabola_two_roots(x):
            return 0.5 * (x - 2) * (x + 3) # Roots at x=2, x=-3
        parabola_state = axes.plot(func_parabola_two_roots, x_range=[-5, 4], color=BLUE_ACCENT)
        roots_state = VGroup(
            Dot(axes.c2p(2, 0), color=HIGHLIGHT_GOLD),
            Dot(axes.c2p(-3, 0), color=HIGHLIGHT_GOLD)
        )
        self.play(Create(parabola_state), Create(roots_state), run_time=2)
        self.wait(0.5)

        # Transition to one root
        def func_parabola_one_root(x):
            return 0.5 * (x - 1)**2 # Root at x=1
        parabola_one_root = axes.plot(func_parabola_one_root, x_range=[-3, 5], color=BLUE_ACCENT)
        root_one_state = Dot(axes.c2p(1, 0), color=HIGHLIGHT_GOLD)

        self.play(
            Transform(parabola_state, parabola_one_root),
            Transform(roots_state, root_one_state), # Transform VGroup to single Dot
            run_time=1.5
        )
        self.wait(0.5)

        # Transition to no roots
        def func_parabola_no_roots(x):
            return 0.5 * x**2 + 2 # No real roots
        parabola_no_roots = axes.plot(func_parabola_no_roots, x_range=[-4, 4], color=BLUE_ACCENT)

        self.play(
            Transform(parabola_state, parabola_no_roots),
            FadeOut(roots_state, scale=0.5), # Fade out the last root(s)
            run_time=1.5
        )
        self.wait(1)

        # Fade out parabola and prepare for specific cases
        self.play(
            FadeOut(parabola_state, shift=DOWN),
            FadeOut(plane),
            FadeOut(axes),
            FadeOut(axes_labels),
            run_time=1.5
        )

        # --- Beat 1: The Discriminant Expression ---
        discriminant_expr = create_discriminant_expression(color=HIGHLIGHT_GOLD, font_size=60)
        discriminant_name = Text("The Discriminant", font_size=50, color=HIGHLIGHT_BLUE).next_to(discriminant_expr, DOWN, buff=0.5)

        self.play(
            FadeIn(discriminant_expr, scale=0.5),
            Write(discriminant_name)
        )
        self.wait(2)

        self.play(FadeOut(discriminant_name), discriminant_expr.animate.to_corner(UL).scale(0.7))
        self.wait(0.5)

        # Re-introduce axes for graphing
        self.play(
            Create(plane),
            Create(axes),
            Create(axes_labels),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 2: Discriminant > 0 (Two Real Solutions) ---
        current_title = Text("Case 1: Discriminant > 0", font_size=40, color=HIGHLIGHT_BLUE).to_edge(UP)
        expr_d_gt_0_symbols = VGroup(
            Text(" > ", font_size=50, color=HIGHLIGHT_GOLD),
            Text("0", font_size=50, color=HIGHLIGHT_GOLD)
        ).arrange(RIGHT, buff=0.1)
        expr_d_gt_0 = VGroup(
            discriminant_expr.copy(),
            expr_d_gt_0_symbols
        ).arrange(RIGHT, buff=0.1).next_to(current_title, DOWN, buff=0.3)
        
        # Function and parabola for > 0 case
        parabola_obj = axes.plot(func_parabola_two_roots, x_range=[-5, 4], color=BLUE_ACCENT)
        roots_obj = VGroup(
            Dot(axes.c2p(2, 0), color=HIGHLIGHT_GOLD),
            Dot(axes.c2p(-3, 0), color=HIGHLIGHT_GOLD)
        )
        label_solutions = Text("Two Distinct Real Solutions", font_size=35, color=LIGHT_TEXT).next_to(expr_d_gt_0, DOWN, buff=0.7)
        label_solutions.align_to(expr_d_gt_0, LEFT)

        self.play(
            FadeIn(current_title, shift=UP),
            ReplacementTransform(discriminant_expr, expr_d_gt_0[0]), # Transform the small discriminant_expr
            Write(expr_d_gt_0[1]), # Write '> 0' VGroup
            Create(parabola_obj),
            run_time=2.5
        )
        self.play(
            Create(roots_obj),
            FadeIn(label_solutions, shift=UP)
        )
        self.wait(2)

        # --- Beat 3: Discriminant = 0 (One Real Solution) ---
        new_title = Text("Case 2: Discriminant = 0", font_size=40, color=HIGHLIGHT_BLUE).to_edge(UP)
        expr_d_eq_0_symbols = VGroup(
            Text(" = ", font_size=50, color=HIGHLIGHT_GOLD),
            Text("0", font_size=50, color=HIGHLIGHT_GOLD)
        ).arrange(RIGHT, buff=0.1)
        expr_d_eq_0 = VGroup(
            expr_d_gt_0[0].copy(), # Use copy of the discriminant part
            expr_d_eq_0_symbols
        ).arrange(RIGHT, buff=0.1).next_to(new_title, DOWN, buff=0.3)
        
        # Function and parabola for = 0 case
        parabola_eq_0 = axes.plot(func_parabola_one_root, x_range=[-3, 5], color=BLUE_ACCENT)
        root_eq_0 = Dot(axes.c2p(1, 0), color=HIGHLIGHT_GOLD)
        label_solutions_eq_0 = Text("One Real Solution (repeated)", font_size=35, color=LIGHT_TEXT).next_to(expr_d_eq_0, DOWN, buff=0.7)
        label_solutions_eq_0.align_to(expr_d_eq_0, LEFT)

        self.play(
            Transform(current_title, new_title), # Transform the title
            FadeTransform(expr_d_gt_0, expr_d_eq_0), # FadeTransform the entire expression
            Transform(parabola_obj, parabola_eq_0), # Transform parabola_obj
            FadeOut(roots_obj, shift=DOWN), # Fade out previous roots
            FadeOut(label_solutions, shift=DOWN), # Fade out previous label
            run_time=2
        )
        self.play(
            Create(root_eq_0),
            FadeIn(label_solutions_eq_0, shift=UP)
        )
        self.wait(2)

        # --- Beat 4: Discriminant < 0 (No Real Solutions) ---
        new_title = Text("Case 3: Discriminant < 0", font_size=40, color=HIGHLIGHT_BLUE).to_edge(UP)
        expr_d_lt_0_symbols = VGroup(
            Text(" < ", font_size=50, color=HIGHLIGHT_GOLD),
            Text("0", font_size=50, color=HIGHLIGHT_GOLD)
        ).arrange(RIGHT, buff=0.1)
        expr_d_lt_0 = VGroup(
            expr_d_eq_0[0].copy(),
            expr_d_lt_0_symbols
        ).arrange(RIGHT, buff=0.1).next_to(new_title, DOWN, buff=0.3)

        # Function and parabola for < 0 case
        parabola_lt_0 = axes.plot(func_parabola_no_roots, x_range=[-4, 4], color=BLUE_ACCENT)
        label_solutions_lt_0 = Text("No Real Solutions", font_size=35, color=LIGHT_TEXT).next_to(expr_d_lt_0, DOWN, buff=0.7)
        label_solutions_lt_0.align_to(expr_d_lt_0, LEFT)

        self.play(
            Transform(current_title, new_title),
            FadeTransform(expr_d_eq_0, expr_d_lt_0),
            Transform(parabola_obj, parabola_lt_0),
            FadeOut(root_eq_0, shift=DOWN),
            FadeOut(label_solutions_eq_0, shift=DOWN),
            run_time=2
        )
        self.play(FadeIn(label_solutions_lt_0, shift=UP))
        self.wait(2)

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(current_title),
            FadeOut(expr_d_lt_0),
            FadeOut(parabola_obj),
            FadeOut(label_solutions_lt_0),
            FadeOut(plane),
            FadeOut(axes),
            FadeOut(axes_labels),
            run_time=1.5
        )

        recap_title = Text("Discriminant Recap", font_size=60, color=HIGHLIGHT_BLUE).to_edge(UP)

        recap_item1 = VGroup(
            create_discriminant_expression(color=HIGHLIGHT_GOLD, font_size=40),
            Text(" > 0", font_size=40, color=HIGHLIGHT_GOLD),
            Text("  →  Two Real Solutions", font_size=35, color=LIGHT_TEXT)
        ).arrange(RIGHT, buff=0.1).next_to(recap_title, DOWN, buff=1)

        recap_item2 = VGroup(
            create_discriminant_expression(color=HIGHLIGHT_GOLD, font_size=40),
            Text(" = 0", font_size=40, color=HIGHLIGHT_GOLD),
            Text("  →  One Real Solution", font_size=35, color=LIGHT_TEXT)
        ).arrange(RIGHT, buff=0.1).next_to(recap_item1, DOWN, buff=0.5)

        recap_item3 = VGroup(
            create_discriminant_expression(color=HIGHLIGHT_GOLD, font_size=40),
            Text(" < 0", font_size=40, color=HIGHLIGHT_GOLD),
            Text("  →  No Real Solutions", font_size=35, color=LIGHT_TEXT)
        ).arrange(RIGHT, buff=0.1).next_to(recap_item2, DOWN, buff=0.5)

        # Align all recap items (specifically, align the discriminant parts)
        recap_items = VGroup(recap_item1, recap_item2, recap_item3)
        recap_items.align_to(recap_item1[0], LEFT) 

        self.play(Write(recap_title), run_time=1)
        self.wait(0.5)
        self.play(
            FadeIn(recap_item1, shift=LEFT),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            FadeIn(recap_item2, shift=LEFT),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            FadeIn(recap_item3, shift=LEFT),
            run_time=1
        )
        self.wait(3)

        # Final fade out for clean end
        self.play(FadeOut(VGroup(recap_title, recap_item1, recap_item2, recap_item3)), run_time=1)