from manim import *

class CellularEnergyTransformations(Scene):
    def construct(self):
        # --- Configuration ---
        # Dark background (from Nord palette)
        self.camera.background_color = "#2E3440"

        # High-contrast colors (from Nord palette)
        BLUE_ACCENT = "#81A1C1"  # Medium blue
        GOLD_ACCENT = "#EBCB8B"  # Gold
        TEXT_COLOR = "#D8DEE9"   # Light grey
        GREEN_ACCENT = "#A3BE8C" # Green, for plant/photosynthesis
        RED_ACCENT = "#BF616A"   # Red, for respiration/energy release

        # --- Helper Mobjects ---
        def create_sun_icon():
            sun = Circle(radius=0.5, color=GOLD_ACCENT, fill_opacity=1)
            rays = VGroup()
            for i in range(8):
                ray = Line(ORIGIN, OUT * 0.75, stroke_width=3, color=GOLD_ACCENT)
                ray.rotate(i * PI / 4, about_point=ORIGIN)
                rays.add(ray)
            return VGroup(sun, rays).scale(0.8)

        def create_generic_cell():
            cell_body = Circle(radius=1.2, color=BLUE_ACCENT, stroke_width=3)
            nucleus = Circle(radius=0.4, color=BLUE_ACCENT, fill_opacity=0.2).move_to(cell_body.get_center())
            return VGroup(cell_body, nucleus)

        def create_plant_cell():
            # A simplified plant cell with a rectangular wall and chloroplasts
            cell_wall = Rectangle(width=2.5, height=2.5, color=GREEN_ACCENT, stroke_width=3)
            cell_membrane = Rectangle(width=2.2, height=2.2, color=GREEN_ACCENT, fill_opacity=0.1).move_to(cell_wall.get_center())
            chloroplasts = VGroup()
            for _ in range(3): # A few small circles for chloroplasts
                chloroplasts.add(Circle(radius=0.15, color=GREEN_ACCENT, fill_opacity=0.8).move_to(cell_wall.get_center() + random.unit_vector() * random.uniform(0.3, 0.8)))
            return VGroup(cell_wall, cell_membrane, chloroplasts).scale(0.8)

        # --- 1. Visual Hook & Title ---
        title = Text("Cellular Energy Transformations", font_size=55, color=TEXT_COLOR)
        subtitle = Text("The Flow of Life's Power", font_size=30, color=BLUE_ACCENT).next_to(title, DOWN, buff=0.4)
        
        # Abstract energy core and particles for a dynamic opening
        energy_core = Dot(point=ORIGIN, radius=0.3, color=GOLD_ACCENT, fill_opacity=1).set_shadow(color=GOLD_ACCENT, dx=0, dy=0, sigma=0.5, opacity=0.8)
        
        particles = VGroup(*[
            Dot(radius=0.08, color=random.choice([BLUE_ACCENT, GOLD_ACCENT])).move_to(energy_core.get_center() + random.unit_vector() * random.uniform(0.5, 2.5))
            for _ in range(50)
        ])
        
        self.play(
            LaggedStart(
                AnimationGroup(*[
                    particle.animate.move_to(energy_core.get_center() + random.unit_vector() * random.uniform(0.1, 0.4))
                    for particle in particles
                ]),
                energy_core.animate.scale(1.5).set_opacity(0.5),
                lag_ratio=0.02,
                run_time=2
            )
        )
        self.play(
            FadeOut(particles, shift=UP),
            energy_core.animate.scale(0.1).set_opacity(0),
            Write(title, run_time=1.5),
            Write(subtitle, run_time=1)
        )
        self.wait(1)

        # --- 2. Beat 1: Energy is Vital - The Cell ---
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(subtitle, shift=UP),
            run_time=1
        )
        
        cell = create_generic_cell().scale(1.2).to_edge(LEFT, buff=2)
        
        energy_in_label = MathTex("E_{\\text{input}}", color=GOLD_ACCENT).next_to(cell, LEFT, buff=1)
        energy_out_label = MathTex("E_{\\text{output}}", color=BLUE_ACCENT).next_to(cell, RIGHT, buff=1)
        
        arrow_in = Arrow(energy_in_label.get_right(), cell.get_left(), buff=0.1, color=GOLD_ACCENT, stroke_width=6)
        arrow_out = Arrow(cell.get_right(), energy_out_label.get_left(), buff=0.1, color=BLUE_ACCENT, stroke_width=6)
        
        self.play(Create(cell), run_time=1.5)
        self.play(
            LaggedStart(
                Write(energy_in_label), Create(arrow_in),
                Write(energy_out_label), Create(arrow_out),
                lag_ratio=0.05,
                run_time=2
            )
        )

        transform_text = Text("Energy Transformed for Life", font_size=35, color=TEXT_COLOR).next_to(cell, UP, buff=1)
        self.play(Write(transform_text), run_time=1.5)

        atp_label = MathTex("\\text{ATP}", color=RED_ACCENT).next_to(arrow_out, DOWN, buff=0.5)
        atp_arrow = CurvedArrow(arrow_out.get_end(), atp_label.get_top(), color=RED_ACCENT)
        
        self.play(
            FadeTransform(energy_out_label.copy(), atp_label), # 'E_output' conceptually becomes 'ATP'
            GrowArrow(atp_arrow),
            run_time=1.5
        )
        self.wait(1)

        # --- 3. Beat 2: Photosynthesis ---
        self.play(
            FadeOut(energy_in_label, arrow_in, energy_out_label, arrow_out, atp_label, atp_arrow, transform_text, shift=DOWN),
            cell.animate.scale(0.8).to_corner(UL), # Shrink and move cell for continuity
            run_time=1.5
        )
        
        photosynthesis_title = MathTex("\\text{Photosynthesis}", color=GREEN_ACCENT, font_size=50).to_edge(UP)
        plant_cell_icon = create_plant_cell().next_to(photosynthesis_title, DOWN, buff=1.5).shift(RIGHT*2)
        
        sun_icon = create_sun_icon().next_to(plant_cell_icon, LEFT, buff=1.5)
        
        co2_h2o = MathTex("6CO_2 + 6H_2O", color=TEXT_COLOR).next_to(sun_icon, LEFT)
        light_energy = MathTex("\\text{Light Energy}", color=GOLD_ACCENT).next_to(sun_icon, UP)
        
        glucose_o2 = MathTex("C_6H_{12}O_6 + 6O_2", color=TEXT_COLOR).next_to(plant_cell_icon, RIGHT, buff=1)

        arrow_photo = Arrow(co2_h2o.get_right(), plant_cell_icon.get_left(), buff=0.1, color=GREEN_ACCENT)
        arrow_glucose = Arrow(plant_cell_icon.get_right(), glucose_o2.get_left(), buff=0.1, color=GREEN_ACCENT)

        self.play(Write(photosynthesis_title), run_time=1)
        self.play(
            Create(plant_cell_icon), Create(sun_icon),
            Write(light_energy),
            Write(co2_h2o),
            Create(arrow_photo),
            run_time=2
        )
        self.play(
            Write(glucose_o2),
            Create(arrow_glucose),
            run_time=1.5
        )

        # Formal notation for photosynthesis equation
        photosynthesis_eq = MathTex(
            "6CO_2 + 6H_2O", "\\xrightarrow{\\text{Light Energy}}", "C_6H_{12}O_6 + 6O_2",
            color=TEXT_COLOR
        ).scale(0.8).next_to(photosynthesis_title, DOWN, buff=0.5).shift(LEFT*0.5)
        photosynthesis_eq[1][0:14].set_color(GOLD_ACCENT) # Highlight "Light Energy"

        self.play(
            FadeOut(sun_icon, co2_h2o, light_energy, glucose_o2, arrow_photo, arrow_glucose, shift=DOWN),
            plant_cell_icon.animate.shift(LEFT*2.5), # Reposition cell for equation
            Write(photosynthesis_eq),
            run_time=2
        )
        self.wait(1)

        # --- 4. Beat 3: Cellular Respiration ---
        self.play(
            FadeOut(photosynthesis_title, shift=UP),
            photosynthesis_eq.animate.to_edge(UP).scale(0.7), # Shrink and move eq up for next beat
            FadeOut(plant_cell_icon, shift=RIGHT), # Fade out plant cell
            run_time=1.5
        )
        
        respiration_title = MathTex("\\text{Cellular Respiration}", color=RED_ACCENT, font_size=50).to_edge(UP)
        generic_cell_icon = create_generic_cell().next_to(respiration_title, DOWN, buff=1.5).shift(RIGHT*2) # Use generic cell again
        
        glucose_o2_resp = MathTex("C_6H_{12}O_6 + 6O_2", color=TEXT_COLOR).next_to(generic_cell_icon, LEFT, buff=1)
        co2_h2o_atp = MathTex("6CO_2 + 6H_2O + \\text{Energy (ATP)}", color=TEXT_COLOR).next_to(generic_cell_icon, RIGHT, buff=0.5)
        co2_h2o_atp[-1][8:].set_color(RED_ACCENT) # Highlight "ATP"
        
        arrow_resp_in = Arrow(glucose_o2_resp.get_right(), generic_cell_icon.get_left(), buff=0.1, color=RED_ACCENT)
        arrow_resp_out = Arrow(generic_cell_icon.get_right(), co2_h2o_atp.get_left(), buff=0.1, color=RED_ACCENT)

        self.play(Write(respiration_title), run_time=1)
        self.play(
            Create(generic_cell_icon),
            Write(glucose_o2_resp),
            Create(arrow_resp_in),
            run_time=2
        )
        self.play(
            Write(co2_h2o_atp),
            Create(arrow_resp_out),
            run_time=1.5
        )

        # Formal notation for cellular respiration equation
        respiration_eq = MathTex(
            "C_6H_{12}O_6 + 6O_2", "\\rightarrow", "6CO_2 + 6H_2O + \\text{Energy (ATP)}",
            color=TEXT_COLOR
        ).scale(0.8).next_to(respiration_title, DOWN, buff=0.5).shift(LEFT*0.5)
        respiration_eq[2][-1][8:].set_color(RED_ACCENT) # Highlight "ATP"

        self.play(
            FadeOut(generic_cell_icon, glucose_o2_resp, co2_h2o_atp, arrow_resp_in, arrow_resp_out, shift=DOWN),
            respiration_title.animate.shift(LEFT*2), # Reposition title for equation
            Write(respiration_eq),
            run_time=2
        )
        self.wait(1)

        # --- 5. Beat 4: The Cycle & Interconnectedness ---
        self.play(
            FadeOut(respiration_title, shift=UP),
            ReplacementTransform(photosynthesis_eq, photosynthesis_eq.animate.to_edge(UL).scale(0.6)),
            ReplacementTransform(respiration_eq, respiration_eq.animate.to_edge(DR).scale(0.6)),
            run_time=2
        )
        
        # Position the equations for visual flow
        photosynthesis_eq.move_to(UP*2.5 + LEFT*0.5)
        respiration_eq.move_to(DOWN*2.5 + LEFT*0.5)

        cycle_title = Text("A Continuous Transformation Cycle", font_size=40, color=TEXT_COLOR).to_edge(UP)
        self.play(Write(cycle_title), run_time=1.5)

        # Highlighting and connecting components
        # Photosynthesis products -> Respiration reactants (Glucose + Oxygen)
        glu_o2_photo = photosynthesis_eq[2]
        glu_o2_resp = respiration_eq[0]
        
        # Respiration products -> Photosynthesis reactants (CO2 + H2O)
        co2_h2o_resp = respiration_eq[2][0:14] # "6CO_2 + 6H_2O"
        co2_h2o_photo = photosynthesis_eq[0]

        # Use CurvedArrows for the cyclic visual flow
        arrow_photo_to_resp = CurvedArrow(
            glu_o2_photo.get_bottom() + DOWN*0.2, # Start slightly below for better visual
            glu_o2_resp.get_top() + UP*0.2,      # End slightly above
            angle=-TAU/4,
            color=GREEN_ACCENT,
            stroke_width=6
        )
        arrow_resp_to_photo = CurvedArrow(
            co2_h2o_resp.get_top() + UP*0.2,     # Start slightly above
            co2_h2o_photo.get_bottom() + DOWN*0.2, # End slightly below
            angle=TAU/4,
            color=RED_ACCENT,
            stroke_width=6
        )
        
        self.play(
            Flash(glu_o2_photo, color=GREEN_ACCENT),
            run_time=0.5
        )
        self.play(
            Create(arrow_photo_to_resp),
            Flash(glu_o2_resp, color=GREEN_ACCENT),
            run_time=1.5
        )

        self.play(
            Flash(co2_h2o_resp, color=RED_ACCENT),
            run_time=0.5
        )
        self.play(
            Create(arrow_resp_to_photo),
            Flash(co2_h2o_photo, color=RED_ACCENT),
            run_time=1.5
        )
        
        self.wait(1.5)

        # --- 6. Recap Card ---
        self.play(
            FadeOut(photosynthesis_eq, respiration_eq, arrow_photo_to_resp, arrow_resp_to_photo, cycle_title, shift=LEFT),
            run_time=2
        )

        recap_card = Rectangle(
            width=8,
            height=5,
            color=TEXT_COLOR,
            fill_opacity=0.1,
            stroke_width=3
        )

        recap_title = Text("Recap: Cellular Energy Transformations", font_size=40, color=TEXT_COLOR).move_to(recap_card.get_top() + DOWN*0.6)

        bullet1_text = "\\bullet \\text{ Energy is vital, constantly transformed.}"
        bullet2_text = "\\bullet \\text{ Photosynthesis: Light } \\rightarrow \\text{ Chemical Energy (Glucose)}"
        bullet3_text = "\\bullet \\text{ Respiration: Chemical Energy (Glucose) } \\rightarrow \\text{ ATP (Usable Energy)}"

        bullet1 = MathTex(bullet1_text, color=TEXT_COLOR).scale(0.7).next_to(recap_title, DOWN, buff=0.5).align_to(recap_card, LEFT).shift(RIGHT*1)
        bullet2 = MathTex(bullet2_text, color=GREEN_ACCENT).scale(0.7).next_to(bullet1, DOWN, buff=0.05).align_to(recap_card, LEFT).shift(RIGHT*1)
        bullet3 = MathTex(bullet3_text, color=RED_ACCENT).scale(0.7).next_to(bullet2, DOWN, buff=0.05).align_to(recap_card, LEFT).shift(RIGHT*1)
        
        self.play(Create(recap_card), Write(recap_title), run_time=1.5)
        self.play(
            LaggedStart(
                Write(bullet1),
                Write(bullet2),
                Write(bullet3),
                lag_ratio=0.5,
                run_time=3
            )
        )
        
        self.wait(3)