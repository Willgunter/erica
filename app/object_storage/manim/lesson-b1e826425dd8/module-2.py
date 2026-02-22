from manim import *

class GeneticsIntro(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = "#1A1A1A"  # Very dark gray
        blue_color = "#00AADD"
        gold_color = "#FFD700"
        text_color = WHITE
        
        # --- Beat 1: The Blueprint - DNA (Visual Hook & Core Concept) ---
        self.camera.background_color = config.background_color # Ensure scene background matches config

        # Visual Hook: Abstract DNA Double Helix
        # Create two parametric curves for the helix backbones
        amplitude = 0.8
        wavelength = 2.0
        y_offset = -0.5
        
        helix1 = ParametricFunction(
            lambda t: np.array([
                amplitude * np.cos(t * wavelength),
                t + y_offset,
                amplitude * np.sin(t * wavelength)
            ]), t_range=[-3, 3], color=blue_color, stroke_width=4
        )
        
        helix2 = ParametricFunction(
            lambda t: np.array([
                amplitude * np.cos(t * wavelength + PI), # Offset by PI for second strand
                t + y_offset,
                amplitude * np.sin(t * wavelength + PI)
            ]), t_range=[-3, 3], color=gold_color, stroke_width=4
        )

        # Scale and rotate the helices
        helix1.scale(0.8).rotate(PI/2, axis=UP, about_point=ORIGIN).shift(UP*0.5)
        helix2.scale(0.8).rotate(PI/2, axis=UP, about_point=ORIGIN).shift(UP*0.5)

        # Create base pairs as lines connecting the helices at intervals
        base_pairs = VGroup()
        for t in np.linspace(-3, 3, 20):
            # Calculate points for each strand at current 't'
            p1 = np.array([amplitude * np.cos(t * wavelength), t + y_offset, amplitude * np.sin(t * wavelength)])
            p2 = np.array([amplitude * np.cos(t * wavelength + PI), t + y_offset, amplitude * np.sin(t * wavelength + PI)])
            
            # Apply the same scaling and rotation as the helices to the points
            # For 3D points, use a rotation matrix or np.dot with a rotation matrix
            # For simplicity in ManimCE (2D projection), we can roughly position or rotate the lines
            # A more robust way would be to create dummy Mobjects at the points and get their screen coordinates
            # For this simple visual, we'll apply a conceptual rotation to the points
            
            # Simplified rotation for visualization in 2D projection
            # Assume the rotation causes points to effectively shift horizontally
            rotated_p1_x = p1[0] * np.cos(PI/2) - p1[2] * np.sin(PI/2) # Rotate around Y axis
            rotated_p1_z = p1[0] * np.sin(PI/2) + p1[2] * np.cos(PI/2)
            rotated_p1 = np.array([rotated_p1_x, p1[1], rotated_p1_z]) * 0.8 + UP*0.5 # Scale and shift

            rotated_p2_x = p2[0] * np.cos(PI/2) - p2[2] * np.sin(PI/2)
            rotated_p2_z = p2[0] * np.sin(PI/2) + p2[2] * np.cos(PI/2)
            rotated_p2 = np.array([rotated_p2_x, p2[1], rotated_p2_z]) * 0.8 + UP*0.5

            bp = Line(rotated_p1, rotated_p2, color=WHITE, stroke_width=2)
            base_pairs.add(bp)

        dna_model = VGroup(helix1, helix2, base_pairs)

        title = Text("Fundamentals of Genetics and DNA", color=WHITE, font_size=48).to_edge(UP)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(0.5)

        self.play(Create(dna_model, run_time=2))
        self.wait(0.5)

        dna_text = Text("DNA: The Blueprint of Life", color=gold_color, font_size=36).next_to(dna_model, DOWN, buff=0.7)
        self.play(Write(dna_text))
        self.wait(1)

        # Show a segment of DNA with bases (A, T, G, C)
        # Simulate base pairs with MathTex
        base_a = MathTex("A", color=BLUE).scale(0.8)
        base_t = MathTex("T", color=GOLD).scale(0.8)
        base_g = MathTex("G", color=BLUE).scale(0.8)
        base_c = MathTex("C", color=GOLD).scale(0.8)
        
        pair1 = VGroup(base_a.copy(), base_t.copy()).arrange(RIGHT, buff=0.8)
        pair2 = VGroup(base_g.copy(), base_c.copy()).arrange(RIGHT, buff=0.8)
        pair3 = VGroup(base_c.copy(), base_g.copy()).arrange(RIGHT, buff=0.8)
        pair4 = VGroup(base_t.copy(), base_a.copy()).arrange(RIGHT, buff=0.8)

        dna_ladder_tex = VGroup(pair1, pair2, pair3, pair4).arrange(DOWN, buff=0.3)
        dna_ladder_tex.move_to(RIGHT*3.5)

        arrow_to_bases = Arrow(dna_model.get_right(), dna_ladder_tex.get_left(), buff=0.1, color=WHITE)
        
        info_label = Text("Genetic Information Encoded", color=WHITE, font_size=28).next_to(dna_ladder_tex, UP, buff=0.5)
        
        self.play(
            FadeOut(dna_text, shift=DOWN),
            dna_model.animate.scale(0.6).shift(LEFT*2.5 + UP*0.5),
            run_time=1
        )
        self.play(
            Create(arrow_to_bases),
            LaggedStart(*[FadeIn(b, shift=RIGHT) for b in dna_ladder_tex], lag_ratio=0.1),
            Write(info_label),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 2: Genes & Chromosomes (Structure & Location) ---
        self.play(
            FadeOut(arrow_to_bases, info_label),
            FadeOut(dna_ladder_tex),
            dna_model.animate.scale(0.8).to_edge(LEFT, buff=0.5).shift(UP*1.5),
            run_time=1
        )

        # Represent a Chromosome (X-shape)
        chromosome_x = VGroup(
            Line(UP*1.5 + LEFT*0.5, DOWN*1.5 + RIGHT*0.5, color=blue_color, stroke_width=8),
            Line(UP*1.5 + RIGHT*0.5, DOWN*1.5 + LEFT*0.5, color=blue_color, stroke_width=8)
        )
        chromosome_x.scale(0.6).next_to(dna_model, RIGHT, buff=2) # Arrange next to DNA
        
        # Add genes as highlighted segments on the chromosome
        gene1_rect = Rectangle(width=0.4, height=0.6, color=gold_color, fill_opacity=0.7, stroke_width=0)
        gene1_rect.move_to(chromosome_x.get_center() + UP*0.7 + LEFT*0.3)
        gene2_rect = Rectangle(width=0.4, height=0.6, color=gold_color, fill_opacity=0.7, stroke_width=0)
        gene2_rect.move_to(chromosome_x.get_center() + DOWN*0.7 + RIGHT*0.3)

        genes = VGroup(gene1_rect, gene2_rect)

        # Arrow from DNA to a gene segment
        arrow_dna_gene = Arrow(dna_model.get_right(), gene1_rect.get_left(), buff=0.1, color=WHITE)
        
        genes_text = Text("Genes: Segments of DNA", color=blue_color, font_size=32).next_to(dna_model, DOWN, buff=0.5)
        chrom_text = Text("Organized into Chromosomes", color=gold_color, font_size=32).next_to(chromosome_x, DOWN, buff=0.5)
        
        self.play(
            Create(genes_text),
            Create(arrow_dna_gene),
            FadeIn(chromosome_x, shift=RIGHT),
            Create(genes),
            Create(chrom_text),
            run_time=2
        )
        self.wait(1.5)

        # --- Beat 3: Alleles & Traits (Variation & Expression) ---
        self.play(
            FadeOut(genes_text, shift=DOWN),
            FadeOut(arrow_dna_gene, shift=RIGHT),
            FadeOut(dna_model),
            Transform(chromosome_x, chromosome_x.copy().shift(LEFT*2)),
            Transform(genes, genes.copy().shift(LEFT*2)),
            Transform(chrom_text, chrom_text.copy().next_to(chromosome_x, DOWN, buff=0.5).set_color(WHITE)),
            run_time=1.5
        )

        # Create a homologous pair of chromosomes
        chromosome_x_homolog = VGroup(
            Line(UP*1.5 + LEFT*0.5, DOWN*1.5 + RIGHT*0.5, color=gold_color, stroke_width=8),
            Line(UP*1.5 + RIGHT*0.5, DOWN*1.5 + LEFT*0.5, color=gold_color, stroke_width=8)
        )
        chromosome_x_homolog.scale(0.6).next_to(chromosome_x, RIGHT, buff=1)

        # Define alleles for a specific gene locus
        gene_locus_pos = chromosome_x.get_center() + UP*0.7 + LEFT*0.3
        allele_A = MathTex("A", color=gold_color).scale(0.9).move_to(gene_locus_pos)

        gene_locus_pos_homolog = chromosome_x_homolog.get_center() + UP*0.7 + LEFT*0.3
        allele_a = MathTex("a", color=blue_color).scale(0.9).move_to(gene_locus_pos_homolog)

        alleles_text = Text("Alleles: Different versions of a gene", color=blue_color, font_size=32).next_to(VGroup(chromosome_x, chromosome_x_homolog), UP, buff=0.7)
        
        self.play(
            FadeIn(chromosome_x_homolog, shift=RIGHT),
            Write(alleles_text),
            run_time=1.5
        )
        self.play(
            ReplacementTransform(genes[0], allele_A),
            Create(allele_a),
            run_time=1
        )
        self.wait(0.5)

        # Represent the trait resulting from the alleles
        trait_icon_1 = Text("🟤 Brown Eyes", color=gold_color, font_size=36).shift(RIGHT*3.5 + UP*1) 
        trait_icon_2 = Text("🔵 Blue Eyes", color=blue_color, font_size=36).shift(RIGHT*3.5 + DOWN*1) 
        
        arrow_to_trait_1 = Arrow(allele_A.get_right(), trait_icon_1.get_left(), buff=0.1, color=WHITE)
        arrow_to_trait_2 = Arrow(allele_a.get_right(), trait_icon_2.get_left(), buff=0.1, color=WHITE)

        trait_expl_text = Text("Determine specific traits", color=WHITE, font_size=28).next_to(VGroup(trait_icon_1, trait_icon_2), UP, buff=0.5)

        self.play(
            Create(arrow_to_trait_1),
            Create(arrow_to_trait_2),
            FadeIn(trait_icon_1, shift=UP),
            FadeIn(trait_icon_2, shift=DOWN),
            Write(trait_expl_text),
            run_time=2
        )
        self.wait(1)

        # --- Beat 4: Inheritance (Passing Down the Code) ---
        self.play(
            FadeOut(chrom_text),
            FadeOut(alleles_text, shift=UP),
            FadeOut(trait_expl_text, shift=UP),
            FadeOut(arrow_to_trait_1, arrow_to_trait_2),
            FadeOut(trait_icon_1, trait_icon_2),
            VGroup(chromosome_x, chromosome_x_homolog, allele_A, allele_a).animate.scale(0.7).arrange(RIGHT, buff=0.5).center().shift(UP*1.5),
            run_time=1.5
        )

        parent_label = Text("Parents", color=WHITE, font_size=28).next_to(VGroup(chromosome_x, chromosome_x_homolog), UP, buff=0.5)
        self.play(FadeIn(parent_label))
        
        # Simulate gamete formation (simplistic)
        gamete1 = VGroup(chromosome_x.copy().scale(0.5), allele_A.copy().scale(0.5)).arrange(RIGHT, buff=0.1).next_to(parent_label, DOWN, buff=1.5).shift(LEFT*2)
        gamete2 = VGroup(chromosome_x_homolog.copy().scale(0.5), allele_a.copy().scale(0.5)).arrange(RIGHT, buff=0.1).next_to(parent_label, DOWN, buff=1.5).shift(RIGHT*2)

        gamete_arrow1 = Arrow(VGroup(chromosome_x, allele_A).get_bottom(), gamete1.get_top(), color=WHITE)
        gamete_arrow2 = Arrow(VGroup(chromosome_x_homolog, allele_a).get_bottom(), gamete2.get_top(), color=WHITE)

        inheritance_text = Text("Inheritance: Genetic information passed on.", color=gold_color, font_size=32).next_to(parent_label, UP, buff=0.7)
        self.play(Write(inheritance_text))
        
        self.play(
            Create(gamete_arrow1), Create(gamete_arrow2),
            FadeIn(gamete1), FadeIn(gamete2),
            run_time=1.5
        )
        self.wait(0.5)

        # Simulate offspring formation (combine gametes)
        # We take the chromosome from gamete1 and allele from gamete1, and same for gamete2
        offspring_chrom_left = gamete1[0].copy().shift(DOWN*2.5 + LEFT*0.2)
        offspring_allele_left = gamete1[1].copy().shift(DOWN*2.5 + LEFT*0.2 + UP*0.1) # Position allele within chromosome

        offspring_chrom_right = gamete2[0].copy().shift(DOWN*2.5 + RIGHT*0.2)
        offspring_allele_right = gamete2[1].copy().shift(DOWN*2.5 + RIGHT*0.2 + UP*0.1)

        offspring_pair_chroms = VGroup(offspring_chrom_left, offspring_chrom_right).arrange(RIGHT, buff=0.1)
        offspring_pair_alleles = VGroup(offspring_allele_left, offspring_allele_right).arrange(RIGHT, buff=0.1).move_to(offspring_pair_chroms.get_center() + UP*0.1)
        
        offspring_mobject = VGroup(offspring_pair_chroms, offspring_pair_alleles).center().shift(DOWN*1.5)

        offspring_arrow = Arrow(VGroup(gamete1, gamete2).get_bottom(), offspring_mobject.get_top(), color=WHITE)
        
        offspring_label = Text("Offspring", color=WHITE, font_size=28).next_to(offspring_mobject, DOWN, buff=0.5)

        self.play(
            Create(offspring_arrow),
            FadeOut(gamete1, gamete2), # Fade out original gametes
            FadeIn(offspring_mobject),
            FadeIn(offspring_label),
            run_time=2
        )
        self.wait(1.5)

        # --- Recap Card ---
        self.play(
            FadeOut(VGroup(parent_label, inheritance_text, gamete_arrow1, gamete_arrow2, offspring_arrow, offspring_label)),
            FadeOut(chromosome_x, chromosome_x_homolog, allele_A, allele_a), # Original parent Mobjects
            FadeOut(offspring_mobject),
            FadeOut(title), # Fade out the initial title
            run_time=1
        )

        recap_title = Text("Genetics: Key Concepts", color=gold_color, font_size=40).to_edge(UP, buff=0.5)
        recap_list = BulletedList(
            "DNA is the genetic blueprint.",
            "Genes are segments of DNA on chromosomes.",
            "Alleles are variations of genes that determine traits.",
            "Genetic information is passed from parents to offspring.",
            font_size=32,
            color=WHITE,
            buff=0.6
        )
        recap_list.arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(recap_title, DOWN, buff=0.7)
        
        self.play(
            Write(recap_title),
            LaggedStart(*[FadeIn(item, shift=LEFT) for item in recap_list], lag_ratio=0.3),
            run_time=3
        )
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_list)))
        self.wait(0.5)