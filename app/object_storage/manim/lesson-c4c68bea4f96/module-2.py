from manim import *

# --- Configuration ---
config.background_color = "#1a1a1a"
BLUE_ACCENT = "#87CEEB"
GOLD_ACCENT = "#FFD700"
WHITE_TEXT = "#FFFFFF"
RED_HIGHLIGHT = "#FF6347"

# --- Helper Functions for Equation Building (No Tex/MathTex) ---

def create_text_mobject(text_str, color=WHITE_TEXT, font_size=40):
    """Creates a Manim Text mobject with default styling."""
    return Text(text_str, color=color, font_size=font_size)

def create_superscript_mobject(base_mobject_or_str, superscript_str, color=WHITE_TEXT, font_size=40):
    """Creates a VGroup representing a base with a superscript."""
    if isinstance(base_mobject_or_str, str):
        base_mobject = create_text_mobject(base_mobject_or_str, color=color, font_size=font_size)
    else:
        base_mobject = base_mobject_or_str
    
    superscript = create_text_mobject(superscript_str, color=color, font_size=font_size * 0.7)
    superscript.next_to(base_mobject, UP + RIGHT, buff=0.05).align_to(base_mobject, UP)
    return VGroup(base_mobject, superscript)

def create_fraction_mobject(numerator_mobj_or_str, denominator_mobj_or_str, color=WHITE_TEXT, font_size=40):
    """Creates a VGroup representing a fraction with numerator, fraction line, and denominator."""
    if isinstance(numerator_mobj_or_str, str):
        numerator_mobj = create_text_mobject(numerator_mobj_or_str, color=color, font_size=font_size)
    else:
        numerator_mobj = numerator_mobj_or_str
    
    if isinstance(denominator_mobj_or_str, str):
        denominator_mobj = create_text_mobject(denominator_mobj_or_str, color=color, font_size=font_size)
    else:
        denominator_mobj = denominator_mobj_or_str

    fraction_line = Line(LEFT, RIGHT, color=color)
    
    # Adjust line width based on the wider of numerator/denominator
    line_width = max(numerator_mobj.width, denominator_mobj.width) * 1.2
    fraction_line.set_width(line_width)
    
    # Position numerator above, denominator below, aligned to the center of the line
    numerator_mobj.next_to(fraction_line, UP, buff=0.15).align_to(fraction_line, X_AXIS)
    denominator_mobj.next_to(fraction_line, DOWN, buff=0.15).align_to(fraction_line, X_AXIS)
        
    return VGroup(numerator_mobj, fraction_line, denominator_mobj)

def assemble_equation(mobjects, buff=0.2):
    """Assembles a list of mobjects horizontally with specified buffer."""
    if not mobjects:
        return VGroup()
    
    equation_group = VGroup(mobjects[0])
    for i in range(1, len(mobjects)):
        mobjects[i].next_to(equation_group[-1], RIGHT, buff=buff)
        equation_group.add(mobjects[i])
    return equation_group

