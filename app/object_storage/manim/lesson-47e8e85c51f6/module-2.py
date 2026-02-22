from manim import *

class GeneticCodeAnimation(Scene):
    def construct(self):
        # 1. Configuration: Clean dark background, high-contrast blue and gold
        config.background_color = BLACK
        blue_color = BLUE_C
        gold_color = GOLD_C
        
        # --- Beat 1: The Blueprint of Life (DNA as Code) ---
        # Strong visual hook: Abstract DNA strands forming
        dna_bases_char = ["A", "T", "C", "G"]
        dna_base_colors = {
            "A": blue_color, "T": gold_color,
            "C": BLUE_E, "G": GOLD_E, # Slightly different shades for variety
        }
        
        scattered_bases = VGroup()
        for i in range(30):
            base_char = random.choice(dna_bases_char)
            base = MathTex(base_char, color=dna_base_colors[base_char]).scale(0.7)
            base.move_to(self.camera.frame.get_random_point() * 0.8)
            scattered_bases.add(base)
            
        self.play(LaggedStart(*[FadeIn(b, shift=UR*0.1) for b in scattered_bases]), run_time=1.5)
        self.wait(0.5)

        # Form a simplified DNA ladder structure
        strand1_chars = "ATGCATGCATGCGTAGCTGA"
        strand2_chars = "TACGTACGTAGCATCGACT" # Complementary strand
        
        strand1_mobjects = VGroup()
        strand2_mobjects = VGroup()

        for i, char in enumerate(strand1_chars):
            mobj = MathTex(char, color=dna_base_colors[char]).scale(0.7)
            strand1_mobjects.add(mobj)
            
        for i, char in enumerate(strand2_chars):
            mobj = MathTex(char, color=dna_base_colors[char]).scale(0.7)
            strand2_mobjects.add(mobj)

        strand1_mobjects.arrange(DOWN, buff=0.4).shift(LEFT * 1.5)
        strand2_mobjects.arrange(DOWN, buff=0.4).shift(RIGHT * 1.5)
        
        # Align bases for pairing
        for i in range(min(len(strand1_mobjects), len(strand2_mobjects))):
            strand2_mobjects[i].next_to(strand1_mobjects[i], RIGHT, buff=2.0)
            
        dna_ladder_bases = VGroup(strand1_mobjects, strand2_mobjects)
        
        self.play(
            scattered_bases.animate.set_opacity(0), # Fade out scattered bases
            ReplacementTransform(scattered_bases.copy(), dna_ladder_bases), # Transition to ladder
            run_time=1.5
        )
        self.wait(0.5)

        # Add connecting lines (hydrogen bonds)
        lines = VGroup()
        for i in range(min(len(strand1_mobjects), len(strand2_mobjects))):
            line = Line(strand1_mobjects[i].get_right(), strand2_mobjects[i].get_left(), color=GREY_A, stroke_width=2)
            lines.add(line)
        
        self.play(Create(lines), run_time=1)
        
        dna_mobj = VGroup(dna_ladder_bases, lines).scale(0.6).center()
        
        title1 = Text("DNA: The Blueprint of Life", color=gold_color).to_edge(UP).scale(0.7)
        self.play(FadeIn(title1, shift=UP))
        self.play(dna_mobj.animate.shift(LEFT * 3), run_time=1)

        # Emphasize DNA as information
        info_text = MathTex(r"\text{Information} \rightarrow \text{Instructions}", color=blue_color).next_to(dna_mobj, RIGHT, buff=1.0)
        arrow = Arrow(dna_mobj.get_right(), info_text.get_left(), buff=0.2, color=gold_color)
        
        self.play(FadeIn(info_text, shift=RIGHT), Create(arrow), run_time=1)
        self.wait(1)
        self.play(FadeOut(title1), FadeOut(info_text), FadeOut(arrow), dna_mobj.animate.scale(0.8).to_edge(LEFT).shift(UP*1.5))
        
        # --- Beat 2: The Genetic Code (Codons) ---
        title2 = Text("The Genetic Code: Codons", color=gold_color).to_edge(UP).scale(0.7)
        self.play(FadeIn(title2, shift=UP))
        
        # Isolate one strand for simplicity and highlight triplets
        single_strand = VGroup(*[m for m in strand1_mobjects]).copy().arrange(DOWN, buff=0.4).scale(0.7).move_to(ORIGIN)
        self.play(
            dna_mobj.animate.scale(0.5).to_corner(UL), # Keep DNA in corner for context
            FadeTransform(dna_mobj, single_strand.copy().to_corner(UL).set_opacity(0.3)), # keep small faded reference
            ReplacementTransform(dna_mobj, single_strand.move_to(LEFT * 3)),
            run_time=1.5
        )

        # Highlight codons (triplets)
        codons_mobj = VGroup()
        # Ensure we don't go out of bounds for the single_strand
        num_codons = len(single_strand) // 3
        for i in range(num_codons):
            codon_group = VGroup(*single_strand[i*3 : (i+1)*3])
            codons_mobj.add(codon_group)
            
        codon_rects = VGroup()
        for i, codon_group in enumerate(codons_mobj):
            rect = SurroundingRectangle(codon_group, color=blue_color, buff=0.1)
            codon_rects.add(rect)
            
        self.play(LaggedStart(*[Create(rect) for rect in codon_rects], lag_ratio=0.2), run_time=1.5)
        self.wait(0.5)

        codon_label = Text("Each triplet is a 'codon'", color=gold_color).next_to(codons_mobj[0], RIGHT, buff=1.0)
        self.play(FadeIn(codon_label, shift=RIGHT), run_time=0.8)
        self.wait(0.5)

        # Show codon mapping (abstractly)
        mapping_title = Text("Codons Map to Amino Acids", color=gold_color).next_to(title2, DOWN).scale(0.6)
        self.play(FadeIn(mapping_title))
        
        # Simple 3x2 grid for mapping using MobjectMatrix
        codon_map_grid = MobjectMatrix(
            [
                [MathTex(r"\text{AUG}", color=blue_color), MathTex(r"\text{Methionine}", color=gold_color)],
                [MathTex(r"\text{UUA}", color=blue_color), MathTex(r"\text{Leucine}", color=gold_color)],
                [MathTex(r"\text{GCU}", color=blue_color), MathTex(r"\text{Alanine}", color=gold_color)],
            ],
            h_buff=1.5, v_buff=0.8,
            left_bracket=MathTex(r"\begin{pmatrix}", color=GREY_A),
            right_bracket=MathTex(r"\end{pmatrix}", color=GREY_A),
        )
        codon_map_grid.scale(0.6).next_to(single_strand, RIGHT, buff=1.5)

        self.play(FadeIn(codon_map_grid, shift=RIGHT), run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(title2), FadeOut(codon_label), FadeOut(mapping_title),
            FadeOut(codon_rects),
            single_strand.animate.scale(0.5).to_corner(UL).set_opacity(0.3), # keep small faded reference
            codon_map_grid.animate.scale(0.7).to_corner(UR)
        )
        
        # --- Beat 3: From Gene to Protein (Simplified) ---
        title3 = Text("From Gene to Protein", color=gold_color).to_edge(UP).scale(0.7)
        self.play(FadeIn(title3, shift=UP))

        # DNA Gene (simplified as a segment)
        gene_dna = Rectangle(width=4, height=0.5, color=blue_color, fill_opacity=0.3, stroke_width=2)
        gene_label = Text("Gene (DNA)", color=blue_color).next_to(gene_dna, LEFT, buff=0.3).scale(0.5)
        gene_group = VGroup(gene_dna, gene_label).move_to(LEFT * 3 + UP * 1.5)
        self.play(Create(gene_group))
        self.wait(0.5)

        # Transcription: DNA -> mRNA
        transcription_arrow = Arrow(gene_dna.get_right(), gene_dna.get_right() + RIGHT*2, buff=0.1, color=gold_color)
        transcription_text = Text("Transcription", color=gold_color).next_to(transcription_arrow, UP, buff=0.1).scale(0.5)

        mRNA_strand = Rectangle(width=3.5, height=0.4, color=YELLOW_C, fill_opacity=0.5, stroke_width=2)
        mRNA_label = Text("mRNA", color=YELLOW_C).next_to(mRNA_strand, RIGHT, buff=0.3).scale(0.5)
        mRNA_group = VGroup(mRNA_strand, mRNA_label).next_to(gene_group, DOWN, buff=1.0).align_to(gene_group, LEFT)
        
        self.play(Create(transcription_arrow), FadeIn(transcription_text, shift=UP))
        self.play(TransformFromCopy(gene_dna, mRNA_group), run_time=1.5)
        self.wait(0.5)

        # Translation: mRNA -> Protein
        translation_arrow = Arrow(mRNA_strand.get_right(), mRNA_strand.get_right() + RIGHT*2, buff=0.1, color=gold_color)
        translation_text = Text("Translation", color=gold_color).next_to(translation_arrow, UP, buff=0.1).scale(0.5)

        protein_chain = VGroup(*[
            Rectangle(width=0.3, height=0.3, color=random_bright_color(), fill_opacity=0.7) for _ in range(7)
        ]).arrange(RIGHT, buff=0.1)
        protein_chain.scale(0.8)
        protein_label = Text("Protein", color=GREY_A).next_to(protein_chain, RIGHT, buff=0.3).scale(0.5)
        protein_group = VGroup(protein_chain, protein_label).next_to(mRNA_group, DOWN, buff=1.0).align_to(mRNA_group, LEFT)

        self.play(Create(translation_arrow), FadeIn(translation_text, shift=UP))
        self.play(TransformFromCopy(mRNA_strand, protein_group), run_time=1.5)
        self.wait(1)

        central_dogma = MathTex(r"\text{DNA} \rightarrow \text{RNA} \rightarrow \text{Protein}", color=gold_color).scale(0.8).next_to(protein_group, DOWN, buff=0.8)
        self.play(Write(central_dogma))
        self.wait(1.5)

        self.play(
            FadeOut(title3), FadeOut(transcription_arrow), FadeOut(transcription_text),
            FadeOut(translation_arrow), FadeOut(translation_text),
            FadeOut(gene_group), FadeOut(mRNA_group), FadeOut(protein_group),
            FadeOut(central_dogma),
            FadeOut(single_strand), FadeOut(codon_map_grid)
        )
        
        # --- Beat 4: Passing on Traits (Inheritance) ---
        title4 = Text("Inheritance: Passing on Traits", color=gold_color).to_edge(UP).scale(0.7)
        self.play(FadeIn(title4, shift=UP))

        # Parent 1 (Blue)
        parent1 = Circle(radius=1.0, color=blue_color, fill_opacity=0.5).shift(LEFT * 3 + UP * 0.5)
        p1_label = Text("Parent 1", color=blue_color).next_to(parent1, DOWN).scale(0.6)
        
        # Parent 2 (Gold)
        parent2 = Circle(radius=1.0, color=gold_color, fill_opacity=0.5).shift(RIGHT * 3 + UP * 0.5)
        p2_label = Text("Parent 2", color=gold_color).next_to(parent2, DOWN).scale(0.6)
        
        self.play(Create(parent1), FadeIn(p1_label), Create(parent2), FadeIn(p2_label))
        self.wait(0.5)

        # Represent genes/alleles (simple shapes/colors)
        gene_p1_a = Square(side_length=0.4, color=BLUE_D, fill_opacity=1).move_to(parent1.get_center() + UL * 0.3)
        gene_p1_b = Square(side_length=0.4, color=BLUE_A, fill_opacity=1).move_to(parent1.get_center() + DR * 0.3)
        genes_p1 = VGroup(gene_p1_a, gene_p1_b)

        gene_p2_a = Square(side_length=0.4, color=GOLD_D, fill_opacity=1).move_to(parent2.get_center() + UL * 0.3)
        gene_p2_b = Square(side_length=0.4, color=GOLD_A, fill_opacity=1).move_to(parent2.get_center() + DR * 0.3)
        genes_p2 = VGroup(gene_p2_a, gene_p2_b)
        
        self.play(FadeIn(genes_p1), FadeIn(genes_p2))
        self.wait(0.5)

        # Offspring with combined genes (abstract Punnett Square idea)
        
        # Simulate passing one gene from each parent
        gene_from_p1_copy = gene_p1_a.copy().set_opacity(0.8)
        gene_from_p2_copy = gene_p2_b.copy().set_opacity(0.8)
        
        offspring_circle = Circle(radius=0.8, color=GREY_B, fill_opacity=0.5).move_to(ORIGIN + DOWN*2)
        offspring_label = Text("Offspring", color=GREY_A).next_to(offspring_circle, DOWN).scale(0.6)

        arrow1_path = ArcBetweenPoints(parent1.get_bottom(), offspring_circle.get_top(), angle=-PI/3)
        arrow2_path = ArcBetweenPoints(parent2.get_bottom(), offspring_circle.get_top(), angle=PI/3)

        self.play(
            Create(offspring_circle),
            FadeIn(offspring_label),
            MoveAlongPath(gene_from_p1_copy, arrow1_path, rate_func=linear, run_time=1.5),
            MoveAlongPath(gene_from_p2_copy, arrow2_path, rate_func=linear, run_time=1.5),
        )
        # Position the copies inside the offspring circle
        self.play(
            gene_from_p1_copy.animate.move_to(offspring_circle.get_center() + LEFT*0.2 + UP*0.2),
            gene_from_p2_copy.animate.move_to(offspring_circle.get_center() + RIGHT*0.2 + DOWN*0.2),
            run_time=0.5
        )
        self.wait(1)

        # Traits are passed text
        inheritance_text = Text("Traits are passed through genes!", color=gold_color).next_to(offspring_circle, UP, buff=1.0)
        self.play(FadeIn(inheritance_text, shift=UP))
        self.wait(1.5)

        self.play(
            FadeOut(title4), FadeOut(parent1), FadeOut(p1_label), FadeOut(genes_p1),
            FadeOut(parent2), FadeOut(p2_label), FadeOut(genes_p2),
            FadeOut(offspring_circle), FadeOut(offspring_label),
            FadeOut(gene_from_p1_copy), FadeOut(gene_from_p2_copy), FadeOut(inheritance_text)
        )

        # --- Recap Card ---
        recap_title = Text("Recap: Genetic Code & Inheritance", color=gold_color).to_edge(UP).scale(0.8)
        
        recap_points = VGroup(
            Text("1. DNA is the blueprint for life.", color=blue_color).scale(0.6),
            Text("2. Codons (triplets) map to amino acids.", color=blue_color).scale(0.6),
            Text("3. DNA -> RNA -> Protein (Central Dogma).", color=blue_color).scale(0.6),
            Text("4. Genes pass traits from parents to offspring.", color=blue_color).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).center()
        
        self.play(FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(*[Write(point) for point in recap_points], lag_ratio=0.7), run_time=3)
        self.wait(3)
        self.play(FadeOut(recap_title), FadeOut(recap_points))