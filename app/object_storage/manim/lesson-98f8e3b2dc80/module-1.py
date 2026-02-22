from manim import *

class QuadraticFormulaAnimation(Scene):
    def construct(self):
        # 1. Configuration: Dark background, high-contrast colors
        self.camera.background_color = BLACK
        # Define custom colors for consistency, inspired by 3Blue1Brown
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C
        RED_ACCENT = RED_E # For 'a' coefficients and highlights
        GREEN_ACCENT = GREEN_E # For solutions/roots

        # --- Beat 1: The Problem & Visual Hook (Introduction to Parabolas) ---
        # Approximately 10 seconds
        self.next_section("Beat 1: The Problem", skip_animations=False)

        # Module Title
        title = Text("Quadratic Equations", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)

        # Visual hook: A projectile path
        intro_text = Text(
            "Curved motion, areas, projectile trajectories...",
            font_size=30, color=WHITE
        ).next_to(title, DOWN, buff=0.5)
        
        # Define a parabola for the projectile path
        # A simple projectile path that starts at (0,0) and lands further
        projectile_func = lambda t: np.array([t, -0.5 * t**2 + 4 * t, 0])
        # Create a temporary plane to visualize the path, then fade it out.
        temp_plane = NumberPlane(
            x_range=[-1, 9, 1], y_range=[-1, 9, 1],
            x_length=10, y_length=7,
            background_line_style={"stroke_opacity": 0} # Invisible lines
        ).shift(DOWN*1)

        projectile_path = temp_plane.get_graph(projectile_func, x_range=[0, 8], color=BLUE_ACCENT, stroke_width=6)
        
        # A small dot moving along the path
        dot = Dot(color=RED_ACCENT, radius=0.1).move_to(projectile_path.get_start())
        
        self.play(
            LaggedStart(
                FadeIn(intro_text, shift=UP),
                Create(projectile_path),
                MoveAlongPath(dot, projectile_path, run_time=3.5, rate_func=linear),
                lag_ratio=0.7
            )
        )
        self.play(FadeOut(dot))
        self.wait(1)
        self.play(FadeOut(intro_text))

        # Setup Axes and NumberPlane for detailed view
        plane = NumberPlane(
            x_range=[-1, 6, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=7,
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            }
        ).add_coordinates()
        axes_labels = plane.get_axis_labels(x_label="x", y_label="y")

        self.play(
            FadeOut(projectile_path), # Fade out the initial dynamic path
            ReplacementTransform(title, title.copy().scale(0.8).to_edge(UP + LEFT)), # Shrink title
            Create(plane),
            FadeIn(axes_labels)
        )
        self.wait(0.5)

        # Introduce the general form of a quadratic equation
        quadratic_eqn_form = MathTex(
            "ax^2 + bx + c = 0",
            font_size=50,
            color=WHITE
        ).next_to(title, RIGHT, buff=0.5)
        
        self.play(Write(quadratic_eqn_form))
        self.wait(1)

        # Graph an example parabola: y = x^2 - 4x + 3
        # This parabola has roots at x=1 and x=3
        parabola_func = lambda x: x**2 - 4*x + 3
        parabola = plane.get_graph(parabola_func, x_range=[-0.5, 4.5], color=BLUE_ACCENT, stroke_width=4)
        
        self.play(Create(parabola))
        self.wait(0.5)

        # Highlight the x-intercepts (roots)
        root1_dot = Dot(plane.c2p(1, 0), color=GREEN_ACCENT, radius=0.1)
        root2_dot = Dot(plane.c2p(3, 0), color=GREEN_ACCENT, radius=0.1)
        
        self.play(
            GrowSmallestToLargest(root1_dot),
            GrowSmallestToLargest(root2_dot),
            run_time=0.8
        )
        
        question = Text("How do we find these X-values?", font_size=35, color=GOLD_ACCENT).next_to(quadratic_eqn_form, DOWN)
        self.play(Write(question))
        self.wait(2)

        self.play(FadeOut(question))


        # --- Beat 2: Intuition - The "Center" and "Spread" ---
        # Approximately 8 seconds
        self.next_section("Beat 2: Intuition", skip_animations=False)

        # Keep the equation ax^2 + bx + c = 0 and the parabola/roots
        # Emphasize the vertex as the center of the roots
        
        # For x^2 - 4x + 3 = 0, a=1, b=-4, c=3. Vertex x = -(-4)/(2*1) = 2
        vertex_x_coord = -(-4) / (2 * 1) 
        
        vertex_line = DashedLine(
            plane.c2p(vertex_x_coord, plane.y_range[0]),
            plane.c2p(vertex_x_coord, plane.y_range[1]),
            color=RED_ACCENT
        )
        
        center_label = MathTex("x = -\\frac{b}{2a}", font_size=35, color=RED_ACCENT).next_to(vertex_line, UP+RIGHT, buff=0.2)
        center_text_explanation = Text("The 'Center'", font_size=30, color=RED_ACCENT).next_to(center_label, DOWN)

        self.play(Create(vertex_line), Write(center_label))
        self.play(Write(center_text_explanation))
        self.wait(1)

        # Show the roots are equidistant from this center
        arrow1 = Arrow(start=plane.c2p(vertex_x_coord, 0.5), end=plane.c2p(1, 0.5), color=GREEN_ACCENT, buff=0, stroke_width=5)
        arrow2 = Arrow(start=plane.c2p(vertex_x_coord, 0.5), end=plane.c2p(3, 0.5), color=GREEN_ACCENT, buff=0, stroke_width=5)
        
        offset_tex = MathTex("\\pm \\text{offset}", font_size=40, color=GREEN_ACCENT).next_to(arrow1, LEFT)
        
        self.play(Create(arrow1), Create(arrow2))
        self.play(Write(offset_tex))
        self.wait(1.5)

        self.play(
            FadeOut(vertex_line),
            FadeOut(center_label),
            FadeOut(center_text_explanation),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(offset_tex),
        )


        # --- Beat 3: Unveiling the Formula ---
        # Approximately 8 seconds
        self.next_section("Beat 3: The Formula", skip_animations=False)

        # Position the general form to the left
        quadratic_eqn_form_final_pos = quadratic_eqn_form.copy()
        self.play(
            quadratic_eqn_form_final_pos.animate.scale(0.9).move_to(LEFT * 4 + UP * 2)
        )
        
        # Highlight a, b, c in the general equation
        # ax^2 + bx + c = 0
        self.play(
            Indicate(quadratic_eqn_form_final_pos[0][0], color=RED_ACCENT), # 'a'
            Indicate(quadratic_eqn_form_final_pos[0][3], color=BLUE_ACCENT), # 'b'
            Indicate(quadratic_eqn_form_final_pos[0][6], color=GOLD_ACCENT), # 'c'
            run_time=1
        )
        self.wait(0.5)

        # Present the Quadratic Formula
        quadratic_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=60,
            color=WHITE
        ).move_to(RIGHT * 2)

        # Color code a, b, c in the formula
        quadratic_formula.set_color_by_tex("a", RED_ACCENT)
        quadratic_formula.set_color_by_tex("b", BLUE_ACCENT)
        quadratic_formula.set_color_by_tex("c", GOLD_ACCENT)
        
        self.play(Write(quadratic_formula))
        self.wait(1)

        # Briefly highlight parts of the formula, linking to intuition
        formula_parts_text = VGroup(
            Text("Center offset", font_size=25, color=BLUE_ACCENT).next_to(quadratic_formula[0][2], UP, buff=0.2), # -b
            Text("Spread / Discriminant", font_size=25, color=GOLD_ACCENT).next_to(quadratic_formula[0][6:13], UP, buff=0.2), # b^2 - 4ac
            Text("Scaling factor", font_size=25, color=RED_ACCENT).next_to(quadratic_formula[0][15:17], DOWN, buff=0.2) # 2a
        ).arrange(DOWN, center=False, aligned_edge=LEFT)


        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(formula_parts_text[0]), Indicate(quadratic_formula[0][2], color=BLUE_ACCENT)), # -b
                AnimationGroup(FadeIn(formula_parts_text[1]), Indicate(quadratic_formula[0][6:13], color=GOLD_ACCENT)), # b^2 - 4ac
                AnimationGroup(FadeIn(formula_parts_text[2]), Indicate(quadratic_formula[0][15:17], color=RED_ACCENT)), # 2a
                lag_ratio=0.7
            )
        )
        self.wait(2)
        self.play(FadeOut(formula_parts_text))


        # --- Beat 4: Application - Finding the Roots ---
        # Approximately 15 seconds
        self.next_section("Beat 4: Application", skip_animations=False)

        # Clear the plane and the existing parabola/dots
        self.play(
            FadeOut(plane),
            FadeOut(axes_labels),
            FadeOut(parabola),
            FadeOut(root1_dot),
            FadeOut(root2_dot),
            FadeOut(quadratic_eqn_form_final_pos), # Fade out the general form, we're using a specific one now
            quadratic_formula.animate.scale(0.8).to_edge(UP).shift(LEFT*2) # Move formula to top-left for reference
        )

        # Specific example: x^2 - 4x + 3 = 0
        specific_eqn = MathTex("x^2 - 4x + 3 = 0", font_size=50, color=WHITE).move_to(UP * 1)
        self.play(Write(specific_eqn))
        self.wait(1)

        # Identify a, b, c values for the example
        abc_values = VGroup(
            MathTex("a = 1", color=RED_ACCENT),
            MathTex("b = -4", color=BLUE_ACCENT),
            MathTex("c = 3", color=GOLD_ACCENT)
        ).arrange(RIGHT, buff=1).next_to(specific_eqn, DOWN, buff=0.5)

        self.play(LaggedStart(*[FadeIn(val, shift=DOWN) for val in abc_values], lag_ratio=0.3))
        self.wait(1)

        # Substitution into the formula
        substitution_guide = MathTex(
            "x = \\frac{- (", "-4", ") \\pm \\sqrt{(", "-4", ")^2 - 4(", "1", ") (", "3", ")}}{2(", "1", ")}",
            font_size=45,
            color=WHITE
        ).next_to(abc_values, DOWN, buff=0.7)

        # Color the substituted values
        substitution_guide[1].set_color(BLUE_ACCENT)  # -4
        substitution_guide[3].set_color(BLUE_ACCENT)  # -4
        substitution_guide[5].set_color(RED_ACCENT)   # 1
        substitution_guide[7].set_color(GOLD_ACCENT)  # 3
        substitution_guide[9].set_color(RED_ACCENT)   # 1

        # Use ReplacementTransform from the abstract formula to the substituted one
        self.play(ReplacementTransform(quadratic_formula.copy().move_to(substitution_guide.get_center()), substitution_guide))
        self.wait(1.5)

        # Simplify step-by-step
        step1 = MathTex(
            "x = \\frac{4 \\pm \\sqrt{16 - 12}}{2}",
            font_size=45,
            color=WHITE
        ).move_to(substitution_guide.get_center())
        self.play(ReplacementTransform(substitution_guide, step1))
        self.wait(1)

        step2 = MathTex(
            "x = \\frac{4 \\pm \\sqrt{4}}{2}",
            font_size=45,
            color=WHITE
        ).move_to(step1.get_center())
        self.play(ReplacementTransform(step1, step2))
        self.wait(1)

        step3 = MathTex(
            "x = \\frac{4 \\pm 2}{2}",
            font_size=45,
            color=WHITE
        ).move_to(step2.get_center())
        self.play(ReplacementTransform(step2, step3))
        self.wait(1.5)

        # Calculate the two roots
        solution1 = MathTex("x_1 = \\frac{4 + 2}{2} = 3", color=GREEN_ACCENT, font_size=40).next_to(step3, DOWN, buff=0.7).shift(LEFT*2)
        solution2 = MathTex("x_2 = \\frac{4 - 2}{2} = 1", color=GREEN_ACCENT, font_size=40).next_to(solution1, RIGHT, buff=1)

        self.play(
            LaggedStart(
                FadeIn(solution1, shift=LEFT),
                FadeIn(solution2, shift=RIGHT),
                lag_ratio=0.8
            )
        )
        self.wait(2)

        # Briefly show the roots on a small graph again
        small_plane = NumberPlane(
            x_range=[0, 4, 1], y_range=[-1, 1, 1],
            x_length=6, y_length=3,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 0.5},
            axis_config={"stroke_opacity": 0.5, "include_numbers": False}
        ).scale(0.7).to_edge(RIGHT).shift(UP*1.5)
        small_parabola = small_plane.get_graph(parabola_func, x_range=[0.5, 3.5], color=BLUE_ACCENT, stroke_width=3)
        small_root1_dot = Dot(small_plane.c2p(1, 0), color=GREEN_ACCENT, radius=0.08)
        small_root2_dot = Dot(small_plane.c2p(3, 0), color=GREEN_ACCENT, radius=0.08)

        self.play(
            Create(small_plane),
            Create(small_parabola),
            GrowSmallestToLargest(small_root1_dot),
            GrowSmallestToLargest(small_root2_dot)
        )
        self.wait(2)
        
        # Clean up for recap
        self.play(
            FadeOut(specific_eqn),
            FadeOut(abc_values),
            FadeOut(step3),
            FadeOut(solution1),
            FadeOut(solution2),
            FadeOut(small_plane),
            FadeOut(small_parabola),
            FadeOut(small_root1_dot),
            FadeOut(small_root2_dot),
            FadeOut(quadratic_formula) # Fade out the initial formula reference
        )
        

        # --- Beat 5: Recap Card ---
        # Approximately 7 seconds
        self.next_section("Beat 5: Recap", skip_animations=False)

        recap_title = Text("Recap: The Quadratic Formula", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        
        final_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=70,
            color=WHITE
        ).move_to(UP*0.5)

        final_formula.set_color_by_tex("a", RED_ACCENT)
        final_formula.set_color_by_tex("b", BLUE_ACCENT)
        final_formula.set_color_by_tex("c", GOLD_ACCENT)

        purpose_text = VGroup(
            Text("Solves equations of the form:", font_size=30, color=WHITE),
            MathTex("ax^2 + bx + c = 0", font_size=40, color=WHITE)
                .set_color_by_tex("a", RED_ACCENT)
                .set_color_by_tex("b", BLUE_ACCENT)
                .set_color_by_tex("c", GOLD_ACCENT),
            Text("Finds the X-intercepts of parabolas.", font_size=30, color=WHITE)
        ).arrange(DOWN, buff=0.5).next_to(final_formula, DOWN, buff=1)

        self.play(
            Transform(title, recap_title),
            FadeIn(final_formula, shift=UP)
        )
        self.wait(0.5)
        self.play(
            LaggedStart(
                FadeIn(purpose_text[0], shift=DOWN),
                FadeIn(purpose_text[1], shift=DOWN),
                FadeIn(purpose_text[2], shift=DOWN),
                lag_ratio=0.5
            )
        )
        self.wait(3)
        self.play(FadeOut(*self.mobjects)) # Fade out everything at the end