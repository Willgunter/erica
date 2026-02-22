from manim import *

class CellStructureAnimation(Scene):
    def construct(self):
        # Set up a dark background for 3B1B style
        self.camera.background_color = BLACK

        # --- Beat 0: Visual Hook - From chaos to structure ---
        # Represent primitive components as dots
        num_dots = 100
        dots = VGroup(*[Dot(point=np.random.rand(3) * 8 - 4, radius=0.03)
                        for _ in range(num_dots)])
        dots.set_color(BLUE_C)

        # Target shape for the initial cell concept (stroke only)
        # This will be the shape the dots converge to.
        initial_cell_shape_stroke = Ellipse(width=3, height=2, stroke_width=4, stroke_color=BLUE_C).move_to(ORIGIN)

        # Animate dots coalescing into the initial cell outline
        self.play(
            LaggedStart(*[dot.animate.move_to(initial_cell_shape_stroke.point_at_percent(np.random.rand()))
                          for dot in dots]),
            run_time=3
        )
        self.play(
            Transform(dots, initial_cell_shape_stroke), # dots transform into the outline
            run_time=2
        )
        self.wait(0.5)

        # Now, 'dots' effectively *is* initial_cell_shape_stroke. Let's use this as our main cell object.
        main_cell = dots 

        # Fill the main cell and set its properties for the next beats
        self.play(
            main_cell.animate.set_fill(color=BLUE_C, opacity=0.1).set_stroke(color=BLUE_C, width=4),
            run_time=1
        )
        self.wait(0.5)

        # --- Beat 1: Cell Theory - Foundational Units ---
        title = MathTex("Cells: \\text{The Foundational Units of Life}", font_size=50)
        title.set_color(GOLD_C)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Scale down the main_cell to fit in a group
        self.play(
            main_cell.animate.scale(0.8),
            run_time=1
        )
        self.wait(0.5)

        # Create a group starting with the scaled main_cell
        cell_group_elements = [main_cell]
        for _ in range(3): # Create 3 more copies
            cell_group_elements.append(main_cell.copy())
        
        cell_group = VGroup(*cell_group_elements)
        cell_group.arrange(RIGHT, buff=0.8).move_to(ORIGIN) # Arrange them

        # Animate the copies appearing from the original main_cell
        self.play(
            LaggedStart(*[TransformFromCopy(main_cell, cell_group[i]) for i in range(1, len(cell_group))],
                        lag_ratio=0.5, run_time=2)
        )
        self.wait(1)

        cell_theory_text = Text("All life is made of cells", font_size=36)
        cell_theory_text.set_color(BLUE_E)
        cell_theory_text.next_to(cell_group, DOWN, buff=0.7)
        
        self.play(Write(cell_theory_text))
        self.wait(1.5)

        # Clear Beat 1 for Beat 2, focusing back on the first cell in the group
        first_cell_in_group = cell_group[0]
        self.play(
            FadeOut(title),
            FadeOut(cell_theory_text),
            *[FadeOut(cell_group[i]) for i in range(1, len(cell_group))], # Fade out copies
            first_cell_in_group.animate.move_to(ORIGIN).scale(1/0.8) # Move the first cell to center and scale back
        )
        self.wait(0.5)

        # Now, first_cell_in_group is the main cell for Beat 2
        # We need to explicitly add it to the scene, as it was part of a VGroup that was partly faded out.
        # It's already been transformed in the last play, so we just refer to it.
        main_cell = first_cell_in_group 
        self.add(main_cell) # Ensure it's active in the scene's Mobject list
        
        # --- Beat 2: Basic Cell Structure (Membrane, Cytoplasm, Nucleus) ---
        membrane_label = Text("Cell Membrane", font_size=28).set_color(WHITE).next_to(main_cell, RIGHT, buff=0.5)
        membrane_arrow = Arrow(membrane_label.get_left(), main_cell.get_right(), buff=0.1, color=BLUE_C)

        # The main_cell already represents the membrane, so we just label it.
        self.play(
            FadeIn(membrane_label, shift=LEFT),
            GrowArrow(membrane_arrow)
        )
        self.wait(1)

        cytoplasm = Ellipse(width=2.8, height=1.8, stroke_width=0, fill_color=GRAY_B, fill_opacity=0.8)
        cytoplasm_label = Text("Cytoplasm", font_size=28).set_color(WHITE).next_to(cytoplasm, DOWN, buff=0.5)
        cytoplasm_arrow = Arrow(cytoplasm_label.get_top(), cytoplasm.get_bottom(), buff=0.1, color=GRAY_B)

        self.play(
            Create(cytoplasm),
            FadeIn(cytoplasm_label, shift=UP),
            GrowArrow(cytoplasm_arrow),
            run_time=2
        )
        self.wait(1)

        nucleus = Circle(radius=0.5, stroke_width=0, fill_color=GOLD_C, fill_opacity=0.9).move_to(ORIGIN)
        nucleus_label = Text("Nucleus", font_size=28).set_color(WHITE).next_to(nucleus, UP, buff=0.5)
        nucleus_arrow = Arrow(nucleus_label.get_bottom(), nucleus.get_top(), buff=0.1, color=GOLD_C)

        self.play(
            Create(nucleus),
            FadeIn(nucleus_label, shift=DOWN),
            GrowArrow(nucleus_arrow),
            run_time=2
        )
        self.wait(1.5)

        # Group basic structures and labels
        basic_structure_group = VGroup(main_cell, cytoplasm, nucleus,
                                       membrane_label, membrane_arrow,
                                       cytoplasm_label, cytoplasm_arrow,
                                       nucleus_label, nucleus_arrow)
        
        # --- Beat 3: Organelles - Internal Machinery ---
        # Shrink and move the basic structure to make room for organelles
        self.play(
            basic_structure_group.animate.scale(0.7).to_edge(LEFT).shift(RIGHT*1.5),
            run_time=1.5
        )
        self.wait(0.5)

        # Mitochondrion (energy production)
        mito = Ellipse(width=0.8, height=0.4, fill_color=RED_E, fill_opacity=0.8)
        inner_mito_line = Arc(radius=0.15, start_angle=PI/2, angle=PI, stroke_width=2, color=RED_A)
        inner_mito_line.next_to(mito, LEFT, buff=0.01).shift(UP*0.05)
        mito_group = VGroup(mito, inner_mito_line).move_to(main_cell.get_center() + RIGHT*1.5 + UP*0.5) # Position relative to main cell
        
        mito_label = Text("Mitochondrion (Energy)", font_size=24).set_color(WHITE).next_to(mito_group, UP, buff=0.3)
        mito_arrow = Arrow(mito_label.get_bottom(), mito_group.get_top(), buff=0.1, color=RED_E)

        # Linear Algebra touch: small circles expanding from mitochondria
        energy_bursts = VGroup(*[Circle(radius=r*0.1, stroke_width=1, color=YELLOW_C, opacity=0) for r in range(1, 5)])
        energy_bursts.move_to(mito_group.get_center())

        self.play(
            FadeIn(mito_group, shift=DOWN),
            FadeIn(mito_label, shift=DOWN),
            GrowArrow(mito_arrow),
            LaggedStart(*[burst.animate.set_opacity(1).scale(2) for burst in energy_bursts], lag_ratio=0.2, run_time=1.5)
        )
        self.wait(1.5)
        self.remove(energy_bursts)


        # Ribosomes (protein synthesis)
        ribo1 = Dot(radius=0.08, color=SILVER).move_to(main_cell.get_center() + DOWN*0.7 + LEFT*1)
        ribo2 = Dot(radius=0.08, color=SILVER).move_to(main_cell.get_center() + DOWN*0.8 + LEFT*0.7)
        ribo3 = Dot(radius=0.08, color=SILVER).move_to(main_cell.get_center() + DOWN*0.6 + RIGHT*0.7)
        ribo_group = VGroup(ribo1, ribo2, ribo3)

        ribo_label = Text("Ribosomes (Proteins)", font_size=24).set_color(WHITE).next_to(ribo_group, DOWN, buff=0.3)
        ribo_arrow = Arrow(ribo_label.get_top(), ribo_group.get_bottom(), buff=0.1, color=SILVER)

        # Linear Algebra touch: small dots moving towards and away
        amino_acid = Dot(radius=0.05, color=WHITE)
        path = Arc(radius=0.3, start_angle=PI, angle=PI/2, num_components=10).shift(ribo_group.get_center() + UP*0.2 + LEFT*0.2)

        self.play(
            FadeIn(ribo_group, shift=UP),
            FadeIn(ribo_label, shift=UP),
            GrowArrow(ribo_arrow),
            MoveAlongPath(amino_acid, path, run_time=1.5)
        )
        self.wait(1.5)
        self.remove(amino_acid)


        # Endoplasmic Reticulum (ER) - network/transport
        er_rect1 = Rectangle(width=1.2, height=0.2, fill_color=GREEN_D, fill_opacity=0.7)
        er_rect2 = Rectangle(width=1.0, height=0.2, fill_color=GREEN_D, fill_opacity=0.7).next_to(er_rect1, DOWN, buff=0.1).align_to(er_rect1, LEFT)
        er_rect3 = Rectangle(width=1.3, height=0.2, fill_color=GREEN_D, fill_opacity=0.7).next_to(er_rect2, DOWN, buff=0.1).align_to(er_rect2, LEFT)
        er_group = VGroup(er_rect1, er_rect2, er_rect3).move_to(main_cell.get_center() + RIGHT*1.5 + DOWN*0.5)

        er_label = Text("ER (Transport)", font_size=24).set_color(WHITE).next_to(er_group, UP, buff=0.3)
        er_arrow = Arrow(er_label.get_bottom(), er_group.get_top(), buff=0.1, color=GREEN_D)
        
        # Linear Algebra touch: small square moving through ER, representing transport
        cargo = Square(side_length=0.1, color=GOLD_C).move_to(er_rect1.get_left())
        
        self.play(
            FadeIn(er_group, shift=RIGHT),
            FadeIn(er_label, shift=RIGHT),
            GrowArrow(er_arrow),
            MoveAlongPath(cargo, Line(er_rect1.get_left(), er_rect1.get_right()), run_time=1.5)
        )
        self.wait(1.5)
        self.remove(cargo)

        self.wait(1)

        # --- Beat 4: Recap Card ---
        self.play(
            FadeOut(basic_structure_group),
            FadeOut(mito_group), FadeOut(mito_label), FadeOut(mito_arrow),
            FadeOut(ribo_group), FadeOut(ribo_label), FadeOut(ribo_arrow),
            FadeOut(er_group), FadeOut(er_label), FadeOut(er_arrow),
        )
        self.wait(0.5)

        recap_card = Rectangle(width=8, height=5, stroke_color=BLUE_C, fill_color=GRAY_D, fill_opacity=0.8, border_width=4)
        recap_card.move_to(ORIGIN)

        recap_title = Text("Key Cell Components", font_size=40).set_color(GOLD_C)
        recap_title.next_to(recap_card.get_top(), DOWN, buff=0.5)

        bullet_points = VGroup(
            Text("- Cell Membrane: Boundary", font_size=28, color=WHITE),
            Text("- Cytoplasm: Internal environment", font_size=28, color=WHITE),
            Text("- Nucleus: Control center", font_size=28, color=WHITE),
            Text("- Mitochondria: Energy production", font_size=28, color=WHITE),
            Text("- Ribosomes: Protein synthesis", font_size=28, color=WHITE),
            Text("- ER: Transport & Synthesis", font_size=28, color=WHITE)
        )
        bullet_points.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        bullet_points.next_to(recap_title, DOWN, buff=0.7).align_to(recap_card.get_left(), LEFT).shift(RIGHT*1)

        self.play(
            Create(recap_card),
            FadeIn(recap_title, shift=UP)
        )
        self.wait(0.5)
        self.play(
            LaggedStart(*[Write(bp) for bp in bullet_points], lag_ratio=0.2, run_time=3)
        )
        self.wait(3)

        self.play(FadeOut(recap_card, recap_title, bullet_points))
        self.wait(1)