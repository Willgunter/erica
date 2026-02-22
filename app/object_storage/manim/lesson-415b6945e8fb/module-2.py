from manim import *

# Custom colors for 3Blue1Brown style
DARK_BACKGROUND = "#1a2a4a" # A dark blue-grey
LIGHT_BLUE_ACCENT = BLUE_C # A brighter blue
GOLD_ACCENT = GOLD_C # A gold/yellow

# Custom font sizes
DEFAULT_TEXT_FONT_SIZE = 36
EQUATION_MAIN_FONT_SIZE = 50

# Helper function to create superscript on a given Mobject
def create_superscript_on_mobject(mobject_base, super_text_str, scale_factor=0.6, color=LIGHT_BLUE_ACCENT):
    """Creates a superscript Mobject positioned relative to the top-right corner of the base Mobject."""
    super_text = Text(super_text_str, font_size=EQUATION_MAIN_FONT_SIZE * scale_factor, color=color)
    super_text.next_to(mobject_base.get_corner(UP + RIGHT), UR, buff=0.05)
    return super_text

# Helper function to create a fraction using Text and Line Mobjects
def create_fraction(numerator_mobjects, denominator_mobjects, scale_factor=0.7, color=LIGHT_BLUE_ACCENT):
    """
    Creates a fraction VGroup from lists of Mobjects for the numerator and denominator.
    Ensures all parts are Mobjects before arranging.
    """
    numerator_vg = VGroup(*numerator_mobjects).arrange(RIGHT, buff=0.1)
    denominator_vg = VGroup(*denominator_mobjects).arrange(RIGHT, buff=0.1)

    frac_line = Line(LEFT, RIGHT, color=color, stroke_width=2)

    max_width = max(numerator_vg.width, denominator_vg.width)
    frac_line.set_width(max_width * 1.1)

    fraction_vg = VGroup(numerator_vg, frac_line, denominator_vg)
    fraction_vg.arrange(DOWN, buff=MED_SMALL_BUFF * 0.5)
    
    # Manually re-center the line and position parts to ensure clean alignment
    frac_line.move_to(fraction_vg.get_center())
    numerator_vg.next_to(frac_line, UP, buff=MED_SMALL_BUFF * 0.5)
    denominator_vg.next_to(frac_line, DOWN, buff=MED_SMALL_BUFF * 0.5)

    return fraction_vg

# Helper to create a variable x^2
def create_x_squared(color=LIGHT_BLUE_ACCENT):
    """Creates an 'x^2' Mobject."""
    x_text = Text("x", font_size=EQUATION_MAIN_FONT_SIZE, color=color)
    sup_2 = create_superscript_on_mobject(x_text, "2", scale_factor=0.6, color=color)
    return VGroup(x_text, sup_2)

# Helper for a single variable 'x'
def create_var_x(color=LIGHT_BLUE_ACCENT):
    """Creates an 'x' Mobject."""
    return Text("x", font_size=EQUATION_MAIN_FONT_SIZE, color=color)

# Helper for numbers (can be used for coefficients too if they are just numbers)
def create_number(num_str, color=WHITE):
    """Creates a number Mobject."""
    return Text(num_str, font_size=EQUATION_MAIN_FONT_SIZE, color=color)

# Helper for operators
def create_operator(op_str, color=WHITE):
    """Creates an operator Mobject."""
    return Text(op_str, font_size=EQUATION_MAIN_FONT_SIZE, color=color)

