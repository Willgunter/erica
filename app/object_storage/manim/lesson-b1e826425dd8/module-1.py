from manim import *

class CellIntroduction(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE # Default Manim blue
        GOLD_ACCENT = GOLD # Classic gold
        TEXT_COLOR = WHITE
        SUB_TEXT_COLOR = LIGHT_GREY

        # --- Beat 1: The Fundamental Unit (Visual Hook & Cell Theory) ---
        
        # Visual Hook: A single point of life expanding
        initial_dot = Dot(color=BLUE_ACCENT, radius=0.05).scale(0.5)
        self.add(initial_dot)
        self.play(initial_dot.animate.scale(3).set_color(GOLD_ACCENT), run_time=0.8) # Pulsating effect

        # Form a basic cell outline and internal components
        cell_outline = Circle(radius=0.8, color=BLUE_ACCENT, stroke_width=3).move_to(initial_dot.get_center())
        cell_interior_dots = VGroup(*[Dot(radius=0.03, color=BLUE_ACCENT).move_to(cell_outline.get_center() + np.random.uniform(-0.4, 0.4, 3)) for _ in range(10)])
        cell_interior_dots.add(VGroup(*[Dot(radius=0.04, color=GOLD_ACCENT).move_to(cell_outline.get_center() + np.random.uniform(-0.4, 0.4, 3)) for _ in range(5)]))
        cell_interior_dots.set_opacity(0.7)

        self.play(
            ReplacementTransform(initial_dot, cell_outline),
            FadeIn(cell_interior_dots, scale=0.5),
            run_time=1.5
        )
        basic_cell = VGroup(cell_outline, cell_interior_dots)

        # Title
        title = Text("Cells: The Fundamental Unit of Life", color=TEXT_COLOR).scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Cell Theory Postulate 1: All living things are made of cells.
        postulate1_text = Text("1. All living things are made of cells.", color=SUB_TEXT_COLOR).scale(0.6).next_to(title, DOWN, buff=0.5).align_left(title)
        self.play(FadeIn(postulate1_text, shift=UP))
        self.wait(0.5)

        # Create copies around the original cell to show 'many cells'
        cell_copies = VGroup()
        for i in range(3): # Create 3 copies
            copy = basic_cell.copy().scale(0.7)
            cell_copies.add(copy)
        
        # Position them relative to the original cell, which also shrinks and moves
        self.play(
            basic_cell.animate.scale(0.7).shift(LEFT*1.8 + UP*0.5), # Original cell also becomes part of the group
            FadeIn(cell_copies[0].shift(RIGHT*0.5 + UP*1.2)),
            FadeIn(cell_copies[1].shift(RIGHT*1.8 + DOWN*0.5)),
            FadeIn(cell_copies[2].shift(LEFT*0.5 + DOWN*1.2)),
            run_time=1.8
        )
        
        # Now collect all cells into one group for subsequent operations
        all_cells = VGroup(basic_cell, cell_copies[0], cell_copies[1], cell_copies[2])
        self.wait(0.5)

        # Cell Theory Postulate 2: Cells are the basic unit of life.
        postulate2_text = Text("2. Cells are the basic unit of life.", color=SUB_TEXT_COLOR).scale(0.6).next_to(postulate1_text, DOWN, buff=0.3).align_left(postulate1_text)
        
        # Highlight one cell by zooming it, fading others
        target_cell_for_zoom = all_cells[0].copy() # Pick the first cell
        
        self.play(
            FadeIn(postulate2_text, shift=UP),
            FadeOut(VGroup(*[c for i, c in enumerate(all_cells) if i != 0])), # Fade out other cells
            Transform(all_cells[0], target_cell_for_zoom.scale(1.8).center()), # Zoom the selected cell
            run_time=1.5
        )
        single_highlight_cell = all_cells[0] # Store the zoomed cell
        self.wait(0.5)

        # Cell Theory Postulate 3: All cells come from pre-existing cells.
        postulate3_text = Text("3. All cells come from pre-existing cells.", color=SUB_TEXT_COLOR).scale(0.6).next_to(postulate2_text, DOWN, buff=0.3).align_left(postulate2_text)
        self.play(FadeIn(postulate3_text, shift=UP))
        self.wait(0.5)

        # Animate cell division (simplified)
        dividing_line = Line(single_highlight_cell.get_top(), single_highlight_cell.get_bottom(), color=GOLD_ACCENT, stroke_width=4)
        self.play(Create(dividing_line), run_time=0.8)
        
        # Animate the split: original cell moves left, a new cell (copy of original) appears and moves right
        daughter_cell_right_copy = single_highlight_cell.copy() # Create a copy to be the 'right' daughter
        self.play(
            single_highlight_cell.animate.shift(LEFT * 0.8), # Original cell moves left
            daughter_cell_right_copy.animate.shift(RIGHT * 0.8), # Copy moves right
            FadeOut(dividing_line),
            run_time=1.5
        )
        
        current_cells_post3 = VGroup(single_highlight_cell, daughter_cell_right_copy)
        all_postulate_texts = VGroup(postulate1_text, postulate2_text, postulate3_text)
        
        self.wait(1)
        self.play(FadeOut(all_postulate_texts, title, current_cells_post3))
        self.wait(0.5)

        # --- Beat 2: Structure - Prokaryotic vs. Eukaryotic ---
        # Prokaryotic cell: simple structure
        prokaryote_outline = Circle(radius=1, color=BLUE_ACCENT, stroke_width=3)
        prokaryote_dna = Dot(color=GOLD_ACCENT, radius=0.1).shift(RIGHT*0.2) # Simple DNA clump
        prokaryote_ribosomes = VGroup(*[Dot(radius=0.05, color=BLUE_ACCENT).shift(cell_point) for cell_point in [UL*0.5, DR*0.6, UR*0.3, DL*0.4]])
        
        prokaryotic_cell = VGroup(prokaryote_outline, prokaryote_dna, prokaryote_ribosomes).center()
        prokaryotic_label = Text("Prokaryotic Cell", color=TEXT_COLOR).scale(0.7).next_to(prokaryotic_cell, DOWN, buff=0.5)
        
        self.play(FadeIn(prokaryotic_cell, shift=UP*0.5), Write(prokaryotic_label))
        self.wait(1)

        # Transform to Eukaryotic cell: complex organization with organelles
        eukaryote_outline = Circle(radius=1.5, color=BLUE_ACCENT, stroke_width=3).center()
        nucleus_outline = Circle(radius=0.6, color=GOLD_ACCENT, stroke_width=3)
        nucleus_dna = Dot(color=BLUE_ACCENT, radius=0.08).shift(nucleus_outline.get_center() + UP*0.1 + LEFT*0.1) # Represent DNA inside nucleus
        
        # Organelles
        mitochondria = Ellipse(width=0.8, height=0.4, color=BLUE_ACCENT, stroke_width=2).shift(UR*1.2)
        er_lines = VGroup(
            Line(LEFT*0.3, RIGHT*0.3, color=GOLD_ACCENT).shift(DL*1.2 + LEFT*0.3),
            Line(LEFT*0.4, RIGHT*0.4, color=GOLD_ACCENT).shift(DL*1.2 + RIGHT*0.3),
            Line(LEFT*0.35, RIGHT*0.35, color=GOLD_ACCENT).shift(DL*1.2)
        ).set_stroke(width=2) # Rough ER representation
        golgi_apparatus = VGroup(
            RoundedRectangle(width=0.6, height=0.2, corner_radius=0.05, color=BLUE_ACCENT).shift(UP*0.5 + LEFT*1.2),
            RoundedRectangle(width=0.7, height=0.2, corner_radius=0.05, color=BLUE_ACCENT).shift(UP*0.2 + LEFT*1.2),
            RoundedRectangle(width=0.65, height=0.2, corner_radius=0.05, color=BLUE_ACCENT).shift(DOWN*0.1 + LEFT*1.2)
        ).set_stroke(width=2) # Golgi representation

        eukaryotic_cell = VGroup(
            eukaryote_outline,
            VGroup(nucleus_outline, nucleus_dna), # Nucleus
            mitochondria, er_lines, golgi_apparatus
        )
        eukaryotic_label = Text("Eukaryotic Cell", color=TEXT_COLOR).scale(0.7).next_to(eukaryotic_cell, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(prokaryotic_cell, eukaryotic_cell),
            TransformMatchingTex(prokaryotic_label, eukaryotic_label),
            run_time=2
        )
        self.wait(1)

        self.play(FadeOut(eukaryotic_cell, eukaryotic_label))
        self.wait(0.5)

        # --- Beat 3: Function - Membrane Transport (Linear Algebra Analogy) ---
        membrane_title = Text("Membrane Transport: Regulating Flow", color=TEXT_COLOR).scale(0.8).to_edge(UP)
        self.play(Write(membrane_title))
        self.wait(0.5)

        # NumberPlane to show spatial context for particle movement
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=10, y_length=6,
            axis_config={"color": SUB_TEXT_COLOR},
            background_line_style={"stroke_color": DARK_GREY, "stroke_width": 1, "stroke_opacity": 0.6}
        ).shift(DOWN*0.5)
        
        membrane = Rectangle(width=0.2, height=6, color=BLUE_ACCENT, fill_opacity=0.8).move_to(plane.get_center())
        
        # Particles on either side, representing concentration difference
        left_particles = VGroup(*[
            Dot(plane.coords_to_point(np.random.uniform(-4, -0.5), np.random.uniform(-3, 3)), radius=0.08, color=GOLD_ACCENT)
            for _ in range(20)
        ])
        right_particles = VGroup(*[
            Dot(plane.coords_to_point(np.random.uniform(0.5, 4), np.random.uniform(-3, 3)), radius=0.08, color=BLUE_ACCENT)
            for _ in range(5)
        ])
        
        self.play(Create(plane), FadeIn(membrane))
        self.play(FadeIn(left_particles, scale=0.5), FadeIn(right_particles, scale=0.5))
        self.wait(0.5)

        # Animate diffusion/transport with arrows and particle movement
        arrows_out = VGroup(*[Arrow(p.get_center(), p.get_center() + RIGHT*0.8, buff=0, max_stroke_width_to_length_ratio=4, color=GOLD_ACCENT, tip_length=0.2) for p in left_particles[:5]])
        arrows_in = VGroup(*[Arrow(p.get_center(), p.get_center() + LEFT*0.8, buff=0, max_stroke_width_to_length_ratio=4, color=BLUE_ACCENT, tip_length=0.2) for p in right_particles[:2]])
        
        self.play(GrowArrow(arrows_out[0]), GrowArrow(arrows_in[0])) # Show example flow arrows
        
        # Select some particles to cross the membrane
        crossing_particles_gold = left_particles[0:5]
        crossing_particles_blue = right_particles[0:2]

        # Animate crossing with slight random movement (akin to molecular motion)
        self.play(
            LaggedStart(
                *[
                    ApplyMethod(p.animate.shift(RIGHT*np.random.uniform(2, 3) + UP*np.random.uniform(-0.5,0.5)), run_time=1.5)
                    for p in crossing_particles_gold
                ],
                *[
                    ApplyMethod(p.animate.shift(LEFT*np.random.uniform(2, 3) + DOWN*np.random.uniform(-0.5,0.5)), run_time=1.5)
                    for p in crossing_particles_blue
                ],
                lag_ratio=0.1
            ),
            FadeOut(arrows_out, arrows_in) # Fade out initial arrows
        )
        self.wait(0.5)
        
        self.play(FadeOut(plane, membrane, left_particles, right_particles, crossing_particles_gold, crossing_particles_blue, membrane_title))
        self.wait(0.5)

        # --- Beat 4: DNA - The Blueprint (Information Storage) ---
        dna_title = Text("DNA: The Instruction Manual", color=TEXT_COLOR).scale(0.8).to_edge(UP)
        self.play(Write(dna_title))
        self.wait(0.5)

        # A simplified nucleus
        nucleus_core = Circle(radius=1.2, color=GOLD_ACCENT, stroke_width=3).center().shift(DOWN*0.5)
        nucleus_label = Text("Nucleus", color=SUB_TEXT_COLOR).scale(0.5).next_to(nucleus_core, UP)
        self.play(Create(nucleus_core), Write(nucleus_label))
        self.wait(0.5)

        # Create a simplified DNA helix using Line objects for strands and connections (bases)
        num_points = 30
        helix_height = 2
        helix_radius = 0.5
        
        strand1_points = []
        strand2_points = []
        
        for i in range(num_points):
            z = helix_height * (i / (num_points - 1)) - helix_height/2 # Y-axis in 2D Manim
            angle = i / (num_points - 1) * 4 * PI # 2 full turns
            x1 = helix_radius * np.cos(angle)
            x2 = helix_radius * np.cos(angle + PI) # Opposite side
            
            strand1_points.append(nucleus_core.get_center() + np.array([x1, z, 0]))
            strand2_points.append(nucleus_core.get_center() + np.array([x2, z, 0]))

        strand1 = VGroup(*[Line(strand1_points[i], strand1_points[i+1], color=BLUE_ACCENT, stroke_width=4) for i in range(len(strand1_points)-1)])
        strand2 = VGroup(*[Line(strand2_points[i], strand2_points[i+1], color=GOLD_ACCENT, stroke_width=4) for i in range(len(strand2_points)-1)])
        
        # Add 'bases' as lines connecting strands
        bases = VGroup()
        for i in range(0, num_points, 3): # Connect every 3rd point for visual clarity
            if i < num_points - 1:
                base_line = Line(strand1_points[i], strand2_points[i], color=LIGHT_GREY, stroke_width=2)
                bases.add(base_line)

        dna_helix = VGroup(strand1, strand2, bases).move_to(nucleus_core.get_center())
        
        self.play(
            ReplacementTransform(nucleus_core, dna_helix), # Transform the nucleus itself into the helix
            FadeOut(nucleus_label),
            run_time=2
        )
        self.wait(1)

        # Information flow analogy: dots moving along the helix
        info_dots = VGroup(*[Dot(color=TEXT_COLOR, radius=0.05).move_to(dna_helix.get_bottom() + UP*0.1 + LEFT*(i%2)*0.1) for i in range(3)])
        
        self.play(FadeIn(info_dots))
        self.play(
            info_dots.animate.shift(UP * 2.2 + RIGHT * 0.2), # Move up to the top of the helix with slight shift
            LaggedStart(*[ApplyMethod(d.animate.shift(RIGHT*0.2*(i%2 == 0) - RIGHT*0.2*(i%2 != 0)), run_time=1.5) for i, d in enumerate(info_dots)], lag_ratio=0.5), # Slight side wobble
            run_time=2.5
        )
        self.wait(0.5)
        
        self.play(FadeOut(dna_helix, dna_title, info_dots))
        self.wait(0.5)

        # --- Beat 5: Recap ---
        recap_title = Text("Recap:", color=TEXT_COLOR).scale(0.9).to_edge(UP)
        self.play(Write(recap_title))
        
        recap_points = VGroup(
            BulletText("Cells are fundamental units of life.", font_size=36, color=SUB_TEXT_COLOR),
            BulletText("Two main types: Prokaryotic & Eukaryotic (simple vs. complex).", font_size=36, color=SUB_TEXT_COLOR),
            BulletText("Membranes regulate flow of substances.", font_size=36, color=SUB_TEXT_COLOR),
            BulletText("DNA stores genetic instructions.", font_size=36, color=SUB_TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(recap_title, DOWN, buff=0.8)

        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.5) for p in recap_points], lag_ratio=0.5))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_points))
        self.wait(1)