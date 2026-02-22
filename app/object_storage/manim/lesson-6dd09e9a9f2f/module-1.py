from manim import *
import numpy as np

class CellStructureAndFunction(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        blue_main = BLUE_E
        gold_main = GOLD_E
        blue_light = BLUE_A
        gold_light = GOLD_A

        # Helper for random vector offset
        def random_vector(scale):
            return np.array([np.random.uniform(-scale, scale), np.random.uniform(-scale, scale), 0])

        # --- Beat 1: Visual Hook & Introduction ---
        # Abstract building blocks forming life
        elements = VGroup()
        for _ in range(30):
            shape_type = np.random.choice([Circle, Square, Triangle])
            shape = shape_type(radius=0.1 + np.random.rand() * 0.05,
                               fill_opacity=0.7,
                               color=np.random.choice([blue_light, gold_light]), # Use defined palette
                               stroke_width=0)
            shape.move_to(self.camera.frame.get_random_point())
            elements.add(shape)

        self.play(LaggedStart(*[FadeIn(s, shift=UP * np.random.rand() * 0.5) for s in elements]), run_time=2)

        # Gather them into a more organized, central cluster
        target_center = ORIGIN + UP * 0.5
        organized_elements = VGroup(*[s.copy().move_to(target_center + random_vector(0.8)) for s in elements])

        self.play(
            Transform(elements, organized_elements),
            run_time=1.5,
            rate_func=CUBIC_BEZIER(0.5, 0.0, 0.5, 1.0) # More organic clustering
        )

        # Introduce the title
        title = MathTex(
            "\\text{The Cell}",
            "\\text{:", " \\text{Smallest Unit of Life}"
        ).to_edge(UP).set_color_by_tex_to_color_map({
            "\\text{The Cell}": gold_main,
            "\\text{Smallest Unit of Life}": blue_main
        }).scale(1.2)

        self.play(
            FadeIn(title),
            elements.animate.scale(0.5).to_edge(DOWN + LEFT), # Move elements aside
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 2: Basic Cell Structure ---
        self.play(FadeOut(elements), run_time=0.5)
        cell_outline_large = Ellipse(width=5, height=3.5, color=gold_main, stroke_width=4)
        cytoplasm_fill = Ellipse(width=4.8, height=3.3, color=blue_light, fill_opacity=0.6, stroke_width=0)
        nucleus_outline = Circle(radius=0.7, color=gold_light, stroke_width=3, fill_opacity=0.7, fill_color=BLUE_A)

        # Animate the cell forming
        self.play(
            Create(cell_outline_large),
            title.animate.scale(0.8).next_to(cell_outline_large, UP, buff=0.7),
            run_time=1
        )
        self.play(
            FadeIn(cytoplasm_fill, scale=0.8),
            run_time=0.7
        )
        self.play(
            FadeIn(nucleus_outline, scale=0.5),
            run_time=0.7
        )

        # Labels for components
        membrane_label = MathTex("\\text{Cell Membrane}").next_to(cell_outline_large, RIGHT, buff=0.3).set_color(gold_main)
        cytoplasm_label = MathTex("\\text{Cytoplasm}").next_to(cytoplasm_fill, DOWN, buff=0.3).set_color(blue_main)
        nucleus_label = MathTex("\\text{Nucleus}").next_to(nucleus_outline, LEFT, buff=0.3).set_color(gold_light)

        membrane_arrow = Arrow(membrane_label.get_left(), cell_outline_large.get_right(), buff=0.1, color=gold_main)
        cytoplasm_arrow = Arrow(cytoplasm_label.get_top(), cytoplasm_fill.get_bottom(), buff=0.1, color=blue_main)
        nucleus_arrow = Arrow(nucleus_label.get_right(), nucleus_outline.get_left(), buff=0.1, color=gold_light)

        self.play(
            LaggedStart(
                GrowArrow(membrane_arrow), FadeIn(membrane_label, shift=LEFT),
                GrowArrow(cytoplasm_arrow), FadeIn(cytoplasm_label, shift=UP),
                GrowArrow(nucleus_arrow), FadeIn(nucleus_label, shift=RIGHT),
                lag_ratio=0.3,
                run_time=2
            )
        )
        self.wait(1)

        cell_components = VGroup(cell_outline_large, cytoplasm_fill, nucleus_outline,
                                 membrane_label, cytoplasm_label, nucleus_label,
                                 membrane_arrow, cytoplasm_arrow, nucleus_arrow)

        # --- Beat 3: Cell Function (Energy & Information Exchange) ---
        self.play(
            cell_components.animate.shift(LEFT*2.5).scale(0.8),
            FadeOut(title), # Fade out original title as new title appears
            run_time=1
        )

        # Create a combined Mobject for easier manipulation of the cell itself
        cell_mobject = VGroup(cell_outline_large, cytoplasm_fill, nucleus_outline)
        # We moved the original cell_components, so its internal Mobjects are already in place
        # No need to copy/shift again here for cell_mobject, just group the transformed components.

        function_title = MathTex("\\text{Function:}", "\\text{ Exchange \& Activity}").to_edge(UP).set_color_by_tex_to_color_map({
            "\\text{Function:}": gold_main,
            "\\text{Exchange \& Activity}": blue_main
        }).scale(1.1)
        self.play(FadeIn(function_title, shift=UP), run_time=0.8)

        # Inputs
        input_label = MathTex("\\text{Inputs}").set_color(blue_light).next_to(cell_mobject, LEFT, buff=1.5)
        input_arrow = Arrow(input_label.get_right(), cell_mobject.get_left(), buff=0.1, color=blue_light)
        input_dots = VGroup(*[Dot(radius=0.08, color=blue_light).shift(input_label.get_right() + LEFT*0.5 + UP*(np.random.rand()-0.5)*0.5) for _ in range(3)])

        self.play(
            FadeIn(input_label), GrowArrow(input_arrow),
            LaggedStart(*[FadeIn(d, shift=LEFT*0.5) for d in input_dots]),
            run_time=1.5
        )

        # Internal activity - pulsing nucleus and cytoplasm
        self.play(
            cell_mobject[1].animate.set_color(BLUE_D).set_stroke(color=BLUE_E, width=2).scale(1.02), # Cytoplasm (index 1)
            cell_mobject[2].animate.set_color(GOLD_D).set_stroke(color=GOLD_E, width=2).scale(1.05), # Nucleus (index 2)
            run_time=0.5,
            rate_func=there_and_back_with_pause
        )
        self.play(
            cell_mobject[1].animate.set_color(blue_light).set_stroke(color=gold_main, width=0).scale(1/1.02),
            cell_mobject[2].animate.set_color(BLUE_A).set_stroke(color=gold_light, width=0).scale(1/1.05),
            run_time=0.5,
            rate_func=there_and_back_with_pause
        )

        # Outputs
        output_label = MathTex("\\text{Outputs}").set_color(gold_light).next_to(cell_mobject, RIGHT, buff=1.5)
        output_arrow = Arrow(cell_mobject.get_right(), output_label.get_left(), buff=0.1, color=gold_light)
        output_dots = VGroup(*[Dot(radius=0.08, color=gold_light).shift(output_label.get_left() + RIGHT*0.5 + UP*(np.random.rand()-0.5)*0.5) for _ in range(3)])

        self.play(
            FadeIn(output_label), GrowArrow(output_arrow),
            LaggedStart(*[FadeIn(d, shift=RIGHT*0.5) for d in output_dots]),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 4: Diversity & Organization ---
        self.play(
            FadeOut(VGroup(input_label, input_arrow, input_dots, output_label, output_arrow, output_dots, function_title)),
            cell_mobject.animate.scale(0.5).move_to(LEFT * 4 + UP),
            FadeOut(cell_components[3:]), # Fade out original labels/arrows from cell_components
            run_time=1
        )

        diversity_title = MathTex("\\text{Diversity}", "\\text{ & Organization}").to_edge(UP).set_color_by_tex_to_color_map({
            "\\text{Diversity}": gold_main,
            "\\text{ & Organization}": blue_main
        }).scale(1.1)
        self.play(FadeIn(diversity_title, shift=UP), run_time=0.8)

        # Create a grid of cells showing variety
        grid_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE_A, "stroke_width": 1},
            background_line_style={"stroke_color": BLUE_A, "stroke_opacity": 0.2}
        ).shift(DOWN*0.5)
        self.play(Create(grid_plane, run_time=1.5))

        # Replicate and vary the cell
        cells_on_grid = VGroup()
        
        # Define some basic cell forms and colors
        base_cell_components = [
            (Ellipse, {"width": 1.5, "height": 1, "color": gold_main, "stroke_width": 2}),
            (Ellipse, {"width": 1.4, "height": 0.9, "color": blue_light, "fill_opacity": 0.6, "stroke_width": 0}),
            (Circle, {"radius": 0.2, "color": gold_light, "fill_opacity": 0.7, "fill_color": BLUE_A})
        ]

        # Define some variations for the grid cells
        cell_types = [
            lambda: VGroup(
                base_cell_components[0][0](**base_cell_components[0][1]),
                base_cell_components[1][0](**base_cell_components[1][1]),
                base_cell_components[2][0](**base_cell_components[2][1])
            ).scale(np.random.uniform(0.8, 1.2)),
            lambda: VGroup(
                Polygon([(-0.7,0.5,0), (0.7,0.5,0), (0.8,-0.5,0), (-0.8,-0.5,0)], color=gold_main, stroke_width=2),
                Polygon([(-0.6,0.4,0), (0.6,0.4,0), (0.7,-0.4,0), (-0.7,-0.4,0)], color=blue_light, fill_opacity=0.6, stroke_width=0),
                Circle(radius=0.2, color=gold_light, fill_opacity=0.7, fill_color=BLUE_A)
            ).scale(np.random.uniform(0.8, 1.2)),
            lambda: VGroup(
                Circle(radius=0.7, color=gold_main, stroke_width=2),
                Circle(radius=0.65, color=blue_light, fill_opacity=0.6, stroke_width=0),
                Dot(radius=0.2, color=gold_light, fill_opacity=0.7, fill_color=BLUE_A)
            ).scale(np.random.uniform(0.8, 1.2)),
        ]

        # Place cells on grid, showing subtle organization and variation
        for i in range(-2, 3):
            for j in range(-2, 2):
                cell_variation = np.random.choice(cell_types)()
                cell_variation.move_to(grid_plane.c2p(i, j) + random_vector(0.3))
                cells_on_grid.add(cell_variation)

        self.play(
            LaggedStart(*[FadeIn(cell, scale=0.5) for cell in cells_on_grid], lag_ratio=0.05),
            run_time=2.5
        )
        self.wait(1)

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(diversity_title),
            FadeOut(grid_plane),
            FadeOut(cells_on_grid),
            FadeOut(cell_mobject),
            run_time=1
        )

        recap_title = MathTex("\\text{Recap}").to_edge(UP).set_color(gold_main).scale(1.2)
        recap_list = BulletedList(
            "Cells are the fundamental units of life.",
            "They possess basic structures: membrane, cytoplasm, nucleus.",
            "Cells constantly exchange energy and information.",
            "Life's diversity arises from various cell types, organized.",
            font_size=36,
            color=blue_main # Set default color for all items
        ).next_to(recap_title, DOWN, buff=0.8).align_left(LEFT_SIDE + RIGHT*1.5)

        self.play(
            FadeIn(recap_title, shift=UP),
            LaggedStart(*[FadeIn(item, shift=LEFT) for item in recap_list.items], lag_ratio=0.3),
            run_time=3
        )
        self.wait(3)