class QuadraticFormulaDerivation(Scene):
    def construct(self):
        self.camera.background_color = DARK_BACKGROUND

        # --- Intro Hook: Parabola and its roots ---
        intro_title = Text("The Quadratic Formula", font_size=DEFAULT_TEXT_FONT_SIZE + 10, color=GOLD_ACCENT)
        self.play(Write(intro_title))
        self.wait(1)
        self.play(intro_title.animate.to_edge(UP).scale(0.8))

        # Setup axes for the parabola visualization
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": GRAY, "stroke_width": 1},
        ).add_coordinates().scale(0.7).to_edge(DOWN)
        
        # Define the function: f(x) = x^2 - 2x - 3
        parabola = axes.get_graph(lambda x: x**2 - 2*x - 3, color=LIGHT_BLUE_ACCENT)
        
        # Mark the x-intercepts (roots)
        root1_dot = Dot(axes.c2p(-1, 0), color=GOLD_ACCENT, radius=0.1)
        root2_dot = Dot(axes.c2p(3, 0), color=GOLD_ACCENT, radius=0.1)
        
        root1_label = Text("x = -1", font_size=DEFAULT_TEXT_FONT_SIZE - 10, color=GOLD_ACCENT).next_to(root1_dot, DOWN)
        root2_label = Text("x = 3", font_size=DEFAULT_TEXT_FONT_SIZE - 10, color=GOLD_ACCENT).next_to(root2_dot, DOWN)
        
        question_text = Text("Where does this cross the x-axis?", font_size=DEFAULT_TEXT_FONT_SIZE, color=WHITE).next_to(parabola, UP, buff=0.5)

        self.play(Create(axes), Create(parabola), run_time=2)
        self.play(FadeIn(root1_dot, scale=0.5), FadeIn(root2_dot, scale=0.5))
        self.play(Write(root1_label), Write(root2_label), Write(question_text))
        self.wait(2)
        self.play(FadeOut(axes, parabola, root1_dot, root2_dot, root1_label, root2_label, question_text))
        
        # --- Beat 1: Standard Form ax^2 + bx + c = 0 ---
        beat_title1 = Text("1. Standard Form", font_size=DEFAULT_TEXT_FONT_SIZE, color=WHITE).next_to(intro_title, DOWN, buff=0.5)
        self.play(FadeIn(beat_title1))

        # Equation 1: ax^2 + bx + c = 0
        eq1_mobjects = VGroup(
            create_number("a", color=GOLD_ACCENT), create_x_squared(color=LIGHT_BLUE_ACCENT), create_operator("+"),
            create_number("b", color=GOLD_ACCENT), create_var_x(color=LIGHT_BLUE_ACCENT), create_operator("+"),
            create_number("c", color=GOLD_ACCENT), create_operator("="), create_number("0")
        ).arrange(RIGHT, buff=0.2).center()

        self.play(Write(eq1_mobjects))
        goal_text = Text("Goal: Find the value(s) of x", font_size=DEFAULT_TEXT_FONT_SIZE * 0.8, color=WHITE).next_to(eq1_mobjects, DOWN, buff=0.7)
        self.play(FadeIn(goal_text))
        self.wait(2)
        self.play(FadeOut(goal_text, beat_title1))

        # --- Beat 2: Isolate x-terms (Divide by 'a', Move 'c') ---
        beat_title2 = Text("2. Isolate x-terms", font_size=DEFAULT_TEXT_FONT_SIZE, color=WHITE).next_to(intro_title, DOWN, buff=0.5)
        self.play(FadeIn(beat_title2))
        
        divide_text = Text("Divide by 'a':", font_size=DEFAULT_TEXT_FONT_SIZE * 0.8, color=WHITE).next_to(eq1_mobjects, DOWN, buff=0.7)
        self.play(FadeIn(divide_text))

        # Equation 2: x^2 + (b/a)x + (c/a) = 0
        frac_b_a = create_fraction([create_number("b", color=GOLD_ACCENT)], [create_number("a", color=GOLD_ACCENT)], scale_factor=0.7)
        frac_c_a = create_fraction([create_number("c", color=GOLD_ACCENT)], [create_number("a", color=GOLD_ACCENT)], scale_factor=0.7)

        eq2_mobjects = VGroup(
            create_x_squared(color=LIGHT_BLUE_ACCENT), create_operator("+"), frac_b_a, create_var_x(color=LIGHT_BLUE_ACCENT),
            create_operator("+"), frac_c_a, create_operator("="), create_number("0")
        ).arrange(RIGHT, buff=0.2).center()
        
        self.play(FadeOut(eq1_mobjects), FadeIn(eq2_mobjects))
        self.wait(1.5)
        self.play(FadeOut(divide_text))

        move_c_text = Text("Move constant 'c/a' to the right:", font_size=DEFAULT_TEXT_FONT_SIZE * 0.8, color=WHITE).next_to(eq2_mobjects, DOWN, buff=0.7)
        self.play(FadeIn(move_c_text))

        # Equation 3: x^2 + (b/a)x = -c/a
        frac_neg_c_a = create_fraction([create_operator("-"), create_number("c", color=GOLD_ACCENT)], [create_number("a", color=GOLD_ACCENT)], scale_factor=0.7)

        eq3_mobjects = VGroup(
            create_x_squared(color=LIGHT_BLUE_ACCENT), create_operator("+"), frac_b_a.copy(), create_var_x(color=LIGHT_BLUE_ACCENT),
            create_operator("="), frac_neg_c_a
        ).arrange(RIGHT, buff=0.2).center()
        
        self.play(FadeOut(eq2_mobjects), FadeIn(eq3_mobjects))
        self.wait(2)
        self.play(FadeOut(move_c_text, beat_title2))

        # --- Beat 3: Completing the Square ---
        beat_title3 = Text("3. Complete the Square", font_size=DEFAULT_TEXT_FONT_SIZE, color=WHITE).next_to(intro_title, DOWN, buff=0.5)
        self.play(FadeIn(beat_title3))

        add_term_text = Text("Add (b/2a)^2 to both sides:", font_size=DEFAULT_TEXT_FONT_SIZE * 0.8, color=WHITE).next_to(eq3_mobjects, DOWN, buff=0.7)
        self.play(FadeIn(add_term_text))

        # Term for (b/2a)^2
        frac_b_2a_base = create_fraction([create_number("b", color=GOLD_ACCENT)], [create_number("2"), create_number("a", color=GOLD_ACCENT)], scale_factor=0.7)
        term_b_2a_in_paren = VGroup(create_operator("("), frac_b_2a_base, create_operator(")")).arrange(RIGHT, buff=0.05)
        term_b_2a_sq = VGroup(term_b_2a_in_paren, create_superscript_on_mobject(term_b_2a_in_paren, "2", scale_factor=0.6, color=LIGHT_BLUE_ACCENT))

        # Equation 4: x^2 + (b/a)x + (b/2a)^2 = -c/a + (b/2a)^2
        eq4_mobjects = VGroup(
            create_x_squared(color=LIGHT_BLUE_ACCENT), create_operator("+"), frac_b_a.copy(), create_var_x(color=LIGHT_BLUE_ACCENT), create_operator("+"), term_b_2a_sq.copy(),
            create_operator("="),
            frac_neg_c_a.copy(), create_operator("+"), term_b_2a_sq.copy()
        ).arrange(RIGHT, buff=0.2).center()

        self.play(FadeOut(eq3_mobjects), FadeIn(eq4_mobjects))
        self.wait(1.5)
        self.play(FadeOut(add_term_text))

        perfect_square_text = Text("The left side is now a perfect square and simplify the right:", font_size=DEFAULT_TEXT_FONT_SIZE * 0.8, color=WHITE).next_to(eq4_mobjects, DOWN, buff=0.7)
        self.play(FadeIn(perfect_square_text))

        # Equation 5: (x + b/2a)^2 = (b^2 - 4ac) / 4a^2
        # Left side: (x + b/2a)^2
        frac_b_2a_left = create_fraction([create_number("b", color=GOLD_ACCENT)], [create_number("2"), create_number("a", color=GOLD_ACCENT)], scale_factor=0.7)
        base_x_b_2a = VGroup(create_operator("("), create_var_x(color=LIGHT_BLUE_ACCENT), create_operator("+"), frac_b_2a_left, create_operator(")")).arrange(RIGHT, buff=0.05)
        sq_left_side = VGroup(base_x_b_2a, create_superscript_on_mobject(base_x_b_2a, "2", scale_factor=0.6, color=LIGHT_BLUE_ACCENT))

        # Right side: (b^2 - 4ac) / 4a^2
        num_b_sq_term = VGroup(create_number("b", color=GOLD_ACCENT), create_superscript_on_mobject(create_number("b", color=GOLD_ACCENT), "2", scale_factor=0.6, color=LIGHT_BLUE_ACCENT))
        num_4ac_term = VGroup(create_number("4"), create_number("a", color=GOLD_ACCENT), create_number("c", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)
        final_numerator_parts = [num_b_sq_term, create_operator("-"), num_4ac_term]

        den_4a_sq_term = VGroup(create_number("4"), create_number("a", color=GOLD_ACCENT), create_superscript_on_mobject(create_number("a", color=GOLD_ACCENT), "2", scale_factor=0.6, color=LIGHT_BLUE_ACCENT))
        final_denominator_parts = [den_4a_sq_term]

        frac_final_right_side = create_fraction(final_numerator_parts, final_denominator_parts, scale_factor=0.7, color=LIGHT_BLUE_ACCENT)

        eq5_mobjects = VGroup(
            sq_left_side, create_operator("="), frac_final_right_side
        ).arrange(RIGHT, buff=0.2).center()

        self.play(FadeOut(eq4_mobjects), FadeIn(eq5_mobjects))
        self.wait(2)
        self.play(FadeOut(perfect_square_text, beat_title3))

        # --- Beat 4: Solve for x ---
        beat_title4 = Text("4. Solve for x", font_size=DEFAULT_TEXT_FONT_SIZE, color=WHITE).next_to(intro_title, DOWN, buff=0.5)
        self.play(FadeIn(beat_title4))

        sqrt_sides_text = Text("Take the square root of both sides:", font_size=DEFAULT_TEXT_FONT_SIZE * 0.8, color=WHITE).next_to(eq5_mobjects, DOWN, buff=0.7)
        self.play(FadeIn(sqrt_sides_text))

        # Equation 6: x + b/2a = +/- sqrt(b^2 - 4ac) / 2a
        # Left side: x + b/2a
        frac_b_2a_right = create_fraction([create_number("b", color=GOLD_ACCENT)], [create_number("2"), create_number("a", color=GOLD_ACCENT)], scale_factor=0.7)
        left_side_eq6 = VGroup(create_var_x(color=LIGHT_BLUE_ACCENT), create_operator("+"), frac_b_2a_right).arrange(RIGHT, buff=0.1)

        # Right side: +/- sqrt(b^2 - 4ac) / 2a
        b_sq_in_sqrt = VGroup(create_number("b", color=GOLD_ACCENT), create_superscript_on_mobject(create_number("b", color=GOLD_ACCENT), "2", scale_factor=0.6, color=LIGHT_BLUE_ACCENT))
        four_ac_in_sqrt = VGroup(create_number("4"), create_number("a", color=GOLD_ACCENT), create_number("c", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)
        sqrt_content_parts = [b_sq_in_sqrt, create_operator("-"), four_ac_in_sqrt]

        sqrt_term_display = VGroup(create_operator("sqrt("), *sqrt_content_parts, create_operator(")")).arrange(RIGHT, buff=0.05)
        den_2a_val = VGroup(create_number("2"), create_number("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)
        
        right_frac_sqrt = create_fraction([sqrt_term_display], [den_2a_val], scale_factor=0.7, color=LIGHT_BLUE_ACCENT)
        right_side_eq6 = VGroup(create_operator("+/-"), right_frac_sqrt).arrange(RIGHT, buff=0.1)

        eq6_mobjects = VGroup(
            left_side_eq6, create_operator("="), right_side_eq6
        ).arrange(RIGHT, buff=0.2).center()

        self.play(FadeOut(eq5_mobjects), FadeIn(eq6_mobjects))
        self.wait(1.5)
        self.play(FadeOut(sqrt_sides_text))

        isolate_x_text = Text("Isolate x:", font_size=DEFAULT_TEXT_FONT_SIZE * 0.8, color=WHITE).next_to(eq6_mobjects, DOWN, buff=0.7)
        self.play(FadeIn(isolate_x_text))

        # Equation 7 (Final Formula): x = (-b +/- sqrt(b^2 - 4ac)) / 2a
        # Numerator: -b +/- sqrt(b^2 - 4ac)
        final_neg_b = VGroup(create_operator("-"), create_number("b", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.05)
        final_numerator_group = VGroup(
            create_operator("("), final_neg_b, create_operator("+/-"), sqrt_term_display.copy(), create_operator(")")
        ).arrange(RIGHT, buff=0.05)

        # Denominator: 2a
        final_denominator_group = VGroup(create_number("2"), create_number("a", color=GOLD_ACCENT)).arrange(RIGHT, buff=0.1)

        final_quadratic_formula_frac = create_fraction([final_numerator_group], [final_denominator_group], scale_factor=0.7, color=LIGHT_BLUE_ACCENT)

        eq7_mobjects = VGroup(
            create_var_x(color=LIGHT_BLUE_ACCENT), create_operator("="), final_quadratic_formula_frac
        ).arrange(RIGHT, buff=0.2).center()
        
        self.play(FadeOut(eq6_mobjects), FadeIn(eq7_mobjects))
        self.wait(2.5)
        self.play(FadeOut(isolate_x_text, beat_title4))

        # --- Recap Card ---
        self.play(eq7_mobjects.animate.scale(1.2).center().to_edge(UP, buff=1.5))
        recap_title = Text("The Quadratic Formula", font_size=DEFAULT_TEXT_FONT_SIZE + 10, color=GOLD_ACCENT).next_to(eq7_mobjects, DOWN, buff=1.0)
        recap_text = Text(
            "Remember: It comes from 'completing the square'!",
            font_size=DEFAULT_TEXT_FONT_SIZE,
            color=WHITE
        ).next_to(recap_title, DOWN, buff=0.5)

        self.play(FadeIn(recap_title, recap_text))
        self.wait(3)
        self.play(FadeOut(intro_title, eq7_mobjects, recap_title, recap_text))
        self.wait(1)