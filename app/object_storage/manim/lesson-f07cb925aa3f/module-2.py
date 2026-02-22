from manim import *

class HeredityAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        BLUE_ACCENT = "#50d1ff"  # High-contrast blue
        GOLD_ACCENT = "#FFD700"  # Gold accent
        TEXT_COLOR = WHITE

        # --- Scene 1: Title (Brief Intro) ---
        title = MathTex(
            "\\text{Heredity: DNA and Cell Division}",
            font_size=60, color=GOLD_ACCENT
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title, shift=UP), run_time=0.7)

        # --- Beat 1: The DNA Double Helix (Visual Hook) ---
        dna_label = MathTex("DNA", color=BLUE_ACCENT, font_size=50).to_edge(LEFT).shift(UP*2.5)

        # Create two parametric curves for the double helix strands
        # Using t for vertical progression, sin/cos for horizontal oscillation
        # Offset by PI for the second strand
        helix_points_left = [
            0.5 * RIGHT + 0.5 * UP * np.cos(t) + 0.5 * LEFT * np.sin(t) + t * DOWN * 0.18
            for t in np.linspace(0, 4 * PI, 50)
        ]
        helix_points_right = [
            0.5 * LEFT + 0.5 * UP * np.cos(t + PI) + 0.5 * RIGHT * np.sin(t + PI) + t * DOWN * 0.18
            for t in np.linspace(0, 4 * PI, 50)
        ]

        strand1 = VMobject(stroke_width=3, color=BLUE_ACCENT).set_points_as_corners(helix_points_left)
        strand2 = VMobject(stroke_width=3, color=BLUE_ACCENT).set_points_as_corners(helix_points_right)
        
        strands = VGroup(strand1, strand2).scale(1.5).center().shift(RIGHT * 2)

        # Connecting 'rungs' (base pairs)
        rungs = VGroup()
        for i in range(10):
            t_rung = i * PI * 0.8
            p1_rung = 0.5 * RIGHT + 0.5 * UP * np.cos(t_rung) + 0.5 * LEFT * np.sin(t_rung) + t_rung * DOWN * 0.18
            p2_rung = 0.5 * LEFT + 0.5 * UP * np.cos(t_rung + PI) + 0.5 * RIGHT * np.sin(t_rung + PI) + t_rung * DOWN * 0.18
            rung = Line(p1_rung, p2_rung, stroke_width=2, color=GOLD_ACCENT).scale(1.5).center().shift(RIGHT * 2)
            rungs.add(rung)

        self.play(Create(strand1), Create(strand2), run_time=1.5)
        self.play(LaggedStart(*[Create(rung) for rung in rungs], lag_ratio=0.05), run_time=1.5)
        self.play(FadeIn(dna_label, shift=LEFT), run_time=0.7)
        self.wait(1.5)

        # --- Beat 2: DNA to Chromosome ---
        chromosome_label = MathTex("Chromosome", color=BLUE_ACCENT, font_size=50).next_to(dna_label, DOWN, buff=0.8)

        # Simplified representation of condensed DNA
        dna_condensed_path = [
            0.5 * np.sin(t) * RIGHT + 0.1 * np.cos(t) * UP + t * DOWN * 0.2
            for t in np.linspace(0, 8 * PI, 100)
        ]
        dna_condensed_visual = VMobject(stroke_width=4, color=BLUE_ACCENT).set_points_as_corners(dna_condensed_path)
        dna_condensed_visual.scale(1.5).center().shift(RIGHT * 2)

        # Transform the double helix into a single, condensed strand
        # We transform the VGroup `strands` into `dna_condensed_visual`
        self.play(
            FadeOut(rungs),
            Transform(strands, dna_condensed_visual),
            run_time=1.5
        )

        # Histones (conceptual, represented by dots)
        histones = VGroup(*[
            Dot(color=GOLD_ACCENT, radius=0.08)
            for _ in range(15)
        ]).arrange_in_grid(rows=5, cols=3, buff=0.7).scale(0.8).next_to(strands, LEFT, buff=0.5)
        
        # Show histones, then fade them out as DNA condenses further
        self.play(FadeIn(histones, shift=RIGHT), run_time=0.8)
        self.play(FadeOut(histones), run_time=0.5)

        # Form a single chromatid arm (rounded rectangle)
        arm_shape = RoundedRectangle(corner_radius=0.5, width=0.8, height=2.5, color=BLUE_ACCENT, fill_opacity=0.7)
        arm_shape.move_to(strands) # Position it where the condensed DNA is

        self.play(Transform(strands, arm_shape), run_time=1.2) # Transform condensed DNA into arm

        # Form the full X-shaped chromosome from two chromatid arms
        chromatid_left_base = RoundedRectangle(corner_radius=0.5, width=0.5, height=2.0, color=BLUE_ACCENT, fill_opacity=0.7)
        chromatid_right_base = chromatid_left_base.copy()
        
        # Position and rotate to form X
        chromatid_left_x = chromatid_left_base.copy().rotate(-PI/6).shift(LEFT * 0.2)
        chromatid_right_x = chromatid_right_base.copy().rotate(PI/6).shift(RIGHT * 0.2)

        centromere = Circle(radius=0.15, color=GOLD_ACCENT, fill_opacity=1).move_to(ORIGIN)
        chromosome_x = VGroup(chromatid_left_x, chromatid_right_x, centromere).scale(0.8).center().shift(RIGHT * 2)

        self.play(
            ReplacementTransform(strands, chromosome_x), # Transform the single arm into the X chromosome
            FadeIn(chromosome_label, shift=LEFT),
            run_time=1.5
        )
        self.wait(1.5)

        # --- Beat 3: Genes: Instructions for Traits ---
        gene_label = MathTex("Genes", color=BLUE_ACCENT, font_size=50).next_to(chromosome_label, DOWN, buff=0.8)
        trait_label = MathTex("\\text{Traits}", color=GOLD_ACCENT, font_size=50).next_to(gene_label, RIGHT, buff=1.5)

        # Highlight sections on the chromosome (genes)
        gene_highlight1 = Rectangle(width=0.6, height=0.4, color=GOLD_ACCENT, fill_opacity=0.5).move_to(chromosome_x[0]).shift(UP*0.7 + LEFT*0.05)
        gene_highlight2 = Rectangle(width=0.6, height=0.4, color=GOLD_ACCENT, fill_opacity=0.5).move_to(chromosome_x[1]).shift(DOWN*0.7 + RIGHT*0.05)

        # Abstract trait representations
        trait1_shape = Square(side_length=0.7, color=RED, fill_opacity=0.7).next_to(gene_highlight1, RIGHT, buff=1)
        trait1_text = MathTex("\\text{Hair Color}", color=TEXT_COLOR, font_size=30).next_to(trait1_shape, DOWN, buff=0.1)
        
        trait2_shape = Circle(radius=0.35, color=GREEN, fill_opacity=0.7).next_to(gene_highlight2, RIGHT, buff=1)
        trait2_text = MathTex("\\text{Eye Color}", color=TEXT_COLOR, font_size=30).next_to(trait2_shape, DOWN, buff=0.1)

        arrow1 = Arrow(gene_highlight1.get_right(), trait1_shape.get_left(), buff=0.1, color=TEXT_COLOR)
        arrow2 = Arrow(gene_highlight2.get_right(), trait2_shape.get_left(), buff=0.1, color=TEXT_COLOR)

        self.play(FadeIn(gene_label, shift=LEFT), run_time=0.7)
        self.play(
            Create(gene_highlight1), FadeIn(trait1_shape), FadeIn(trait1_text), Create(arrow1),
            run_time=1.2
        )
        self.play(
            Create(gene_highlight2), FadeIn(trait2_shape), FadeIn(trait2_text), Create(arrow2),
            FadeIn(trait_label, shift=LEFT),
            run_time=1.2
        )
        self.wait(1.5)

        # --- Beat 4: Cell Division (Simplified Mitosis) ---
        cell_division_label = MathTex("Cell Division", color=BLUE_ACCENT, font_size=50).next_to(gene_label, DOWN, buff=0.8)

        # Clear previous elements and recenter chromosome
        self.play(
            FadeOut(dna_label, chromosome_label, gene_label, trait_label),
            FadeOut(gene_highlight1, gene_highlight2, trait1_shape, trait1_text, trait2_shape, trait2_text, arrow1, arrow2),
            chromosome_x.animate.scale(0.8).center(), # Shrink and center for focus
            run_time=1
        )
        self.wait(0.5)

        # Re-construct chromosome for easy splitting (it's already 3 components)
        # chromosome_x is VGroup(chromatid_left_x, chromatid_right_x, centromere)
        
        # Split the sister chromatids
        chromatid_left_split = chromosome_x[0].copy().shift(LEFT * 2.5 + UP * 0.5)
        chromatid_right_split = chromosome_x[1].copy().shift(RIGHT * 2.5 + UP * 0.5)

        self.play(FadeIn(cell_division_label, shift=LEFT), run_time=0.7)
        self.play(
            Transform(chromosome_x[0], chromatid_left_split),
            Transform(chromosome_x[1], chromatid_right_split),
            FadeOut(chromosome_x[2]), # Fade out centromere
            run_time=1.5
        )
        self.wait(0.5)

        # Form new cells and move chromatids into them
        cell1 = Circle(radius=1.5, color=BLUE_ACCENT, fill_opacity=0.2).shift(LEFT * 2.5 + DOWN * 1)
        cell2 = Circle(radius=1.5, color=BLUE_ACCENT, fill_opacity=0.2).shift(RIGHT * 2.5 + DOWN * 1)

        self.play(
            FadeIn(cell1), FadeIn(cell2),
            chromatid_left_split.animate.move_to(cell1.get_center() + UP * 0.5),
            chromatid_right_split.animate.move_to(cell2.get_center() + UP * 0.5),
            run_time=1.5
        )
        self.wait(1.5)

        # --- Recap Card ---
        self.play(
            FadeOut(cell_division_label, chromosome_x[0], chromosome_x[1], cell1, cell2),
            run_time=1
        )

        recap_title = Text("Key Takeaways", color=GOLD_ACCENT, font_size=55).to_edge(UP, buff=0.5)
        recap_items = VGroup(
            Tex("- DNA: The Blueprint of Life", color=TEXT_COLOR),
            Tex("- Chromosomes: Organized DNA Packages", color=TEXT_COLOR),
            Tex("- Genes: Instructions for Traits", color=TEXT_COLOR),
            Tex("- Cell Division: Passing on the Information", color=TEXT_COLOR)
        ).scale(0.8).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(recap_title, DOWN, buff=0.8)

        # Highlight key terms in blue accent
        recap_items.set_color_by_tex("DNA", BLUE_ACCENT)
        recap_items.set_color_by_tex("Chromosomes", BLUE_ACCENT)
        recap_items.set_color_by_tex("Genes", BLUE_ACCENT)
        recap_items.set_color_by_tex("Cell Division", BLUE_ACCENT)

        self.play(
            FadeIn(recap_title, shift=UP),
            LaggedStart(*[FadeIn(item, shift=LEFT) for item in recap_items], lag_ratio=0.2),
            run_time=3
        )
        self.wait(3)