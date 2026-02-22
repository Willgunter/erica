from manim import *

class EnergyConversionAnimation(Scene):
    def construct(self):
        # 1. Configuration
        config.background_color = BLACK
        title_font_size = 60
        equation_font_size = 35
        text_font_size = 30

        # Define custom colors for accents
        BLUE_ACCENT = BLUE_C # For photosynthesis, inputs
        GOLD_ACCENT = GOLD_C # For outputs
        GREEN_PLANT = GREEN_B # For the plant icon
        RED_ACCENT = RED_B # For the animal icon, and respiration title
        ENERGY_COLOR = YELLOW_A # For light energy and ATP
        ARROW_COLOR = GREY_B # For general flow arrows

        # --- Beat 1: The Energy Source (Visual Hook) ---
        title = Text("Energy Conversion", font_size=title_font_size, color=WHITE).to_edge(UP)
        subtitle = Text("Photosynthesis & Respiration", font_size=title_font_size * 0.7, color=BLUE_ACCENT).next_to(title, DOWN)
        self.play(
            LaggedStart(
                FadeIn(title, shift=UP),
                FadeIn(subtitle, shift=DOWN),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)

        # Visual Hook: Sun -> Plant -> Animal -> Cycle
        sun = Dot(radius=0.8, color=ENERGY_COLOR, fill_opacity=1).move_to([-4, 1, 0])
        sun_rays = VGroup(*[
            Line(sun.get_center(), sun.get_center() + UR.rotate(i*PI/4)*2, color=ENERGY_COLOR, stroke_width=3)
            for i in range(8)
        ])
        sun_group = VGroup(sun, sun_rays)

        # Simple plant: stem and leaves using Manim primitives
        plant_stem = Line(ORIGIN, UP*0.8, color=GREEN_PLANT, stroke_width=4)
        leaf1 = Arc(radius=0.5, start_angle=PI/2, angle=PI/2, color=GREEN_PLANT, stroke_width=4).flip(UP).shift(LEFT*0.3+UP*0.2)
        leaf2 = Arc(radius=0.5, start_angle=PI/2, angle=PI/2, color=GREEN_PLANT, stroke_width=4).shift(RIGHT*0.3+UP*0.2)
        plant_icon = VGroup(plant_stem, leaf1, leaf2).scale(0.8).move_to([-1.5, -0.5, 0])

        # Simple animal (e.g., a blob with legs) using Manim primitives
        animal_body = Ellipse(width=1.5, height=0.8, color=RED_ACCENT, fill_opacity=0.8).shift(UP*0.2)
        leg1 = Line(animal_body.get_left() + DOWN*0.2, animal_body.get_left() + DOWN*0.6, color=RED_ACCENT, stroke_width=3)
        leg2 = Line(animal_body.get_right() + DOWN*0.2, animal_body.get_right() + DOWN*0.6, color=RED_ACCENT, stroke_width=3)
        animal_icon = VGroup(animal_body, leg1, leg2).scale(0.8).move_to([1.5, -0.5, 0])

        energy_flow1_arrow = Arrow(sun_group.get_right(), plant_icon.get_top(), buff=0.1, color=ARROW_COLOR, tip_length=0.2)
        energy_text_1 = Text("Light Energy", font_size=text_font_size*0.7, color=ENERGY_COLOR).next_to(energy_flow1_arrow, UP)
        
        energy_flow2_arrow = Arrow(plant_icon.get_right(), animal_icon.get_left(), buff=0.1, color=ARROW_COLOR, tip_length=0.2)
        energy_text_2 = Text("Chemical Energy", font_size=text_font_size*0.7, color=GOLD_ACCENT).next_to(energy_flow2_arrow, UP)

        self.play(FadeIn(sun_group, scale=0.8))
        self.play(GrowArrow(energy_flow1_arrow), Write(energy_text_1))
        self.play(FadeIn(plant_icon, shift=RIGHT))
        self.play(GrowArrow(energy_flow2_arrow), Write(energy_text_2))
        self.play(FadeIn(animal_icon, shift=LEFT))
        self.wait(1)

        # Clear the initial hook elements, keep title
        self.play(
            FadeOut(sun_group, energy_flow1_arrow, energy_text_1, plant_icon, energy_flow2_arrow, energy_text_2, animal_icon),
            subtitle.animate.next_to(title, DOWN, buff=0.2).set_color(WHITE).set_opacity(0.5) # Fade subtitle a bit
        )
        self.wait(0.5)

        # --- Beat 2: Photosynthesis (Energy Capture) ---
        photosynthesis_title = Text("1. Photosynthesis: Capturing Light Energy", font_size=text_font_size, color=BLUE_ACCENT).to_edge(LEFT).shift(UP*2)
        self.play(Write(photosynthesis_title))

        # Equation for photosynthesis
        co2_ph = MathTex("6", "\\text{CO}_2", color=BLUE_ACCENT, font_size=equation_font_size)
        h2o_ph = MathTex("6", "\\text{H}_2\\text{O}", color=BLUE_ACCENT, font_size=equation_font_size)
        light_energy_term = MathTex("+ \\text{Light Energy}", color=ENERGY_COLOR, font_size=equation_font_size)
        
        plus_ph1 = MathTex("+", font_size=equation_font_size, color=WHITE)
        arrow_ph = MathTex("\\rightarrow", font_size=equation_font_size, color=WHITE)
        plus_ph2 = MathTex("+", font_size=equation_font_size, color=WHITE)

        glucose_ph = MathTex("C_6H_{12}O_6", color=GOLD_ACCENT, font_size=equation_font_size)
        o2_ph = MathTex("6", "\\text{O}_2", color=GOLD_ACCENT, font_size=equation_font_size)

        ph_eq = VGroup(co2_ph, plus_ph1, h2o_ph, light_energy_term, arrow_ph, glucose_ph, plus_ph2, o2_ph).arrange(RIGHT, buff=0.3)
        ph_eq.move_to(ORIGIN).shift(UP*0.5)

        # Labels for inputs/outputs
        inputs_label_ph = Text("Inputs", font_size=text_font_size*0.8, color=BLUE_ACCENT).next_to(VGroup(co2_ph, plus_ph1, h2o_ph, light_energy_term), UP, buff=0.2)
        outputs_label_ph = Text("Outputs", font_size=text_font_size*0.8, color=GOLD_ACCENT).next_to(VGroup(glucose_ph, plus_ph2, o2_ph), UP, buff=0.2)

        self.play(Write(inputs_label_ph), Write(outputs_label_ph))
        
        self.play(FadeIn(co2_ph, shift=LEFT*0.5), FadeIn(plus_ph1), FadeIn(h2o_ph, shift=LEFT*0.5), FadeIn(light_energy_term, shift=LEFT*0.5), run_time=1.5)
        
        # Animate the energy input leading to the arrow
        energy_flash = Circle(radius=0.2, color=ENERGY_COLOR, fill_opacity=1).move_to(light_energy_term.get_center())
        self.play(
            GrowFromCenter(energy_flash),
            energy_flash.animate.scale(5).set_opacity(0),
            GrowArrow(arrow_ph),
            run_time=1
        )
        self.play(FadeIn(glucose_ph, shift=RIGHT*0.5), FadeIn(plus_ph2), FadeIn(o2_ph, shift=RIGHT*0.5), run_time=1.5)
        
        # Flash the glucose and O2 to signify creation
        self.play(
            Indicate(VGroup(glucose_ph, o2_ph), scale_factor=1.2, color=GOLD_ACCENT),
            run_time=0.8
        )
        
        self.wait(1.5)

        # --- Beat 3: Cellular Respiration (Energy Release) ---
        respiration_title = Text("2. Cellular Respiration: Releasing Stored Energy", font_size=text_font_size, color=RED_ACCENT).to_edge(LEFT).shift(UP*2)
        
        # Shift Photosynthesis elements up and fade a bit
        self.play(
            FadeTransform(photosynthesis_title, respiration_title),
            ph_eq.animate.to_edge(UP).shift(UP*0.2).scale(0.7).fade(0.5),
            inputs_label_ph.animate.next_to(ph_eq, DOWN, buff=0.1).scale(0.7).fade(0.5), # Reposition labels
            outputs_label_ph.animate.next_to(ph_eq, DOWN, buff=0.1).scale(0.7).fade(0.5),
            run_time=1
        )
        self.wait(0.5)

        # Equation for respiration
        glucose_res = MathTex("C_6H_{12}O_6", color=BLUE_ACCENT, font_size=equation_font_size)
        o2_res = MathTex("6", "\\text{O}_2", color=BLUE_ACCENT, font_size=equation_font_size)
        
        plus_res1 = MathTex("+", font_size=equation_font_size, color=WHITE)
        arrow_res = MathTex("\\rightarrow", font_size=equation_font_size, color=WHITE)
        plus_res2 = MathTex("+", font_size=equation_font_size, color=WHITE)

        co2_res = MathTex("6", "\\text{CO}_2", color=GOLD_ACCENT, font_size=equation_font_size)
        h2o_res = MathTex("6", "\\text{H}_2\\text{O}", color=GOLD_ACCENT, font_size=equation_font_size)
        atp = MathTex("+ \\text{ATP (Energy)}", color=ENERGY_COLOR, font_size=equation_font_size)

        res_eq = VGroup(glucose_res, plus_res1, o2_res, arrow_res, co2_res, plus_res2, h2o_res, atp).arrange(RIGHT, buff=0.3)
        res_eq.move_to(ORIGIN).shift(DOWN*0.5)

        inputs_label_res = Text("Inputs", font_size=text_font_size*0.8, color=BLUE_ACCENT).next_to(VGroup(glucose_res, plus_res1, o2_res), UP, buff=0.2)
        outputs_label_res = Text("Outputs", font_size=text_font_size*0.8, color=GOLD_ACCENT).next_to(VGroup(co2_res, plus_res2, h2o_res, atp), UP, buff=0.2)

        self.play(Write(inputs_label_res), Write(outputs_label_res))
        self.play(FadeIn(glucose_res, shift=LEFT*0.5), FadeIn(plus_res1), FadeIn(o2_res, shift=LEFT*0.5), run_time=1.5)
        
        # Animate glucose breaking down, leading to the arrow
        self.play(
            FadeOut(glucose_res.copy().scale(1.2).set_opacity(0), shift=RIGHT), # Visual cue for breakdown
            GrowArrow(arrow_res),
            run_time=1
        )
        self.play(FadeIn(co2_res, shift=RIGHT*0.5), FadeIn(plus_res2), FadeIn(h2o_res, shift=RIGHT*0.5), FadeIn(atp, shift=RIGHT*0.5), run_time=1.5)
        
        # Flash ATP
        self.play(
            Indicate(atp, scale_factor=1.2, color=ENERGY_COLOR),
            run_time=0.8
        )
        self.wait(1.5)

        # --- Beat 4: The Cycle (Interdependence) ---
        cycle_title = Text("3. The Energy Cycle: Interdependence", font_size=text_font_size, color=WHITE).to_edge(LEFT).shift(UP*2)

        # Shift respiration elements up, fade, and transform title
        self.play(
            FadeTransform(respiration_title, cycle_title),
            res_eq.animate.to_edge(DOWN).shift(DOWN*0.2).scale(0.7).fade(0.5),
            inputs_label_res.animate.next_to(res_eq, DOWN, buff=0.1).scale(0.7).fade(0.5),
            outputs_label_res.animate.next_to(res_eq, DOWN, buff=0.1).scale(0.7).fade(0.5),
            run_time=1
        )
        
        self.wait(0.5)

        # Simplified boxes for Photosynthesis and Respiration
        ph_box = Rectangle(width=4.5, height=2, color=BLUE_ACCENT, fill_opacity=0.2).move_to(LEFT*3.5)
        ph_text = Text("Photosynthesis", font_size=text_font_size*0.8, color=BLUE_ACCENT).move_to(ph_box.get_center())

        res_box = Rectangle(width=4.5, height=2, color=RED_ACCENT, fill_opacity=0.2).move_to(RIGHT*3.5)
        res_text = Text("Respiration", font_size=text_font_size*0.8, color=RED_ACCENT).move_to(res_box.get_center())

        self.play(Create(ph_box), Write(ph_text))
        self.play(Create(res_box), Write(res_text))

        # CO2 + H2O from Respiration to Photosynthesis
        co2_h2o_label = Text("CO2, H2O", font_size=text_font_size*0.7, color=GOLD_ACCENT).shift(UP*2.5)
        arrow_res_to_ph = CurvedArrow(res_box.get_top()+UP*0.1, ph_box.get_top()+UP*0.1, color=ARROW_COLOR, tip_length=0.2, angle=-PI/2, radius=3)
        co2_h2o_label.next_to(arrow_res_to_ph, UP, buff=0.1)

        # Glucose + O2 from Photosynthesis to Respiration
        glucose_o2_label = Text("Glucose, O2", font_size=text_font_size*0.7, color=GOLD_ACCENT).shift(DOWN*2.5)
        arrow_ph_to_res = CurvedArrow(ph_box.get_bottom()+DOWN*0.1, res_box.get_bottom()+DOWN*0.1, color=ARROW_COLOR, tip_length=0.2, angle=-PI/2, radius=3)
        glucose_o2_label.next_to(arrow_ph_to_res, DOWN, buff=0.1)

        # Light Energy into Photosynthesis
        light_label = Text("Light Energy", font_size=text_font_size*0.7, color=ENERGY_COLOR).move_to(ph_box.get_left() + LEFT*1.5)
        arrow_light_ph = Arrow(light_label.get_right(), ph_box.get_left(), color=ENERGY_COLOR, tip_length=0.2)
        
        # ATP (Energy) out of Respiration
        atp_label = Text("ATP (Energy)", font_size=text_font_size*0.7, color=ENERGY_COLOR).move_to(res_box.get_right() + RIGHT*1.5)
        arrow_atp_res = Arrow(res_box.get_right(), atp_label.get_left(), color=ENERGY_COLOR, tip_length=0.2)

        self.play(
            GrowArrow(arrow_ph_to_res), Write(glucose_o2_label),
            run_time=1.5
        )
        self.play(
            GrowArrow(arrow_res_to_ph), Write(co2_h2o_label),
            run_time=1.5
        )
        self.play(
            GrowArrow(arrow_light_ph), Write(light_label),
            run_time=1
        )
        self.play(
            GrowArrow(arrow_atp_res), Write(atp_label),
            run_time=1
        )
        self.wait(2)

        # --- Recap Card ---
        self.play(
            FadeOut(ph_box, ph_text, res_box, res_text, arrow_res_to_ph, arrow_ph_to_res, arrow_light_ph, arrow_atp_res,
                    glucose_o2_label, co2_h2o_label, light_label, atp_label, cycle_title,
                    ph_eq, res_eq, inputs_label_ph, outputs_label_ph, inputs_label_res, outputs_label_res, subtitle),
            title.animate.center().set_color(WHITE).set_opacity(1) # Bring main title back to full prominence
        )
        self.wait(0.5)

        recap_box = Rectangle(width=10, height=5, color=WHITE, stroke_width=2, fill_opacity=0.1).scale(0.8)
        recap_title = Text("Recap: The Energy Cycle", font_size=title_font_size*0.6, color=BLUE_ACCENT)

        recap_text1 = Text("1. Photosynthesis: Converts Light Energy into Chemical Energy (Glucose).", font_size=text_font_size*0.8, color=WHITE)
        recap_text2 = Text("2. Respiration: Releases Chemical Energy (ATP) from Glucose.", font_size=text_font_size*0.8, color=WHITE)
        recap_text3 = Text("3. These processes form a vital cycle, exchanging CO2, H2O, Glucose & O2.", font_size=text_font_size*0.8, color=WHITE)

        recap_group = VGroup(recap_title, recap_text1, recap_text2, recap_text3).arrange(DOWN, center=True, buff=0.5)
        recap_group.move_to(ORIGIN)
        recap_box.stretch_to_fit_height(recap_group.height + 1).stretch_to_fit_width(recap_group.width + 1).move_to(ORIGIN)
        
        self.play(
            FadeIn(recap_box, scale=0.8),
            Transform(title, recap_title) # Transform main title into recap title
        )
        self.play(
            LaggedStart(
                Write(recap_text1),
                Write(recap_text2),
                Write(recap_text3),
                lag_ratio=0.7
            )
        )
        self.wait(3)
        self.play(
            FadeOut(VGroup(recap_box, title, recap_text1, recap_text2, recap_text3))
        )
        self.wait(0.5)