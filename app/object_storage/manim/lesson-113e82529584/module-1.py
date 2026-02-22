from manim import *

class SolveQuadratics(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = "#88DDFF"  # Lighter blue
        GOLD_ACCENT = "#FFD700"  # Pure gold
        TEXT_COLOR = WHITE

        # --- Helper function for quadratic graphs ---
        def create_quadratic_function(a, b, c):
            return lambda x: a * x**2 + b * x + c

        # --- Beat 1: Visual Hook & Problem Introduction (~5 seconds) ---
        # 1.1 Create Axes and NumberPlane
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-6, 6, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": GOLD_ACCENT, "include_numbers": False},
            x_axis_config={"numbers_to_exclude": [0]},
            y_axis_config={"numbers_to_exclude": [0]},
        ).add_coordinates()
        axes.to_center()
        
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-6, 6, 1],
            x_length=10,
            y_length=10,
            background_line_style={
                "stroke_color": GOLD_ACCENT,
                "stroke_width": 0.5,
                "stroke_opacity": 0.2
            }
        )
        plane.to_center()

        self.play(Create(plane), Create(axes), run_time=1.5)

        # 1.2 Draw a sample parabola
        quad_func_initial = create_quadratic_function(1, 0, -4) # y = x^2 - 4
        parabola = axes.get_graph(quad_func_initial, color=BLUE_ACCENT, x_range=[-3, 3])

        self.play(Create(parabola), run_time=1.5)

        # 1.3 Highlight roots
        root1_coords = axes.c2p(-2, 0)
        root2_coords = axes.c2p(2, 0)

        dot1 = Dot(root1_coords, color=GOLD_ACCENT, radius=0.15)
        dot2 = Dot(root2_coords, color=GOLD_ACCENT, radius=0.15)

        label_question = Text("Where does it cross the x-axis?", font_size=36, color=TEXT_COLOR)
        label_question.to_edge(UP).shift(DOWN * 0.5)

        self.play(
            FadeIn(dot1, scale=0.5), FadeIn(dot2, scale=0.5),
            Write(label_question),
            run_time=1.5
        )

        self.wait(1)
        self.play(FadeOut(parabola, dot1, dot2, label_question), run_time=1)
        self.wait(0.5) # Short pause before next beat

        # --- Beat 2: Standard Form ax² + bx + c = 0 (~7 seconds) ---
        # 2.1 Create Text for standard form (using unicode ² for simplicity, no MathTex)
        standard_form_text = Text("ax² + bx + c = 0", color=TEXT_COLOR).scale(1)
        standard_form_text.move_to(ORIGIN)

        self.play(
            Write(standard_form_text),
            run_time=2
        )

        # 2.2 Highlight coefficients
        a_char = standard_form_text[0]  # 'a'
        b_char = standard_form_text[6]  # 'b'
        c_char = standard_form_text[11] # 'c'
        
        self.play(
            a_char.animate.set_color(BLUE_ACCENT).scale(1.2),
            b_char.animate.set_color(BLUE_ACCENT).scale(1.2),
            c_char.animate.set_color(BLUE_ACCENT).scale(1.2),
            run_time=1.5
        )
        
        desc_coeffs = Text("a, b, c are coefficients", font_size=28, color=TEXT_COLOR)
        desc_coeffs.next_to(standard_form_text, DOWN, buff=0.7)
        self.play(Write(desc_coeffs), run_time=1)
        self.wait(1)

        self.play(
            FadeOut(desc_coeffs),
            a_char.animate.set_color(TEXT_COLOR).scale(1/1.2),
            b_char.animate.set_color(TEXT_COLOR).scale(1/1.2),
            c_char.animate.set_color(TEXT_COLOR).scale(1/1.2),
            run_time=1
        )
        self.wait(0.5)

        # --- Beat 3: The Quadratic Formula (~7 seconds) ---
        self.play(
            standard_form_text.animate.to_edge(UP).shift(DOWN*0.5).scale(0.7),
            FadeOut(plane), # Keep axes for now, will fade in next beat
            run_time=1.5
        )
        
        # Create formula elements (no MathTex, custom sqrt symbol)
        x_equals = Text("x =", color=TEXT_COLOR).scale(0.8)
        
        # Numerator components
        minus_b_txt = Text("-b", color=TEXT_COLOR).scale(0.8)
        plus_minus_txt = Text("±", color=TEXT_COLOR).scale(0.8)
        
        b_txt_in_b_squared = Text("b", color=TEXT_COLOR).scale(0.8)
        power2_in_b_squared = Text("2", font_size=20, color=TEXT_COLOR).move_to(b_txt_in_b_squared.get_corner(UR) + RIGHT*0.05 + UP*0.05)
        b_squared_grp = VGroup(b_txt_in_b_squared, power2_in_b_squared)

        four_ac_txt = Text("4ac", color=TEXT_COLOR).scale(0.8)
        minus_four_ac_grp = VGroup(Text(" - ", color=TEXT_COLOR).scale(0.8), four_ac_txt).arrange(RIGHT, buff=0.05)
        
        # Custom square root symbol using lines
        sqrt_line1 = Line(ORIGIN, RIGHT * 0.4, color=TEXT_COLOR, stroke_width=2)
        sqrt_line2 = Line(sqrt_line1.get_end(), sqrt_line1.get_end() + UL * 0.2, color=TEXT_COLOR, stroke_width=2)
        sqrt_line3 = Line(sqrt_line2.get_end(), sqrt_line2.get_end() + RIGHT * 0.6 + DOWN * 0.4, color=TEXT_COLOR, stroke_width=2)
        sqrt_line4 = Line(sqrt_line3.get_end(), sqrt_line3.get_end() + RIGHT * 1.5, color=TEXT_COLOR, stroke_width=2)
        sqrt_symbol_grp = VGroup(sqrt_line1, sqrt_line2, sqrt_line3, sqrt_line4).scale(0.8)
        
        radical_content_grp = VGroup(b_squared_grp, minus_four_ac_grp).arrange(RIGHT, buff=0.05)
        
        # Position sqrt symbol relative to its content
        sqrt_symbol_grp.next_to(radical_content_grp, LEFT, buff=0.05).align_to(radical_content_grp, DOWN)
        sqrt_symbol_grp.shift(UP * 0.1) # Fine tune vertical alignment

        numerator_grp = VGroup(minus_b_txt, plus_minus_txt, sqrt_symbol_grp, radical_content_grp).arrange(RIGHT, buff=0.05)
        
        # Denominator components
        denominator_line = Line(LEFT * (numerator_grp.width / 2 + 0.1), RIGHT * (numerator_grp.width / 2 + 0.1), color=TEXT_COLOR, stroke_width=2)
        two_a_txt = Text("2a", color=TEXT_COLOR).scale(0.8)
        
        # Assemble the full formula
        quadratic_formula_parts = VGroup(numerator_grp, denominator_line, two_a_txt)
        quadratic_formula_parts.arrange(DOWN, center=True, buff=0.4)
        
        x_equals.next_to(quadratic_formula_parts, LEFT, buff=0.2)
        full_formula_grp = VGroup(x_equals, quadratic_formula_parts).move_to(ORIGIN)
        full_formula_grp.scale(0.9) # Scale down slightly to fit

        # Animate formula build-up
        self.play(Write(x_equals), run_time=0.5)
        self.play(LaggedStart(
            Write(minus_b_txt),
            Write(plus_minus_txt),
            Create(sqrt_symbol_grp),
            Write(b_squared_grp),
            Write(minus_four_ac_grp),
            Create(denominator_line),
            Write(two_a_txt),
            lag_ratio=0.2,
            run_time=3
        ))
        
        self.wait(1.5)

        # --- Beat 4: Applying the Formula - Intuition (~10 seconds) ---
        # 4.1 Move formula to corner and bring back axes
        self.play(
            full_formula_grp.animate.scale(0.6).to_corner(UR).shift(LEFT*0.5 + DOWN*0.2),
            axes.animate.to_edge(DOWN).shift(UP*1.5).scale(0.7),
            run_time=1.5
        )

        # 4.2 Reintroduce the initial parabola
        # Re-initialize parabola (as axes might have scaled)
        parabola_small = axes.get_graph(create_quadratic_function(1, 0, -4), color=BLUE_ACCENT, x_range=[-2.5, 2.5])
        self.play(Create(parabola_small), run_time=1)
        
        # 4.3 Identify a, b, c for y = x² - 4
        current_eq_text = Text("For y = x² - 4:", font_size=32, color=TEXT_COLOR)
        current_eq_text.to_edge(UP).shift(DOWN*0.2)
        
        a_val_text = Text("a = 1", font_size=28, color=BLUE_ACCENT).next_to(current_eq_text, DOWN, buff=0.3).align_to(current_eq_text, LEFT)
        b_val_text = Text("b = 0", font_size=28, color=BLUE_ACCENT).next_to(a_val_text, RIGHT, buff=0.8)
        c_val_text = Text("c = -4", font_size=28, color=BLUE_ACCENT).next_to(b_val_text, RIGHT, buff=0.8)

        coeff_group_values = VGroup(a_val_text, b_val_text, c_val_text)
        
        self.play(Write(current_eq_text), FadeIn(coeff_group_values, shift=UP), run_time=1.5)

        # 4.4 Simulate plugging in values (conceptual highlighting)
        # Using the direct Mobjects from formula construction
        a_in_4ac = four_ac_txt[1] # 'a' from Text("4ac")
        c_in_4ac = four_ac_txt[2] # 'c' from Text("4ac")

        b_in_minus_b = minus_b_txt[1] # 'b' from Text("-b")
        b_in_b_squared = b_txt_in_b_squared[0] # 'b' from Text("b")

        a_in_2a = two_a_txt[1] # 'a' from Text("2a")

        self.play(
            Indicate(a_val_text),
            Indicate(a_in_4ac, color=GOLD_ACCENT),
            Indicate(a_in_2a, color=GOLD_ACCENT),
            run_time=0.8
        )
        self.play(
            Indicate(b_val_text),
            Indicate(b_in_minus_b, color=GOLD_ACCENT),
            Indicate(b_in_b_squared, color=GOLD_ACCENT),
            run_time=0.8
        )
        self.play(
            Indicate(c_val_text),
            Indicate(c_in_4ac, color=GOLD_ACCENT),
            run_time=0.8
        )

        # Show results appearing
        result_text = Text("This gives us x = -2 and x = 2", font_size=32, color=TEXT_COLOR)
        result_text.next_to(coeff_group_values, DOWN, buff=0.5)

        root1_coords_final = axes.c2p(-2, 0)
        root2_coords_final = axes.c2p(2, 0)
        dot1_final = Dot(root1_coords_final, color=GOLD_ACCENT, radius=0.1)
        dot2_final = Dot(root2_coords_final, color=GOLD_ACCENT, radius=0.1)

        solution_arrows = VGroup(
            Arrow(result_text.get_left(), dot1_final.get_top(), buff=0.1, color=GOLD_ACCENT),
            Arrow(result_text.get_right(), dot2_final.get_top(), buff=0.1, color=GOLD_ACCENT)
        )
        
        self.play(
            Write(result_text),
            FadeIn(dot1_final, dot2_final),
            GrowArrow(solution_arrows[0]),
            GrowArrow(solution_arrows[1]),
            run_time=2
        )
        self.wait(1.5)

        self.play(
            FadeOut(current_eq_text, coeff_group_values, result_text, solution_arrows, dot1_final, dot2_final, parabola_small),
            run_time=1.5
        )
        self.wait(0.5)
        
        # --- Beat 5: Recap Card (~5 seconds) ---
        recap_title = Text("Recap: Quadratic Formula", font_size=44, color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        
        recap_points = VGroup(
            Text("1. Standard Form: ax² + bx + c = 0", font_size=34, color=TEXT_COLOR),
            Text("2. Finds x-intercepts (roots)", font_size=34, color=TEXT_COLOR),
            Text("3. a, b, c are coefficients", font_size=34, color=TEXT_COLOR),
        ).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.5).shift(UP*1)
        
        # Re-create formula centered for recap (using copies of existing Mobjects for efficiency)
        recap_x_equals = x_equals.copy()
        recap_minus_b_txt = minus_b_txt.copy()
        recap_plus_minus_txt = plus_minus_txt.copy()
        recap_b_squared_grp = b_squared_grp.copy()
        recap_minus_four_ac_grp = minus_four_ac_grp.copy()
        recap_sqrt_symbol_grp = sqrt_symbol_grp.copy()

        recap_radical_content_grp = VGroup(recap_b_squared_grp, recap_minus_four_ac_grp).arrange(RIGHT, buff=0.05)
        recap_sqrt_symbol_grp.next_to(recap_radical_content_grp, LEFT, buff=0.05).align_to(recap_radical_content_grp, DOWN)
        recap_sqrt_symbol_grp.shift(UP * 0.1)

        recap_numerator_grp = VGroup(recap_minus_b_txt, recap_plus_minus_txt, recap_sqrt_symbol_grp, recap_radical_content_grp).arrange(RIGHT, buff=0.05)
        recap_denominator_line = denominator_line.copy() # Line requires specific length, will adjust
        recap_denominator_line.set_width(recap_numerator_grp.width + 0.2) # Adjust width for new group
        recap_two_a_txt = two_a_txt.copy()
        
        recap_quadratic_formula_parts = VGroup(recap_numerator_grp, recap_denominator_line, recap_two_a_txt)
        recap_quadratic_formula_parts.arrange(DOWN, center=True, buff=0.4)
        
        recap_x_equals.next_to(recap_quadratic_formula_parts, LEFT, buff=0.2)
        recap_full_formula_grp = VGroup(recap_x_equals, recap_quadratic_formula_parts).move_to(ORIGIN)
        recap_full_formula_grp.scale(0.7).next_to(recap_points, DOWN, buff=0.8)

        self.play(
            FadeOut(axes, full_formula_grp, standard_form_text),
            Write(recap_title),
            FadeIn(recap_points, shift=UP),
            FadeIn(recap_full_formula_grp, shift=UP),
            run_time=2.5
        )
        self.wait(3)
        self.play(FadeOut(self.mobjects)) # Clear scene