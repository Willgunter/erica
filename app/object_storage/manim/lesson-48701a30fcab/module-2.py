from manim import *

class GeneticsIntro(Scene):
    def construct(self):
        # 1. Configuration (Dark background, high-contrast colors)
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_E
        TEXT_COLOR = WHITE

        # --- Beat 1: Visual Hook & Introduction to DNA as Information ---
        # Strong visual hook: Swirling chaos resolving into a helix
        abstract_dots = VGroup(*[Dot(radius=0.05).set_color(random_color()).move_to(random_vector(3) * 2) for _ in range(100)])
        self.play(
            LaggedStart(*[FadeIn(d, shift=random_vector(3)*0.5) for d in abstract_dots]),
            run_time=2
        )
        self.wait(0.5)

        # Create a simplified 2D representation of a double helix
        helix_points_left = []
        helix_points_right = []
        num_segments = 50
        amplitude = 0.5
        frequency = 2 * PI
        for i in range(num_segments + 1):
            t = i / num_segments
            x_left = -amplitude * np.sin(frequency * t) - 0.5
            x_right = amplitude * np.sin(frequency * t) + 0.5
            y = 3 * t - 1.5
            helix_points_left.append([x_left, y, 0])
            helix_points_right.append([x_right, y, 0])

        helix_left = VMobject().set_points_as_corners(helix_points_left).make_smooth().set_color(BLUE_ACCENT)
        helix_right = VMobject().set_points_as_corners(helix_points_right).make_smooth().set_color(BLUE_ACCENT)

        cross_bars = VGroup()
        for i in range(5, num_segments, 5):
            point_l = helix_left.get_point_from_function(lambda t: t/num_segments*num_segments, i)
            point_r = helix_right.get_point_from_function(lambda t: t/num_segments*num_segments, i)
            cross_bar = Line(point_l, point_r, color=GOLD_ACCENT, stroke_width=2)
            cross_bars.add(cross_bar)

        double_helix = VGroup(helix_left, helix_right, cross_bars).scale(0.8).shift(UP*0.5)

        title = Text("The Code of Life.", font_size=50, color=TEXT_COLOR).move_to(UP*2.5)
        subtitle = Text("Genetics: Information Passed Down.", font_size=30, color=TEXT_COLOR).next_to(title, DOWN*0.8)

        self.play(
            FadeOut(abstract_dots, target_position=double_helix),
            Create(double_helix, run_time=3, lag_ratio=0.1),
            Write(title),
            Write(subtitle),
            run_time=4
        )
        self.wait(1)

        # Zoom into DNA as Blueprint, fading out titles
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            double_helix.animate.scale(1.5).shift(LEFT*2.5),
            run_time=2
        )

        dna_blueprint_text = Text("DNA: Our Genetic Blueprint", font_size=35, color=TEXT_COLOR).move_to(RIGHT*3 + UP*1.5)
        info_storage_text = Text("Information Storage", font_size=30, color=GOLD_ACCENT).next_to(dna_blueprint_text, DOWN*0.8)
        self.play(
            Write(dna_blueprint_text),
            Write(info_storage_text)
        )
        self.wait(1.5)

        # --- Beat 2: Genes as "Instructions" / "Functions" and Alleles as "Variants" ---
        self.play(
            FadeOut(dna_blueprint_text),
            FadeOut(info_storage_text),
            double_helix.animate.shift(LEFT*1)
        )

        # Represent genes as highlighted segments
        gene_1_segment = Rectangle(width=1.8, height=0.5, color=BLUE_ACCENT, fill_opacity=0.3, stroke_width=2).move_to(double_helix.get_center() + DOWN*0.5)
        gene_1_label = Text("Gene (Instruction)", font_size=25, color=TEXT_COLOR).next_to(gene_1_segment, RIGHT)
        self.play(
            Create(gene_1_segment),
            Write(gene_1_label)
        )
        self.wait(1)

        # Metaphor: Function 'trait_color'
        func_notation = MathTex(
            "f_{\\text{trait\_color}}", "(", "\\text{input}", ")", "\\rightarrow", "\\text{output}"
        ).set_color(BLUE_ACCENT).scale(0.8).next_to(gene_1_segment, DOWN*2)
        self.play(Write(func_notation))
        self.wait(1)

        # Introduce Alleles as variants
        gene_1_label_new = Text("Genes: Specific Instructions", font_size=28, color=TEXT_COLOR).move_to(UP*2.5)
        alleles_label = Text("Alleles: Different Versions", font_size=28, color=GOLD_ACCENT).move_to(UP*1.5)
        
        self.play(
            Transform(gene_1_label, gene_1_label_new),
            FadeOut(func_notation),
            gene_1_segment.animate.move_to(LEFT*2.5 + DOWN*0.5).scale(0.8)
        )
        self.play(Write(alleles_label))

        allele_A = MathTex("A", font_size=50, color=BLUE_ACCENT).next_to(gene_1_segment, RIGHT*2)
        allele_a = MathTex("a", font_size=50, color=GOLD_ACCENT).next_to(allele_A, RIGHT*1.5)
        allele_a_label = Text("(Variant)", font_size=20, color=GOLD_ACCENT).next_to(allele_a, DOWN*0.5)

        self.play(Write(allele_A))
        self.play(ReplacementTransform(allele_A.copy(), allele_a), Write(allele_a_label))
        self.wait(1.5)

        # --- Beat 3: Inheritance - Passing on Traits (Parent to Offspring) ---
        self.play(
            FadeOut(gene_1_segment),
            FadeOut(gene_1_label),
            FadeOut(alleles_label),
            FadeOut(allele_a_label),
            FadeOut(double_helix), # Clear the helix for a simpler representation
            allele_A.animate.scale(0.7).move_to(LEFT*4 + UP*2),
            allele_a.animate.scale(0.7).move_to(RIGHT*4 + UP*2),
        )

        parent1_gene_text = MathTex("AA").set_color_by_tex("A", BLUE_ACCENT).arrange(RIGHT, buff=0.2).scale(0.8).move_to(LEFT*4 + UP*2)
        parent2_gene_text = MathTex("aa").set_color_by_tex("a", GOLD_ACCENT).arrange(RIGHT, buff=0.2).scale(0.8).move_to(RIGHT*4 + UP*2)
        
        parent1_label = Text("Parent 1", font_size=25, color=TEXT_COLOR).next_to(parent1_gene_text, UP)
        parent2_label = Text("Parent 2", font_size=25, color=TEXT_COLOR).next_to(parent2_gene_text, UP)

        self.play(
            ReplacementTransform(allele_A, parent1_gene_text),
            ReplacementTransform(allele_a, parent2_gene_text),
            Write(parent1_label),
            Write(parent2_label)
        )
        self.wait(0.5)

        # Simulate gamete contribution and offspring combinations (simplified)
        offspring_label = Text("Offspring", font_size=25, color=TEXT_COLOR).move_to(UP*0.5)

        p1_gamete = parent1_gene_text[0].copy().move_to(LEFT*2.5 + DOWN*0.5)
        p2_gamete = parent2_gene_text[0].copy().move_to(RIGHT*2.5 + DOWN*0.5)
        
        self.play(
            FadeOut(parent1_label), FadeOut(parent2_label),
            Create(Arrow(parent1_gene_text.get_center(), p1_gamete.get_center(), buff=0.1, color=TEXT_COLOR)),
            Create(Arrow(parent2_gene_text.get_center(), p2_gamete.get_center(), buff=0.1, color=TEXT_COLOR)),
            FadeOut(parent1_gene_text[1]), FadeOut(parent2_gene_text[1]), # Fade out other allele for simplicity
            ReplacementTransform(parent1_gene_text[0], p1_gamete),
            ReplacementTransform(parent2_gene_text[0], p2_gamete),
            Write(offspring_label)
        )
        self.wait(0.5)
        
        # Combine alleles
        offspring_gene1 = MathTex("A", "a").set_color_by_tex("A", BLUE_ACCENT).set_color_by_tex("a", GOLD_ACCENT).arrange(RIGHT, buff=0.2).scale(0.9).move_to(DOWN*1.5)
        
        self.play(
            ReplacementTransform(p1_gamete, offspring_gene1[0]),
            ReplacementTransform(p2_gamete, offspring_gene1[1]),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 4: Genotype vs. Phenotype ---
        genotype_label = Text("Genotype: The Code", font_size=30, color=GOLD_ACCENT).move_to(LEFT*3 + UP*2)
        phenotype_label = Text("Phenotype: The Trait", font_size=30, color=BLUE_ACCENT).move_to(RIGHT*3 + UP*2)

        self.play(
            FadeOut(offspring_label),
            offspring_gene1.animate.move_to(LEFT*3 + DOWN*1),
            Write(genotype_label),
            Write(phenotype_label),
            run_time=1.5
        )

        genotype_notation_Aa = MathTex("Aa").set_color_by_tex("A", BLUE_ACCENT).set_color_by_tex("a", GOLD_ACCENT).scale(1.2).next_to(genotype_label, DOWN)
        phenotype_result_text_Aa = Text("Dominant Trait (e.g., Brown Eyes)", font_size=28, color=TEXT_COLOR).next_to(phenotype_label, DOWN*1.5)
        phenotype_result_circle_Aa = Circle(radius=0.7, color=BLUE_ACCENT, fill_opacity=0.7).next_to(phenotype_result_text_Aa, DOWN)
        
        self.play(
            ReplacementTransform(offspring_gene1, genotype_notation_Aa),
            Write(phenotype_result_text_Aa),
            Create(phenotype_result_circle_Aa)
        )
        self.wait(1.5)

        # Show other genotypes and phenotypes
        genotype_notation_AA = MathTex("AA").set_color(BLUE_ACCENT).scale(1.2).move_to(LEFT*3 + DOWN*3)
        phenotype_result_text_AA = Text("Dominant Trait (e.g., Brown Eyes)", font_size=28, color=TEXT_COLOR).next_to(phenotype_result_circle_Aa, DOWN*2)
        phenotype_result_circle_AA = Circle(radius=0.7, color=BLUE_ACCENT, fill_opacity=0.7).next_to(phenotype_result_text_AA, DOWN)

        self.play(
            FadeOut(phenotype_result_text_Aa), # Clear previous text to avoid clutter
            genotype_notation_Aa.animate.shift(UP*0.5), # Slight shift up to make room
            phenotype_result_circle_Aa.animate.shift(UP*0.5), # Slight shift up
            Write(genotype_notation_AA),
            Write(phenotype_result_text_AA),
            Create(phenotype_result_circle_AA)
        )
        self.wait(1.5)

        genotype_notation_aa = MathTex("aa").set_color(GOLD_ACCENT).scale(1.2).move_to(LEFT*3 + DOWN*5)
        phenotype_result_text_aa = Text("Recessive Trait (e.g., Blue Eyes)", font_size=28, color=TEXT_COLOR).next_to(phenotype_result_circle_AA, DOWN*2)
        phenotype_result_circle_aa = Circle(radius=0.7, color=GOLD_ACCENT, fill_opacity=0.7).next_to(phenotype_result_text_aa, DOWN)

        self.play(
            FadeOut(phenotype_result_text_AA), # Clear previous text
            genotype_notation_AA.animate.shift(UP*0.5),
            phenotype_result_circle_AA.animate.shift(UP*0.5),
            Write(genotype_notation_aa),
            Write(phenotype_result_text_aa),
            Create(phenotype_result_circle_aa)
        )
        self.wait(1.5)

        # --- Recap Card ---
        self.play(
            FadeOut(genotype_label), FadeOut(phenotype_label),
            FadeOut(genotype_notation_Aa), FadeOut(phenotype_result_circle_Aa),
            FadeOut(genotype_notation_AA), FadeOut(phenotype_result_circle_AA),
            FadeOut(genotype_notation_aa), FadeOut(phenotype_result_circle_aa),
            FadeOut(phenotype_result_text_aa) # Ensure all texts are faded
        )

        recap_title = Text("Genetics Recap", font_size=50, color=TEXT_COLOR).move_to(UP*2.5)
        
        bullet1 = BulletedList(
            "DNA = Blueprint (Information)",
            font_size=35, color=TEXT_COLOR, buff=0.8
        ).move_to(LEFT*1 + UP*0.5)
        
        bullet2 = BulletedList(
            "Genes = Instructions (Functions)",
            font_size=35, color=TEXT_COLOR, buff=0.8
        ).next_to(bullet1, DOWN*0.5, aligned_edge=LEFT)
        
        bullet3 = BulletedList(
            "Alleles = Variants (Parameters)",
            font_size=35, color=TEXT_COLOR, buff=0.8
        ).next_to(bullet2, DOWN*0.5, aligned_edge=LEFT)
        
        bullet4 = BulletedList(
            "Genotype $\\rightarrow$ Phenotype",
            font_size=35, color=TEXT_COLOR, buff=0.8
        ).next_to(bullet3, DOWN*0.5, aligned_edge=LEFT)

        self.play(Write(recap_title))
        self.play(LaggedStart(
            Write(bullet1),
            Write(bullet2),
            Write(bullet3),
            Write(bullet4),
            lag_ratio=0.7
        ))
        self.wait(3)

        self.play(FadeOut(VGroup(recap_title, bullet1, bullet2, bullet3, bullet4)))
        self.wait(0.5)