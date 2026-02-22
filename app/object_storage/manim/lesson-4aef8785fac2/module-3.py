from manim import *

class QuadraticFormulaVisuals(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        TEXT_COLOR = WHITE
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E

        # --- Helper for creating Text-based math expressions ---
        def create_text_formula_part(text_str, color=TEXT_COLOR, font_size=40):
            return Text(text_str, font_size=font_size, color=color, disable_ligatures=True)

        def create_quadratic_formula_text_objects():
            # x =
            x_text = create_text_formula_part("x", color=GOLD_ACCENT)
            eq_text = create_text_formula_part("=", color=TEXT_COLOR)
            x_eq_group = VGroup(x_text, eq_text).arrange(RIGHT, buff=0.2)

            # Numerator parts: -b
            minus_text = create_text_formula_part("-", color=TEXT_COLOR)
            b_text_minus_b = create_text_formula_part("b", color=BLUE_ACCENT)
            minus_b_group = VGroup(minus_text, b_text_minus_b).arrange(RIGHT, buff=0.1)

            # Plus/Minus symbol
            plus_minus_text = create_text_formula_part("±", color=TEXT_COLOR)

            # Square root content (b^2 - 4ac)
            # Create b^2 part
            b_text_b_sq = create_text_formula_part("b", color=BLUE_ACCENT)
            sq_text = create_text_formula_part("2", font_size=25, color=TEXT_COLOR) # Smaller font for superscript
            b_sq_group = VGroup(b_text_b_sq, sq_text)
            sq_text.next_to(b_text_b_sq, UP + RIGHT * 0.1, buff=0.05) # Manual superscript positioning

            # Create -4ac part
            minus_4 = create_text_formula_part("-", color=TEXT_COLOR)
            four_text = create_text_formula_part("4", color=TEXT_COLOR)
            a_text_4ac = create_text_formula_part("a", color=BLUE_ACCENT)
            c_text_4ac = create_text_formula_part("c", color=BLUE_ACCENT)
            minus_4ac_group = VGroup(minus_4, four_text, a_text_4ac, c_text_4ac).arrange(RIGHT, buff=0.05)

            discriminant_content = VGroup(b_sq_group, minus_4ac_group).arrange(RIGHT, buff=0.1)
            
            # Custom square root symbol (drawing with lines)
            # Start point for the sqrt hook/check
            sqrt_start_point = LEFT * 0.5 + DOWN * 0.1 
            
            s1 = Line(sqrt_start_point, sqrt_start_point + RIGHT * 0.1 + UP * 0.2, stroke_width=2, color=TEXT_COLOR)
            s2 = Line(s1.get_end(), s1.get_end() + RIGHT * 0.2 + DOWN * 0.4, stroke_width=2, color=TEXT_COLOR)
            s3 = Line(s2.get_end(), s2.get_end() + RIGHT * 0.2 + UP * 0.4, stroke_width=2, color=TEXT_COLOR)
            
            sqrt_symbol_parts = VGroup(s1, s2, s3)
            # Scale it to fit well with the text height
            sqrt_symbol_parts.set_height(discriminant_content.height * 0.7)
            sqrt_symbol_parts.align_to(discriminant_content, DOWN).shift(UP * 0.1 + LEFT * 0.05) # Adjust position

            # Top bar for the square root
            sqrt_top_line = Line(
                sqrt_symbol_parts.get_right() + RIGHT * 0.05,
                discriminant_content.get_right() + RIGHT * 0.1,
                stroke_width=2, color=TEXT_COLOR
            ).align_to(discriminant_content, UP)
            
            sqrt_term_group = VGroup(sqrt_symbol_parts, sqrt_top_line, discriminant_content)

            # Denominator parts
            two_text = create_text_formula_part("2", color=TEXT_COLOR)
            a_text_denom = create_text_formula_part("a", color=BLUE_ACCENT)
            two_a_group = VGroup(two_text, a_text_denom).arrange(RIGHT, buff=0.1)

            # Group numerator: minus_b, plus_minus, sqrt_term
            numerator_group = VGroup(minus_b_group, plus_minus_text, sqrt_term_group).arrange(RIGHT, buff=0.2)
            
            # Fraction bar
            fraction_bar = Line(LEFT, RIGHT, stroke_width=2, color=TEXT_COLOR).set_width(numerator_group.width * 1.2)
            
            # Combine all (numerator, fraction_bar, denominator)
            formula_fraction_part = VGroup(
                numerator_group,
                fraction_bar,
                two_a_group
            ).arrange(DOWN, buff=0.4)
            
            # Adjust fraction bar width and position
            fraction_bar.set_width(max(numerator_group.width, two_a_group.width) * 1.1)
            fraction_bar.move_to(formula_fraction_part.get_center())
            numerator_group.align_to(fraction_bar, DOWN).shift(UP * 0.3)
            two_a_group.align_to(fraction_bar, UP).shift(DOWN * 0.3)

            full_formula_vgroup = VGroup(x_eq_group, formula_fraction_part).arrange(RIGHT, buff=0.2)
            
            # Return all granular parts needed for highlighting and transforms
            return (
                full_formula_vgroup, x_eq_group, numerator_group, fraction_bar, two_a_group, 
                minus_b_group, plus_minus_text, sqrt_term_group, discriminant_content, 
                sqrt_symbol_parts, sqrt_top_line, b_sq_group, minus_4ac_group,
                b_text_minus_b, b_text_b_sq, a_text_4ac, c_text_4ac, a_text_denom
            )

        # --- Beat 1: The Problem - Finding X-intercepts ---
        self.wait(0.5)
        title = create_text_formula_part("Applying the Quadratic Formula and Visuals", font_size=50, color=GOLD_ACCENT).to_edge(UP, buff=0.7)
        self.play(Write(title))
        self.wait(1)

        intro_text = create_text_formula_part("Finding where a parabola crosses the x-axis...", font_size=35, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5)
        self.play(Write(intro_text))
        self.wait(1)

        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            x_length=10, y_length=7,
            background_line_style={"stroke_opacity": 0.5, "stroke_color": GREY_B},
            axis_config={"color": GREY_A}
        ).shift(DOWN * 0.5)
        
        parabola_func = lambda x: 0.5 * x**2 - x - 3
        parabola = ParametricFunction(
            lambda t: plane.coords_to_point(t, parabola_func(t)),
            t_range=[-3, 5], color=BLUE_ACCENT, stroke_width=5
        )

        self.play(FadeIn(plane, shift=UP))
        self.play(Create(parabola))
        self.wait(0.5)

        x_axis_label = create_text_formula_part("x-axis (where y = 0)", font_size=28, color=GOLD_ACCENT).next_to(plane.get_x_axis(), DOWN, buff=0.2)
        self.play(FadeIn(x_axis_label, shift=UP))
        
        root1_coords = [-2, 0]
        root2_coords = [4, 0]
        
        dot1 = Dot(point=plane.coords_to_point(*root1_coords), color=GOLD_ACCENT, radius=0.15)
        dot2 = Dot(point=plane.coords_to_point(*root2_coords), color=GOLD_ACCENT, radius=0.15)

        roots_label = create_text_formula_part("Roots", font_size=30, color=GOLD_ACCENT).next_to(dot1, UP).shift(RIGHT*0.5)
        
        self.play(GrowSmallest(dot1), GrowSmallest(dot2), Write(roots_label))
        self.wait(1.5)

        # --- Beat 2: The Tool - Quadratic Formula Intuition ---
        self.play(
            FadeOut(intro_text), FadeOut(x_axis_label), FadeOut(roots_label),
            parabola.animate.set_color(BLUE_ACCENT).scale(0.8).shift(UP * 0.5), # Shrink & move parabola slightly
            dot1.animate.scale(0.8).shift(UP * 0.5), dot2.animate.scale(0.8).shift(UP * 0.5),
            plane.animate.set_opacity(0.3)
        )

        tool_text = create_text_formula_part("A universal key for ANY parabola's roots!", font_size=35, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5)
        self.play(FadeTransform(
            create_text_formula_part("Finding where a parabola crosses the x-axis...", font_size=35, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5),
            tool_text
        ))
        
        # Simulate different parabolas to show universality
        parabola_func2 = lambda x: -0.3 * x**2 + x + 2
        parabola2 = ParametricFunction(
            lambda t: plane.coords_to_point(t, parabola_func2(t)),
            t_range=[-3, 6], color=BLUE_ACCENT, stroke_width=5
        ).scale(0.8).shift(UP * 0.5) # Same scale and shift as parabola 1 after transform

        parabola_func3 = lambda x: 0.8 * x**2 + 2*x - 1
        parabola3 = ParametricFunction(
            lambda t: plane.coords_to_point(t, parabola_func3(t)),
            t_range=[-3.5, 1.5], color=BLUE_ACCENT, stroke_width=5
        ).scale(0.8).shift(UP * 0.5)

        self.play(ReplacementTransform(parabola, parabola2), FadeOut(dot1, dot2))
        self.wait(0.5)
        self.play(ReplacementTransform(parabola2, parabola3))
        self.wait(0.5)
        self.play(ReplacementTransform(parabola3, parabola)) # Go back to original for continuity

        universal_icon = create_text_formula_part("🔑", font_size=100, color=GOLD_ACCENT).shift(RIGHT*3 + UP*2)
        self.play(FadeIn(universal_icon, scale=0.5))
        self.play(universal_icon.animate.shift(LEFT * 4)) # Move the key across screen
        self.wait(0.5)
        
        # --- Beat 3: Unveiling the Formula (Character by Character) ---
        self.play(
            FadeOut(plane), FadeOut(parabola), FadeOut(universal_icon),
            FadeOut(tool_text)
        )
        self.remove(universal_icon) # Ensure it's fully gone

        # Create the full formula using the helper
        (
            full_formula_mobj, x_eq_group, numerator_group, fraction_bar_mobj, two_a_group, 
            minus_b_group, plus_minus_text, sqrt_term_group, discriminant_content, 
            sqrt_symbol_parts, sqrt_top_line, b_sq_group, minus_4ac_group,
            b_text_minus_b, b_text_b_sq, a_text_4ac, c_text_4ac, a_text_denom
        ) = create_quadratic_formula_text_objects()
        
        full_formula_mobj.move_to(ORIGIN)

        # Animate building the formula
        unveil_text = create_text_formula_part("The Quadratic Formula!", font_size=45, color=GOLD_ACCENT).next_to(title, DOWN, buff=0.5)
        self.play(FadeTransform(
            create_text_formula_part("A universal key for ANY parabola's roots!", font_size=35, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5),
            unveil_text
        ))
        
        self.play(Write(x_eq_group))
        self.wait(0.2)
        self.play(Create(fraction_bar_mobj))
        self.wait(0.2)
        self.play(Write(minus_b_group))
        self.wait(0.2)
        self.play(Write(plus_minus_text))
        self.wait(0.2)
        self.play(Write(discriminant_content))
        self.play(Create(sqrt_symbol_parts), Create(sqrt_top_line))
        self.wait(0.2)
        self.play(Write(two_a_group))
        self.wait(1.5)

        # --- Beat 4: Applying it (Conceptual) ---
        applying_text = create_text_formula_part("Input 'a', 'b', 'c' from your equation...", font_size=35, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5)
        self.play(FadeTransform(unveil_text, applying_text))

        # Example general quadratic equation (text-based)
        eq_a = create_text_formula_part("a", color=BLUE_ACCENT, font_size=45)
        eq_x2 = create_text_formula_part("x", color=TEXT_COLOR, font_size=45)
        eq_sup2 = create_text_formula_part("2", font_size=28, color=TEXT_COLOR) # Superscript '2'
        eq_plus_b = create_text_formula_part(" + ", color=TEXT_COLOR, font_size=45)
        eq_b = create_text_formula_part("b", color=BLUE_ACCENT, font_size=45)
        eq_x = create_text_formula_part("x", color=TEXT_COLOR, font_size=45)
        eq_plus_c = create_text_formula_part(" + ", color=TEXT_COLOR, font_size=45)
        eq_c = create_text_formula_part("c", color=BLUE_ACCENT, font_size=45)
        eq_eq0 = create_text_formula_part(" = 0", color=TEXT_COLOR, font_size=45)

        # Assemble the general equation
        gen_equation_parts = [eq_a, eq_x2, eq_sup2, eq_plus_b, eq_b, eq_x, eq_plus_c, eq_c, eq_eq0]
        
        # Position manually for visual clarity (instead of arrange)
        eq_x2_group = VGroup(eq_x2, eq_sup2)
        eq_sup2.next_to(eq_x2, UP + RIGHT * 0.1, buff=0)
        
        gen_equation = VGroup(eq_a, eq_x2_group, eq_plus_b, eq_b, eq_x, eq_plus_c, eq_c, eq_eq0)
        gen_equation.arrange(RIGHT, buff=0.1)
        gen_equation.shift(UP * 2)

        self.play(FadeIn(gen_equation))
        self.wait(0.5)

        # Animate 'a', 'b', 'c' moving from equation to formula
        # Create copies to animate the "movement"
        temp_a_eq_copy = eq_a.copy().set_color(GOLD_ACCENT)
        temp_b_eq_copy = eq_b.copy().set_color(GOLD_ACCENT)
        temp_c_eq_copy = eq_c.copy().set_color(GOLD_ACCENT)

        self.play(
            LaggedStart(
                Transform(temp_a_eq_copy, a_text_4ac.copy().set_color(GOLD_ACCENT)),
                Transform(temp_b_eq_copy, b_text_minus_b.copy().set_color(GOLD_ACCENT)),
                Transform(temp_c_eq_copy, c_text_4ac.copy().set_color(GOLD_ACCENT)),
                lag_ratio=0.5,
                run_time=1.5
            )
        )
        self.remove(temp_a_eq_copy, temp_b_eq_copy, temp_c_eq_copy) # Remove the first set of copies

        # Animate remaining a, b
        temp_a_eq_copy2 = eq_a.copy().set_color(GOLD_ACCENT)
        temp_b_eq_copy2 = eq_b.copy().set_color(GOLD_ACCENT)

        self.play(
            LaggedStart(
                Transform(temp_a_eq_copy2, a_text_denom.copy().set_color(GOLD_ACCENT)),
                Transform(temp_b_eq_copy2, b_text_b_sq.copy().set_color(GOLD_ACCENT)),
                lag_ratio=0.5,
                run_time=1.5
            )
        )
        self.remove(temp_a_eq_copy2, temp_b_eq_copy2)
        self.wait(1)
        
        # --- Beat 5: Visualizing the Solutions ---
        self.play(FadeOut(gen_equation))
        self.play(
            FadeOut(applying_text),
            full_formula_mobj.animate.scale(0.6).to_edge(UP).shift(RIGHT * 2),
        )

        visualize_text = create_text_formula_part("Two potential solutions: x1 and x2!", font_size=35, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5)
        self.play(FadeTransform(
            create_text_formula_part("Input 'a', 'b', 'c' from your equation...", font_size=35, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5),
            visualize_text
        ))

        self.play(FadeIn(plane.set_opacity(1))) # Bring plane back to full opacity
        
        parabola_visual = ParametricFunction(
            lambda t: plane.coords_to_point(t, parabola_func(t)),
            t_range=[-3, 5], color=BLUE_ACCENT, stroke_width=5
        ).shift(DOWN * 0.5) # Reset position relative to plane
        self.play(Create(parabola_visual))

        # Animate the plus/minus splitting
        plus_part_symbol = create_text_formula_part("+", color=TEXT_COLOR).move_to(plus_minus_text.get_center())
        minus_part_symbol = create_text_formula_part("-", color=TEXT_COLOR).move_to(plus_minus_text.get_center())

        plus_arrow = Arrow(plus_part_symbol.get_center(), plus_part_symbol.get_center() + UP*0.8 + LEFT*0.5, buff=0.1, max_stroke_width_to_length_ratio=0.08, color=GOLD_ACCENT)
        minus_arrow = Arrow(minus_part_symbol.get_center(), minus_part_symbol.get_center() + DOWN*0.8 + LEFT*0.5, buff=0.1, max_stroke_width_to_length_ratio=0.08, color=GOLD_ACCENT)

        x1_calc_text = create_text_formula_part("x1 calculation", font_size=28, color=TEXT_COLOR).next_to(plus_arrow, UP, buff=0.2).align_to(full_formula_mobj, LEFT).shift(RIGHT*0.5)
        x2_calc_text = create_text_formula_part("x2 calculation", font_size=28, color=TEXT_COLOR).next_to(minus_arrow, DOWN, buff=0.2).align_to(full_formula_mobj, LEFT).shift(RIGHT*0.5)
        
        self.play(
            Transform(plus_minus_text, plus_part_symbol), # Transform into '+'
            FadeIn(minus_part_symbol), # Fade in the '-' separately
            Create(plus_arrow), Create(minus_arrow),
            FadeIn(x1_calc_text), FadeIn(x2_calc_text),
            run_time=1.5
        )
        self.wait(0.5)

        # Show the roots appearing from the formula side
        dot1_final = Dot(point=plane.coords_to_point(*root1_coords), color=GOLD_ACCENT, radius=0.15)
        dot2_final = Dot(point=plane.coords_to_point(*root2_coords), color=GOLD_ACCENT, radius=0.15)
        
        arrow_to_dot1 = Arrow(x1_calc_text.get_left(), dot1_final.get_center(), buff=0.1, max_stroke_width_to_length_ratio=0.08, color=GOLD_ACCENT)
        arrow_to_dot2 = Arrow(x2_calc_text.get_left(), dot2_final.get_center(), buff=0.1, max_stroke_width_to_length_ratio=0.08, color=GOLD_ACCENT)

        x1_val_text = create_text_formula_part("x = -2", font_size=35, color=GOLD_ACCENT).next_to(dot1_final, LEFT, buff=0.2)
        x2_val_text = create_text_formula_part("x = 4", font_size=35, color=GOLD_ACCENT).next_to(dot2_final, RIGHT, buff=0.2)

        self.play(
            Create(arrow_to_dot1), GrowSmallest(dot1_final), Write(x1_val_text),
            Create(arrow_to_dot2), GrowSmallest(dot2_final), Write(x2_val_text),
            FadeOut(plus_arrow, minus_arrow, x1_calc_text, x2_calc_text, plus_part_symbol, minus_part_symbol)
        )
        self.wait(2)

        # --- Recap Card ---
        self.play(
            FadeOut(plane), FadeOut(parabola_visual), FadeOut(dot1_final), FadeOut(dot2_final),
            FadeOut(x1_val_text), FadeOut(x2_val_text),
            FadeOut(full_formula_mobj),
            FadeOut(visualize_text)
        )

        recap_title = create_text_formula_part("Recap: Quadratic Formula", font_size=45, color=GOLD_ACCENT).to_edge(UP, buff=0.7)
        self.play(FadeTransform(title, recap_title))
        self.wait(0.5)

        # Recreate the formula for the recap card, centered
        (
            full_formula_recap, _, _, _, _, _, _, _, _, _, _, _, _, 
            _, _, _, _, _
        ) = create_quadratic_formula_text_objects()
        full_formula_recap.scale(0.8).move_to(ORIGIN + UP * 1.5)
        self.play(FadeIn(full_formula_recap))

        recap_points = VGroup(
            create_text_formula_part("- Find 'a', 'b', 'c' from ax² + bx + c = 0", font_size=30, color=TEXT_COLOR),
            create_text_formula_part("- Plug into the formula", font_size=30, color=TEXT_COLOR),
            create_text_formula_part("- Calculate for '±' to get x1, x2 (the roots!)", font_size=30, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(full_formula_recap, DOWN, buff=0.8).align_to(full_formula_recap, LEFT).shift(LEFT * 0.5)
        
        self.play(LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.7))
        self.wait(3)
        self.play(FadeOut(self.mobjects)) # Fade out everything at the end