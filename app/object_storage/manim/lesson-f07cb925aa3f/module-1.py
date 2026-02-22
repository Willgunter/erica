from manim import *

class CellStructureAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = '#87CEEB'  # Lighter blue for accents
        GOLD_ACCENT = '#FFD700'  # Gold for highlights
        GREY_TEXT = '#A9A9A9'   # Darker grey for secondary text

        # --- Beat 1: The Fundamental Units (Visual Hook) ---
        title = MathTex("Cellular \\, Foundations", font_size=72, color=GOLD_ACCENT)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7))

        # Visual hook: A grid forming from a central point
        initial_dot = Dot(point=ORIGIN, radius=0.1, color=BLUE_ACCENT)
        self.play(GrowFromCenter(initial_dot))

        num_cells_x = 7
        num_cells_y = 5
        cell_size = 0.5
        grid_cells = VGroup()
        for i in range(num_cells_x):
            for j in range(num_cells_y):
                cell = Circle(radius=cell_size / 2, color=BLUE_ACCENT, fill_opacity=0.3, stroke_width=1)
                cell.move_to(RIGHT * (i - num_cells_x / 2 + 0.5) * cell_size * 1.5 + UP * (j - num_cells_y / 2 + 0.5) * cell_size * 1.5)
                grid_cells.add(cell)

        # Animate the grid forming, one cell growing from the center outward
        self.play(LaggedStart(*[GrowFromCenter(cell) for cell in grid_cells], lag_ratio=0.01), run_time=2)
        self.wait(0.5)

        # Introduce text: "Building Blocks of Life"
        building_blocks_text = MathTex("Fundamental \\, Units", color=GREY_TEXT, font_size=40).next_to(grid_cells, DOWN, buff=0.7)
        self.play(Write(building_blocks_text))
        self.wait(1)

        # --- Beat 2: Zooming into a Single Cell - The Encapsulated Unit ---
        # Select one cell to zoom into
        target_cell = grid_cells[len(grid_cells) // 2] # Middle cell
        
        # Prepare the "zoomed in" cell before the transform
        zoomed_membrane = Circle(radius=2, color=BLUE_ACCENT, stroke_width=4)
        zoomed_cytoplasm = Circle(radius=1.9, color=DARK_GREY, fill_opacity=0.5, stroke_opacity=0)

        membrane_label = MathTex("Cell \\, Membrane", color=BLUE_ACCENT, font_size=30).next_to(zoomed_membrane, RIGHT, buff=0.3)
        cytoplasm_label = MathTex("Cytoplasm", color=GREY_TEXT, font_size=30).next_to(zoomed_cytoplasm, DOWN, buff=0.3)

        membrane_arrow = Arrow(start=membrane_label.get_left(), end=zoomed_membrane.point_at_angle(0), color=BLUE_ACCENT, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        cytoplasm_arrow = Arrow(start=cytoplasm_label.get_top(), end=zoomed_cytoplasm.get_bottom() + 0.5 * UP, color=GREY_TEXT, stroke_width=2, max_tip_length_to_length_ratio=0.1)

        # Fade out grid and text, then transform one cell into the zoomed version
        self.play(
            FadeOut(grid_cells),
            FadeOut(building_blocks_text),
            FadeOut(title),
            run_time=1
        )
        self.play(
            ReplacementTransform(target_cell.copy().move_to(ORIGIN), zoomed_membrane),
            Create(zoomed_cytoplasm),
            run_time=1.5
        )

        self.play(
            Write(membrane_label),
            Create(membrane_arrow),
            run_time=0.7
        )
        self.play(
            Write(cytoplasm_label),
            Create(cytoplasm_arrow),
            run_time=0.7
        )
        self.wait(1)

        # CS Analogy: Encapsulation
        encapsulation_text = MathTex("\\text{Encapsulation} \\, \\approx \\, \\text{API Interface}", color=GOLD_ACCENT, font_size=35).next_to(zoomed_membrane, RIGHT, buff=1.5)
        encapsulation_text.shift(UP * 0.5)
        self.play(FadeIn(encapsulation_text, shift=UP))
        self.wait(1)
        self.play(FadeOut(encapsulation_text))

        # --- Beat 3: The Control Center (Nucleus) & Energy Source (Mitochondria) ---
        # Nucleus as the control center
        nucleus = Circle(radius=0.7, color=GOLD_ACCENT, fill_opacity=0.6, stroke_width=2)
        nucleus_label = MathTex("Nucleus", color=GOLD_ACCENT, font_size=30).next_to(nucleus, LEFT, buff=0.3)
        nucleus_arrow = Arrow(start=nucleus_label.get_right(), end=nucleus.get_left(), color=GOLD_ACCENT, stroke_width=2, max_tip_length_to_length_ratio=0.1)

        self.play(
            SpinInFromNothing(nucleus),
            Write(nucleus_label),
            Create(nucleus_arrow),
            run_time=1.5
        )
        self.wait(0.5)

        # CS Analogy: CPU/Kernel
        cpu_text = MathTex("\\text{Control Center} \\, \\approx \\, \\text{CPU}", color=GOLD_ACCENT, font_size=35).next_to(nucleus, LEFT, buff=1.5)
        cpu_text.shift(UP * 0.5)
        self.play(FadeIn(cpu_text, shift=UP))
        self.wait(1)
        self.play(FadeOut(cpu_text))

        # Mitochondria as energy producers
        mito_1 = Ellipse(width=0.8, height=0.4, color=BLUE_ACCENT, fill_opacity=0.4, stroke_width=1).shift(UP * 1 + RIGHT * 1)
        mito_2 = Ellipse(width=0.8, height=0.4, color=BLUE_ACCENT, fill_opacity=0.4, stroke_width=1).shift(DOWN * 1.2 + LEFT * 1)
        
        mitochondria_label = MathTex("Mitochondria", color=BLUE_ACCENT, font_size=30).next_to(mito_1, RIGHT, buff=0.3)
        mito_arrow = Arrow(start=mitochondria_label.get_left(), end=mito_1.get_right(), color=BLUE_ACCENT, stroke_width=2, max_tip_length_to_length_ratio=0.1)

        self.play(
            LaggedStart(GrowFromCenter(mito_1), GrowFromCenter(mito_2), lag_ratio=0.5),
            Write(mitochondria_label),
            Create(mito_arrow),
            run_time=1.5
        )
        self.wait(0.5)

        # CS Analogy: Power Supply
        power_text = MathTex("\\text{Energy} \\, \\approx \\, \\text{Power Supply}", color=GOLD_ACCENT, font_size=35).next_to(VGroup(mito_1, mito_2), RIGHT, buff=1.5)
        power_text.shift(DOWN * 0.5)
        self.play(FadeIn(power_text, shift=DOWN))
        self.wait(1)
        self.play(FadeOut(power_text))

        self.play(
            FadeOut(membrane_label, membrane_arrow),
            FadeOut(cytoplasm_label, cytoplasm_arrow),
            FadeOut(nucleus_label, nucleus_arrow),
            FadeOut(mitochondria_label, mito_arrow)
        )
        self.wait(0.5)

        # --- Beat 4: Fundamental Functions - Metabolism & Reproduction ---
        functions_title = MathTex("Fundamental \\, Functions", color=GOLD_ACCENT, font_size=48).to_edge(UP)
        self.play(Write(functions_title))
        self.wait(0.5)
        
        # Metabolism (simplified as resource flow)
        metabolism_text = MathTex("Metabolism \\,(Resource \\, Processing)", color=GREY_TEXT, font_size=35).to_edge(LEFT).shift(UP*1)
        self.play(Write(metabolism_text))

        resource_dot_1 = Dot(color=GREEN, radius=0.08).shift(LEFT * 3 + UP * 0.5)
        resource_dot_2 = Dot(color=GREEN, radius=0.08).shift(LEFT * 3 + DOWN * 0.5)
        
        resource_arrow_1 = Arrow(start=resource_dot_1.get_right(), end=zoomed_membrane.get_left() + UP*0.5, color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        resource_arrow_2 = Arrow(start=resource_dot_2.get_right(), end=zoomed_membrane.get_left() + DOWN*0.5, color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.1)

        self.play(
            FadeIn(resource_dot_1, shift=LEFT),
            FadeIn(resource_dot_2, shift=LEFT),
            Create(resource_arrow_1),
            Create(resource_arrow_2),
            run_time=1
        )
        self.play(
            MoveAlongPath(resource_dot_1, Line(start=resource_dot_1.get_center(), end=nucleus.get_center())),
            MoveAlongPath(resource_dot_2, Line(start=resource_dot_2.get_center(), end=mito_1.get_center())),
            run_time=1.5
        )
        self.play(FadeOut(resource_dot_1, resource_dot_2, resource_arrow_1, resource_arrow_2))
        self.wait(0.5)

        # CS Analogy: Data Processing
        data_processing_text = MathTex("\\approx \\, \\text{Data Processing}", color=GOLD_ACCENT, font_size=30).next_to(metabolism_text, DOWN, buff=0.3)
        self.play(FadeIn(data_processing_text, shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(metabolism_text, data_processing_text))


        # Reproduction (Cell Division)
        reproduction_text = MathTex("Reproduction \\,(Self-Replication)", color=GREY_TEXT, font_size=35).to_edge(RIGHT).shift(UP*1)
        self.play(Write(reproduction_text))

        # Show cell elongating and dividing
        original_cell_group = VGroup(zoomed_membrane, zoomed_cytoplasm, nucleus, mito_1, mito_2)
        
        # Animate elongation
        elongated_membrane = Ellipse(width=4.5, height=4, color=BLUE_ACCENT, stroke_width=4)
        elongated_cytoplasm = Ellipse(width=4.4, height=3.9, color=DARK_GREY, fill_opacity=0.5)
        
        # Clone nucleus and mitochondria for division
        nucleus_copy = nucleus.copy().shift(LEFT * 0.7)
        nucleus.shift(RIGHT * 0.7)
        mito_1_copy = mito_1.copy().shift(LEFT * 1)
        mito_2_copy = mito_2.copy().shift(LEFT * 1)
        mito_1.shift(RIGHT * 1)
        mito_2.shift(RIGHT * 1)


        self.play(
            Transform(zoomed_membrane, elongated_membrane),
            Transform(zoomed_cytoplasm, elongated_cytoplasm),
            Transform(nucleus, nucleus), # No visual change to nucleus but keeps it in animation group
            Transform(mito_1, mito_1),
            Transform(mito_2, mito_2),
            Transform(nucleus_copy, nucleus_copy),
            Transform(mito_1_copy, mito_1_copy),
            Transform(mito_2_copy, mito_2_copy),
            run_time=1.5
        )

        # Divide into two cells
        new_cell_1_membrane = Circle(radius=2, color=BLUE_ACCENT, stroke_width=4).shift(LEFT * 1.5)
        new_cell_1_cytoplasm = Circle(radius=1.9, color=DARK_GREY, fill_opacity=0.5, stroke_opacity=0).shift(LEFT * 1.5)
        new_cell_2_membrane = Circle(radius=2, color=BLUE_ACCENT, stroke_width=4).shift(RIGHT * 1.5)
        new_cell_2_cytoplasm = Circle(radius=1.9, color=DARK_GREY, fill_opacity=0.5, stroke_opacity=0).shift(RIGHT * 1.5)

        self.play(
            FadeTransform(zoomed_membrane, VGroup(new_cell_1_membrane, new_cell_2_membrane)),
            FadeTransform(zoomed_cytoplasm, VGroup(new_cell_1_cytoplasm, new_cell_2_cytoplasm)),
            FadeTransform(nucleus, nucleus_copy.move_to(new_cell_1_membrane.get_center())),
            FadeTransform(nucleus_copy, nucleus.move_to(new_cell_2_membrane.get_center())),
            FadeTransform(mito_1, mito_1_copy.shift(LEFT * 2)),
            FadeTransform(mito_2, mito_2_copy.shift(LEFT * 2)),
            FadeTransform(mito_1_copy, mito_1.shift(RIGHT * 2)),
            FadeTransform(mito_2_copy, mito_2.shift(RIGHT * 2)),
            run_time=2
        )
        self.wait(0.5)

        # CS Analogy: Spawning Processes
        spawning_text = MathTex("\\approx \\, \\text{Spawning Processes}", color=GOLD_ACCENT, font_size=30).next_to(reproduction_text, DOWN, buff=0.3)
        self.play(FadeIn(spawning_text, shift=LEFT))
        self.wait(1)
        self.play(FadeOut(reproduction_text, spawning_text))

        self.play(
            FadeOut(functions_title),
            FadeOut(new_cell_1_membrane, new_cell_1_cytoplasm, new_cell_2_membrane, new_cell_2_cytoplasm),
            FadeOut(nucleus, nucleus_copy, mito_1, mito_2, mito_1_copy, mito_2_copy) # ensure all clones are removed
        )

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Cell Structure & Functions", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(recap_title))

        recap_points = VGroup(
            MathTex("\\bullet \\, \\text{Cells: Fundamental Units of Life}", color=GREY_TEXT),
            MathTex("\\bullet \\, \\text{Cell Membrane: Boundary/Interface}", color=GREY_TEXT),
            MathTex("\\bullet \\, \\text{Nucleus: Control Center (CPU)}", color=GREY_TEXT),
            MathTex("\\bullet \\, \\text{Mitochondria: Energy Production (Power Supply)}", color=GREY_TEXT),
            MathTex("\\bullet \\, \\text{Functions: Metabolism (Processing), Reproduction (Spawning)}", color=GREY_TEXT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).scale(0.8).next_to(recap_title, DOWN, buff=0.7)

        self.play(LaggedStart(*[FadeIn(point, shift=UP) for point in recap_points], lag_ratio=0.2), run_time=3)
        self.wait(3)
        self.play(FadeOut(recap_title, recap_points))
        self.wait(1)