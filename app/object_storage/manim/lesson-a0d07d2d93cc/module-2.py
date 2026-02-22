from manim import *

# Custom colors for 3B1B style
BLUE_ACCENT = "#87CEEB"  # Sky blue
GOLD_ACCENT = "#FFD700"  # Gold
DARK_BACKGROUND = "#1a1a1a" # Very dark grey
GREEN_HIGHLIGHT = "#7CFC00" # Bright green
RED_HIGHLIGHT = "#FF6347" # Tomato red
GREY_BOND = "#808080" # Grey for bonds

class DnaInheritanceCellDivision(Scene):
    def construct(self):
        self.camera.background_color = DARK_BACKGROUND

        # --- Opening Hook: Abstract DNA Helix Formation ---
        self.play_opening_hook()

        # --- Beat 1: DNA Structure - The Blueprint ---
        self.play_dna_structure_beat()

        # --- Beat 2: Inheritance - Passing on Traits ---
        self.play_inheritance_beat()

        # --- Beat 3: Cell Division - Making More Cells ---
        self.play_cell_division_beat()

        # --- Recap Card ---
        self.play_recap_card()

    def play_opening_hook(self):
        title = Text("DNA: Blueprint of Life", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(0.5)

        # Create scattered points that will form a helix
        num_points = 60
        scattered_points_1 = VGroup(*[Dot(point=np.random.rand(3)*4 - 2, radius=0.05, color=BLUE_ACCENT) for _ in range(num_points)])
        scattered_points_2 = VGroup(*[Dot(point=np.random.rand(3)*4 - 2, radius=0.05, color=GOLD_ACCENT) for _ in range(num_points)])

        # Target helix points (2D representation of a helix)
        helix_points_1 = []
        helix_points_2 = []
        radius = 1.0
        height = 3.0
        num_turns = 2
        for i in range(num_points):
            t = i / (num_points - 1) * num_turns * 2 * PI
            x1 = radius * np.cos(t) * (1 - i/(num_points*2)) # Slightly contract helix
            y1 = radius * np.sin(t) * (1 - i/(num_points*2))
            z1 = t * height / (2 * PI * num_turns) - height/2
            helix_points_1.append(np.array([x1, y1, z1]))

            x2 = radius * np.cos(t + PI) * (1 - i/(num_points*2)) # Opposite side
            y2 = radius * np.sin(t + PI) * (1 - i/(num_points*2))
            z2 = z1 
            helix_points_2.append(np.array([x2, y2, z2]))
        
        target_helix_1 = VGroup(*[Dot(point=p, radius=0.05, color=BLUE_ACCENT) for p in helix_points_1])
        target_helix_2 = VGroup(*[Dot(point=p, radius=0.05, color=GOLD_ACCENT) for p in helix_points_2])

        self.play(
            LaggedStart(
                Transform(scattered_points_1, target_helix_1),
                Transform(scattered_points_2, target_helix_2),
                lag_ratio=0.01,
                run_time=3
            )
        )
        
        # Connect them to form a helix-like structure (lines between corresponding points for base pairs)
        base_pair_lines = VGroup()
        for i in range(num_points):
            line = DashedLine(target_helix_1[i].get_center(), target_helix_2[i].get_center(), stroke_width=1, color=GREY_BOND)
            base_pair_lines.add(line)
        
        self.play(Create(base_pair_lines, lag_ratio=0.01), run_time=2)
        dna_helix = VGroup(target_helix_1, target_helix_2, base_pair_lines)
        self.play(dna_helix.animate.scale(0.8).shift(LEFT*3 + DOWN*0.5), run_time=1.5)

        # Introduce the concept
        intro_text = Text("Genetics: How traits are passed down", font_size=36, color=WHITE).next_to(dna_helix, RIGHT, buff=1)
        dna_text = Text("Dictated by DNA", font_size=36, color=BLUE_ACCENT).next_to(intro_text, DOWN, aligned_edge=LEFT)
        
        self.play(Write(intro_text), run_time=1.5)
        self.play(Write(dna_text), run_time=1.5)
        
        self.wait(1)
        self.play(FadeOut(dna_helix, intro_text, dna_text, title))

    def create_dna_segment(self, length=4):
        # Create a simplified DNA segment with specified number of base pairs
        base_pairs_group = VGroup()

        # Define colors for A, T, G, C
        A_COLOR = BLUE_ACCENT
        T_COLOR = GOLD_ACCENT
        G_COLOR = GREEN_HIGHLIGHT
        C_COLOR = RED_HIGHLIGHT

        # Define shapes for A, T, G, C (using squares for clarity)
        base_A_proto = Square(side_length=0.2, color=A_COLOR, fill_opacity=1)
        base_T_proto = Square(side_length=0.2, color=T_COLOR, fill_opacity=1)
        base_G_proto = Square(side_length=0.2, color=G_COLOR, fill_opacity=1)
        base_C_proto = Square(side_length=0.2, color=C_COLOR, fill_opacity=1)

        # Sequence for visual interest, ensuring A-T and G-C pairing
        base_pairs_sequence = [
            (base_A_proto, base_T_proto),
            (base_G_proto, base_C_proto),
            (base_T_proto, base_A_proto),
            (base_C_proto, base_G_proto),
            (base_A_proto, base_T_proto),
            (base_G_proto, base_C_proto)
        ]
        
        vertical_spacing = 0.5
        horizontal_base_offset = 0.5 # Distance from center line for bases
        horizontal_backbone_offset = 1.0 # Distance from center line for backbone
        
        left_backbone_points = []
        right_backbone_points = []

        for i in range(length):
            y_pos = (length / 2 - i - 0.5) * vertical_spacing # Center vertically

            # Create bases
            base1_proto, base2_proto = base_pairs_sequence[i % len(base_pairs_sequence)]
            base1 = base1_proto.copy().move_to(LEFT * horizontal_base_offset + UP * y_pos)
            base2 = base2_proto.copy().move_to(RIGHT * horizontal_base_offset + UP * y_pos)
            
            # Connect bases with dashed lines (hydrogen bonds)
            h_bonds = DashedLine(base1.get_center(), base2.get_center(), color=GREY_BOND, stroke_width=1.5)
            
            base_pairs_group.add(VGroup(base1, base2, h_bonds))

            # Store backbone points
            left_backbone_points.append(np.array([ -horizontal_backbone_offset, y_pos, 0 ]))
            right_backbone_points.append(np.array([ horizontal_backbone_offset, y_pos, 0 ]))
            
        # Create continuous backbone lines
        left_backbone_path = VGroup(*[Line(left_backbone_points[i], left_backbone_points[i+1], color=WHITE, stroke_width=3) for i in range(len(left_backbone_points)-1)])
        right_backbone_path = VGroup(*[Line(right_backbone_points[i], right_backbone_points[i+1], color=WHITE, stroke_width=3) for i in range(len(right_backbone_points)-1)])

        dna_segment = VGroup(left_backbone_path, right_backbone_path, base_pairs_group)
        return dna_segment.center()

    def play_dna_structure_beat(self):
        title = Text("DNA Structure: The Double Helix", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(0.5)

        dna_segment = self.create_dna_segment(length=4).scale(1.2).to_edge(LEFT, buff=0.5)
        self.play(Create(dna_segment), run_time=3)
        self.wait(1)

        # Labeling components
        backbone_label = Text("Sugar-Phosphate Backbone", font_size=28, color=BLUE_ACCENT).next_to(dna_segment[0], UP, buff=0.3)
        bases_label = Text("Nucleotide Bases (A, T, G, C)", font_size=28, color=GOLD_ACCENT).next_to(dna_segment[2][0], RIGHT, buff=0.5)
        h_bond_label = Text("Hydrogen Bonds", font_size=28, color=GREY_BOND).next_to(dna_segment[2][0][2], DOWN, buff=0.3)

        self.play(Write(backbone_label))
        self.play(Write(bases_label))
        self.play(Write(h_bond_label))
        self.wait(2)

        # Show sequence as information
        sequence_text = MathTex(
            r"\text{...A-G-C-T-T-C-G-A...}",
            font_size=40, color=WHITE
        ).next_to(dna_segment, RIGHT, buff=1.5).shift(UP*1.5)
        
        info_text = Text("Genetic Information", font_size=32, color=GREEN_HIGHLIGHT).next_to(sequence_text, DOWN, buff=0.5)
        info_arrow = Arrow(info_text.get_top(), sequence_text.get_bottom(), color=GREEN_HIGHLIGHT)

        self.play(Write(sequence_text), Create(info_arrow), Write(info_text), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(title, dna_segment, backbone_label, bases_label, h_bond_label, sequence_text, info_arrow, info_text)
        )

    def create_single_chromatid(self, color, scale=0.5):
        return RoundedRectangle(width=0.15 * scale, height=1.0 * scale, corner_radius=0.075 * scale, color=color, fill_opacity=1, stroke_width=0)

    def create_duplicated_chromosome(self, color, scale=0.5):
        chromatid1 = self.create_single_chromatid(color, scale).shift(LEFT * 0.08 * scale)
        chromatid2 = self.create_single_chromatid(color, scale).shift(RIGHT * 0.08 * scale)
        centromere = Circle(radius=0.06*scale, color=GREY_BOND, fill_opacity=1, stroke_width=0).move_to(ORIGIN)
        return VGroup(chromatid1, chromatid2, centromere).center()

    def play_inheritance_beat(self):
        title = Text("Inheritance: Passing on Traits", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(0.5)

        # Parent 1 Chromosomes (blue)
        parent1_chr1 = self.create_single_chromatid(BLUE_ACCENT, scale=0.7).shift(LEFT*4 + UP*0.5)
        parent1_chr2 = self.create_single_chromatid(BLUE_ACCENT, scale=0.7).shift(LEFT*4 + DOWN*0.5)
        parent1_label = Text("Parent 1 (2n)", font_size=28, color=BLUE_ACCENT).next_to(parent1_chr1, UP, buff=0.8).set_x(parent1_chr1.get_x())
        parent1 = VGroup(parent1_chr1, parent1_chr2, parent1_label)

        # Parent 2 Chromosomes (gold)
        parent2_chr1 = self.create_single_chromatid(GOLD_ACCENT, scale=0.7).shift(RIGHT*4 + UP*0.5)
        parent2_chr2 = self.create_single_chromatid(GOLD_ACCENT, scale=0.7).shift(RIGHT*4 + DOWN*0.5)
        parent2_label = Text("Parent 2 (2n)", font_size=28, color=GOLD_ACCENT).next_to(parent2_chr1, UP, buff=0.8).set_x(parent2_chr1.get_x())
        parent2 = VGroup(parent2_chr1, parent2_chr2, parent2_label)

        self.play(Create(parent1), Create(parent2), run_time=2)
        self.wait(1)

        # Meiosis / Gamete formation (only one chromosome from each parent shown)
        gamete1_chr = self.create_single_chromatid(BLUE_ACCENT, scale=0.5).move_to(LEFT*2 + DOWN*0.5)
        gamete2_chr = self.create_single_chromatid(GOLD_ACCENT, scale=0.5).move_to(RIGHT*2 + DOWN*0.5)
        
        gamete1_label = Text("Gamete (n)", font_size=24, color=BLUE_ACCENT).next_to(gamete1_chr, DOWN)
        gamete2_label = Text("Gamete (n)", font_size=24, color=GOLD_ACCENT).next_to(gamete2_chr, DOWN)
        
        self.play(
            FadeOut(parent1_chr2, parent2_chr2), 
            Transform(parent1_chr1, gamete1_chr),
            Transform(parent2_chr1, gamete2_chr),
            FadeIn(gamete1_label, gamete2_label, shift=UP),
            FadeOut(parent1_label, parent2_label),
            run_time=2
        )
        self.wait(1)

        # Fertilization (combination)
        zygote_chr1 = gamete1_chr.copy().move_to(ORIGIN + LEFT*0.5)
        zygote_chr2 = gamete2_chr.copy().move_to(ORIGIN + RIGHT*0.5)
        
        zygote_label = Text("Offspring (2n)", font_size=32, color=WHITE).next_to(zygote_chr1, DOWN, buff=1).set_x(ORIGIN[0])

        plus_sign = MathTex("+", font_size=50, color=WHITE).move_to(ORIGIN + LEFT*2)
        equals_sign = MathTex("=", font_size=50, color=WHITE).move_to(ORIGIN + RIGHT*2)

        self.play(
            FadeTransform(gamete1_chr, zygote_chr1),
            FadeTransform(gamete2_chr, zygote_chr2),
            FadeOut(gamete1_label, gamete2_label),
            Write(plus_sign), Write(equals_sign),
            Create(zygote_label, shift=UP),
            run_time=2
        )

        self.wait(2)
        self.play(
            FadeOut(title, zygote_chr1, zygote_chr2, zygote_label, plus_sign, equals_sign)
        )
    
    def play_cell_division_beat(self):
        title = Text("Cell Division: Growth & Reproduction", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(0.5)

        # Cell representation
        cell = Circle(radius=2, color=WHITE, stroke_width=3)
        cell_label = Text("Parent Cell (2n)", font_size=28, color=WHITE).next_to(cell, DOWN, buff=0.3)
        self.play(Create(cell), Write(cell_label), run_time=1.5)

        # Chromosomes inside the cell (start as single chromatids for duplication visual)
        chr1 = self.create_single_chromatid(BLUE_ACCENT, scale=0.5).move_to(cell.get_center() + UP*0.5 + LEFT*0.5)
        chr2 = self.create_single_chromatid(GOLD_ACCENT, scale=0.5).move_to(cell.get_center() + DOWN*0.5 + RIGHT*0.5)
        chromosomes = VGroup(chr1, chr2)

        self.play(Create(chromosomes), run_time=1)
        self.wait(0.5)

        # --- Mitosis ---
        mitosis_label = Text("Mitosis (Identical Cells)", font_size=36, color=GREEN_HIGHLIGHT).to_edge(LEFT).shift(UP*2)
        self.play(Write(mitosis_label))
        
        # Chromosomes duplicate
        chr1_dup = self.create_duplicated_chromosome(BLUE_ACCENT, scale=0.5).move_to(chr1.get_center())
        chr2_dup = self.create_duplicated_chromosome(GOLD_ACCENT, scale=0.5).move_to(chr2.get_center())
        
        self.play(
            FadeOut(chr1, chr2), 
            Create(chr1_dup), Create(chr2_dup),
            run_time=1.5
        )
        self.wait(0.5)

        # Alignment at metaphase plate
        metaphase_plate = Line(LEFT*1.5, RIGHT*1.5, color=GREY_BOND).move_to(cell.get_center())
        plate_label = Text("Metaphase Plate", font_size=24, color=GREY_BOND).next_to(metaphase_plate, UP, buff=0.2)
        
        self.play(
            Create(metaphase_plate), Write(plate_label),
            chr1_dup.animate.shift(UP*0.5).set_x(0),
            chr2_dup.animate.shift(DOWN*0.5).set_x(0),
            run_time=1.5
        )
        self.wait(1)

        # Separation of sister chromatids
        pole_top = Dot(UP*1.5, color=WHITE)
        pole_bottom = Dot(DOWN*1.5, color=WHITE)
        
        arrow_top = Arrow(metaphase_plate.get_top(), pole_top.get_bottom(), color=WHITE)
        arrow_bottom = Arrow(metaphase_plate.get_bottom(), pole_bottom.get_top(), color=WHITE)

        self.play(
            Create(pole_top), Create(pole_bottom),
            Create(arrow_top), Create(arrow_bottom),
            FadeOut(metaphase_plate, plate_label),
            run_time=1
        )
        
        split_chr1_a = self.create_single_chromatid(BLUE_ACCENT, scale=0.5).move_to(pole_top.get_center() + DOWN*0.3)
        split_chr1_b = self.create_single_chromatid(BLUE_ACCENT, scale=0.5).move_to(pole_bottom.get_center() + UP*0.3)
        split_chr2_a = self.create_single_chromatid(GOLD_ACCENT, scale=0.5).move_to(pole_top.get_center() + DOWN*0.6)
        split_chr2_b = self.create_single_chromatid(GOLD_ACCENT, scale=0.5).move_to(pole_bottom.get_center() + UP*0.6)

        self.play(
            FadeOut(chr1_dup, chr2_dup), 
            Create(split_chr1_a), Create(split_chr1_b),
            Create(split_chr2_a), Create(split_chr2_b),
            run_time=2
        )
        self.wait(0.5)

        # Cell divides
        cell_left = Circle(radius=1.5, color=WHITE, stroke_width=2).shift(LEFT*3)
        cell_right = Circle(radius=1.5, color=WHITE, stroke_width=2).shift(RIGHT*3)

        self.play(
            ReplacementTransform(cell, VGroup(cell_left, cell_right)),
            FadeOut(cell_label, pole_top, pole_bottom, arrow_top, arrow_bottom),
            split_chr1_a.animate.move_to(cell_left.get_center() + UP*0.3),
            split_chr2_a.animate.move_to(cell_left.get_center() + DOWN*0.3),
            split_chr1_b.animate.move_to(cell_right.get_center() + UP*0.3),
            split_chr2_b.animate.move_to(cell_right.get_center() + DOWN*0.3),
            Write(Text("Daughter Cells (2n)", font_size=24, color=WHITE).next_to(cell_left, DOWN)),
            Write(Text("Daughter Cells (2n)", font_size=24, color=WHITE).next_to(cell_right, DOWN)),
            run_time=2.5
        )
        self.wait(2)
        self.play(FadeOut(*self.mobjects)) 

        # --- Meiosis ---
        meiosis_label = Text("Meiosis (Unique Gametes)", font_size=36, color=RED_HIGHLIGHT).to_edge(RIGHT).shift(UP*2)
        cell_m = Circle(radius=2, color=WHITE, stroke_width=3)
        cell_m_label = Text("Parent Cell (2n)", font_size=28, color=WHITE).next_to(cell_m, DOWN, buff=0.3)
        
        # Start with single chromatids, then duplicate to show duplicated homologous chromosomes
        chr1_m_single = self.create_single_chromatid(BLUE_ACCENT, scale=0.5).move_to(cell_m.get_center() + UP*0.5 + LEFT*0.5)
        chr2_m_single = self.create_single_chromatid(GOLD_ACCENT, scale=0.5).move_to(cell_m.get_center() + DOWN*0.5 + RIGHT*0.5)

        self.play(Create(cell_m), Write(cell_m_label), Create(VGroup(chr1_m_single, chr2_m_single)), Write(meiosis_label), run_time=2)
        self.wait(1)

        # Duplication
        chr1_m_dup = self.create_duplicated_chromosome(BLUE_ACCENT, scale=0.5).move_to(chr1_m_single.get_center())
        chr2_m_dup = self.create_duplicated_chromosome(GOLD_ACCENT, scale=0.5).move_to(chr2_m_single.get_center())
        
        self.play(
            FadeOut(chr1_m_single, chr2_m_single),
            Create(chr1_m_dup), Create(chr2_m_dup),
            run_time=1.5
        )
        self.wait(0.5)

        # Meiosis I: Homologous chromosomes align and separate
        metaphase_plate_m1 = Line(LEFT*1.5, RIGHT*1.5, color=GREY_BOND).move_to(cell_m.get_center())
        plate_label_m1 = Text("Meiosis I Plate", font_size=24, color=GREY_BOND).next_to(metaphase_plate_m1, UP, buff=0.2)
        
        self.play(
            Create(metaphase_plate_m1), Write(plate_label_m1),
            chr1_m_dup.animate.shift(LEFT*0.5), # Align homologous pairs
            chr2_m_dup.animate.shift(RIGHT*0.5),
            run_time=1.5
        )
        self.wait(1)

        # Separation of homologous chromosomes
        cell_m1_left = Circle(radius=1.5, color=WHITE, stroke_width=2).shift(LEFT*3)
        cell_m1_right = Circle(radius=1.5, color=WHITE, stroke_width=2).shift(RIGHT*3)
        
        self.play(
            ReplacementTransform(cell_m, VGroup(cell_m1_left, cell_m1_right)),
            FadeOut(cell_m_label, metaphase_plate_m1, plate_label_m1),
            chr1_m_dup.animate.move_to(cell_m1_left.get_center()), # Entire duplicated chromosome moves to one cell
            chr2_m_dup.animate.move_to(cell_m1_right.get_center()), # Entire duplicated chromosome moves to other cell
            run_time=2
        )
        self.wait(1)

        # Meiosis II: Sister chromatids separate
        # New "daughter cells" from Meiosis I are now parent cells for Meiosis II
        metaphase_plate_m2_left = Line(LEFT*0.7, RIGHT*0.7, color=GREY_BOND).move_to(cell_m1_left.get_center())
        metaphase_plate_m2_right = Line(LEFT*0.7, RIGHT*0.7, color=GREY_BOND).move_to(cell_m1_right.get_center())
        plate_label_m2 = Text("Meiosis II Plate", font_size=24, color=GREY_BOND).next_to(metaphase_plate_m2_left, UP, buff=0.2).set_x(0)

        self.play(
            Create(metaphase_plate_m2_left), Create(metaphase_plate_m2_right), Write(plate_label_m2),
            chr1_m_dup.animate.move_to(cell_m1_left.get_center()),
            chr2_m_dup.animate.move_to(cell_m1_right.get_center()),
            run_time=1.5
        )
        self.wait(1)

        # Separation of sister chromatids
        gamete_cell_1 = Circle(radius=1, color=WHITE, stroke_width=1).shift(LEFT*4.5 + DOWN*2)
        gamete_cell_2 = Circle(radius=1, color=WHITE, stroke_width=1).shift(LEFT*1.5 + DOWN*2)
        gamete_cell_3 = Circle(radius=1, color=WHITE, stroke_width=1).shift(RIGHT*1.5 + DOWN*2)
        gamete_cell_4 = Circle(radius=1, color=WHITE, stroke_width=1).shift(RIGHT*4.5 + DOWN*2)

        final_chr1_a = self.create_single_chromatid(BLUE_ACCENT, scale=0.5).move_to(gamete_cell_1.get_center())
        final_chr1_b = self.create_single_chromatid(BLUE_ACCENT, scale=0.5).move_to(gamete_cell_2.get_center())
        final_chr2_a = self.create_single_chromatid(GOLD_ACCENT, scale=0.5).move_to(gamete_cell_3.get_center())
        final_chr2_b = self.create_single_chromatid(GOLD_ACCENT, scale=0.5).move_to(gamete_cell_4.get_center())

        self.play(
            ReplacementTransform(cell_m1_left, VGroup(gamete_cell_1, gamete_cell_2)),
            ReplacementTransform(cell_m1_right, VGroup(gamete_cell_3, gamete_cell_4)),
            FadeOut(metaphase_plate_m2_left, metaphase_plate_m2_right, plate_label_m2),
            FadeOut(chr1_m_dup, chr2_m_dup), 
            Create(final_chr1_a), Create(final_chr1_b),
            Create(final_chr2_a), Create(final_chr2_b),
            Write(Text("Gametes (n)", font_size=20, color=WHITE).next_to(gamete_cell_1, DOWN)),
            Write(Text("Gametes (n)", font_size=20, color=WHITE).next_to(gamete_cell_2, DOWN)),
            Write(Text("Gametes (n)", font_size=20, color=WHITE).next_to(gamete_cell_3, DOWN)),
            Write(Text("Gametes (n)", font_size=20, color=WHITE).next_to(gamete_cell_4, DOWN)),
            run_time=3
        )
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

    def play_recap_card(self):
        recap_title = Text("Recap: DNA, Inheritance, Cell Division", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(recap_title))

        points = VGroup(
            Text("• DNA: The blueprint of life, a double helix.", font_size=36, color=BLUE_ACCENT),
            Text("• Inheritance: Passing traits via chromosomes in gametes.", font_size=36, color=GOLD_ACCENT),
            Text("• Mitosis: Produces identical body cells (2n → 2n).", font_size=36, color=GREEN_HIGHLIGHT),
            Text("• Meiosis: Produces unique gametes (2n → n).", font_size=36, color=RED_HIGHLIGHT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).next_to(recap_title, DOWN, buff=1)

        self.play(LaggedStart(*[Write(p) for p in points], lag_ratio=0.7), run_time=5)
        self.wait(3)

        farewell = Text("Continue your journey!", font_size=40, color=WHITE).to_edge(DOWN)
        self.play(Write(farewell))
        self.wait(2)