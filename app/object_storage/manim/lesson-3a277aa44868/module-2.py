from manim import *

class CompletingTheSquareDerivation(Scene):
    def construct(self):
        # --- Configuration & Colors ---
        self.camera.background_color = "#202020" # Dark gray background

        # Custom colors for a 3Blue1Brown-inspired look
        blue_accent = BLUE_C
        gold_accent = GOLD_C
        text_color = WHITE
        highlight_gold = "#FFD700"  # Brighter gold for highlights
        highlight_blue = "#1E90FF"  # Dodger blue for secondary highlights

        # --- Beat 1: Visual Hook & Problem Statement ---
        self.beat1_hook(blue_accent, gold_accent, text_color)
        self.wait(0.5)

        # --- Beat 2: Geometric Intuition (x^2 + Bx) ---
        self.beat2_geometric_intuition(blue_accent, gold_accent, text_color)
        self.wait(0.5)

        # --- Beat 3: Algebraic Formalization (x^2 + Bx + C) ---
        self.beat3_algebraic_formalization(blue_accent, gold_accent, text_color, highlight_gold)
        self.wait(0.5)

        # --- Beat 4: General Case (ax^2 + bx + c) ---
        self.beat4_general_case(blue_accent, gold_accent, text_color, highlight_gold, highlight_blue)
        self.wait(0.5)

        # --- Beat 5: Recap ---
        self.beat5_recap(blue_accent, gold_accent, text_color)
        self.wait(2)

    def beat1_hook(self, blue_accent, gold_accent, text_color):
        title = Text("Completing the Square", font_size=50, color=text_color).to_edge(UP)
        self.play(FadeIn(title))

        # Graph a sample quadratic to show roots visually
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": GRAY_A},
            y_axis_config={"numbers_to_exclude": [0]}
        ).shift(DOWN * 0.5)
        graph_func = lambda x: x**2 + x - 2
        graph = axes.plot(graph_func, color=blue_accent)

        # Roots for x^2 + x - 2 = 0 are x=1 and x=-2
        root1 = Dot(axes.c2p(1, 0), color=gold_accent)
        root2 = Dot(axes.c2p(-2, 0), color=gold_accent)

        self.play(Create(axes), Create(graph))
        self.play(FadeIn(root1, scale=0.8), FadeIn(root2, scale=0.8))
        self.wait(1)

        problem_text = Text("How to find these points for ANY quadratic?", color=text_color, font_size=32).to_corner(UL).shift(RIGHT * 2)
        eq_general = MathTex("ax^2 + bx + c = 0", color=blue_accent, font_size=40).next_to(problem_text, DOWN * 0.8)
        self.play(Write(problem_text), Write(eq_general))
        self.wait(1)

        method_intro = Text("Introducing: Completing the Square", color=gold_accent, font_size=45).move_to(ORIGIN)
        self.play(
            FadeOut(axes, graph, root1, root2, problem_text, eq_general),
            Transform(title, Text("Completing the Square Derivation", font_size=50, color=text_color).to_edge(UP)),
            Write(method_intro)
        )
        self.wait(1.5)
        self.play(FadeOut(method_intro))


    def beat2_geometric_intuition(self, blue_accent, gold_accent, text_color):
        beat_title = Text("Geometric Intuition", color=gold_accent, font_size=35).to_edge(UL)
        self.play(Write(beat_title))

        square_side = 1.8
        rect_small_side = 0.8  # Represents B/2 for visualization
        
        # 1. x^2 square
        x_square = Square(side_length=square_side, color=blue_accent, fill_opacity=0.6).shift(LEFT * 2 + UP * 1)
        x_label_l = MathTex("x", color=text_color).next_to(x_square, LEFT, buff=0.1)
        x_label_b = MathTex("x", color=text_color).next_to(x_square, DOWN, buff=0.1)
        x2_area_tex = MathTex("x^2", color=text_color).move_to(x_square)
        
        self.play(Create(x_square), Write(x_label_l), Write(x_label_b), Write(x2_area_tex))
        self.wait(0.5)

        # 2. Add two x * (B/2) rectangles
        rect_x_bh = Rectangle(width=rect_small_side, height=square_side, color=gold_accent, fill_opacity=0.6).shift(RIGHT * 0.5 + UP * 1) # Separated for now
        rect_bh_x = Rectangle(width=square_side, height=rect_small_side, color=gold_accent, fill_opacity=0.6).shift(LEFT * 2 + DOWN * 1.5) # Separated for now

        bh_label_t = MathTex("\\frac{B}{2}", color=text_color).next_to(rect_x_bh, UP, buff=0.1)
        bh_label_l = MathTex("\\frac{B}{2}", color=text_color).next_to(rect_bh_x, LEFT, buff=0.1)
        
        self.play(
            Create(rect_x_bh), Create(rect_bh_x),
            Write(bh_label_t), Write(bh_label_l)
        )
        self.wait(0.5)

        # 3. Form the L-shape by moving rectangles next to x_square
        self.play(
            rect_x_bh.animate.next_to(x_square, RIGHT, buff=0),
            rect_bh_x.animate.next_to(x_square, DOWN, buff=0),
            bh_label_t.animate.next_to(rect_x_bh.get_top(), UP * 0.5), # Reposition labels
            bh_label_l.animate.next_to(rect_bh_x.get_left(), LEFT * 0.5)
        )
        self.wait(0.5)

        # 4. Highlight the missing corner
        missing_corner_rect = Rectangle(width=rect_small_side, height=rect_small_side, color=RED, fill_opacity=0.2, stroke_opacity=1).next_to(rect_x_bh, DOWN, buff=0).align_to(rect_bh_x, RIGHT)
        self.play(Create(missing_corner_rect))
        self.wait(0.5)

        # 5. Fill the corner: (B/2)^2
        filled_corner = Square(side_length=rect_small_side, color=blue_accent, fill_opacity=0.8).move_to(missing_corner_rect)
        corner_area_tex = MathTex("\\left(\\frac{B}{2}\\right)^2", color=text_color, font_size=28).move_to(filled_corner)
        self.play(ReplacementTransform(missing_corner_rect, filled_corner), Write(corner_area_tex))
        self.wait(1)

        # 6. Show the algebraic identity
        group_geo_parts = VGroup(x_square, rect_x_bh, rect_bh_x, filled_corner, 
                                  x_label_l, x_label_b, bh_label_t, bh_label_l, x2_area_tex, corner_area_tex)
        
        algebraic_identity = MathTex(
            "x^2", "+", "Bx", "+", "\\left(\\frac{B}{2}\\right)^2", "=", "\\left(x + \\frac{B}{2}\\right)^2",
            color=text_color, font_size=38
        ).move_to(DOWN * 2.5)

        self.play(
            FadeOut(group_geo_parts),
            Write(algebraic_identity)
        )
        self.wait(2)
        self.play(FadeOut(beat_title, algebraic_identity))


    def beat3_algebraic_formalization(self, blue_accent, gold_accent, text_color, highlight_gold):
        beat_title = Text("Algebraic Formalization", color=gold_accent, font_size=35).to_edge(UL)
        self.play(Write(beat_title))

        eq1 = MathTex("x^2", "+", "Bx", "+", "C", "=", "0", color=text_color).to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(eq1))
        self.wait(0.5)

        # Step 1: Isolate x^2 + Bx
        step1_text = Text("1. Isolate x² + Bx terms:", color=gold_accent, font_size=28).next_to(eq1, DOWN * 1.5, aligned_edge=LEFT)
        eq2 = MathTex("x^2", "+", "Bx", "=", "-C", color=text_color).next_to(step1_text, DOWN * 0.5, aligned_edge=LEFT)
        self.play(Write(step1_text), TransformMatchingTex(eq1.copy(), eq2, transform_mobject_indices={
            (0,0):0, (0,1):1, (0,2):2, (0,3):-1, (0,4):-1, (0,5):-1, (0,6):-1
        }))
        self.wait(1)

        # Step 2: Add (B/2)^2 to both sides
        step2_text = Text("2. Add (B/2)² to both sides:", color=gold_accent, font_size=28).next_to(eq2, DOWN * 1.5, aligned_edge=LEFT)
        eq3_left_parts = MathTex("x^2", "+", "Bx", "+", "\\left(\\frac{B}{2}\\right)^2", color=text_color)
        eq3_right_parts = MathTex("= -C", "+", "\\left(\\frac{B}{2}\\right)^2", color=text_color)
        eq3_full = VGroup(eq3_left_parts, eq3_right_parts).arrange(RIGHT, buff=0.1).next_to(step2_text, DOWN * 0.5, aligned_edge=LEFT)

        self.play(Write(step2_text))
        self.play(
            TransformMatchingTex(eq2.copy(), eq3_full[0], transform_mobject_indices={
                (0,0):0, (0,1):1, (0,2):2, (0,3):-1, (0,4):-1
            }),
            Write(eq3_full[0][3:]), # The "+ (B/2)^2" part on left
            FadeIn(eq3_full[1][0]), # The "=" sign
            TransformMatchingTex(eq2[4].copy(), eq3_full[1][1], transform_mobject_indices={ # -C
                (0,0):0
            }),
            Write(eq3_full[1][2:]) # The "+ (B/2)^2" part on right
        )
        self.wait(1)

        # Step 3: Factor the left side
        step3_text = Text("3. Factor the left side:", color=gold_accent, font_size=28).next_to(eq3_full, DOWN * 1.5, aligned_edge=LEFT)
        eq4 = MathTex("\\left(x + \\frac{B}{2}\\right)^2", "=", "-C", "+", "\\left(\\frac{B}{2}\\right)^2", color=text_color).next_to(step3_text, DOWN * 0.5, aligned_edge=LEFT)
        
        self.play(Write(step3_text))
        self.play(
            ReplacementTransform(eq3_full[0], eq4[0]), # x^2 + Bx + (B/2)^2 -> (x+B/2)^2
            TransformMatchingTex(eq3_full[1].copy(), VGroup(*eq4[1:])) # = -C + (B/2)^2 remains
        )
        self.wait(1.5)
        
        # Highlight the completed square form
        final_form_brace = Brace(eq4, DOWN, color=highlight_gold)
        final_form_text = final_form_brace.get_text("The Completed Square Form!", color=highlight_gold, font_size=30)
        self.play(Create(final_form_brace), Write(final_form_text))
        self.wait(1)

        self.play(FadeOut(beat_title, eq1, step1_text, eq2, step2_text, eq3_full, step3_text, eq4, final_form_brace, final_form_text))


    def beat4_general_case(self, blue_accent, gold_accent, text_color, highlight_gold, highlight_blue):
        beat_title = Text("General Case: ax² + bx + c = 0", color=gold_accent, font_size=35).to_edge(UL)
        self.play(Write(beat_title))

        eq_general_orig = MathTex("ax^2", "+", "bx", "+", "c", "=", "0", color=text_color).to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(eq_general_orig))
        self.wait(0.5)

        # Step 1: Divide by 'a'
        step1_text = Text("1. Divide by 'a' (if a ≠ 1):", color=gold_accent, font_size=28).next_to(eq_general_orig, DOWN * 1.5, aligned_edge=LEFT)
        eq_div_a = MathTex("x^2", "+", "\\frac{b}{a}x", "+", "\\frac{c}{a}", "=", "0", color=text_color).next_to(step1_text, DOWN * 0.5, aligned_edge=LEFT)
        
        self.play(Write(step1_text))
        self.play(TransformMatchingTex(eq_general_orig.copy(), eq_div_a))
        self.wait(1)

        # Step 2: Identify B and C, then apply previous steps
        step2_text = Text("2. Apply Completing the Square method:", color=gold_accent, font_size=28).next_to(eq_div_a, DOWN * 1.5, aligned_edge=LEFT)
        self.play(Write(step2_text))
        self.wait(0.5)

        # Show B and C mapping
        B_term = MathTex("B", "=", "\\frac{b}{a}", color=highlight_gold).next_to(step2_text, DOWN * 0.5, aligned_edge=LEFT).shift(RIGHT * 1)
        C_term = MathTex("C", "=", "\\frac{c}{a}", color=highlight_blue).next_to(B_term, DOWN * 0.5, aligned_edge=LEFT)
        self.play(
            eq_div_a[2].animate.set_color(highlight_gold),
            eq_div_a[4].animate.set_color(highlight_blue),
            Write(B_term), Write(C_term)
        )
        self.wait(1)
        
        # Apply the transformation (condensed)
        eq_final_form_general = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2", "=", 
            "-\\frac{c}{a}", "+", "\\left(\\frac{b}{2a}\\right)^2",
            color=text_color
        ).next_to(C_term, DOWN * 1.5, aligned_edge=LEFT).shift(LEFT * 1)

        # Animating from parts of eq_div_a and writing new parts
        self.play(
            ReplacementTransform(eq_div_a[0].copy(), eq_final_form_general[0][0]), # x^2 -> part of (x + b/2a)^2
            ReplacementTransform(eq_div_a[2].copy(), eq_final_form_general[0][2]), # b/a x -> part of (x + b/2a)^2
            ReplacementTransform(eq_div_a[4].copy(), eq_final_form_general[2]), # c/a -> -c/a
            Write(VGroup(*eq_final_form_general[0][1].get_submobjects(), *eq_final_form_general[0][3:].get_submobjects())), # Remaining parts of (x + b/2a)^2
            Write(eq_final_form_general[1]), # =
            Write(VGroup(eq_final_form_general[3], eq_final_form_general[4])) # + (b/2a)^2
        )
        self.wait(1.5)

        final_eq_simplified = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2", "=", "\\frac{b^2 - 4ac}{4a^2}",
            color=text_color
        ).move_to(eq_final_form_general)

        self.play(TransformMatchingTex(eq_final_form_general, final_eq_simplified))
        self.wait(1.5)
        
        self.play(FadeOut(beat_title, eq_general_orig, step1_text, eq_div_a, step2_text, B_term, C_term, final_eq_simplified))


    def beat5_recap(self, blue_accent, gold_accent, text_color):
        recap_title = Text("Recap: Completing the Square", color=gold_accent, font_size=40).to_edge(UP)
        self.play(Write(recap_title))

        # Each recap point is a VGroup of a Text and a MathTex
        # Arrange them horizontally first, then stack these VGroups vertically
        steps_group = VGroup(
            VGroup(
                Text("1. Visualize & Identity:", color=text_color, font_size=28),
                MathTex("x^2 + Bx + \\left(\\frac{B}{2}\\right)^2 = \\left(x + \\frac{B}{2}\\right)^2", color=blue_accent, font_size=28)
            ).arrange(RIGHT, aligned_edge=LEFT, buff=0.2),

            VGroup(
                Text("2. Isolate variable terms:", color=text_color, font_size=28),
                MathTex("ax^2 + bx = -c", color=blue_accent, font_size=28)
            ).arrange(RIGHT, aligned_edge=LEFT, buff=0.2),

            VGroup(
                Text("3. Normalize (divide by 'a') & Add (B/2)²:", color=text_color, font_size=28),
                MathTex("x^2 + \\frac{b}{a}x + \\left(\\frac{b}{2a}\\right)^2 = \\ldots", color=blue_accent, font_size=28)
            ).arrange(RIGHT, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("4. Factor the perfect square:", color=text_color, font_size=28),
                MathTex("\\left(x + \\frac{b}{2a}\\right)^2 = \\text{Constant}", color=blue_accent, font_size=28)
            ).arrange(RIGHT, aligned_edge=LEFT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8).shift(UP*0.5)

        # Align the text part of each point to the left of the entire group
        for sub_group in steps_group:
            sub_group[0].align_to(steps_group[0][0], LEFT)

        self.play(LaggedStart(*[FadeIn(step, shift=UP*0.5) for step in steps_group], lag_ratio=0.3))
        self.wait(3)
        self.play(FadeOut(recap_title, steps_group))