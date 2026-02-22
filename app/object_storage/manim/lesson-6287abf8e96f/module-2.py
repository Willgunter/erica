from manim import *

class CompletingTheSquareDerivation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E
        RED_ACCENT = RED_E

        # --- Title Card (Opening Hook) ---
        title = Text("Completing the Square Derivation", font_size=50, color=GOLD_ACCENT)
        underline = Line(LEFT * 4, RIGHT * 4, color=BLUE_ACCENT).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), Create(underline))
        self.wait(1.5)
        self.play(FadeOut(title, shift=UP), FadeOut(underline, shift=DOWN))
        self.wait(0.5)

        # --- Beat 1: The Problem - x^2 + bx ---
        problem_statement = MathTex("x^2 + bx", color=WHITE)
        problem_statement.to_edge(UP, buff=0.5)
        self.play(Write(problem_statement))
        self.wait(0.5)

        # Visualizing x^2
        x_side_length = 2.5
        x_square = Square(side_length=x_side_length, color=BLUE_ACCENT, fill_opacity=0.5)
        x_square.move_to(LEFT * 2.5 + UP * 0.5)
        
        x_label_h = MathTex("x", color=BLUE_ACCENT).next_to(x_square.get_left(), LEFT, buff=0.1)
        x_label_v = MathTex("x", color=BLUE_ACCENT).next_to(x_square.get_bottom(), DOWN, buff=0.1)
        
        self.play(Create(x_square), Write(x_label_h), Write(x_label_v))
        self.wait(0.5)

        # Visualizing bx
        b_width_val = 1.0 # This represents 'b' in the expression (for bx rectangle)
        b_rect_original = Rectangle(width=b_width_val, height=x_side_length, color=GOLD_ACCENT, fill_opacity=0.5)
        b_rect_original.next_to(x_square, RIGHT, buff=0)
        
        b_label_original = MathTex("b", color=GOLD_ACCENT).next_to(b_rect_original.get_top(), UP, buff=0.1)
        
        self.play(Create(b_rect_original), Write(b_label_original))
        self.wait(1)

        current_area_label = MathTex("\\text{Area: } x^2 + bx", color=WHITE).next_to(x_square, DOWN, buff=1.5).shift(RIGHT*1)
        self.play(Write(current_area_label))
        self.wait(1.5)
        self.play(FadeOut(problem_statement), FadeOut(current_area_label, shift=DOWN))

        # --- Beat 2: Reshaping - Cutting and Rearranging ---
        self.play(
            VGroup(x_square, x_label_h, x_label_v, b_rect_original, b_label_original).animate.shift(LEFT * 1.5)
        )
        
        # Split b_rect_original into two b/2 pieces
        b_half_width_val = b_width_val / 2
        
        rect_right_piece = Rectangle(width=b_half_width_val, height=x_side_length, color=GOLD_ACCENT, fill_opacity=0.5)
        rect_right_piece.next_to(x_square, RIGHT, buff=0)
        
        rect_bottom_piece = Rectangle(width=x_side_length, height=b_half_width_val, color=GOLD_ACCENT, fill_opacity=0.5)
        rect_bottom_piece.next_to(x_square, DOWN, buff=0)
        rect_bottom_piece.align_to(x_square, LEFT) # Align left edges

        b_half_label_top = MathTex("\\frac{b}{2}", color=GOLD_ACCENT).next_to(rect_right_piece.get_top(), UP, buff=0.1)
        b_half_label_side = MathTex("\\frac{b}{2}", color=GOLD_ACCENT).next_to(rect_bottom_piece.get_left(), LEFT, buff=0.1)

        self.play(
            Transform(b_rect_original, rect_right_piece),
            Transform(b_label_original, b_half_label_top),
            Create(rect_bottom_piece),
            Create(b_half_label_side),
        )
        self.wait(1.5)

        # Highlight the missing corner
        missing_corner_square = Square(side_length=b_half_width_val, color=RED_ACCENT, stroke_opacity=0.8, fill_opacity=0)
        # Position using rect_right_piece and rect_bottom_piece
        missing_corner_square.next_to(rect_right_piece, DOWN, buff=0)
        missing_corner_square.align_to(rect_bottom_piece, RIGHT)
        
        self.play(Create(missing_corner_square))
        self.wait(1)

        # --- Beat 3: Completing the Square - Adding (b/2)^2 ---
        missing_area_tex = MathTex("\\left(\\frac{b}{2}\\right)^2", color=RED_ACCENT).move_to(missing_corner_square.get_center())
        self.play(Write(missing_area_tex))
        self.wait(0.5)

        completed_square_fill = Square(side_length=b_half_width_val, color=GOLD_ACCENT, fill_opacity=0.7)
        completed_square_fill.move_to(missing_corner_square.get_center())
        
        self.play(Transform(missing_corner_square, completed_square_fill), FadeOut(missing_area_tex))
        self.wait(1)

        # Show the new total square's dimensions
        x_plus_b_half_h = MathTex("x + \\frac{b}{2}", color=WHITE).next_to(rect_right_piece.get_right(), RIGHT, buff=0.2)
        x_plus_b_half_v = MathTex("x + \\frac{b}{2}", color=WHITE).next_to(rect_bottom_piece.get_bottom(), DOWN, buff=0.2)
        
        # Adjust position slightly for better visual alignment
        x_plus_b_half_h.set_x(x_square.get_x() + x_side_length/2 + b_half_width_val/2 + 0.3)
        x_plus_b_half_h.set_y(x_square.get_y() + x_side_length/2 + 0.5)
        x_plus_b_half_v.set_x(x_square.get_x() - x_side_length/2 - 0.5)
        x_plus_b_half_v.set_y(x_square.get_y() - x_side_length/2 - b_half_width_val/2 - 0.3)
        
        self.play(
            FadeOut(x_label_h), FadeOut(x_label_v), FadeOut(b_half_label_top), FadeOut(b_half_label_side),
            Write(x_plus_b_half_h), Write(x_plus_b_half_v)
        )
        self.wait(1.5)
        
        # --- Beat 4: Formalizing the Algebra ---
        self.play(FadeOut(VGroup(x_square, b_rect_original, rect_bottom_piece, completed_square_fill)),
                  FadeOut(x_plus_b_half_h), FadeOut(x_plus_b_half_v))
        self.wait(0.5)

        algebraic_form_orig = MathTex("x^2 + bx", color=WHITE)
        algebraic_form_orig.to_edge(UP, buff=0.5)
        self.play(Write(algebraic_form_orig))
        self.wait(0.5)
        
        algebraic_form_completed = MathTex("x^2 + bx + ", "\\left(\\frac{b}{2}\\right)^2", "=", "\\left(x + \\frac{b}{2}\\right)^2", color=WHITE)
        algebraic_form_completed.to_edge(UP, buff=0.5)

        self.play(
            TransformMatchingTex(algebraic_form_orig, algebraic_form_completed[0]), # x^2 + bx part
            FadeIn(algebraic_form_completed[1], shift=UP), # (b/2)^2
            FadeIn(algebraic_form_completed[2], shift=UP), # =
            FadeIn(algebraic_form_completed[3], shift=UP), # (x + b/2)^2
        )
        self.wait(2.5)

        # --- Beat 5: Application - Solving ax^2 + bx + c = 0 ---
        quadratic_eq_start = MathTex("ax^2 + bx + c = 0", color=WHITE)
        quadratic_eq_start.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(algebraic_form_completed, quadratic_eq_start))
        self.wait(1)

        # Divide by a
        step_divide_a = MathTex("x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0", color=WHITE)
        step_divide_a.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(quadratic_eq_start, step_divide_a))
        self.wait(1)

        # Move c/a to RHS
        step_move_c = MathTex("x^2 + \\frac{b}{a}x = -\\frac{c}{a}", color=WHITE)
        step_move_c.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(step_divide_a, step_move_c))
        self.wait(1.5)

        # Add (b/2a)^2 to both sides
        b_over_a_coeff = MathTex("\\frac{b}{a}", color=GOLD_ACCENT).next_to(step_move_c[1], DOWN, buff=0.5)
        is_our_b = Text("Our 'b' for completing the square", font_size=25, color=GOLD_ACCENT).next_to(b_over_a_coeff, RIGHT, buff=0.2)
        self.play(Write(b_over_a_coeff), Write(is_our_b))
        self.wait(1)
        self.play(FadeOut(VGroup(b_over_a_coeff, is_our_b)))

        add_term = MathTex("+\\left(\\frac{b}{2a}\\right)^2", color=BLUE_ACCENT)
        
        step_add_term = MathTex("x^2 + \\frac{b}{a}x", add_term, "=", "-\\frac{c}{a}", add_term, color=WHITE)
        step_add_term.arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.5)

        self.play(TransformMatchingTex(step_move_c, step_add_term[0:4], transform_mismatches=True))
        self.play(FadeIn(step_add_term[1]), FadeIn(step_add_term[4]))
        self.wait(1.5)

        # Factor LHS
        step_factor = MathTex("\\left(x + \\frac{b}{2a}\\right)^2 = -\\frac{c}{a} + \\left(\\frac{b}{2a}\\right)^2", color=WHITE)
        step_factor.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(step_add_term, step_factor))
        self.wait(2)

        # Indicate next steps (solve for x)
        next_steps_text = Text("Now, take the square root of both sides", font_size=35, color=GOLD_ACCENT).next_to(step_factor, DOWN, buff=0.8)
        then_solve_text = Text("and solve for 'x' to find the quadratic formula!", font_size=35, color=GOLD_ACCENT).next_to(next_steps_text, DOWN, buff=0.3)
        
        self.play(FadeIn(next_steps_text, shift=UP))
        self.play(FadeIn(then_solve_text, shift=UP))
        self.wait(3)
        self.play(FadeOut(VGroup(next_steps_text, then_solve_text)))

        # --- Recap Card ---
        self.play(FadeOut(step_factor))
        
        recap_title = Text("Recap: Completing the Square", font_size=40, color=GOLD_ACCENT)
        recap_title.to_edge(UP, buff=0.5)
        
        recap_eq1 = MathTex("1. \\text{ Goal: Transform } x^2 + bx \\text{ into a perfect square}", color=WHITE)
        recap_eq2 = MathTex("2. \\text{ This is done by adding } \\left(\\frac{b}{2}\\right)^2", color=BLUE_ACCENT)
        recap_eq3 = MathTex("3. \\text{ Result: } x^2 + bx + \\left(\\frac{b}{2}\\right)^2 = \\left(x + \\frac{b}{2}\\right)^2", color=GOLD_ACCENT)
        recap_eq4 = MathTex("4. \\text{ Applied to solve } ax^2 + bx + c = 0", color=WHITE)

        recap_group = VGroup(recap_eq1, recap_eq2, recap_eq3, recap_eq4).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        recap_group.next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(eq, shift=UP) for eq in recap_group], lag_ratio=0.7))
        self.wait(4)
        self.play(FadeOut(VGroup(recap_title, recap_group)))
        
        # --- Final Message ---
        final_message = Text("Mastering the foundations leads to deeper understanding!", font_size=40, color=BLUE_ACCENT)
        self.play(Write(final_message))
        self.wait(2.5)
        self.play(FadeOut(final_message))