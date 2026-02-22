from manim import *
import random # For random position and angle generation

# Set custom colors and background
config.background_color = "#1A1A1A"  # Clean dark background
BLUE_ACCENT = "#87CEEB"             # High-contrast blue
GOLD_ACCENT = "#FFD700"             # High-contrast gold

class CellBasicsAnimation(Scene):
    def construct(self):
        self.camera.background_color = config.background_color # Ensure background color is set for the scene
        
        # --- 0. Visual Hook: Life's Fundamental Units ---
        # Start with a scatter of "protocell" dots
        many_dots = VGroup(*[
            Dot(point=[random.uniform(-FRAME_WIDTH/2, FRAME_WIDTH/2), random.uniform(-FRAME_HEIGHT/2, FRAME_HEIGHT/2), 0], 
                radius=0.05, color=BLUE_ACCENT, opacity=0.7) 
            for _ in range(150)
        ])
        self.play(FadeIn(many_dots))

        # Coalesce and form a structured cluster, symbolizing organization
        target_cluster = VGroup(*[Dot(radius=0.05, color=BLUE_ACCENT) for _ in range(150)]).arrange_in_grid(rows=10, cols=15, buff=0.1).scale(0.8).to_center()
        
        self.play(Transform(many_dots, target_cluster), run_time=1.5)
        self.play(many_dots.animate.set_color(GOLD_ACCENT).scale(1.2), run_time=0.5)

        # Introduce the idea of fundamental building blocks
        hook_text = Text("Life's Fundamental Units", font_size=48, color=GOLD_ACCENT).next_to(many_dots, DOWN*2)
        self.play(Write(hook_text))
        self.wait(1)
        self.play(FadeOut(many_dots, hook_text))


        # --- Beat 1: Cell Theory - The Fundamental Unit ---
        title1 = Text("Beat 1: The Fundamental Unit", font_size=36, color=GOLD_ACCENT).to_corner(UL)
        self.play(FadeIn(title1, shift=UP))

        # Introduce a basic cell as a blueprint
        blueprint_cell = Circle(radius=1.5, color=BLUE_ACCENT, stroke_width=4).to_center()
        self.play(GrowFromCenter(blueprint_cell))
        self.wait(0.5)

        # Show it as a unit that replicates and forms larger structures
        cell_replicas = VGroup(*[
            Circle(radius=0.4, color=BLUE_ACCENT, fill_opacity=0.1, stroke_width=2).move_to(
                blueprint_cell.get_center() + np.array([random.uniform(-3,3), random.uniform(-2,2), 0])
            ) for _ in range(15)
        ])
        
        cell_theory_statement1 = Text("Cells are the fundamental units of life.", font_size=32, color=BLUE_ACCENT)
        cell_theory_statement2 = Text("All living things are made of cells.", font_size=32, color=BLUE_ACCENT)
        cell_theory_statement3 = Text("New cells come from existing cells.", font_size=32, color=BLUE_ACCENT)
        
        cell_theory_group_text = VGroup(
            cell_theory_statement1, 
            cell_theory_statement2, 
            cell_theory_statement3
        ).arrange(DOWN, buff=0.4).to_edge(RIGHT).shift(LEFT*0.5)

        self.play(
            blueprint_cell.animate.scale(0.4).to_corner(UL).shift(RIGHT*1 + DOWN*0.5),
            LaggedStart(*[FadeIn(c) for c in cell_replicas], lag_ratio=0.05, run_time=1.5)
        )
        self.play(Write(cell_theory_group_text[0], run_time=1))
        self.play(Write(cell_theory_group_text[1], run_time=1))
        self.play(Write(cell_theory_group_text[2], run_time=1))

        cell_theory_title = Text("Cell Theory", font_size=48, color=GOLD_ACCENT).next_to(cell_theory_group_text, UP*2)
        self.play(FadeIn(cell_theory_title, shift=UP))
        self.wait(1.5)

        self.play(FadeOut(blueprint_cell, cell_replicas, cell_theory_group_text, cell_theory_title, title1))


        # --- Beat 2: Basic Cell Structure ---
        title2 = Text("Beat 2: Basic Cell Structure", font_size=36, color=GOLD_ACCENT).to_corner(UL)
        self.play(FadeIn(title2, shift=UP))

        # Draw a larger, central cell for dissection
        cell_outer = Circle(radius=2.5, color=BLUE_ACCENT, stroke_width=5)
        cell_inner_fill = Circle(radius=2.4, color=BLUE_ACCENT, fill_opacity=0.1)
        main_cell = VGroup(cell_outer, cell_inner_fill).to_center()
        self.play(GrowFromCenter(main_cell))

        # Cell Membrane
        membrane_label = Text("Cell Membrane", color=GOLD_ACCENT).next_to(main_cell, RIGHT*2 + UP*0.5)
        membrane_arrow = Arrow(membrane_label.get_left(), main_cell.get_right() + UP*0.5, buff=0.1, color=GOLD_ACCENT)
        
        # Highlight the membrane
        membrane_focus = Annulus(inner_radius=cell_outer.radius - 0.1, outer_radius=cell_outer.radius, 
                                 color=BLUE_ACCENT, fill_opacity=0.5, stroke_width=0)
        self.play(Write(membrane_label), GrowArrow(membrane_arrow), FadeIn(membrane_focus))
        self.wait(0.8)
        self.play(FadeOut(membrane_focus)) # remove highlight

        # Cytoplasm
        cytoplasm_label = Text("Cytoplasm", color=GOLD_ACCENT).next_to(main_cell, RIGHT*2 + DOWN*0.5)
        cytoplasm_arrow = Arrow(cytoplasm_label.get_left(), main_cell.get_center() + LEFT * (main_cell.radius - 0.5) + DOWN*0.5, 
                                buff=0.1, color=GOLD_ACCENT)

        cytoplasm_particles = VGroup(*[Dot(point=main_cell.point_at_angle(random.uniform(0, 2*PI)) * random.uniform(0.1, 0.9), 
                                          radius=0.06, color=BLUE_ACCENT, opacity=0.6) for _ in range(70)])
        self.play(Write(cytoplasm_label), GrowArrow(cytoplasm_arrow), FadeIn(cytoplasm_particles))
        self.wait(1.2)

        self.play(FadeOut(membrane_label, membrane_arrow, cytoplasm_label, cytoplasm_arrow, cytoplasm_particles, title2))


        # --- Beat 3: Introducing Organelles - Specialized Compartments ---
        title3 = Text("Beat 3: Specialized Compartments", font_size=36, color=GOLD_ACCENT).to_corner(UL)
        self.play(FadeIn(title3, shift=UP))

        organelle_concept_text = Text("Internal 'mini-organs' with specific jobs.", color=BLUE_ACCENT, font_size=32).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(organelle_concept_text))

        # Transform main_cell to be smaller and centered
        main_cell.generate_target()
        main_cell.target.scale(0.8).to_center()
        self.play(MoveToTarget(main_cell))

        # Show various abstract shapes appearing inside the cell
        organelle1 = Circle(radius=0.7, color=GOLD_ACCENT, fill_opacity=0.6, stroke_width=2).shift(LEFT*1.2 + UP*1)
        organelle2 = Ellipse(width=1.5, height=0.8, color=BLUE_ACCENT, fill_opacity=0.6, stroke_width=2).shift(RIGHT*1.5 + DOWN*0.5)
        organelle3 = Polygon(ORIGIN, UP*0.5, RIGHT*0.7, DOWN*0.3, color=GOLD_ACCENT, fill_opacity=0.6, stroke_width=2).shift(LEFT*1 + DOWN*1.5).scale(0.8)
        organelle4 = Square(side_length=0.6, color=BLUE_ACCENT, fill_opacity=0.6, stroke_width=2).shift(RIGHT*0.5 + UP*1.8)

        organelles = VGroup(organelle1, organelle2, organelle3, organelle4)
        
        self.play(LaggedStart(*[GrowFromCenter(o) for o in organelles], lag_ratio=0.2, run_time=2))

        organelle_label = Text("Organelles", color=GOLD_ACCENT, font_size=48).next_to(main_cell, DOWN*3)
        self.play(Write(organelle_label))
        self.wait(1)

        self.play(FadeOut(organelle_concept_text, organelle_label, main_cell, organelles, title3))


        # --- Beat 4: Key Organelles in Action - Nucleus & Mitochondrion ---
        title4 = Text("Beat 4: Key Organelles in Action", font_size=36, color=GOLD_ACCENT).to_corner(UL)
        self.play(FadeIn(title4, shift=UP))

        # Nucleus (control center)
        nucleus_outer = Circle(radius=0.8, color=GOLD_ACCENT, stroke_width=3, fill_opacity=0.3).shift(LEFT*3)
        nucleus_inner = Circle(radius=0.3, color=BLUE_ACCENT, fill_opacity=0.8).move_to(nucleus_outer.get_center())
        nucleus_body = VGroup(nucleus_outer, nucleus_inner)

        nucleus_label = Text("Nucleus", color=GOLD_ACCENT).next_to(nucleus_body, UP)
        nucleus_function = Text("Control Center (DNA)", color=BLUE_ACCENT, font_size=28).next_to(nucleus_body, DOWN)

        self.play(GrowFromCenter(nucleus_body), Write(nucleus_label), Write(nucleus_function))
        
        # Simulate information flow (DNA instructions)
        dna_line_start = nucleus_inner.get_top()
        dna_line_end = nucleus_inner.get_top() + UP*0.8
        dna_pulse_line = Line(dna_line_start, dna_line_end, color=BLUE_ACCENT, stroke_width=4)
        
        self.play(ShowPassingFlash(dna_pulse_line, time_width=0.5, run_time=1.5, rate_func=linear))
        self.wait(0.5)

        # Mitochondrion (powerhouse)
        mitochondria_shape = Ellipse(width=1.8, height=0.9, color=GOLD_ACCENT, stroke_width=3, fill_opacity=0.3).shift(RIGHT*3)
        # Inner folds (cristae)
        cristae = VGroup(
            Line(mitochondria_shape.get_left() + UP * 0.2, mitochondria_shape.get_right() + UP * 0.1, color=BLUE_ACCENT, stroke_width=2),
            Line(mitochondria_shape.get_left() + DOWN * 0.2, mitochondria_shape.get_right() + DOWN * 0.1, color=BLUE_ACCENT, stroke_width=2),
            Line(mitochondria_shape.get_left() + UP * 0.4, mitochondria_shape.get_right() + UP * 0.3, color=BLUE_ACCENT, stroke_width=2),
            Line(mitochondria_shape.get_left() + DOWN * 0.4, mitochondria_shape.get_right() + DOWN * 0.3, color=BLUE_ACCENT, stroke_width=2)
        )
        mitochondria_body = VGroup(mitochondria_shape, cristae)
        mitochondria_label = Text("Mitochondrion", color=GOLD_ACCENT).next_to(mitochondria_body, UP)
        mitochondria_function = Text("Energy Production", color=BLUE_ACCENT, font_size=28).next_to(mitochondria_body, DOWN)

        self.play(GrowFromCenter(mitochondria_body), Write(mitochondria_label), Write(mitochondria_function))

        # Simulate energy output with expanding rings
        energy_rings = VGroup()
        for i in range(3):
            ring = Circle(radius=0.2 + i*0.3, color=GOLD_ACCENT, stroke_width=3, opacity=1 - i*0.3).move_to(mitochondria_body.get_center())
            energy_rings.add(ring)
        
        self.play(
            LaggedStart(
                Succession(
                    GrowFromCenter(energy_rings[0]),
                    Transform(energy_rings[0], Circle(radius=1.2, color=GOLD_ACCENT, stroke_width=1, opacity=0).move_to(mitochondria_body.get_center()), run_time=1.2)
                ),
                Succession(
                    GrowFromCenter(energy_rings[1]),
                    Transform(energy_rings[1], Circle(radius=1.2, color=GOLD_ACCENT, stroke_width=1, opacity=0).move_to(mitochondria_body.get_center()), run_time=1.2)
                ),
                Succession(
                    GrowFromCenter(energy_rings[2]),
                    Transform(energy_rings[2], Circle(radius=1.2, color=GOLD_ACCENT, stroke_width=1, opacity=0).move_to(mitochondria_body.get_center()), run_time=1.2)
                ),
                lag_ratio=0.3, run_time=2.5
            )
        )
        self.wait(1)

        self.play(FadeOut(nucleus_body, nucleus_label, nucleus_function, mitochondria_body, mitochondria_label, mitochondria_function, title4))

        # --- Recap Card ---
        recap_title = Text("Recap: Cell Basics", font_size=60, color=GOLD_ACCENT).to_edge(UP).shift(DOWN*0.5)
        
        recap_bullet1 = MathTex(r"\bullet \text{ Cells: Fundamental building blocks of life}", font_size=36, color=BLUE_ACCENT)
        recap_bullet2 = MathTex(r"\bullet \text{ Basic Structure: Cell Membrane, Cytoplasm}", font_size=36, color=BLUE_ACCENT)
        recap_bullet3 = MathTex(r"\bullet \text{ Organelles: Specialized internal components}", font_size=36, color=BLUE_ACCENT)
        recap_bullet4 = MathTex(r"\bullet \text{ E.g., Nucleus (Control), Mitochondrion (Energy)}", font_size=36, color=BLUE_ACCENT)

        recap_group_bullets = VGroup(recap_bullet1, recap_bullet2, recap_bullet3, recap_bullet4).arrange(DOWN, buff=0.7).to_center().shift(DOWN*0.5)
        
        self.play(Write(recap_title))
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.5) for b in recap_group_bullets], lag_ratio=0.3, run_time=2))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_group_bullets))