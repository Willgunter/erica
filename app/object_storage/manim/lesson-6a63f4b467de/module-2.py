from manim import *

# Define custom colors for 3Blue1Brown style
BLUE = "#88CCEE"  # Light blue
GOLD = "#EECC66"  # Light gold
WHITE = "#FFFFFF" # White for main text
BLACK = "#000000" # Background

# Helper for superscripts (accepts base_text and exponent_text)
def create_superscript_mobject(base_mobject, exponent_mobject, scale_exponent=0.6, shift_exponent_right=0.05, shift_exponent_up=0.25):
    exponent_mobject.scale(scale_exponent)
    # Position relative to the *last* character of the base_mobject if it's Text
    if isinstance(base_mobject, Text):
        # Find the last character if base_mobject is a VGroup of chars
        if isinstance(base_mobject, VGroup) and len(base_mobject) > 0:
            last_char_of_base = base_mobject[-1]
        else:
            last_char_of_base = base_mobject # Assume it's a single Text mobject
        exponent_mobject.next_to(last_char_of_base, UP + RIGHT, buff=SMALL_BUFF)
    else: # If base is a more complex mobject, position relative to its top-right corner
        exponent_mobject.next_to(base_mobject.get_corner(UP + RIGHT), buff=SMALL_BUFF)

    # Manual fine-tuning for placement
    exponent_mobject.shift(RIGHT * shift_exponent_right + UP * shift_exponent_up)
    return VGroup(base_mobject, exponent_mobject)

# Helper for fractions (accepts Mobjects for numerator and denominator)
def create_fraction_mobject(numerator_mobject, denominator_mobject, color=WHITE, font_size=40):
    line = Line(LEFT * 0.5, RIGHT * 0.5, color=color, stroke_width=2)
    
    # Set line width based on content
    max_width = max(numerator_mobject.width, denominator_mobject.width) * 1.2
    line.set_width(max_width)
    
    numerator_mobject.next_to(line, UP, buff=0.1)
    denominator_mobject.next_to(line, DOWN, buff=0.1)

    # Center num/den relative to the line (important for aesthetic balance)
    numerator_mobject.move_to(line.get_center() + UP * (line.height/2 + numerator_mobject.height/2 + 0.1))
    denominator_mobject.move_to(line.get_center() + DOWN * (line.height/2 + denominator_mobject.height/2 + 0.1))
    
    return VGroup(numerator_mobject, line, denominator_mobject)

# Helper for basic square root symbol (not perfect but avoids Tex)
def create_square_root_mobject(content_mobject, color=GOLD, scale=1.0):
    # This is a very basic visual representation.
    content_width = content_mobject.width
    content_height = content_mobject.height

    # Create the horizontal bar
    horizontal_bar = Line(RIGHT * 0.1, RIGHT * (content_width + 0.3), color=color, stroke_width=4)
    horizontal_bar.move_to(content_mobject.get_center() + UP * (content_height / 2 + 0.1))
    
    # Create the main part of the root symbol (a checkmark shape)
    v1 = Point(LEFT * 0.2 + DOWN * 0.1)
    v2 = Point(LEFT * 0.05 + DOWN * 0.4)
    v3 = Point(RIGHT * 0.05 + UP * 0.2)
    
    root_lines = VGroup(
        Line(v1.get_center(), v2.get_center(), color=color, stroke_width=4),
        Line(v2.get_center(), v3.get_center(), color=color, stroke_width=4)
    )
    
    root_symbol_core = VGroup(root_lines, horizontal_bar)
    root_symbol_core.move_to(content_mobject.get_center() + LEFT * (content_width / 2 + 0.3) + UP * 0.05)
    
    symbol_and_content = VGroup(root_symbol_core, content_mobject)
    
    return symbol_and_content.scale(scale)


