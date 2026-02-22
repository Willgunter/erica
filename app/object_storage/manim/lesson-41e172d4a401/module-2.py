from manim import *

# --- Custom Mobject Helpers (No Tex/MathTex allowed) ---

COLOR_BLUE = BLUE_D
COLOR_GOLD = GOLD

def get_char_mobject(char, color=COLOR_BLUE, font_size=DEFAULT_FONT_SIZE):
    """Creates a Text Mobject for a single character or number."""
    return Text(str(char), color=color, font_size=font_size)

def get_op_mobject(op, color=COLOR_GOLD, font_size=DEFAULT_FONT_SIZE):
    """Creates a Text Mobject for an operator."""
    return Text(op, color=color, font_size=font_size)

def get_superscript_mobject(base_mobject, script_str, color=COLOR_BLUE, font_size=24):
    """
    Creates a Mobject with a superscript.
    Args:
        base_mobject: The Mobject for the base (e.g., 'x').
        script_str: The string for the superscript (e.g., '2').
        color: Color for the superscript.
        font_size: Font size for the superscript.
    Returns:
        A VGroup containing the base and superscript.
    """
    script_mobject = Text(script_str, font_size=font_size, color=color)
    script_mobject.next_to(base_mobject, UP + RIGHT, buff=0.05)
    return VGroup(base_mobject, script_mobject)

def create_fraction_mobject(numerator_parts, denominator_parts, scale=0.7, color_line=COLOR_GOLD, line_buff=0.08):
    """
    Creates a fraction Mobject.
    Args:
        numerator_parts: List of Mobjects or strings for the numerator.
        denominator_parts: List of Mobjects or strings for the denominator.
        scale: Scale factor for the fraction elements.
        color_line: Color of the division line.
        line_buff: Buffer space between line and numerator/denominator.
    Returns:
        A VGroup representing the fraction.
    """
    numerator_m = VGroup(*[get_char_mobject(p, font_size=DEFAULT_FONT_SIZE*scale) if isinstance(p, str) else p for p in numerator_parts]).arrange(RIGHT, buff=0.05)
    denominator_m = VGroup(*[get_char_mobject(p, font_size=DEFAULT_FONT_SIZE*scale) if isinstance(p, str) else p for p in denominator_parts]).arrange(RIGHT, buff=0.05)
    
    line = Line(LEFT * 0.5, RIGHT * 0.5, color=color_line, stroke_width=4)
    
    max_width = max(numerator_m.get_width(), denominator_m.get_width(), line.get_width()) * 1.1
    line.set_width(max_width)

    numerator_m.move_to(line.get_center() + UP * (line.get_height() / 2 + numerator_m.get_height() / 2 + line_buff))
    denominator_m.move_to(line.get_center() + DOWN * (line.get_height() / 2 + denominator_m.get_height() / 2 + line_buff))
    
    frac = VGroup(numerator_m, line, denominator_m).scale(scale)
    return frac

def create_sqrt_symbol_mobject(height=0.6, width_extension=0.5, color=GOLD, stroke_width=4):
    """
    Creates a minimalistic square root symbol Mobject.
    Args:
        height: Target height for the 'v' part of the symbol.
        width_extension: Additional width for the top bar.
        color: Color of the symbol.
        stroke_width: Stroke width of the symbol lines.
    Returns:
        A VGroup representing the square root symbol.
    """
    v_part = Line(LEFT * 0.1, RIGHT * 0.1, color=color, stroke_width=stroke_width) # base
    v_part.add(Line(v_part.get_start(), v_part.get_start() + UP * height * 0.5 + RIGHT * 0.1, color=color, stroke_width=stroke_width))
    v_part.add(Line(v_part.get_start() + UP * height * 0.5 + RIGHT * 0.1, v_part.get_start() + UP * height * 0.9 + RIGHT * 0.3, color=color, stroke_width=stroke_width))
    
    top_bar = Line(v_part[-1].get_end(), v_part[-1].get_end() + RIGHT * width_extension, color=color, stroke_width=stroke_width)
    
    symbol = VGroup(v_part, top_bar)
    symbol.move_to(ORIGIN)
    symbol.set_height(height) # Set height of the 'v' part
    return symbol

