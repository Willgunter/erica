from manim import *

# Define custom colors for 3b1b style
# Dark background is set directly on camera.background_color
BLUE_ACCENT = "#87CEEB"  # Bright sky blue
GOLD_ACCENT = "#FFD700"  # Bright gold
GREEN_ORGANELLE = "#7CFC00" # Green for chloroplast
MAROON_ORGANELLE = "#800000" # Maroon for mitochondria
TEXT_MAIN = WHITE

class CellularEnergy(Scene):
    def construct(self):
        # 1. Configuration: Clean dark background with high-contrast blue and gold accents
        self.camera.background_color = "#1a1a1a" # Very dark grey/black background

        # --- Beat 1: Title & Hook (Energy Flow) ---
        title = Text("Cellular Energy:", color=BLUE_ACCENT).scale(1.5)
        subtitle = Text("Photosynthesis & Respiration", color=GOLD_ACCENT).scale(1.2)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)

        self.play(Write(title_group))
        self.wait(1)
        self.play(title_group.animate.to_edge(UP).scale(0.7), run_time=1.5)

        # Visual Hook: Abstract energy flow
        energy_source = Circle(radius=0.7, color=GOLD_ACCENT, fill_opacity=0.8)
        energy_source.set_x(-config.frame_width/3)
        energy_source_label = MathTex("\\text{Sunlight}", color=TEXT_MAIN).next_to(energy_source, LEFT)

        energy_converter_plant = Rectangle(width=2, height=2, color=GREEN_ORGANELLE, fill_opacity=0.3)
        energy_converter_plant_label = Text("Plant", font_size=36, color=TEXT_MAIN).move_to(energy_converter_plant)
        energy_converter_plant.set_x(0)

        energy_output = Circle(radius=0.7, color=BLUE_ACCENT, fill_opacity=0.8) # Representing chemical energy/glucose
        energy_output.set_x(config.frame_width/3)
        energy_output_label = Text("Chemical Energy", font_size=30, color=TEXT_MAIN).next_to(energy_output, RIGHT)

        arrow1 = Arrow(start=energy_source.get_right(), end=energy_converter_plant.get_left(), buff=0.1, color=GOLD_ACCENT)
        arrow2 = Arrow(start=energy_converter_plant.get_right(), end=energy_output.get_left(), buff=0.1, color=BLUE_ACCENT)

        energy_flow_group = VGroup(energy_source, energy_source_label, energy_converter_plant, energy_converter_plant_label, energy_output, energy_output_label, arrow1, arrow2)

        self.play(FadeIn(energy_source, energy_source_label, shift=LEFT))
        self.play(GrowArrow(arrow1))
        self.play(Create(energy_converter_plant), Write(energy_converter_plant_label))
        self.play(GrowArrow(arrow2))
        self.play(FadeIn(energy_output, energy_output_label, shift=RIGHT))
        self.wait(1.5)
        self.play(FadeOut(energy_flow_group, shift=UP)) # Clear for next beat

        # --- Beat 2: Photosynthesis ---
        photosynthesis_title = Text("Photosynthesis", color=BLUE_ACCENT).scale(1).to_edge(UP)
        self.play(Transform(title_group, photosynthesis_title))

        # Inputs
        co2_in = MathTex("\\text{CO}_2", color=TEXT_MAIN).scale(1.2).move_to([-4, 2, 0])
        h2o_in = MathTex("\\text{H}_2\\text{O}", color=TEXT_MAIN).scale(1.2).move_to([-4, 0, 0])
        sun_icon = Star(n=8, outer_radius=0.4, inner_radius=0.2, color=GOLD_ACCENT, fill_opacity=0.8).move_to([-4, -2, 0])
        sunlight_label = Text("Sunlight", font_size=28, color=TEXT_MAIN).next_to(sun_icon, LEFT, buff=0.1)
        sun_group = VGroup(sun_icon, sunlight_label)

        # Plant/Chloroplast
        plant_box = Rectangle(width=3, height=4, color=GREEN_ORGANELLE, fill_opacity=0.2).move_to([0, 0, 0])
        plant_label = Text("Chloroplast", font_size=30, color=TEXT_MAIN).move_to(plant_box.get_center())

        # Outputs
        glucose_out = MathTex("\\text{C}_6\\text{H}_{12}\\text{O}_6", color=GOLD_ACCENT).scale(1.2).move_to([4, 1.5, 0])
        oxygen_out = MathTex("\\text{O}_2", color=TEXT_MAIN).scale(1.2).move_to([4, -1.5, 0])

        self.play(FadeIn(co2_in, shift=LEFT), FadeIn(h2o_in, shift=LEFT), FadeIn(sun_group, shift=LEFT))
        self.play(Create(plant_box), Write(plant_label))

        arrow_co2 = Arrow(co2_in.get_right(), plant_box.get_top() + LEFT*0.5, buff=0.1, color=TEXT_MAIN)
        arrow_h2o = Arrow(h2o_in.get_right(), plant_box.get_center() + LEFT*0.5, buff=0.1, color=TEXT_MAIN)
        arrow_sun = Arrow(sun_group.get_right(), plant_box.get_bottom() + LEFT*0.5, buff=0.1, color=GOLD_ACCENT)
        
        self.play(GrowArrow(arrow_co2), GrowArrow(arrow_h2o), GrowArrow(arrow_sun))
        self.wait(0.5)

        self.play(FadeIn(glucose_out, shift=RIGHT), FadeIn(oxygen_out, shift=RIGHT))
        arrow_glucose = Arrow(plant_box.get_top() + RIGHT*0.5, glucose_out.get_left(), buff=0.1, color=GOLD_ACCENT)
        arrow_oxygen = Arrow(plant_box.get_bottom() + RIGHT*0.5, oxygen_out.get_left(), buff=0.1, color=TEXT_MAIN)
        self.play(GrowArrow(arrow_glucose), GrowArrow(arrow_oxygen))
        self.wait(1.5)

        # Photosynthesis Equation (briefly)
        photo_eq = MathTex(
            "6\\text{CO}_2", "+", "6\\text{H}_2\\text{O}", "+", "\\text{Sunlight}", "\\rightarrow", 
            "\\text{C}_6\\text{H}_{12}\\text{O}_6", "+", "6\\text{O}_2",
            color=TEXT_MAIN
        ).scale(0.8).next_to(plant_box, DOWN, buff=0.5)

        self.play(
            FadeOut(co2_in, h2o_in, sun_group, arrow_co2, arrow_h2o, arrow_sun),
            FadeOut(plant_box, plant_label),
            FadeOut(glucose_out, oxygen_out, arrow_glucose, arrow_oxygen),
            title_group.animate.shift(UP*1), # Keep title visible but make space
            LaggedStart(
                Write(photo_eq[0:5], run_time=1),
                FadeIn(photo_eq[5]),
                Write(photo_eq[6:], run_time=1),
                lag_ratio=0.5
            )
        )
        self.wait(1)
        self.play(FadeOut(photo_eq))

        # --- Beat 3: Cellular Respiration ---
        respiration_title = Text("Cellular Respiration", color=GOLD_ACCENT).scale(1).to_edge(UP)
        self.play(Transform(title_group, respiration_title))

        # Inputs (Glucose & Oxygen - products of Photosynthesis)
        glucose_in_res = MathTex("\\text{C}_6\\text{H}_{12}\\text{O}_6", color=GOLD_ACCENT).scale(1.2).move_to([-4, 1.5, 0])
        oxygen_in_res = MathTex("\\text{O}_2", color=TEXT_MAIN).scale(1.2).move_to([-4, -1.5, 0])
        
        # Mitochondria
        mito_box = Ellipse(width=4, height=2.5, color=MAROON_ORGANELLE, fill_opacity=0.3).move_to([0, 0, 0])
        mito_label = Text("Mitochondria", font_size=30, color=TEXT_MAIN).move_to(mito_box.get_center())

        # Outputs
        co2_out_res = MathTex("\\text{CO}_2", color=TEXT_MAIN).scale(1.2).move_to([4, 2, 0])
        h2o_out_res = MathTex("\\text{H}_2\\text{O}", color=TEXT_MAIN).scale(1.2).move_to([4, 0, 0])
        atp_out = MathTex("\\text{ATP}", color=BLUE_ACCENT).scale(1.5).move_to([4, -2, 0])

        self.play(FadeIn(glucose_in_res, shift=LEFT), FadeIn(oxygen_in_res, shift=LEFT))
        self.play(Create(mito_box), Write(mito_label))

        arrow_glucose_res = Arrow(glucose_in_res.get_right(), mito_box.get_top() + LEFT*0.5, buff=0.1, color=GOLD_ACCENT)
        arrow_oxygen_res = Arrow(oxygen_in_res.get_right(), mito_box.get_bottom() + LEFT*0.5, buff=0.1, color=TEXT_MAIN)
        self.play(GrowArrow(arrow_glucose_res), GrowArrow(arrow_oxygen_res))
        self.wait(0.5)

        self.play(FadeIn(co2_out_res, shift=RIGHT), FadeIn(h2o_out_res, shift=RIGHT), FadeIn(atp_out, shift=RIGHT))
        arrow_co2_res = Arrow(mito_box.get_top() + RIGHT*0.5, co2_out_res.get_left(), buff=0.1, color=TEXT_MAIN)
        arrow_h2o_res = Arrow(mito_box.get_center() + RIGHT*0.5, h2o_out_res.get_left(), buff=0.1, color=TEXT_MAIN)
        arrow_atp = Arrow(mito_box.get_bottom() + RIGHT*0.5, atp_out.get_left(), buff=0.1, color=BLUE_ACCENT)
        self.play(GrowArrow(arrow_co2_res), GrowArrow(arrow_h2o_res), GrowArrow(arrow_atp))
        self.wait(1.5)

        # Respiration Equation (briefly)
        resp_eq = MathTex(
            "\\text{C}_6\\text{H}_{12}\\text{O}_6", "+", "6\\text{O}_2", "\\rightarrow", 
            "6\\text{CO}_2", "+", "6\\text{H}_2\\text{O}", "+", "\\text{ATP}",
            color=TEXT_MAIN
        ).scale(0.8).next_to(mito_box, DOWN, buff=0.5)

        self.play(
            FadeOut(glucose_in_res, oxygen_in_res, arrow_glucose_res, arrow_oxygen_res),
            FadeOut(mito_box, mito_label),
            FadeOut(co2_out_res, h2o_out_res, atp_out, arrow_co2_res, arrow_h2o_res, arrow_atp),
            LaggedStart(
                Write(resp_eq[0:3], run_time=1),
                FadeIn(resp_eq[3]),
                Write(resp_eq[4:], run_time=1),
                lag_ratio=0.5
            )
        )
        self.wait(1)
        self.play(FadeOut(resp_eq))

        # --- Beat 4: The Cycle & ATP ---
        cycle_title = Text("The Energy Cycle", color=BLUE_ACCENT).scale(1).to_edge(UP)
        self.play(Transform(title_group, cycle_title))

        # Re-introduce photosynthesis and respiration as interconnected boxes
        photo_process = Text("Photosynthesis", font_size=36, color=GREEN_ORGANELLE).to_edge(LEFT, buff=1.5).shift(UP*0.5)
        resp_process = Text("Respiration", font_size=36, color=MAROON_ORGANELLE).to_edge(RIGHT, buff=1.5).shift(UP*0.5)

        self.play(FadeIn(photo_process, shift=LEFT), FadeIn(resp_process, shift=RIGHT))

        # Inputs/Outputs for the cycle
        cycle_co2_h2o = VGroup(
            MathTex("\\text{CO}_2", color=TEXT_MAIN),
            MathTex("\\text{H}_2\\text{O}", color=TEXT_MAIN)
        ).arrange(DOWN, buff=0.0).next_to(photo_process, UP, buff=0.5)
        
        cycle_sun = Star(n=8, outer_radius=0.3, inner_radius=0.15, color=GOLD_ACCENT, fill_opacity=0.8).next_to(cycle_co2_h2o, DOWN, buff=0.5)
        cycle_sun_label = Text("Sunlight", font_size=24, color=TEXT_MAIN).next_to(cycle_sun, RIGHT, buff=0.1)
        cycle_sun_group = VGroup(cycle_sun, cycle_sun_label)


        cycle_glucose_o2 = VGroup(
            MathTex("\\text{C}_6\\text{H}_{12}\\text{O}_6", color=GOLD_ACCENT),
            MathTex("\\text{O}_2", color=TEXT_MAIN)
        ).arrange(DOWN, buff=0.0).next_to(resp_process, UP, buff=0.5)

        cycle_atp = MathTex("\\text{ATP}", color=BLUE_ACCENT).scale(1.2).next_to(resp_process, DOWN, buff=0.5)

        # Arrows connecting inputs to photosynthesis
        arrow_photo_inputs = Arrow(cycle_co2_h2o.get_bottom(), photo_process.get_top(), buff=0.1, color=TEXT_MAIN)
        arrow_sun_input = Arrow(cycle_sun_group.get_bottom(), photo_process.get_top()+DOWN*0.5+LEFT*0.5, buff=0.1, color=GOLD_ACCENT)
        
        # Curved arrows for the cycle
        arrow_photo_to_resp = ArcArrow(
            photo_process.get_right() + RIGHT * 0.2 + UP * 0.5,
            resp_process.get_left() + LEFT * 0.2 + UP * 0.5,
            color=TEXT_MAIN,
            tip_length=0.2,
            arc_config={'angle': -TAU/4} # Arc downwards
        )
        arrow_photo_to_resp_label = Text("Glucose, O2", font_size=24, color=TEXT_MAIN).next_to(arrow_photo_to_resp, UP, buff=0.1)

        arrow_resp_to_photo = ArcArrow(
            resp_process.get_left() + LEFT * 0.2 + DOWN * 0.5,
            photo_process.get_right() + RIGHT * 0.2 + DOWN * 0.5,
            color=TEXT_MAIN,
            tip_length=0.2,
            arc_config={'angle': TAU/4} # Arc upwards
        )
        arrow_resp_to_photo_label = Text("CO2, H2O", font_size=24, color=TEXT_MAIN).next_to(arrow_resp_to_photo, DOWN, buff=0.1)

        arrow_resp_atp = Arrow(resp_process.get_bottom(), cycle_atp.get_top(), buff=0.1, color=BLUE_ACCENT)

        self.play(FadeIn(cycle_co2_h2o, shift=UP), FadeIn(cycle_sun_group, shift=UP))
        self.play(GrowArrow(arrow_photo_inputs), GrowArrow(arrow_sun_input))

        self.play(
            LaggedStart(
                FadeIn(cycle_glucose_o2, shift=UP),
                GrowArrow(arrow_photo_to_resp),
                Write(arrow_photo_to_resp_label),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)

        self.play(
            LaggedStart(
                GrowArrow(arrow_resp_to_photo),
                Write(arrow_resp_to_photo_label),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)

        # Introduce ATP
        atp_label = Text("Energy Currency", font_size=30, color=BLUE_ACCENT).next_to(cycle_atp, DOWN, buff=0.2)
        self.play(FadeIn(cycle_atp, shift=DOWN), GrowArrow(arrow_resp_atp), Write(atp_label))
        self.wait(2)

        self.play(FadeOut(VGroup(photo_process, resp_process, cycle_co2_h2o, cycle_sun_group, cycle_glucose_o2, cycle_atp, atp_label, 
                                 arrow_photo_inputs, arrow_sun_input, arrow_photo_to_resp, arrow_photo_to_resp_label, 
                                 arrow_resp_to_photo, arrow_resp_to_photo_label, arrow_resp_atp)))
        
        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Cellular Energy", color=GOLD_ACCENT).scale(1.2).to_edge(UP)
        self.play(Transform(title_group, recap_title))

        recap_points = BulletedList(
            "Photosynthesis: Converts light energy to chemical energy (Glucose).",
            "Respiration: Breaks down glucose to release usable energy (ATP).",
            "These processes form a continuous cycle, vital for life.",
            font_size=36,
            color=TEXT_MAIN
        ).scale(0.8).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=1).shift(DOWN*0.5)

        self.play(LaggedStart(*[FadeIn(point, shift=LEFT) for point in recap_points], lag_ratio=0.5))
        self.wait(3)

        final_message = Text("Understand the flow, understand life!", color=BLUE_ACCENT).scale(1).next_to(recap_points, DOWN, buff=1)
        self.play(Write(final_message))
        self.wait(2)
        
        self.play(FadeOut(VGroup(title_group, recap_points, final_message)))