class DeriveQuadraticFormula(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Visual Hook ---
        title = Text("Deriving the Quadratic Formula", color=GOLD, font_size=50).to_edge(UP)
        self.play(Write(title))
        
        # Manually assemble initial equation ax^2 + bx + c = 0
        ax_m = Text("a", color=BLUE)
        x_m = Text("x", color=BLUE)
        exp2_m = Text("2", color=WHITE, font_size=20)
        ax2 = create_superscript_mobject(VGroup(ax_m, x_m.next_to(ax_m, RIGHT, buff=0.05)), exp2_m, shift_exponent_right=0.01, shift_exponent_up=0.15)
        
        bx = Text(" + bx", color=BLUE, font_size=40).next_to(ax2, RIGHT, buff=0.1)
        c = Text(" + c", color=BLUE, font_size=40).next_to(bx, RIGHT, buff=0.1)
        equals_zero = Text(" = 0", color=BLUE, font_size=40).next_to(c, RIGHT, buff=0.1)
        
        initial_equation = VGroup(ax2, bx, c, equals_zero).center().shift(UP*1.5)

        # Show parabola and its roots
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-3, 5, 1],
            x_length=10, y_length=8,
            axis_config={"color": GRAY, "stroke_width": 1},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.4}
        ).scale(0.6).to_edge(DOWN).shift(LEFT*2)
        
        parabola = lambda x: 0.5 * (x - 1) * (x + 3) # Example parabola for visual
        curve = plane.plot(parabola, x_range=[-4, 2], color=GOLD)
        
        root1_dot = Dot(plane.c2p(1, 0), color=BLUE, radius=0.08)
        root2_dot = Dot(plane.c2p(-3, 0), color=BLUE, radius=0.08)
        root_label1 = Text("x = 1", color=BLUE, font_size=25).next_to(root1_dot, DOWN)
        root_label2 = Text("x = -3", color=BLUE, font_size=25).next_to(root2_dot, DOWN)

        roots_group = VGroup(root1_dot, root2_dot, root_label1, root_label2)
        
        self.play(
            Create(plane),
            Create(curve),
            run_time=1.5
        )
        self.play(
            FadeIn(roots_group),
            Write(initial_equation.copy().scale(0.8).shift(RIGHT*3)), # Show equation next to parabola
            run_time=2
        )
        self.wait(1)
        self.play(
            FadeOut(plane, curve, roots_group),
            initial_equation.animate.center().shift(UP*1.5),
            FadeOut(title),
            run_time=1.5
        )

        # Beat 1: Divide by 'a'
        beat1_title = Text("Step 1: Divide by 'a'", color=GOLD, font_size=40).to_edge(UP)
        self.play(FadeIn(beat1_title))
        current_eq = initial_equation
        self.play(current_eq.animate.shift(UP * 1.5))

        div_line_x2 = Line(LEFT*0.3, RIGHT*0.3, color=WHITE).next_to(ax2[0], DOWN, buff=0.1)
        div_a_x2 = Text("a", color=WHITE, font_size=25).next_to(div_line_x2, DOWN, buff=0.1)
        div_line_bx = Line(LEFT*0.3, RIGHT*0.3, color=WHITE).next_to(bx[1], DOWN, buff=0.1) # 'x' in 'bx'
        div_a_bx = Text("a", color=WHITE, font_size=25).next_to(div_line_bx, DOWN, buff=0.1)
        div_line_c = Line(LEFT*0.3, RIGHT*0.3, color=WHITE).next_to(c[1], DOWN, buff=0.1) # 'c'
        div_a_c = Text("a", color=WHITE, font_size=25).next_to(div_line_c, DOWN, buff=0.1)
        div_line_0 = Line(LEFT*0.3, RIGHT*0.3, color=WHITE).next_to(equals_zero[1], DOWN, buff=0.1) # '0'
        div_a_0 = Text("a", color=WHITE, font_size=25).next_to(div_line_0, DOWN, buff=0.1)

        div_mobjects = VGroup(
            VGroup(div_line_x2, div_a_x2),
            VGroup(div_line_bx, div_a_bx),
            VGroup(div_line_c, div_a_c),
            VGroup(div_line_0, div_a_0)
        )
        div_mobjects[0].align_to(current_eq[0], RIGHT).shift(LEFT*0.5)
        div_mobjects[1].align_to(current_eq[1], RIGHT).shift(LEFT*0.1)
        div_mobjects[2].align_to(current_eq[2], RIGHT).shift(LEFT*0.1)
        div_mobjects[3].align_to(current_eq[3], RIGHT).shift(LEFT*0.1)

        self.play(LaggedStart(*[FadeIn(m) for m in div_mobjects], lag_ratio=0.5))
        self.wait(1)

        # New equation after dividing
        x2_term = create_superscript_mobject(Text("x", color=BLUE, font_size=40), Text("2", color=WHITE, font_size=20), shift_exponent_right=0.01, shift_exponent_up=0.15)
        
        b_a_m = create_fraction_mobject(Text("b", color=BLUE, font_size=30), Text("a", color=BLUE, font_size=30), color=BLUE, scale=0.8)
        bx_a_term = VGroup(Text(" + ", color=BLUE, font_size=40), b_a_m.shift(UP*0.05), Text("x", color=BLUE, font_size=40))
        bx_a_term[1].next_to(bx_a_term[0], RIGHT, buff=0.05)
        bx_a_term[2].next_to(bx_a_term[1], RIGHT, buff=0.05)
        
        c_a_m = create_fraction_mobject(Text("c", color=BLUE, font_size=30), Text("a", color=BLUE, font_size=30), color=BLUE, scale=0.8)
        c_a_term = VGroup(Text(" + ", color=BLUE, font_size=40), c_a_m.shift(UP*0.05))
        c_a_term[1].next_to(c_a_term[0], RIGHT, buff=0.05)

        new_eq_line1_equals_zero = Text(" = 0", color=BLUE, font_size=40)
        
        new_eq_line1 = VGroup(x2_term, bx_a_term, c_a_term, new_eq_line1_equals_zero).arrange(RIGHT, buff=0.1).center().shift(DOWN*1)

        self.play(
            FadeOut(div_mobjects),
            Transform(current_eq, new_eq_line1),
            run_time=2
        )
        self.wait(1)

        # Beat 2: Move c/a to the right
        beat2_title = Text("Step 2: Isolate x terms", color=GOLD, font_size=40).to_edge(UP)
        self.play(
            ReplacementTransform(beat1_title, beat2_title),
            current_eq.animate.shift(UP * 1.5)
        )
        
        # New equation parts for the move
        left_side = VGroup(current_eq[0], current_eq[1]) # x^2 + (b/a)x
        
        equals_sign = Text(" = ", color=BLUE, font_size=40)
        neg_c_a = VGroup(Text("-", color=BLUE, font_size=40), create_fraction_mobject(Text("c", color=BLUE, font_size=30), Text("a", color=BLUE, font_size=30), color=BLUE, scale=0.8).shift(UP*0.05))
        neg_c_a[1].next_to(neg_c_a[0], RIGHT, buff=0.05)

        new_eq_line2 = VGroup(left_side, equals_sign, neg_c_a).arrange(RIGHT, buff=0.1).center().shift(DOWN * 1)

        self.play(
            ReplacementTransform(current_eq, new_eq_line2),
            run_time=2
        )
        self.wait(1)

        # Beat 3: Completing the Square
        beat3_title = Text("Step 3: Complete the Square", color=GOLD, font_size=40).to_edge(UP)
        self.play(
            ReplacementTransform(beat2_title, beat3_title),
            new_eq_line2.animate.shift(UP * 1.5)
        )
        current_eq = new_eq_line2

        # Visuals for completing the square
        square_x = Square(side_length=2, color=BLUE, fill_opacity=0.5).shift(LEFT * 3 + DOWN * 1.5)
        text_x2_geom = create_superscript_mobject(Text("x", color=WHITE, font_size=30), Text("2", color=WHITE, font_size=20)).move_to(square_x.get_center())
        
        rectangle_b_a_x = Rectangle(width=2, height=1, color=GOLD, fill_opacity=0.5).next_to(square_x, RIGHT, buff=0)
        text_b_a_x_geom = VGroup(create_fraction_mobject(Text("b", color=WHITE, font_size=25), Text("a", color=WHITE, font_size=25), color=WHITE, scale=0.7), Text("x", color=WHITE, font_size=30)).arrange(RIGHT, buff=0.05).move_to(rectangle_b_a_x.get_center())
        
        self.play(Create(square_x), Write(text_x2_geom), run_time=1)
        self.play(Create(rectangle_b_a_x), Write(text_b_a_x_geom), run_time=1)
        self.wait(0.5)

        # Split the rectangle
        rectangle_b_a_x_top = Rectangle(width=2, height=0.5, color=GOLD, fill_opacity=0.5).align_to(rectangle_b_a_x, UP)
        rectangle_b_a_x_bottom = Rectangle(width=2, height=0.5, color=GOLD, fill_opacity=0.5).align_to(rectangle_b_a_x, DOWN)
        text_b_2a_x_top = VGroup(create_fraction_mobject(Text("b", color=WHITE, font_size=25), Text("2a", color=WHITE, font_size=25), color=WHITE, scale=0.7), Text("x", color=WHITE, font_size=30)).arrange(RIGHT, buff=0.05).move_to(rectangle_b_a_x_top.get_center())
        text_b_2a_x_bottom = VGroup(create_fraction_mobject(Text("b", color=WHITE, font_size=25), Text("2a", color=WHITE, font_size=25), color=WHITE, scale=0.7), Text("x", color=WHITE, font_size=30)).arrange(RIGHT, buff=0.05).move_to(rectangle_b_a_x_bottom.get_center())

        self.play(
            FadeOut(rectangle_b_a_x, text_b_a_x_geom),
            FadeIn(rectangle_b_a_x_top, rectangle_b_a_x_bottom),
            FadeIn(text_b_2a_x_top, text_b_2a_x_bottom),
            run_time=1
        )
        self.wait(0.5)

        # Move bottom rectangle to the right
        self.play(
            rectangle_b_a_x_bottom.animate.next_to(square_x, DOWN, buff=0).rotate(PI/2),
            text_b_2a_x_bottom.animate.next_to(square_x, DOWN, buff=0).rotate(PI/2),
            run_time=1
        )
        text_b_2a_x_bottom.set_rotation(0).move_to(rectangle_b_a_x_bottom.get_center()) # Fix text rotation
        self.wait(0.5)
        
        # Add the missing square
        small_square_side = rectangle_b_a_x_bottom.height # Should be 0.5
        missing_square = Square(side_length=small_square_side, color=BLUE, fill_opacity=0.5).next_to(rectangle_b_a_x_top, DOWN, buff=0).align_to(rectangle_b_a_x_bottom, RIGHT)
        
        missing_frac_m = create_fraction_mobject(Text("b", color=WHITE, font_size=20), Text("2a", color=WHITE, font_size=20), color=WHITE, scale=0.6)
        missing_square_text = create_superscript_mobject(VGroup(Text("(", color=WHITE, font_size=25), missing_frac_m, Text(")", color=WHITE, font_size=25)).arrange(RIGHT, buff=0.01), Text("2", color=WHITE, font_size=15)).move_to(missing_square.get_center())
        
        self.play(Create(missing_square), Write(missing_square_text), run_time=1)
        self.wait(1)

        # Fade out geometry
        self.play(
            FadeOut(square_x, text_x2_geom, rectangle_b_a_x_top, text_b_2a_x_top, 
                    rectangle_b_a_x_bottom, text_b_2a_x_bottom, missing_square, missing_square_text),
            run_time=1.5
        )

        # Formal equation for completing the square
        # Add (b/2a)^2 to both sides
        b_2a_frac = create_fraction_mobject(Text("b", color=BLUE, font_size=30), Text("2a", color=BLUE, font_size=30), color=BLUE, scale=0.8)
        plus_b_2a_sq = create_superscript_mobject(VGroup(Text(" + (", color=BLUE, font_size=40), b_2a_frac.shift(UP*0.05), Text(")", color=BLUE, font_size=40)).arrange(RIGHT, buff=0.01), Text("2", color=WHITE, font_size=20))
        
        # Re-construct left side with the added term
        left_side_new = VGroup(current_eq[0], current_eq[1]) # x^2 + (b/a)x
        new_left_side_full = VGroup(left_side_new, plus_b_2a_sq).arrange(RIGHT, buff=0.1)

        # Right side with added term
        right_side_current = VGroup(current_eq[2]) # = -c/a
        
        # Clone the + (b/2a)^2 for the right side
        plus_b_2a_sq_right = create_superscript_mobject(VGroup(Text(" + (", color=BLUE, font_size=40), b_2a_frac.copy().shift(UP*0.05), Text(")", color=BLUE, font_size=40)).arrange(RIGHT, buff=0.01), Text("2", color=WHITE, font_size=20))

        new_eq_line3 = VGroup(new_left_side_full, right_side_current, plus_b_2a_sq_right).arrange(RIGHT, buff=0.1).center().shift(DOWN * 1)
        
        self.play(
            FadeOut(current_eq),
            FadeIn(new_eq_line3),
            run_time=2
        )
        self.wait(1)

        # Simplify left side to (x + b/2a)^2
        simplified_left_frac = create_fraction_mobject(Text("b", color=BLUE, font_size=30), Text("2a", color=BLUE, font_size=30), color=BLUE, scale=0.8)
        simplified_left = create_superscript_mobject(VGroup(Text("(", color=BLUE, font_size=40), Text("x", color=BLUE, font_size=40), Text(" + ", color=BLUE, font_size=40), simplified_left_frac.shift(UP*0.05), Text(")", color=BLUE, font_size=40)).arrange(RIGHT, buff=0.01), Text("2", color=WHITE, font_size=20))
        
        equals_sign_simplified = Text(" = ", color=BLUE, font_size=40)
        
        # Simplify right side: -c/a + b^2/4a^2 = (b^2 - 4ac) / 4a^2
        num_b2_m = create_superscript_mobject(Text("b", color=BLUE, font_size=30), Text("2", color=WHITE, font_size=20))
        num_minus_4ac_m = Text(" - 4ac", color=BLUE, font_size=30).next_to(num_b2_m, RIGHT, buff=0.05)
        numerator_mobject = VGroup(num_b2_m, num_minus_4ac_m)

        den_4a2_m = create_superscript_mobject(Text("4a", color=BLUE, font_size=30), Text("2", color=WHITE, font_size=20))
        
        final_right_fraction = create_fraction_mobject(numerator_mobject, den_4a2_m, color=BLUE, scale=0.8)
        
        new_eq_line4 = VGroup(simplified_left, equals_sign_simplified, final_right_fraction.shift(UP*0.05)).arrange(RIGHT, buff=0.1).center().shift(DOWN*1)

        self.play(
            Transform(new_eq_line3, new_eq_line4),
            run_time=2
        )
        self.wait(1)

        # Beat 4: Take square root & Isolate x
        beat4_title = Text("Step 4: Take Square Root & Isolate x", color=GOLD, font_size=40).to_edge(UP)
        self.play(
            ReplacementTransform(beat3_title, beat4_title),
            new_eq_line4.animate.shift(UP * 1.5)
        )
        current_eq = new_eq_line4

        # Left side: sqrt((x + b/2a)^2) -> x + b/2a
        x_plus_b_2a_frac = create_fraction_mobject(Text("b", color=BLUE, font_size=30), Text("2a", color=BLUE, font_size=30), color=BLUE, scale=0.8)
        x_plus_b_2a = VGroup(Text("x", color=BLUE, font_size=40), Text(" + ", color=BLUE, font_size=40), x_plus_b_2a_frac.shift(UP*0.05)).arrange(RIGHT, buff=0.01)
        
        equals_pm_sign = VGroup(Text(" = ", color=BLUE, font_size=40), Text("±", color=GOLD, font_size=40)).arrange(RIGHT, buff=0.05)
        
        # Right side: sqrt((b^2 - 4ac) / 4a^2)
        # Numerator: sqrt(b^2 - 4ac)
        sqrt_numerator_b2_m = create_superscript_mobject(Text("b", color=BLUE, font_size=25), Text("2", color=WHITE, font_size=15))
        sqrt_numerator_minus_4ac_m = Text(" - 4ac", color=BLUE, font_size=25).next_to(sqrt_numerator_b2_m, RIGHT, buff=0.05)
        sqrt_numerator_content = VGroup(sqrt_numerator_b2_m, sqrt_numerator_minus_4ac_m).arrange(RIGHT, buff=0.01)
        
        sqrt_numerator_mobject = create_square_root_mobject(sqrt_numerator_content, color=BLUE, scale=0.8)
        
        # Denominator: sqrt(4a^2) -> 2a
        denom_2a = Text("2a", color=BLUE, font_size=30)

        right_side_sqrt_fraction = create_fraction_mobject(sqrt_numerator_mobject.shift(LEFT*0.05), denom_2a, color=BLUE, scale=0.8) # Adjust sqrt position within fraction
        
        new_eq_line5 = VGroup(x_plus_b_2a, equals_pm_sign, right_side_sqrt_fraction.shift(UP*0.05)).arrange(RIGHT, buff=0.1).center().shift(DOWN*1)

        self.play(
            Transform(current_eq, new_eq_line5),
            run_time=2
        )
        self.wait(1)

        # Isolate x
        isolated_x = Text("x", color=BLUE, font_size=40)
        equals_sign_final = Text(" = ", color=BLUE, font_size=40)
        
        neg_b = Text("-b", color=BLUE, font_size=40)
        pm_symbol = Text("±", color=GOLD, font_size=40)
        
        # Reconstruct the numerator: -b ± sqrt(b^2 - 4ac)
        final_numerator_content = VGroup(
            neg_b, 
            pm_symbol.next_to(neg_b, RIGHT, buff=0.1),
            sqrt_numerator_mobject.copy().next_to(pm_symbol, RIGHT, buff=0.1)
        )
        
        final_denominator = Text("2a", color=BLUE, font_size=40)
        
        final_formula_frac = create_fraction_mobject(final_numerator_content, final_denominator, color=BLUE, scale=1.0)
        
        final_formula = VGroup(isolated_x, equals_sign_final, final_formula_frac).arrange(RIGHT, buff=0.1).center().shift(DOWN*1)

        self.play(
            Transform(new_eq_line5, final_formula),
            run_time=3
        )
        self.wait(2)

        # Recap Card
        self.play(FadeOut(final_formula, beat4_title))
        recap_title = Text("Recap: Quadratic Formula", color=GOLD, font_size=50).to_edge(UP)
        
        # Assemble the full formula for recap, ensure proper scaling and positioning
        x_recap = Text("x", color=BLUE)
        equals_recap = Text(" = ", color=BLUE)

        b_recap = Text("-b", color=BLUE)
        pm_recap = Text("±", color=GOLD)
        
        b2_recap_m = create_superscript_mobject(Text("b", color=BLUE), Text("2", color=WHITE, font_size=20), shift_exponent_right=0.01, shift_exponent_up=0.15)
        minus_4ac_recap = Text(" - 4ac", color=BLUE).next_to(b2_recap_m, RIGHT, buff=0.05)
        sqrt_content_recap = VGroup(b2_recap_m, minus_4ac_recap)
        sqrt_recap = create_square_root_mobject(sqrt_content_recap, color=BLUE, scale=0.8)

        numerator_recap = VGroup(b_recap, pm_recap.next_to(b_recap, RIGHT, buff=0.1), sqrt_recap.next_to(pm_recap, RIGHT, buff=0.1)).arrange(RIGHT, buff=0.1)
        
        denominator_recap = Text("2a", color=BLUE)
        
        formula_frac_recap = create_fraction_mobject(numerator_recap, denominator_recap, color=BLUE, scale=1.2) # Larger for recap

        recap_formula_display = VGroup(x_recap, equals_recap.next_to(x_recap, RIGHT, buff=0.1), formula_frac_recap.next_to(equals_recap, RIGHT, buff=0.1)).center()

        self.play(FadeIn(recap_title), Write(recap_formula_display))
        self.wait(3)