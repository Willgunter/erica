from manim import *

class BiologicalEnergyTransformations(Scene):
    def construct(self):
        # --- Configuration for 3Blue1Brown style ---
        self.camera.background_color = "#1a1a1a" # Clean dark background
        # Define custom high-contrast colors for accents
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C
        TEXT_COLOR = WHITE

        # --- Beat 1: Hook & Introduction (Energy Flow) ---
        # Strong visual hook: A pulsating energy core
        energy_ball = Dot(radius=0.3, color=GOLD_ACCENT)
        energy_aura = Circle(radius=0.5, color=GOLD_ACCENT, stroke_width=2).set_opacity(0.5)
        
        self.play(Create(energy_ball), Create(energy_aura), run_time=1)
        self.play(
            energy_aura.animate.scale(1.5).set_opacity(0).set_stroke_width(0), # Scale out and fade aura
            energy_ball.animate.scale(0.8),
            run_time=0.8
        )
        # Re-create and pulse aura for a second beat
        energy_aura = Circle(radius=0.5, color=GOLD_ACCENT, stroke_width=2).set_opacity(0.5)
        self.play(
            FadeIn(energy_aura), 
            energy_ball.animate.scale(1/0.8),
            run_time=0.8
        )
        self.wait(0.5)

        # Title and objective
        title = Text("Biological Energy Transformations", font_size=50, color=BLUE_ACCENT)
        objective = Text("Understanding how life converts energy", font_size=30, color=TEXT_COLOR).next_to(title, DOWN, buff=0.5)

        self.play(
            FadeOut(energy_aura, shift=UP),
            energy_ball.animate.scale(0.1).to_corner(UL), # Shrink and move energy ball to corner
            Write(title),
            Write(objective)
        )
        self.wait(1)

        # Intuition first: Energy constantly converted, not created
        intro_text = Text(
            "Life runs on energy conversion, not creation.",
            font_size=36,
            color=TEXT_COLOR
        ).next_to(objective, DOWN, buff=1.0).to_edge(LEFT, buff=1)
        self.play(Write(intro_text), run_time=2)
        self.wait(1.5)

        # Clean up for next beat with smooth fade-out
        self.play(
            FadeOut(title, objective, intro_text),
            energy_ball.animate.set_opacity(0) # Also fade out the small energy dot
        )
        self.wait(0.5)

        # --- Beat 2: Photosynthesis (Energy Capture) ---
        photosynthesis_title = Text("1. Photosynthesis: Capturing Light", font_size=40, color=BLUE_ACCENT).to_edge(UP)
        self.play(Write(photosynthesis_title))

        # Intuition: Sunlight -> Plant -> Sugar (chemical energy)
        sun = Dot(radius=0.4, color=YELLOW).move_to([-4, 2, 0])
        sun_label = Text("Sunlight", font_size=24, color=TEXT_COLOR).next_to(sun, UP)
        
        # Simple plant shape using Manim primitives
        plant_shape = VGroup(
            Polygon([-2.5, -1, 0], [-1.5, 0.5, 0], [-3.5, 0.5, 0]), # Leaf 1
            Polygon([-1.5, -1.2, 0], [-0.5, 0.3, 0], [-2.5, 0.3, 0]), # Leaf 2
            Rectangle(width=0.3, height=1.5).shift(DOWN*0.7) # Stem
        ).set_color(GREEN_E).set_fill(GREEN_E, opacity=0.8).move_to([-2, -0.5, 0])
        plant_label = Text("Plant", font_size=24, color=TEXT_COLOR).next_to(plant_shape, DOWN)

        sugar_mol = Circle(radius=0.3, color=GOLD_ACCENT, fill_opacity=0.8).move_to([2, 0, 0])
        sugar_label = Text("Sugar (Chemical Energy)", font_size=24, color=TEXT_COLOR).next_to(sugar_mol, DOWN)

        arrow1 = Arrow(sun.get_right(), plant_shape.get_left(), buff=0.3, color=BLUE_ACCENT)
        arrow2 = Arrow(plant_shape.get_right(), sugar_mol.get_left(), buff=0.3, color=BLUE_ACCENT)

        self.play(FadeIn(sun, sun_label), Create(plant_shape), Write(plant_label), run_time=1.5)
        self.play(GrowArrow(arrow1), run_time=0.8)
        self.play(FadeIn(sugar_mol, sugar_label), run_time=1)
        self.play(GrowArrow(arrow2), run_time=0.8)
        self.wait(1)

        # Formal notation: Chemical equation for photosynthesis using MathTex
        photosynthesis_eq = MathTex(
            r"6\text{CO}_2", r"+", r"6\text{H}_2\text{O}", r"+", r"\text{Light Energy}",
            r"\rightarrow", r"\text{C}_6\text{H}_{12}\text{O}_6", r"+", r"6\text{O}_2",
            color=TEXT_COLOR
        ).scale(0.7).to_edge(DOWN)
        
        self.play(Write(photosynthesis_eq), run_time=2)
        # Highlight connections between intuition and formal notation
        self.play(
            Indicate(VGroup(sun_label, photosynthesis_eq[4]), color=YELLOW),
            Indicate(VGroup(plant_label, photosynthesis_eq[0], photosynthesis_eq[2]), color=GREEN_E),
            Indicate(VGroup(sugar_label, photosynthesis_eq[6]), color=GOLD_ACCENT),
            run_time=2
        )
        self.wait(0.5)

        # Clean up
        self.play(
            FadeOut(photosynthesis_title, sun, sun_label, plant_shape, plant_label, sugar_mol, sugar_label, arrow1, arrow2, photosynthesis_eq)
        )
        self.wait(0.5)

        # --- Beat 3: Cellular Respiration (Energy Release) ---
        respiration_title = Text("2. Cellular Respiration: Releasing Energy", font_size=40, color=BLUE_ACCENT).to_edge(UP)
        self.play(Write(respiration_title))

        # Intuition: Sugar -> Organism -> ATP (usable energy)
        sugar_mol_res = Circle(radius=0.3, color=GOLD_ACCENT, fill_opacity=0.8).move_to([-2, 0, 0])
        sugar_label_res = Text("Sugar", font_size=24, color=TEXT_COLOR).next_to(sugar_mol_res, DOWN)

        # Simple organism shape without external files
        organism_shape = VGroup(
            RegularPolygon(n=5, color=BLUE_ACCENT, fill_opacity=0.6).scale(0.8),
            Circle(radius=0.2, color=TEXT_COLOR, fill_opacity=0.8).shift(UP*0.3 + LEFT*0.2), # Eye 1
            Circle(radius=0.2, color=TEXT_COLOR, fill_opacity=0.8).shift(UP*0.3 + RIGHT*0.2)  # Eye 2
        ).move_to(ORIGIN)
        organism_label = Text("Organism", font_size=24, color=TEXT_COLOR).next_to(organism_shape, DOWN)

        # ATP representation
        atp_block = Rectangle(width=0.6, height=0.4, color=GOLD_ACCENT, fill_opacity=0.8).shift(UP*0.3)
        atp_block2 = atp_block.copy().shift(DOWN*0.6)
        atp_label = Text("ATP (Usable Energy)", font_size=24, color=TEXT_COLOR).next_to(VGroup(atp_block, atp_block2), DOWN)
        atp_group = VGroup(atp_block, atp_block2, atp_label).move_to([2, 0, 0])
        
        arrow3 = Arrow(sugar_mol_res.get_right(), organism_shape.get_left(), buff=0.3, color=BLUE_ACCENT)
        arrow4 = Arrow(organism_shape.get_right(), atp_group.get_left(), buff=0.3, color=BLUE_ACCENT)

        self.play(FadeIn(sugar_mol_res, sugar_label_res), Create(organism_shape), Write(organism_label), run_time=1.5)
        self.play(GrowArrow(arrow3), run_time=0.8)
        self.play(FadeIn(atp_group), run_time=1)
        self.play(GrowArrow(arrow4), run_time=0.8)
        self.wait(1)

        # Formal notation: Chemical equation for cellular respiration
        respiration_eq = MathTex(
            r"\text{C}_6\text{H}_{12}\text{O}_6", r"+", r"6\text{O}_2",
            r"\rightarrow", r"6\text{CO}_2", r"+", r"6\text{H}_2\text{O}", r"+", r"\text{ATP (Energy)}",
            color=TEXT_COLOR
        ).scale(0.7).to_edge(DOWN)
        
        self.play(Write(respiration_eq), run_time=2)
        # Highlight connections
        self.play(
            Indicate(VGroup(sugar_label_res, respiration_eq[0]), color=GOLD_ACCENT),
            Indicate(VGroup(organism_label, respiration_eq[8]), color=BLUE_ACCENT), # ATP is used by organism
            Indicate(VGroup(respiration_eq[4], respiration_eq[6])), # CO2, H2O as byproducts
            run_time=2
        )
        self.wait(0.5)

        # Clean up
        self.play(
            FadeOut(respiration_title, sugar_mol_res, sugar_label_res, organism_shape, organism_label, atp_group, arrow3, arrow4, respiration_eq)
        )
        self.wait(0.5)

        # --- Beat 4: The Cycle (Continuity & Systems) ---
        cycle_title = Text("3. The Interconnected Cycle", font_size=40, color=BLUE_ACCENT).to_edge(UP)
        self.play(Write(cycle_title))

        # Position elements for a clear cyclic flow
        photosynthesis_text = Text("Photosynthesis", font_size=30, color=BLUE_ACCENT).move_to(LEFT*3.5 + UP*1)
        respiration_text = Text("Cellular Respiration", font_size=30, color=GOLD_ACCENT).move_to(RIGHT*3.5 + DOWN*1)

        photosynthesis_box = SurroundingRectangle(photosynthesis_text, color=BLUE_ACCENT, buff=0.5)
        respiration_box = SurroundingRectangle(respiration_text, color=GOLD_ACCENT, buff=0.5)

        self.play(
            Create(photosynthesis_box), Write(photosynthesis_text),
            Create(respiration_box), Write(respiration_text),
            run_time=1.5
        )

        # Inputs and outputs for Photosynthesis
        light_source = Dot(color=YELLOW).move_to(photosynthesis_box.get_top() + UP*0.5)
        light_label = Text("Light Energy", font_size=20, color=YELLOW).next_to(light_source, UP)
        co2_h2o_in_p = MathTex(r"\text{CO}_2 + \text{H}_2\text{O}", color=TEXT_COLOR).scale(0.7).next_to(photosynthesis_box, LEFT, buff=0.5)
        glucose_o2_out_p = MathTex(r"\text{Glucose} + \text{O}_2", color=TEXT_COLOR).scale(0.7).next_to(photosynthesis_box, RIGHT, buff=0.5)
        
        arrow_light = Arrow(light_source.get_bottom(), photosynthesis_box.get_top(), color=YELLOW, buff=0.1)
        arrow_co2_in_p = Arrow(co2_h2o_in_p.get_right(), photosynthesis_box.get_left(), color=TEXT_COLOR, buff=0.1)
        arrow_glucose_out_p = Arrow(photosynthesis_box.get_right(), glucose_o2_out_p.get_left(), color=TEXT_COLOR, buff=0.1)

        self.play(
            LaggedStart( # Lively staggered appearance of elements
                FadeIn(light_source, light_label, arrow_light),
                FadeIn(co2_h2o_in_p, arrow_co2_in_p),
                FadeIn(glucose_o2_out_p, arrow_glucose_out_p),
                lag_ratio=0.5,
                run_time=3
            )
        )
        self.wait(0.5)

        # Inputs and outputs for Cellular Respiration
        atp_text_r = Text("ATP Energy", font_size=20, color=GOLD_ACCENT).next_to(respiration_box, DOWN, buff=0.5)
        glucose_o2_in_r = MathTex(r"\text{Glucose} + \text{O}_2", color=TEXT_COLOR).scale(0.7).next_to(respiration_box, LEFT, buff=0.5)
        co2_h2o_out_r = MathTex(r"\text{CO}_2 + \text{H}_2\text{O}", color=TEXT_COLOR).scale(0.7).next_to(respiration_box, RIGHT, buff=0.5)

        arrow_atp_out_r = Arrow(respiration_box.get_bottom(), atp_text_r.get_top(), color=GOLD_ACCENT, buff=0.1)
        arrow_glucose_in_r = Arrow(glucose_o2_in_r.get_right(), respiration_box.get_left(), color=TEXT_COLOR, buff=0.1)
        arrow_co2_out_r = Arrow(respiration_box.get_right(), co2_h2o_out_r.get_left(), color=TEXT_COLOR, buff=0.1)

        self.play(
            LaggedStart( # Lively staggered appearance of elements
                FadeIn(atp_text_r, arrow_atp_out_r),
                FadeIn(glucose_o2_in_r, arrow_glucose_in_r),
                FadeIn(co2_h2o_out_r, arrow_co2_out_r),
                lag_ratio=0.5,
                run_time=3
            )
        )
        self.wait(0.5)

        # Connect the cycle using CurvedArrows for visual flow
        cycle_arrow_1 = CurvedArrow(
            glucose_o2_out_p.get_bottom() + DOWN*0.2, # Start slightly below photosynthesis output
            glucose_o2_in_r.get_top() + UP*0.2,     # End slightly above respiration input
            angle=-PI/2, # Defines the curve direction
            color=BLUE_ACCENT,
            tip_length=0.2
        )
        cycle_arrow_1_label = Text("Energy stored in food", font_size=20, color=TEXT_COLOR).next_to(cycle_arrow_1, RIGHT, buff=0.1)

        cycle_arrow_2 = CurvedArrow(
            co2_h2o_out_r.get_top() + UP*0.2,       # Start slightly above respiration output
            co2_h2o_in_p.get_bottom() + DOWN*0.2,   # End slightly below photosynthesis input
            angle=-PI/2, # Defines the curve direction
            color=GOLD_ACCENT,
            tip_length=0.2
        )
        cycle_arrow_2_label = Text("Waste for plants", font_size=20, color=TEXT_COLOR).next_to(cycle_arrow_2, LEFT, buff=0.1)

        self.play(
            GrowArrow(cycle_arrow_1), Write(cycle_arrow_1_label),
            run_time=1.5
        )
        self.play(
            GrowArrow(cycle_arrow_2), Write(cycle_arrow_2_label),
            run_time=1.5
        )
        self.wait(2)

        # Clean up everything on screen for the recap card
        self.play(
            FadeOut(VGroup(*self.mobjects)) 
        )
        self.wait(0.5)

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Energy Flow in Life", font_size=50, color=BLUE_ACCENT).to_edge(UP)
        
        recap_items = VGroup(
            Text("• Photosynthesis: Light energy → Chemical energy (Glucose)", font_size=30, color=TEXT_COLOR),
            Text("• Cellular Respiration: Chemical energy (Glucose) → Usable energy (ATP)", font_size=30, color=TEXT_COLOR),
            Text("• The Cycle: These processes are fundamentally linked, sustaining ecosystems.", font_size=30, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(recap_title, DOWN, buff=0.8).to_edge(LEFT, buff=1)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[Write(item) for item in recap_items], lag_ratio=0.7))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_items)))
        self.wait(1)