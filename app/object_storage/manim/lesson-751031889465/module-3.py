from manim import *
import os # Import os for checking file existence

# Fallback for SVG if not available. Creates a simple plant shape.
def get_simple_plant_icon():
    stem = Rectangle(width=0.3, height=1.5, color=GREEN_B, fill_opacity=0.8).move_to(ORIGIN + DOWN*0.75)
    leaf1 = Ellipse(width=1, height=0.5, color=GREEN_D, fill_opacity=0.9).rotate(PI/4).shift(UP*0.2 + LEFT*0.4)
    leaf2 = Ellipse(width=1, height=0.5, color=GREEN_D, fill_opacity=0.9).rotate(-PI/4).shift(UP*0.2 + RIGHT*0.4)
    flower_center = Circle(radius=0.2, color=YELLOW, fill_opacity=1).shift(UP*0.8)
    # Simple petals
    petal1 = Polygon([flower_center.get_center(), flower_center.get_center() + UP*0.5 + LEFT*0.2, flower_center.get_center() + UP*0.5 + RIGHT*0.2], color=ORANGE, fill_opacity=1).rotate(PI/4)
    petal2 = petal1.copy().rotate(PI/2, about_point=flower_center.get_center())
    petal3 = petal1.copy().rotate(PI, about_point=flower_center.get_center())
    petal4 = petal1.copy().rotate(3*PI/2, about_point=flower_center.get_center())
    flower = VGroup(flower_center, petal1, petal2, petal3, petal4)
    return VGroup(stem, leaf1, leaf2, flower).scale(0.8) # Adjust scale as needed

