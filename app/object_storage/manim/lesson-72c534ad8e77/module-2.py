from manim import *
import random

class DNAHeredityCellDivision(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK

        # --- Beat 0: Title & Hook ---
        title = Text("DNA, Heredity, & Cell Division", font_size=72, color=GOLD_A).to_edge(UP)
        subtitle = Text("Life's Code, Passed Down, Replicated", font_size=36, color=BLUE_A).next_to(title, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                Write(title, run_time=1.5),
                Write(subtitle, run_time=1.5),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)

        # Hook: Abstract information flow coalescing into a DNA-like structure
        # Create scattered dots representing raw information
        flow_points = VGroup(*[Dot(point=2*np.random.rand(3)-1, radius=0.08, color=random_color()) for _ in range(70)])
        flow_points.arrange_in_grid(rows=7, cols=10, buff=0.3).shift(LEFT * 4)

        # Create a basic double helix for the hook
        helix_segments = VGroup()
        num_segments = 12
        segment_height = 0.5
        total_height = num_segments * segment_height
        for i in range(num_segments):
            y_start = total_height/2 - i * segment_height
            y_end = total_height/2 - (i + 1) * segment_height
            
            # Simulate a helix twist
            angle_start = i * PI / 3
            angle_end = (i + 1) * PI / 3
            
            x_left_start = -1 * np.cos(angle_start) * 0.5
            x_right_start = 1 * np.cos(angle_start) * 0.5
            
            x_left_end = -1 * np.cos(angle_end) * 0.5
            x_right_end = 1 * np.cos(angle_end) * 0.5

            # Backbones
            segment_left = Line(LEFT * 0.5 + UP * y_start, LEFT * 0.5 + UP * y_end, color=BLUE_C, stroke_width=3)
            segment_right = Line(RIGHT * 0.5 + UP * y_start, RIGHT * 0.5 + UP * y_end, color=BLUE_C, stroke_width=3)
            
            # Connectors (base pairs)
            connector = Line(segment_left.get_center(), segment_right.get_center(), color=GOLD_C, stroke_width=1.5)
            
            helix_segments.add(segment_left, segment_right, connector)

        initial_dna_hook = helix_segments.scale(0.8).move_to(RIGHT * 3)

        self.play(FadeIn(flow_points), run_time=1)
        self.play(
            flow_points.animate.move_to(initial_dna_hook.get_center()).scale(0.1).set_opacity(0.3),
            Create(initial_dna_hook, run_time=2),
            run_time=2
        )
        self.play(FadeOut(flow_points), run_time=0.5)
        self.wait(1)
        
        # Shrink initial_dna_hook and title/subtitle for the transition
        self.play(
            FadeOut(title, subtitle),
            initial_dna_hook.animate.scale(0.4).to_corner(UL),
            run_time=1
        )
        current_dna_representation = initial_dna_hook.copy()


        # --- Beat 1: Genetics - The Core (~8-10 seconds) ---
        beat1_title = Text("1. Genetics: Inheriting Life's Code", font_size=48, color=GOLD_A).to_edge(UP)
        dna_core_text = MathTex(r"\textbf{DNA}", color=BLUE_A, font_size=96).scale(0.8).move_to(RIGHT*3)
        dna_desc = Text("The core information molecule.", font_size=32, color=WHITE).next_to(dna_core_text, DOWN, buff=0.5)

        # Abstract inheritance visual (e.g., parental traits combining)
        parent_shape1 = Circle(radius=0.7, color=BLUE_C, fill_opacity=0.5).shift(LEFT * 3 + UP * 1.5)
        parent_shape2 = Square(side_length=1.4, color=GOLD_C, fill_opacity=0.5).shift(LEFT * 3 + DOWN * 1.5)
        trait_arrow1 = Arrow(parent_shape1.get_right(), ORIGIN + LEFT*1.5, buff=0.1, color=WHITE)
        trait_arrow2 = Arrow(parent_shape2.get_right(), ORIGIN + LEFT*1.5, buff=0.1, color=WHITE)
        # Child shape combining features: a square with a circular outline inside
        child_outer = Square(side_length=1.4, color=GOLD_C, fill_opacity=0.5)
        child_inner = Circle(radius=0.6, color=BLUE_C, fill_opacity=0.5)
        child_shape = VGroup(child_outer, child_inner).move_to(LEFT*1.5)

        self.play(Write(beat1_title))
        self.play(
            FadeIn(parent_shape1, shift=LEFT), FadeIn(parent_shape2, shift=LEFT),
            Create(trait_arrow1), Create(trait_arrow2),
            run_time=1.5
        )
        self.play(
            ReplacementTransform(VGroup(parent_shape1, parent_shape2, trait_arrow1, trait_arrow2), child_shape),
            run_time=2
        )
        self.play(
            current_dna_representation.animate.scale(1.5).move_to(LEFT*2.5 + UP*1), # Bring prev DNA closer
            FadeIn(dna_core_text, shift=DOWN),
            Write(dna_desc),
            run_time=2
        )
        self.wait(1)
        self.play(
            FadeOut(beat1_title, shift=UP),
            FadeOut(child_shape, shift=LEFT),
            FadeOut(dna_core_text, shift=RIGHT),
            FadeOut(dna_desc, shift=RIGHT),
            current_dna_representation.animate.scale(0.4/1.5).to_corner(UL), # Shrink back to UL and adjust scale
            run_time=1.5
        )
        
        # current_dna_representation is now back in UL corner


        # --- Beat 2: DNA Structure - The Blueprint (~8-10 seconds) ---
        beat2_title = Text("2. DNA Structure: The Blueprint", font_size=48, color=GOLD_A).to_edge(UP)
        
        # Simplified DNA segment
        dna_segment_height = 4
        left_backbone = Line(UP * dna_segment_height / 2, DOWN * dna_segment_height / 2, color=BLUE_C, stroke_width=4)
        right_backbone = Line(UP * dna_segment_height / 2, DOWN * dna_segment_height / 2, color=BLUE_C, stroke_width=4)
        
        base_pairs_group = VGroup()
        bases_chart = {
            "A": {"pair": "T", "color": TEAL_C},
            "T": {"pair": "A", "color": RED_C},
            "C": {"pair": "G", "color": PURPLE_C},
            "G": {"pair": "C", "color": ORANGE_C}
        }
        
        sequence = ["A", "C", "T", "G"] # Example sequence
        
        num_pairs = len(sequence)
        for i, base1_char in enumerate(sequence):
            y_offset = (dna_segment_height / (num_pairs - 1)) * i - dna_segment_height / 2
            
            # Simple simulation of twist for visual appeal
            twist_offset = 0.1 * np.sin(y_offset * PI / 1.5)
            
            left_pos = LEFT * (0.6 + twist_offset) + UP * y_offset
            right_pos = RIGHT * (0.6 - twist_offset) + UP * y_offset

            base1_label = MathTex(base1_char, color=bases_chart[base1_char]["color"], font_size=36).move_to(left_pos)
            base2_char = bases_chart[base1_char]["pair"]
            base2_label = MathTex(base2_char, color=bases_chart[base2_char]["color"], font_size=36).move_to(right_pos)
            
            connector_line = Line(base1_label.get_right(), base2_label.get_left(), color=WHITE, stroke_width=1)
            
            base_pairs_group.add(VGroup(base1_label, base2_label, connector_line))

        simplified_dna_model = VGroup(left_backbone, right_backbone, base_pairs_group).center().scale(0.8).shift(LEFT*2)

        code_text = Text("A, T, C, G: The Genetic Alphabet", font_size=36, color=WHITE).next_to(simplified_dna_model, RIGHT*2)
        code_desc = Text("Instructions for building life.", font_size=32, color=BLUE_A).next_to(code_text, DOWN, buff=0.5)

        self.play(Write(beat2_title))
        self.play(FadeIn(simplified_dna_model, shift=DOWN), run_time=2)
        self.play(Write(code_text), Write(code_desc), run_time=2)
        self.play(
            # Animate a focus on the base pairs
            base_pairs_group.animate.set_stroke(YELLOW, 2).set_opacity(0.8),
            run_time=1
        )
        self.wait(1)
        self.play(
            FadeOut(beat2_title, shift=UP),
            FadeOut(code_text, shift=RIGHT),
            FadeOut(code_desc, shift=RIGHT),
            simplified_dna_model.animate.scale(0.4).to_corner(UL), # Move new DNA to UL
            FadeOut(current_dna_representation), # Remove old DNA
            run_time=1.5
        )
        current_dna_representation = simplified_dna_model.copy()


        # --- Beat 3: Heredity - Passing the Blueprint (~8-10 seconds) ---
        beat3_title = Text("3. Heredity: Passing Traits", font_size=48, color=GOLD_A).to_edge(UP)

        # Represent parent DNA as smaller versions of the simplified_dna_model
        parent_dna1 = simplified_dna_model.copy().scale(0.8).shift(UP*2 + LEFT*3)
        parent_dna2 = simplified_dna_model.copy().scale(0.8).shift(DOWN*2 + LEFT*3)
        
        arrow_to_child1 = Arrow(parent_dna1.get_right(), LEFT*1.5, buff=0.1, color=WHITE)
        arrow_to_child2 = Arrow(parent_dna2.get_right(), LEFT*1.5, buff=0.1, color=WHITE)
        
        child_dna = simplified_dna_model.copy().scale(1.0).move_to(RIGHT*2) # Child is similar but centered
        
        traits_text = Text("Characteristics from parents to offspring.", font_size=32, color=BLUE_A).next_to(child_dna, DOWN, buff=0.5)
        
        self.play(Write(beat3_title))
        self.play(
            FadeIn(parent_dna1, shift=LEFT), FadeIn(parent_dna2, shift=LEFT),
            Create(arrow_to_child1), Create(arrow_to_child2),
            run_time=2
        )
        self.play(
            Transform(VGroup(parent_dna1, parent_dna2, arrow_to_child1, arrow_to_child2), child_dna),
            Write(traits_text),
            run_time=2.5
        )
        self.wait(1)
        self.play(
            FadeOut(beat3_title, shift=UP),
            FadeOut(traits_text, shift=DOWN),
            child_dna.animate.scale(0.4/1.0).to_corner(UL), # Adjust scale and position based on previous UL object
            FadeOut(current_dna_representation), # Remove old UL DNA
            run_time=1.5
        )
        current_dna_representation = child_dna.copy() # Update current_dna_representation


        # --- Beat 4: Cell Division - Replicating the Code (~8-10 seconds) ---
        beat4_title = Text("4. Cell Division: Replicating Life", font_size=48, color=GOLD_A).to_edge(UP)

        cell = Circle(radius=2, color=BLUE_C, fill_opacity=0.3).center()
        dna_in_cell = simplified_dna_model.copy().scale(0.7).move_to(cell.get_center())

        self.play(Write(beat4_title))
        self.play(FadeIn(cell), FadeIn(dna_in_cell), run_time=1.5)

        # Animate DNA replication
        dna_in_cell_split_left = dna_in_cell.copy().shift(LEFT * 0.7)
        dna_in_cell_split_right = dna_in_cell.copy().shift(RIGHT * 0.7)

        replication_text = Text("DNA duplicates itself...", font_size=32, color=WHITE).next_to(cell, DOWN, buff=0.5)
        self.play(
            ReplacementTransform(dna_in_cell, VGroup(dna_in_cell_split_left, dna_in_cell_split_right)),
            Write(replication_text),
            run_time=2
        )
        self.wait(0.5)

        # Animate cell division
        cell_left = cell.copy().shift(LEFT * 2)
        cell_right = cell.copy().shift(RIGHT * 2)
        
        dna_left_final = dna_in_cell_split_left.copy().move_to(cell_left.get_center())
        dna_right_final = dna_in_cell_split_right.copy().move_to(cell_right.get_center())

        division_text = Text("...then the cell divides, forming exact copies.", font_size=32, color=BLUE_A).next_to(cell_left, DOWN, buff=0.5)
        self.play(FadeOut(replication_text))
        self.play(
            Transform(VGroup(cell, dna_in_cell_split_left, dna_in_cell_split_right), VGroup(cell_left, cell_right, dna_left_final, dna_right_final)),
            Write(division_text),
            run_time=2.5
        )
        self.wait(1)

        self.play(
            FadeOut(beat4_title, shift=UP),
            FadeOut(VGroup(cell_left, cell_right, dna_left_final, dna_right_final), shift=DOWN),
            FadeOut(division_text, shift=DOWN),
            FadeOut(current_dna_representation), # Remove old UL DNA
            run_time=1.5
        )


        # --- Recap Card ---
        recap_title = Text("Recap: Key Concepts", font_size=60, color=GOLD_A).to_edge(UP)
        
        recap_bullet1 = Text("DNA: The Blueprint of Life", font_size=40, color=BLUE_A).shift(UP * 1.5)
        recap_bullet2 = Text("Heredity: Traits Passed Down", font_size=40, color=BLUE_A).next_to(recap_bullet1, DOWN, buff=0.8)
        recap_bullet3 = Text("Cell Division: Replicating the Code", font_size=40, color=BLUE_A).next_to(recap_bullet2, DOWN, buff=0.8)

        # Add a subtle "Next Steps" or AI Spar reference to link back to prompt
        next_steps_text = Text(
            "Ready to test your understanding with Erica?",
            font_size=30, color=WHITE
        ).next_to(recap_bullet3, DOWN, buff=1.0)
        
        recap_group = VGroup(recap_title, recap_bullet1, recap_bullet2, recap_bullet3, next_steps_text)
        recap_group.center()

        self.play(Write(recap_title), run_time=1)
        self.play(
            LaggedStart(
                Write(recap_bullet1, run_time=1),
                Write(recap_bullet2, run_time=1),
                Write(recap_bullet3, run_time=1),
                lag_ratio=0.7
            ),
            run_time=3
        )
        self.play(Write(next_steps_text), run_time=1)
        self.wait(2)
        self.play(FadeOut(recap_group))
        self.wait(1)