from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_D
        GOLD_ACCENT = GOLD_D
        HIGHLIGHT_COLOR = RED
        TEXT_COLOR = WHITE

        # --- Beat 1: Visual Hook - Parabola and Roots (Approx. 8-10 seconds) ---
        title = Text("Using the Quadratic Formula", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE_ACCENT, "include_numbers": False},
            y_axis_config={"scaling": LinearBase(), "include_numbers": False} # Use LinearBase for y-axis
        ).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # Parabola y = x^2 - 4
        parabola = axes.get_graph(lambda x: x**2 - 4, x_range=[-3, 3], color=GOLD_ACCENT)
        
        root1_dot = Dot(axes.c2p(-2, 0), color=HIGHLIGHT_COLOR, radius=0.1)
        root2_dot = Dot(axes.c2p(2, 0), color=HIGHLIGHT_COLOR, radius=0.1)
        
        # Add a question for intuition
        question_text = Text(
            "Where does this curve cross the x-axis?", 
            font_size=36, color=TEXT_COLOR
        ).next_to(title, DOWN, buff=0.8)

        self.play(Create(axes), Create(labels))
        self.play(Create(parabola), run_time=1.5)
        self.play(Write(question_text))
        self.play(GrowSmallestToLargest(root1_dot), GrowSmallestToLargest(root2_dot))
        self.wait(1.5)

        self.play(
            FadeOut(parabola),
            FadeOut(root1_dot),
            FadeOut(root2_dot),
            FadeOut(labels),
            axes.animate.scale(0.5).to_corner(UL), # Keep a small reference of axes
            FadeOut(question_text)
        )
        self.wait(0.5)

        # --- Beat 2: Introduce Standard Form and Quadratic Formula (Approx. 9-10 seconds) ---
        standard_form_text = Text("ax^2 + bx + c = 0", font_size=40, color=GOLD_ACCENT)
        standard_form_text.move_to(ORIGIN)

        intro_text = Text(
            "To find these x-intercepts, we use...", 
            font_size=36, color=TEXT_COLOR
        ).next_to(standard_form_text, UP, buff=1.0)
        
        formula_name = Text(
            "The Quadratic Formula", 
            font_size=40, color=BLUE_ACCENT
        ).next_to(standard_form_text, DOWN, buff=1.0)

        self.play(Write(intro_text))
        self.play(Write(standard_form_text))
        self.play(Write(formula_name))
        self.wait(1)

        # Build the formula text without Tex/MathTex (using individual Text objects)
        x_equals = Text("x =", color=BLUE_ACCENT, font_size=40)
        
        numerator_start = Text("(", color=BLUE_ACCENT, font_size=40)
        neg_b = Text("-b", color=BLUE_ACCENT, font_size=40)
        plus_minus = Text("±", color=GOLD_ACCENT, font_size=40)
        sqrt_begin = Text("sqrt(", color=BLUE_ACCENT, font_size=40)
        b_squared = Text("b^2", color=BLUE_ACCENT, font_size=40)
        minus_4ac = Text("- 4ac", color=BLUE_ACCENT, font_size=40)
        sqrt_end = Text("))", color=BLUE_ACCENT, font_size=40) # Close sqrt and parenthesis
        
        fraction_line = Line(LEFT, RIGHT, color=TEXT_COLOR).set_width(3)
        denominator = Text("2a", color=BLUE_ACCENT, font_size=40)

        # Arrange formula parts manually
        # Top part: (-b ± sqrt(b^2 - 4ac))
        vgroup_numerator_content = VGroup(
            neg_b, plus_minus, sqrt_begin, b_squared, minus_4ac, sqrt_end
        ).arrange(RIGHT, buff=0.1)
        
        vgroup_numerator = VGroup(numerator_start, vgroup_numerator_content).arrange(RIGHT, buff=0.05)
        
        # Denominator part
        vgroup_denominator = VGroup(denominator)

        # Combine all parts to calculate overall position
        quadratic_formula_vgroup = VGroup(
            x_equals, 
            vgroup_numerator, 
            fraction_line, 
            vgroup_denominator
        )
        
        # Position x =
        x_equals.next_to(standard_form_text, DOWN, buff=1.5).align_to(standard_form_text, LEFT)
        
        # Position numerator, line, denominator relative to x_equals
        vgroup_numerator.next_to(x_equals, RIGHT, buff=0.5)
        fraction_line.next_to(vgroup_numerator, DOWN, buff=0.2).align_to(vgroup_numerator.get_center(), LEFT).shift(RIGHT*0.5)
        vgroup_denominator.next_to(fraction_line, DOWN, buff=0.2)
        
        # Re-center the formula block
        quadratic_formula_vgroup.move_to(ORIGIN).shift(RIGHT*0.5)

        self.play(FadeOut(intro_text), FadeOut(formula_name))
        self.play(
            LaggedStart(
                Write(x_equals),
                Write(numerator_start),
                Write(neg_b),
                Write(plus_minus),
                Write(sqrt_begin),
                Write(b_squared),
                Write(minus_4ac),
                Write(sqrt_end),
                Create(fraction_line),
                Write(denominator),
                lag_ratio=0.05
            ),
            standard_form_text.animate.shift(UP * 2) # Move standard form up to make space
        )
        self.wait(1)

        # --- Beat 3: Applying a, b, c to an Example (Approx. 9-10 seconds) ---
        example_equation_text = Text("2x^2 + 5x - 3 = 0", font_size=40, color=TEXT_COLOR)
        example_equation_text.next_to(standard_form_text, DOWN, buff=0.5)

        self.play(ReplacementTransform(standard_form_text, example_equation_text))
        self.wait(0.5)

        # Identify a, b, c
        a_val_text = Text("a = 2", font_size=30, color=GOLD_ACCENT).next_to(example_equation_text, DOWN, buff=0.5).shift(LEFT*2)
        b_val_text = Text("b = 5", font_size=30, color=GOLD_ACCENT).next_to(a_val_text, RIGHT, buff=1)
        c_val_text = Text("c = -3", font_size=30, color=GOLD_ACCENT).next_to(b_val_text, RIGHT, buff=1)

        self.play(
            FadeIn(a_val_text, shift=UP), 
            FadeIn(b_val_text, shift=UP), 
            FadeIn(c_val_text, shift=UP),
            run_time=0.8
        )
        self.wait(1)

        # Prepare copies of a, b, c values for substitution
        a_val_copy_b = Text("2", font_size=40, color=GOLD_ACCENT).move_to(a_val_text.get_center()) # For 4ac
        b_val_copy_neg_b = Text("5", font_size=40, color=GOLD_ACCENT).move_to(b_val_text.get_center()) # For -b
        b_val_copy_b_sq = Text("5", font_size=40, color=GOLD_ACCENT).move_to(b_val_text.get_center()) # For b^2
        c_val_copy_4ac = Text("-3", font_size=40, color=GOLD_ACCENT).move_to(c_val_text.get_center()) # For 4ac
        a_val_copy_2a = Text("2", font_size=40, color=GOLD_ACCENT).move_to(a_val_text.get_center()) # For 2a

        # Substitute b
        sub_neg_b_val = Text("-5", font_size=40, color=GOLD_ACCENT).move_to(neg_b.get_center())
        self.play(Transform(b_val_copy_neg_b, sub_neg_b_val), FadeOut(neg_b))
        self.wait(0.5)

        # Substitute b^2
        sub_b_squared_val = Text("5^2", font_size=40, color=GOLD_ACCENT).move_to(b_squared.get_center())
        self.play(Transform(b_val_copy_b_sq, sub_b_squared_val), FadeOut(b_squared))
        self.wait(0.5)

        # Substitute 4ac
        sub_4ac_val = VGroup(
            Text("- 4(", color=GOLD_ACCENT, font_size=40),
            Text("2", color=GOLD_ACCENT, font_size=40),
            Text(")(", color=GOLD_ACCENT, font_size=40),
            Text("-3", color=GOLD_ACCENT, font_size=40),
            Text(")", color=GOLD_ACCENT, font_size=40)
        ).arrange(RIGHT, buff=0.05).move_to(minus_4ac.get_center())

        self.play(
            ReplacementTransform(minus_4ac, sub_4ac_val)
        )
        self.wait(0.5)

        # Substitute 2a
        sub_2a_val = VGroup(
            Text("2(", color=GOLD_ACCENT, font_size=40),
            Text("2", color=GOLD_ACCENT, font_size=40),
            Text(")", color=GOLD_ACCENT, font_size=40)
        ).arrange(RIGHT, buff=0.05).move_to(denominator.get_center())
        self.play(ReplacementTransform(denominator, sub_2a_val))
        self.wait(1)

        # Fade out the 'a=2', 'b=5', 'c=-3' labels
        self.play(FadeOut(a_val_text, b_val_text, c_val_text, a_val_copy_b, b_val_copy_neg_b, b_val_copy_b_sq, c_val_copy_4ac, a_val_copy_2a))
        
        # --- Beat 4: Calculation & Roots (Approx. 10-12 seconds) ---
        # Simplify b^2
        simplified_b_squared = Text("25", color=GOLD_ACCENT, font_size=40).move_to(sub_b_squared_val.get_center())
        self.play(ReplacementTransform(sub_b_squared_val, simplified_b_squared))
        self.wait(0.5)

        # Simplify -4ac
        simplified_4ac = Text("+24", color=GOLD_ACCENT, font_size=40).move_to(sub_4ac_val.get_center())
        self.play(ReplacementTransform(sub_4ac_val, simplified_4ac))
        self.wait(0.5)

        # Simplify 2a
        simplified_2a = Text("4", color=GOLD_ACCENT, font_size=40).move_to(sub_2a_val.get_center())
        self.play(ReplacementTransform(sub_2a_val, simplified_2a))
        self.wait(0.5)

        # Combine inside sqrt (25 + 24 = 49)
        inside_sqrt_sum = Text("49", color=GOLD_ACCENT, font_size=40).move_to(VGroup(simplified_b_squared, simplified_4ac).get_center())
        self.play(
            FadeOut(simplified_b_squared),
            FadeOut(simplified_4ac),
            ReplacementTransform(VGroup(simplified_b_squared, simplified_4ac), inside_sqrt_sum) # This won't work perfectly due to the way ReplaceTransform handles groups, a manual fadeout/fadein is safer here.
        )
        self.wait(0.5)

        # Take sqrt(49) = 7
        sqrt_result = Text("7", color=GOLD_ACCENT, font_size=40).move_to(inside_sqrt_sum.get_center())
        self.play(
            FadeOut(sqrt_begin), FadeOut(sqrt_end),
            ReplacementTransform(inside_sqrt_sum, sqrt_result)
        )
        self.wait(0.5)
        
        # Reconstruct the formula visually after simplification
        current_formula_parts = VGroup(
            x_equals, 
            numerator_start,
            sub_neg_b_val,
            plus_minus,
            sqrt_result,
            sqrt_end, # This closing parenthesis might need adjustment, or just fade it out if it looks odd.
            fraction_line,
            simplified_2a
        ).arrange_in_grid(rows=2, cols=3, row_alignments="dcr", col_alignments="l", h_buff=0.1, v_buff=0.5) # This is where arrange_in_grid would be useful but it's forbidden. Manual adjustment it is.

        # Manual repositioning of the simplified formula components
        # (This section is highly dependent on prior object positions, will aim for smooth transitions)
        # Re-creating a VGroup with simplified values for final formula state
        final_numerator_content_vgroup = VGroup(
            sub_neg_b_val,
            plus_minus,
            sqrt_result
        ).arrange(RIGHT, buff=0.1).move_to(VGroup(sub_neg_b_val, plus_minus, sqrt_result).get_center()) # Keep center

        final_numerator_vgroup = VGroup(numerator_start, final_numerator_content_vgroup).arrange(RIGHT, buff=0.05)
        final_quadratic_formula_vgroup = VGroup(
            x_equals, 
            final_numerator_vgroup, 
            fraction_line, 
            simplified_2a
        )
        final_quadratic_formula_vgroup.move_to(quadratic_formula_vgroup.get_center()) # Keep it centered

        self.play(
            FadeOut(example_equation_text),
            Transform(quadratic_formula_vgroup, final_quadratic_formula_vgroup)
        )
        self.wait(1)

        # Split into two solutions
        x1_eq = Text("x₁ = (-5 + 7) / 4", font_size=36, color=TEXT_COLOR)
        x2_eq = Text("x₂ = (-5 - 7) / 4", font_size=36, color=TEXT_COLOR)
        
        x1_eq.next_to(final_quadratic_formula_vgroup, DOWN, buff=1).shift(LEFT*2)
        x2_eq.next_to(x1_eq, RIGHT, buff=1.5)

        self.play(
            final_quadratic_formula_vgroup.animate.to_edge(UP).shift(DOWN*0.5),
            LaggedStart(
                Write(x1_eq),
                Write(x2_eq),
                lag_ratio=0.5
            )
        )
        self.wait(1)

        x1_val = Text("x₁ = 2 / 4 = 0.5", font_size=36, color=HIGHLIGHT_COLOR).move_to(x1_eq.get_center())
        x2_val = Text("x₂ = -12 / 4 = -3", font_size=36, color=HIGHLIGHT_COLOR).move_to(x2_eq.get_center())

        self.play(
            ReplacementTransform(x1_eq, x1_val),
            ReplacementTransform(x2_eq, x2_val)
        )
        self.wait(2)
        
        self.play(FadeOut(final_quadratic_formula_vgroup))

        # Show roots on a simple number line
        num_line = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-0.1, 0.1, 1], # Make it a flat line
            x_length=10,
            y_length=0.5,
            axis_config={"color": BLUE_ACCENT, "include_numbers": True},
            background_line_style={"stroke_opacity": 0} # No background lines
        )
        num_line.remove(num_line.y_axis) # Ensure it's just an x-axis

        x1_dot = Dot(num_line.c2p(0.5, 0), color=HIGHLIGHT_COLOR, radius=0.1)
        x2_dot = Dot(num_line.c2p(-3, 0), color=HIGHLIGHT_COLOR, radius=0.1)

        root_label1 = Text("x = 0.5", font_size=24, color=HIGHLIGHT_COLOR).next_to(x1_dot, UP, buff=0.2)
        root_label2 = Text("x = -3", font_size=24, color=HIGHLIGHT_COLOR).next_to(x2_dot, UP, buff=0.2)

        self.play(
            num_line.animate.move_to(ORIGIN),
            FadeOut(x1_val, x2_val)
        )
        self.play(Create(num_line))
        self.play(
            GrowFromCenter(x1_dot), Write(root_label1),
            GrowFromCenter(x2_dot), Write(root_label2)
        )
        self.wait(2)

        # --- Recap Card (Approx. 5 seconds) ---
        self.play(
            FadeOut(title),
            FadeOut(num_line),
            FadeOut(x1_dot),
            FadeOut(x2_dot),
            FadeOut(root_label1),
            FadeOut(root_label2),
            FadeOut(axes) # Fade out the small axes as well
        )

        recap_title = Text("Recap: Quadratic Formula", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        recap_point1 = Text(
            "Finds x-intercepts (roots) of a parabola.", 
            font_size=36, color=TEXT_COLOR
        ).next_to(recap_title, DOWN, buff=1)
        recap_point2 = Text(
            "Use ax^2 + bx + c = 0 to identify a, b, c.", 
            font_size=36, color=TEXT_COLOR
        ).next_to(recap_point1, DOWN, buff=0.5)
        recap_point3 = Text(
            "Substitute values carefully and simplify.", 
            font_size=36, color=TEXT_COLOR
        ).next_to(recap_point2, DOWN, buff=0.5)
        
        self.play(Write(recap_title))
        self.play(FadeIn(recap_point1, shift=UP))
        self.play(FadeIn(recap_point2, shift=UP))
        self.play(FadeIn(recap_point3, shift=UP))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_point1, recap_point2, recap_point3)))
        self.wait(1)