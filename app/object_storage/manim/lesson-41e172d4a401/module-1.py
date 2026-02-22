from manim import *

class QuadraticEquationBasics(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE
        GOLD_ACCENT = GOLD
        TEXT_COLOR = WHITE
        AXIS_COLOR = GREY_B1

        # --- Helper for creating custom x^2 text ---
        def create_x_squared_text(x_color=TEXT_COLOR, exp_color=GOLD_ACCENT, font_size=40):
            x_char = Text("x", font_size=font_size, color=x_color)
            exp_char = Text("2", font_size=font_size * 0.7, color=exp_color)
            exp_char.next_to(x_char, UP + RIGHT, buff=0.05).shift(RIGHT * 0.05)
            return VGroup(x_char, exp_char)

        # --- BEAT 1: The Basic Parabola (y = x^2) ---
        title = Text("Quadratic Equation Basics", font_size=55, color=TEXT_COLOR).to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)

        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-0.5, 10, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": AXIS_COLOR},
            x_axis_config={"numbers_to_include": range(-3, 4)},
            y_axis_config={"numbers_to_include": range(0, 11, 2)},
        ).add_coordinates()
        axes.to_edge(LEFT, buff=0.5)

        labels = axes.get_axis_labels(x_label="x", y_label="y").set_color(TEXT_COLOR)

        self.play(Create(axes), Create(labels), run_time=1.5)
        self.wait(0.5)

        # Plot y = x^2
        parabola_curve = axes.plot(lambda x: x**2, color=BLUE_ACCENT)
        
        y_text = Text("y", font_size=40, color=TEXT_COLOR)
        equals_text = Text("=", font_size=40, color=TEXT_COLOR)
        x_squared_base = create_x_squared_text(font_size=40)
        
        y_equals_x_squared_eq = VGroup(y_text, equals_text, x_squared_base).arrange(RIGHT, buff=0.1).next_to(axes, RIGHT, buff=1).shift(UP*2)
        
        intro_text = Text("This is a Parabola. The graph of x².", font_size=35, color=TEXT_COLOR).next_to(y_equals_x_squared_eq, DOWN, buff=0.5)
        
        self.play(Create(parabola_curve), Write(y_equals_x_squared_eq))
        self.wait(0.5)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(FadeOut(intro_text))

        # --- BEAT 2: The 'a' coefficient (y = ax^2) ---
        a_char = Text("a", font_size=40, color=BLUE_ACCENT)
        
        # Insert 'a' into the equation VGroup
        y_equals_ax_squared_eq = VGroup(
            y_equals_x_squared_eq[0], # y
            y_equals_x_squared_eq[1], # =
            a_char,
            y_equals_x_squared_eq[2]  # x^2
        ).arrange(RIGHT, buff=0.1).move_to(y_equals_x_squared_eq.get_center())

        self.play(
            FadeIn(a_char.next_to(y_equals_x_squared_eq[2], LEFT, buff=0.05)), # 'a' appears before 'x^2'
            VGroup(y_equals_x_squared_eq[2]).animate.shift(RIGHT * 0.4) # Shift x^2 to make space for a
        )
        # Recreate the VGroup to reflect the new arrangement. Manually manage since TransformMatchingTex is forbidden.
        y_equals_ax_squared_eq = VGroup(y_text, equals_text, a_char, x_squared_base).arrange(RIGHT, buff=0.1).move_to(y_equals_x_squared_eq.get_center())
        
        explain_a = Text("The 'a' value stretches or flips it.", font_size=35, color=TEXT_COLOR).next_to(y_equals_ax_squared_eq, DOWN, buff=0.5)
        self.play(Write(explain_a))
        self.wait(0.5)

        current_a_value_text = Text("a = 1", font_size=30, color=BLUE_ACCENT).next_to(explain_a, DOWN, buff=0.3)
        self.play(Write(current_a_value_text))
        
        # Animate 'a' changing
        a_vals = [2, 0.5, -1]
        for a_val in a_vals:
            new_parabola = axes.plot(lambda x: a_val * x**2, color=BLUE_ACCENT)
            new_a_text = Text(f"a = {a_val}", font_size=30, color=BLUE_ACCENT).move_to(current_a_value_text.get_center())
            self.play(
                Transform(parabola_curve, new_parabola),
                Transform(current_a_value_text, new_a_text),
                run_time=1
            )
            self.wait(0.5)

        # Reset for next beat
        self.play(
            FadeOut(explain_a),
            FadeOut(current_a_value_text),
            FadeOut(a_char), # Fade out 'a' for a cleaner transition to 'bx' and 'c' later
            Transform(parabola_curve, axes.plot(lambda x: x**2, color=BLUE_ACCENT)), # Reset parabola to y=x^2
            run_time=1.5
        )
        # Re-initialize y_equals_x_squared_eq without 'a'
        y_equals_x_squared_eq = VGroup(y_text, equals_text, x_squared_base).arrange(RIGHT, buff=0.1).move_to(y_equals_ax_squared_eq.get_center())
        self.add(y_equals_x_squared_eq) # Re-add to scene explicitly
        self.wait(0.5)

        # --- BEAT 3: The 'b' coefficient (y = x^2 + bx) ---
        plus_char_b = Text("+", font_size=40, color=TEXT_COLOR)
        b_char = Text("b", font_size=40, color=GOLD_ACCENT)
        x_char_b = Text("x", font_size=40, color=TEXT_COLOR)
        
        bx_term = VGroup(plus_char_b, b_char, x_char_b).arrange(RIGHT, buff=0.05)
        
        # Combine existing y=x^2 with new bx term
        y_equals_x_squared_plus_bx_eq = VGroup(y_equals_x_squared_eq.copy(), bx_term).arrange(RIGHT, buff=0.1).move_to(y_equals_x_squared_eq.get_center())

        self.play(
            FadeOut(y_equals_x_squared_eq), # Fade out y=x^2
            FadeIn(y_equals_x_squared_plus_bx_eq) # Fade in y=x^2+bx
        )
        
        explain_b = Text("The 'b' value shifts it horizontally.", font_size=35, color=TEXT_COLOR).next_to(y_equals_x_squared_plus_bx_eq, DOWN, buff=0.5)
        self.play(Write(explain_b))
        self.wait(0.5)

        current_b_value_text = Text("b = 0", font_size=30, color=GOLD_ACCENT).next_to(explain_b, DOWN, buff=0.3)
        self.play(Write(current_b_value_text))

        # Animate 'b' changing (a=1 assumed)
        b_vals = [2, -2]
        for b_val in b_vals:
            new_parabola = axes.plot(lambda x: x**2 + b_val * x, color=BLUE_ACCENT)
            new_b_text = Text(f"b = {b_val}", font_size=30, color=GOLD_ACCENT).move_to(current_b_value_text.get_center())
            self.play(
                Transform(parabola_curve, new_parabola),
                Transform(current_b_value_text, new_b_text),
                run_time=1
            )
            self.wait(0.5)

        # Reset for next beat
        self.play(
            FadeOut(explain_b),
            FadeOut(current_b_value_text),
            Transform(parabola_curve, axes.plot(lambda x: x**2, color=BLUE_ACCENT)), # Reset parabola to y=x^2
            FadeOut(y_equals_x_squared_plus_bx_eq), # Fade out y=x^2+bx
            run_time=1.5
        )
        y_equals_x_squared_eq = VGroup(y_text, equals_text, x_squared_base).arrange(RIGHT, buff=0.1).next_to(axes, RIGHT, buff=1).shift(UP*2)
        self.add(y_equals_x_squared_eq)
        self.wait(0.5)

        # --- BEAT 4: The 'c' coefficient (y = x^2 + c) ---
        plus_char_c = Text("+", font_size=40, color=TEXT_COLOR)
        c_char = Text("c", font_size=40, color=TEXT_COLOR)

        c_term = VGroup(plus_char_c, c_char).arrange(RIGHT, buff=0.05)
        
        # Combine existing y=x^2 with new c term
        y_equals_x_squared_plus_c_eq = VGroup(y_equals_x_squared_eq.copy(), c_term).arrange(RIGHT, buff=0.1).move_to(y_equals_x_squared_eq.get_center())

        self.play(
            FadeOut(y_equals_x_squared_eq), # Fade out y=x^2
            FadeIn(y_equals_x_squared_plus_c_eq) # Fade in y=x^2+c
        )

        explain_c = Text("The 'c' value shifts it vertically.", font_size=35, color=TEXT_COLOR).next_to(y_equals_x_squared_plus_c_eq, DOWN, buff=0.5)
        self.play(Write(explain_c))
        self.wait(0.5)

        current_c_value_text = Text("c = 0", font_size=30, color=TEXT_COLOR).next_to(explain_c, DOWN, buff=0.3)
        self.play(Write(current_c_value_text))

        # Animate 'c' changing (a=1, b=0 assumed)
        c_vals = [2, -2]
        for c_val in c_vals:
            new_parabola = axes.plot(lambda x: x**2 + c_val, color=BLUE_ACCENT)
            new_c_text = Text(f"c = {c_val}", font_size=30, color=TEXT_COLOR).move_to(current_c_value_text.get_center())
            self.play(
                Transform(parabola_curve, new_parabola),
                Transform(current_c_value_text, new_c_text),
                run_time=1
            )
            self.wait(0.5)
        
        self.play(
            FadeOut(explain_c),
            FadeOut(current_c_value_text),
            Transform(parabola_curve, axes.plot(lambda x: x**2, color=BLUE_ACCENT)), # Reset parabola
            FadeOut(y_equals_x_squared_plus_c_eq), # Fade out y=x^2+c
            run_time=1.5
        )

        # --- BEAT 5: The General Form (ax^2 + bx + c = 0) ---
        # Construct ax^2 + bx + c = 0 step-by-step with Text
        
        a_char_final = Text("a", font_size=48, color=BLUE_ACCENT)
        x_squared_final = create_x_squared_text(font_size=48)
        ax2_term_final = VGroup(a_char_final, x_squared_final).arrange(RIGHT, buff=0.05)

        plus1_final = Text("+", font_size=48, color=TEXT_COLOR)
        b_char_final = Text("b", font_size=48, color=GOLD_ACCENT)
        x_final = Text("x", font_size=48, color=TEXT_COLOR)
        bx_term_final = VGroup(b_char_final, x_final).arrange(RIGHT, buff=0.05)

        plus2_final = Text("+", font_size=48, color=TEXT_COLOR)
        c_char_final = Text("c", font_size=48, color=TEXT_COLOR)

        equals_zero_final = VGroup(Text("=", font_size=48, color=TEXT_COLOR), Text("0", font_size=48, color=TEXT_COLOR)).arrange(RIGHT, buff=0.05)
        
        # Assemble them in a VGroup
        full_equation = VGroup(
            ax2_term_final, plus1_final, bx_term_final, plus2_final, c_char_final, equals_zero_final
        ).arrange(RIGHT, buff=0.2).move_to(ORIGIN).shift(RIGHT * 1.5) # Center it on the right side of the screen

        self.play(
            FadeOut(parabola_curve), FadeOut(axes), FadeOut(labels), FadeOut(title), # Fade out everything except what's needed
            FadeIn(full_equation)
        )

        definition_line1 = Text("This is the general form of a", font_size=35, color=TEXT_COLOR).next_to(full_equation, UP, buff=0.8)
        quadratic_word = Text("Quadratic Equation", font_size=45, color=BLUE_ACCENT).next_to(definition_line1, DOWN, buff=0.2)
        degree_two = Text("A Degree Two Polynomial", font_size=30, color=GOLD_ACCENT).next_to(quadratic_word, DOWN, buff=0.2)

        self.play(Write(definition_line1), Write(quadratic_word))
        self.wait(1)
        self.play(Write(degree_two))
        self.wait(1)

        # Highlight a, b, c
        self.play(Indicate(a_char_final, color=BLUE_ACCENT), run_time=1)
        a_info = Text("'a': Determines shape (width/direction)", font_size=28, color=BLUE_ACCENT).next_to(degree_two, DOWN, buff=0.5).align_to(full_equation, LEFT).shift(LEFT*1.5)
        self.play(Write(a_info))
        self.wait(1)

        self.play(Indicate(b_char_final, color=GOLD_ACCENT), run_time=1)
        b_info = Text("'b': Shifts horizontally", font_size=28, color=GOLD_ACCENT).next_to(a_info, DOWN, buff=0.2).align_to(a_info, LEFT)
        self.play(Write(b_info))
        self.wait(1)

        self.play(Indicate(c_char_final, color=TEXT_COLOR), run_time=1)
        c_info = Text("'c': Shifts vertically (y-intercept)", font_size=28, color=TEXT_COLOR).next_to(b_info, DOWN, buff=0.2).align_to(a_info, LEFT)
        self.play(Write(c_info))
        self.wait(2) # Give a bit more time here

        # --- RECAP CARD ---
        final_info_group = VGroup(definition_line1, quadratic_word, degree_two, a_info, b_info, c_info)
        self.play(FadeOut(final_info_group))
        
        recap_title = Text("Recap: Quadratic Equation Structure", font_size=50, color=BLUE_ACCENT).to_edge(UP, buff=0.5)
        
        # Re-center equation and scale for recap
        self.play(full_equation.animate.scale(0.8).move_to(ORIGIN))

        # Using unicode for squared '²' for simplicity in recap bullet points
        bullet1 = Text("•  ax\u00b2: 'a' controls shape/direction", font_size=35, color=TEXT_COLOR).next_to(recap_title, DOWN, buff=0.8).align_to(full_equation, LEFT).shift(LEFT*2)
        bullet1[3].set_color(BLUE_ACCENT) # The 'a'
        bullet2 = Text("•  + bx: 'b' shifts horizontally", font_size=35, color=TEXT_COLOR).next_to(bullet1, DOWN, buff=0.3).align_to(bullet1, LEFT)
        bullet2[2].set_color(GOLD_ACCENT) # The 'b'
        bullet3 = Text("•  + c: 'c' shifts vertically (y-intercept)", font_size=35, color=TEXT_COLOR).next_to(bullet2, DOWN, buff=0.3).align_to(bullet1, LEFT)
        bullet4 = Text("•  = 0: We look for x-intercepts (roots)", font_size=35, color=TEXT_COLOR).next_to(bullet3, DOWN, buff=0.3).align_to(bullet1, LEFT)

        self.play(Write(recap_title), LaggedStart(
            FadeIn(bullet1, shift=UP),
            FadeIn(bullet2, shift=UP),
            FadeIn(bullet3, shift=UP),
            FadeIn(bullet4, shift=UP),
            lag_ratio=0.7,
            run_time=3
        ))
        self.wait(3)

        self.play(FadeOut(VGroup(recap_title, bullet1, bullet2, bullet3, bullet4, full_equation)))
        self.wait(1)