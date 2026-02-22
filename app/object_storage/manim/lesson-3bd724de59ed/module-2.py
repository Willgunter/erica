from manim import *

# Custom Colors (3Blue1Brown inspired)
DARK_BACKGROUND = "#1A1A1A"
ACCENT_BLUE = "#42BFDD"  # A vibrant blue
ACCENT_GOLD = "#FFD700"  # Classic gold
TEXT_COLOR = WHITE

class PhotosynthesisAnimation(Scene):
    def construct(self):
        # 1. Setup - Dark Background
        self.camera.background_color = DARK_BACKGROUND

        # 2. Strong Visual Hook (Opening)
        title = Text("Metabolism Photosynthesis:", font_size=50, color=ACCENT_BLUE).to_edge(UP)
        subtitle = Text("Plants Convert Light to Chemical Energy", font_size=36, color=TEXT_COLOR).next_to(title, DOWN)

        self.play(Write(title), Write(subtitle), run_time=1.5)
        self.wait(0.5)

        # Abstract 'light energy' entering a 'plant cell/chloroplast' reactor
        light_emitter = Circle(radius=0.4, color=ACCENT_GOLD, fill_opacity=1).move_to(LEFT * 4 + UP * 1.5)
        light_rays = VGroup(*[
            Line(light_emitter.get_center(), light_emitter.get_center() + RIGHT.rotate(i * 30 * DEGREES) * 1.5, color=ACCENT_GOLD)
            for i in range(-2, 3) # A few rays pointing right
        ])

        # Simple chloroplast/plant cell representation
        chloroplast_shape = Ellipse(width=3, height=2, color=ACCENT_BLUE, fill_opacity=0.2).move_to(ORIGIN)
        chloroplast_border = chloroplast_shape.copy().set_fill(opacity=0).set_stroke(color=ACCENT_BLUE, width=3)

        self.play(
            FadeIn(light_emitter),
            Create(chloroplast_border),
            FadeIn(chloroplast_shape),
            run_time=1
        )
        self.play(
            LaggedStart(*[
                ray.animate.put_start_and_end_on(ray.get_start(), chloroplast_border.get_center_of_mass())
                for ray in light_rays
            ], lag_ratio=0.1, run_time=1.5),
            FadeOut(light_emitter)
        )
        # Indicate internal activity
        energy_burst = Dot(radius=0.1, color=ACCENT_GOLD).move_to(chloroplast_border.get_center())
        self.play(
            FadeIn(energy_burst, scale=0.1),
            energy_burst.animate.scale(5).set_opacity(0.5).set_color(ACCENT_BLUE),
            run_time=0.8
        )
        self.play(FadeOut(energy_burst, light_rays))
        self.wait(0.5)

        self.play(FadeOut(title, subtitle))

        # Beat 1: Intuition - Light to Chemical Energy
        concept_title_1 = Text("Energy Conversion", font_size=40, color=ACCENT_GOLD).to_edge(UP)
        self.play(Write(concept_title_1))

        light_energy_label = Text("Light Energy", color=ACCENT_GOLD, font_size=30).move_to(LEFT * 4)
        chemical_energy_label = Text("Chemical Energy (Glucose)", color=ACCENT_BLUE, font_size=30).move_to(RIGHT * 4)
        conversion_arrow = Arrow(start=light_energy_label.get_right(), end=chemical_energy_label.get_left(), color=TEXT_COLOR)
        conversion_text = Text("Plants Convert", color=TEXT_COLOR, font_size=24).next_to(conversion_arrow, UP)

        self.play(
            FadeIn(light_energy_label, shift=LEFT),
            FadeIn(chemical_energy_label, shift=RIGHT),
            Create(conversion_arrow),
            Write(conversion_text),
            run_time=2
        )
        self.wait(1)

        # Beat 2: Formal Notation - Inputs (6CO2 + 6H2O)
        self.play(
            FadeOut(light_energy_label, chemical_energy_label, conversion_arrow, conversion_text),
            concept_title_1.animate.set_text("Photosynthesis Inputs").to_edge(UP),
            run_time=1
        )

        equation_inputs = MathTex(
            r"6\text{CO}_2", r" + ", r"6\text{H}_2\text{O}",
            font_size=50, color=TEXT_COLOR
        ).move_to(LEFT * 3)

        co2_icon = Circle(radius=0.2, color=RED, fill_opacity=0.8).next_to(equation_inputs[0], DOWN, buff=0.5)
        co2_text = MathTex(r"\text{Carbon Dioxide}", font_size=24, color=RED).next_to(co2_icon, DOWN, buff=0.2)

        h2o_icon = Dot(radius=0.2, color=BLUE_B, fill_opacity=0.8).next_to(equation_inputs[2], DOWN, buff=0.5)
        h2o_text = MathTex(r"\text{Water}", font_size=24, color=BLUE_B).next_to(h2o_icon, DOWN, buff=0.2)

        self.play(Write(equation_inputs[0]), FadeIn(co2_icon, shift=DOWN), Write(co2_text))
        self.wait(0.5)
        self.play(Write(equation_inputs[1]), Write(equation_inputs[2]), FadeIn(h2o_icon, shift=DOWN), Write(h2o_text))
        self.wait(1)

        # Animate inputs moving into chloroplast
        self.play(
            VGroup(co2_icon, co2_text).animate.move_to(chloroplast_shape.get_left() + LEFT*0.5).set_opacity(0),
            VGroup(h2o_icon, h2o_text).animate.move_to(chloroplast_shape.get_left() + LEFT*0.5).set_opacity(0),
            run_time=1
        )
        self.play(
            Transform(equation_inputs.copy(), chloroplast_shape.get_center(), path_arc=PI/2),
            FadeOut(equation_inputs),
            run_time=0.8
        )
        self.wait(0.5)


        # Beat 3: The Process - Visualizing Transformation
        self.play(
            concept_title_1.animate.set_text("The Photosynthesis Reaction").to_edge(UP),
            chloroplast_border.animate.set_stroke(color=ACCENT_GOLD, width=4), # Highlight processing
            Indicate(chloroplast_shape, scale_factor=1.1, color=ACCENT_GOLD),
            run_time=1
        )
        self.play(chloroplast_border.animate.set_stroke(color=ACCENT_BLUE, width=3)) # Revert highlight
        self.wait(1)

        # Beat 4: Formal Notation - Outputs (Glucose + Oxygen)
        equation_arrow = MathTex(r"\xrightarrow{\text{Light Energy}}", font_size=50, color=TEXT_COLOR).move_to(ORIGIN)
        equation_outputs = MathTex(
            r"\text{C}_6\text{H}_{12}\text{O}_6", r" + ", r"6\text{O}_2",
            font_size=50, color=TEXT_COLOR
        ).move_to(RIGHT * 3)

        glucose_icon = RegularPolygon(n=6, side_length=0.5, color=ACCENT_BLUE, fill_opacity=0.7).next_to(equation_outputs[0], DOWN, buff=0.5)
        glucose_text = MathTex(r"\text{Glucose}", font_size=24, color=ACCENT_BLUE).next_to(glucose_icon, DOWN, buff=0.2)

        oxygen_icon = VGroup(Dot(radius=0.15, color=GREEN_B), Dot(radius=0.15, color=GREEN_B).next_to(Dot(), RIGHT*0.3)).next_to(equation_outputs[2], DOWN, buff=0.5)
        oxygen_text = MathTex(r"\text{Oxygen}", font_size=24, color=GREEN_B).next_to(oxygen_icon, DOWN, buff=0.2)


        # Position the full equation components
        equation_inputs_final = MathTex(r"6\text{CO}_2 + 6\text{H}_2\text{O}", font_size=50, color=TEXT_COLOR).move_to(LEFT * 4)
        equation_full = VGroup(equation_inputs_final, equation_arrow, equation_outputs).arrange(RIGHT, buff=0.75).center()


        self.play(
            ReplacementTransform(VGroup(equation_inputs), equation_inputs_final),
            Create(equation_arrow),
            FadeOut(chloroplast_shape, chloroplast_border), # Fade out the chloroplast now that we are showing the equation
            run_time=1
        )
        self.play(Write(equation_outputs[0]), FadeIn(glucose_icon, shift=DOWN), Write(glucose_text))
        self.wait(0.5)
        self.play(Write(equation_outputs[1]), Write(equation_outputs[2]), FadeIn(oxygen_icon, shift=DOWN), Write(oxygen_text))
        self.wait(1.5)

        self.play(FadeOut(glucose_icon, glucose_text, oxygen_icon, oxygen_text))
        self.wait(1)

        # Beat 5: Full Equation Display
        final_equation_text = MathTex(
            r"6\text{CO}_2 + 6\text{H}_2\text{O} \xrightarrow{\text{Light Energy}} \text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2",
            font_size=48, color=TEXT_COLOR
        ).center()

        self.play(
            ReplacementTransform(VGroup(equation_inputs_final, equation_arrow, equation_outputs), final_equation_text),
            Transform(concept_title_1, Text("The Full Photosynthesis Equation", font_size=40, color=ACCENT_GOLD).to_edge(UP)),
            run_time=1.5
        )
        self.wait(2)


        # Recap Card
        self.play(FadeOut(final_equation_text))
        recap_title = Text("Recap: Photosynthesis - Plants Convert", font_size=48, color=ACCENT_GOLD).to_edge(UP)

        recap_point1 = MathTex(r"\text{1. Converts Light to Chemical Energy}", color=TEXT_COLOR, font_size=36).next_to(recap_title, DOWN, buff=1)
        recap_point2 = MathTex(r"\text{2. Inputs: } 6\text{CO}_2 + 6\text{H}_2\text{O}", color=TEXT_COLOR, font_size=36).next_to(recap_point1, DOWN)
        recap_point3 = MathTex(r"\text{3. Outputs: } \text{C}_6\text{H}_{12}\text{O}_6 \text{ (Glucose)} + 6\text{O}_2", color=TEXT_COLOR, font_size=36).next_to(recap_point2, DOWN)

        recap_group = VGroup(recap_point1, recap_point2, recap_point3).arrange(DOWN, center=True, buff=0.5)

        self.play(
            Transform(concept_title_1, recap_title),
            LaggedStart(*[Write(mob) for mob in recap_group], lag_ratio=0.7),
            run_time=3
        )
        self.wait(4)
        self.play(FadeOut(concept_title_1, recap_group))