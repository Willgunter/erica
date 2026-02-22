from manim import *

class DNAHeredityCellDivision(Scene):
    def construct(self):
        # 1. Configuration: Dark background, high-contrast accents
        self.camera.background_color = BLACK # Explicitly set background color
        BLUE_ACCENT = ManimColor("#50B4F2") # A brighter blue
        GOLD_ACCENT = ManimColor("#FFD700") # Gold color
        DARK_GREY = ManimColor("#333333")
        LIGHT_GREY = ManimColor("#CCCCCC")

        # --- Initial Module Title ---
        main_title = Text("DNA, Heredity, & Cell Division", font_size=50, color=GOLD_ACCENT)
        self.play(Write(main_title))
        self.wait(0.8)
        self.play(FadeOut(main_title, shift=UP))

        # --- Beat 1: DNA - The Information Code ---
        # Strong visual hook: Abstract information converging into DNA helix
        info_bits = VGroup(*[
            Dot(radius=0.08, color=random_bright_color()).move_to(random_vector(2)).shift(random_vector(1))
            for _ in range(50)
        ])
        info_label = Text("Information Flow...", font_size=30, color=LIGHT_GREY).to_edge(UP).shift(LEFT*2)

        self.play(LaggedStart(*[FadeIn(bit) for bit in info_bits], lag_ratio=0.05), Write(info_label))
        self.wait(0.5)

        # Create a simplified 2D DNA double helix
        helix_arc_length = 5
        num_segments = 30 # More segments for smoother curve
        
        strand1_points = []
        strand2_points = []
        for i in range(num_segments + 1):
            y = i / num_segments * helix_arc_length - helix_arc_length / 2 # Y-axis
            x_offset = 0.5 * np.sin(i / num_segments * 2 * PI * 2.5) # X-axis, 2.5 complete waves
            strand1_points.append(np.array([x_offset, y, 0]))
            strand2_points.append(np.array([-x_offset, y, 0])) # Opposite phase
            
        strand1 = VMobject().set_points_as_corners(strand1_points).set_color(BLUE_ACCENT).set_stroke(width=3)
        strand2 = VMobject().set_points_as_corners(strand2_points).set_color(BLUE_ACCENT).set_stroke(width=3)
        
        # Base pairs as lines
        base_pair_connectors = VGroup()
        base_colors = [GOLD_ACCENT, LIGHT_GREY] # Alternating colors for visual variety
        for i in range(0, num_segments, 3): # Connect every 3rd segment
            p1 = strand1.get_point_from_proportion(i / num_segments)
            p2 = strand2.get_point_from_proportion(i / num_segments)
            base_pair_connectors.add(Line(p1, p2, color=base_colors[i%2], stroke_width=2))
        
        helix_mobject = Group(strand1, strand2, base_pair_connectors).scale(0.8)
        
        # CS analogy: "The Code"
        dna_title = Text("DNA: The Genetic Blueprint", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        cs_analogy_dna = Text("Like Digital Code: Stores Instructions", font_size=28, color=LIGHT_GREY).next_to(dna_title, DOWN)

        self.play(
            FadeOut(info_bits, shift=DOWN),
            FadeOut(info_label, shift=LEFT),
            Create(helix_mobject),
            Write(dna_title)
        )
        self.play(Write(cs_analogy_dna))
        self.wait(1)

        # Show simplified base pairs (A, T, C, G)
        base_labels = VGroup(
            MathTex(r"\text{A}", color=GOLD_ACCENT),
            MathTex(r"\text{T}", color=BLUE_ACCENT),
            MathTex(r"\text{C}", color=GOLD_ACCENT),
            MathTex(r"\text{G}", color=BLUE_ACCENT)
        ).arrange(RIGHT, buff=0.5).next_to(helix_mobject, DOWN, buff=1)

        base_arrows = VGroup()
        # Points near the helix for arrows
        dummy_point_start = helix_mobject.get_center() + DOWN*1.5 + LEFT*1.5
        dummy_point_end = helix_mobject.get_center() + DOWN*1.5 + RIGHT*1.5
        for i, label in enumerate(base_labels):
            # Interpolate a start point for each arrow along an invisible line
            dummy_point = interpolate(dummy_point_start, dummy_point_end, i / (len(base_labels) - 1))
            arrow = Arrow(dummy_point, label.get_center(), buff=0.2, color=LIGHT_GREY, stroke_width=2)
            base_arrows.add(arrow)
            
        self.play(LaggedStart(*[FadeIn(label, shift=DOWN) for label in base_labels], lag_ratio=0.1),
                  LaggedStart(*[GrowArrow(arrow) for arrow in base_arrows], lag_ratio=0.1))
        self.wait(1.5)

        self.play(
            FadeOut(dna_title, shift=UP),
            FadeOut(cs_analogy_dna, shift=UP),
            FadeOut(base_labels, shift=DOWN),
            FadeOut(base_arrows, shift=DOWN),
            FadeOut(helix_mobject, shift=DOWN)
        )

        # --- Beat 2: Heredity - Passing the Blueprint ---
        heredity_title = Text("Heredity: Passing the Blueprint", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        cs_analogy_heredity = Text("Inheritance: Sharing Code", font_size=28, color=LIGHT_GREY).next_to(heredity_title, DOWN)

        # Simplify chromosomes
        parent1_chromo_line = Line(UP*0.5, DOWN*0.5).set_color(BLUE_ACCENT).set_stroke(width=6)
        parent2_chromo_line = Line(UP*0.5, DOWN*0.5).set_color(GOLD_ACCENT).set_stroke(width=6)
        parent1_chromo_label = Text("Gene A", font_size=20, color=LIGHT_GREY).next_to(parent1_chromo_line, LEFT*0.7)
        parent2_chromo_label = Text("Gene B", font_size=20, color=LIGHT_GREY).next_to(parent2_chromo_line, RIGHT*0.7)
        parent1_chromo = VGroup(parent1_chromo_line, parent1_chromo_label).shift(LEFT*3)
        parent2_chromo = VGroup(parent2_chromo_line, parent2_chromo_label).shift(RIGHT*3)
        
        parent_label_p1 = Text("Parent 1", font_size=24, color=BLUE_ACCENT).next_to(parent1_chromo, DOWN)
        parent_label_p2 = Text("Parent 2", font_size=24, color=GOLD_ACCENT).next_to(parent2_chromo, DOWN)
        
        plus_sign = MathTex("+", color=LIGHT_GREY).move_to(ORIGIN)
        
        # Offspring chromosome (mixing colors)
        offspring_chromo_segment1 = Line(UP*0.5, ORIGIN).set_color(BLUE_ACCENT).set_stroke(width=6)
        offspring_chromo_segment2 = Line(ORIGIN, DOWN*0.5).set_color(GOLD_ACCENT).set_stroke(width=6)
        offspring_chromo_v = VGroup(offspring_chromo_segment1, offspring_chromo_segment2)
        offspring_gene_a = Text("Gene A", font_size=20, color=LIGHT_GREY).next_to(offspring_chromo_segment1, LEFT*0.7)
        offspring_gene_b = Text("Gene B", font_size=20, color=LIGHT_GREY).next_to(offspring_chromo_segment2, RIGHT*0.7)
        offspring_chromo = VGroup(offspring_chromo_v, offspring_gene_a, offspring_gene_b).shift(RIGHT*2)

        offspring_label = Text("Offspring", font_size=24, color=LIGHT_GREY).next_to(offspring_chromo, DOWN)

        arrow_to_offspring = Arrow(plus_sign.get_right(), offspring_chromo.get_left(), color=LIGHT_GREY, buff=0.2)
        
        self.play(
            FadeIn(heredity_title, shift=UP),
            FadeIn(cs_analogy_heredity, shift=UP),
            Create(parent1_chromo),
            Create(parent2_chromo),
            Write(parent_label_p1),
            Write(parent_label_p2),
            Write(plus_sign)
        )
        self.wait(0.5)
        
        self.play(
            Create(offspring_chromo),
            GrowArrow(arrow_to_offspring),
            Write(offspring_label)
        )
        self.wait(1.5)

        self.play(
            FadeOut(heredity_title, shift=UP),
            FadeOut(cs_analogy_heredity, shift=UP),
            FadeOut(parent1_chromo, shift=LEFT),
            FadeOut(parent2_chromo, shift=RIGHT),
            FadeOut(parent_label_p1, shift=LEFT),
            FadeOut(parent_label_p2, shift=RIGHT),
            FadeOut(plus_sign),
            FadeOut(arrow_to_offspring),
            FadeOut(offspring_chromo, shift=DOWN),
            FadeOut(offspring_label, shift=DOWN)
        )

        # --- Beat 3: Cell Division - Copying the Blueprint ---
        cell_division_title = Text("Cell Division: Copying the Blueprint", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        cs_analogy_division = Text("Replication: Identical Copies", font_size=28, color=LIGHT_GREY).next_to(cell_division_title, DOWN)

        # Single cell with a chromosome
        parent_cell_shape = Circle(radius=1.5, color=DARK_GREY, fill_opacity=0.3)
        initial_chromosome_line = Line(UP*0.5, DOWN*0.5, color=BLUE_ACCENT, stroke_width=5)
        parent_cell_group = VGroup(parent_cell_shape, initial_chromosome_line.copy()).shift(LEFT*3) # Group cell and chromosome

        self.play(
            FadeIn(cell_division_title, shift=UP),
            FadeIn(cs_analogy_division, shift=UP),
            Create(parent_cell_group)
        )
        self.wait(0.5)

        # DNA Replication: Chromosome duplicates
        duplicated_chromosome_lines = VGroup(
            initial_chromosome_line.copy().shift(LEFT*0.2),
            initial_chromosome_line.copy().shift(RIGHT*0.2)
        ).move_to(parent_cell_group[0].get_center()) # Position correctly
        
        replication_text = Text("Replication!", font_size=30, color=GOLD_ACCENT).next_to(parent_cell_group, UP)

        self.play(
            Transform(parent_cell_group[1], duplicated_chromosome_lines), # Transform only the chromosome part
            Write(replication_text)
        )
        self.wait(1)
        self.play(FadeOut(replication_text))

        # Cell Division (Mitosis): Cell divides
        child_cell_1_shape = Circle(radius=1.2, color=DARK_GREY, fill_opacity=0.3).shift(LEFT*2.5 + DOWN*1.5)
        child_cell_2_shape = Circle(radius=1.2, color=DARK_GREY, fill_opacity=0.3).shift(RIGHT*2.5 + DOWN*1.5)

        # Create target chromosomes for the children from the duplicated ones
        child_chromo_1_target = initial_chromosome_line.copy().move_to(child_cell_1_shape.get_center())
        child_chromo_2_target = initial_chromosome_line.copy().move_to(child_cell_2_shape.get_center())

        self.play(
            Transform(parent_cell_group[0], VGroup(child_cell_1_shape, child_cell_2_shape)), # Parent cell splits
            Transform(parent_cell_group[1][0], child_chromo_1_target), # Left strand goes to child 1
            Transform(parent_cell_group[1][1], child_chromo_2_target), # Right strand goes to child 2
            run_time=2
        )
        
        # Add labels for child cells
        cell1_label = Text("New Cell 1", font_size=24, color=LIGHT_GREY).next_to(child_cell_1_shape, DOWN)
        cell2_label = Text("New Cell 2", font_size=24, color=LIGHT_GREY).next_to(child_cell_2_shape, DOWN)
        self.play(Write(cell1_label), Write(cell2_label))
        self.wait(1.5)

        # Fade out all elements from this beat
        self.play(
            FadeOut(cell_division_title, shift=UP),
            FadeOut(cs_analogy_division, shift=UP),
            FadeOut(parent_cell_group[0]), # Fade out the original cell shape (now transformed into child cell shapes)
            FadeOut(parent_cell_group[1][0]), FadeOut(parent_cell_group[1][1]), # Fade out the transformed chromosome pieces
            FadeOut(child_cell_1_shape), FadeOut(child_cell_2_shape), # Ensure child shapes are faded out if not completely covered by the transform
            FadeOut(child_chromo_1_target), FadeOut(child_chromo_2_target), # Fade out the final chromosomes
            FadeOut(cell1_label), FadeOut(cell2_label)
        )

        # --- Recap Card ---
        recap_title = Text("Recap:", font_size=45, color=GOLD_ACCENT).to_edge(UP)
        recap_points = VGroup(
            Text("• DNA: The Blueprint of Life (Information Code)", font_size=32, color=LIGHT_GREY),
            Text("• Heredity: Passing Traits (Sharing Code)", font_size=32, color=LIGHT_GREY),
            Text("• Cell Division: Duplicating for Growth (Replication)", font_size=32, color=LIGHT_GREY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(recap_title), FadeIn(recap_points[0]))
        self.wait(0.5)
        self.play(FadeIn(recap_points[1]))
        self.wait(0.5)
        self.play(FadeIn(recap_points[2]))
        self.wait(2)
        self.play(FadeOut(recap_title), FadeOut(recap_points))
        
        self.wait(0.5) # Final buffer