from manim import *

class CellularEnergy(Scene):
    def construct(self):
        # --- Scene Setup ---
        self.camera.background_color = "#1a1a1a" # Dark background
        BLUE_ACCENT = "#64B5F6" # Light blue
        GOLD_ACCENT = "#FFD700" # Gold
        GREEN_ACCENT = "#8BC34A" # Green for plants/glucose
        RED_ACCENT = "#EF5350" # Red for CO2/carbon

        # --- Beat 1: Visual Hook - Life Needs Energy ---
        title = Text("Cellular Energy", font_size=72, color=BLUE_ACCENT).to_edge(UP)
        subtitle = Text("Photosynthesis & Respiration", font_size=48, color=GOLD_ACCENT).next_to(title, DOWN)
        self.play(
            LaggedStart(
                FadeIn(title, shift=UP),
                FadeIn(subtitle, shift=DOWN),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)

        # Sun representing energy source
        sun = Circle(radius=0.8, color=GOLD_ACCENT, fill_opacity=0.8).move_to([-4, 2, 0])
        sun_rays = VGroup(*[
            Line(sun.get_center(), sun.get_center() + 1.5 * UR).rotate(i * 360/8 * DEGREES, about_point=sun.get_center()).set_stroke(GOLD_ACCENT, width=2)
            for i in range(8)
        ])
        sun_label = Text("Sunlight", font_size=24, color=GOLD_ACCENT).next_to(sun, DOWN)

        # Abstract "Life" form
        life_shape = Polygon(
            [-1, -1.5, 0], [1, -1.5, 0], [1.5, -0.5, 0], [0, 0.5, 0], [-1.5, -0.5, 0],
            color=BLUE_ACCENT, fill_opacity=0.3, stroke_width=2
        ).shift(RIGHT * 2 + DOWN * 0.5)
        life_label = Text("Living Organism", font_size=24, color=BLUE_ACCENT).next_to(life_shape, DOWN)

        energy_flow_text = Text("Life Needs Energy", font_size=40, color=GOLD_ACCENT).move_to(ORIGIN)

        self.play(FadeIn(sun, sun_rays), FadeIn(sun_label), run_time=1)
        self.play(Write(energy_flow_text))
        self.wait(0.5)

        # Show energy particles flowing
        energy_particles = VGroup()
        for i in range(10):
            particle = Dot(point=sun.get_center(), color=GOLD_ACCENT, radius=0.05).set_opacity(0)
            energy_particles.add(particle)
            target_point = life_shape.point_from_proportion((i+1)/11)
            self.add(particle)
            self.play(
                particle.animate.set_opacity(1).move_to(target_point),
                run_time=0.8,
                rate_func=linear
            )
            self.wait(0.05) # Small pause between particles

        self.play(
            FadeOut(energy_flow_text),
            FadeIn(life_shape),
            FadeIn(life_label),
            FadeOut(energy_particles), # Fade out particles after flow
            run_time=1
        )
        self.wait(1)

        # --- Transition from Beat 1 to Beat 2 ---
        self.play(
            FadeOut(sun_rays), # Ensure sun_rays are gone
            FadeOut(life_shape, life_label),
            FadeOut(title, subtitle) # Fade out initial titles
        )
        self.wait(0.5)

        # --- Beat 2: Photosynthesis ---
        photosynthesis_title = Text("1. Photosynthesis", font_size=48, color=BLUE_ACCENT).to_edge(UP)
        self.play(FadeIn(photosynthesis_title))

        plant_cell = RoundedRectangle(width=4, height=3, corner_radius=0.5, color=GREEN_ACCENT, fill_opacity=0.2).move_to(ORIGIN + LEFT*2)
        plant_label = Text("Plant Cell", font_size=28, color=GREEN_ACCENT).next_to(plant_cell, DOWN)

        self.play(FadeIn(plant_cell, shift=LEFT), FadeIn(plant_label, shift=LEFT))
        self.play(sun.animate.move_to(plant_cell.get_left() + LEFT*1.5), run_time=0.8) # Move sun closer

        # Inputs for Photosynthesis
        co2_in = MathTex(r"\text{CO}_2", color=RED_ACCENT).scale(0.8).move_to([-5, 1, 0])
        h2o_in = MathTex(r"\text{H}_2\text{O}", color=BLUE_ACCENT).scale(0.8).move_to([-5, -1, 0])
        light_energy_symbol_obj = self.create_light_symbol().scale(0.5).move_to([-5, 2, 0]) # Direct use of Mobject

        self.play(FadeIn(co2_in, shift=LEFT), FadeIn(h2o_in, shift=LEFT), FadeIn(light_energy_symbol_obj, shift=LEFT))
        self.wait(0.5)

        # Show inputs entering cell
        arrow_co2 = Arrow(co2_in.get_right(), plant_cell.get_left() + UP*0.5, buff=0.1, color=RED_ACCENT)
        arrow_h2o = Arrow(h2o_in.get_right(), plant_cell.get_left() + DOWN*0.5, buff=0.1, color=BLUE_ACCENT)
        arrow_light = Arrow(light_energy_symbol_obj.get_right(), plant_cell.get_top() + LEFT*0.5, buff=0.1, color=GOLD_ACCENT)

        self.play(Create(arrow_co2), Create(arrow_h2o), Create(arrow_light), run_time=0.8)
        self.play(FadeOut(co2_in), FadeOut(h2o_in), FadeOut(light_energy_symbol_obj),
                  FadeOut(arrow_co2), FadeOut(arrow_h2o), FadeOut(arrow_light),
                  FadeOut(sun, sun_label)) # Sun moves away after providing light

        # Outputs for Photosynthesis
        glucose_out = MathTex(r"\text{C}_6\text{H}_{12}\text{O}_6", color=GREEN_ACCENT).scale(0.8).move_to([1, 1, 0])
        o2_out = MathTex(r"\text{O}_2", color=BLUE_ACCENT).scale(0.8).move_to([1, -1, 0])

        arrow_glucose = Arrow(plant_cell.get_right() + UP*0.5, glucose_out.get_left(), buff=0.1, color=GREEN_ACCENT)
        arrow_o2 = Arrow(plant_cell.get_right() + DOWN*0.5, o2_out.get_left(), buff=0.1, color=BLUE_ACCENT)

        self.play(FadeIn(glucose_out, shift=RIGHT), FadeIn(o2_out, shift=RIGHT), Create(arrow_glucose), Create(arrow_o2), run_time=1)
        self.wait(0.5)

        # Photosynthesis Equation
        equation_photosynthesis = MathTex(
            r"6\text{CO}_2", "+", r"6\text{H}_2\text{O}", "+", r"\text{Light Energy}",
            r"\rightarrow",
            r"\text{C}_6\text{H}_{12}\text{O}_6", "+", r"6\text{O}_2",
            substrings_to_isolate=["CO_2", "H_2O", "Light Energy", "C_6H_{12}O_6", "O_2"]
        ).scale(0.7).to_edge(DOWN)
        equation_photosynthesis.set_color_by_tex("CO_2", RED_ACCENT)
        equation_photosynthesis.set_color_by_tex("H_2O", BLUE_ACCENT)
        equation_photosynthesis.set_color_by_tex("Light Energy", GOLD_ACCENT)
        equation_photosynthesis.set_color_by_tex("C_6H_{12}O_6", GREEN_ACCENT)
        equation_photosynthesis.set_color_by_tex("O_2", BLUE_ACCENT)

        self.play(Write(equation_photosynthesis))
        self.wait(1)

        self.play(
            FadeOut(photosynthesis_title),
            FadeOut(plant_cell), FadeOut(plant_label),
            FadeOut(arrow_glucose), FadeOut(arrow_o2),
            glucose_out.animate.scale(1.2).move_to([-3, 0.5, 0]),
            o2_out.animate.scale(1.2).move_to([-3, -0.5, 0]),
            equation_photosynthesis.animate.shift(UP*1.5).scale(0.8), # Make space for respiration
            run_time=1.5
        )
        self.wait(0.5)

        # --- Beat 3: Cellular Respiration ---
        respiration_title = Text("2. Cellular Respiration", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(respiration_title))

        animal_cell = RoundedRectangle(width=4, height=3, corner_radius=0.5, color=BLUE_ACCENT, fill_opacity=0.2).move_to(RIGHT*2)
        animal_label = Text("Animal Cell / Mitochondria", font_size=24, color=BLUE_ACCENT).next_to(animal_cell, DOWN)
        self.play(FadeIn(animal_cell, shift=RIGHT), FadeIn(animal_label, shift=RIGHT))

        # Inputs for Respiration (use the outputs from photosynthesis)
        # Reposition the existing glucose_out and o2_out for entry
        arrow_glucose_res = Arrow(glucose_out.get_right(), animal_cell.get_left() + UP*0.5, buff=0.1, color=GREEN_ACCENT)
        arrow_o2_res = Arrow(o2_out.get_right(), animal_cell.get_left() + DOWN*0.5, buff=0.1, color=BLUE_ACCENT)

        self.play(Create(arrow_glucose_res), Create(arrow_o2_res),
                  glucose_out.animate.move_to(animal_cell.get_left() + UP*0.5),
                  o2_out.animate.move_to(animal_cell.get_left() + DOWN*0.5),
                  run_time=0.8)
        self.play(FadeOut(glucose_out), FadeOut(o2_out),
                  FadeOut(arrow_glucose_res), FadeOut(arrow_o2_res),
                  run_time=0.5)

        # Outputs for Respiration
        co2_out_res = MathTex(r"\text{CO}_2", color=RED_ACCENT).scale(0.8).move_to([5, 1, 0])
        h2o_out_res = MathTex(r"\text{H}_2\text{O}", color=BLUE_ACCENT).scale(0.8).move_to([5, -1, 0])
        atp_out = MathTex(r"\text{ATP}", color=GOLD_ACCENT).scale(1.2).move_to([5, 2, 0])
        atp_label = Text("Energy Currency", font_size=20, color=GOLD_ACCENT).next_to(atp_out, DOWN)

        arrow_co2_res = Arrow(animal_cell.get_right() + UP*0.5, co2_out_res.get_left(), buff=0.1, color=RED_ACCENT)
        arrow_h2o_res = Arrow(animal_cell.get_right() + DOWN*0.5, h2o_out_res.get_left(), buff=0.1, color=BLUE_ACCENT)
        arrow_atp_res = Arrow(animal_cell.get_top() + RIGHT*0.5, atp_out.get_left(), buff=0.1, color=GOLD_ACCENT)

        self.play(FadeIn(co2_out_res, shift=RIGHT), FadeIn(h2o_out_res, shift=RIGHT),
                  FadeIn(atp_out, shift=RIGHT), FadeIn(atp_label),
                  Create(arrow_co2_res), Create(arrow_h2o_res), Create(arrow_atp_res), run_time=1)
        self.wait(0.5)

        # Respiration Equation
        equation_respiration = MathTex(
            r"\text{C}_6\text{H}_{12}\text{O}_6", "+", r"6\text{O}_2",
            r"\rightarrow",
            r"6\text{CO}_2", "+", r"6\text{H}_2\text{O}", "+", r"\text{ATP (Energy)}",
            substrings_to_isolate=["C_6H_{12}O_6", "O_2", "CO_2", "H_2O", "ATP (Energy)"]
        ).scale(0.7).to_edge(DOWN)
        equation_respiration.set_color_by_tex("C_6H_{12}O_6", GREEN_ACCENT)
        equation_respiration.set_color_by_tex("O_2", BLUE_ACCENT)
        equation_respiration.set_color_by_tex("CO_2", RED_ACCENT)
        equation_respiration.set_color_by_tex("H_2O", BLUE_ACCENT)
        equation_respiration.set_color_by_tex("ATP (Energy)", GOLD_ACCENT)

        self.play(Write(equation_respiration))
        self.wait(1)

        self.play(FadeOut(respiration_title))

        # --- Beat 4: The Cycle / Interconnection ---
        cycle_title = Text("3. The Cycle of Life", font_size=48, color=BLUE_ACCENT).to_edge(UP)
        self.play(FadeIn(cycle_title))

        # Reposition and fade out/in elements for the cycle
        self.play(
            FadeOut(atp_out, atp_label, arrow_atp_res),
            FadeOut(equation_photosynthesis),
            FadeOut(equation_respiration),
            animal_cell.animate.move_to(RIGHT*3.5 + DOWN*1.5), # Reposition animal cell
            animal_label.animate.next_to(animal_cell, DOWN*0.5).set_color(BLUE_ACCENT),
            co2_out_res.animate.move_to(RIGHT*0.5 + UP*0.5).scale(0.7),
            h2o_out_res.animate.move_to(RIGHT*0.5 + DOWN*0.5).scale(0.7),
            FadeOut(arrow_co2_res), FadeOut(arrow_h2o_res),
            run_time=1.5
        )

        # Re-introduce plant cell (simplified)
        plant_cell_cycle = RoundedRectangle(width=3, height=2, corner_radius=0.3, color=GREEN_ACCENT, fill_opacity=0.2).move_to(RIGHT*3.5 + UP*1.5)
        plant_label_cycle = Text("Photosynthesis", font_size=20, color=GREEN_ACCENT).next_to(plant_cell_cycle, DOWN*0.5)
        self.play(FadeIn(plant_cell_cycle, plant_label_cycle))

        # Use existing animal_cell object, just change its label for cycle clarity
        self.play(Transform(animal_label, Text("Respiration", font_size=20, color=BLUE_ACCENT).next_to(animal_cell, DOWN*0.5)))
        
        # Glucose/O2 from Photosynthesis to Respiration (visualized as general "Nutrients" and O2)
        glucose_o2_label = VGroup(
            MathTex(r"\text{Glucose}", color=GREEN_ACCENT),
            MathTex(r"\text{O}_2", color=BLUE_ACCENT)
        ).arrange(DOWN, buff=0.1).scale(0.7).move_to(LEFT*0.5 + UP*0.5)

        arrow_photo_to_resp = CurvedArrow(
            plant_cell_cycle.get_left() + LEFT*0.5,
            animal_cell.get_left() + LEFT*0.5,
            color=GOLD_ACCENT, angle=PI/2
        ).add_tip()

        self.play(FadeIn(glucose_o2_label), Create(arrow_photo_to_resp))

        # CO2/H2O from Respiration to Photosynthesis (use the existing co2_out_res and h2o_out_res)
        co2_h2o_label = VGroup(co2_out_res, h2o_out_res).arrange(DOWN, buff=0.1).scale(1/0.7).scale(0.7) # Adjust scaling
        co2_h2o_label.move_to(LEFT*0.5 + DOWN*0.5)

        arrow_resp_to_photo = CurvedArrow(
            animal_cell.get_left() + LEFT*0.5,
            plant_cell_cycle.get_left() + LEFT*0.5,
            color=GOLD_ACCENT, angle=-PI/2
        ).add_tip()
        
        self.play(Transform(co2_out_res, co2_h2o_label[0]), Transform(h2o_out_res, co2_h2o_label[1]), Create(arrow_resp_to_photo))

        energy_text_cycle = Text("Interconnected Cycle", font_size=32, color=GOLD_ACCENT).move_to(ORIGIN)
        self.play(Write(energy_text_cycle))
        self.wait(1.5)

        self.play(
            FadeOut(cycle_title),
            FadeOut(plant_cell_cycle, plant_label_cycle),
            FadeOut(animal_cell, animal_label), # Fade out the original animal_cell with transformed label
            FadeOut(glucose_o2_label, arrow_photo_to_resp),
            FadeOut(co2_out_res, h2o_out_res, arrow_resp_to_photo), # Use the transformed labels
            FadeOut(energy_text_cycle),
            run_time=1.5
        )

        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Cellular Energy", font_size=60, color=BLUE_ACCENT).to_edge(UP)
        recap_card = Rectangle(width=10, height=6, color=BLUE_ACCENT, fill_opacity=0.1, stroke_width=2)
        
        recap_bullet1 = BulletedList(
            "Photosynthesis: Plants convert light energy into glucose (food).",
            font_size=36, color=GOLD_ACCENT, buff=0.4
        )
        recap_bullet1.set_color_by_tex("Photosynthesis", GREEN_ACCENT)
        recap_bullet1.set_color_by_tex("glucose", GREEN_ACCENT)

        recap_bullet2 = BulletedList(
            "Respiration: Organisms break down glucose to release ATP (energy).",
            font_size=36, color=GOLD_ACCENT, buff=0.4
        )
        recap_bullet2.set_color_by_tex("Respiration", BLUE_ACCENT)
        recap_bullet2.set_color_by_tex("ATP", GOLD_ACCENT)

        recap_bullet3 = BulletedList(
            "These processes form a vital cycle, sustaining life.",
            font_size=36, color=GOLD_ACCENT, buff=0.4
        )

        recap_bullets = VGroup(recap_bullet1, recap_bullet2, recap_bullet3).arrange(DOWN, center=True, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)

        self.play(FadeIn(recap_title))
        self.play(FadeIn(recap_card))
        self.play(
            LaggedStart(
                FadeIn(recap_bullet1, shift=LEFT),
                FadeIn(recap_bullet2, shift=LEFT),
                FadeIn(recap_bullet3, shift=LEFT),
                lag_ratio=0.7
            )
        )
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_card, recap_bullets)))

    def create_light_symbol(self):
        # Creates a simple light symbol like a stylized 'L' or wave
        line1 = Line(LEFT*0.3 + UP*0.3, RIGHT*0.3 + UP*0.3, color=GOLD_ACCENT)
        line2 = Line(LEFT*0.3 + DOWN*0.3, RIGHT*0.3 + DOWN*0.3, color=GOLD_ACCENT)
        wave = FunctionGraph(lambda x: 0.2*np.sin(2*PI*x/0.6), x_range=[-0.3, 0.3], color=GOLD_ACCENT)
        return VGroup(line1, line2, wave)