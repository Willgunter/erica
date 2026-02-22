from manim import *

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # 0. Setup and Initial Hook
        self.camera.background_color = BLACK
        self.set_up_colors()
        self.intro_hook()

        # 1. Beat 1: Visualizing x^2 + bx
        self.visualize_x_squared_plus_bx()

        # 2. Beat 2: Completing the Square
        self.complete_the_square()

        # 3. Beat 3: Isolating x (for a=1 case)
        self.isolate_x_a_equals_1()

        # 4. Beat 4: Generalizing and Final Formula
        self.generalize_to_full_formula()

        # 5. Recap
        self.recap_card()

    def set_up_colors(self):
        self.blue_color = BLUE_E
        self.gold_color = GOLD_E
        self.text_color = WHITE

    def create_exponent_text(self, base_text_str, exp_str, color=WHITE):
        base = Text(base_text_str, color=color)
        exp = Text(exp_str, color=color).scale(0.5).move_to(base.get_corner(UR) + 0.1 * UR)
        return VGroup(base, exp)

    def create_fraction_text(self, numerator_str, denominator_str, line_length=0.8, color=WHITE):
        num = Text(numerator_str, color=color)
        den = Text(denominator_str, color=color)
        line = Line(LEFT * line_length / 2, RIGHT * line_length / 2, color=color)
        
        # Position numerator and denominator relative to the line's center
        num.next_to(line.get_center(), UP, buff=0.1)
        den.next_to(line.get_center(), DOWN, buff=0.1)
        
        return VGroup(num, line, den)

    def create_sqrt_text(self, content_vgroup, color=WHITE):
        # This is a highly simplified sqrt representation.
        # It approximates a square root visually.
        sqrt_sym = Text("sqrt", color=color).scale(0.8)
        open_paren = Text("(", color=color).next_to(sqrt_sym, RIGHT, buff=0.05)
        content_vgroup_centered = content_vgroup.copy().next_to(open_paren, RIGHT, buff=0.05)
        close_paren = Text(")", color=color).next_to(content_vgroup_centered, RIGHT, buff=0.05)
        return VGroup(sqrt_sym, open_paren, content_vgroup_centered, close_paren)

    def intro_hook(self):
        title = Text("Unlocking Formula Derivation", color=self.text_color).scale(1.2)
        subtitle = Text("The Quadratic Formula", color=self.gold_color).next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title, shift=UP), FadeOut(subtitle, shift=UP))

        # Visual hook: A dynamic area changing
        square_x = Square(side_length=2, color=self.blue_color, fill_opacity=0.6)
        label_x = Text("x", color=self.text_color).next_to(square_x.get_bottom(), DOWN, buff=0.1)
        label_x2 = self.create_exponent_text("x", "2", color=self.text_color).move_to(square_x.get_center())

        self.play(Create(square_x), FadeIn(label_x))
        self.play(Transform(label_x, label_x2))
        self.wait(0.5)

        rect_width = 1.5
        rect_height = 2
        rectangle = Rectangle(width=rect_width, height=rect_height, color=self.gold_color, fill_opacity=0.6)
        label_area_rect = Text("Area", color=self.text_color).move_to(rectangle.get_center())

        self.play(
            FadeOut(label_x),
            Transform(square_x, rectangle.next_to(ORIGIN, LEFT, buff=1)),
            FadeTransform(label_x2, label_area_rect.next_to(rectangle.get_center(), UP, buff=0.2))
        )
        self.wait(1)
        self.play(FadeOut(rectangle), FadeOut(label_area_rect))

    def visualize_x_squared_plus_bx(self):
        title = Text("1. Visualizing", color=self.gold_color).to_edge(UP + LEFT)
        concept_exp = self.create_exponent_text("x", "2", color=self.blue_color)
        plus_txt = Text("+", color=self.text_color)
        b_x_txt = VGroup(Text("b", color=self.gold_color), Text("x", color=self.blue_color)).arrange(RIGHT, buff=0.05)
        
        full_concept_text = VGroup(concept_exp, plus_txt, b_x_txt).arrange(RIGHT, buff=0.2).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        
        self.play(FadeIn(title, shift=UP))
        self.play(Write(full_concept_text))
        self.wait(0.5)

        # Geometric representation
        x_len = 2.0
        b_half_len = 0.8 # Represents b/2
        
        # Square x^2
        square_x = Square(side_length=x_len, color=self.blue_color, fill_opacity=0.6).shift(LEFT * 2)
        label_x_side_h = Text("x", color=self.text_color).next_to(square_x.get_left(), LEFT, buff=0.1)
        label_x_side_w = Text("x", color=self.text_color).next_to(square_x.get_bottom(), DOWN, buff=0.1)
        label_x_squared = self.create_exponent_text("x", "2", color=self.text_color).move_to(square_x.get_center())

        self.play(Create(square_x), FadeIn(label_x_side_h), FadeIn(label_x_side_w))
        self.play(FadeTransform(VGroup(label_x_side_h, label_x_side_w), label_x_squared))
        self.wait(0.5)

        # Rectangles bx/2
        rect_bx_half_1 = Rectangle(width=b_half_len, height=x_len, color=self.gold_color, fill_opacity=0.6).next_to(square_x, RIGHT, buff=0)
        rect_bx_half_2 = Rectangle(width=x_len, height=b_half_len, color=self.gold_color, fill_opacity=0.6).next_to(square_x, UP, buff=0)

        label_b_half = self.create_fraction_text("b", "2", color=self.text_color).next_to(rect_bx_half_1.get_right(), RIGHT, buff=0.1)
        label_x_for_rect1 = Text("x", color=self.text_color).next_to(rect_bx_half_1.get_bottom(), DOWN, buff=0.1)
        label_b_half_2 = self.create_fraction_text("b", "2", color=self.text_color).next_to(rect_bx_half_2.get_top(), UP, buff=0.1)
        label_x_for_rect2 = Text("x", color=self.text_color).next_to(rect_bx_half_2.get_left(), LEFT, buff=0.1)
        
        bx_half_text_1_simple = VGroup(Text("b", color=self.text_color), Text("x", color=self.text_color)).arrange(RIGHT, buff=0.05).move_to(rect_bx_half_1.get_center()).scale(0.8)
        bx_half_text_2_simple = VGroup(Text("b", color=self.text_color), Text("x", color=self.text_color)).arrange(RIGHT, buff=0.05).move_to(rect_bx_half_2.get_center()).scale(0.8)
        
        self.play(
            Create(rect_bx_half_1), Create(rect_bx_half_2),
            FadeIn(label_b_half), FadeIn(label_x_for_rect1),
            FadeIn(label_b_half_2), FadeIn(label_x_for_rect2)
        )
        self.wait(0.5)

        self.play(
            FadeOut(label_b_half), FadeOut(label_x_for_rect1),
            FadeOut(label_b_half_2), FadeOut(label_x_for_rect2),
            FadeIn(bx_half_text_1_simple), FadeIn(bx_half_text_2_simple)
        )
        self.wait(1)

        total_area_text_p1 = VGroup(
            label_x_squared.copy().move_to(ORIGIN).align_to(full_concept_text, LEFT).shift(DOWN*0.5),
            Text("+", color=self.text_color).next_to(label_x_squared.copy(), RIGHT, buff=0.2),
            VGroup(Text("b", color=self.gold_color), Text("x", color=self.blue_color)).arrange(RIGHT, buff=0.05).next_to(Text("+", color=self.text_color), RIGHT, buff=0.2)
        ).move_to(ORIGIN).to_edge(RIGHT, buff=1)

        self.play(
            label_x_squared.animate.scale(0.8).move_to(total_area_text_p1[0].get_center()),
            bx_half_text_1_simple.animate.scale(0.8).move_to(total_area_text_p1[2].get_center()).shift(LEFT * 0.2),
            bx_half_text_2_simple.animate.set_opacity(0),
            FadeIn(total_area_text_p1[1]),
            FadeIn(total_area_text_p1[2])
        )
        self.wait(1)
        self.play(FadeOut(full_concept_text), FadeOut(title))
        self.play(
            FadeOut(square_x), FadeOut(rect_bx_half_1), FadeOut(rect_bx_half_2),
            FadeOut(label_x_squared), FadeOut(bx_half_text_1_simple), FadeOut(bx_half_text_2_simple),
            FadeOut(total_area_text_p1)
        )

    def complete_the_square(self):
        title = Text("2. Completing the Square", color=self.gold_color).to_edge(UP + LEFT)
        self.play(FadeIn(title, shift=UP))

        x_len = 2.0
        b_half_len = 0.8 # Represents b/2

        # Recreate the initial shape (x^2 + bx)
        square_x = Square(side_length=x_len, color=self.blue_color, fill_opacity=0.6).shift(LEFT * 2)
        rect_bx_half_1 = Rectangle(width=b_half_len, height=x_len, color=self.gold_color, fill_opacity=0.6).next_to(square_x, RIGHT, buff=0)
        rect_bx_half_2 = Rectangle(width=x_len, height=b_half_len, color=self.gold_color, fill_opacity=0.6).next_to(square_x, UP, buff=0)

        total_shape = VGroup(square_x, rect_bx_half_1, rect_bx_half_2)
        self.play(Create(total_shape))
        self.wait(0.5)

        # Show the missing piece
        missing_square = Square(side_length=b_half_len, color=self.blue_color, fill_opacity=0.3, stroke_opacity=0.8).next_to(rect_bx_half_1, UP, buff=0).next_to(rect_bx_half_2, RIGHT, buff=0)
        
        label_b_half_side = self.create_fraction_text("b", "2", color=self.text_color).next_to(missing_square.get_right(), RIGHT, buff=0.1)
        label_b_half_side_2 = self.create_fraction_text("b", "2", color=self.text_color).next_to(missing_square.get_top(), UP, buff=0.1)

        self.play(Create(missing_square), FadeIn(label_b_half_side), FadeIn(label_b_half_side_2))
        self.wait(1)

        # Label the area of the missing piece: (b/2)^2
        b_half_squared_frac = self.create_fraction_text("b", "2", color=self.text_color, line_length=0.5)
        b_half_squared_exp = Text("2", color=self.text_color).scale(0.5).next_to(b_half_squared_frac.get_corner(UR), UP + RIGHT, buff=0.05)
        b_half_squared_vgroup = VGroup(b_half_squared_frac, b_half_squared_exp).move_to(missing_square.get_center()).scale(0.7)

        self.play(
            FadeOut(label_b_half_side), FadeOut(label_b_half_side_2),
            FadeIn(b_half_squared_vgroup)
        )
        self.wait(0.5)

        # Form the complete square visually
        complete_square_label_x_plus_b_half = VGroup(
            Text("(", color=self.text_color),
            Text("x", color=self.blue_color),
            Text("+", color=self.text_color),
            self.create_fraction_text("b", "2", color=self.gold_color, line_length=0.5),
            Text(")", color=self.text_color)
        ).arrange(RIGHT, buff=0.1).next_to(total_shape.get_bottom(), DOWN, buff=0.3)

        complete_square_label_exp = Text("2", color=self.text_color).scale(0.5).next_to(complete_square_label_x_plus_b_half.get_corner(UR), UP + RIGHT, buff=0.05)
        
        # Construct the equation: x^2 + bx + (b/2)^2 = (x + b/2)^2
        # Left side
        left_side_x2 = self.create_exponent_text("x", "2", color=self.blue_color)
        left_side_bx = VGroup(Text("b", color=self.gold_color), Text("x", color=self.blue_color)).arrange(RIGHT, buff=0.05)
        left_side_b_half_sq = b_half_squared_vgroup.copy()
        
        total_left_side_eq = VGroup(
            left_side_x2,
            Text("+", color=self.text_color),
            left_side_bx,
            Text("+", color=self.text_color),
            left_side_b_half_sq
        ).arrange(RIGHT, buff=0.1).to_edge(RIGHT, buff=0.5)

        equal_sign = Text("=", color=self.text_color).next_to(total_left_side_eq, RIGHT, buff=0.2)
        
        # Right side
        total_right_side_eq = VGroup(
            complete_square_label_x_plus_b_half.copy(),
            complete_square_label_exp.copy()
        ).arrange(RIGHT, buff=0.05).next_to(equal_sign, RIGHT, buff=0.2)

        equation = VGroup(total_left_side_eq, equal_sign, total_right_side_eq).center().shift(UP*1.5)

        self.play(FadeIn(complete_square_label_x_plus_b_half), FadeIn(complete_square_label_exp))
        self.play(
            LaggedStart(
                FadeIn(total_left_side_eq[0]),FadeIn(total_left_side_eq[1]),FadeIn(total_left_side_eq[2]),
                FadeIn(total_left_side_eq[3]),FadeIn(total_left_side_eq[4]),
                lag_ratio=0.2
            )
        )
        self.play(Write(equal_sign))
        self.play(FadeIn(total_right_side_eq))
        self.wait(1)
        
        self.play(
            FadeOut(title),
            FadeOut(complete_square_label_x_plus_b_half), FadeOut(complete_square_label_exp),
            FadeOut(b_half_squared_vgroup),
            total_shape.animate.scale(0.8).shift(LEFT * 2) # Move for next beat
        )
        self.play(equation.animate.to_edge(UP, buff=0.5).scale(0.8)) # Keep equation for reference

        self.equation_ref = equation # Store for next beat
        self.complete_square_ref = total_shape # Store for next beat (though faded)

    def isolate_x_a_equals_1(self):
        title = Text("3. Isolating 'x'", color=self.gold_color).to_edge(UP + LEFT)
        self.play(FadeIn(title, shift=UP))

        equation_from_prev = self.equation_ref.copy()
        self.play(FadeIn(equation_from_prev))
        self.wait(0.5)

        # Introduce '= 0' and subtract 'c'
        zero_text = Text("= 0", color=self.text_color).next_to(equation_from_prev, RIGHT, buff=0.2)
        self.play(Write(zero_text))
        self.wait(0.5)

        # Rearrange from x^2 + bx + (b/2)^2 = -c + (b/2)^2
        # To: (x + b/2)^2 = (b/2)^2 - c
        
        term_x_plus_b_half_squared = VGroup(
            Text("(", color=self.text_color),
            Text("x", color=self.blue_color),
            Text("+", color=self.text_color),
            self.create_fraction_text("b", "2", color=self.gold_color, line_length=0.5),
            Text(")", color=self.text_color),
            Text("2", color=self.text_color).scale(0.5).shift(UP * 0.2 + RIGHT * 0.1)
        ).arrange(RIGHT, buff=0.1).to_edge(LEFT, buff=1).shift(UP*1)

        eq_sign_2 = Text("=", color=self.text_color).next_to(term_x_plus_b_half_squared, RIGHT, buff=0.2)

        b_half_squared_frac = self.create_fraction_text("b", "2", color=self.gold_color, line_length=0.5)
        b_half_squared_exp = Text("2", color=self.text_color).scale(0.5).next_to(b_half_squared_frac.get_corner(UR), UP + RIGHT, buff=0.05)
        b_half_squared_term_vgroup = VGroup(b_half_squared_frac, b_half_squared_exp).arrange(RIGHT, buff=0.05)

        c_term_minus = VGroup(Text("-", color=self.text_color), Text("c", color=self.text_color)).arrange(RIGHT, buff=0.05)
        
        right_side_eq_2 = VGroup(b_half_squared_term_vgroup, c_term_minus).arrange(RIGHT, buff=0.1).next_to(eq_sign_2, RIGHT, buff=0.2)
        
        full_eq_step_1 = VGroup(term_x_plus_b_half_squared, eq_sign_2, right_side_eq_2).center().shift(UP*0.5)

        self.play(
            FadeOut(equation_from_prev),
            FadeOut(zero_text),
            FadeOut(self.complete_square_ref) # Clear the geometric shapes
        )
        self.play(FadeIn(full_eq_step_1))
        self.wait(1)

        # Take square root of both sides
        plus_minus = Text("+/-", color=self.text_color)
        
        sqrt_content_vgroup = VGroup(b_half_squared_term_vgroup.copy(), c_term_minus.copy()).arrange(RIGHT, buff=0.1)
        sqrt_right_side = self.create_sqrt_text(sqrt_content_vgroup, color=self.text_color)
        sqrt_right_side.next_to(plus_minus, RIGHT, buff=0.1)

        # Left side: x + b/2
        left_side_no_exp = VGroup(term_x_plus_b_half_squared[0], term_x_plus_b_half_squared[1], term_x_plus_b_half_squared[2], term_x_plus_b_half_squared[3], term_x_plus_b_half_squared[4]).copy()
        
        equation_sqrt_step = VGroup(left_side_no_exp, Text("=", color=self.text_color), plus_minus, sqrt_right_side).arrange(RIGHT, buff=0.2).center().shift(DOWN*0.5)

        self.play(ReplacementTransform(full_eq_step_1, equation_sqrt_step))
        self.wait(1)
        
        # Isolate x
        minus_b_half = self.create_fraction_text("-b", "2", color=self.gold_color, line_length=0.5)
        
        final_x_a1 = VGroup(
            Text("x", color=self.blue_color),
            Text("=", color=self.text_color),
            minus_b_half,
            equation_sqrt_step[2].copy(), # +/-
            equation_sqrt_step[3].copy()  # sqrt term
        ).arrange(RIGHT, buff=0.2).center().shift(DOWN*1.5)

        self.play(ReplacementTransform(equation_sqrt_step, final_x_a1))
        self.wait(1.5)

        self.play(FadeOut(title))
        self.final_x_a1_ref = final_x_a1 # Store for next beat

    def generalize_to_full_formula(self):
        title = Text("4. Generalizing and Final Formula", color=self.gold_color).to_edge(UP + LEFT)
        self.play(FadeIn(title, shift=UP))

        # Start with the a=1 formula
        a1_formula = self.final_x_a1_ref.copy().to_edge(UP, buff=0.5)
        self.play(FadeIn(a1_formula))
        self.wait(0.5)

        # The full quadratic equation: ax^2 + bx + c = 0
        general_eq_text = VGroup(
            Text("a", color=self.gold_color), self.create_exponent_text("x", "2", color=self.blue_color),
            Text("+", color=self.text_color),
            Text("b", color=self.gold_color), Text("x", color=self.blue_color),
            Text("+", color=self.text_color),
            Text("c", color=self.text_color),
            Text("=", color=self.text_color),
            Text("0", color=self.text_color)
        ).arrange(RIGHT, buff=0.1).center().shift(UP*1.5)
        
        self.play(Write(general_eq_text))
        self.wait(1)
        
        # Explain the transformation to the general formula
        transformation_text = Text("Adjust coefficients for 'a'", color=self.text_color).next_to(general_eq_text, DOWN, buff=0.5)
        self.play(Write(transformation_text))
        self.wait(0.5)

        # Construct the full quadratic formula directly (due to no Tex constraint for complex intermediate steps)
        # x = (-b +/- sqrt(b^2 - 4ac)) / (2a)
        
        num_minus_b = Text("-b", color=self.gold_color)
        num_plus_minus = Text("+/-", color=self.text_color)
        
        b_squared = self.create_exponent_text("b", "2", color=self.gold_color)
        minus_4ac_group = VGroup(Text("-", color=self.text_color), Text("4", color=self.text_color), Text("a", color=self.gold_color), Text("c", color=self.text_color)).arrange(RIGHT, buff=0.05)
        
        discriminant_content = VGroup(b_squared, minus_4ac_group).arrange(RIGHT, buff=0.1)
        
        sqrt_discriminant = self.create_sqrt_text(discriminant_content, color=self.text_color)
        
        numerator_vgroup = VGroup(num_minus_b, num_plus_minus, sqrt_discriminant).arrange(RIGHT, buff=0.1)
        
        denominator_vgroup = VGroup(Text("2", color=self.text_color), Text("a", color=self.gold_color)).arrange(RIGHT, buff=0.05)
        
        final_formula_line = Line(LEFT, RIGHT, color=self.text_color).set_width(numerator_vgroup.get_width() * 1.2)
        
        final_formula_display = VGroup(
            Text("x", color=self.blue_color),
            Text("=", color=self.text_color),
            VGroup(
                numerator_vgroup.copy().next_to(final_formula_line, UP, buff=0.2),
                final_formula_line,
                denominator_vgroup.copy().next_to(final_formula_line, DOWN, buff=0.2)
            )
        ).arrange(RIGHT, buff=0.2).center().shift(DOWN*0.5).scale(0.9)


        self.play(
            FadeOut(general_eq_text), FadeOut(transformation_text), FadeOut(title),
            ReplacementTransform(a1_formula, final_formula_display)
        )
        self.wait(2)

    def recap_card(self):
        self.play(FadeOut(self.mobjects)) # Clear everything

        recap_title = Text("Recap: Formula Derivation Steps", color=self.gold_color).to_edge(UP)
        
        step1 = Text("1. Visualize (x^2 + bx) as areas.", color=self.text_color).next_to(recap_title, DOWN, buff=0.8).align_to(recap_title, LEFT).shift(RIGHT*0.5)
        step2 = Text("2. Complete the square geometrically.", color=self.text_color).next_to(step1, DOWN, buff=0.4).align_to(step1, LEFT)
        step3 = Text("3. Isolate 'x' using algebraic steps.", color=self.text_color).next_to(step2, DOWN, buff=0.4).align_to(step2, LEFT)
        step4 = Text("4. Generalize for 'a' to reach the final formula.", color=self.text_color).next_to(step3, DOWN, buff=0.4).align_to(step3, LEFT)

        steps_group = VGroup(recap_title, step1, step2, step3, step4)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[FadeIn(step, shift=UP) for step in steps_group[1:]], lag_ratio=0.3))
        self.wait(3)
        self.play(FadeOut(steps_group))