def get_sqrt_expression_mobject(expression_mobject, symbol_color=GOLD):
    """
    Creates a square root Mobject with an expression under it.
    Args:
        expression_mobject: The Mobject to be placed under the square root.
        symbol_color: Color of the square root symbol.
    Returns:
        A VGroup containing the square root symbol and the expression.
    """
    expr_width = expression_mobject.get_width()
    expr_height = expression_mobject.get_height()
    
    sqrt_symbol = create_sqrt_symbol_mobject(height=expr_height * 1.2, width_extension=expr_width + 0.2, color=symbol_color)
    
    sqrt_symbol.next_to(expression_mobject, LEFT, buff=0.1)
    sqrt_symbol.align_to(expression_mobject, DOWN)
    sqrt_symbol.shift(UP * expr_height * 0.05) # Small lift to visually center around expression
    
    sqrt_symbol[-1].set_width(expression_mobject.get_width() + 0.2)
    sqrt_symbol[-1].next_to(sqrt_symbol[-2].get_end(), RIGHT, buff=0)

    full_sqrt = VGroup(sqrt_symbol, expression_mobject)
    full_sqrt.arrange(RIGHT, buff=0.05)
    return full_sqrt


class QuadraticFormulaDerivation(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Beat 1: Visual Hook & Introduction to Quadratics ---
        title = Text("Quadratic Formula: Derivation", color=COLOR_GOLD).scale(1.2).to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-8, 8, 1],
            x_length=12,
            y_length=10,
            axis_config={"color": GRAY},
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        ).shift(DOWN * 0.5)
        
        axes_label_x = Text("x", color=GRAY).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1)
        axes_label_y = Text("y", color=GRAY).next_to(plane.y_axis.get_end(), UP, buff=0.1)

        def parabola_func(x):
            return 0.5 * x**2 + x - 3.5

        graph = FunctionGraph(parabola_func, x_range=[-5, 3], color=COLOR_BLUE)
        
        root1_coords = plane.coords_to_point(-4.4, 0)
        root2_coords = plane.coords_to_point(2.4, 0)
        root1_dot = Dot(root1_coords, color=GOLD)
        root2_dot = Dot(root2_coords, color=GOLD)
        
        parabola_text = Text("y = ax^2 + bx + c", color=COLOR_BLUE).scale(0.8).next_to(graph, UP + RIGHT, buff=0.5)

        self.play(Create(plane), Create(axes_label_x), Create(axes_label_y))
        self.play(Create(graph), FadeIn(parabola_text))
        self.play(LaggedStart(GrowFromCenter(root1_dot), GrowFromCenter(root2_dot)), run_time=1.5)

        question_text = Text("Where does y = 0?", color=COLOR_GOLD).scale(0.7).next_to(parabola_text, DOWN, buff=0.5)
        self.play(Write(question_text))
        self.wait(2)

        initial_equation = VGroup(
            get_char_mobject("a"), get_superscript_mobject(get_char_mobject("x"), "2"), get_op_mobject("+"),
            get_char_mobject("b"), get_char_mobject("x"), get_op_mobject("+"),
            get_char_mobject("c"), get_op_mobject("="), get_char_mobject("0")
        ).arrange(RIGHT, buff=0.2).scale(0.8).to_edge(DOWN)

        self.play(
            FadeOut(parabola_text),
            FadeOut(question_text),
            FadeOut(graph),
            FadeOut(root1_dot),
            FadeOut(root2_dot),
            FadeOut(plane),
            FadeOut(axes_label_x),
            FadeOut(axes_label_y),
            FadeIn(initial_equation)
        )
        self.play(initial_equation.animate.move_to(ORIGIN))
        self.wait(1)
        self.play(FadeOut(title))
        self.wait(1)

        # --- Beat 2: Completing the Square - Intuition (Geometric) ---
        beat2_title = Text("Completing the Square: Visualized", color=COLOR_GOLD).scale(1).to_edge(UP)
        self.play(FadeIn(beat2_title, shift=UP))

        self.play(FadeOut(initial_equation, shift=DOWN))

        # Geometric representation of x^2 + bx
        x_square = Square(side_length=2, color=COLOR_BLUE, fill_opacity=0.3).move_to(LEFT * 3 + UP * 1)
        x_label_left = Text("x", color=COLOR_BLUE).next_to(x_square.get_left(), LEFT, buff=0.1)
        x_label_top = Text("x", color=COLOR_BLUE).next_to(x_square.get_top(), UP, buff=0.1)
        x_sq_label = get_superscript_mobject(get_char_mobject("x"), "2").move_to(x_square.get_center())

        self.play(Create(x_square), Write(x_label_left), Write(x_label_top), FadeIn(x_sq_label))
        self.wait(1)

        b_over_2_width = 1 # Visual width for b/2 (assuming b=2 for visualization)
        rect1 = Rectangle(width=b_over_2_width, height=2, color=COLOR_GOLD, fill_opacity=0.3).next_to(x_square, RIGHT, buff=0)
        rect2 = Rectangle(width=2, height=b_over_2_width, color=COLOR_GOLD, fill_opacity=0.3).next_to(x_square, DOWN, buff=0)
        
        b_half_text_top_right = create_fraction_mobject(["b"], ["2"], scale=0.6).next_to(rect1.get_top(), UP, buff=0.1)
        x_text_right_edge = Text("x", color=COLOR_BLUE).next_to(rect1.get_right(), RIGHT, buff=0.1)
        b_half_text_bottom_left = create_fraction_mobject(["b"], ["2"], scale=0.6).next_to(rect2.get_left(), LEFT, buff=0.1)
        x_text_bottom_edge = Text("x", color=COLOR_BLUE).next_to(rect2.get_bottom(), DOWN, buff=0.1)

        self.play(
            Create(rect1), FadeIn(b_half_text_top_right), FadeIn(x_text_right_edge),
            Create(rect2), FadeIn(b_half_text_bottom_left), FadeIn(x_text_bottom_edge)
        )
        self.wait(1.5)

        missing_square = Square(side_length=b_over_2_width, color=COLOR_BLUE, fill_opacity=0.5).next_to(rect2, RIGHT, buff=0)
        missing_label_content = VGroup(get_op_mobject("("), create_fraction_mobject(["b"], ["2"], scale=0.6), get_op_mobject(")")).arrange(RIGHT, buff=0.05)
        missing_label = get_superscript_mobject(missing_label_content, "2", font_size=20).move_to(missing_square.get_center())
        
        self.play(Create(missing_square), FadeIn(missing_label))
        self.wait(1.5)

        full_square = VGroup(x_square, rect1, rect2, missing_square)
        labels_to_fade = VGroup(x_label_left, x_label_top, x_text_right_edge, x_text_bottom_edge, 
                                b_half_text_top_right, b_half_text_bottom_left, x_sq_label, missing_label)
        self.play(full_square.animate.shift(RIGHT * 1.5 + DOWN * 0.5), FadeOut(labels_to_fade))
        
        x_plus_b_over_2_label_content = VGroup(
            get_op_mobject("("), get_char_mobject("x"), get_op_mobject("+"),
            create_fraction_mobject(["b"], ["2"], scale=0.6), get_op_mobject(")")
        ).arrange(RIGHT, buff=0.05)
        x_plus_b_over_2_sq_label = get_superscript_mobject(x_plus_b_over_2_label_content, "2", font_size=24)
        x_plus_b_over_2_sq_label.next_to(full_square, DOWN, buff=0.5)

        self.play(FadeIn(x_plus_b_over_2_sq_label))
        self.wait(2)
        
        self.play(FadeOut(full_square, x_plus_b_over_2_sq_label, beat2_title))
        self.wait(1)

        # --- Beat 3: Derivation Part 1 (Simple Case: a=1) ---
        beat3_title = Text("Derivation: Step-by-Step (a=1)", color=COLOR_GOLD).scale(1).to_edge(UP)
        self.play(FadeIn(beat3_title, shift=UP))

        # Start with x^2 + bx + c = 0
        equation_b3_1 = VGroup(
            get_superscript_mobject(get_char_mobject("x"), "2"), get_op_mobject("+"),
            get_char_mobject("b"), get_char_mobject("x"), get_op_mobject("+"),
            get_char_mobject("c"), get_op_mobject("="), get_char_mobject("0")
        ).arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN)
        self.play(FadeIn(equation_b3_1, shift=UP))
        self.wait(1)

        # x^2 + bx = -c
        equation_b3_2 = VGroup(
            get_superscript_mobject(get_char_mobject("x"), "2"), get_op_mobject("+"),
            get_char_mobject("b"), get_char_mobject("x"), get_op_mobject("="),
            get_op_mobject("-"), get_char_mobject("c")
        ).arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN)
        self.play(ReplacementTransform(equation_b3_1, equation_b3_2))
        self.wait(1)
        
        # Add (b/2)^2 to both sides
        b_over_2_sq_term_content = VGroup(get_op_mobject("("), create_fraction_mobject(["b"], ["2"], scale=0.6), get_op_mobject(")")).arrange(RIGHT, buff=0.05)
        b_over_2_sq_term = get_superscript_mobject(b_over_2_sq_term_content, "2", font_size=20)
        
        equation_b3_3 = VGroup(
            VGroup(*equation_b3_2[0:4].copy_submobjects(equation_b3_2)), get_op_mobject("+"), b_over_2_sq_term.copy(),
            VGroup(*equation_b3_2[4:].copy_submobjects(equation_b3_2)), get_op_mobject("+"), b_over_2_sq_term.copy()
        ).arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN)
        self.play(ReplacementTransform(equation_b3_2, equation_b3_3))
        self.wait(1.5)

        # (x + b/2)^2 = (b^2/4) - c
        b_sq_over_4 = create_fraction_mobject([get_superscript_mobject(get_char_mobject("b"), "2")], ["4"], scale=0.6)
        
        eq_b3_4_lhs = get_superscript_mobject(
            VGroup(get_op_mobject("("), get_char_mobject("x"), get_op_mobject("+"),
                   create_fraction_mobject(["b"], ["2"], scale=0.6), get_op_mobject(")")).arrange(RIGHT, buff=0.05), "2", font_size=20
        )
        eq_b3_4_rhs = VGroup(b_sq_over_4, get_op_mobject("-"), get_char_mobject("c")).arrange(RIGHT, buff=0.1)
        equation_b3_4 = VGroup(eq_b3_4_lhs, get_op_mobject("="), eq_b3_4_rhs).arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN)
        self.play(ReplacementTransform(equation_b3_3, equation_b3_4))
        self.wait(1.5)
        
        # x + b/2 = +/- sqrt(b^2/4 - c)
        b_sq_over_4_minus_c = VGroup(b_sq_over_4.copy(), get_op_mobject("-"), get_char_mobject("c")).arrange(RIGHT, buff=0.1)
        sqrt_rhs_expr = get_sqrt_expression_mobject(b_sq_over_4_minus_c)
        
        eq_b3_5_lhs = VGroup(
            get_char_mobject("x"), get_op_mobject("+"), create_fraction_mobject(["b"], ["2"], scale=0.6)
        ).arrange(RIGHT, buff=0.1)
        eq_b3_5_rhs = VGroup(get_op_mobject("±"), sqrt_rhs_expr).arrange(RIGHT, buff=0.1)
        equation_b3_5 = VGroup(eq_b3_5_lhs, get_op_mobject("="), eq_b3_5_rhs).arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN)
        self.play(ReplacementTransform(equation_b3_4, equation_b3_5))
        self.wait(1.5)

        # x = -b/2 +/- sqrt(b^2/4 - c)
        eq_b3_6_lhs = get_char_mobject("x")
        eq_b3_6_rhs = VGroup(
            get_op_mobject("-"), create_fraction_mobject(["b"], ["2"], scale=0.6),
            get_op_mobject("±"), sqrt_rhs_expr.copy()
        ).arrange(RIGHT, buff=0.1)
        equation_b3_6 = VGroup(eq_b3_6_lhs, get_op_mobject("="), eq_b3_6_rhs).arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN)
        self.play(ReplacementTransform(equation_b3_5, equation_b3_6))
        self.wait(2)
        
        self.play(FadeOut(equation_b3_6, beat3_title))
        self.wait(1)

        # --- Beat 4: Generalizing to ax^2 + bx + c = 0 (Full Derivation) ---
        beat4_title = Text("General Case: ax^2 + bx + c = 0", color=COLOR_GOLD).scale(1).to_edge(UP)
        self.play(FadeIn(beat4_title, shift=UP))

        # 1. ax^2 + bx + c = 0
        equation_4_1_content = VGroup(
            get_char_mobject("a"), get_superscript_mobject(get_char_mobject("x"), "2"), get_op_mobject("+"),
            get_char_mobject("b"), get_char_mobject("x"), get_op_mobject("+"),
            get_char_mobject("c"), get_op_mobject("="), get_char_mobject("0")
        )
        equation_4_1 = equation_4_1_content.copy().arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN + UP * 2.5)
        self.play(FadeIn(equation_4_1, shift=UP))
        self.wait(1)

        # 2. Divide by a: x^2 + (b/a)x + (c/a) = 0
        equation_4_2_content = VGroup(
            get_superscript_mobject(get_char_mobject("x"), "2"), get_op_mobject("+"),
            create_fraction_mobject(["b"], ["a"]), get_char_mobject("x"), get_op_mobject("+"),
            create_fraction_mobject(["c"], ["a"]), get_op_mobject("="), get_char_mobject("0")
        )
        equation_4_2 = equation_4_2_content.copy().arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN + UP * 1.5)
        self.play(ReplacementTransform(equation_4_1, equation_4_2))
        self.wait(1)

        # 3. x^2 + (b/a)x = -c/a
        equation_4_3_content = VGroup(
            get_superscript_mobject(get_char_mobject("x"), "2"), get_op_mobject("+"),
            create_fraction_mobject(["b"], ["a"]), get_char_mobject("x"), get_op_mobject("="),
            get_op_mobject("-"), create_fraction_mobject(["c"], ["a"])
        )
        equation_4_3 = equation_4_3_content.copy().arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN + UP * 0.5)
        self.play(ReplacementTransform(equation_4_2, equation_4_3))
        self.wait(1)

        # 4. Add (b/2a)^2 to both sides
        b_over_2a_sq_term_content = VGroup(get_op_mobject("("), create_fraction_mobject(["b"], ["2a"]), get_op_mobject(")")).arrange(RIGHT, buff=0.05)
        b_over_2a_sq_term = get_superscript_mobject(b_over_2a_sq_term_content, "2", font_size=20)
        
        equation_4_4_content = VGroup(
            *equation_4_3_content[0:4].copy_submobjects(equation_4_3_content), get_op_mobject("+"), b_over_2a_sq_term.copy(),
            *equation_4_3_content[4:].copy_submobjects(equation_4_3_content), get_op_mobject("+"), b_over_2a_sq_term.copy()
        )
        equation_4_4 = equation_4_4_content.copy().arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN + DOWN * 0.5)
        self.play(ReplacementTransform(equation_4_3, equation_4_4))
        self.wait(1.5)

        # 5. Factor LHS, combine RHS: (x + b/2a)^2 = (b^2 - 4ac) / (4a^2)
        eq_4_5_lhs_content = VGroup(get_op_mobject("("), get_char_mobject("x"), get_op_mobject("+"),
                   create_fraction_mobject(["b"], ["2a"]), get_op_mobject(")")).arrange(RIGHT, buff=0.05)
        eq_4_5_lhs = get_superscript_mobject(eq_4_5_lhs_content, "2", font_size=20)
        
        b_sq = get_superscript_mobject(get_char_mobject("b"), "2", font_size=24)
        four_ac = VGroup(get_char_mobject("4"), get_char_mobject("a"), get_char_mobject("c")).arrange(RIGHT, buff=0.05)
        b_sq_minus_4ac_numerator = VGroup(b_sq, get_op_mobject("-"), four_ac).arrange(RIGHT, buff=0.05)
        four_a_sq_denominator = VGroup(get_char_mobject("4"), get_superscript_mobject(get_char_mobject("a"), "2", font_size=24)).arrange(RIGHT, buff=0.05)
        eq_4_5_rhs = create_fraction_mobject([b_sq_minus_4ac_numerator], [four_a_sq_denominator], scale=0.8)

        equation_4_5_content = VGroup(eq_4_5_lhs, get_op_mobject("="), eq_4_5_rhs)
        equation_4_5 = equation_4_5_content.copy().arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN + DOWN * 1.5)
        self.play(ReplacementTransform(equation_4_4, equation_4_5))
        self.wait(2)
        
        # 6. Take square root: x + b/2a = +/- sqrt((b^2 - 4ac) / (4a^2))
        eq_4_6_lhs = VGroup(get_char_mobject("x"), get_op_mobject("+"), create_fraction_mobject(["b"], ["2a"])).arrange(RIGHT, buff=0.1)
        
        # Prepare content for square root
        sqrt_content_frac = create_fraction_mobject(
            [VGroup(b_sq.copy(), get_op_mobject("-"), four_ac.copy()).arrange(RIGHT, buff=0.05)],
            [VGroup(get_char_mobject("4"), get_superscript_mobject(get_char_mobject("a"), "2", font_size=24)).arrange(RIGHT, buff=0.05)],
            scale=0.8
        )
        sqrt_rhs_expr_v2 = get_sqrt_expression_mobject(sqrt_content_frac)
        eq_4_6_rhs = VGroup(get_op_mobject("±"), sqrt_rhs_expr_v2).arrange(RIGHT, buff=0.1)
        
        equation_4_6_content = VGroup(eq_4_6_lhs, get_op_mobject("="), eq_4_6_rhs)
        equation_4_6 = equation_4_6_content.copy().arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN + DOWN * 2.5)
        self.play(ReplacementTransform(equation_4_5, equation_4_6))
        self.wait(2)

        # 7. Simplify sqrt and isolate x: x = (-b +/- sqrt(b^2 - 4ac)) / (2a)
        final_formula_num_b = VGroup(get_op_mobject("-"), get_char_mobject("b")).arrange(RIGHT, buff=0.05)
        final_sqrt_content = VGroup(b_sq.copy(), get_op_mobject("-"), four_ac.copy()).arrange(RIGHT, buff=0.05)
        final_sqrt = get_sqrt_expression_mobject(final_sqrt_content)

        final_numerator_group = VGroup(final_formula_num_b, get_op_mobject("±"), final_sqrt).arrange(RIGHT, buff=0.1)
        final_denominator_group = VGroup(get_char_mobject("2"), get_char_mobject("a")).arrange(RIGHT, buff=0.05)
        
        final_formula_fraction = create_fraction_mobject([final_numerator_group], [final_denominator_group], scale=0.9)

        equation_4_7_content = VGroup(get_char_mobject("x"), get_op_mobject("="), final_formula_fraction)
        equation_4_7 = equation_4_7_content.copy().arrange(RIGHT, buff=0.2).scale(1).move_to(ORIGIN)
        
        self.play(FadeOut(equation_4_6), FadeOut(beat4_title))
        self.play(FadeIn(equation_4_7, scale=0.5))
        self.wait(3)

        # --- Beat 5: Recap Card ---
        self.play(FadeOut(equation_4_7))

        recap_title = Text("The Quadratic Formula", color=COLOR_GOLD).scale(1.2).to_edge(UP)
        final_formula_recap = equation_4_7.copy().scale(1.2)
        final_formula_recap.move_to(ORIGIN + UP * 0.5)

        recap_text1 = Text("Universal solution for:", color=COLOR_BLUE).scale(0.7).next_to(final_formula_recap, UP, buff=0.5)
        recap_text2_eq_content = VGroup(
            get_char_mobject("a"), get_superscript_mobject(get_char_mobject("x"), "2"), get_op_mobject("+"),
            get_char_mobject("b"), get_char_mobject("x"), get_op_mobject("+"),
            get_char_mobject("c"), get_op_mobject("="), get_char_mobject("0")
        )
        recap_text2 = recap_text2_eq_content.copy().scale(0.7).next_to(recap_text1, DOWN, buff=0.1)

        recap_text3 = Text("Finds x-intercepts of parabolas!", color=COLOR_GOLD).scale(0.7).next_to(final_formula_recap, DOWN, buff=0.5)

        self.play(FadeIn(recap_title, shift=UP))
        self.play(Write(recap_text1), Write(recap_text2))
        self.play(FadeIn(final_formula_recap))
        self.play(Write(recap_text3))
        self.wait(3)

        self.play(
            FadeOut(recap_title),
            FadeOut(final_formula_recap),
            FadeOut(recap_text1),
            FadeOut(recap_text2),
            FadeOut(recap_text3)
        )
        self.wait(1)