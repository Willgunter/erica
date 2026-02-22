from manim import *

# Define custom colors for clarity and consistency
BLUE_ACCENT = ManimColor("#6F9CEB")  # Lighter blue for primary accents
GOLD_ACCENT = ManimColor("#FFD700")  # Gold for secondary accents
DARK_BLUE = ManimColor("#0A0A1A")  # Very dark blue for background
LIGHT_GREY = ManimColor("#CCCCCC")  # Light grey for secondary text/lines, arrows
WHITE_TEXT = ManimColor("#FFFFFF")  # White for main text and titles

class CellBasicsAnimation(Scene):
    def construct(self):
        self.camera.background_color = DARK_BLUE  # Set a very dark blue background

        # --- Beat 1: The Abstraction Journey (Visual Hook) ---
        self.play_beat_1_abstraction()

        # --- Beat 2: Introducing the Cell ---
        # The cell is created here and its components are returned for continuity
        cell_membrane, nucleus, cytoplasm_fill = self.play_beat_2_intro_cell()

        # --- Beat 3: Basic Structure - The Core Components ---
        self.play_beat_3_structure(cell_membrane, nucleus, cytoplasm_fill)

        # --- Beat 4: Basic Function - What Cells Do ---
        self.play_beat_4_function(cell_membrane, nucleus, cytoplasm_fill)

        # --- Beat 5: The Cell as a System / Object ---
        self.play_beat_5_system_analogy(cell_membrane, nucleus, cytoplasm_fill)

        # --- Recap Card ---
        self.play_recap()

    def play_beat_1_abstraction(self):
        # Start with a complex grid representing a system (e.g., a computer network, data structure)
        num_cells_grid = 12
        complex_system_units = VGroup(*[
            Rectangle(width=0.4, height=0.4, fill_opacity=0.3, color=BLUE_ACCENT, stroke_color=BLUE_ACCENT, stroke_width=1)
            for _ in range(num_cells_grid * num_cells_grid)
        ]).arrange_in_grid(num_cells_grid, num_cells_grid, buff=0.05).scale(0.8)

        system_label = MathTex("\\text{Complex Systems}", color=WHITE_TEXT).scale(0.8).to_edge(UP)

        self.play(
            FadeIn(complex_system_units, shift=UP),
            Write(system_label)
        )
        self.wait(1.5)

        # Transform label and fade out the complex system
        fundamental_units_label = MathTex("\\text{Fundamental Units}", color=WHITE_TEXT).scale(0.8).to_edge(UP)
        self.play(
            FadeOut(complex_system_units, shift=DOWN),
            TransformMatchingTex(system_label, fundamental_units_label)
        )
        self.wait(0.5)

        # Introduce a generic unit (square) to represent the abstract fundamental unit
        generic_unit_square = Square(side_length=1.5, color=GOLD_ACCENT, stroke_width=4, fill_opacity=0.0)
        self.play(FadeIn(generic_unit_square, scale=0.5))
        self.wait(0.5)

        # Transform the generic unit into a cell-like outline
        cell_outline_temp = Circle(radius=1.5, color=GOLD_ACCENT, stroke_width=4)
        self.play(
            Transform(generic_unit_square, cell_outline_temp, run_time=1.5, rate_func=ease_in_out_sine)
        )
        self.wait(0.5)
        
        # Fade out the temporary cell outline and the label. Beat 2 will re-introduce the full cell.
        self.play(FadeOut(VGroup(generic_unit_square, fundamental_units_label), shift=UP)) 
        self.wait(0.5)

    def play_beat_2_intro_cell(self):
        # Create the full cell structure for this beat and subsequent ones
        cell_radius = 1.5
        cell_membrane = Circle(radius=cell_radius, color=GOLD_ACCENT, stroke_width=4)
        nucleus = Dot(radius=0.4, color=BLUE_ACCENT).move_to(ORIGIN)
        # Cytoplasm is a slightly smaller circle to appear as a filled interior
        cytoplasm_fill = Circle(radius=cell_radius * 0.95, color=DARK_BLUE, fill_opacity=0.7) 
        
        # Group them, ensuring cytoplasm is behind membrane and nucleus
        cell_vgroup = VGroup(cytoplasm_fill, cell_membrane, nucleus)

        title = MathTex("\\text{The Cell: Basic Unit of Life}", color=WHITE_TEXT).scale(0.9).to_edge(UP)
        
        # Introduce the complete cell as a single unit
        self.play(
            FadeIn(cell_vgroup, scale=0.8), 
            Write(title)
        )
        self.wait(1.5)
        
        # Animate a pulse on the cell to symbolize its living, active nature
        pulse_cell = cell_membrane.copy().set_stroke(width=8, color=GOLD_ACCENT).set_opacity(0.0)
        self.play(
            Transform(cell_membrane.copy(), pulse_cell, path_arc=PI/2), # Animate a copy to avoid changing original
            pulse_cell.animate.scale(1.1).set_opacity(1.0).set_stroke(width=2).set_opacity(0.0), # Second half of pulse
            run_time=0.8
        )
        self.wait(1)
        self.play(FadeOut(title, shift=UP))
        self.remove(pulse_cell) # Clean up the pulse copy

        return cell_membrane, nucleus, cytoplasm_fill # Return for continuity

    def play_beat_3_structure(self, cell_membrane, nucleus, cytoplasm_fill):
        # Ensure the cell components are on screen
        self.add(cytoplasm_fill, cell_membrane, nucleus) 

        # Labels for structure components
        membrane_label = MathTex("\\text{Boundary (Membrane)}", color=GOLD_ACCENT).scale(0.7).next_to(cell_membrane, RIGHT, buff=0.5)
        nucleus_label = MathTex("\\text{Control Center (Nucleus)}", color=BLUE_ACCENT).scale(0.7).next_to(nucleus, LEFT, buff=0.5)
        cytoplasm_label = MathTex("\\text{Environment (Cytoplasm)}", color=LIGHT_GREY).scale(0.7).next_to(nucleus_label, DOWN, buff=0.8)

        # Arrows pointing to components
        arrow_mem = Arrow(membrane_label.get_left(), cell_membrane.get_right(), buff=0.1, color=LIGHT_GREY, stroke_width=2)
        arrow_nuc = Arrow(nucleus_label.get_right(), nucleus.get_left(), buff=0.1, color=LIGHT_GREY, stroke_width=2)
        arrow_cyto = Arrow(cytoplasm_label.get_right(), cytoplasm_fill.get_center() + LEFT*0.5, buff=0.1, color=LIGHT_GREY, stroke_width=2)

        title = MathTex("\\text{Basic Structure}", color=WHITE_TEXT).scale(0.9).to_edge(UP)
        
        self.play(Write(title))
        self.wait(0.5)

        # Animate structure components and their labels/arrows using LaggedStart for sequential entry
        self.play(LaggedStart(
            FadeIn(membrane_label, shift=LEFT), GrowArrow(arrow_mem),
            FadeIn(nucleus_label, shift=RIGHT), GrowArrow(arrow_nuc),
            FadeIn(cytoplasm_label, shift=RIGHT), GrowArrow(arrow_cyto),
            lag_ratio=0.3
        ), run_time=3)
        self.wait(1.5)

        # CS analogy overlay for better understanding by computer science learners
        cs_analogy_mem = MathTex("(\\text{API / Firewall})", color=BLUE_ACCENT).scale(0.6).next_to(membrane_label, DOWN, buff=0.1)
        cs_analogy_nuc = MathTex("(\\text{CPU / Data Storage})", color=GOLD_ACCENT).scale(0.6).next_to(nucleus_label, DOWN, buff=0.1)
        cs_analogy_cyto = MathTex("(\\text{Runtime Environment})", color=LIGHT_GREY).scale(0.6).next_to(cytoplasm_label, DOWN, buff=0.1)

        self.play(LaggedStart(
            FadeIn(cs_analogy_mem),
            FadeIn(cs_analogy_nuc),
            FadeIn(cs_analogy_cyto),
            lag_ratio=0.2
        ), run_time=1.5)
        self.wait(1.5)

        # Fade out all labels and arrows, leaving the cell itself for the next beat
        self.play(FadeOut(VGroup(title, membrane_label, nucleus_label, cytoplasm_label,
                                 arrow_mem, arrow_nuc, arrow_cyto,
                                 cs_analogy_mem, cs_analogy_nuc, cs_analogy_cyto), shift=UP))
        self.wait(0.5) 

    def play_beat_4_function(self, cell_membrane, nucleus, cytoplasm_fill):
        self.add(cytoplasm_fill, cell_membrane, nucleus) # Ensure they are on screen

        title = MathTex("\\text{Basic Function}", color=WHITE_TEXT).scale(0.9).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 1. Information Processing (Nucleus -> Cytoplasm)
        proc_label = MathTex("\\text{Process Instructions}", color=GOLD_ACCENT).scale(0.7).to_edge(LEFT).shift(UP*1)
        # A tiny moving dot to represent instruction flow from nucleus to cytoplasm
        instruction_dot = Dot(radius=0.1, color=GOLD_ACCENT).move_to(nucleus.get_right() + LEFT*0.2)
        
        self.play(
            Write(proc_label),
            FadeIn(instruction_dot, scale=0.5),
            MoveAlongPath(instruction_dot, Line(nucleus.get_right(), cytoplasm_fill.get_right() + RIGHT*0.5)),
            nucleus.animate.set_color(YELLOW_D), # Briefly highlight nucleus
            run_time=2
        )
        self.play(FadeOut(instruction_dot), nucleus.animate.set_color(BLUE_ACCENT)) # Reset nucleus color
        self.wait(0.5)

        # 2. Energy Generation (in Cytoplasm)
        energy_source = Circle(radius=0.3, color=BLUE_ACCENT, fill_opacity=0.8).move_to(cell_membrane.get_bottom() + UP*0.5 + LEFT*0.5)
        energy_label = MathTex("\\text{Generate Energy}", color=BLUE_ACCENT).scale(0.7).to_edge(LEFT).shift(DOWN*0.5)
        
        self.play(
            FadeIn(energy_source, shift=RIGHT),
            Write(energy_label),
            run_time=1
        )
        # Animate a pulse on the energy source
        self.play(
            energy_source.animate.scale(1.2).set_opacity(0.3),
            energy_source.animate.scale(1/1.2).set_opacity(0.8),
            run_time=0.8
        )
        self.wait(0.5)

        # 3. Interaction (Membrane Input/Output)
        io_label = MathTex("\\text{Interact (I/O)}", color=LIGHT_GREY).scale(0.7).to_edge(RIGHT).shift(UP*1)
        input_arrow = Arrow(RIGHT*3.5, cell_membrane.get_right(), buff=0.1, color=LIGHT_GREY, stroke_width=2)
        output_arrow = Arrow(cell_membrane.get_left(), LEFT*3.5, buff=0.1, color=LIGHT_GREY, stroke_width=2)

        self.play(
            Write(io_label),
            GrowArrow(input_arrow),
            GrowArrow(output_arrow),
            cell_membrane.animate.set_color(YELLOW_D), # Briefly highlight membrane
            run_time=1.5
        )
        self.play(cell_membrane.animate.set_color(GOLD_ACCENT)) # Reset membrane color
        self.wait(0.5)

        self.play(FadeOut(VGroup(title, proc_label, energy_label, energy_source, io_label, input_arrow, output_arrow), shift=UP))
        self.wait(0.5)

    def play_beat_5_system_analogy(self, cell_membrane, nucleus, cytoplasm_fill):
        self.add(cytoplasm_fill, cell_membrane, nucleus) # Ensure they are on screen

        title = MathTex("\\text{Cell as a Self-Contained System}", color=WHITE_TEXT).scale(0.9).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Analogies reinforcing CS concepts
        encapsulation_label = MathTex("\\text{Encapsulated State}", color=BLUE_ACCENT).scale(0.8).shift(UP*1.5)
        encapsulation_arrow = Arrow(encapsulation_label.get_bottom(), nucleus.get_top(), buff=0.1, color=BLUE_ACCENT, stroke_width=2)

        interface_label = MathTex("\\text{Defined Interface (API)}", color=GOLD_ACCENT).scale(0.8).shift(DOWN*1.5)
        interface_arrow = Arrow(interface_label.get_top(), cell_membrane.get_bottom(), buff=0.1, color=GOLD_ACCENT, stroke_width=2)

        self.play(
            FadeIn(encapsulation_label, shift=UP), GrowArrow(encapsulation_arrow)
        )
        self.wait(1)
        self.play(
            FadeIn(interface_label, shift=DOWN), GrowArrow(interface_arrow)
        )
        self.wait(1.5)

        # Briefly show an abstract function plot to represent predictable behavior
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3,
            y_length=3,
            axis_config={"color": LIGHT_GREY, "stroke_width": 1}
        ).scale(0.5).to_corner(UL).shift(RIGHT*1.5, DOWN*0.5) # Position to not overlap other labels
        
        func_label = MathTex("\\text{Predictable Behavior}", color=LIGHT_GREY).scale(0.6).next_to(axes, DOWN, buff=0.2)
        graph = axes.plot(lambda x: np.sin(x) * x/2, color=BLUE_ACCENT)

        self.play(
            FadeIn(axes), Create(graph), FadeIn(func_label),
            run_time=1.5
        )
        self.wait(1)
        self.play(
            FadeOut(axes), FadeOut(graph), FadeOut(func_label)
        )

        self.play(FadeOut(VGroup(title, encapsulation_label, encapsulation_arrow, interface_label, interface_arrow)))
        self.wait(0.5)
        # Fade out the cell components at the end of this beat
        self.play(FadeOut(VGroup(cell_membrane, nucleus, cytoplasm_fill)))

    def play_recap(self):
        recap_title = MathTex("\\text{Recap: Cell Basics}", color=WHITE_TEXT).scale(1.1).to_edge(UP)

        bullet_points = VGroup(
            MathTex("- \\text{Cell: Basic unit of life}", color=WHITE_TEXT),
            MathTex("- \\text{Structure: Boundary, Control, Environment}", color=GOLD_ACCENT),
            MathTex("- \\text{Function: Process, Energy, Interact}", color=BLUE_ACCENT),
            MathTex("- \\text{Think: Micro-System with API}", color=LIGHT_GREY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).scale(0.8).next_to(recap_title, DOWN, buff=1)

        self.play(Write(recap_title))
        # Use LaggedStart for a dynamic reveal of each bullet point
        self.play(LaggedStart(*[FadeIn(bp, shift=LEFT) for bp in bullet_points], lag_ratio=0.5))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, bullet_points)))