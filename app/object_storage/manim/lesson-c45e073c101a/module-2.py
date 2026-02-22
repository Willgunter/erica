from manim import *

# Define colors for 3Blue1Brown style
BG_COLOR = "#000000"  # Black background
ACCENT_BLUE = "#50BFE6" # A vivid blue
ACCENT_GOLD = "#FFD700" # Gold
TEXT_COLOR = "#FFFFFF" # White text
HIGHLIGHT_COLOR = "#FF6347" # Tomato red for highlights

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- Helper for creating styled Text objects for math expressions ---
        # This function creates VGroups for superscripts, which is necessary without Tex/MathTex.
        def create_math_text(text_str, color=TEXT_COLOR, font_size=40):
            if "^" in text_str:
                base, power = text_str.split("^")
                base_mobj = Text(base, color=color, font_size=font_size)
                power_mobj = Text(power, color=color, font_size=font_size * 0.7).next_to(base_mobj, UP + RIGHT, buff=0.05)
                return VGroup(base_mobj, power_mobj)
            return Text(text_str, color=color, font_size=font_size)

        # --- BEAT 1: Visual Hook & The Problem Setup ---
        title = Text("Solving Equations: The Quadratic Formula", color=ACCENT_GOLD, font_size=55)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.8))

        # Setup Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": ACCENT_BLUE, "include_numbers": False},
            x_axis_config={"tip_length": 0.2},
            y_axis_config={"tip_length": 0.2}
        ).shift(DOWN * 0.5)
        x_label = Text("x", color=ACCENT_BLUE, font_size=30).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("y", color=ACCENT_BLUE, font_size=30).next_to(axes.y_axis, UP, buff=0.1)
        axes_labels = VGroup(x_label, y_label)

        # Function: y = x^2 - 4
        def func1(x):
            return x**2 - 4
        graph1 = axes.plot(func1, color=ACCENT_GOLD)
        
        # Initial parabola animation
        self.play(
            LaggedStart(
                Create(axes),
                Create(axes_labels),
                run_time=2,
                lag_ratio=0.5
            )
        )
        
        intro_parabola_text = create_math_text("y = x^2 - 4", font_size=35).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Create(graph1), Write(intro_parabola_text))
        
        roots_dots_1 = VGroup(
            Dot(axes.c2p(-2, 0), color=HIGHLIGHT_COLOR),
            Dot(axes.c2p(2, 0), color=HIGHLIGHT_COLOR)
        )
        
        # Arrows pointing to the roots
        arrow1 = Arrow(start=ORIGIN, end=roots_dots_1[0].get_center(), color=HIGHLIGHT_COLOR).next_to(roots_dots_1[0], DOWN*0.5+LEFT*0.5)
        arrow2 = Arrow(start=ORIGIN, end=roots_dots_1[1].get_center(), color=HIGHLIGHT_COLOR).next_to(roots_dots_1[1], DOWN*0.5+RIGHT*0.5)
        
        question_text = Text("Where does y = 0?", color=ACCENT_BLUE, font_size=35).next_to(intro_parabola_text, DOWN, buff=0.5)
        self.play(FadeIn(roots_dots_1, shift=UP), Create(arrow1), Create(arrow2), Write(question_text))
        self.wait(1.5)
        
        # Transition to general quadratic equation
        self.play(
            FadeOut(graph1, roots_dots_1, arrow1, arrow2, intro_parabola_text, question_text, shift=DOWN),
            axes.animate.shift(UP*1.5).scale(0.8) # Shift axes up slightly for the equation
        )
        
        # General quadratic equation text construction
        a_text = create_math_text("a", color=ACCENT_GOLD)
        x_squared = create_math_text("x^2", color=TEXT_COLOR)
        plus_b = create_math_text("+ b", color=ACCENT_GOLD)
        x_text = create_math_text("x", color=TEXT_COLOR)
        plus_c = create_math_text("+ c", color=ACCENT_GOLD)
        equals_zero = create_math_text("= 0", color=TEXT_COLOR)

        equation_parts = VGroup(a_text, x_squared, plus_b, x_text, plus_c, equals_zero).arrange(RIGHT, buff=0.2)
        equation_parts.move_to(ORIGIN + UP*1.5)

        # Refine superscript position after arrange (as arrange can alter relative positions)
        x_squared.submobjects[1].next_to(x_squared.submobjects[0], UP+RIGHT, buff=0.05)
        
        # Highlight a, b, c
        a_rect = SurroundingRectangle(a_text, color=ACCENT_BLUE, buff=0.1)
        b_rect = SurroundingRectangle(plus_b.submobjects[0], color=ACCENT_BLUE, buff=0.1) # just 'b'
        c_rect = SurroundingRectangle(plus_c.submobjects[0], color=ACCENT_BLUE, buff=0.1) # just 'c'

        equation_desc = Text("General Quadratic Equation", font_size=35, color=ACCENT_BLUE).next_to(equation_parts, UP, buff=0.8)

        self.play(Write(equation_desc), Create(equation_parts))
        self.play(Create(a_rect), Create(b_rect), Create(c_rect))
        self.wait(1)
        
        self.play(
            FadeOut(a_rect, b_rect, c_rect),
            FadeOut(axes, axes_labels, shift=DOWN),
            FadeOut(equation_desc, shift=UP),
            equation_parts.animate.move_to(UP * 2.5).scale(0.7)
        )

        # --- BEAT 2: The Formula Appears ---
        # Construct the quadratic formula piece by piece using create_math_text
        x_eq = create_math_text("x =", font_size=45, color=ACCENT_GOLD).shift(LEFT * 4)
        
        # Numerator parts
        minus_b = create_math_text("-b", font_size=45)
        plus_minus = create_math_text("±", font_size=45, color=ACCENT_BLUE)
        
        sqrt_symbol = create_math_text("√", font_size=70).scale(1.2).shift(LEFT * 0.1) # Emulate square root symbol
        b_squared_term = create_math_text("b^2", font_size=45)
        minus_4ac = create_math_text("-4ac", font_size=45)
        
        b_squared_term.submobjects[1].next_to(b_squared_term.submobjects[0], UP+RIGHT, buff=0.05)

        # Numerator content under the square root
        numerator_sqrt_content = VGroup(b_squared_term, minus_4ac).arrange(RIGHT, buff=0.1)
        sqrt_expr = VGroup(sqrt_symbol, numerator_sqrt_content).arrange(RIGHT, buff=0.1).shift(UP * 0.05) # Adjust for sqrt symbol height

        # Full numerator group
        numerator = VGroup(minus_b, plus_minus, sqrt_expr).arrange(RIGHT, buff=0.1).shift(RIGHT*0.2)
        
        # Fraction line
        fraction_line = Line(LEFT * 2, RIGHT * 2, color=TEXT_COLOR).next_to(numerator, DOWN, buff=0.3)
        
        # Denominator
        two_a = create_math_text("2a", font_size=45).next_to(fraction_line, DOWN, buff=0.3)
        
        # Show formula appearing
        formula_title = Text("The Quadratic Formula", font_size=45, color=ACCENT_BLUE).next_to(VGroup(numerator, fraction_line, two_a), UP, buff=1.0)
        
        self.play(FadeIn(formula_title))
        self.play(
            Create(x_eq),
            Create(minus_b),
            Create(plus_minus),
            Create(sqrt_symbol),
            Create(b_squared_term),
            Create(minus_4ac),
            Create(fraction_line),
            Create(two_a),
            run_time=3,
            lag_ratio=0.1
        )
        self.wait(1)

        # Map a, b, c from general equation to formula
        map_a = Arrow(equation_parts.submobjects[0].get_center(), two_a.submobjects[1].get_center(), color=ACCENT_GOLD, buff=0.2, max_tip_length_to_length_ratio=0.1)
        map_b1 = Arrow(equation_parts.submobjects[2].submobjects[0].get_center(), minus_b.get_center(), color=ACCENT_GOLD, buff=0.2, max_tip_length_to_length_ratio=0.1)
        map_b2 = Arrow(equation_parts.submobjects[2].submobjects[0].get_center(), b_squared_term.submobjects[0].get_center(), color=ACCENT_GOLD, buff=0.2, max_tip_length_to_length_ratio=0.1)
        map_c = Arrow(equation_parts.submobjects[4].submobjects[0].get_center(), minus_4ac.submobjects[2].get_center(), color=ACCENT_GOLD, buff=0.2, max_tip_length_to_length_ratio=0.1)
        
        self.play(
            FadeIn(map_a),
            FadeIn(map_b1),
            FadeIn(map_b2),
            FadeIn(map_c)
        )
        self.wait(2)
        
        self.play(
            FadeOut(map_a, map_b1, map_b2, map_c),
            FadeOut(equation_parts, shift=UP),
            formula_title.animate.to_edge(UP).scale(0.8),
            VGroup(x_eq, numerator, fraction_line, two_a).animate.scale(0.9).shift(UP*0.5)
        )
        self.wait(1)

        # --- BEAT 3: Applying the Formula - Example ---
        example_equation_text = Text("Example: x^2 - 4x + 3 = 0", color=ACCENT_BLUE, font_size=40).next_to(formula_title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Write(example_equation_text))

        # Example equation parts (manual construction)
        ex_a = create_math_text("1", color=ACCENT_GOLD)
        ex_x2 = create_math_text("x^2", color=TEXT_COLOR)
        ex_minus_4 = create_math_text("- 4", color=ACCENT_GOLD)
        ex_x = create_math_text("x", color=TEXT_COLOR)
        ex_plus_3 = create_math_text("+ 3", color=ACCENT_GOLD)
        ex_equals_0 = create_math_text("= 0", color=TEXT_COLOR)

        example_equation = VGroup(ex_a, ex_x2, ex_minus_4, ex_x, ex_plus_3, ex_equals_0).arrange(RIGHT, buff=0.2)
        example_equation.next_to(example_equation_text, DOWN, buff=0.3).align_to(example_equation_text, LEFT)
        ex_x2.submobjects[1].next_to(ex_x2.submobjects[0], UP+RIGHT, buff=0.05)

        self.play(Create(example_equation))

        # Identify a, b, c for the example
        a_val_text = create_math_text("a = 1", font_size=35, color=ACCENT_BLUE).next_to(example_equation, DOWN, buff=0.5).shift(LEFT*2)
        b_val_text = create_math_text("b = -4", font_size=35, color=ACCENT_BLUE).next_to(a_val_text, RIGHT, buff=1)
        c_val_text = create_math_text("c = 3", font_size=35, color=ACCENT_BLUE).next_to(b_val_text, RIGHT, buff=1)
        
        self.play(Write(a_val_text), Write(b_val_text), Write(c_val_text))
        self.wait(1)

        # Create new formula components with substituted values for transformation
        x_eq_subs = x_eq.copy()
        
        minus_b_subs = create_math_text("-(-4)", font_size=45)
        plus_minus_subs = plus_minus.copy()
        sqrt_symbol_subs = sqrt_symbol.copy()
        
        b_squared_subs = create_math_text("(-4)^2", font_size=45)
        b_squared_subs.submobjects[1].next_to(b_squared_subs.submobjects[0], UP+RIGHT, buff=0.05)
        
        minus_4ac_subs = create_math_text("-4(1)(3)", font_size=45)

        numerator_sqrt_content_subs = VGroup(b_squared_subs, minus_4ac_subs).arrange(RIGHT, buff=0.1)
        sqrt_expr_subs = VGroup(sqrt_symbol_subs, numerator_sqrt_content_subs).arrange(RIGHT, buff=0.1).shift(UP * 0.05)

        numerator_subs = VGroup(minus_b_subs, plus_minus_subs, sqrt_expr_subs).arrange(RIGHT, buff=0.1).shift(RIGHT*0.2)
        fraction_line_subs = fraction_line.copy()
        two_a_subs = create_math_text("2(1)", font_size=45).next_to(fraction_line_subs, DOWN, buff=0.3)
        
        # Transform the formula with substituted values
        self.play(
            Transform(x_eq, x_eq_subs),
            ReplacementTransform(minus_b, minus_b_subs),
            ReplacementTransform(plus_minus, plus_minus_subs),
            ReplacementTransform(sqrt_symbol, sqrt_symbol_subs),
            ReplacementTransform(b_squared_term, b_squared_subs),
            ReplacementTransform(minus_4ac, minus_4ac_subs),
            ReplacementTransform(two_a, two_a_subs),
            FadeOut(formula_title),
            fraction_line.animate.become(fraction_line_subs), # Update fraction line if needed
            run_time=2.5
        )
        self.wait(1)

        # Simplify discriminant (b^2 - 4ac)
        calc_discriminant = create_math_text("16 - 12", font_size=45).move_to(numerator_sqrt_content_subs.get_center())
        self.play(ReplacementTransform(numerator_sqrt_content_subs, calc_discriminant))
        self.wait(0.5)
        
        calc_4 = create_math_text("4", font_size=45).move_to(calc_discriminant.get_center())
        self.play(ReplacementTransform(calc_discriminant, calc_4))
        self.wait(0.5)

        sqrt_result = create_math_text("2", font_size=45).move_to(VGroup(sqrt_symbol_subs, calc_4).get_center())
        self.play(ReplacementTransform(sqrt_symbol_subs, VGroup()), ReplacementTransform(calc_4, sqrt_result)) # Fade out sqrt symbol
        self.wait(0.5)
        
        # Simplify denominator
        calc_denom = create_math_text("2", font_size=45).move_to(two_a_subs.get_center())
        self.play(ReplacementTransform(two_a_subs, calc_denom))
        self.wait(0.5)

        # Fade out intermediate formula elements to prepare for x1/x2 calculation
        self.play(
            FadeOut(minus_b_subs), # We replace -(-4) with 4 in the simplified expression
            FadeOut(plus_minus_subs), # Replace with actual plus/minus operations
            FadeOut(sqrt_result), # Will be part of new expression
            FadeOut(fraction_line_subs), # Need to adjust length if numbers change much
            FadeOut(calc_denom)
        )
        self.wait(0.5)
        
        # Calculate x1 and x2
        x1_eq_text = create_math_text("x1 =", font_size=40, color=ACCENT_GOLD).align_to(x_eq_subs, LEFT).shift(DOWN*2.0)
        x1_numerator = create_math_text("4 + 2", font_size=40).next_to(x1_eq_text, RIGHT, buff=0.2)
        x1_frac_line = Line(LEFT*0.5, RIGHT*0.5, color=TEXT_COLOR).next_to(x1_numerator, DOWN, buff=0.3)
        x1_denominator = create_math_text("2", font_size=40).next_to(x1_frac_line, DOWN, buff=0.3)
        x1_full_expr = VGroup(x1_eq_text, x1_numerator, x1_frac_line, x1_denominator)

        x2_eq_text = create_math_text("x2 =", font_size=40, color=ACCENT_GOLD).next_to(x1_full_expr, DOWN, buff=0.8).align_to(x1_eq_text, LEFT)
        x2_numerator = create_math_text("4 - 2", font_size=40).next_to(x2_eq_text, RIGHT, buff=0.2)
        x2_frac_line = Line(LEFT*0.5, RIGHT*0.5, color=TEXT_COLOR).next_to(x2_numerator, DOWN, buff=0.3)
        x2_denominator = create_math_text("2", font_size=40).next_to(x2_frac_line, DOWN, buff=0.3)
        x2_full_expr = VGroup(x2_eq_text, x2_numerator, x2_frac_line, x2_denominator)

        self.play(Write(x1_full_expr), Write(x2_full_expr))
        self.wait(1)

        x1_result = create_math_text("x1 = 3", font_size=40, color=ACCENT_GOLD).move_to(x1_full_expr.get_center()).shift(RIGHT*1.5)
        x2_result = create_math_text("x2 = 1", font_size=40, color=ACCENT_GOLD).move_to(x2_full_expr.get_center()).shift(RIGHT*1.5)

        self.play(Transform(x1_full_expr, x1_result), Transform(x2_full_expr, x2_result))
        self.wait(1.5)
        
        # Bring back graph to show roots
        self.play(
            FadeOut(x1_full_expr, x2_full_expr, x_eq_subs, example_equation_text, example_equation, a_val_text, b_val_text, c_val_text, shift=UP),
            FadeIn(axes, axes_labels.copy().shift(DOWN*0.5)), # Bring back fresh axes
            title.animate.to_edge(UP).scale(0.8) # Keep title
        )
        
        # New graph for y = x^2 - 4x + 3
        def func2(x):
            return x**2 - 4*x + 3
        graph2 = axes.plot(func2, color=ACCENT_GOLD)
        
        roots_found_text = Text("Roots found!", font_size=35, color=ACCENT_BLUE).next_to(title, DOWN, buff=0.5)
        self.play(Create(graph2), Write(roots_found_text))

        # Mark roots
        root_dot_1 = Dot(axes.c2p(1, 0), color=HIGHLIGHT_COLOR)
        root_dot_2 = Dot(axes.c2p(3, 0), color=HIGHLIGHT_COLOR)
        
        self.play(FadeIn(root_dot_1, shift=UP), FadeIn(root_dot_2, shift=UP))
        self.wait(2)

        self.play(
            FadeOut(axes, axes_labels, graph2, root_dot_1, root_dot_2, roots_found_text, shift=DOWN)
        )
        
        # --- BEAT 4: Recap ---
        recap_card = Rectangle(width=10, height=6, color=ACCENT_BLUE, fill_opacity=0.2).scale(0.8)
        recap_title = Text("Recap: Quadratic Formula", font_size=45, color=ACCENT_GOLD).next_to(recap_card, UP, buff=0.5)
        self.play(FadeIn(recap_card), FadeIn(recap_title))

        # Reconstruct the formula for recap (cannot reuse previous VGroup easily due to transformations)
        x_eq_recap = create_math_text("x =", font_size=40, color=ACCENT_GOLD).shift(LEFT * 3)
        
        minus_b_recap = create_math_text("-b", font_size=40)
        plus_minus_recap = create_math_text("±", font_size=40, color=ACCENT_BLUE)
        sqrt_symbol_recap = create_math_text("√", font_size=60).scale(1.2).shift(LEFT * 0.1)
        b_squared_term_recap = create_math_text("b^2", font_size=40)
        b_squared_term_recap.submobjects[1].next_to(b_squared_term_recap.submobjects[0], UP+RIGHT, buff=0.05)
        minus_4ac_recap = create_math_text("-4ac", font_size=40)
        
        numerator_sqrt_content_recap = VGroup(b_squared_term_recap, minus_4ac_recap).arrange(RIGHT, buff=0.1)
        sqrt_expr_recap = VGroup(sqrt_symbol_recap, numerator_sqrt_content_recap).arrange(RIGHT, buff=0.1).shift(UP * 0.05)
        numerator_recap = VGroup(minus_b_recap, plus_minus_recap, sqrt_expr_recap).arrange(RIGHT, buff=0.1).shift(RIGHT*0.2)
        
        fraction_line_recap = Line(LEFT * 1.5, RIGHT * 1.5, color=TEXT_COLOR).next_to(numerator_recap, DOWN, buff=0.3)
        two_a_recap = create_math_text("2a", font_size=40).next_to(fraction_line_recap, DOWN, buff=0.3)
        
        quadratic_formula_recap = VGroup(x_eq_recap, numerator_recap, fraction_line_recap, two_a_recap)
        quadratic_formula_recap.move_to(recap_card.get_center()).shift(UP*0.5)
        
        self.play(FadeIn(quadratic_formula_recap, shift=UP))
        
        general_eq_recap_a_text = Text("From: ax^2 + bx + c = 0", font_size=35, color=ACCENT_BLUE).next_to(recap_card, DOWN, buff=0.5)
        # Manually adjust superscript after creation
        general_eq_recap_a_text.submobjects[2].next_to(general_eq_recap_a_text.submobjects[1], UP+RIGHT, buff=0.05)
        self.play(FadeIn(general_eq_recap_a_text, shift=DOWN))

        self.wait(3)
        self.play(FadeOut(VGroup(recap_card, recap_title, quadratic_formula_recap, general_eq_recap_a_text, title)))