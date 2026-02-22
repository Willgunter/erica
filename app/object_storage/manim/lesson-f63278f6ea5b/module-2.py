from manim import *

# Configure colors for 3B1B style
BLUE_ACCENT = BLUE_C
GOLD_ACCENT = GOLD_C
TEXT_COLOR = WHITE

class DNAHeredityCellDivision(Scene):
    def construct(self):
        # Helper function to create a stylized double helix
        def create_dna_helix(scale_factor=1, num_turns=1.5, radius=0.8, height=3, strand_colors=(BLUE_ACCENT, GOLD_ACCENT), rung_color=TEXT_COLOR):
            points = []
            points2 = []
            for t in np.linspace(0, num_turns * 2 * PI, 100):
                x = radius * np.cos(t)
                y = radius * np.sin(t)
                z = (t / (num_turns * 2 * PI)) * height - height/2 # To ensure it's centered
                points.append([x, y, z])
                points2.append([-x, y, z]) # Complementary strand
            
            strand1 = VMobject().set_points_smoothly(points).set_color(strand_colors[0])
            strand2 = VMobject().set_points_smoothly(points2).set_color(strand_colors[1])
            
            rungs_group = VGroup()
            for i in range(0, 100, 10): # Add rungs at intervals
                rung = Line(strand1.points[i], strand2.points[i], color=rung_color, stroke_width=2)
                rungs_group.add(rung)

            return VGroup(strand1, strand2, rungs_group).scale(scale_factor)

        # --- Beat 1: The Blueprint of Life - DNA (Visual Hook) ---
        title_beat1 = Text("DNA: The Blueprint of Life", font_size=50, color=TEXT_COLOR).to_edge(UP)
        self.play(FadeIn(title_beat1, shift=UP))

        # Visual Hook: Abstract lines transforming into a double helix
        initial_lines = VGroup(*[
            Line(np.random.rand(3) * 6 - 3, np.random.rand(3) * 6 - 3, color=random.choice([BLUE_ACCENT, GOLD_ACCENT]))
            for _ in range(20)
        ]).center().scale(1.5)
        self.play(Create(initial_lines), run_time=1.5)

        dna_helix = create_dna_helix(scale_factor=0.8).center().shift(LEFT*2.5)
        dna_label = MathTex("\\text{DNA}", "\\text{ (Deoxyribonucleic Acid)}", font_size=40).next_to(dna_helix, RIGHT)
        dna_label[0].set_color(BLUE_ACCENT)
        dna_label[1].set_color(TEXT_COLOR)

        self.play(
            ReplacementTransform(initial_lines, dna_helix),
            Write(dna_label[0]), FadeIn(dna_label[1], shift=RIGHT),
            run_time=2
        )
        self.wait(1)
        self.play(FadeOut(title_beat1))


        # --- Beat 2: Genetic Information (The Code) ---
        title_beat2 = Text("Genetic Code: Information Storage", font_size=50, color=TEXT_COLOR).to_edge(UP)
        self.play(FadeIn(title_beat2, shift=UP))

        # Zoom in on a segment and show base pairs abstractly
        zoomed_dna = create_dna_helix(scale_factor=0.3, height=1.5).center().shift(LEFT*3) # Smaller segment
        self.play(
            ReplacementTransform(dna_helix, zoomed_dna),
            FadeOut(dna_label[1]),
            dna_label[0].animate.next_to(zoomed_dna, RIGHT, buff=0.5).scale(0.8) # Adjust label position
        )

        # Represent bases and their pairings
        base_A = Square(0.4, color=BLUE_ACCENT, fill_opacity=0.8).next_to(zoomed_dna.submobjects[0].points[30], LEFT, buff=0.1)
        base_T = Square(0.4, color=GOLD_ACCENT, fill_opacity=0.8).next_to(zoomed_dna.submobjects[1].points[30], RIGHT, buff=0.1)
        base_C = Triangle(color=BLUE_ACCENT, fill_opacity=0.8).scale(0.25).next_to(zoomed_dna.submobjects[0].points[50], LEFT, buff=0.1)
        base_G = Triangle(color=GOLD_ACCENT, fill_opacity=0.8).scale(0.25).next_to(zoomed_dna.submobjects[1].points[50], RIGHT, buff=0.1)

        at_math = MathTex("A", "- ", "T", font_size=35).next_to(base_A, LEFT).set_color(TEXT_COLOR)
        cg_math = MathTex("C", "- ", "G", font_size=35).next_to(base_C, LEFT).set_color(TEXT_COLOR)
        at_math[0].set_color(BLUE_ACCENT); at_math[2].set_color(GOLD_ACCENT)
        cg_math[0].set_color(BLUE_ACCENT); cg_math[2].set_color(GOLD_ACCENT)

        base_pair_group = VGroup(base_A, base_T, base_C, base_G, at_math, cg_math)
        self.play(FadeIn(base_pair_group, shift=RIGHT), run_time=1.5)
        
        # A NumberPlane to suggest structured information/sequence
        info_plane = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=4, y_length=4,
            background_line_style={"stroke_opacity": 0.3, "stroke_color": TEXT_COLOR},
            axis_config={"include_numbers": False, "stroke_opacity": 0.5}
        ).shift(RIGHT * 3.5).scale(0.7)
        info_label = Text("Sequence", font_size=25, color=TEXT_COLOR).next_to(info_plane, UP)

        self.play(Create(info_plane), FadeIn(info_label), run_time=1)
        
        read_arrow = Arrow(info_plane.get_left(), info_plane.get_right(), buff=0.1, color=BLUE_ACCENT)
        read_label = Text("Readout", font_size=25, color=BLUE_ACCENT).next_to(read_arrow, DOWN)
        self.play(Create(read_arrow), FadeIn(read_label), run_time=0.7)

        self.wait(1.5)
        self.play(
            FadeOut(title_beat2, shift=UP),
            FadeOut(base_pair_group),
            FadeOut(info_plane),
            FadeOut(info_label),
            FadeOut(read_arrow),
            FadeOut(read_label),
            dna_label[0].animate.center().scale(1/0.8).shift(LEFT*2.5) # Reset dna_label position for next beat
        )


        # --- Beat 3: Replication & Heredity (Passing It On) ---
        title_beat3 = Text("Replication: Passing on the Blueprint", font_size=50, color=TEXT_COLOR).to_edge(UP)
        self.play(FadeIn(title_beat3, shift=UP))
        
        # Current DNA helix from previous beat, resized
        current_dna_helix = dna_helix.copy().scale(0.7).center().shift(LEFT*2.5)
        self.play(ReplacementTransform(zoomed_dna, current_dna_helix), run_time=1)
        
        # Animate unzipping
        original_strand1 = current_dna_helix.submobjects[0]
        original_strand2 = current_dna_helix.submobjects[1]
        original_rungs = current_dna_helix.submobjects[2]

        self.play(
            original_rungs.animate.fade(1), # Fade out rungs
            original_strand1.animate.shift(LEFT*0.6),
            original_strand2.animate.shift(RIGHT*0.6),
            run_time=1.5
        )
        
        # Create new complementary strands appearing
        new_strand_points1 = original_strand2.points.copy() # Points for the new strand complementing original_strand1
        new_strand_points2 = original_strand1.points.copy() # Points for the new strand complementing original_strand2
        
        new_dna1_strand = VMobject().set_points_smoothly(new_strand_points2).set_color(GOLD_ACCENT)
        new_dna2_strand = VMobject().set_points_smoothly(new_strand_points1).set_color(BLUE_ACCENT)

        # Rungs for the newly forming helices
        new_rungs1 = VGroup(*[Line(original_strand1.points[i], new_dna1_strand.points[i], color=TEXT_COLOR, stroke_width=1) for i in range(0, 100, 10)])
        new_rungs2 = VGroup(*[Line(original_strand2.points[i], new_dna2_strand.points[i], color=TEXT_COLOR, stroke_width=1) for i in range(0, 100, 10)])

        self.play(
            Create(new_dna1_strand),
            Create(new_dna2_strand),
            Create(new_rungs1),
            Create(new_rungs2),
            run_time=1.5
        )

        # Form two complete DNA helices, separating them
        dna_copy1_group = VGroup(original_strand1, new_dna1_strand, new_rungs1).copy().shift(LEFT*0.6) # Shift back the original piece
        dna_copy2_group = VGroup(original_strand2, new_dna2_strand, new_rungs2).copy().shift(RIGHT*0.6) # Shift back the original piece

        dna_copy1_group.generate_target()
        dna_copy2_group.generate_target()

        dna_copy1_group.target.center().shift(LEFT*3)
        dna_copy2_group.target.center().shift(RIGHT*3)
        
        self.play(
            Transform(dna_copy1_group, dna_copy1_group.target),
            Transform(dna_copy2_group, dna_copy2_group.target),
            run_time=2
        )
        
        heredity_arrow = Arrow(LEFT*1.5, RIGHT*1.5, buff=0.1, color=GOLD_ACCENT).next_to(ORIGIN, DOWN, buff=1)
        heredity_text = Text("Heredity", font_size=35, color=GOLD_ACCENT).next_to(heredity_arrow, DOWN)

        self.play(Create(heredity_arrow), FadeIn(heredity_text))

        self.wait(1.5)
        self.play(
            FadeOut(title_beat3, shift=UP),
            FadeOut(dna_copy1_group.target),
            FadeOut(dna_copy2_group.target),
            FadeOut(heredity_arrow),
            FadeOut(heredity_text),
            FadeOut(dna_label[0])
        )


        # --- Beat 4: Cell Division ---
        title_beat4 = Text("Cell Division: Sharing the Blueprint", font_size=50, color=TEXT_COLOR).to_edge(UP)
        self.play(FadeIn(title_beat4, shift=UP))

        # Start with a simple cell (circle) containing replicated DNA (abstract chromosomes)
        cell = Circle(radius=2, color=BLUE_ACCENT, fill_opacity=0.1).center()
        
        chromosome_left = Rectangle(width=0.4, height=1.5, color=GOLD_ACCENT, fill_opacity=0.8).shift(LEFT*0.5)
        chromosome_right = Rectangle(width=0.4, height=1.5, color=BLUE_ACCENT, fill_opacity=0.8).shift(RIGHT*0.5)
        
        # Replicated structure of chromosomes (sister chromatids)
        chromosome_pair1 = VGroup(
            chromosome_left.copy().shift(LEFT*0.2), 
            chromosome_left.copy().shift(RIGHT*0.2)
        ).scale(0.7).rotate(PI/4).shift(LEFT*1)
        
        chromosome_pair2 = VGroup(
            chromosome_right.copy().shift(LEFT*0.2), 
            chromosome_right.copy().shift(RIGHT*0.2)
        ).scale(0.7).rotate(PI/4).shift(RIGHT*1)

        dna_in_cell = VGroup(chromosome_pair1, chromosome_pair2).move_to(cell.get_center())
        
        self.play(Create(cell), Create(dna_in_cell), run_time=1.5)
        self.wait(0.5)

        # Cell elongates and chromosomes separate and move to poles
        cell_elongated = Ellipse(width=5.5, height=2.5, color=BLUE_ACCENT, fill_opacity=0.1).center()
        
        # Separate sister chromatids and move to opposite ends
        separated_chromatid1_a = chromosome_pair1.submobjects[0].copy().shift(LEFT * 2)
        separated_chromatid1_b = chromosome_pair1.submobjects[1].copy().shift(LEFT * 2) # This one is actually moving right
        separated_chromatid2_a = chromosome_pair2.submobjects[0].copy().shift(RIGHT * 2) # This one is actually moving left
        separated_chromatid2_b = chromosome_pair2.submobjects[1].copy().shift(RIGHT * 2)

        self.play(
            Transform(cell, cell_elongated),
            ReplacementTransform(chromosome_pair1.submobjects[0], separated_chromatid1_a.shift(UP*0.5)),
            ReplacementTransform(chromosome_pair1.submobjects[1], separated_chromatid2_a.shift(UP*0.5)),
            ReplacementTransform(chromosome_pair2.submobjects[0], separated_chromatid1_b.shift(DOWN*0.5)),
            ReplacementTransform(chromosome_pair2.submobjects[1], separated_chromatid2_b.shift(DOWN*0.5)),
            run_time=2
        )
        
        # Collect into pole groups
        pole1_chromosomes = VGroup(separated_chromatid1_a, separated_chromatid1_b.shift(LEFT*4)).arrange(DOWN, buff=0.5).shift(LEFT*2.5)
        pole2_chromosomes = VGroup(separated_chromatid2_a.shift(RIGHT*4), separated_chromatid2_b).arrange(DOWN, buff=0.5).shift(RIGHT*2.5)

        # Fade out elongated cell and create two new ones
        new_cell1 = Circle(radius=1.5, color=BLUE_ACCENT, fill_opacity=0.1).shift(LEFT * 2.5)
        new_cell2 = Circle(radius=1.5, color=BLUE_ACCENT, fill_opacity=0.1).shift(RIGHT * 2.5)
        
        self.play(
            FadeOut(cell),
            FadeTransform(VGroup(separated_chromatid1_a, separated_chromatid1_b.shift(LEFT*4)), pole1_chromosomes),
            FadeTransform(VGroup(separated_chromatid2_a.shift(RIGHT*4), separated_chromatid2_b), pole2_chromosomes),
            Create(new_cell1),
            Create(new_cell2),
            run_time=1.5
        )
        
        divided_label = Text("Two Daughter Cells", font_size=30, color=TEXT_COLOR).next_to(new_cell1, DOWN).shift(RIGHT*2.5)
        self.play(Write(divided_label))

        self.wait(1.5)
        self.play(
            FadeOut(title_beat4, shift=UP),
            FadeOut(new_cell1),
            FadeOut(new_cell2),
            FadeOut(pole1_chromosomes),
            FadeOut(pole2_chromosomes),
            FadeOut(divided_label)
        )

        # --- Recap Card ---
        recap_title = Text("Recap:", font_size=60, color=GOLD_ACCENT).to_edge(UP)
        
        recap_points = VGroup(
            Tex("- \\textbf{DNA} is the blueprint of life.", font_size=40, color=TEXT_COLOR),
            Tex("- \\textbf{Genetic code} stores inherited information.", font_size=40, color=TEXT_COLOR),
            Tex("- \\textbf{Replication} ensures faithful copying of DNA.", font_size=40, color=TEXT_COLOR),
            Tex("- \\textbf{Cell division} passes DNA to new cells.", font_size=40, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).next_to(recap_title, DOWN, buff=0.8).shift(LEFT * 0.5)
        
        # Color specific keywords
        recap_points[0].submobjects[1][0:3].set_color(BLUE_ACCENT) # DNA
        recap_points[1].submobjects[1][0:12].set_color(GOLD_ACCENT) # Genetic code
        recap_points[2].submobjects[1][0:11].set_color(BLUE_ACCENT) # Replication
        recap_points[3].submobjects[1][0:12].set_color(GOLD_ACCENT) # Cell division

        self.play(FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT) for p in recap_points], lag_ratio=0.5), run_time=3)
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_points)))
        self.wait(1)