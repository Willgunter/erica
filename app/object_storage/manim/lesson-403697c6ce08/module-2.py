from manim import *

class GeneticInheritance(Scene):
    def construct(self):
        # Configuration for dark background and custom colors
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE_A # High-contrast blue
        GOLD_ACCENT = GOLD_A # High-contrast gold
        TEXT_COLOR = WHITE   # General text color

        # --- Beat 1: Hook & Introduction ---
        # Title of the module
        title = Text("Genetic Information and Inheritance", font_size=50, color=GOLD_ACCENT).move_to(UP*2.5)
        self.play(Write(title))
        self.wait(0.5)

        # Visual Hook: Abstract DNA Helix formation
        # Creating points for two strands of a helix with a slight 3D perspective
        helix_points_1 = []
        helix_points_2 = []
        num_segments = 30
        amplitude = 1.5
        frequency = 2.5
        z_depth_factor = 0.5 # Gives a sense of depth without full 3D objects
        vertical_span = 4

        for i in range(num_segments + 1):
            t = i / num_segments * TAU # Parametric angle
            # Strand 1
            x1 = amplitude * np.sin(t * frequency)
            y1 = i / num_segments * vertical_span - (vertical_span / 2)
            z1 = amplitude * np.cos(t * frequency) * z_depth_factor
            helix_points_1.append(np.array([x1, y1, z1]))

            # Strand 2 (phase-shifted by PI)
            x2 = amplitude * np.sin(t * frequency + PI)
            y2 = i / num_segments * vertical_span - (vertical_span / 2)
            z2 = amplitude * np.cos(t * frequency + PI) * z_depth_factor
            helix_points_2.append(np.array([x2, y2, z2]))

        strand1 = VGroup(*[Line(helix_points_1[i], helix_points_1[i+1], color=BLUE_ACCENT, stroke_width=3) for i in range(num_segments)])
        strand2 = VGroup(*[Line(helix_points_2[i], helix_points_2[i+1], color=BLUE_ACCENT, stroke_width=3) for i in range(num_segments)])

        # Rungs connecting the two strands (simplified)
        rungs = VGroup()
        for i in range(0, num_segments + 1, 3): # Connect points less frequently for visual clarity
            rung_color = GOLD_ACCENT # Consistent color for rungs
            rungs.add(Line(helix_points_1[i], helix_points_2[i], color=rung_color, stroke_width=2))

        dna_helix = VGroup(strand1, strand2, rungs).scale(0.8).shift(LEFT*3) # Group and scale for screen fit

        # Animation for helix creation
        self.play(
            LaggedStart(
                Create(strand1, run_time=1.5),
                Create(strand2, run_time=1.5),
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.play(Create(rungs, run_time=1.5))
        self.wait(0.5)

        # Text: "The blueprint of life"
        blueprint_text = Text("The Blueprint of Life", font_size=36, color=TEXT_COLOR).next_to(dna_helix, RIGHT, buff=1)
        self.play(FadeIn(blueprint_text, shift=UP))
        self.wait(1)

        # --- Beat 2: DNA Structure and Information Storage ---
        # Prepare to focus on DNA structure
        self.play(
            dna_helix.animate.scale(0.5).move_to(LEFT*4 + UP*1.5), # Shrink and move the full helix out of the way
            FadeOut(title, blueprint_text)
        )

        dna_struct_title = Text("DNA: A Double Helix", font_size=40, color=GOLD_ACCENT).to_corner(UL)
        self.play(Write(dna_struct_title))

        # Create a simplified 2D segment of DNA for clarity
        segment_length = 2.5
        segment_width = 0.5
        base_spacing = 0.5
        
        backbone_left = Line(LEFT*segment_width, LEFT*segment_width + UP*segment_length, color=BLUE_ACCENT, stroke_width=5)
        backbone_right = Line(RIGHT*segment_width, RIGHT*segment_width + UP*segment_length, color=BLUE_ACCENT, stroke_width=5)
        
        bases = VGroup()
        base_pairs_tex = VGroup() # For the A, T, C, G labels
        base_pairs = [("A", "T"), ("G", "C"), ("T", "A"), ("C", "G")]

        for i, (b1_char, b2_char) in enumerate(base_pairs):
            y_pos = i * base_spacing
            
            base_line = Line(LEFT*segment_width, RIGHT*segment_width, color=GOLD_ACCENT, stroke_width=2)
            base_line.move_to(UP*y_pos)
            
            b1_tex = MathTex(b1_char, color=GOLD_ACCENT).next_to(base_line, LEFT, buff=0.1)
            b2_tex = MathTex(b2_char, color=GOLD_ACCENT).next_to(base_line, RIGHT, buff=0.1)

            bases.add(base_line) # Only add lines to 'bases' for easy fading
            base_pairs_tex.add(b1_tex, b2_tex) # Add MathTex objects to 'base_pairs_tex'

        dna_segment_structure = VGroup(backbone_left, backbone_right, bases)
        dna_segment_labeled = VGroup(dna_segment_structure, base_pairs_tex).move_to(RIGHT*2.5 + UP*0.5).scale(1.2)

        self.play(
            FadeIn(dna_segment_labeled, shift=RIGHT),
            run_time=1.5
        )

        info_text_1 = Text("Stores genetic instructions", font_size=32, color=TEXT_COLOR).next_to(dna_segment_labeled, DOWN, buff=0.8)
        info_text_2 = Text("using 4 chemical letters (A, T, C, G).", font_size=32, color=TEXT_COLOR).next_to(info_text_1, DOWN, buff=0.2)
        
        self.play(Write(info_text_1), FadeIn(info_text_2, shift=DOWN))
        self.wait(1.5)

        # Highlight base pairing with arrows
        arrows = VGroup()
        for i in range(len(base_pairs_tex)//2):
            arrow = Arrow(
                base_pairs_tex[2*i].get_right(), # From the right of the first letter
                base_pairs_tex[2*i+1].get_left(), # To the left of the second letter
                buff=0.1, stroke_width=3, max_stroke_width_to_length_ratio=4,
                max_tip_length_to_length_ratio=0.3, color=BLUE_ACCENT
            )
            arrows.add(arrow)
        
        self.play(Create(arrows))
        self.wait(1)
        
        self.play(
            FadeOut(dna_segment_labeled, info_text_1, info_text_2, arrows, dna_struct_title)
        )

        # --- Beat 3: Genes as Segments of DNA, Traits ---
        # Re-use a copy of the DNA segment for visual continuity
        gene_dna = dna_segment_labeled.copy().center()
        self.play(FadeIn(gene_dna))
        
        gene_title = Text("Genes: Segments of DNA", font_size=40, color=GOLD_ACCENT).to_corner(UL)
        self.play(Write(gene_title))

        # Highlight a section as a "gene"
        gene_segment_highlight = Rectangle(
            width=gene_dna.width * 0.4,
            height=gene_dna.height * 0.3,
            color=BLUE_ACCENT,
            fill_opacity=0.3,
            stroke_width=3
        ).move_to(gene_dna.get_center() + UP * 0.5)

        self.play(Create(gene_segment_highlight))
        
        gene_text_1 = Text("A gene is a specific segment", font_size=32, color=TEXT_COLOR).next_to(gene_dna, DOWN, buff=0.8)
        gene_text_2 = Text("that codes for a particular trait.", font_size=32, color=TEXT_COLOR).next_to(gene_text_1, DOWN, buff=0.2)
        
        self.play(Write(gene_text_1), FadeIn(gene_text_2, shift=DOWN))
        self.wait(1)

        # Show connection to a "trait"
        trait_arrow = Arrow(gene_segment_highlight.get_right(), RIGHT*4, color=GOLD_ACCENT, buff=0.2)
        trait_box = SurroundingRectangle(MathTex("\\text{Trait}", color=TEXT_COLOR), color=BLUE_ACCENT, buff=0.3)
        trait_example_text = MathTex("\\text{Eye Color}", color=TEXT_COLOR).move_to(trait_box.get_center())
        trait_group = VGroup(trait_box, trait_example_text).next_to(trait_arrow, RIGHT, buff=0.2)
        
        self.play(Create(trait_arrow), Create(trait_group))
        self.wait(1.5)

        self.play(
            FadeOut(gene_dna, gene_segment_highlight, gene_title, gene_text_1, gene_text_2, trait_arrow, trait_group)
        )

        # --- Beat 4: Inheritance ---
        inheritance_title = Text("Inheritance: Passing Genes", font_size=40, color=GOLD_ACCENT).to_corner(UL)
        self.play(Write(inheritance_title))

        # Parent 1 (Blue themed DNA)
        parent1_dna_segment = VGroup(
            Line(LEFT*0.2, LEFT*0.2 + UP*1.5, color=BLUE_ACCENT, stroke_width=4),
            Line(RIGHT*0.2, RIGHT*0.2 + UP*1.5, color=BLUE_ACCENT, stroke_width=4),
            VGroup(*[Line(LEFT*0.2, RIGHT*0.2, color=GOLD_ACCENT).shift(UP*(i*0.4)) for i in range(4)])
        ).scale(0.8).shift(LEFT*3.5 + UP*1)
        parent1_text = Text("Parent 1", font_size=28, color=BLUE_ACCENT).next_to(parent1_dna_segment, DOWN, buff=0.3)
        
        # Parent 2 (Gold themed DNA) - slightly different pattern for visual distinction
        parent2_dna_segment = VGroup(
            Line(LEFT*0.2, LEFT*0.2 + UP*1.5, color=GOLD_ACCENT, stroke_width=4),
            Line(RIGHT*0.2, RIGHT*0.2 + UP*1.5, color=GOLD_ACCENT, stroke_width=4),
            VGroup(*[Line(LEFT*0.2, RIGHT*0.2, color=BLUE_ACCENT).shift(UP*(i*0.4)) for i in range(4)])
        ).scale(0.8).shift(RIGHT*3.5 + UP*1)
        parent2_text = Text("Parent 2", font_size=28, color=GOLD_ACCENT).next_to(parent2_dna_segment, DOWN, buff=0.3)

        self.play(FadeIn(parent1_dna_segment, parent1_text, parent2_dna_segment, parent2_text))

        # Offspring DNA - visually represents a combination
        offspring_dna_segment = VGroup(
            Line(LEFT*0.2, LEFT*0.2 + UP*1.5, color=BLUE_ACCENT, stroke_width=4), # One backbone from P1
            Line(RIGHT*0.2, RIGHT*0.2 + UP*1.5, color=GOLD_ACCENT, stroke_width=4), # One backbone from P2
            VGroup(
                Line(LEFT*0.2, RIGHT*0.2, color=GOLD_ACCENT).shift(UP*(0*0.4)), # Mix of base patterns
                Line(LEFT*0.2, RIGHT*0.2, color=BLUE_ACCENT).shift(UP*(1*0.4)),
                Line(LEFT*0.2, RIGHT*0.2, color=GOLD_ACCENT).shift(UP*(2*0.4)),
                Line(LEFT*0.2, RIGHT*0.2, color=BLUE_ACCENT).shift(UP*(3*0.4)),
            )
        ).scale(0.8).shift(DOWN*1.5)
        offspring_text = Text("Offspring", font_size=28, color=TEXT_COLOR).next_to(offspring_dna_segment, DOWN, buff=0.3)

        # Arrows showing genetic contribution
        p1_arrow = Arrow(parent1_dna_segment.get_bottom(), offspring_dna_segment.get_top() + LEFT*0.5, color=BLUE_ACCENT, buff=0.2)
        p2_arrow = Arrow(parent2_dna_segment.get_bottom(), offspring_dna_segment.get_top() + RIGHT*0.5, color=GOLD_ACCENT, buff=0.2)
        
        self.play(Create(p1_arrow), Create(p2_arrow))
        self.play(FadeIn(offspring_dna_segment, offspring_text))
        
        inherit_desc_1 = Text("Offspring receive a combination", font_size=32, color=TEXT_COLOR).to_corner(DR).shift(UP*0.5)
        inherit_desc_2 = Text("of genes from both parents.", font_size=32, color=TEXT_COLOR).next_to(inherit_desc_1, DOWN, buff=0.2)

        self.play(Write(inherit_desc_1), FadeIn(inherit_desc_2, shift=DOWN))
        self.wait(2)

        self.play(
            FadeOut(parent1_dna_segment, parent1_text, parent2_dna_segment, parent2_text,
                    offspring_dna_segment, offspring_text, p1_arrow, p2_arrow,
                    inherit_desc_1, inherit_desc_2, inheritance_title)
        )

        # --- Beat 5: Recap ---
        recap_title = Text("Recap", font_size=50, color=GOLD_ACCENT).to_corner(UL).shift(RIGHT*1.5)
        self.play(Write(recap_title))

        # Bullet points for recap
        recap_points = VGroup(
            VGroup(BulletPoint().scale(0.7).set_color(BLUE_ACCENT), MathTex("\\text{DNA: The genetic blueprint of life.}", color=TEXT_COLOR)),
            VGroup(BulletPoint().scale(0.7).set_color(BLUE_ACCENT), MathTex("\\text{Genes: Segments of DNA coding for traits.}", color=TEXT_COLOR)),
            VGroup(BulletPoint().scale(0.7).set_color(BLUE_ACCENT), MathTex("\\text{Inheritance: Passing genes from parents to offspring.}", color=TEXT_COLOR))
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(recap_title, DOWN, buff=0.8, aligned_edge=LEFT)

        for point_group in recap_points:
            self.play(FadeIn(point_group, shift=RIGHT), run_time=0.8)
            self.wait(0.5)
        
        self.wait(1.5)
        
        # Final module title card
        final_module_title = Text("Module: Genetic Information and Inheritance", font_size=40, color=BLUE_ACCENT).to_edge(DOWN)
        self.play(FadeOut(recap_points, recap_title), FadeIn(final_module_title, shift=UP))
        self.wait(2)