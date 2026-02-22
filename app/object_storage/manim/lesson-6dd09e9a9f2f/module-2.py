from manim import *

class GeneticsDNA(Scene):
    def construct(self):
        # 1. Configuration: Dark background, high-contrast blue and gold
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E

        # Initial Title (Visual Hook Setup)
        title = MathTex(r"\text{Genetics, DNA, \& Cell Division}", color=BLUE_ACCENT).scale(1.5).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Beat 1: DNA Structure - The Code of Life (~8-10 seconds)
        # Strong visual hook: Scattered bases then forming a double helix

        # Start with abstract bases
        atcg_bases = VGroup(
            MathTex("A", color=BLUE_ACCENT), MathTex("T", color=BLUE_ACCENT),
            MathTex("C", color=GOLD_ACCENT), MathTex("G", color=GOLD_ACCENT)
        ).arrange_in_grid(rows=2, cols=2, buff=1.0).scale(1.5).shift(UP*0.5)

        dna_blueprint_text = MathTex(r"\text{DNA: The Blueprint of Life}", color=BLUE_ACCENT).scale(1.2).to_edge(UP)

        self.play(
            FadeTransform(title, dna_blueprint_text),
            FadeIn(atcg_bases, shift=UP),
            run_time=1.5
        )
        self.wait(0.5)

        # Create the double helix structure using FunctionGraph for smooth curves
        helix_path1 = FunctionGraph(lambda x: 0.8 * np.sin(x), x_range=[-3.5, 3.5], color=BLUE_ACCENT, stroke_width=4).rotate(PI/2).scale_to_fit_height(5).center()
        helix_path2 = FunctionGraph(lambda x: 0.8 * np.sin(x + PI), x_range=[-3.5, 3.5], color=GOLD_ACCENT, stroke_width=4).rotate(PI/2).scale_to_fit_height(5).center()
        
        num_cross_bars = 18
        cross_bars_mobj = VGroup()
        for i in range(num_cross_bars):
            t = i / (num_cross_bars - 1)
            point1 = helix_path1.point_from_proportion(t)
            point2 = helix_path2.point_from_proportion(t)
            bar = Line(point1, point2, color=GREY_A, stroke_width=1.5)
            
            # Add base letters, alternating A-T and C-G for visual representation
            base_pair_text = VGroup()
            if i % 2 == 0: # A-T pair
                base_pair_text.add(MathTex("A", color=WHITE).move_to(point1).shift(0.1*LEFT*np.cos(t*PI)).scale(0.5))
                base_pair_text.add(MathTex("T", color=WHITE).move_to(point2).shift(0.1*RIGHT*np.cos(t*PI)).scale(0.5))
            else: # C-G pair
                base_pair_text.add(MathTex("C", color=WHITE).move_to(point1).shift(0.1*LEFT*np.cos(t*PI)).scale(0.5))
                base_pair_text.add(MathTex("G", color=WHITE).move_to(point2).shift(0.1*RIGHT*np.cos(t*PI)).scale(0.5))
            
            cross_bars_mobj.add(VGroup(bar, base_pair_text)) # Group bar and text
            
        dna_helix = VGroup(helix_path1, helix_path2, cross_bars_mobj).scale(0.7)
        dna_helix.center().to_edge(LEFT, buff=1) # Position for subsequent beats
        
        self.play(
            FadeOut(atcg_bases),
            Create(helix_path1),
            Create(helix_path2),
            LaggedStart(*[FadeIn(bar) for bar in cross_bars_mobj], lag_ratio=0.05),
            run_time=3.5
        )
        self.wait(1.5)
        
        # Beat 2: Genes - Instructions for Traits (~8-10 seconds)
        gene_title = MathTex(r"\text{Genes: Instructions for Traits}", color=BLUE_ACCENT).scale(1.2).to_edge(UP)

        gene_highlight = Rectangle(
            width=dna_helix[0].get_width() + 0.5,
            height=dna_helix[0].get_height()/4,
            color=RED_E,
            stroke_width=3
        ).move_to(dna_helix[0].point_from_proportion(0.3)).set_opacity(0.5)

        gene_label = MathTex(r"\text{Gene Region}", color=RED_E).next_to(gene_highlight, RIGHT, buff=0.5)
        
        trait_square = Square(side_length=1.5, color=GREEN_E, fill_opacity=0.5).to_edge(RIGHT, buff=1.5).shift(UP*0.5)
        trait_text = MathTex(r"\text{Trait (e.g., eye color)}", color=GREEN_E).next_to(trait_square, UP)

        self.play(
            FadeTransform(dna_blueprint_text, gene_title),
            dna_helix.animate.shift(LEFT*1.5), # Make space for trait
            Create(gene_highlight),
            Write(gene_label)
        )
        self.wait(1)

        arrow_gene_trait = Arrow(gene_highlight.get_right(), trait_square.get_left(), buff=0.2, color=WHITE)

        self.play(
            GrowFromCenter(trait_square),
            Write(trait_text),
            Create(arrow_gene_trait)
        )
        self.wait(2)

        # Beat 3: Cell Division (Mitosis) - Copying the Blueprint (~8-10 seconds)
        mitosis_title = MathTex(r"\text{Mitosis: Copying the Blueprint}", color=BLUE_ACCENT).scale(1.2).to_edge(UP)

        self.play(
            FadeOut(gene_highlight),
            FadeOut(gene_label),
            FadeOut(trait_square),
            FadeOut(trait_text),
            FadeOut(arrow_gene_trait),
            FadeTransform(gene_title, mitosis_title),
            dna_helix.animate.scale(1.2).center(), # Re-center and slightly enlarge
            run_time=1
        )
        self.wait(0.5)

        # Abstract chromosome as a single line
        chromosome_single = Line(ORIGIN, UP*2, stroke_width=8, color=BLUE_ACCENT).center()
        chrom_label = MathTex(r"\text{Chromosome}", color=WHITE).next_to(chromosome_single, DOWN, buff=0.3)
        
        self.play(
            ReplacementTransform(dna_helix, chromosome_single), # Abstract helix into a single chromosome representation
            Write(chrom_label)
        )
        self.wait(1)

        # Replication: single chromosome duplicates into two sister chromatids (parallel lines)
        chromosome_replicated_left = Line(ORIGIN, UP*2, stroke_width=8, color=BLUE_ACCENT).shift(LEFT*0.2)
        chromosome_replicated_right = Line(ORIGIN, UP*2, stroke_width=8, color=BLUE_ACCENT).shift(RIGHT*0.2)
        replicated_chromosomes = VGroup(chromosome_replicated_left, chromosome_replicated_right).center()

        self.play(
            Transform(chromosome_single, replicated_chromosomes), # single line becomes two parallel lines
            chrom_label.animate.next_to(replicated_chromosomes, DOWN, buff=0.3)
        )
        self.wait(1)

        # Cell division: the two sister chromatids separate into two new cells
        cell1 = Circle(radius=1.5, color=GREY_A, stroke_width=2).shift(LEFT*3)
        cell2 = Circle(radius=1.5, color=GREY_A, stroke_width=2).shift(RIGHT*3)
        
        # The separated chromosomes in new cells (back to single line representation)
        chrom1_in_cell1 = Line(ORIGIN, UP*2, stroke_width=8, color=BLUE_ACCENT).move_to(cell1.get_center())
        chrom2_in_cell2 = Line(ORIGIN, UP*2, stroke_width=8, color=BLUE_ACCENT).move_to(cell2.get_center())
        
        self.play(
            Transform(replicated_chromosomes[0], chrom1_in_cell1), 
            Transform(replicated_chromosomes[1], chrom2_in_cell2), 
            Create(cell1),
            Create(cell2),
            FadeOut(chrom_label),
            run_time=2
        )
        
        cell_label1 = MathTex(r"\text{New Cell 1}", color=WHITE).next_to(cell1, DOWN)
        cell_label2 = MathTex(r"\text{New Cell 2}", color=WHITE).next_to(cell2, DOWN)
        
        self.play(
            Write(cell_label1),
            Write(cell_label2)
        )
        self.wait(2)

        # Beat 4: Inheritance - Combining Blueprints (~8-10 seconds)
        inheritance_title = MathTex(r"\text{Inheritance: Combining Blueprints}", color=BLUE_ACCENT).scale(1.2).to_edge(UP)

        self.play(
            FadeOut(cell1), FadeOut(cell2),
            FadeOut(chrom1_in_cell1), FadeOut(chrom2_in_cell2),
            FadeOut(cell_label1), FadeOut(cell_label2),
            FadeTransform(mitosis_title, inheritance_title),
            run_time=1
        )
        
        # Parent DNA segments (simplified alleles as rectangles with letters)
        parent1_gene = VGroup(
            Rectangle(width=0.8, height=2, color=BLUE_ACCENT, fill_opacity=0.8),
            MathTex("A", color=WHITE)
        ).arrange(RIGHT, buff=0.2).move_to(LEFT*3 + UP*1.5) 
        
        parent2_gene = VGroup(
            Rectangle(width=0.8, height=2, color=GOLD_ACCENT, fill_opacity=0.8),
            MathTex("a", color=WHITE)
        ).arrange(RIGHT, buff=0.2).move_to(RIGHT*3 + UP*1.5) 

        parent1_label = MathTex(r"\text{Parent 1 (Allele A)}", color=BLUE_ACCENT).next_to(parent1_gene, UP)
        parent2_label = MathTex(r"\text{Parent 2 (Allele a)}", color=GOLD_ACCENT).next_to(parent2_gene, UP)

        self.play(
            FadeIn(parent1_gene, shift=UP), Write(parent1_label),
            FadeIn(parent2_gene, shift=UP), Write(parent2_label)
        )
        self.wait(1)

        # Show contribution and offspring formation
        arrow_p1 = Arrow(parent1_gene.get_bottom(), ORIGIN + DOWN*0.5 + LEFT*1.0, buff=0.2, color=WHITE)
        arrow_p2 = Arrow(parent2_gene.get_bottom(), ORIGIN + DOWN*0.5 + RIGHT*1.0, buff=0.2, color=WHITE)
        
        # Child DNA (heterozygous) by combining parent contributions
        child_gene = VGroup(
            Rectangle(width=0.8, height=2, color=BLUE_ACCENT, fill_opacity=0.4), # half from parent 1
            Rectangle(width=0.8, height=2, color=GOLD_ACCENT, fill_opacity=0.4),  # half from parent 2
        ).arrange(RIGHT, buff=0.01).center().shift(DOWN*1.5) 

        child_alleles = VGroup(
            MathTex("A", color=WHITE).move_to(child_gene[0].get_center()),
            MathTex("a", color=WHITE).move_to(child_gene[1].get_center())
        )
        
        child_gene_full = VGroup(child_gene, child_alleles)
        
        child_label = MathTex(r"\text{Offspring (Genotype Aa)}", color=WHITE).next_to(child_gene_full, DOWN)

        self.play(
            Create(arrow_p1), Create(arrow_p2),
            run_time=1
        )
        self.play(
            ReplacementTransform(parent1_gene.copy(), child_gene[0]), # Visual contribution
            ReplacementTransform(parent2_gene.copy(), child_gene[1]), # Visual contribution
            FadeIn(child_alleles),
            Write(child_label),
            FadeOut(parent1_gene), FadeOut(parent2_gene),
            FadeOut(parent1_label), FadeOut(parent2_label),
            FadeOut(arrow_p1), FadeOut(arrow_p2)
        )
        self.wait(2)

        # Recap Card
        self.play(
            FadeOut(child_gene_full), FadeOut(child_label),
            FadeOut(inheritance_title),
            run_time=1
        )

        recap_title = MathTex(r"\text{Recap: Key Concepts}", color=BLUE_ACCENT).scale(1.4).to_edge(UP)
        
        recap_points = VGroup(
            MathTex(r"\bullet \textbf{DNA}: \text{The genetic blueprint (A, T, C, G)}", color=WHITE),
            MathTex(r"\bullet \textbf{Genes}: \text{Segments of DNA coding for traits}", color=WHITE),
            MathTex(r"\bullet \textbf{Mitosis}: \text{Cell division for exact DNA copies}", color=WHITE),
            MathTex(r"\bullet \textbf{Inheritance}: \text{Offspring get genes from parents}", color=WHITE)
        ).arrange(DOWN, buff=0.8, aligned_edge=LEFT).scale(0.9).next_to(recap_title, DOWN, buff=1)

        self.play(
            Write(recap_title)
        )
        self.play(
            LaggedStart(*[FadeIn(point, shift=UP) for point in recap_points], lag_ratio=0.5),
            run_time=4
        )
        self.wait(3)