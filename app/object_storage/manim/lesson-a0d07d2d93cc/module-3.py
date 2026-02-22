from manim import *

class EnergyCycle(Scene):
    def construct(self):
        # --- Configuration ---
        # Dark theme colors, inspired by 3Blue1Brown
        config.background_color = "#121212"  # Very dark gray/black
        BLUE_ACCENT = "#78BFFF"  # Brighter blue for light/water
        GOLD_ACCENT = "#FFD700"  # Gold for glucose/energy currency
        RED_ACCENT = "#FF6347"   # Tomato red for CO2/oxygen (distinct, not 'waste')
        GREEN_ACCENT = "#66BB6A" # Green for plant/chloroplast
        TEXT_COLOR = WHITE

        self.camera.background_color = config.background_color

        # --- Beat 1: Visual Hook - The Essence of Energy Transformation (Intuition) ---
        
        # Central node representing energy transformation
        core_circle = Circle(radius=0.7, color=GOLD_ACCENT, fill_opacity=0.6).shift(UP*0.5)
        core_pulse = Circle(radius=0.8, color=BLUE_ACCENT).set_opacity(0.3)
        core_group = VGroup(core_circle, core_pulse)

        # Incoming "raw energy" stream (light/basic molecules)
        in_stream_start = UP*3 + LEFT*2
        in_stream_end = core_circle.get_top()
        in_arrow = Arrow(in_stream_start, in_stream_end, color=BLUE_ACCENT, buff=0.1, max_stroke_width_to_length_ratio=0.1).set_opacity(0.8)
        
        # Outgoing "processed energy" stream (glucose/ATP)
        out_stream_start = core_circle.get_bottom()
        out_stream_end = DOWN*2 + RIGHT*2
        out_arrow = Arrow(out_stream_start, out_stream_end, color=GOLD_ACCENT, buff=0.1, max_stroke_width_to_length_ratio=0.1).set_opacity(0.8)

        # Title for the hook
        hook_title = Text("Life's Energy: Capture & Conversion", font_size=40, color=TEXT_COLOR).to_edge(UP)

        self.play(
            FadeIn(hook_title),
            DrawBorderThenFill(core_circle),
            FadeIn(core_pulse),
            run_time=1.5
        )
        self.wait(0.5)

        # Animate particles flowing, transforming color, and flowing out
        num_particles = 10 
        in_dots = VGroup(*[Dot(radius=0.05, color=BLUE_ACCENT).move_to(in_stream_start + LEFT*random.uniform(-0.5, 0.5) + UP*random.uniform(-0.5, 0.5)) for _ in range(num_particles)])
        
        self.play(
            FadeIn(in_dots),
            Create(in_arrow),
            Create(out_arrow),
            run_time=1
        )
        self.play(
            in_dots.animate(run_time=2, rate_func=linear).move_to(core_circle.get_center()),
        )
        self.play(
            in_dots.animate(run_time=1).set_color(GOLD_ACCENT),
        )
        self.play(
            in_dots.animate(run_time=2, rate_func=linear).move_to(out_stream_end),
            FadeOut(in_dots),
        )
        self.wait(0.5)

        # Clean up for next beat
        self.play(
            FadeOut(hook_title, core_group, in_arrow, out_arrow)
        )
        self.wait(0.5)

        # --- Beat 2: Photosynthesis - Capturing Light Energy (Formal Notation & Visual Metaphor) ---
        photosynthesis_title = Text("1. Photosynthesis: Light to Chemical Energy", font_size=36, color=TEXT_COLOR).to_edge(UP)
        
        # Plant "reactor"
        chloroplast_processor = RoundedRectangle(corner_radius=0.3, width=3.5, height=2.5, color=GREEN_ACCENT, fill_opacity=0.2, stroke_width=3).move_to(LEFT*3)
        chloroplast_label = Text("Chloroplast", font_size=24, color=GREEN_ACCENT).next_to(chloroplast_processor, DOWN)
        
        # Inputs to Photosynthesis
        co2_input = MathTex(r"\text{6CO}_2", color=RED_ACCENT).scale(0.8).next_to(chloroplast_processor, LEFT, buff=0.8).shift(UP*0.5)
        h2o_input = MathTex(r"\text{6H}_2\text{O}", color=BLUE_ACCENT).scale(0.8).next_to(chloroplast_processor, LEFT, buff=0.8).shift(DOWN*0.5)
        light_energy_obj = MathTex(r"\text{Light Energy}", color=BLUE_ACCENT).scale(0.7).next_to(chloroplast_processor, UP, buff=0.5)

        # Arrows into chloroplast
        arrow_co2 = Arrow(co2_input.get_right(), chloroplast_processor.get_left(), color=TEXT_COLOR, buff=0.1)
        arrow_h2o = Arrow(h2o_input.get_right(), chloroplast_processor.get_left(), color=TEXT_COLOR, buff=0.1)
        arrow_light = Arrow(light_energy_obj.get_bottom(), chloroplast_processor.get_top(), color=BLUE_ACCENT, buff=0.1)

        # Outputs of Photosynthesis
        glucose_output = MathTex(r"\text{C}_6\text{H}_{12}\text{O}_6", color=GOLD_ACCENT).scale(0.8).next_to(chloroplast_processor, RIGHT, buff=0.8).shift(UP*0.5)
        o2_output = MathTex(r"\text{6O}_2", color=RED_ACCENT).scale(0.8).next_to(chloroplast_processor, RIGHT, buff=0.8).shift(DOWN*0.5)
        
        # Arrows out of chloroplast
        arrow_glucose_o2 = Arrow(chloroplast_processor.get_right(), VGroup(glucose_output, o2_output).get_left(), color=TEXT_COLOR, buff=0.1)

        # Photosynthesis Equation
        equation_photosynthesis = MathTex(
            r"\text{6CO}_2", r" + ", r"\text{6H}_2\text{O}", r" + ", r"\text{Light Energy}", 
            r"\xrightarrow{\text{Chloroplast}}", 
            r"\text{C}_6\text{H}_{12}\text{O}_6", r" + ", r"\text{6O}_2",
            substrings_to_isolate=[r"\text{6CO}_2", r"\text{6H}_2\text{O}", r"\text{Light Energy}", r"\text{C}_6\text{H}_{12}\text{O}_6", r"\text{6O}_2"]
        ).scale(0.6).to_edge(DOWN)

        equation_photosynthesis.set_color_by_tex(r"\text{6CO}_2", RED_ACCENT)
        equation_photosynthesis.set_color_by_tex(r"\text{6H}_2\text{O}", BLUE_ACCENT)
        equation_photosynthesis.set_color_by_tex(r"\text{Light Energy}", BLUE_ACCENT)
        equation_photosynthesis.set_color_by_tex(r"\text{C}_6\text{H}_{12}\text{O}_6", GOLD_ACCENT)
        equation_photosynthesis.set_color_by_tex(r"\text{6O}_2", RED_ACCENT)

        self.play(Write(photosynthesis_title))
        self.play(
            FadeIn(co2_input, shift=LEFT), FadeIn(h2o_input, shift=LEFT),
            Create(arrow_co2), Create(arrow_h2o), run_time=1.5
        )
        self.play(Create(chloroplast_processor), Write(chloroplast_label), run_time=1)
        self.play(FadeIn(light_energy_obj, shift=UP), Create(arrow_light), run_time=1)
        self.play(
            FadeIn(glucose_output, shift=RIGHT), FadeIn(o2_output, shift=RIGHT),
            Create(arrow_glucose_o2), run_time=1.5
        )
        self.wait(0.5)
        self.play(Write(equation_photosynthesis), run_time=2)
        self.wait(1.5)

        # --- Transition to Beat 3 ---
        # Move glucose and oxygen to become inputs for cellular respiration
        self.play(
            FadeOut(photosynthesis_title, co2_input, h2o_input, light_energy_obj, arrow_co2, arrow_h2o, arrow_light, chloroplast_label),
            Transform(chloroplast_processor, chloroplast_processor.copy().set_opacity(0.1)), # Fade chloroplast
            FadeOut(arrow_glucose_o2),
            glucose_output.animate.move_to(LEFT*4 + UP*0.5).scale(1.1),
            o2_output.animate.move_to(LEFT*4 + DOWN*0.5).scale(1.1),
            equation_photosynthesis.animate.shift(UP*0.5).set_opacity(0.3).scale(0.8) # Keep equation faded in background
        )
        self.wait(0.5)

        # --- Beat 3: Cellular Respiration - Releasing Stored Energy (Formal Notation & Visual Metaphor) ---
        cellular_respiration_title = Text("2. Cellular Respiration: Releasing Usable Energy", font_size=36, color=TEXT_COLOR).to_edge(UP)

        # Mitochondria "reactor"
        mitochondria_processor = Ellipse(width=3.5, height=2.5, color=RED_ACCENT, fill_opacity=0.2, stroke_width=3).move_to(RIGHT*3)
        mitochondria_label = Text("Mitochondria", font_size=24, color=RED_ACCENT).next_to(mitochondria_processor, DOWN)
        
        # Inputs to Respiration (from Photosynthesis outputs)
        glucose_respiration_in = glucose_output # Use transformed object
        o2_respiration_in = o2_output # Use transformed object

        # Arrows into mitochondria
        arrow_glucose_in = Arrow(glucose_respiration_in.get_right(), mitochondria_processor.get_left(), color=TEXT_COLOR, buff=0.1).shift(UP*0.5/2)
        arrow_o2_in = Arrow(o2_respiration_in.get_right(), mitochondria_processor.get_left(), color=TEXT_COLOR, buff=0.1).shift(DOWN*0.5/2)
        
        # Outputs of Respiration
        atp_output = MathTex(r"\text{Energy (ATP)}", color=GOLD_ACCENT).scale(0.8).next_to(mitochondria_processor, RIGHT, buff=0.8).shift(UP*1)
        co2_respiration_out = MathTex(r"\text{6CO}_2", color=RED_ACCENT).scale(0.8).next_to(mitochondria_processor, RIGHT, buff=0.8).shift(UP*0)
        h2o_respiration_out = MathTex(r"\text{6H}_2\text{O}", color=BLUE_ACCENT).scale(0.8).next_to(mitochondria_processor, RIGHT, buff=0.8).shift(DOWN*1)

        # Arrows out of mitochondria
        arrow_respiration_outputs = Arrow(mitochondria_processor.get_right(), VGroup(atp_output, co2_respiration_out, h2o_respiration_out).get_left(), color=TEXT_COLOR, buff=0.1)

        # Cellular Respiration Equation
        equation_respiration = MathTex(
            r"\text{C}_6\text{H}_{12}\text{O}_6", r" + ", r"\text{6O}_2", 
            r"\xrightarrow{\text{Mitochondria}}", 
            r"\text{6CO}_2", r" + ", r"\text{6H}_2\text{O}", r" + ", r"\text{Energy (ATP)}",
            substrings_to_isolate=[r"\text{C}_6\text{H}_{12}\text{O}_6", r"\text{6O}_2", r"\text{6CO}_2", r"\text{6H}_2\text{O}", r"\text{Energy (ATP)}"]
        ).scale(0.6).to_edge(DOWN)

        equation_respiration.set_color_by_tex(r"\text{C}_6\text{H}_{12}\text{O}_6", GOLD_ACCENT)
        equation_respiration.set_color_by_tex(r"\text{6O}_2", RED_ACCENT)
        equation_respiration.set_color_by_tex(r"\text{6CO}_2", RED_ACCENT)
        equation_respiration.set_color_by_tex(r"\text{6H}_2\text{O}", BLUE_ACCENT)
        equation_respiration.set_color_by_tex(r"\text{Energy (ATP)}", GOLD_ACCENT)

        self.play(Write(cellular_respiration_title))
        self.play(
            Create(arrow_glucose_in), Create(arrow_o2_in),
            FadeIn(glucose_respiration_in), FadeIn(o2_respiration_in),
            run_time=1.5
        )
        self.play(Create(mitochondria_processor), Write(mitochondria_label), run_time=1)
        self.play(
            FadeIn(atp_output, shift=RIGHT), FadeIn(co2_respiration_out, shift=RIGHT), FadeIn(h2o_respiration_out, shift=RIGHT),
            Create(arrow_respiration_outputs), run_time=1.5
        )
        self.wait(0.5)
        self.play(ReplacementTransform(equation_photosynthesis, equation_respiration), run_time=2)
        self.wait(1.5)

        # --- Beat 4: The Cycle and Interdependence ---
        cycle_title = Text("3. The Interdependent Energy Cycle", font_size=36, color=TEXT_COLOR).to_edge(UP)

        # Repositioning processors for a clearer cycle view
        chloroplast_cycle = chloroplast_processor.copy().move_to(LEFT*3)
        chloroplast_label_cycle = Text("Chloroplast", font_size=24, color=GREEN_ACCENT).next_to(chloroplast_cycle, DOWN)
        mitochondria_cycle = mitochondria_processor.copy().move_to(RIGHT*3)
        mitochondria_label_cycle = Text("Mitochondria", font_size=24, color=RED_ACCENT).next_to(mitochondria_cycle, DOWN)

        # Light Energy input for Photosynthesis
        light_energy_cycle_label = MathTex(r"\text{Light Energy}", color=BLUE_ACCENT).scale(0.7).next_to(chloroplast_cycle, UP, buff=0.5)
        arrow_light_cycle = Arrow(light_energy_cycle_label.get_bottom(), chloroplast_cycle.get_top(), color=BLUE_ACCENT, buff=0.1)

        # ATP output from Respiration (final usable energy)
        atp_cycle_output = atp_output.copy().move_to(RIGHT*6).scale(1.2)
        atp_label = Text("Usable Energy", font_size=24, color=GOLD_ACCENT).next_to(atp_cycle_output, UP)

        self.play(
            FadeOut(cellular_respiration_title, glucose_respiration_in, o2_respiration_in,
                    arrow_glucose_in, arrow_o2_in, arrow_respiration_outputs, mitochondria_label),
            Transform(chloroplast_processor, chloroplast_cycle),
            Transform(mitochondria_processor, mitochondria_cycle),
            Write(chloroplast_label_cycle),
            Write(mitochondria_label_cycle),
            Write(cycle_title)
        )
        self.play(
            FadeIn(light_energy_cycle_label, shift=UP), Create(arrow_light_cycle),
            TransformMatchingTex(atp_output, atp_cycle_output),
            FadeIn(atp_label, shift=UP),
            FadeOut(equation_respiration) # Fade out equation for clarity of cycle
        )
        self.wait(0.5)

        # Cycle paths for CO2/H2O and Glucose/O2
        
        # CO2 & H2O cycle: from Mitochondria to Chloroplast
        co2_h2o_recycled_label = VGroup(
            co2_respiration_out.copy().scale(0.9),
            h2o_respiration_out.copy().scale(0.9)
        ).arrange(DOWN, buff=0.3).move_to(mitochondria_cycle.get_right() + RIGHT*0.5)

        arrow_co2_h2o_path = ArcBetweenPoints(
            mitochondria_cycle.get_right(), chloroplast_cycle.get_right(),
            angle=PI*0.8,  # Arc above
            color=RED_ACCENT, stroke_width=4
        ).add_tip()
        
        self.play(
            ReplacementTransform(co2_respiration_out, co2_h2o_recycled_label[0]),
            ReplacementTransform(h2o_respiration_out, co2_h2o_recycled_label[1]),
            Create(arrow_co2_h2o_path),
            run_time=2
        )
        self.wait(0.5)
        
        # Animate CO2/H2O moving along the path
        co2_h2o_anim = co2_h2o_recycled_label.copy().move_to(arrow_co2_h2o_path.point_from_proportion(0.1))
        self.play(
            MoveAlongPath(co2_h2o_anim, arrow_co2_h2o_path, rate_func=linear),
            FadeOut(co2_h2o_recycled_label),
            run_time=2.5
        )
        self.wait(0.5)

        # Glucose & O2 cycle: from Chloroplast to Mitochondria
        glucose_o2_recycled_label = VGroup(
            MathTex(r"\text{C}_6\text{H}_{12}\text{O}_6", color=GOLD_ACCENT).scale(0.9),
            MathTex(r"\text{6O}_2", color=RED_ACCENT).scale(0.9)
        ).arrange(DOWN, buff=0.3).move_to(chloroplast_cycle.get_left() + LEFT*0.5)

        arrow_glucose_o2_path = ArcBetweenPoints(
            chloroplast_cycle.get_left(), mitochondria_cycle.get_left(),
            angle=-PI*0.8, # Arc below
            color=GOLD_ACCENT, stroke_width=4
        ).add_tip()

        self.play(
            FadeIn(glucose_o2_recycled_label, shift=LEFT),
            Create(arrow_glucose_o2_path),
            run_time=1.5
        )
        
        # Animate Glucose/O2 moving along the path
        glucose_o2_anim = glucose_o2_recycled_label.copy().move_to(arrow_glucose_o2_path.point_from_proportion(0.1))
        self.play(
            MoveAlongPath(glucose_o2_anim, arrow_glucose_o2_path, rate_func=linear),
            FadeOut(glucose_o2_recycled_label),
            run_time=2.5
        )
        self.wait(1)
        
        final_cycle_text = Text("The Cycle Sustains Life", font_size=30, color=TEXT_COLOR).to_edge(DOWN)
        self.play(Write(final_cycle_text))
        self.wait(2)


        # --- Final cleanup for recap ---
        self.play(
            FadeOut(
                cycle_title, chloroplast_cycle, chloroplast_label_cycle, mitochondria_cycle,
                mitochondria_label_cycle, light_energy_cycle_label, arrow_light_cycle,
                atp_cycle_output, atp_label, arrow_co2_h2o_path, arrow_glucose_o2_path,
                co2_h2o_anim, glucose_o2_anim, final_cycle_text
            )
        )
        self.wait(0.5)


        # --- Beat 5: Recap Card ---
        recap_title = Text("Recap: Life's Energy Transformations", font_size=48, color=TEXT_COLOR).to_edge(UP)
        
        line1_text = Tex(r"1. \textbf{Photosynthesis}: \\", r"Light Energy ", r"$\rightarrow$ ", r"Chemical Energy (Glucose)", font_size=36)
        line1_text[1].set_color(BLUE_ACCENT)
        line1_text[3].set_color(GOLD_ACCENT)
        line1_text.next_to(recap_title, DOWN, buff=1)

        line2_text = Tex(r"2. \textbf{Cellular Respiration}: \\", r"Chemical Energy (Glucose) ", r"$\rightarrow$ ", r"Usable Energy (ATP)", font_size=36)
        line2_text[1].set_color(GOLD_ACCENT)
        line2_text[3].set_color(GOLD_ACCENT)
        line2_text.next_to(line1_text, DOWN, buff=0.8)

        final_message = Text("An elegant, continuous energy system.", font_size=30, color=TEXT_COLOR).next_to(line2_text, DOWN, buff=1)
        
        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(FadeIn(line1_text, shift=UP), run_time=1.5)
        self.wait(1.5)
        self.play(FadeIn(line2_text, shift=UP), run_time=1.5)
        self.wait(1.5)
        self.play(Write(final_message), run_time=1.5)
        self.wait(3)