class CellularEnergyAnimation(Scene):
    def construct(self):
        # --- Scene 1: Title Card ---
        title = Text("Cellular Energy:", font_size=72, color=BLUE).shift(UP*0.5)
        subtitle = Text("Photosynthesis and Respiration", font_size=60, color=GREEN).shift(DOWN*0.5)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5) # Total ~4.5 seconds (2 writes + 1.5 wait)

        self.play(FadeOut(title, shift=UP), FadeOut(subtitle, shift=DOWN))
        self.wait(0.5)

        # --- Scene 2: Why Energy? ---
        life_needs_energy_text = Text("Life Fundamentally Relies on Energy", font_size=48, color=WHITE)
        self.play(Write(life_needs_energy_text))
        self.wait(1.5)

        # Illustrate 'energy' using a pulsing core, initially for the text transform
        energy_core_temp = Circle(radius=0.8, color=YELLOW, fill_opacity=0.8)
        energy_symbol_temp = Text("E", font_size=96, color=BLACK).move_to(energy_core_temp)
        energy_group_temp = VGroup(energy_core_temp, energy_symbol_temp)
        
        # Position the 'E' in a smaller form at the top left as a persistent hint
        self.play(Transform(life_needs_energy_text, energy_group_temp.copy().scale(0.5).to_corner(UL).shift(RIGHT*0.5)))
        self.wait(0.5)

        # Main energy symbol in center, with radiating work examples
        main_energy_core = Circle(radius=1.2, color=YELLOW, fill_opacity=0.8)
        main_energy_symbol = Text("E", font_size=120, color=BLACK).move_to(main_energy_core)
        main_energy_group = VGroup(main_energy_core, main_energy_symbol)

        self.play(FadeIn(main_energy_group))
        
        # Add examples of what energy is for
        growth = Text("Growth", font_size=36, color=PINK).next_to(main_energy_group, DR, buff=0.8)
        movement = Text("Movement", font_size=36, color=RED).next_to(main_energy_group, DOWN, buff=0.8)
        reproduction = Text("Reproduction", font_size=36, color=ORANGE).next_to(main_energy_group, DL, buff=0.8)
        
        self.play(FadeIn(growth, shift=UP), FadeIn(movement, shift=UP), FadeIn(reproduction, shift=UP))
        self.wait(2) # Total ~7.5 seconds (Write + Transform + FadeIn main group + 3 FadeIns + 2 wait)

        self.play(FadeOut(VGroup(main_energy_group, growth, movement, reproduction, life_needs_energy_text))) # Fade out the old transformed text too
        self.wait(0.5)

        # --- Scene 3: Energy Source (Sun) ---
        sun = Circle(radius=1, color=YELLOW_E, fill_opacity=1).move_to(LEFT * 3 + UP * 1.5)
        sun_label = Text("Sun", color=YELLOW_D).next_to(sun, DOWN)
        
        self.play(Create(sun), FadeIn(sun_label))
        self.wait(0.5)

        sun_rays = VGroup(*[
            Line(sun.get_center(), sun.get_center() + rotate_vector(UP*2, TAU/8 * i), color=YELLOW_A, stroke_width=3)
            for i in range(8)
        ])
        self.play(Create(sun_rays, run_time=1))

        source_text = Text("Ultimate Source: The Sun", font_size=48, color=WHITE).to_edge(RIGHT).shift(UP*1.5)
        self.play(Write(source_text))
        self.wait(2) # Total ~6 seconds (Create/FadeIn + Create + Write + 2 wait)

        self.play(FadeOut(sun, sun_label, sun_rays, source_text))
        self.wait(0.5)
        
        # --- Scene 4: Introducing Photosynthesis ---
        photosynthesis_title = Text("1. Photosynthesis", font_size=60, color=GREEN).to_edge(UP)
        self.play(Write(photosynthesis_title))
        self.wait(0.5)

        # Check for SVG in 'assets/' directory, otherwise use fallback
        if os.path.exists("assets/plant_icon.svg"):
            plant_icon = SVGMobject("assets/plant_icon.svg").scale(1.5).shift(LEFT*3)
        else:
            plant_icon = get_simple_plant_icon().scale(1.5).shift(LEFT*3)
            
        self.play(FadeIn(plant_icon))

        # Inputs
        co2_input = Text("CO₂", color=BLUE_A, font_size=40).shift(LEFT*5.5 + UP*1)
        h2o_input = Text("H₂O", color=BLUE_B, font_size=40).shift(LEFT*5.5 + DOWN*0.5)
        sun_energy_input = Text("Light Energy", color=YELLOW, font_size=40).shift(LEFT*5.5 + UP*2.5)

        arrow_co2 = Arrow(co2_input.get_right(), plant_icon.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        arrow_h2o = Arrow(h2o_input.get_right(), plant_icon.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        arrow_sun = Arrow(sun_energy_input.get_right(), plant_icon.get_top(), buff=0.1, color=YELLOW, stroke_width=2)
        
        self.play(FadeIn(co2_input), Create(arrow_co2), FadeIn(h2o_input), Create(arrow_h2o), FadeIn(sun_energy_input), Create(arrow_sun))
        self.wait(1)

        # Outputs
        glucose_output = Text("C₆H₁₂O₆ (Glucose)", color=ORANGE, font_size=40).shift(RIGHT*4 + UP*1.5)
        o2_output = Text("O₂", color=RED_B, font_size=40).shift(RIGHT*4 + DOWN*0.5)

        arrow_glucose = Arrow(plant_icon.get_right(), glucose_output.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        arrow_o2 = Arrow(plant_icon.get_right(), o2_output.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        
        self.play(Create(arrow_glucose), FadeIn(glucose_output), Create(arrow_o2), FadeIn(o2_output))
        self.wait(1.5) # Total ~9 seconds (Write + FadeIn + 6 FadeIn/Create + 2 wait)

        photosynthesis_scene_objects = VGroup(photosynthesis_title, plant_icon, co2_input, h2o_input, sun_energy_input, 
                                            arrow_co2, arrow_h2o, arrow_sun, glucose_output, o2_output, arrow_glucose, arrow_o2)
        self.play(FadeOut(photosynthesis_scene_objects))
        self.wait(0.5)

        # --- Scene 5: Introducing Respiration ---
        respiration_title = Text("2. Cellular Respiration", font_size=60, color=RED).to_edge(UP)
        self.play(Write(respiration_title))
        self.wait(0.5)

        animal_cell_icon = Circle(radius=1.5, color=MAROON, fill_opacity=0.7).shift(LEFT*3)
        nucleus = Circle(radius=0.5, color=MAROON_D, fill_opacity=0.9).move_to(animal_cell_icon.get_center() + RIGHT*0.3 + UP*0.3)
        cell_label = Text("Animal Cell", font_size=30, color=WHITE).next_to(animal_cell_icon, DOWN)
        self.play(FadeIn(animal_cell_icon), FadeIn(nucleus), FadeIn(cell_label))

        # Inputs (Glucose & Oxygen from Photosynthesis)
        glucose_input_resp = Text("C₆H₁₂O₆ (Glucose)", color=ORANGE, font_size=40).shift(LEFT*5.5 + UP*1.5)
        o2_input_resp = Text("O₂", color=RED_B, font_size=40).shift(LEFT*5.5 + DOWN*0.5)
        
        arrow_glucose_resp = Arrow(glucose_input_resp.get_right(), animal_cell_icon.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        arrow_o2_resp = Arrow(o2_input_resp.get_right(), animal_cell_icon.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        
        self.play(FadeIn(glucose_input_resp), Create(arrow_glucose_resp), FadeIn(o2_input_resp), Create(arrow_o2_resp))
        self.wait(1)

        # Outputs
        atp_output = Text("ATP (Energy)", color=YELLOW_A, font_size=40).shift(RIGHT*4 + UP*1.5)
        co2_output_resp = Text("CO₂", color=BLUE_A, font_size=40).shift(RIGHT*4 + UP*0)
        h2o_output_resp = Text("H₂O", color=BLUE_B, font_size=40).shift(RIGHT*4 + DOWN*1.5)

        arrow_atp = Arrow(animal_cell_icon.get_right(), atp_output.get_left(), buff=0.1, color=YELLOW, stroke_width=2)
        arrow_co2_resp = Arrow(animal_cell_icon.get_right(), co2_output_resp.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        arrow_h2o_resp = Arrow(animal_cell_icon.get_right(), h2o_output_resp.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        
        self.play(Create(arrow_atp), FadeIn(atp_output), Create(arrow_co2_resp), FadeIn(co2_output_resp), Create(arrow_h2o_resp), FadeIn(h2o_output_resp))
        self.wait(1.5) # Total ~9 seconds (Write + 3 FadeIn + 6 FadeIn/Create + 2 wait)

        respiration_scene_objects = VGroup(respiration_title, animal_cell_icon, nucleus, cell_label, glucose_input_resp, 
                                            o2_input_resp, arrow_glucose_resp, arrow_o2_resp, atp_output, 
                                            co2_output_resp, h2o_output_resp, arrow_atp, arrow_co2_resp, arrow_h2o_resp)
        self.play(FadeOut(respiration_scene_objects))
        self.wait(0.5)

        # --- Scene 6: The Cycle / Interconnection ---
        cycle_title = Text("The Fundamental Cycle", font_size=60, color=WHITE).to_edge(UP)
        self.play(Write(cycle_title))
        self.wait(0.5)

        # Simplified Plant and Animal cells for the cycle
        plant_box = Rectangle(width=3, height=2, color=GREEN_C, fill_opacity=0.7).shift(UP*0.5 + LEFT*3.5)
        plant_label_cycle = Text("Plant (Photosynthesis)", font_size=28, color=BLACK).move_to(plant_box)
        
        animal_box = Rectangle(width=3, height=2, color=RED_C, fill_opacity=0.7).shift(UP*0.5 + RIGHT*3.5)
        animal_label_cycle = Text("Animal (Respiration)", font_size=28, color=BLACK).move_to(animal_box)

        self.play(FadeIn(plant_box), FadeIn(plant_label_cycle), FadeIn(animal_box), FadeIn(animal_label_cycle))
        self.wait(0.5)

        # Flow from Plant to Animal (Glucose & O2)
        glucose_o2_arrow = CurvedArrow(plant_box.get_right(), animal_box.get_left(), angle=-TAU/4, color=ORANGE, buff=0.1)
        glucose_o2_label = Text("Glucose & O₂", font_size=28, color=ORANGE).next_to(glucose_o2_arrow, UP*0.2) 
        
        self.play(Create(glucose_o2_arrow), FadeIn(glucose_o2_label))
        self.wait(1)

        # Flow from Animal to Plant (CO2 & H2O)
        co2_h2o_arrow = CurvedArrow(animal_box.get_left(), plant_box.get_right(), angle=TAU/4, color=BLUE_A, buff=0.1)
        co2_h2o_label = Text("CO₂ & H₂O", font_size=28, color=BLUE_A).next_to(co2_h2o_arrow, DOWN*0.2) 
        
        self.play(Create(co2_h2o_arrow), FadeIn(co2_h2o_label))
        self.wait(1.5)

        # Add "Energy" output from animal
        atp_output_cycle = Text("ATP (Energy)", color=YELLOW_A, font_size=32).next_to(animal_box, DOWN, buff=0.5)
        atp_arrow_cycle = Arrow(animal_box.get_bottom(), atp_output_cycle.get_top(), buff=0.1, color=YELLOW_A)
        
        self.play(Create(atp_arrow_cycle), FadeIn(atp_output_cycle))
        self.wait(1.5) # Total ~9 seconds (Write + 4 FadeIn + 2 Create/FadeIn + 2 Create/FadeIn + 3 wait)

        self.play(FadeOut(VGroup(cycle_title, plant_box, plant_label_cycle, animal_box, animal_label_cycle,
                                  glucose_o2_arrow, glucose_o2_label, co2_h2o_arrow, co2_h2o_label,
                                  atp_output_cycle, atp_arrow_cycle)))
        self.wait(0.5)

        # --- Scene 7: Wrap-up/Call to Action ---
        end_text = Text("Cellular Energy: The Core of Life", font_size=60, color=WHITE)
        self.play(Write(end_text))
        self.wait(1.5)
        
        final_message = Text("Understand the Cycle, Understand Life!", font_size=40, color=GOLD).next_to(end_text, DOWN, buff=0.8)
        self.play(FadeIn(final_message, shift=UP))
        self.wait(2)
        
        self.play(FadeOut(end_text, final_message))
        self.wait(0.5)