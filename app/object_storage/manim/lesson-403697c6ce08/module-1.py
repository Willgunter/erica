from manim import *

class CellsModule(Scene):
    def construct(self):
        # 1. Setup Colors (3Blue1Brown inspired: dark background, blue and gold accents)
        BLUE_ACCENT = ManimColor("#4285F4")  # A vibrant blue
        GOLD_ACCENT = ManimColor("#FBBC04")  # A bright gold/yellow
        TEXT_COLOR = WHITE

        # Ensure explicit black background
        self.camera.background_color = BLACK

        # --- Visual Hook: Abstract Building Blocks ---
        title = Text("Cells: Life's Basic Building Blocks", font_size=56, color=TEXT_COLOR).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # A grid of uniform 'components'
        initial_grid = VGroup(*[
            Rectangle(width=0.8, height=0.8, color=GOLD_ACCENT, fill_opacity=0.6)
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.3).scale(0.8)
        self.play(FadeIn(initial_grid, shift=DOWN), run_time=1.5)
        self.wait(0.5)

        # Components transform, showing variation and hinting at organic forms
        target_shapes = VGroup()
        for i, shape in enumerate(initial_grid):
            if i % 3 == 0:  # Every third one becomes a blue circle
                new_shape = Circle(radius=shape.width / 2, color=BLUE_ACCENT, fill_opacity=0.7).move_to(shape)
            else:  # Others stay golden rectangles/squares, slightly modified
                new_shape = shape.copy().set_color(GOLD_ACCENT).set_fill_opacity(0.7).scale(random.uniform(0.9, 1.1))
            target_shapes.add(new_shape)

        self.play(
            Transform(initial_grid, target_shapes),
            initial_grid.animate.shift(LEFT * 0.5 + UP * 0.5).scale(0.9),  # slight movement for dynamism
            run_time=2
        )
        self.wait(1)
        self.play(FadeOut(initial_grid, shift=UP), FadeOut(title, shift=UP))  # Clear the hook


        # --- Beat 1: The Fundamental Unit ---
        beat1_title = Text("1. The Fundamental Unit", color=BLUE_ACCENT, font_size=40).to_edge(UL, buff=0.7)
        self.play(Write(beat1_title))
        self.wait(0.5)

        # Abstract representation of an organism (complex system)
        organism = Polygon(
            [-2, 1, 0], [0, 3, 0], [2, 1, 0], [1.5, -1.5, 0], [-1.5, -1.5, 0],
            color=BLUE_ACCENT, fill_opacity=0.7
        ).scale(1.5).shift(RIGHT * 2)
        self.play(FadeIn(organism, shift=LEFT), run_time=1.5)

        organism_label = Text("Organism (Complex System)", color=TEXT_COLOR, font_size=28).next_to(organism, DOWN, buff=0.5)
        self.play(Write(organism_label))
        self.wait(1)

        # Show organism breaking down into many cells
        cells = VGroup()
        for _ in range(30):
            # Create cells randomly within the organism's bounds for a 'shattering' effect
            cell = Circle(radius=0.2, color=GOLD_ACCENT, fill_opacity=0.8).move_to(organism.get_random_point())
            cells.add(cell)

        self.play(
            FadeOut(organism_label),
            FadeOut(organism),  # Organism fades out
            LaggedStart(
                *[FadeIn(cell) for cell in cells],  # Cells fade in, scattered
                lag_ratio=0.05
            ),
            run_time=2
        )
        self.wait(0.5)

        cell_label_intro = Text("Composed of many units...", color=TEXT_COLOR, font_size=28).next_to(cells, DOWN, buff=0.5)
        self.play(Write(cell_label_intro))
        self.wait(1)

        # Emphasize one cell and introduce the formal concept
        one_cell_proto = Circle(radius=0.5, color=GOLD_ACCENT, fill_opacity=0.8).move_to(LEFT * 3)
        self.play(
            LaggedStart(
                *[cell.animate.set_opacity(0.2) for cell in cells], # Dim other cells
                lag_ratio=0.05
            ),
            Transform(cells.get_center_mobject(), one_cell_proto), # Move one cell to focus and enlarge
            cell_label_intro.animate.set_opacity(0.2), # Dim previous label
            run_time=1.5
        )
        self.wait(0.5)

        cell_concept_text = MathTex(r"\text{Cell}", r"\text{ (Life's Basic Building Block)}", font_size=48, color=TEXT_COLOR)
        cell_concept_text[0].set_color(BLUE_ACCENT)
        cell_concept_text[1].set_color(GOLD_ACCENT)
        cell_concept_text.next_to(one_cell_proto, RIGHT, buff=1)

        self.play(
            FadeIn(cell_concept_text[0], shift=UP),
            one_cell_proto.animate.scale(1.2),
            run_time=1
        )
        self.play(
            FadeIn(cell_concept_text[1], shift=DOWN),
            run_time=1
        )
        self.wait(2)

        self.play(
            FadeOut(one_cell_proto, cell_concept_text, cells, cell_label_intro.set_opacity(1), beat1_title), # Fade out all elements
            run_time=1.5
        )


        # --- Beat 2: A Tiny Machine (Simplified Cell Structure) ---
        beat2_title = Text("2. A Tiny Machine (Cell Structure)", color=BLUE_ACCENT, font_size=40).to_edge(UL, buff=0.7)
        self.play(Write(beat2_title))
        self.wait(0.5)

        # Outer membrane (boundary)
        membrane = Circle(radius=1.5, color=GOLD_ACCENT, fill_opacity=0.2, stroke_width=4)
        membrane_label = Text("Cell Membrane", color=TEXT_COLOR, font_size=24).next_to(membrane, UP + RIGHT, buff=0.2)

        # Cytoplasm (internal environment)
        cytoplasm = Circle(radius=1.45, color=BLUE_ACCENT, fill_opacity=0.3)
        cytoplasm_label = Text("Cytoplasm", color=TEXT_COLOR, font_size=24).next_to(cytoplasm, DOWN + LEFT, buff=0.2)

        # Nucleus (control center)
        nucleus = Circle(radius=0.7, color=GOLD_ACCENT, fill_opacity=0.6)
        nucleus_label = Text("Nucleus", color=TEXT_COLOR, font_size=24).next_to(nucleus, RIGHT, buff=0.2)

        self.play(GrowFromCenter(membrane), FadeIn(membrane_label), run_time=1.5)
        self.play(GrowFromCenter(cytoplasm), FadeIn(cytoplasm_label), run_time=1.5)
        self.play(GrowFromCenter(nucleus), FadeIn(nucleus_label), run_time=1.5)
        self.wait(1)

        analogy_text = Text("Like a self-contained module in CS.", color=TEXT_COLOR, font_size=32).shift(DOWN * 3)
        self.play(Write(analogy_text), run_time=1.5)
        self.wait(2)

        self.play(
            FadeOut(membrane, membrane_label, cytoplasm, cytoplasm_label, nucleus, nucleus_label, analogy_text, beat2_title),
            run_time=1.5
        )


        # --- Beat 3: Diversity and Specialization ---
        beat3_title = Text("3. Diversity & Specialization", color=BLUE_ACCENT, font_size=40).to_edge(UL, buff=0.7)
        self.play(Write(beat3_title))
        self.wait(0.5)

        # Cell 1: Neuron (Star-like, for communication)
        neuron = Star(n=5, outer_radius=0.7, inner_radius=0.3, color=GOLD_ACCENT, fill_opacity=0.7).shift(LEFT * 3 + UP * 0.5)
        neuron_nucleus = Circle(radius=0.2, color=BLUE_ACCENT, fill_opacity=0.8).move_to(neuron)
        neuron_group = VGroup(neuron, neuron_nucleus)
        neuron_label = Text("Nerve Cell (Communication)", color=TEXT_COLOR, font_size=24).next_to(neuron_group, DOWN, buff=0.3)

        # Cell 2: Red Blood Cell (Disk-like, for transport)
        rbc = Circle(radius=0.6, color=GOLD_ACCENT, fill_opacity=0.7).shift(UP * 0.5)
        rbc_nucleus = Circle(radius=0.1, color=BLUE_ACCENT, fill_opacity=0.8).move_to(rbc)
        rbc_group = VGroup(rbc, rbc_nucleus)
        rbc_label = Text("Blood Cell (Transport)", color=TEXT_COLOR, font_size=24).next_to(rbc_group, DOWN, buff=0.3)

        # Cell 3: Plant Cell (Rectangular, for photosynthesis)
        plant_cell = Rectangle(width=1.2, height=1.5, color=GOLD_ACCENT, fill_opacity=0.7).shift(RIGHT * 3 + UP * 0.5)
        plant_cell_nucleus = Circle(radius=0.3, color=BLUE_ACCENT, fill_opacity=0.8).move_to(plant_cell.get_center() + LEFT * 0.3 + UP * 0.3)
        plant_cell_group = VGroup(plant_cell, plant_cell_nucleus)
        plant_cell_label = Text("Plant Cell (Photosynthesis)", color=TEXT_COLOR, font_size=24).next_to(plant_cell_group, DOWN, buff=0.3)

        self.play(
            FadeIn(neuron_group, shift=LEFT), Write(neuron_label),
            FadeIn(rbc_group, shift=UP), Write(rbc_label),
            FadeIn(plant_cell_group, shift=RIGHT), Write(plant_cell_label),
            lag_ratio=0.5, run_time=2.5
        )
        self.wait(1)

        analogy_cs = Text("Different 'classes' or 'functions' in code.", color=TEXT_COLOR, font_size=32).shift(DOWN * 3)
        self.play(Write(analogy_cs))
        self.wait(2)

        self.play(
            FadeOut(neuron_group, neuron_label, rbc_group, rbc_label, plant_cell_group, plant_cell_label, analogy_cs, beat3_title),
            run_time=1.5
        )


        # --- Beat 4: Organization - From Cells to Systems ---
        beat4_title = Text("4. Organization: From Cells to Systems", color=BLUE_ACCENT, font_size=40).to_edge(UL, buff=0.7)
        self.play(Write(beat4_title))
        self.wait(0.5)

        # Individual cells
        base_cell_for_org = Circle(radius=0.2, color=GOLD_ACCENT, fill_opacity=0.7)
        initial_cells_group = VGroup(*[base_cell_for_org.copy() for _ in range(12)])  # 12 cells for a small grid
        initial_cells_group.arrange_in_grid(rows=3, cols=4, buff=0.1).shift(LEFT * 4)

        self.play(FadeIn(initial_cells_group, shift=LEFT))
        cells_label = Text("Cells", color=TEXT_COLOR, font_size=24).next_to(initial_cells_group, DOWN, buff=0.3)
        self.play(Write(cells_label))
        self.wait(1)

        # Cells -> Tissue
        tissue_block_proto = Rectangle(width=2, height=1.5, color=BLUE_ACCENT, fill_opacity=0.6, stroke_width=3).shift(LEFT * 0.5)
        tissue_label = Text("Tissue", color=TEXT_COLOR, font_size=24).next_to(tissue_block_proto, DOWN, buff=0.3)

        arrow1 = Arrow(start=initial_cells_group.get_right(), end=tissue_block_proto.get_left() - LEFT * 0.5, color=WHITE)

        self.play(
            FadeOut(cells_label),
            initial_cells_group.animate.move_to(tissue_block_proto.get_center()).scale(0.8),  # Cells cluster to the tissue's location
            GrowArrow(arrow1),
            run_time=1.5
        )
        self.play(
            Transform(initial_cells_group, tissue_block_proto),  # Clustered cells morph into the tissue block
            FadeIn(tissue_label),
            run_time=1.5
        )
        self.wait(1)

        # Tissue -> Organ
        organ_shape_proto = Polygon(
            [2, 0, 0], [3, 1.5, 0], [4, 0, 0], [3.5, -1.5, 0], [2.5, -1.5, 0],
            color=GOLD_ACCENT, fill_opacity=0.7
        ).scale(1.2).shift(RIGHT * 3)
        organ_label = Text("Organ", color=TEXT_COLOR, font_size=24).next_to(organ_shape_proto, DOWN, buff=0.3)

        arrow2 = Arrow(start=tissue_block_proto.get_right(), end=organ_shape_proto.get_left() - LEFT * 0.5, color=WHITE)

        self.play(
            FadeOut(tissue_label),
            ReplacementTransform(tissue_block_proto, organ_shape_proto),  # Tissue morphs into organ
            GrowArrow(arrow2),
            FadeIn(organ_label),
            run_time=1.5
        )
        self.wait(1)

        analogy_hierarchy = Text("Hierarchical design: from modules to systems.", color=TEXT_COLOR, font_size=32).shift(DOWN * 3.5)
        self.play(Write(analogy_hierarchy))
        self.wait(2)

        self.play(
            FadeOut(organ_shape_proto, organ_label, arrow1, arrow2, analogy_hierarchy, beat4_title),
            run_time=1.5
        )


        # --- Recap Card ---
        recap_title = Text("Recap: Cells - The Basic Building Blocks", color=BLUE_ACCENT, font_size=48).to_edge(UP, buff=0.7)
        self.play(Write(recap_title))

        recap_points = VGroup(
            Text("1. Cells are the fundamental units of all life.", color=TEXT_COLOR, font_size=32).shift(UP * 1),
            Text("2. Each cell is a complex, self-contained 'machine'.", color=TEXT_COLOR, font_size=32),
            Text("3. Cells are diverse, specializing in different functions.", color=TEXT_COLOR, font_size=32).shift(DOWN * 1),
            Text("4. Cells organize into tissues, organs, and systems.", color=TEXT_COLOR, font_size=32).shift(DOWN * 2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=1)

        for i, point in enumerate(recap_points):
            self.play(FadeIn(point, shift=LEFT), run_time=0.8)
            self.wait(0.3)

        self.wait(3)
        self.play(FadeOut(recap_title, recap_points, shift=UP), run_time=1.5)