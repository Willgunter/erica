from manim import *

class GeometricInterpretationDiscriminant(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E
        GREY_TEXT = GREY_B

        # --- Initial Title ---
        title = Text("Geometric Interpretation & Discriminant", color=WHITE, font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title, shift=UP))

        # --- Beat 1: Visual Hook - Dynamic Parabola & Roots ---
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": GREY_TEXT},
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1, "stroke_opacity": 0.6}
        ).add_coordinates()
        plane.set_opacity(0.5)

        x_axis_label = Text("x", color=GREY_TEXT, font_size=24).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1)
        y_axis_label = Text("y", color=GREY_TEXT, font_size=24).next_to(plane.y_axis.get_end(), UP, buff=0.1)

        self.play(Create(plane), Write(x_axis_label), Write(y_axis_label))
        self.wait(0.5)

        # Parabola parameters: y = ax^2 + bx + c
        a_val = 1
        b_val = -2 # Vertex at x = -b/(2a) = 2/2 = 1
        c_tracker = ValueTracker(-2) # Tracks the vertical shift

        # Parabola as a ParametricFunction
        parabola = always_redraw(
            lambda: plane.get_graph(
                lambda x: a_val * x**2 + b_val * x + c_tracker.get_value(),
                x_range=[-4, 4],
                color=BLUE_ACCENT
            ).set_stroke(width=5)
        )

        # Dynamic equation text
        equation_text = always_redraw(
            lambda: Text(
                f"y = x^2 - 2x + {c_tracker.get_value():.1f}",
                color=WHITE, font_size=36
            ).to_corner(UP + LEFT)
        )
        
        # Dynamic dots for roots
        def get_root_dots():
            current_c = c_tracker.get_value()
            disc = b_val**2 - 4 * a_val * current_c # Discriminant for x^2 - 2x + c = 0
            new_dots_group = VGroup()
            if disc > 0: # Two distinct real roots
                root1 = (-b_val + math.sqrt(disc)) / (2 * a_val)
                root2 = (-b_val - math.sqrt(disc)) / (2 * a_val)
                if plane.x_range[0] <= root1 <= plane.x_range[1]:
                    new_dots_group.add(Dot(plane.coords_to_point(root1, 0), color=GOLD_ACCENT, radius=0.15))
                if plane.x_range[0] <= root2 <= plane.x_range[1]:
                    new_dots_group.add(Dot(plane.coords_to_point(root2, 0), color=GOLD_ACCENT, radius=0.15))
            elif disc == 0: # One real root
                root = -b_val / (2 * a_val)
                if plane.x_range[0] <= root <= plane.x_range[1]:
                    new_dots_group.add(Dot(plane.coords_to_point(root, 0), color=GOLD_ACCENT, radius=0.15))
            return new_dots_group

        animated_root_dots = always_redraw(get_root_dots)

        self.play(
            Create(parabola),
            Write(equation_text),
            FadeIn(animated_root_dots)
        )
        self.wait(0.5)

        self.play(c_tracker.animate.set_value(1), run_time=2.5) # One root
        self.play(c_tracker.animate.set_value(2.5), run_time=2.5) # No roots
        self.play(c_tracker.animate.set_value(-2), run_time=2.5) # Two roots again
        self.wait(1)

        # --- Beat 2: Standard Form and Geometric Meaning ---
        self.remove(animated_root_dots) # Stop redrawing dynamic dots
        self.play(FadeOut(equation_text, shift=UP)) # Fade out the dynamic equation
        
        # Set to a fixed parabola with two roots for explanation
        c_tracker.set_value(-1) # For x^2 - 2x - 1 = 0, discriminant 4 - 4(-1) = 8 > 0
        current_parabola = parabola.copy() # Make a static copy
        
        # Roots for current_parabola (x^2 - 2x - 1 = 0)
        root1_val = (-b_val + math.sqrt(b_val**2 - 4*a_val*c_tracker.get_value())) / (2 * a_val)
        root2_val = (-b_val - math.sqrt(b_val**2 - 4*a_val*c_tracker.get_value())) / (2 * a_val)
        
        root_dot1 = Dot(plane.coords_to_point(root1_val, 0), color=GOLD_ACCENT, radius=0.15)
        root_dot2 = Dot(plane.coords_to_point(root2_val, 0), color=GOLD_ACCENT, radius=0.15)
        
        # Formal quadratic equation text
        quad_equation = Text(
            "ax^2 + bx + c = 0",
            color=WHITE, font_size=40
        ).to_corner(UP + LEFT)
        
        geometric_meaning_text = Text(
            "Where does the parabola", color=GREY_TEXT, font_size=28
        ).next_to(quad_equation, DOWN, buff=0.5, aligned_edge=LEFT)
        geometric_meaning_text2 = Text(
            "cross the x-axis?", color=GREY_TEXT, font_size=28
        ).next_to(geometric_meaning_text, DOWN, buff=0.1, aligned_edge=LEFT)

        self.play(
            FadeOut(parabola), # Remove the always_redraw object
            FadeIn(current_parabola), # Introduce the static parabola
            Write(quad_equation),
            LaggedStart(
                Write(geometric_meaning_text),
                Write(geometric_meaning_text2),
                lag_ratio=0.5
            ),
            Create(root_dot1),
            Create(root_dot2)
        )
        self.wait(2)

        # Arrow linking equation to roots
        arrow1 = Arrow(
            quad_equation.get_bottom(),
            plane.coords_to_point(0, 0), # Pointing generally towards the roots area
            buff=0.5,
            color=GOLD_ACCENT
        )
        self.play(GrowArrow(arrow1))
        self.wait(1)
        self.play(FadeOut(arrow1))

        # --- Beat 3: Exploring Root Cases (2, 1, 0) in detail ---
        self.play(
            FadeOut(geometric_meaning_text),
            FadeOut(geometric_meaning_text2),
            FadeOut(quad_equation)
        )
        
        # Initial state: 2 roots
        c_val_2_roots = -1
        parabola_2_roots_obj = plane.get_graph(
            lambda x: a_val * x**2 + b_val * x + c_val_2_roots,
            x_range=[-4, 4],
            color=BLUE_ACCENT
        ).set_stroke(width=5)
        
        root1_2r_val = (-b_val + math.sqrt(b_val**2 - 4*a_val*c_val_2_roots)) / (2 * a_val)
        root2_2r_val = (-b_val - math.sqrt(b_val**2 - 4*a_val*c_val_2_roots)) / (2 * a_val)
        
        dot1_2r = Dot(plane.coords_to_point(root1_2r_val, 0), color=GOLD_ACCENT, radius=0.15)
        dot2_2r = Dot(plane.coords_to_point(root2_2r_val, 0), color=GOLD_ACCENT, radius=0.15)
        
        label_2_roots = Text("Two Real Roots", color=WHITE, font_size=36).to_corner(UP + LEFT)
        
        self.play(
            ReplacementTransform(current_parabola, parabola_2_roots_obj),
            ReplacementTransform(root_dot1, dot1_2r),
            ReplacementTransform(root_dot2, dot2_2r),
            Write(label_2_roots)
        )
        self.wait(1.5)

        # Case: One Real Root
        c_val_1_root = 1 
        parabola_1_root_obj = plane.get_graph(
            lambda x: a_val * x**2 + b_val * x + c_val_1_root,
            x_range=[-4, 4],
            color=BLUE_ACCENT
        ).set_stroke(width=5)
        
        root_1r_val = -b_val / (2 * a_val) # For discriminant = 0
        dot_1r = Dot(plane.coords_to_point(root_1r_val, 0), color=GOLD_ACCENT, radius=0.15)
        
        label_1_root = Text("One Real Root", color=WHITE, font_size=36).to_corner(UP + LEFT)
        
        self.play(
            Transform(parabola_2_roots_obj, parabola_1_root_obj),
            FadeOut(dot1_2r, target_position=dot_1r.get_center()),
            FadeOut(dot2_2r, target_position=dot_1r.get_center()),
            FadeIn(dot_1r),
            ReplacementTransform(label_2_roots, label_1_root)
        )
        self.wait(1.5)

        # Case: No Real Roots
        c_val_0_roots = 2.5
        parabola_0_roots_obj = plane.get_graph(
            lambda x: a_val * x**2 + b_val * x + c_val_0_roots,
            x_range=[-4, 4],
            color=BLUE_ACCENT
        ).set_stroke(width=5)
        
        label_0_roots = Text("No Real Roots", color=WHITE, font_size=36).to_corner(UP + LEFT)
        
        self.play(
            Transform(parabola_2_roots_obj, parabola_0_roots_obj),
            FadeOut(dot_1r),
            ReplacementTransform(label_1_root, label_0_roots)
        )
        self.wait(1.5)

        # --- Beat 4: Introducing the Discriminant ---
        self.play(
            FadeOut(parabola_2_roots_obj),
            FadeOut(label_0_roots),
            FadeOut(plane),
            FadeOut(x_axis_label),
            FadeOut(y_axis_label)
        )
        
        # General equation
        general_eq = Text("ax^2 + bx + c = 0", color=WHITE, font_size=50).move_to(ORIGIN + UP * 2)
        
        discriminant_intro = Text("The Discriminant", color=GOLD_ACCENT, font_size=50).next_to(general_eq, DOWN, buff=1)
        
        discriminant_expr = Text(
            "D = b^2 - 4ac",
            color=BLUE_ACCENT, font_size=60
        ).next_to(discriminant_intro, DOWN, buff=0.5)

        self.play(Write(general_eq))
        self.wait(1)
        self.play(Write(discriminant_intro))
        self.play(Write(discriminant_expr))
        self.wait(1.5)

        # Reintroduce the plane for context with discriminant cases
        self.play(
            FadeIn(plane),
            FadeIn(x_axis_label),
            FadeIn(y_axis_label),
            FadeOut(general_eq, shift=LEFT),
            FadeOut(discriminant_intro, shift=LEFT)
        )
        self.wait(0.5)

        # Display discriminant conditions and corresponding parabolas
        # Case 1: D > 0 (Two Real Roots)
        parabola_2_roots_obj = plane.get_graph(
            lambda x: a_val * x**2 + b_val * x + c_val_2_roots,
            x_range=[-4, 4],
            color=BLUE_ACCENT
        ).set_stroke(width=5)
        
        dot1_2r = Dot(plane.coords_to_point(root1_2r_val, 0), color=GOLD_ACCENT, radius=0.15)
        dot2_2r = Dot(plane.coords_to_point(root2_2r_val, 0), color=GOLD_ACCENT, radius=0.15)

        disc_cond_gt_0 = Text("D > 0", color=GOLD_ACCENT, font_size=48).to_corner(UP + LEFT)
        roots_count_gt_0 = Text("Two Real Roots", color=WHITE, font_size=36).next_to(disc_cond_gt_0, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(
            Transform(discriminant_expr, disc_cond_gt_0), 
            Create(parabola_2_roots_obj),
            Create(dot1_2r),
            Create(dot2_2r),
            Write(roots_count_gt_0)
        )
        self.wait(2)

        # Case 2: D = 0 (One Real Root)
        parabola_1_root_obj = plane.get_graph(
            lambda x: a_val * x**2 + b_val * x + c_val_1_root,
            x_range=[-4, 4],
            color=BLUE_ACCENT
        ).set_stroke(width=5)
        
        dot_1r = Dot(plane.coords_to_point(root_1r_val, 0), color=GOLD_ACCENT, radius=0.15)
        
        disc_cond_eq_0 = Text("D = 0", color=GOLD_ACCENT, font_size=48).to_corner(UP + LEFT)
        roots_count_eq_0 = Text("One Real Root", color=WHITE, font_size=36).next_to(disc_cond_eq_0, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(
            Transform(parabola_2_roots_obj, parabola_1_root_obj),
            FadeOut(dot1_2r, target_position=dot_1r.get_center()),
            FadeOut(dot2_2r, target_position=dot_1r.get_center()),
            FadeIn(dot_1r),
            ReplacementTransform(disc_cond_gt_0, disc_cond_eq_0),
            ReplacementTransform(roots_count_gt_0, roots_count_eq_0)
        )
        self.wait(2)

        # Case 3: D < 0 (No Real Roots)
        parabola_0_roots_obj = plane.get_graph(
            lambda x: a_val * x**2 + b_val * x + c_val_0_roots,
            x_range=[-4, 4],
            color=BLUE_ACCENT
        ).set_stroke(width=5)
        
        disc_cond_lt_0 = Text("D < 0", color=GOLD_ACCENT, font_size=48).to_corner(UP + LEFT)
        roots_count_lt_0 = Text("No Real Roots", color=WHITE, font_size=36).next_to(disc_cond_lt_0, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(
            Transform(parabola_2_roots_obj, parabola_0_roots_obj),
            FadeOut(dot_1r),
            ReplacementTransform(disc_cond_eq_0, disc_cond_lt_0),
            ReplacementTransform(roots_count_eq_0, roots_count_lt_0)
        )
        self.wait(2)

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(parabola_2_roots_obj),
            FadeOut(disc_cond_lt_0),
            FadeOut(roots_count_lt_0),
            FadeOut(plane),
            FadeOut(x_axis_label),
            FadeOut(y_axis_label)
        )

        recap_title = Text("Recap: The Discriminant", color=GOLD_ACCENT, font_size=60).to_edge(UP, buff=1)
        
        recap_d_formula = Text("D = b^2 - 4ac", color=BLUE_ACCENT, font_size=48).next_to(recap_title, DOWN, buff=1)
        
        recap_case_gt = Text("D > 0 : Two Real Roots", color=WHITE, font_size=40).next_to(recap_d_formula, DOWN, buff=0.7, aligned_edge=LEFT)
        recap_case_eq = Text("D = 0 : One Real Root", color=WHITE, font_size=40).next_to(recap_case_gt, DOWN, buff=0.4, aligned_edge=LEFT)
        recap_case_lt = Text("D < 0 : No Real Roots", color=WHITE, font_size=40).next_to(recap_case_eq, DOWN, buff=0.4, aligned_edge=LEFT)

        recap_group = VGroup(recap_title, recap_d_formula, recap_case_gt, recap_case_eq, recap_case_lt).center()
        
        self.play(
            LaggedStart(
                Write(recap_title),
                Write(recap_d_formula),
                Write(recap_case_gt),
                Write(recap_case_eq),
                Write(recap_case_lt),
                lag_ratio=0.5,
                run_time=4
            )
        )
        self.wait(3)
        self.play(FadeOut(recap_group))
        self.wait(1)