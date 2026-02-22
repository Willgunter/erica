from manim import *

class GraphingSolutionsDiscriminant(Scene):
    def construct(self):
        # --- Configuration ---
        BLUE_ACCENT = '#58C4ED' # Bright cyan-blue
        GOLD_ACCENT = '#FFD700' # Pure gold
        DARK_TEXT_COLOR = WHITE # For text on dark background

        # --- Scene Setup ---
        self.camera.background_color = BLACK

        # --- Helper Function for Parabolas ---
        def get_parabola(a, b, c, x_range=(-4, 4), color=BLUE_ACCENT):
            return self.axes.get_graph(lambda x: a*x**2 + b*x + c, x_range=x_range, color=color)
        
        # Helper function to find x-intercepts for y = x^2 + C
        def get_x_intercepts_for_x_squared_plus_c(c_val, x_range=(-4, 4)):
            intercepts = []
            if c_val < 0:
                root1 = -np.sqrt(-c_val)
                root2 = np.sqrt(-c_val)
                if x_range[0] <= root1 <= x_range[1]:
                    intercepts.append(root1)
                if x_range[0] <= root2 <= x_range[1]:
                    intercepts.append(root2)
            elif c_val == 0:
                if x_range[0] <= 0 <= x_range[1]:
                    intercepts.append(0)
            return intercepts

        # --- Axes setup for graphing ---
        self.axes = Axes(
            x_range=[-4.5, 4.5, 1],
            y_range=[-4.5, 4.5, 1],
            x_length=9,
            y_length=9,
            tips=False,
            axis_config={"color": DARK_TEXT_COLOR, "include_numbers": True} # Include numbers for initial context
        )
        
        # Manually create 'x' and 'y' axis labels for finer control
        x_axis_label_text = MathTex("x", color=DARK_TEXT_COLOR).next_to(self.axes.x_axis.get_end(), DR)
        y_axis_label_text = MathTex("y", color=DARK_TEXT_COLOR).next_to(self.axes.y_axis.get_end(), UL)
        
        all_axes_labels = VGroup(
            self.axes.get_x_axis().get_tick_labels(),
            self.axes.get_y_axis().get_tick_labels(),
            x_axis_label_text,
            y_axis_label_text
        )

        self.play(Create(self.axes), Create(all_axes_labels))
        self.wait(0.5)

        # --- Beat 1: Visual Hook - Dynamic Parabola & Intercepts ---
        # Start with a parabola above the x-axis, then move it down.
        c_tracker = ValueTracker(2) # Initial c = 2, so y = x^2 + 2 (no intercepts)
        
        # The parabola function depends on the tracker's value
        parabola_func_dynamic = lambda x: x**2 + c_tracker.get_value()
        initial_parabola = self.axes.get_graph(parabola_func_dynamic, color=BLUE_ACCENT)

        # Intercepts are redrawn whenever c_tracker changes
        x_intercepts_dynamic = always_redraw(
            lambda: VGroup(*[
                Dot(self.axes.coords_to_point(x_val, 0), color=GOLD_ACCENT, radius=DEFAULT_DOT_RADIUS*1.5)
                for x_val in get_x_intercepts_for_x_squared_plus_c(c_tracker.get_value())
            ])
        )

        title_hook = Text("Graphing Solutions: Discriminant & X-intercepts", font_size=48, color=DARK_TEXT_COLOR).to_edge(UP)
        
        self.play(
            FadeIn(title_hook),
            Create(initial_parabola),
            run_time=1.5
        )
        self.play(FadeIn(x_intercepts_dynamic)) # Intercepts might not exist initially, so this will show an empty VGroup.
        self.wait(0.5)

        # Animate c decreasing: parabola moves down, intercepts appear, merge, then separate
        self.play(c_tracker.animate.set_value(-2), run_time=3) # Ends with y = x^2 - 2 (two intercepts)
        self.wait(1)

        # --- Beat 2: Intuition - How many crossings? ---
        question_text = Text(
            "How many times does a parabola cross the x-axis?",
            color=DARK_TEXT_COLOR, font_size=36
        ).next_to(self.axes, UP*2) # Position it above the axes

        self.play(
            FadeOut(initial_parabola),
            FadeOut(x_intercepts_dynamic),
            Transform(title_hook, question_text) # Transform title to question
        )
        
        # Show a generic parabola with two intercepts (y = x^2 - 1)
        parabola_intuition = get_parabola(1, 0, -1)
        dots_intuition = VGroup(
            Dot(self.axes.coords_to_point(-1, 0), color=GOLD_ACCENT, radius=DEFAULT_DOT_RADIUS*1.5),
            Dot(self.axes.coords_to_point(1, 0), color=GOLD_ACCENT, radius=DEFAULT_DOT_RADIUS*1.5)
        )
        self.play(Create(parabola_intuition), FadeIn(dots_intuition))
        self.wait(1.5)
        self.play(FadeOut(dots_intuition)) # Fade out dots to clear for next concept

        # --- Beat 3: Formal Notation - The Quadratic Formula's Secret ---
        quad_eq_text = MathTex("ax^2 + bx + c = 0", color=DARK_TEXT_COLOR).move_to(title_hook.get_center())
        self.play(Transform(title_hook, quad_eq_text)) # Question transforms to quadratic equation
        self.wait(1)

        quad_formula_text = MathTex(
            r"x = \frac{-b \pm \sqrt{", "b^2 - 4ac", r"}}{2a}",
            color=DARK_TEXT_COLOR
        ).next_to(title_hook, DOWN, buff=0.7).scale(0.8)
        
        # Highlight the discriminant
        discriminant_tex_part = quad_formula_text.get_parts_by_tex("b^2 - 4ac")[0]
        discriminant_box = SurroundingRectangle(discriminant_tex_part, color=GOLD_ACCENT, buff=0.1)

        self.play(
            FadeOut(parabola_intuition),
            Write(quad_formula_text)
        )
        self.wait(0.5)
        self.play(Create(discriminant_box))
        
        discriminant_label = MathTex(r"\text{Discriminant } (D)", color=GOLD_ACCENT).next_to(discriminant_box, DOWN, buff=0.3)
        self.play(FadeIn(discriminant_label))
        self.wait(1.5)

        # --- Beat 4: Connecting Discriminant to Intercepts (3 Scenarios) ---
        self.play(
            FadeOut(quad_formula_text),
            FadeOut(discriminant_box),
            FadeOut(discriminant_label),
            FadeOut(title_hook), # Clear previous text
            self.axes.animate.scale(0.8).to_edge(LEFT, buff=0.5), # Move axes to make room for text
            FadeOut(all_axes_labels), # Fade out all previous labels
            run_time=1.5
        )
        # We need to recreate tick labels and axis labels for the scaled axes if we want them.
        # For simplicity and focus on the parabolas, we'll keep them off for this beat.


        # Helper to get dots for intercepts
        def get_intercept_dots(coords):
            return VGroup(*[Dot(self.axes.coords_to_point(x, 0), color=GOLD_ACCENT, radius=DEFAULT_DOT_RADIUS*1.5) for x in coords])

        # Scenario 1: D > 0 (Two Real Roots)
        a1, b1, c1 = 1, 0, -2 # y = x^2 - 2; D = 0^2 - 4(1)(-2) = 8
        parabola1 = get_parabola(a1, b1, c1)
        dots1 = get_intercept_dots([-np.sqrt(2), np.sqrt(2)])
        
        text1_D = MathTex("D > 0", color=GOLD_ACCENT).next_to(self.axes, RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        text1_result = Text("2 Real Solutions\n2 X-intercepts", color=DARK_TEXT_COLOR, font_size=32).next_to(text1_D, DOWN, buff=0.5)

        self.play(Create(parabola1), FadeIn(dots1))
        self.play(Write(text1_D), Write(text1_result))
        self.wait(2)

        # Scenario 2: D = 0 (One Real Root)
        a2, b2, c2 = 1, 0, 0 # y = x^2; D = 0^2 - 4(1)(0) = 0
        parabola2 = get_parabola(a2, b2, c2)
        dots2 = get_intercept_dots([0]) # One intercept at (0,0)

        text2_D = MathTex("D = 0", color=GOLD_ACCENT).match_x(text1_D).match_y(text1_D)
        text2_result = Text("1 Real Solution\n1 X-intercept", color=DARK_TEXT_COLOR, font_size=32).match_x(text1_result).match_y(text1_result)

        self.play(
            ReplacementTransform(parabola1, parabola2),
            Transform(dots1, dots2), # Dots merge/transform
            TransformMatchingTex(text1_D, text2_D),
            TransformMatchingTex(text1_result, text2_result),
            run_time=2
        )
        self.wait(2)

        # Scenario 3: D < 0 (No Real Roots)
        a3, b3, c3 = 1, 0, 2 # y = x^2 + 2; D = 0^2 - 4(1)(2) = -8
        parabola3 = get_parabola(a3, b3, c3)
        # No dots for intercepts

        text3_D = MathTex("D < 0", color=GOLD_ACCENT).match_x(text1_D).match_y(text1_D)
        text3_result = Text("No Real Solutions\nNo X-intercepts", color=DARK_TEXT_COLOR, font_size=32).match_x(text1_result).match_y(text1_result)

        self.play(
            ReplacementTransform(parabola2, parabola3),
            FadeOut(dots1), # Fade out the single dot
            TransformMatchingTex(text2_D, text3_D),
            TransformMatchingTex(text2_result, text3_result),
            run_time=2
        )
        self.wait(2)

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(parabola3),
            FadeOut(text3_D),
            FadeOut(text3_result),
            FadeOut(self.axes),
            run_time=1.5
        )

        recap_title = Text("Recap: Discriminant & X-intercepts", color=BLUE_ACCENT, font_size=42).to_edge(UP)
        
        recap_content = VGroup(
            MathTex(r"\textbf{D > 0}", r"\implies \text{2 X-intercepts}", color=DARK_TEXT_COLOR),
            MathTex(r"\textbf{D = 0}", r"\implies \text{1 X-intercept}", color=DARK_TEXT_COLOR),
            MathTex(r"\textbf{D < 0}", r"\implies \text{0 X-intercepts}", color=DARK_TEXT_COLOR),
        ).arrange(DOWN, buff=0.7).scale(0.9)
        
        recap_card = Rectangle(
            width=recap_content.width + 1.5,
            height=recap_content.height + 1.5,
            color=DARK_TEXT_COLOR,
            fill_opacity=0.1,
            stroke_width=2
        ).move_to(recap_content.get_center())

        recap_group = VGroup(recap_title, recap_card, recap_content).center()

        self.play(
            LaggedStart(
                FadeIn(recap_title),
                Create(recap_card),
                Write(recap_content[0]),
                Write(recap_content[1]),
                Write(recap_content[2]),
                lag_ratio=0.7,
                run_time=4
            )
        )
        self.wait(3)