class DeriveQuadraticFormula(Scene):
    def construct(self):
        # --- Beat 1: Visual Hook & Introduction ---
        title = create_text_mobject("Deriving the Quadratic Formula", font_size=60, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Visual Hook: A simple parabola showing its roots
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            background_line_style={"stroke_opacity": 0.3},
            faded_line_style={"stroke_opacity": 0}
        ).shift(DOWN*0.5)
        
        parabola_func = lambda x: 0.5 * x**2 - 2
        parabola = plane.get_graph(parabola_func, x_range=[-3, 3], color=BLUE_ACCENT)
        
        x_intercept_1 = plane.coords_to_point(-2, 0)
        x_intercept_2 = plane.coords_to_point(2, 0)
        root_dot_1 = Dot(x_intercept_1, color=RED_HIGHLIGHT, radius=0.1)
        root_dot_2 = Dot(x_intercept_2, color=RED_HIGHLIGHT, radius=0.1)
        
        self.play(Create(plane), Create(parabola), run_time=1.5)
        self.play(FadeIn(root_dot_1, scale=0.5), FadeIn(root_dot_2, scale=0.5))
        self.wait(1)

        question_text = create_text_mobject("How do we find these roots for ANY quadratic?", font_size=36, color=WHITE_TEXT).next_to(plane, UP, buff=0.8)
        self.play(Write(question_text))
        self.wait(2)

        self.play(FadeOut(plane, parabola, root_dot_1, root_dot_2, question_text))
        
        # Introduce the general form: ax^2 + bx + c = 0
        a_coeff = create_text_mobject("a", color=GOLD_ACCENT)
        x_base = create_text_mobject("x", color=BLUE_ACCENT)
        x_squared = create_superscript_mobject(x_base, "2")
        ax_squared = assemble_equation([a_coeff, x_squared], buff=0.1)
        
        plus_bx = assemble_equation([create_text_mobject("+"), create_text_mobject("b", color=GOLD_ACCENT), create_text_mobject("x", color=BLUE_ACCENT)], buff=0.1)
        plus_c = assemble_equation([create_text_mobject("+"), create_text_mobject("c", color=GOLD_ACCENT)], buff=0.1)
        equals_zero = assemble_equation([create_text_mobject("="), create_text_mobject("0")], buff=0.1)
        
        general_quadratic = assemble_equation([ax_squared, plus_bx, plus_c, equals_zero]).center().shift(UP*0.5)
        self.play(Write(general_quadratic), run_time=2)
        self.wait(1)
        
        current_eq = general_quadratic

        # --- Beat 2: Isolate x^2 and x terms ---
        self.play(FadeOut(title), current_eq.animate.to_edge(UP).shift(DOWN*0.5))
        self.wait(0.5)

        # Transition: ax^2 + bx = -c
        minus_c = create_text_mobject("-c", color=GOLD_ACCENT)
        equals_minus_c = assemble_equation([create_text_mobject("="), minus_c], buff=0.1)
        
        # Re-create parts for the new equation structure
        new_ax_squared = ax_squared.copy()
        new_plus_bx = plus_bx.copy()
        new_eq_step1 = assemble_equation([new_ax_squared, new_plus_bx, equals_minus_c]).center().shift(UP*0.5)

        self.play(
            FadeOut(current_eq[2]), # Fade out '+c'
            ReplacementTransform(current_eq[3], equals_minus_c), # Transform '=0' to '= -c'
            # Explicitly move non-transformed parts to new positions
            new_ax_squared.animate.move_to(new_eq_step1[0].get_center()),
            new_plus_bx.animate.move_to(new_eq_step1[1].get_center()),
            run_time=1.5
        )
        current_eq = new_eq_step1
        self.wait(1)

        # Divide by 'a'
        divide_a_text = create_text_mobject("Divide by 'a'", font_size=30, color=WHITE_TEXT).next_to(current_eq, DOWN, buff=0.5)
        self.play(Write(divide_a_text))
        
        # Transition: x^2 + (b/a)x = -c/a
        x_squared_alone = create_superscript_mobject(create_text_mobject("x", color=BLUE_ACCENT), "2")
        
        b_over_a_frac = create_fraction_mobject(create_text_mobject("b", color=GOLD_ACCENT), create_text_mobject("a", color=GOLD_ACCENT))
        plus_b_over_a_x = assemble_equation([create_text_mobject("+"), b_over_a_frac, create_text_mobject("x", color=BLUE_ACCENT)], buff=0.1)
        new_left_side = assemble_equation([x_squared_alone, plus_b_over_a_x])
        
        minus_c_over_a_frac = create_fraction_mobject(create_text_mobject("-c", color=GOLD_ACCENT), create_text_mobject("a", color=GOLD_ACCENT))
        new_equals_right_side = assemble_equation([create_text_mobject("="), minus_c_over_a_frac])
        
        new_eq_step2 = assemble_equation([new_left_side, new_equals_right_side]).center().shift(UP*0.5)
        
        self.play(
            FadeOut(divide_a_text),
            ReplacementTransform(current_eq, new_eq_step2), # Transform the whole group
            run_time=2
        )
        current_eq = new_eq_step2
        self.wait(1)
        
        # --- Beat 3: Completing the Square ---
        self.play(current_eq.animate.to_edge(UP).shift(DOWN*0.5))
        self.wait(0.5)
        
        complete_square_text = create_text_mobject("Completing the Square", font_size=40, color=GOLD_ACCENT).next_to(current_eq, DOWN, buff=0.5)
        self.play(Write(complete_square_text))
        self.wait(1)

        # Show the term to add: (b/2a)^2
        b_num_frac = create_text_mobject("b", color=GOLD_ACCENT)
        two_a_den_text_2 = create_text_mobject("2")
        two_a_den_text_a = create_text_mobject("a", color=GOLD_ACCENT)
        two_a_den_frac = assemble_equation([two_a_den_text_2, two_a_den_text_a], buff=0.05)
        b_over_2a_frac = create_fraction_mobject(b_num_frac, two_a_den_frac)
        b_over_2a_squared = create_superscript_mobject(b_over_2a_frac, "2")
        
        term_to_add = b_over_2a_squared.copy().scale(0.8).next_to(complete_square_text, DOWN, buff=0.5)
        add_text = create_text_mobject("Add this to both sides:", font_size=30).next_to(term_to_add, UP)
        self.play(FadeIn(term_to_add, shift=UP), Write(add_text))
        self.wait(1)
        self.play(FadeOut(add_text))

        # Transition: x^2 + (b/a)x + (b/2a)^2 = -c/a + (b/2a)^2
        plus_term_left_added = assemble_equation([create_text_mobject("+"), b_over_2a_squared.copy()], buff=0.1)
        plus_term_right_added = assemble_equation([create_text_mobject("+"), b_over_2a_squared.copy()], buff=0.1)
        
        new_left_side_added_eq = assemble_equation([current_eq[0][0].copy(), current_eq[0][1].copy(), plus_term_left_added])
        new_right_side_added_eq = assemble_equation([current_eq[1][0].copy(), current_eq[1][1].copy(), plus_term_right_added])
        new_eq_step3_added = assemble_equation([new_left_side_added_eq, new_right_side_added_eq]).center().shift(UP*0.5)

        self.play(
            FadeOut(complete_square_text), FadeOut(term_to_add),
            ReplacementTransform(current_eq, new_eq_step3_added),
            run_time=2
        )
        current_eq = new_eq_step3_added
        self.wait(1)

        # Factor the left side: (x + b/2a)^2
        # Left side factored base
        x_factor = create_text_mobject("x", color=BLUE_ACCENT)
        b_over_2a_factor = b_over_2a_frac.copy()
        left_side_factored_base = assemble_equation([create_text_mobject("("), x_factor, create_text_mobject("+"), b_over_2a_factor, create_text_mobject(")")], buff=0.1)
        left_side_factored = create_superscript_mobject(left_side_factored_base, "2")

        # Right side: -c/a + b^2/4a^2
        b_sq_num = create_superscript_mobject(create_text_mobject("b", color=GOLD_ACCENT), "2")
        four_a_sq_den = assemble_equation([create_text_mobject("4"), create_superscript_mobject(create_text_mobject("a", color=GOLD_ACCENT), "2")], buff=0.05)
        b_sq_over_4a_sq = create_fraction_mobject(b_sq_num, four_a_sq_den)
        
        # Combine current right side parts
        right_side_combined_terms = assemble_equation([current_eq[1][1].copy(), create_text_mobject("+"), b_sq_over_4a_sq])

        new_equals_sign = create_text_mobject("=").next_to(left_side_factored, RIGHT, buff=0.2)
        new_eq_step3_factored = assemble_equation([left_side_factored, new_equals_sign, right_side_combined_terms]).center().shift(UP*0.5)
        
        self.play(
            ReplacementTransform(current_eq, new_eq_step3_factored),
            run_time=2
        )
        current_eq = new_eq_step3_factored
        self.wait(1)

        # Combine right side: (b^2 - 4ac) / 4a^2
        b_sq_num_combined = create_superscript_mobject(create_text_mobject("b", color=GOLD_ACCENT), "2")
        minus_4ac = assemble_equation([create_text_mobject("-"), create_text_mobject("4"), create_text_mobject("a", color=GOLD_ACCENT), create_text_mobject("c", color=GOLD_ACCENT)], buff=0.1)
        combined_numerator = assemble_equation([b_sq_num_combined, minus_4ac], buff=0.2)
        
        combined_denominator = four_a_sq_den.copy() # Reuse 4a^2 denominator
        
        combined_fraction_right = create_fraction_mobject(combined_numerator, combined_denominator)
        
        new_equals_sign_combined = create_text_mobject("=").next_to(current_eq[0], RIGHT, buff=0.2)
        new_eq_step3_combined = assemble_equation([current_eq[0].copy(), new_equals_sign_combined, combined_fraction_right]).center().shift(UP*0.5)

        self.play(
            ReplacementTransform(current_eq, new_eq_step3_combined),
            run_time=1.5
        )
        current_eq = new_eq_step3_combined
        self.wait(1)

        # --- Beat 4: Solving for x ---
        self.play(current_eq.animate.to_edge(UP).shift(DOWN*0.5))
        self.wait(0.5)

        take_root_text = create_text_mobject("Take the square root of both sides", font_size=30, color=GOLD_ACCENT).next_to(current_eq, DOWN, buff=0.5)
        self.play(Write(take_root_text))
        self.wait(1)

        # Left side: x + b/2a
        x_plus_b_over_2a = assemble_equation([create_text_mobject("x", color=BLUE_ACCENT), create_text_mobject("+"), b_over_2a_frac.copy()], buff=0.1)

        # Right side: +/- sqrt(b^2 - 4ac) / 2a
        plus_minus = create_text_mobject("±", font_size=40, color=WHITE_TEXT) # Unicode plus-minus
        
        sqrt_open = create_text_mobject("sqrt(", color=GOLD_ACCENT)
        sqrt_close = create_text_mobject(")", color=GOLD_ACCENT)
        sqrt_term_num = assemble_equation([sqrt_open, combined_numerator.copy(), sqrt_close], buff=0.05)

        two_a_den_final = assemble_equation([create_text_mobject("2"), create_text_mobject("a", color=GOLD_ACCENT)], buff=0.05)
        
        simplified_sqrt_fraction = create_fraction_mobject(sqrt_term_num, two_a_den_final)
        
        right_side_root_final = assemble_equation([plus_minus, simplified_sqrt_fraction], buff=0.1)

        new_equals_root = create_text_mobject("=").next_to(x_plus_b_over_2a, RIGHT, buff=0.2)
        new_eq_step4_rooted = assemble_equation([x_plus_b_over_2a, new_equals_root, right_side_root_final]).center().shift(UP*0.5)

        self.play(
            FadeOut(take_root_text),
            ReplacementTransform(current_eq, new_eq_step4_rooted),
            run_time=2
        )
        current_eq = new_eq_step4_rooted
        self.wait(1)
        
        # Isolate x
        isolate_x_text = create_text_mobject("Isolate 'x'", font_size=30, color=GOLD_ACCENT).next_to(current_eq, DOWN, buff=0.5)
        self.play(Write(isolate_x_text))
        self.wait(1)

        # Transition: x = -b/2a +/- sqrt(...) / 2a
        x_final = create_text_mobject("x", color=BLUE_ACCENT)
        
        minus_b_num_isolated = create_text_mobject("-b", color=GOLD_ACCENT)
        minus_b_over_2a_isolated = create_fraction_mobject(minus_b_num_isolated, two_a_den_final.copy())
        
        right_side_isolated_terms = assemble_equation([minus_b_over_2a_isolated, right_side_root_final.copy()], buff=0.2)
        
        new_equals_isolated = create_text_mobject("=").next_to(x_final, RIGHT, buff=0.2)
        new_eq_step4_isolated = assemble_equation([x_final, new_equals_isolated, right_side_isolated_terms]).center().shift(UP*0.5)
        
        self.play(
            FadeOut(isolate_x_text),
            ReplacementTransform(current_eq, new_eq_step4_isolated),
            run_time=2
        )
        current_eq = new_eq_step4_isolated
        self.wait(1)

        # --- Beat 5: Final Formula & Recap ---
        self.play(current_eq.animate.to_edge(UP).shift(DOWN*0.5))
        self.wait(0.5)
        
        # Combine into a single fraction: x = (-b +/- sqrt(b^2 - 4ac)) / 2a
        final_numerator_parts = assemble_equation([create_text_mobject("-b", color=GOLD_ACCENT), plus_minus.copy(), sqrt_term_num.copy()], buff=0.1)
        final_denominator_parts = two_a_den_final.copy()
        
        final_formula_fraction = create_fraction_mobject(final_numerator_parts, final_denominator_parts)
        
        final_x_display = create_text_mobject("x", color=BLUE_ACCENT)
        final_equals_display = create_text_mobject("=")
        
        final_formula_mobject = assemble_equation([final_x_display, final_equals_display, final_formula_fraction]).center().shift(UP*0.5)
        
        self.play(
            ReplacementTransform(current_eq, final_formula_mobject),
            run_time=2
        )
        self.wait(2)

        # Recap Card
        self.play(FadeOut(final_formula_mobject))
        
        recap_title = create_text_mobject("Recap: Steps to Derive", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        step1 = create_text_mobject("1. Isolate ax^2 + bx", font_size=36, color=WHITE_TEXT).shift(UP*1.5 + LEFT*2)
        step2 = create_text_mobject("2. Divide by 'a'", font_size=36, color=WHITE_TEXT).next_to(step1, DOWN, buff=0.5).align_to(step1, LEFT)
        step3 = create_text_mobject("3. Complete the square (add (b/2a)^2)", font_size=36, color=WHITE_TEXT).next_to(step2, DOWN, buff=0.5).align_to(step1, LEFT)
        step4 = create_text_mobject("4. Take square root", font_size=36, color=WHITE_TEXT).next_to(step3, DOWN, buff=0.5).align_to(step1, LEFT)
        step5 = create_text_mobject("5. Isolate 'x' & Simplify", font_size=36, color=WHITE_TEXT).next_to(step4, DOWN, buff=0.5).align_to(step1, LEFT)
        
        recap_steps = VGroup(step1, step2, step3, step4, step5)

        self.play(Write(recap_title), LaggedStart(*[FadeIn(step, shift=UP) for step in recap_steps], lag_ratio=0.3))
        self.wait(3)

        # Final Formula Display
        final_formula_display_large = final_formula_mobject.copy().scale(1.2).center()
        # Apply specific colors for emphasis (this part is brittle due to no MathTex)
        final_formula_display_large[0].set_color(BLUE_ACCENT) # 'x'
        final_formula_display_large[1].set_color(WHITE_TEXT) # '='
        final_formula_display_large[2][0][0].set_color(GOLD_ACCENT) # '-b'
        final_formula_display_large[2][0][1].set_color(WHITE_TEXT) # '±'
        # The sqrt part is a nested VGroup, coloring its components
        final_formula_display_large[2][0][2][0].set_color(GOLD_ACCENT) # 'sqrt('
        final_formula_display_large[2][0][2][1][0].set_color(GOLD_ACCENT) # 'b^2'
        final_formula_display_large[2][0][2][1][1][0].set_color(WHITE_TEXT) # '-'
        final_formula_display_large[2][0][2][1][1][1].set_color(WHITE_TEXT) # '4'
        final_formula_display_large[2][0][2][1][1][2].set_color(GOLD_ACCENT) # 'a'
        final_formula_display_large[2][0][2][1][1][3].set_color(GOLD_ACCENT) # 'c'
        final_formula_display_large[2][0][2][2].set_color(GOLD_ACCENT) # ')'
        final_formula_display_large[2][2][0].set_color(WHITE_TEXT) # '2'
        final_formula_display_large[2][2][1].set_color(GOLD_ACCENT) # 'a'

        self.play(FadeOut(recap_steps), FadeOut(recap_title))
        self.play(Write(final_formula_display_large))
        self.wait(3)
        self.play(FadeOut(final_formula_display_large))