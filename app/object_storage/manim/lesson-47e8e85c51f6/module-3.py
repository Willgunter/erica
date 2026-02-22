from manim import *

class CellularEnergyAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#1a1a1a" # Dark background
        blue_accent = BLUE_C
        gold_accent = GOLD_C
        energy_flow_color = YELLOW
        light_source_color = ORANGE
        plant_color = GREEN_C
        animal_color = RED_C
        text_color = WHITE
        
        # --- Beat 0: Visual Hook - The Essence of Energy (~7s) ---
        title = Text("Cellular Energy: Fueling Life", font_size=0.8, color=gold_accent).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        central_core = Circle(radius=1.5, color=blue_accent, fill_opacity=0.7)
        core_label = Text("Cell", color=text_color, font_size=0.5).next_to(central_core, UP, buff=0.2)
        
        # Energy flowing in (represented by yellow dots)
        energy_in_particles = VGroup(*[
            Dot(point=RIGHT * 5 + UP * random.uniform(-2, 2), radius=0.05, color=energy_flow_color)
            for _ in range(30)
        ])
        in_arrow = Arrow(RIGHT * 4, central_core.get_left(), color=energy_flow_color, buff=0.1)
        in_label = Text("Energy In", color=energy_flow_color, font_size=0.3).next_to(in_arrow, UP, buff=0.1)

        # Energy flowing out (as work/heat, represented by grey dots)
        energy_out_particles = VGroup(*[
            Dot(point=LEFT * 5 + UP * random.uniform(-2, 2), radius=0.05, color=GRAY)
            for _ in range(30)
        ])
        out_arrow = Arrow(central_core.get_right(), LEFT * 4, color=GRAY, buff=0.1)
        out_label = Text("Work / Heat Out", color=GRAY, font_size=0.3).next_to(out_arrow, UP, buff=0.1)

        self.play(
            GrowFromCenter(central_core),
            Write(core_label),
            FadeIn(in_arrow, in_label, shift=LEFT),
            FadeIn(out_arrow, out_label, shift=RIGHT)
        )
        self.play(
            LaggedStart(*[
                particle.animate.shift(LEFT * 5 + DOWN * random.uniform(-0.5, 0.5)).set_opacity(0)
                for particle in energy_in_particles
            ], lag_ratio=0.05, run_time=2),
            LaggedStart(*[
                particle.animate.shift(RIGHT * 5 + UP * random.uniform(-0.5, 0.5)).set_opacity(0)
                for particle in energy_out_particles
            ], lag_ratio=0.05, run_time=2),
            rate_func=linear
        )
        self.wait(0.5)
        
        self.play(FadeOut(energy_in_particles, energy_out_particles, in_arrow, in_label, out_arrow, out_label, core_label, central_core))

        # --- Beat 1: The Cell's Need for Energy (~10s) ---
        title.become(Text("1. Cells Need Energy to Function", font_size=0.7, color=gold_accent).to_edge(UP))
        self.play(Transform(self.mobjects[0], title))
        
        cell_rect = Rectangle(width=4, height=2.5, color=blue_accent, fill_opacity=0.3)
        cell_text = Text("Cell", color=text_color, font_size=0.6).move_to(cell_rect.get_center())

        energy_in = Text("Energy In", color=energy_flow_color, font_size=0.4).next_to(cell_rect, LEFT, buff=0.5)
        energy_in_arrow = Arrow(energy_in.get_right(), cell_rect.get_left(), color=energy_flow_color)

        work_out = Text("Work Out", color=gold_accent, font_size=0.4).next_to(cell_rect, RIGHT, buff=0.5)
        work_out_arrow = Arrow(cell_rect.get_right(), work_out.get_left(), color=gold_accent)

        self.play(Create(cell_rect), Write(cell_text))
        self.play(FadeIn(energy_in, energy_in_arrow, shift=LEFT))
        self.play(FadeIn(work_out, work_out_arrow, shift=RIGHT))
        self.wait(1)

        # Illustrate 'work' - simple transformation
        task_icon = Square(side_length=0.8, color=gold_accent).next_to(work_out_arrow, RIGHT, buff=0.5)
        task_label = Text("Build / Move / Grow", color=text_color, font_size=0.3).next_to(task_icon, DOWN)
        self.play(GrowFromCenter(task_icon), Write(task_label))
        self.play(
            task_icon.animate.shift(UP * 0.5 + RIGHT * 0.5).scale(0.8),
            run_time=0.8
        )
        self.play(
            task_icon.animate.shift(DOWN * 1 + LEFT * 1).set_color(blue_accent),
            run_time=0.8
        )
        self.wait(1)
        
        all_beat1_mobs = VGroup(cell_rect, cell_text, energy_in, energy_in_arrow, work_out, work_out_arrow, task_icon, task_label)
        self.play(FadeOut(all_beat1_mobs))

        # --- Beat 2: Photosynthesis - The Energy Input (~12s) ---
        title.become(Text("2. Photosynthesis: Capturing Light Energy", font_size=0.7, color=gold_accent).to_edge(UP))
        self.play(Transform(self.mobjects[0], title))
        
        plant_box = Rectangle(width=3.5, height=2.5, color=plant_color, fill_opacity=0.3).to_edge(LEFT, buff=1)
        plant_label = Text("Plant Cell", color=text_color, font_size=0.4).next_to(plant_box, DOWN)

        # Inputs
        light_source = Circle(radius=0.5, color=light_source_color, fill_opacity=0.8).next_to(plant_box, UP, buff=0.5)
        light_rays = VGroup(*[Line(light_source.get_bottom(), plant_box.get_top() + DOWN*0.1, color=light_source_color, stroke_width=3).rotate(i * 10 * DEGREES, about_point=light_source.get_center()) for i in range(-2, 3)])
        light_text = Text("Light Energy", color=light_source_color, font_size=0.3).next_to(light_source, UP)

        co2_in = MathTex(r"\text{CO}_2", color=blue_accent).scale(0.8).next_to(plant_box, LEFT, buff=0.8).shift(UP*0.5)
        h2o_in = MathTex(r"\text{H}_2\text{O}", color=blue_accent).scale(0.8).next_to(plant_box, LEFT, buff=0.8).shift(DOWN*0.5)

        arrow_co2_in = Arrow(co2_in.get_right(), plant_box.get_left(), color=blue_accent, buff=0.1)
        arrow_h2o_in = Arrow(h2o_in.get_right(), plant_box.get_left(), color=blue_accent, buff=0.1)

        self.play(Create(plant_box), Write(plant_label))
        self.play(FadeIn(light_source, light_rays, light_text, shift=UP))
        self.play(FadeIn(co2_in, arrow_co2_in, shift=LEFT), FadeIn(h2o_in, arrow_h2o_in, shift=LEFT))
        self.wait(0.5)

        # Outputs
        glucose_out = MathTex(r"\text{C}_6\text{H}_{12}\text{O}_6", r"\text{(Glucose)}", color=gold_accent).scale(0.8).next_to(plant_box, RIGHT, buff=0.8).shift(UP*0.5)
        o2_out = MathTex(r"\text{O}_2", r"\text{(Oxygen)}", color=blue_accent).scale(0.8).next_to(plant_box, RIGHT, buff=0.8).shift(DOWN*0.5)
        
        arrow_glucose_out = Arrow(plant_box.get_right(), glucose_out.get_left(), color=gold_accent, buff=0.1)
        arrow_o2_out = Arrow(plant_box.get_right(), o2_out.get_left(), color=blue_accent, buff=0.1)

        self.play(
            Create(arrow_glucose_out), Write(glucose_out),
            Create(arrow_o2_out), Write(o2_out),
            run_time=2
        )
        self.wait(1.5)

        # Keep glucose and oxygen for next beat, fade out others
        # Prepare glucose_formula and oxygen_formula for next beat's use
        self.glucose_formula = glucose_out.copy().to_corner(UL).scale(0.7)
        self.oxygen_formula = o2_out.copy().to_corner(DL).scale(0.7)

        self.play(
            FadeOut(plant_box, plant_label, light_source, light_rays, light_text,
                    co2_in, arrow_co2_in, h2o_in, arrow_h2o_in),
            Transform(glucose_out, self.glucose_formula),
            Transform(o2_out, self.oxygen_formula)
        )
        self.wait(0.5)

        # --- Beat 3: Cellular Respiration - Releasing Stored Energy (~15s) ---
        title.become(Text("3. Respiration: Releasing Stored Energy", font_size=0.7, color=gold_accent).to_edge(UP))
        self.play(Transform(self.mobjects[0], title))

        all_cells_box = Rectangle(width=3.5, height=2.5, color=animal_color, fill_opacity=0.3).move_to(ORIGIN)
        all_cells_label = Text("All Cells (Mitochondria)", color=text_color, font_size=0.4).next_to(all_cells_box, DOWN)

        # Inputs (from photosynthesis outputs)
        glucose_input = self.glucose_formula.copy().move_to(LEFT * 4 + UP)
        oxygen_input = self.oxygen_formula.copy().move_to(LEFT * 4 + DOWN)
        
        arrow_glucose_in_resp = Arrow(glucose_input.get_right(), all_cells_box.get_left(), color=gold_accent, buff=0.1)
        arrow_oxygen_in_resp = Arrow(oxygen_input.get_right(), all_cells_box.get_left(), color=blue_accent, buff=0.1)

        self.play(
            Create(all_cells_box), Write(all_cells_label),
            ReplacementTransform(self.glucose_formula, glucose_input),
            ReplacementTransform(self.oxygen_formula, oxygen_input),
            Create(arrow_glucose_in_resp), Create(arrow_oxygen_in_resp)
        )
        self.wait(1)

        # Outputs
        atp_out = Text("ATP (Energy)", color=energy_flow_color, font_size=0.5).next_to(all_cells_box, RIGHT, buff=0.8).shift(UP*0.8)
        co2_out_resp = MathTex(r"\text{CO}_2", color=blue_accent).scale(0.8).next_to(all_cells_box, RIGHT, buff=0.8).shift(DOWN*0.1)
        h2o_out_resp = MathTex(r"\text{H}_2\text{O}", color=blue_accent).scale(0.8).next_to(all_cells_box, RIGHT, buff=0.8).shift(DOWN*0.8)

        arrow_atp_out = Arrow(all_cells_box.get_right(), atp_out.get_left(), color=energy_flow_color, buff=0.1)
        arrow_co2_out_resp = Arrow(all_cells_box.get_right(), co2_out_resp.get_left(), color=blue_accent, buff=0.1)
        arrow_h2o_out_resp = Arrow(all_cells_box.get_right(), h2o_out_resp.get_left(), color=blue_accent, buff=0.1)

        self.play(
            Create(arrow_atp_out), Write(atp_out),
            Create(arrow_co2_out_resp), Write(co2_out_resp),
            Create(arrow_h2o_out_resp), Write(h2o_out_resp),
            run_time=2
        )
        self.wait(1.5)

        # Link back to Photosynthesis (cycle) - placeholders for visual continuity
        photosyn_inputs_label = Text("Photosynthesis\n(Inputs)", color=plant_color, font_size=0.3).move_to(LEFT * 5 + UP * 2.5)
        photosyn_co2_target = MathTex(r"\text{CO}_2", color=blue_accent).scale(0.6).move_to(LEFT * 5 + UP * 1.5)
        photosyn_h2o_target = MathTex(r"\text{H}_2\text{O}", color=blue_accent).scale(0.6).move_to(LEFT * 5 + DOWN * 1.5)
        
        arrow_co2_cycle = CurvedArrow(co2_out_resp.get_bottom(), photosyn_co2_target.get_top(), color=blue_accent, angle=-TAU/4)
        arrow_h2o_cycle = CurvedArrow(h2o_out_resp.get_bottom(), photosyn_h2o_target.get_top(), color=blue_accent, angle=-TAU/4)
        
        self.play(
            Write(photosyn_inputs_label),
            FadeIn(photosyn_co2_target), FadeIn(photosyn_h2o_target),
            Create(arrow_co2_cycle),
            Create(arrow_h2o_cycle)
        )
        self.wait(1.5)
        
        all_beat3_mobs = VGroup(all_cells_box, all_cells_label, glucose_input, oxygen_input,
                                arrow_glucose_in_resp, arrow_oxygen_in_resp,
                                co2_out_resp, h2o_out_resp, arrow_co2_out_resp, arrow_h2o_out_resp,
                                photosyn_inputs_label, photosyn_co2_target, photosyn_h2o_target,
                                arrow_co2_cycle, arrow_h2o_cycle)
        self.play(FadeOut(all_beat3_mobs))
        
        # Keep ATP for next beat
        self.atp_energy_text = atp_out.copy().to_corner(UL).scale(0.8)
        self.play(Transform(atp_out, self.atp_energy_text))

        # --- Beat 4: ATP - The Energy Currency (~12s) ---
        title.become(Text("4. ATP: The Cell's Energy Currency", font_size=0.7, color=gold_accent).to_edge(UP))
        self.play(Transform(self.mobjects[0], title))

        adp_label = MathTex(r"\text{ADP}", color=blue_accent).scale(1.2).shift(LEFT * 3 + UP * 0.5)
        p_label = MathTex(r"\text{P}_i", color=blue_accent).scale(1.2).next_to(adp_label, RIGHT, buff=0.8)
        energy_label_in = Text("+ Energy", color=energy_flow_color, font_size=0.4).next_to(p_label, RIGHT, buff=0.8)
        
        # ATP synthesis
        atp_synthesis_group = VGroup(adp_label, p_label, energy_label_in)
        arrow_synthesis = Arrow(atp_synthesis_group.get_right(), RIGHT * 1.5, color=text_color)

        atp_molecule = MathTex(r"\text{ATP}", color=gold_accent).scale(1.8).move_to(RIGHT * 3)
        
        self.play(Write(adp_label), Write(p_label), Write(energy_label_in))
        self.play(
            Create(arrow_synthesis),
            TransformMatchingTex(VGroup(adp_label, p_label, energy_label_in), atp_molecule, path_arc=PI/2),
            run_time=2
        )
        self.wait(1)

        # ATP breakdown
        energy_release_label = Text("Energy for Work", color=energy_flow_color, font_size=0.4).move_to(DOWN*2)
        arrow_breakdown = Arrow(atp_molecule.get_bottom(), energy_release_label.get_top(), color=energy_flow_color, buff=0.2)
        
        burst_of_energy = VGroup(*[
            Dot(atp_molecule.get_center(), radius=0.08, color=energy_flow_color)
            for _ in range(20)
        ])
        
        adp_recreated = MathTex(r"\text{ADP}", color=blue_accent).scale(1.2).shift(LEFT * 3 + DOWN * 0.5)
        p_recreated = MathTex(r"\text{P}_i", color=blue_accent).scale(1.2).next_to(adp_recreated, RIGHT, buff=0.8)

        self.play(
            FadeOut(arrow_synthesis),
            atp_molecule.animate.shift(UP*1), # Shift ATP up to make room for breakdown
            FadeIn(energy_release_label, arrow_breakdown),
            LaggedStart(*[
                dot.animate.shift(random_vector(0.5, 1.5))
                for dot in burst_of_energy
            ], lag_ratio=0.05, run_time=1.5),
            FadeIn(adp_recreated, p_recreated),
            FadeOut(burst_of_energy)
        )
        self.wait(1.5)

        all_beat4_mobs = VGroup(adp_label, p_label, energy_label_in,
                                atp_molecule, energy_release_label, arrow_breakdown,
                                adp_recreated, p_recreated, self.atp_energy_text)
        self.play(FadeOut(all_beat4_mobs))
        self.wait(0.5)

        # --- Beat 5: Recap Card (~7s) ---
        title.become(Text("Recap: Cellular Energy", font_size=0.7, color=gold_accent).to_edge(UP))
        self.play(Transform(self.mobjects[0], title))

        recap_card = Rectangle(width=7, height=4, color=blue_accent, fill_opacity=0.2, corner_radius=0.3)
        
        recap_text1 = MathTex(r"\text{1. Photosynthesis: }", r"\text{Light} \to \text{Glucose (Plants)}", color=text_color).scale(0.7).move_to(UP*1.5)
        recap_text2 = MathTex(r"\text{2. Cellular Respiration: }", r"\text{Glucose} \to \text{ATP (All Cells)}", color=text_color).scale(0.7).next_to(recap_text1, DOWN, buff=0.5)
        recap_text3 = MathTex(r"\text{3. ATP: }", r"\text{The Energy Currency}", color=text_color).scale(0.7).next_to(recap_text2, DOWN, buff=0.5)
        
        recap_group = VGroup(recap_card, recap_text1, recap_text2, recap_text3).center()

        self.play(FadeIn(recap_card, scale=0.8))
        self.play(Write(recap_text1[0]), Write(recap_text1[1], run_time=1.5))
        self.play(Write(recap_text2[0]), Write(recap_text2[1], run_time=1.5))
        self.play(Write(recap_text3[0]), Write(recap_text3[1], run_time=1.5))
        self.wait(2)
        
        self.play(FadeOut(recap_group, title))
        self.wait(1)