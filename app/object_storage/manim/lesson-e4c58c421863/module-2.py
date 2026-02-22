from manim import *

class QuadraticFormulaApplication(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD
        TEXT_COLOR = BLUE_ACCENT
        HIGHLIGHT_COLOR = GOLD_ACCENT

        # --- Helper function to create superscript for Text ---
        def create_superscript(base, sup, color=TEXT_COLOR, scale_factor=0.6):
            base_mobj = Text(str(base), color=color)
            sup_mobj = Text(str(sup), color=color, font_size=base_mobj.font_size * scale_factor)
            sup_mobj.next_to(base_mobj, UP + RIGHT * 0.1, buff=0.01)
            return VGroup(base_mobj, sup_mobj)

        # --- Beat 1: Visual Hook & Roots of a Parabola ---
        title = Text("Applying the Quadratic Formula", color=HIGHLIGHT_COLOR).scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # NumberPlane
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-2, 7, 1],
            x_length=7,
            y_length=6,
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1}
        ).shift(DOWN * 0.5)
        plane.add_coordinates()

        self.play(Create(plane), run_time=1.5)

        # Parabola y = x^2 - 4x + 3
        parabola_func = lambda x: x**2 - 4*x + 3
        parabola = plane.plot(parabola_func, color=BLUE_ACCENT)
        
        # Manually create 'x²' using Text and VGroup
        x_sq_grp = create_superscript("x", "2", color=BLUE_ACCENT)
        
        parabola_eq_text = VGroup(
            Text("y = ", color=BLUE_ACCENT),
            x_sq_grp,
            Text(" - 4x + 3", color=BLUE_ACCENT)
        ).arrange(RIGHT, buff=0.05).next_to(parabola, UP, buff=0.3)

        self.play(Create(parabola), Write(parabola_eq_text))
        self.wait(0.5)

        # Roots
        root1 = Dot(plane.coords_to_point(1, 0), color=HIGHLIGHT_COLOR, radius=0.08)
        root2 = Dot(plane.coords_to_point(3, 0), color=HIGHLIGHT_COLOR, radius=0.08)
        root1_label = Text("x = 1", color=HIGHLIGHT_COLOR).next_to(root1, DOWN, buff=0.1)
        root2_label = Text("x = 3", color=HIGHLIGHT_COLOR).next_to(root2, DOWN, buff=0.1)

        finding_roots_text = Text("Finding the roots...", color=TEXT_COLOR).next_to(parabola_eq_text, UP, buff=0.5)
        self.play(Write(finding_roots_text))
        self.play(GrowArrow(root1), GrowArrow(root2), FadeIn(root1_label), FadeIn(root2_label))
        self.wait(1)
        self.play(FadeOut(finding_roots_text), FadeOut(root1), FadeOut(root2), FadeOut(root1_label), FadeOut(root2_label))

        # --- Beat 2: When Factoring Fails & Generic Form ---
        # Transition to a parabola whose roots are irrational
        parabola_2_func = lambda x: x**2 + 2*x - 1
        parabola_2 = plane.plot(parabola_2_func, color=BLUE_ACCENT)

        x_sq_grp_2 = create_superscript("x", "2", color=BLUE_ACCENT)
        
        parabola_eq_text_2 = VGroup(
            Text("y = ", color=BLUE_ACCENT),
            x_sq_grp_2,
            Text(" + 2x - 1", color=BLUE_ACCENT)
        ).arrange(RIGHT, buff=0.05).next_to(parabola_2, UP, buff=0.3)

        hard_to_factor_text = Text("But what about this one?", color=TEXT_COLOR).next_to(parabola_eq_text_2, UP, buff=0.5)

        self.play(
            ReplacementTransform(parabola, parabola_2),
            ReplacementTransform(parabola_eq_text, parabola_eq_text_2)
        )
        self.play(Write(hard_to_factor_text))
        self.wait(1)

        # Introduce generic form
        generic_eq_text_elements = [
            create_superscript("ax", "2", color=HIGHLIGHT_COLOR),
            Text(" + ", color=TEXT_COLOR),
            Text("bx", color=HIGHLIGHT_COLOR),
            Text(" + ", color=TEXT_COLOR),
            Text("c", color=HIGHLIGHT_COLOR),
            Text(" = 0", color=TEXT_COLOR)
        ]
        generic_eq = VGroup(*generic_eq_text_elements).arrange(RIGHT, buff=0.1)
        generic_eq.scale(0.9).next_to(plane, UP*2, buff=0.5).to_edge(RIGHT)
        
        generic_intro_text = Text("For any quadratic equation...", color=TEXT_COLOR).next_to(generic_eq, LEFT, buff=0.5)
        self.play(FadeOut(hard_to_factor_text))
        self.play(Write(generic_intro_text), FadeIn(generic_eq))
        
        a_highlight = Circle(color=HIGHLIGHT_COLOR, radius=0.3).move_to(generic_eq_text_elements[0].get_center())
        b_highlight = Circle(color=HIGHLIGHT_COLOR, radius=0.3).move_to(generic_eq_text_elements[2].get_center())
        c_highlight = Circle(color=HIGHLIGHT_COLOR, radius=0.3).move_to(generic_eq_text_elements[4].get_center())
        
        self.play(Create(a_highlight), Create(b_highlight), Create(c_highlight))
        self.wait(1)
        self.play(FadeOut(a_highlight), FadeOut(b_highlight), FadeOut(c_highlight))
        self.play(FadeOut(generic_intro_text))

        # --- Beat 3: The Quadratic Formula Revealed (Manual Text Construction) ---
        # Move previous elements to make space
        self.play(
            plane.animate.shift(LEFT*3.5),
            parabola_2.animate.shift(LEFT*3.5),
            parabola_eq_text_2.animate.shift(LEFT*3.5),
            generic_eq.animate.shift(LEFT*3.5)
        )

        # Construct the quadratic formula piece by piece using Text and Line
        formula_x_eq = Text("x = ", color=TEXT_COLOR).scale(0.8)

        # Numerator components
        neg_b = Text("-b", color=HIGHLIGHT_COLOR).scale(0.8)
        plus_minus = Text("±", color=TEXT_COLOR).scale(0.8)
        
        b_sq_grp_formula = create_superscript("b", "2", color=HIGHLIGHT_COLOR, scale_factor=0.6)
        b_sq_grp_formula.scale(0.8)

        minus_4ac = Text(" - 4ac", color=TEXT_COLOR).scale(0.8)
        
        discriminant_content = VGroup(b_sq_grp_formula, minus_4ac).arrange(RIGHT, buff=0.05)
        
        sqrt_line = Line(discriminant_content.get_corner(UP + LEFT) + LEFT * 0.1, 
                         discriminant_content.get_corner(UP + RIGHT) + RIGHT * 0.1).set_stroke(color=TEXT_COLOR, width=3)
        sqrt_symbol = Text("√", color=TEXT_COLOR).scale(1.5).next_to(sqrt_line, LEFT, buff=0.05)
        sqrt_symbol.align_to(sqrt_line, DOWN) # Adjust vertical alignment

        sqrt_expression = VGroup(sqrt_symbol, sqrt_line, discriminant_content)
        
        numerator_full = VGroup(neg_b, plus_minus, sqrt_expression).arrange(RIGHT, buff=0.1)

        # Denominator
        denominator_text = Text("2a", color=HIGHLIGHT_COLOR).scale(0.8)

        # Fraction line
        fraction_line = Line(LEFT, RIGHT).set_length(numerator_full.width * 1.1).set_stroke(color=TEXT_COLOR, width=3)
        
        # Assemble the full formula
        formula_parts = VGroup(numerator_full, fraction_line, denominator_text).arrange(DOWN, buff=0.1)
        full_formula = VGroup(formula_x_eq, formula_parts).arrange(RIGHT, buff=0.1).scale(1.2).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)

        # Animation for formula construction
        self.play(Write(formula_x_eq))
        self.play(Write(neg_b))
        self.play(Write(plus_minus))
        self.play(Write(b_sq_grp_formula))
        self.play(Write(minus_4ac))
        self.play(Create(sqrt_line))
        self.play(Write(sqrt_symbol))
        self.play(Create(fraction_line))
        self.play(Write(denominator_text))
        self.wait(1)

        formula_intro_text = Text("The Quadratic Formula!", color=HIGHLIGHT_COLOR).scale(1.2).next_to(full_formula, UP, buff=0.5)
        self.play(Write(formula_intro_text))
        self.wait(1)
        self.play(FadeOut(formula_intro_text))
        
        # Group all formula parts for later transformation
        full_formula_mobj = VGroup(formula_x_eq, neg_b, plus_minus, sqrt_symbol, sqrt_line, discriminant_content, fraction_line, denominator_text)
        
        # --- Beat 4: Applying the Formula - Substitution ---
        # Use x^2 - 4x + 3 = 0 (from Beat 1)
        equation_to_solve = VGroup(
            create_superscript("x", "2", color=BLUE_ACCENT),
            Text(" - 4x + 3 = 0", color=BLUE_ACCENT)
        ).arrange(RIGHT, buff=0.05).scale(1.1)

        self.play(
            FadeOut(plane),
            FadeOut(parabola_2),
            FadeOut(parabola_eq_text_2),
            FadeOut(generic_eq),
            full_formula_mobj.animate.scale(0.7).to_edge(RIGHT, buff=0.2).to_edge(UP, buff=0.2), # Move formula to corner
            Transform(title, title.copy().scale(0.8).to_edge(UP+LEFT))
        )
        
        # Make a new title for "Applying..."
        apply_title = Text("Applying the Formula", color=HIGHLIGHT_COLOR).scale(1.2).to_edge(UP)
        self.add(apply_title) 

        # Identify a, b, c
        self.play(Write(equation_to_solve.to_edge(LEFT, buff=0.5).shift(UP*1.5)))
        
        # Define a, b, c Text objects
        a_val = Text("a = 1", color=HIGHLIGHT_COLOR).next_to(equation_to_solve, DOWN, buff=0.5).align_to(equation_to_solve, LEFT)
        b_val = Text("b = -4", color=HIGHLIGHT_COLOR).next_to(a_val, DOWN, buff=0.3).align_to(equation_to_solve, LEFT)
        c_val = Text("c = 3", color=HIGHLIGHT_COLOR).next_to(b_val, DOWN, buff=0.3).align_to(equation_to_solve, LEFT)

        self.play(Write(a_val))
        self.play(Write(b_val))
        self.play(Write(c_val))
        self.wait(1)

        # Show the substitution more clearly by moving the formula to center and then transforming
        self.play(full_formula_mobj.animate.move_to(ORIGIN).shift(RIGHT*1))

        # Prepare targets for substitution
        target_neg_b = Text("-(-4)", color=HIGHLIGHT_COLOR).scale(0.8).move_to(neg_b.get_center())
        target_b_sq_grp = create_superscript("(-4)", "2", color=HIGHLIGHT_COLOR, scale_factor=0.6).scale(0.8).move_to(b_sq_grp_formula.get_center())
        target_minus_4ac = Text(" - 4(1)(3)", color=TEXT_COLOR).scale(0.8).move_to(minus_4ac.get_center())
        target_denominator_text = Text("2(1)", color=HIGHLIGHT_COLOR).scale(0.8).move_to(denominator_text.get_center())

        # Play substitutions
        self.play(
            Transform(neg_b, target_neg_b),
            Transform(b_sq_grp_formula, target_b_sq_grp),
            Transform(minus_4ac, target_minus_4ac),
            Transform(denominator_text, target_denominator_text)
        )
        self.wait(1)

        # --- Beat 5: Solving & Visualizing Roots ---
        # Simplify the substituted formula
        
        # Step 1: -(-4) = 4, (-4)^2 = 16, 4(1)(3) = 12, 2(1) = 2
        formula_step1_neg_b = Text("4", color=HIGHLIGHT_COLOR).scale(0.8).move_to(neg_b.get_center())
        formula_step1_b_sq = Text("16", color=HIGHLIGHT_COLOR).scale(0.8).move_to(b_sq_grp_formula.get_center())
        formula_step1_minus_4ac = Text(" - 12", color=TEXT_COLOR).scale(0.8).move_to(minus_4ac.get_center())
        formula_step1_denominator_text = Text("2", color=HIGHLIGHT_COLOR).scale(0.8).move_to(denominator_text.get_center())

        self.play(
            ReplacementTransform(neg_b, formula_step1_neg_b),
            ReplacementTransform(b_sq_grp_formula, formula_step1_b_sq),
            ReplacementTransform(minus_4ac, formula_step1_minus_4ac),
            ReplacementTransform(denominator_text, formula_step1_denominator_text),
        )
        self.wait(1)

        # Update the discriminant content group for next step's transformation
        current_discriminant_content = VGroup(formula_step1_b_sq, formula_step1_minus_4ac).arrange(RIGHT, buff=0.05).move_to(discriminant_content.get_center())
        
        # Step 2: 16 - 12 = 4
        formula_step2_discriminant_content = Text("4", color=HIGHLIGHT_COLOR).scale(0.8).move_to(current_discriminant_content.get_center())
        
        self.play(
            ReplacementTransform(current_discriminant_content, formula_step2_discriminant_content)
        )
        self.wait(1)

        # Update the sqrt_expression group for next step's transformation
        current_sqrt_expression = VGroup(sqrt_symbol, sqrt_line, formula_step2_discriminant_content)
        
        # Step 3: sqrt(4) = 2
        formula_step3_sqrt_result = Text("2", color=HIGHLIGHT_COLOR).scale(0.8).move_to(current_sqrt_expression.get_center()) # The result of sqrt(4)
        
        self.play(
            ReplacementTransform(current_sqrt_expression, formula_step3_sqrt_result)
        )
        self.wait(1)

        # Now, arrange the final expression elements after all transformations
        final_numerator_full = VGroup(formula_step1_neg_b, plus_minus, formula_step3_sqrt_result).arrange(RIGHT, buff=0.1)
        final_fraction_line = Line(LEFT, RIGHT).set_length(final_numerator_full.width * 1.1).set_stroke(color=TEXT_COLOR, width=3).next_to(final_numerator_full, DOWN, buff=0.1)
        final_denominator_text = formula_step1_denominator_text.next_to(final_fraction_line, DOWN, buff=0.1)
        final_parts = VGroup(final_numerator_full, final_fraction_line, final_denominator_text).arrange(DOWN, buff=0.1)
        final_full_expression = VGroup(formula_x_eq, final_parts).arrange(RIGHT, buff=0.1).move_to(ORIGIN).shift(RIGHT*1)

        self.play(Transform(full_formula_mobj, final_full_expression)) # This will clean up positioning after individual transforms

        # Step 4: Calculate x1 and x2
        x1_eq = Text("x₁ = (4 + 2) / 2 = 6 / 2 = 3", color=HIGHLIGHT_COLOR).scale(0.8).next_to(final_full_expression, DOWN, buff=0.8).align_to(final_full_expression, LEFT)
        x2_eq = Text("x₂ = (4 - 2) / 2 = 2 / 2 = 1", color=HIGHLIGHT_COLOR).scale(0.8).next_to(x1_eq, DOWN, buff=0.3).align_to(x1_eq, LEFT)
        
        self.play(FadeOut(final_full_expression))
        self.play(Write(x1_eq))
        self.play(Write(x2_eq))
        self.wait(1)

        # --- Visualize roots on graph again ---
        # Bring back the plane and parabola for x^2 - 4x + 3 = 0
        self.play(
            FadeOut(equation_to_solve), FadeOut(a_val), FadeOut(b_val), FadeOut(c_val),
            FadeOut(apply_title),
            FadeOut(title) # Fade out the corner title as well
        )

        plane_final = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-2, 7, 1],
            x_length=7,
            y_length=6,
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1}
        ).move_to(ORIGIN)
        plane_final.add_coordinates()
        
        parabola_func_final = lambda x: x**2 - 4*x + 3
        parabola_final = plane_final.plot(parabola_func_final, color=BLUE_ACCENT)

        x_sq_grp_final = create_superscript("x", "2", color=BLUE_ACCENT)
        
        parabola_eq_text_final = VGroup(
            Text("y = ", color=BLUE_ACCENT),
            x_sq_grp_final,
            Text(" - 4x + 3", color=BLUE_ACCENT)
        ).arrange(RIGHT, buff=0.05).next_to(parabola_final, UP, buff=0.3)

        self.play(FadeIn(plane_final), FadeIn(parabola_final), FadeIn(parabola_eq_text_final))
        
        root1_final = Dot(plane_final.coords_to_point(1, 0), color=HIGHLIGHT_COLOR, radius=0.08)
        root2_final = Dot(plane_final.coords_to_point(3, 0), color=HIGHLIGHT_COLOR, radius=0.08)
        root1_label_final = Text("x = 1", color=HIGHLIGHT_COLOR).next_to(root1_final, DOWN, buff=0.1)
        root2_label_final = Text("x = 3", color=HIGHLIGHT_COLOR).next_to(root2_final, DOWN, buff=0.1)

        self.play(
            FadeOut(x1_eq), FadeOut(x2_eq),
            FadeIn(root1_final), FadeIn(root2_final),
            FadeIn(root1_label_final), FadeIn(root2_label_final)
        )
        found_roots_text = Text("The roots match!", color=TEXT_COLOR).next_to(parabola_eq_text_final, UP, buff=0.5)
        self.play(Write(found_roots_text))
        self.wait(2)
        
        # --- Beat 6: Recap Card ---
        self.play(
            FadeOut(plane_final), FadeOut(parabola_final), FadeOut(parabola_eq_text_final),
            FadeOut(root1_final), FadeOut(root2_final), FadeOut(root1_label_final), FadeOut(root2_label_final),
            FadeOut(found_roots_text)
        )
        
        recap_title = Text("Recap: Applying the Quadratic Formula", color=HIGHLIGHT_COLOR).scale(1.1)
        recap_points_part1 = VGroup(
            Text("1. Identify a, b, c from ax² + bx + c = 0", color=TEXT_COLOR).scale(0.8),
            Text("2. Substitute values into the formula: ", color=TEXT_COLOR).scale(0.8),
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).shift(UP*1.5)

        # Build a simplified quadratic formula for recap without animation
        recap_formula_x_eq = Text("x = ", color=TEXT_COLOR).scale(0.6)
        recap_neg_b = Text("-b", color=HIGHLIGHT_COLOR).scale(0.6)
        recap_plus_minus = Text("±", color=TEXT_COLOR).scale(0.6)
        
        recap_b_sq_grp = create_superscript("b", "2", color=HIGHLIGHT_COLOR, scale_factor=0.6)
        recap_b_sq_grp.scale(0.6)

        recap_minus_4ac = Text(" - 4ac", color=TEXT_COLOR).scale(0.6)
        recap_discriminant_content = VGroup(recap_b_sq_grp, recap_minus_4ac).arrange(RIGHT, buff=0.05)
        
        recap_sqrt_line = Line(recap_discriminant_content.get_corner(UP + LEFT) + LEFT * 0.1, 
                         recap_discriminant_content.get_corner(UP + RIGHT) + RIGHT * 0.1).set_stroke(color=TEXT_COLOR, width=2)
        recap_sqrt_symbol = Text("√", color=TEXT_COLOR).scale(1.2).next_to(recap_sqrt_line, LEFT, buff=0.05)
        recap_sqrt_symbol.align_to(recap_sqrt_line, DOWN)
        recap_sqrt_expression = VGroup(recap_sqrt_symbol, recap_sqrt_line, recap_discriminant_content)
        
        recap_numerator_full = VGroup(recap_neg_b, recap_plus_minus, recap_sqrt_expression).arrange(RIGHT, buff=0.1)

        recap_denominator_text = Text("2a", color=HIGHLIGHT_COLOR).scale(0.6)
        recap_fraction_line = Line(LEFT, RIGHT).set_length(recap_numerator_full.width * 1.1).set_stroke(color=TEXT_COLOR, width=2)
        
        recap_formula_parts = VGroup(recap_numerator_full, recap_fraction_line, recap_denominator_text).arrange(DOWN, buff=0.1)
        recap_full_formula = VGroup(recap_formula_x_eq, recap_formula_parts).arrange(RIGHT, buff=0.1).scale(1.1)
        
        recap_full_formula.next_to(recap_points_part1[1], RIGHT, buff=0.2).align_to(recap_points_part1[1], LEFT) # Align with the text "2. Substitute..."
        
        recap_point3 = Text("3. Simplify carefully to find the two roots.", color=TEXT_COLOR).scale(0.8).next_to(recap_points_part1[1], DOWN, buff=0.7).align_to(recap_points_part1[0], LEFT)
        recap_point4 = Text("4. Works for ANY quadratic equation!", color=TEXT_COLOR).scale(0.8).next_to(recap_point3, DOWN, buff=0.3).align_to(recap_points_part1[0], LEFT)
        
        recap_all = VGroup(recap_title, recap_points_part1[0], recap_points_part1[1], recap_full_formula, recap_point3, recap_point4).arrange(DOWN, buff=0.5, aligned_edge=LEFT).center()
        
        self.play(Write(recap_title))
        self.play(LaggedStart(*[Write(p) for p in [recap_points_part1[0], recap_points_part1[1], recap_full_formula, recap_point3, recap_point4]], lag_ratio=0.7))
        self.wait(3)
        self.play(FadeOut(recap_all))
        self.wait(1)