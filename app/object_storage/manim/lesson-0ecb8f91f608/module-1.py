from manim import *

class QuadraticGeneralForm(Scene):
    def construct(self):
        # Configuration
        config.background_color = BLACK

        # Initialize plane early for the hook and subsequent graph plotting
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": GRAY, "stroke_width": 1},
            background_line_style={"stroke_color": GRAY_A, "stroke_opacity": 0.3}
        ).add_coordinates()

        # --- Beat 1: The Parabola - Our Star ---
        self.camera.background_color = BLACK # Ensures the background is black for this scene.

        # Visual Hook: A dynamic line bending into a parabola
        initial_line = Line(plane.c2p(-3, -3), plane.c2p(3, -3), color=BLUE)
        hook_parabola_target = plane.get_graph(lambda x: 0.5 * x**2 - 2, x_range=[-3, 3], color=BLUE)
        
        self.play(Create(initial_line, run_time=1.5, rate_func=smooth))
        self.play(Transform(initial_line, hook_parabola_target, run_time=1.5, rate_func=wiggle))
        self.wait(0.5)

        title = Text("Quadratic Equations", font_size=50, color=GOLD).to_edge(UP)
        subtitle = Text("General Form & Graphing Intuition", font_size=30, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)

        # Introduce NumberPlane and Axes
        axes_label_x = Text("x", color=GRAY_B, font_size=20).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1)
        axes_label_y = Text("y", color=GRAY_B, font_size=20).next_to(plane.y_axis.get_end(), UP, buff=0.1)
        axes = VGroup(plane, axes_label_x, axes_label_y)

        self.play(
            FadeOut(initial_line), # hook_parabola_target is gone since initial_line transformed into it
            FadeOut(title),
            FadeOut(subtitle),
            LaggedStart(
                Create(plane),
                Create(axes_label_x),
                Create(axes_label_y),
                lag_ratio=0.5,
                run_time=2
            )
        )
        self.wait(0.5)

        # The baseline parabola y = x^2
        current_parabola = plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=BLUE)
        equation_y_x_squared = self.create_equation_mobject("y", "=", "x", "2").to_corner(UL)
        self.play(Create(current_parabola), Write(equation_y_x_squared))
        self.wait(1)

        # --- Beat 2: The `a` Factor - Shape Shifter ---
        self.next_section("a_factor")
        a_text_label = Text("a:", color=GOLD).next_to(equation_y_x_squared, DOWN, buff=0.5).align_to(equation_y_x_squared, LEFT)
        a_effect_text = Text("Stretch, Compress, Flip!", font_size=25, color=BLUE).next_to(a_text_label, RIGHT)
        self.play(Write(a_text_label), Write(a_effect_text))
        self.wait(0.5)

        # Transform to y = ax^2
        # Explicitly show '1' as 'a' first
        current_eq_x_squared_parts = self.create_equation_mobject("y", "=", "1", "x", "2").move_to(equation_y_x_squared.get_center())
        self.play(ReplacementTransform(equation_y_x_squared, current_eq_x_squared_parts)) # y = x^2 -> y = 1x^2
        self.wait(0.5)

        a_var_mobject = current_eq_x_squared_parts[2] # This is the '1'
        
        a_values_to_show = [2, 0.5, -1, -2, 1] # End with 1
        for val in a_values_to_show:
            new_parabola = plane.get_graph(lambda x: val * x**2, x_range=[-3, 3], color=BLUE)
            new_a_var_text = Text(str(val), color=GOLD, font_size=30).move_to(a_var_mobject.get_center())
            self.play(
                Transform(current_parabola, new_parabola),
                Transform(a_var_mobject, new_a_var_text),
                run_time=0.8
            )
            self.wait(0.3)
        
        # Replace '1' with 'a' symbol
        equation_y_ax_squared = self.create_equation_mobject("y", "=", "a", "x", "2").move_to(current_eq_x_squared_parts.get_center())
        self.play(ReplacementTransform(current_eq_x_squared_parts, equation_y_ax_squared))
        self.wait(0.5)

        self.play(FadeOut(a_text_label, a_effect_text))

        # --- Beat 3: The `c` Factor - Vertical Mover ---
        self.next_section("c_factor")
        c_text_label = Text("c:", color=GOLD).align_to(equation_y_ax_squared, LEFT).shift(DOWN*0.5)
        c_effect_text = Text("Vertical Shift", font_size=25, color=BLUE).next_to(c_text_label, RIGHT)
        self.play(Write(c_text_label), Write(c_effect_text))
        self.wait(0.5)

        # Add +c to the equation
        plus_c_mobj_group = self.create_equation_mobject("+", "c").next_to(equation_y_ax_squared, RIGHT, buff=0.2)
        
        self.play(FadeIn(plus_c_mobj_group, shift=RIGHT))
        self.wait(0.5)

        c_val_mobj = plus_c_mobj_group[1] # This is the 'c' in (+c)
        c_plus_mobj = plus_c_mobj_group[0] # This is the '+' in (+c)

        # Add an arrow for vertical shift
        c_arrow = Arrow(start=plane.c2p(0, -1), end=plane.c2p(0, 1), buff=0, color=GOLD, stroke_width=7).set_opacity(0) # Start invisible
        self.add(c_arrow)

        c_values_to_show = [2, -2, 0] # End with 0 for next beat
        for val in c_values_to_show:
            new_parabola = plane.get_graph(lambda x: x**2 + val, x_range=[-3, 3], color=BLUE) # Keeping a=1 for simplicity
            new_c_val_text = Text(str(abs(val)), color=GOLD, font_size=30).move_to(c_val_mobj.get_center())
            new_c_plus_text = Text("+" if val >= 0 else "-", color=GOLD, font_size=30).move_to(c_plus_mobj.get_center())
            if val == 0:
                new_c_val_text = Text("", color=GOLD, font_size=30).move_to(c_val_mobj.get_center()) # Hide '0'
                new_c_plus_text = Text("", color=GOLD, font_size=30).move_to(c_plus_mobj.get_center()) # Hide '+'
                arrow_target = c_arrow.copy().set_opacity(0)
            else:
                arrow_target = Arrow(start=plane.c2p(0, 0), end=plane.c2p(0, val * 2), buff=0, color=GOLD, stroke_width=7).set_opacity(1) # Scale arrow for visibility

            self.play(
                Transform(current_parabola, new_parabola),
                Transform(c_val_mobj, new_c_val_text),
                Transform(c_plus_mobj, new_c_plus_text),
                Transform(c_arrow, arrow_target), # Animate arrow movement
                run_time=0.8
            )
            self.wait(0.3)
        
        # Fade out +c numerical value
        self.play(FadeOut(plus_c_mobj_group), FadeOut(c_arrow))
        self.play(FadeOut(c_text_label, c_effect_text))


        # --- Beat 4: The `b` Factor - Horizontal Shifter & Vertex Mover ---
        self.next_section("b_factor")
        b_text_label = Text("b:", color=GOLD).align_to(equation_y_ax_squared, LEFT).shift(DOWN*0.5)
        b_effect_text = Text("Vertex Horizontal Shift", font_size=25, color=BLUE).next_to(b_text_label, RIGHT)
        self.play(Write(b_text_label), Write(b_effect_text))
        self.wait(0.5)

        # Add +bx and +c to the equation. Shift ax^2, then add.
        # Starting with y=ax^2. 'a' is currently a placeholder text.
        
        # Construct the full equation for transformation
        # y = ax^2 + bx + c
        # Reuse existing equation_y_ax_squared for y=ax^2 part
        
        # Individual parts of +bx
        plus_b_text = Text("+", color=GOLD, font_size=30)
        b_text_var = Text("b", color=GOLD, font_size=30)
        x_text_var_for_b = Text("x", color=GOLD, font_size=30)
        
        # Individual parts of +c
        plus_c_text = Text("+", color=GOLD, font_size=30)
        c_text_var = Text("c", color=GOLD, font_size=30)

        # Arrange them
        current_eq_ax2_end = equation_y_ax_squared[-1].get_right()[0] # Get right edge of '2' in x^2
        
        plus_b_text.move_to(current_eq_ax2_end + 0.2 + plus_b_text.get_width()/2 * RIGHT)
        b_text_var.next_to(plus_b_text, RIGHT, buff=0.1)
        x_text_var_for_b.next_to(b_text_var, RIGHT, buff=0.05)
        
        plus_c_text.next_to(x_text_var_for_b, RIGHT, buff=0.2)
        c_text_var.next_to(plus_c_text, RIGHT, buff=0.1)

        added_bx_c = VGroup(plus_b_text, b_text_var, x_text_var_for_b, plus_c_text, c_text_var)
        # Combine existing equation_y_ax_squared with new parts
        full_equation_parts_combined = VGroup(equation_y_ax_squared, added_bx_c).to_corner(UL)
        
        self.play(
            FadeIn(added_bx_c, shift=RIGHT),
            full_equation_parts_combined.animate.to_corner(UL), # Keep it in place
            run_time=1.5
        )
        self.wait(0.5)

        # Animate changing 'b' (keeping a=1, c=0 for the parabola demo)
        self.play(
            Transform(current_parabola, plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=BLUE)) # Reset parabola
        )
        
        # Target the numerical b in the equation parts
        b_val_mobj = b_text_var
        b_plus_mobj = plus_b_text
        x_in_bx_mobj = x_text_var_for_b

        # Add an arrow for horizontal shift
        b_arrow = Arrow(start=plane.c2p(-1, 0), end=plane.c2p(1, 0), buff=0, color=GOLD, stroke_width=7).set_opacity(0)
        self.add(b_arrow)

        # Animate changing 'b' on parabola
        b_values_to_show = [-2, 2, 0]
        for val in b_values_to_show:
            new_parabola = plane.get_graph(lambda x: x**2 + val * x, x_range=[-4, 4], color=BLUE) # a=1, c=0
            
            new_b_val_text = Text(str(abs(val)), color=GOLD, font_size=30).move_to(b_val_mobj.get_center())
            new_b_plus_text = Text("+" if val >= 0 else "-", color=GOLD, font_size=30).move_to(b_plus_mobj.get_center())
            
            # Special handling for b=0: Hide bx term entirely
            if val == 0:
                new_b_val_text.set_opacity(0)
                new_b_plus_text.set_opacity(0)
                x_in_bx_mobj_target = Text("x", color=GOLD, font_size=30).move_to(x_in_bx_mobj.get_center()).set_opacity(0)
                arrow_target = b_arrow.copy().set_opacity(0)
            else:
                x_in_bx_mobj_target = Text("x", color=GOLD, font_size=30).move_to(x_in_bx_mobj.get_center())
                # Vertex for y=x^2+bx is at x = -b/2a. With a=1, it's at x = -b/2.
                # Arrow points from origin to the vertex's x-coordinate.
                arrow_target = Arrow(start=plane.c2p(0, 0), end=plane.c2p(-val/2 * 2, 0), buff=0, color=GOLD, stroke_width=7).set_opacity(1) # Scale factor of 2 for visibility
            
            self.play(
                Transform(current_parabola, new_parabola),
                Transform(b_val_mobj, new_b_val_text),
                Transform(b_plus_mobj, new_b_plus_text),
                Transform(x_in_bx_mobj, x_in_bx_mobj_target),
                Transform(b_arrow, arrow_target),
                run_time=1
            )
            self.wait(0.3)
        
        # Clean up b animation elements and the general form equation
        self.play(
            FadeOut(full_equation_parts_combined, b_text_label, b_effect_text),
            FadeOut(b_val_mobj, b_plus_mobj, x_in_bx_mobj, b_arrow) # Ensure individual numeric elements are gone
        )
        self.play(Transform(current_parabola, plane.get_graph(lambda x: x**2, x_range=[-3, 3], color=BLUE))) # Reset parabola
        self.wait(0.5)


        # --- Beat 5: Roots and the General Form ---
        self.next_section("roots_general_form")
        
        general_form_title = Text("General Form", color=GOLD, font_size=35).to_corner(UL).shift(UP*0.5)
        roots_title = Text("Roots: Where y = 0", color=BLUE, font_size=30).next_to(general_form_title, DOWN, buff=0.5).align_to(general_form_title, LEFT)
        
        # Construct the full general form equation: ax^2 + bx + c = 0
        eq_ax2 = self.create_equation_mobject("a", "x", "2")
        eq_bx = self.create_equation_mobject("+", "b", "x")
        eq_c = self.create_equation_mobject("+", "c")
        eq_equals_zero = self.create_equation_mobject("=", "0", color_equals=GOLD, color_zero=BLUE) # Blue for 0 to match concept

        eq_bx.next_to(eq_ax2, RIGHT, buff=0.2)
        eq_c.next_to(eq_bx, RIGHT, buff=0.2)
        eq_equals_zero.next_to(eq_c, RIGHT, buff=0.2)
        
        general_form_eq_group = VGroup(eq_ax2, eq_bx, eq_c, eq_equals_zero).to_corner(UL)

        self.play(
            Write(general_form_title),
            Create(general_form_eq_group, run_time=2)
        )
        self.play(Write(roots_title))
        self.wait(1)

        # Show a parabola crossing x-axis
        parabola_roots = plane.get_graph(lambda x: x**2 - 4, x_range=[-3, 3], color=BLUE) # roots at -2, 2
        root1_dot = Dot(plane.c2p(-2, 0), color=GOLD)
        root2_dot = Dot(plane.c2p(2, 0), color=GOLD)

        root1_label = Text("-2", color=GOLD, font_size=25).next_to(root1_dot, DOWN)
        root2_label = Text("2", color=GOLD, font_size=25).next_to(root2_dot, DOWN)

        self.play(
            Transform(current_parabola, parabola_roots),
            Create(root1_dot),
            Create(root2_dot),
            Write(root1_label),
            Write(root2_label),
            run_time=2
        )
        self.wait(1)

        # Animate parabola shifting to show different roots
        parabola_shift_1 = plane.get_graph(lambda x: x**2 - 2*x - 3, x_range=[-2.5, 4.5], color=BLUE) # roots at -1, 3
        new_root1_dot = Dot(plane.c2p(-1, 0), color=GOLD)
        new_root2_dot = Dot(plane.c2p(3, 0), color=GOLD)
        new_label1 = Text("-1", color=GOLD, font_size=25).next_to(new_root1_dot, DOWN)
        new_label2 = Text("3", color=GOLD, font_size=25).next_to(new_root2_dot, DOWN)

        self.play(
            Transform(current_parabola, parabola_shift_1),
            Transform(root1_dot, new_root1_dot),
            Transform(root2_dot, new_root2_dot),
            Transform(root1_label, new_label1),
            Transform(root2_label, new_label2),
            run_time=1.5
        )
        self.wait(1)

        parabola_shift_2 = plane.get_graph(lambda x: x**2 + x - 2, x_range=[-3, 2.5], color=BLUE) # roots at -2, 1
        new_root1_dot = Dot(plane.c2p(-2, 0), color=GOLD)
        new_root2_dot = Dot(plane.c2p(1, 0), color=GOLD)
        new_label1 = Text("-2", color=GOLD, font_size=25).next_to(new_root1_dot, DOWN)
        new_label2 = Text("1", color=GOLD, font_size=25).next_to(new_root2_dot, DOWN)

        self.play(
            Transform(current_parabola, parabola_shift_2),
            Transform(root1_dot, new_root1_dot),
            Transform(root2_dot, new_root2_dot),
            Transform(root1_label, new_label1),
            Transform(root2_label, new_label2),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            FadeOut(current_parabola),
            FadeOut(root1_dot, root2_dot, root1_label, root2_label),
            FadeOut(general_form_eq_group),
            FadeOut(general_form_title),
            FadeOut(roots_title),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Recap Card ---
        self.next_section("recap")
        recap_title = Text("Recap: Quadratic Intuition", color=GOLD, font_size=40).to_edge(UP)

        bullet_a = Text("a: Stretches, Compresses, Flips shape", font_size=28, color=BLUE).next_to(recap_title, DOWN, buff=0.8).align_to(recap_title, LEFT).shift(RIGHT*0.5)
        bullet_c = Text("c: Vertical position shift", font_size=28, color=BLUE).next_to(bullet_a, DOWN, buff=0.4).align_to(bullet_a, LEFT)
        bullet_b = Text("b: Horizontal vertex shift", font_size=28, color=BLUE).next_to(bullet_c, DOWN, buff=0.4).align_to(bullet_c, LEFT)
        bullet_roots = Text("Roots: x-values where ax^2 + bx + c = 0", font_size=28, color=BLUE).next_to(bullet_b, DOWN, buff=0.4).align_to(bullet_b, LEFT)

        recap_elements = VGroup(recap_title, bullet_a, bullet_c, bullet_b, bullet_roots)

        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(bullet) for bullet in [bullet_a, bullet_c, bullet_b, bullet_roots]], lag_ratio=0.7, run_time=5))
        self.wait(3)

        self.play(FadeOut(recap_elements, plane, axes_label_x, axes_label_y))
        self.wait(1)
    
    # Helper function to create equation Mobjects from individual Text elements
    def create_equation_mobject(self, *parts, color_equals=GOLD, color_zero=BLUE):
        mobjects = []
        for i, part_str in enumerate(parts):
            if part_str == "2": # For exponents
                mobj = Text(part_str, color=GOLD, font_size=20)
            elif part_str == "=":
                mobj = Text(part_str, color=color_equals, font_size=30)
            elif part_str == "0" and "=" in parts: # Custom color for 0 if part of an " = 0" expression
                mobj = Text(part_str, color=color_zero, font_size=30)
            elif part_str in ["+", "-"]:
                mobj = Text(part_str, color=GOLD, font_size=30)
            else:
                mobj = Text(part_str, color=GOLD, font_size=30)
            mobjects.append(mobj)
        
        # Manually arrange elements
        if not mobjects:
            return VGroup()

        # Place the first Mobject at ORIGIN for relative positioning later
        if mobjects:
            mobjects[0].move_to(ORIGIN)

        # Handle explicit '2' as exponent by positioning it relative to 'x' *before* arranging the rest.
        # This assumes 'x' always comes immediately before '2' if '2' is an exponent.
        for i in range(len(mobjects) - 1):
            if parts[i+1] == "2" and parts[i] == "x":
                mobjects[i+1].move_to(mobjects[i].get_center() + 0.1 * UP + mobjects[i].get_width()/2 * RIGHT).scale(0.7)
        
        # Arrange the rest of the elements, respecting exponent positions
        for i in range(1, len(mobjects)):
            # If the current element is an exponent, it's already positioned correctly
            # relative to its base. Do not use next_to for it again.
            if parts[i] == "2" and parts[i-1] == "x":
                pass 
            else:
                mobjects[i].next_to(mobjects[i-1], RIGHT, buff=0.1)
        
        return VGroup(*mobjects)