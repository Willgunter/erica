from manim import *

class QuadraticEquations(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_COLOR = '#88DAFF'  # Light blue
        GOLD_COLOR = '#FFD700'  # Gold
        TEXT_COLOR = WHITE

        # --- Beat 1: The Hook & Introduction ---
        # A dynamic visual hook: points forming a parabolic shape
        intro_dots = VGroup(*[Dot(radius=0.05, color=BLUE_COLOR) for _ in range(20)])
        
        # Define the target path (y = x^2)
        def parabolic_path(t):
            # Scale t from 0-1 to x-range e.g. -2 to 2 for better visibility
            x = t * 4 - 2 
            y = x**2 / 2    # Scale y to fit screen
            return np.array([x, y, 0])
        
        # Position dots initially randomly around center
        for dot in intro_dots:
            dot.move_to(np.random.rand(3) * 6 - 3 * np.array([1,1,0])) # Random position within a box
            
        # Title and Subtitle
        title = Text("What are Quadratic Equations?", font_size=55, color=GOLD_COLOR).to_edge(UP)
        subtitle = Text("Discovering the shapes of change...", font_size=30, color=BLUE_COLOR).next_to(title, DOWN, buff=0.4)

        # Animate dots forming a parabola
        self.play(
            LaggedStart(*[dot.animate.move_to(parabolic_path(i/len(intro_dots))) for i, dot in enumerate(intro_dots)],
                        lag_ratio=0.05, run_time=3)
        )
        self.wait(0.5)
        # Fade in title and subtitle, fade out dots
        self.play(
            FadeIn(title, shift=UP),
            FadeIn(subtitle, shift=UP),
            FadeOut(intro_dots)
        )
        self.wait(2)

        # --- Beat 2: Visualizing y = ax^2 - The Core Shape ---
        self.play(FadeOut(subtitle, shift=DOWN))
        self.play(title.animate.to_corner(UL).scale(0.7))

        # Setup NumberPlane and labels
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1], # Start with y >= 0 for x^2
            x_length=7,
            y_length=6,
            background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.6},
            axes_config={"include_numbers": True, "font_size": 24, "color": TEXT_COLOR}
        ).shift(DOWN*0.5)
        
        labels = plane.get_axis_labels(x_label="x", y_label="y")

        # Plot y = x^2
        eq_y_x_squared = MathTex("y = x^2", color=BLUE_COLOR).next_to(plane, UP, buff=0.5)
        graph_x_squared = plane.plot(lambda x: x**2, color=BLUE_COLOR)
        
        self.play(Create(plane), Create(labels))
        self.wait(0.5)
        self.play(Create(graph_x_squared), Write(eq_y_x_squared))
        self.wait(2)
        
        # Show what 'a' does
        eq_y_a_x_squared = MathTex("y = ax^2", color=BLUE_COLOR).move_to(eq_y_x_squared)
        graph_2x_squared = plane.plot(lambda x: 2*x**2, color=GOLD_COLOR)
        graph_half_x_squared = plane.plot(lambda x: 0.5*x**2, color=WHITE)
        
        parabola_text_width = Text("'a' changes its width...", font_size=24, color=WHITE).next_to(plane, RIGHT).shift(LEFT*0.5)
        parabola_text_direction = Text("...and direction.", font_size=24, color=WHITE).next_to(plane, RIGHT).shift(LEFT*0.5)
        
        self.play(ReplacementTransform(eq_y_x_squared, eq_y_a_x_squared))
        self.play(
            Transform(graph_x_squared, graph_2x_squared),
            FadeIn(parabola_text_width, shift=LEFT)
        )
        self.wait(1.5)
        self.play(Transform(graph_x_squared, graph_half_x_squared))
        self.wait(1)
        self.play(
            Transform(graph_x_squared, plane.plot(lambda x: -x**2, color=GOLD_COLOR)), # Flip
            ReplacementTransform(parabola_text_width, parabola_text_direction)
        )
        self.wait(1.5)
        
        parabola_name_text = Text("This curve is called a Parabola.", font_size=28, color=TEXT_COLOR).next_to(plane, DOWN, buff=0.5)
        self.play(
            FadeOut(parabola_text_direction),
            Transform(graph_x_squared, plane.plot(lambda x: x**2, color=BLUE_COLOR)), # Reset to x^2
            FadeIn(parabola_name_text, shift=UP)
        )
        self.wait(2)

        # --- Beat 3: Adding bx and c - Shifting and Moving ---
        self.play(FadeOut(parabola_name_text))
        
        # Add '+ c' for vertical shift
        eq_y_x_c = MathTex("y = x^2 + c", color=BLUE_COLOR).move_to(eq_y_a_x_squared)
        graph_x_squared_plus_2 = plane.plot(lambda x: x**2 + 2, color=GOLD_COLOR)
        vertical_shift_text = Text("'+ c' shifts it vertically...", font_size=24, color=WHITE).next_to(plane, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(eq_y_a_x_squared, eq_y_x_c),
            Transform(graph_x_squared, graph_x_squared_plus_2),
            FadeIn(vertical_shift_text, shift=UP)
        )
        self.wait(2)
        
        # Add '+ bx' for horizontal shift
        eq_y_x_bx_c = MathTex("y = ax^2 + bx + c", color=BLUE_COLOR).move_to(eq_y_x_c)
        graph_full_form = plane.plot(lambda x: 0.8*x**2 - 2*x + 3, color=GOLD_COLOR) # Example of full quadratic
        horizontal_shift_text = Text("...and '+ bx' shifts it horizontally.", font_size=24, color=WHITE).next_to(plane, DOWN, buff=0.5)

        self.play(FadeOut(vertical_shift_text, shift=DOWN))
        self.play(
            ReplacementTransform(eq_y_x_c, eq_y_x_bx_c),
            Transform(graph_x_squared, graph_full_form),
            FadeIn(horizontal_shift_text, shift=UP)
        )
        self.wait(2.5)

        # --- Beat 4: Formal Notation & Definition ---
        self.play(FadeOut(horizontal_shift_text, shift=DOWN))

        # Show general form
        eq_general_form = MathTex("y = ax^2 + bx + c", color=TEXT_COLOR).move_to(eq_y_x_bx_c)
        self.play(ReplacementTransform(eq_y_x_bx_c, eq_general_form))
        self.wait(1)

        # Introduce the quadratic equation (set to zero)
        quadratic_equation = MathTex("ax^2 + bx + c = 0", color=GOLD_COLOR, font_size=50).move_to(eq_general_form.get_center())
        
        definition_text = Text("This is a Quadratic Equation!", font_size=32, color=BLUE_COLOR).next_to(quadratic_equation, DOWN, buff=0.6)
        
        # Highlight coefficients and condition a != 0
        a_coeff = quadratic_equation.get_part_by_tex("a")
        b_coeff = quadratic_equation.get_part_by_tex("b")
        c_coeff = quadratic_equation.get_part_by_tex("c")

        a_expl = Text("Coefficients", font_size=24, color=TEXT_COLOR).next_to(quadratic_equation, RIGHT, buff=0.5).shift(UP*0.2)
        a_cond = MathTex("a \\neq 0", color=BLUE_COLOR, font_size=30).next_to(a_expl, DOWN, buff=0.2).align_left(a_expl)
        
        self.play(
            TransformMatchingTex(eq_general_form, quadratic_equation),
            FadeOut(graph_x_squared),
            FadeOut(plane),
            FadeOut(labels)
        )
        self.wait(1)
        self.play(
            FadeIn(definition_text, shift=UP),
            FadeIn(a_expl, shift=LEFT),
            FadeIn(a_cond, shift=LEFT)
        )
        self.wait(1)
        
        roots_text = Text("We are looking for the x-values", font_size=28, color=TEXT_COLOR).next_to(definition_text, DOWN, buff=0.5)
        roots_text2 = Text("where the parabola crosses the x-axis.", font_size=28, color=TEXT_COLOR).next_to(roots_text, DOWN, buff=0.2)
        
        self.play(FadeIn(roots_text, shift=UP))
        self.play(FadeIn(roots_text2, shift=UP))
        self.wait(3)

        self.play(
            FadeOut(quadratic_equation),
            FadeOut(definition_text),
            FadeOut(a_expl),
            FadeOut(a_cond),
            FadeOut(roots_text),
            FadeOut(roots_text2),
            title.animate.center().scale(1/0.7).to_edge(UP) # Reset title position and size
        )
        self.wait(0.5)

        # --- Beat 5: Recap Card ---
        self.play(FadeOut(title))
        
        recap_title = Text("Recap: Quadratic Equations", font_size=45, color=GOLD_COLOR).to_edge(UP)
        
        bullet1 = MathTex("1. ", "\\text{Form: } ax^2 + bx + c = 0", color=TEXT_COLOR, font_size=36)
        bullet2 = MathTex("2. ", "\\text{Creates a parabola shape}", color=TEXT_COLOR, font_size=36)
        bullet3 = MathTex("3. ", "\\text{Solutions are x-intercepts}", color=TEXT_COLOR, font_size=36)
        bullet4 = MathTex("4. ", "\\text{'a' cannot be zero}", color=TEXT_COLOR, font_size=36)
        
        bullets = VGroup(bullet1, bullet2, bullet3, bullet4).arrange(
            DOWN, aligned_edge=LEFT, buff=0.6
        ).next_to(recap_title, DOWN, buff=0.8).shift(LEFT*1.5)
        
        self.play(FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(*[FadeIn(bullet, shift=LEFT) for bullet in bullets], lag_ratio=0.2))
        self.wait(4)
        
        self.play(
            FadeOut(recap_title),
            FadeOut(bullets)
        )
        self.wait(1)