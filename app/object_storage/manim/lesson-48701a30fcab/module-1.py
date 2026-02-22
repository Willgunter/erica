from manim import *

class CellStructureAnimation(Scene):
    def construct(self):
        # --- Custom Colors (3B1B inspired) ---
        BLUE_ACCENT = ManimColor("#83B7FF")  # Lighter blue for primary elements
        GOLD_ACCENT = ManimColor("#FFD700")  # Gold for highlights/secondary elements
        TEXT_COLOR = WHITE
        DARK_BACKGROUND = BLACK
        MUTED_GRAY = ManimColor("#4A4A4A") # For background grids/planes

        self.camera.background_color = DARK_BACKGROUND

        # --- Scene 1: The Basic Unit of Life (Visual Hook & Modularity) ---
        
        # Initial title for the module
        module_title = Text("Fundamental Cell Structure and Function", font_size=48, color=TEXT_COLOR)
        module_title.to_edge(UP)

        self.play(FadeIn(module_title, shift=UP), run_time=1)
        self.wait(0.5)

        # Use a NumberPlane to represent a conceptual space
        intro_plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=6,
            background_line_style={"stroke_color": MUTED_GRAY, "stroke_width": 0.5},
            faded_line_ratio=4 # Lines fade out more gently
        ).shift(2.5 * LEFT + 0.5 * UP).scale(0.8)
        
        # Start with a point, then visualize it expanding into a fundamental unit
        point_of_origin = Dot(point=intro_plane.c2p(0, 0), color=GOLD_ACCENT).scale(1.5)

        self.play(Create(intro_plane), FadeIn(point_of_origin), run_time=1.5)
        self.wait(0.5)

        # Transform point into a primitive cell shape (circle for membrane, dot for nucleus)
        primitive_membrane = Circle(radius=0.8, color=BLUE_ACCENT, stroke_width=3)
        primitive_membrane.move_to(point_of_origin)
        primitive_nucleus = Dot(point=primitive_membrane.get_center(), radius=0.15, color=GOLD_ACCENT)
        primitive_cell_mobject = VGroup(primitive_membrane, primitive_nucleus)

        unit_label = Text("A Unit", font_size=24, color=TEXT_COLOR).next_to(primitive_cell_mobject, RIGHT, buff=0.2)

        self.play(
            Transform(point_of_origin, primitive_membrane), # Point becomes the membrane
            FadeIn(primitive_nucleus),
            Write(unit_label),
            run_time=2
        )
        self.wait(0.5)

        # Emphasize "The Basic Unit of Life" and show modularity by replicating
        beat1_title = Text("The Basic Unit of Life", font_size=36, color=TEXT_COLOR).to_edge(LEFT).shift(UP*1.5)
        
        # Create multiple instances of the cell unit
        cell_prototypes = VGroup(
            VGroup(Circle(radius=0.6, color=BLUE_ACCENT, stroke_width=3), Dot(radius=0.1, color=GOLD_ACCENT)),
            VGroup(Circle(radius=0.6, color=BLUE_ACCENT, stroke_width=3), Dot(radius=0.1, color=GOLD_ACCENT)),
            VGroup(Circle(radius=0.6, color=BLUE_ACCENT, stroke_width=3), Dot(radius=0.1, color=GOLD_ACCENT)),
            VGroup(Circle(radius=0.6, color=BLUE_ACCENT, stroke_width=3), Dot(radius=0.1, color=GOLD_ACCENT)),
        ).arrange_in_grid(rows=2, cols=2, buff=0.8)
        cell_prototypes.shift(1.5*RIGHT)

        self.play(
            FadeOut(intro_plane, shift=LEFT),
            FadeOut(point_of_origin), # Fades out the original transformed point
            FadeOut(unit_label),
            ReplacementTransform(primitive_cell_mobject, cell_prototypes), # Transform single cell into group of cells
            TransformMatchingTex(module_title, beat1_title), # Animate title change
            run_time=2
        )
        self.wait(1)

        # --- Scene 2: The Cell Membrane (Boundary & Regulation) ---
        # Focus on one cell, zoom in
        main_cell = cell_prototypes[0].copy().scale(1.5).move_to(ORIGIN)
        membrane = main_cell[0] # The circle is the membrane
        nucleus_remains = main_cell[1] # Nucleus stays for context

        beat2_title = Text("1. Cell Membrane: The Boundary", font_size=36, color=TEXT_COLOR).to_edge(UP)

        self.play(
            FadeOut(cell_prototypes),
            ReplacementTransform(beat1_title, beat2_title),
            FadeIn(main_cell),
            run_time=1.5
        )
        self.wait(0.5)

        membrane_label = MathTex(r"\text{Cell Membrane}", font_size=32, color=BLUE_ACCENT).next_to(membrane, UP + RIGHT, buff=0.1)
        membrane_func = Text("Regulates Passage", font_size=28, color=GOLD_ACCENT).next_to(membrane_label, DOWN, buff=0.2)

        self.play(Indicate(membrane, scale_factor=1.1, color=BLUE_ACCENT), Write(membrane_label), FadeIn(membrane_func, shift=DOWN))
        self.wait(1)

        # Illustrate passage of molecules
        particle_in1 = Dot(color=YELLOW_A).move_to(membrane.point_at_angle(PI * 0.75) + UP * 0.5)
        particle_in2 = Dot(color=YELLOW_A).move_to(membrane.point_at_angle(PI * 0.25) + UP * 0.5)
        particle_blocked = Dot(color=YELLOW_A).move_to(membrane.point_at_angle(PI * 1.25) + DOWN * 0.5)
        
        self.play(FadeIn(particle_in1), FadeIn(particle_in2), FadeIn(particle_blocked))
        self.wait(0.2)

        self.play(
            particle_in1.animate.move_to(membrane.point_at_angle(PI * 0.75) * 0.5), # Moves inside
            particle_in2.animate.move_to(membrane.point_at_angle(PI * 0.25) * 0.5), # Moves inside
            particle_blocked.animate.shift(0.5 * DOWN), # Stays outside, indicating blockage
            Flash(particle_blocked, color=RED_E, line_length=0.2, num_lines=4, flash_radius=0.3, line_stroke_width=2),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(particle_in1, particle_in2, particle_blocked, membrane_func, membrane_label))

        # --- Scene 3: The Nucleus (Control Center & Information) ---
        beat3_title = Text("2. Nucleus: The Command Center", font_size=36, color=TEXT_COLOR).to_edge(UP)

        nucleus_label = MathTex(r"\text{Nucleus}", font_size=32, color=GOLD_ACCENT).next_to(nucleus_remains, UP, buff=0.2)
        nucleus_func = Text("Contains Genetic Information (DNA)", font_size=28, color=TEXT_COLOR).next_to(nucleus_label, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(beat2_title, beat3_title),
            Indicate(nucleus_remains, scale_factor=1.2, color=GOLD_ACCENT),
            Write(nucleus_label),
            FadeIn(nucleus_func, shift=DOWN),
            run_time=1.5
        )
        self.wait(1)

        # Represent DNA helix as a 3D object
        dna_helix = self._create_dna_helix().scale(0.4).move_to(nucleus_remains.get_center())
        
        self.play(Create(dna_helix), run_time=2)
        self.wait(0.5)

        # Information flow: from nucleus to outside
        info_arrow = Arrow(nucleus_remains.get_right() * 0.5, membrane.get_right() * 0.7, buff=0.1, color=BLUE_ACCENT)
        info_text = MathTex(r"\text{Instructions}", font_size=20, color=BLUE_ACCENT).next_to(info_arrow, UP, buff=0.1)
        
        self.play(Create(info_arrow), Write(info_text))
        self.wait(1)
        self.play(FadeOut(nucleus_label, nucleus_func, dna_helix, info_arrow, info_text))

        # --- Scene 4: Cytoplasm & Organelles (The Workspace) ---
        beat4_title = Text("3. Cytoplasm & Organelles: The Workspace", font_size=36, color=TEXT_COLOR).to_edge(UP)
        cytoplasm_label = Text("Cytoplasm", font_size=32, color=TEXT_COLOR).move_to(membrane.get_center()).shift(DOWN*0.5 + LEFT*0.5)

        self.play(
            ReplacementTransform(beat3_title, beat4_title),
            Write(cytoplasm_label)
        )
        self.wait(0.5)

        # Organelles as abstract shapes
        organelle1 = Circle(radius=0.2, color=GOLD_ACCENT, fill_opacity=0.8).move_to(membrane.point_at_angle(PI * 0.4) * 0.6)
        organelle2 = Square(side_length=0.4, color=BLUE_ACCENT, fill_opacity=0.8).move_to(membrane.point_at_angle(PI * 1.6) * 0.7)
        organelle3 = Triangle(color=GOLD_ACCENT, fill_opacity=0.8).scale(0.3).move_to(membrane.point_at_angle(PI * 0.9) * 0.7)
        organelle4 = Rectangle(width=0.5, height=0.3, color=BLUE_ACCENT, fill_opacity=0.8).move_to(membrane.point_at_angle(PI * 1.1) * 0.5)
        
        organelles_group = VGroup(organelle1, organelle2, organelle3, organelle4)
        organelles_label = Text("Organelles: Specialized Tasks", font_size=28, color=TEXT_COLOR).next_to(organelles_group, RIGHT, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(org, scale=0.5) for org in organelles_group], lag_ratio=0.3),
            Write(organelles_label)
        )
        self.wait(1)

        # Show processes/interactions
        process_arrow1 = Arrow(nucleus_remains.get_top(), organelle1.get_bottom(), buff=0.1, color=BLUE_ACCENT)
        process_arrow2 = Arrow(organelle2.get_right(), organelle3.get_left(), buff=0.1, color=GOLD_ACCENT)
        process_arrow3 = Arrow(organelle4.get_right(), membrane.point_at_angle(PI * 1.3), buff=0.1, color=BLUE_ACCENT)

        self.play(Create(process_arrow1), Indicate(organelle1), run_time=0.8)
        self.play(Create(process_arrow2), Indicate(organelle2), Indicate(organelle3), run_time=0.8)
        self.play(Create(process_arrow3), Indicate(organelle4), Indicate(membrane), run_time=0.8)
        self.wait(1)

        self.play(
            FadeOut(process_arrow1, process_arrow2, process_arrow3,
                    cytoplasm_label, organelles_label, organelles_group)
        )

        # --- Scene 5: Cell as a Modular System (CS Analogy) ---
        beat5_title = Text("Cell: A Modular, Self-Contained System", font_size=36, color=TEXT_COLOR).to_edge(UP)
        self.play(
            ReplacementTransform(beat4_title, beat5_title),
            Indicate(main_cell, scale_factor=1.05, color=BLUE_ACCENT),
            run_time=1
        )
        self.wait(0.5)

        cs_analogy_text = Text("Think of it as a function in programming:", font_size=28, color=GOLD_ACCENT).next_to(beat5_title, DOWN, buff=0.5)
        
        # Python-like pseudo-code representation using MathTex
        func_declaration = MathTex(r"\text{def cell\_system(inputs):}", font_size=32, color=TEXT_COLOR)
        func_body_nucleus = MathTex(r"\quad \text{genetic\_data} = \text{nucleus.read\_dna()}", font_size=28, color=BLUE_ACCENT)
        func_body_organelles = MathTex(r"\quad \text{processed\_output} = \text{organelles.execute\_tasks(genetic\_data, inputs)}", font_size=28, color=GOLD_ACCENT)
        func_body_membrane = MathTex(r"\quad \text{membrane.regulate\_exchange(processed\_output, inputs)}", font_size=28, color=BLUE_ACCENT)
        func_return = MathTex(r"\quad \text{return processed\_output}", font_size=28, color=TEXT_COLOR)

        code_group = VGroup(func_declaration, func_body_nucleus, func_body_organelles, func_body_membrane, func_return).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code_group.next_to(cs_analogy_text, DOWN, buff=0.5).to_edge(LEFT)
        
        self.play(Write(cs_analogy_text))
        self.wait(0.5)
        self.play(Write(func_declaration))
        self.wait(0.2)
        self.play(Write(func_body_nucleus))
        self.wait(0.2)
        self.play(Write(func_body_organelles))
        self.wait(0.2)
        self.play(Write(func_body_membrane))
        self.wait(0.2)
        self.play(Write(func_return))
        self.wait(2)

        # --- Recap Card ---
        self.play(FadeOut(main_cell, beat5_title, cs_analogy_text, code_group))

        recap_title = Text("Recap: Key Cell Components", font_size=42, color=TEXT_COLOR).to_edge(UP)
        self.play(FadeIn(recap_title, shift=UP))
        self.wait(0.5)

        recap_list = VGroup(
            Text("1. Cell: The basic unit of life.", font_size=32, color=BLUE_ACCENT),
            Text("2. Cell Membrane: Boundary that regulates passage.", font_size=32, color=GOLD_ACCENT),
            Text("3. Nucleus: Command center containing genetic instructions (DNA).", font_size=32, color=BLUE_ACCENT),
            Text("4. Cytoplasm & Organelles: The workspace for specialized tasks.", font_size=32, color=GOLD_ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        
        recap_list.next_to(recap_title, DOWN, buff=1)

        self.play(LaggedStart(*[FadeIn(item, shift=LEFT) for item in recap_list], lag_ratio=0.5))
        self.wait(3)

        self.play(FadeOut(*self.mobjects))
        self.wait(1)

    # Helper function for a stylized DNA helix
    def _create_dna_helix(self):
        # A simplified 3D representation using parametric functions
        
        helix_radius = 0.5
        helix_pitch = 1.5 # How much it advances per turn
        num_turns = 1.5

        # Path 1: Blue strand
        helix1 = ParametricFunction(
            lambda t: np.array([
                helix_radius * np.cos(t),
                helix_radius * np.sin(t),
                t * helix_pitch / (2 * PI) # z-component for vertical extension
            ]),
            t_range=[-num_turns * PI, num_turns * PI],
            color=BLUE_ACCENT,
            stroke_width=3
        )

        # Path 2: Gold strand, shifted by PI for the double helix effect
        helix2 = ParametricFunction(
            lambda t: np.array([
                helix_radius * np.cos(t + PI), # Shifted by PI (180 degrees)
                helix_radius * np.sin(t + PI),
                t * helix_pitch / (2 * PI)
            ]),
            t_range=[-num_turns * PI, num_turns * PI],
            color=GOLD_ACCENT,
            stroke_width=3
        )
        
        # Connecting rungs (simplified, a few horizontal lines)
        rungs = VGroup()
        for t_val in np.linspace(-num_turns * PI, num_turns * PI, 5): # 5 rungs
            start_point = np.array([helix_radius * np.cos(t_val), helix_radius * np.sin(t_val), t_val * helix_pitch / (2 * PI)])
            end_point = np.array([helix_radius * np.cos(t_val + PI), helix_radius * np.sin(t_val + PI), t_val * helix_pitch / (2 * PI)])
            rung = Line(start_point, end_point, color=MUTED_GRAY, stroke_width=1.5)
            rungs.add(rung)

        dna_group = VGroup(helix1, helix2, rungs)
        dna_group.rotate(PI/2, axis=RIGHT) # Rotate to be more vertical on screen
        dna_group.set_z_index(2) # Ensure it's rendered correctly if depth is considered

        return dna_group