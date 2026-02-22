from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # Set up scene configuration
        config.background_color = BLACK

        # --- Helper for custom square root symbol without Tex ---
        # (This is a simplified visual representation due to the "no Tex" constraint)
        def create_custom_sqrt_symbol(content_mobject):
            # The left-side hook of the radical symbol
            hook_len = 0.15
            hook_left = Line(ORIGIN, UP * hook_len).set_stroke(width=3).set_color(WHITE)
            hook_right = Line(ORIGIN, RIGHT * hook_len).rotate(-PI/4).next_to(hook_left.get_end(), DR, buff=0)

            # The horizontal bar over the content
            bar_width = content_mobject.get_width() * 1.1 # Slightly wider than the content
            bar = Line(ORIGIN, RIGHT * bar_width).set_stroke(width=3).set_color(WHITE)

            # Position the bar over the content
            bar.next_to(content_mobject, UP, buff=0.1)
            bar.align_to(content_mobject.get_left(), LEFT).shift(LEFT * 0.05) # Align left and shift slightly

            # Position the hook relative to the bar's start
            hook_group = VGroup(hook_left, hook_right)
            hook_group.next_to(bar.get_left(), LEFT, buff=0.05).align_to(bar, DOWN)

            return VGroup(hook_group, bar)

        # --- Beat 1: Opening Hook - The Parabola and its Roots ---
        title = Text("Applying the Quadratic Formula to Solve", color=WHITE).scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": GRAY_D},
            background_line_style={"stroke_color": GRAY, "stroke_width": 1, "stroke_opacity": 0.5}
        ).add_coordinates().scale(0.7).to_edge(DOWN).shift(UP*0.5)

        # Define a parabola function: y = x^2 - 4
        def parabola_func(x):
            return x**2 - 4

        parabola = plane.get_graph(parabola_func, x_range=[-2.5, 2.5], color=BLUE_B, stroke_width=4)

        x_intercept1 = Dot(plane.c2p(-2, 0), color=GOLD)
        x_intercept2 = Dot(plane.c2p(2, 0), color=GOLD)

        question = Text("Where does it cross the X-axis?", color=WHITE).scale(0.6).next_to(plane, UP, buff=0.5)
        arrow1 = Arrow(question.get_bottom(), x_intercept1.get_top(), buff=0.1, color=WHITE)
        arrow2 = Arrow(question.get_bottom(), x_intercept2.get_top(), buff=0.1, color=WHITE)

        self.play(FadeIn(plane, shift=UP))
        self.play(Create(parabola), run_time=1.5)
        self.play(FadeIn(x_intercept1, x_intercept2), Write(question), GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(1.5)
        self.play(FadeOut(question, arrow1, arrow2, x_intercept1, x_intercept2))

        # --- Beat 2: The General Quadratic Equation ---
        general_form_label = Text("Every parabola has a quadratic equation:", color=WHITE).scale(0.6).to_edge(UP, buff=1.5)
        self.play(ReplacementTransform(title, general_form_label))
        
        # Construct ax^2 + bx + c = 0 manually
        a_char = Text("a").set_color(GOLD)
        x_char1 = Text("x").set_color(WHITE)
        exp2 = Text("2").scale(0.6).next_to(x_char1, UP + RIGHT * 0.1, buff=0.05).set_color(WHITE)
        ax2 = VGroup(a_char, x_char1, exp2).arrange(RIGHT, buff=0.05)

        plus1 = Text("+").set_color(WHITE)

        b_char = Text("b").set_color(GOLD)
        x_char2 = Text("x").set_color(WHITE)
        bx = VGroup(b_char, x_char2).arrange(RIGHT, buff=0.05)

        plus2 = Text("+").set_color(WHITE)
        c_char = Text("c").set_color(GOLD)
        equals0 = Text(" = 0").set_color(WHITE)

        general_equation = VGroup(ax2, plus1, bx, plus2, c_char, equals0).arrange(RIGHT, buff=0.2).move_to(ORIGIN)

        self.play(FadeOut(parabola, plane), FadeIn(general_equation, shift=UP), run_time=1.5)
        self.wait(0.5)

        coefficients_text = Text("a, b, and c are coefficients that define it.", color=WHITE).scale(0.5).next_to(general_equation, DOWN, buff=0.5)
        self.play(
            LaggedStart(
                Flash(a_char, color=GOLD),
                Flash(b_char, color=GOLD),
                Flash(c_char, color=GOLD),
                Write(coefficients_text),
                lag_ratio=0.5
            )
        )
        self.wait(1.5)

        self.play(FadeOut(coefficients_text))

        # --- Beat 3: The Quadratic Formula Revealed ---
        formula_label = Text("To find where it crosses the X-axis (the roots), we use:", color=WHITE).scale(0.6).to_edge(UP, buff=1.5)
        self.play(ReplacementTransform(general_form_label, formula_label), FadeOut(general_equation, shift=DOWN))
        self.wait(0.5)

        # Construct Quadratic Formula Piece by Piece (without Tex/MathTex)
        x_equals = Text("x =").set_color(BLUE)

        num_b = Text("-b").set_color(GOLD)
        plus_minus = Text("\u00B1").set_color(WHITE) # Unicode plus-minus

        b_sq_char = Text("b").set_color(GOLD)
        sq_exp = Text("2").scale(0.6).next_to(b_sq_char, UP + RIGHT * 0.05, buff=0.05).set_color(WHITE)
        b_squared = VGroup(b_sq_char, sq_exp)

        minus_4_text = Text("-4").set_color(WHITE)
        a_formula_char = Text("a").set_color(GOLD)
        c_formula_char = Text("c").set_color(GOLD)

        discriminant_terms = VGroup(b_squared, minus_4_text, a_formula_char, c_formula_char).arrange(RIGHT, buff=0.05)
        
        # Custom square root symbol using the helper
        sqrt_symbol = create_custom_sqrt_symbol(discriminant_terms)

        # Combine numerator elements
        # Arrange discriminant terms and sqrt symbol first
        discriminant_group = VGroup(discriminant_terms, sqrt_symbol).move_to(ORIGIN)
        sqrt_symbol[1].set_width(discriminant_terms.get_width() * 1.1)
        sqrt_symbol[1].next_to(discriminant_terms, UP, buff=0.1)
        sqrt_symbol[1].align_to(discriminant_terms.get_left(), LEFT).shift(LEFT * 0.05)
        sqrt_symbol[0].next_to(sqrt_symbol[1].get_left(), LEFT, buff=0.05).align_to(sqrt_symbol[1], DOWN)
        
        # Final arrangement of numerator
        numerator_elements = VGroup(num_b, plus_minus, discriminant_group).arrange(RIGHT, buff=0.2)

        # Denominator
        two_a = Text("2a").set_color(GOLD)

        # Fraction bar
        fraction_bar = Line(LEFT, RIGHT).set_color(WHITE).set_width(numerator_elements.get_width() * 1.1)
        
        # Position all parts
        fraction_bar.move_to(ORIGIN)
        numerator_elements.next_to(fraction_bar, UP, buff=0.2)
        two_a.next_to(fraction_bar, DOWN, buff=0.2)
        x_equals.next_to(fraction_bar, LEFT, buff=0.5)

        quadratic_formula = VGroup(x_equals, numerator_elements, fraction_bar, two_a)
        quadratic_formula.scale(0.7).move_to(ORIGIN)

        self.play(FadeIn(x_equals))
        self.play(Create(fraction_bar))
        self.play(FadeIn(num_b, shift=UP), FadeIn(plus_minus, shift=UP))
        self.play(FadeIn(two_a, shift=DOWN))
        self.play(
            LaggedStart(
                FadeIn(b_squared, shift=UP),
                FadeIn(minus_4_text, shift=UP),
                FadeIn(a_formula_char, shift=UP),
                FadeIn(c_formula_char, shift=UP),
                lag_ratio=0.1
            ),
            Create(sqrt_symbol)
        )
        self.wait(2)

        formula_name = Text("The Quadratic Formula", color=WHITE).scale(0.6).next_to(quadratic_formula, DOWN, buff=0.5)
        self.play(Write(formula_name))
        self.wait(1)

        # --- Beat 4: Applying the Formula - Identifying a, b, c ---
        example_label = Text("Let's identify a, b, and c for an example equation:", color=WHITE).scale(0.6).to_edge(UP, buff=1.5)
        self.play(ReplacementTransform(formula_label, example_label), FadeOut(formula_name))
        
        # Keep quadratic_formula on screen, but move it up slightly
        self.play(quadratic_formula.animate.scale(0.8).to_edge(UP).shift(DOWN*0.5), run_time=1.5)

        # Example equation: 2x^2 + 5x - 3 = 0
        ex_a_val = Text("2").set_color(GOLD)
        ex_x_char1 = Text("x").set_color(WHITE)
        ex_exp2 = Text("2").scale(0.6).next_to(ex_x_char1, UP + RIGHT * 0.1, buff=0.05).set_color(WHITE)
        ex_ax2 = VGroup(ex_a_val, ex_x_char1, ex_exp2).arrange(RIGHT, buff=0.05)

        ex_plus1 = Text("+").set_color(WHITE)

        ex_b_val = Text("5").set_color(GOLD)
        ex_x_char2 = Text("x").set_color(WHITE)
        ex_bx = VGroup(ex_b_val, ex_x_char2).arrange(RIGHT, buff=0.05)

        ex_minus = Text("-").set_color(WHITE)
        ex_c_val = Text("3").set_color(GOLD)
        ex_equals0 = Text(" = 0").set_color(WHITE)

        example_equation = VGroup(ex_ax2, ex_plus1, ex_bx, ex_minus, ex_c_val, ex_equals0).arrange(RIGHT, buff=0.2).move_to(ORIGIN).shift(DOWN*0.5).scale(0.8)
        
        # Ensure c_val is -3 conceptually
        ex_c_val_full = VGroup(ex_minus, ex_c_val)
        ex_c_val_full.set_color(GOLD) # The value is -3

        self.play(Write(example_equation))
        self.wait(1)

        # Arrows mapping a, b, c
        a_arrow = Arrow(ex_a_val.get_center(), a_formula_char.get_center(), buff=0.1, color=GOLD)
        b_arrow = Arrow(ex_b_val.get_center(), num_b.get_center(), buff=0.1, color=GOLD)
        c_arrow = Arrow(ex_c_val_full.get_center(), c_formula_char.get_center(), buff=0.1, color=GOLD) # Point from -3

        mapping_label = Text("Identify a, b, and c...", color=WHITE).scale(0.5).next_to(example_equation, DOWN, buff=0.5)
        self.play(Write(mapping_label))
        
        # Create 'a', 'b', 'c' placeholders for the example (values)
        a_is = Text("a = ").next_to(mapping_label, DOWN*2, buff=0.5).shift(LEFT*1.5)
        b_is = Text("b = ").next_to(a_is, RIGHT, buff=1.5)
        c_is = Text("c = ").next_to(b_is, RIGHT, buff=1.5)

        a_val_map = Text("2", color=GOLD).next_to(a_is, RIGHT, buff=0.1)
        b_val_map = Text("5", color=GOLD).next_to(b_is, RIGHT, buff=0.1)
        c_val_map = Text("-3", color=GOLD).next_to(c_is, RIGHT, buff=0.1) # Emphasize -3 for c

        self.play(GrowArrow(a_arrow), Write(a_is), ReplacementTransform(ex_a_val.copy(), a_val_map))
        self.wait(0.5)
        self.play(GrowArrow(b_arrow), Write(b_is), ReplacementTransform(ex_b_val.copy(), b_val_map))
        self.wait(0.5)
        self.play(GrowArrow(c_arrow), Write(c_is), ReplacementTransform(ex_c_val_full.copy(), c_val_map))
        self.wait(2)

        self.play(FadeOut(example_label, mapping_label, a_arrow, b_arrow, c_arrow, a_is, b_is, c_is, a_val_map, b_val_map, c_val_map, example_equation))

        # --- Beat 5: Recap Card ---
        recap_card = VGroup(
            Text("Recap:", color=BLUE).scale(0.8),
            Text("- Quadratic equations describe parabolas.", color=WHITE).scale(0.6),
            Text("- Roots are where the parabola crosses the X-axis.", color=WHITE).scale(0.6),
            Text("- The Quadratic Formula gives these roots.", color=WHITE).scale(0.6),
            Text("- Always identify a, b, and c carefully!", color=GOLD).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)

        self.play(FadeOut(quadratic_formula, shift=UP)) # Fade out the formula
        self.play(Write(recap_card[0]))
        self.play(LaggedStart(*[Write(text) for text in recap_card[1:]], lag_ratio=0.7))
        self.wait(3)

        self.play(FadeOut(recap_card))
        self.wait(0.5)