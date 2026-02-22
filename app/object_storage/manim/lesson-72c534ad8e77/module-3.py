from manim import *

# Define custom colors for 3Blue1Brown-inspired style
BLUE_ACCENT = ManimColor("#83B4FF")  # A vibrant blue
GOLD_ACCENT = ManimColor("#FFD700")  # Classic gold
GREEN_PLANT = ManimColor("#5CB85C") # Green for plant elements
RED_CELL = ManimColor("#D9534F")    # Red for cell/mitochondria elements
BACKGROUND_DARK = ManimColor("#1A1A1A") # Slightly off-black for depth

class BiologicalEnergyTransformations(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_DARK

        # --- Visual Hook (Beat 0) ---
        title = Text("Biological Energy Transformations", font_size=50, color=BLUE_ACCENT, weight=BOLD)
        self.play(Write(title))
        self.wait(0.5)

        # Abstract energy representation
        energy_orb = Dot(point=ORIGIN, radius=0.3, color=GOLD_ACCENT, z_index=2, fill_opacity=1)
        energy_waves = VGroup(*[
            Circle(radius=r, stroke_width=4, color=GOLD_ACCENT).set_opacity(1-r/3)
            for r in np.linspace(0.5, 2.5, 5)
        ])
        
        self.play(
            FadeOut(title.copy().scale(1.5), scale=0.5), # Fade out a larger copy to hint at transformation
            Transform(title, Text("Energy In Motion", font_size=40, color=WHITE).to_edge(UP)),
            FadeIn(energy_orb)
        )
        self.play(
            AnimationGroup(
                energy_orb.animate.scale(1.2).set_opacity(0.8),
                LaggedStart(*[FadeIn(wave, scale=0.5) for wave in energy_waves], lag_ratio=0.1),
                run_time=1.5
            )
        )
        self.play(
            FadeOut(energy_orb), 
            FadeOut(energy_waves),
            title.animate.to_edge(UP, buff=0.7).scale(0.8)
        )
        self.wait(0.5)

        # --- Beat 1: Core Idea - Energy Transformation ---
        beat_title_1 = Text("Organisms constantly transform energy", font_size=36, color=WHITE).next_to(title, DOWN, buff=0.5)
        self.play(Write(beat_title_1))

        # Abstract shapes representing energy states
        input_energy_shape = Polygon(
            [-1, 1, 0], [1, 1, 0], [1.5, 0, 0], [1, -1, 0], [-1, -1, 0], [-1.5, 0, 0],
            color=GOLD_ACCENT, fill_opacity=0.8
        ).scale(0.8).move_to(LEFT * 3) # Jagged shape for input energy (e.g., light)
        
        output_energy_shape = Circle(radius=0.7, color=BLUE_ACCENT, fill_opacity=0.8).move_to(RIGHT * 3) # Smooth shape for output (e.g., chemical/usable)
        
        transform_arrow = Arrow(input_energy_shape.get_right(), output_energy_shape.get_left(), buff=0.3, color=WHITE)
        
        label_in = Text("Input Form", color=GOLD_ACCENT, font_size=28).next_to(input_energy_shape, DOWN, buff=0.3)
        label_out = Text("Output Form", color=BLUE_ACCENT, font_size=28).next_to(output_energy_shape, DOWN, buff=0.3)

        self.play(FadeIn(input_energy_shape), FadeIn(output_energy_shape), Create(transform_arrow), FadeIn(label_in), FadeIn(label_out))
        self.wait(1.5)

        # Transition to Photosynthesis
        self.play(FadeOut(input_energy_shape), FadeOut(output_energy_shape), FadeOut(transform_arrow), FadeOut(label_in), FadeOut(label_out))


        # --- Beat 2: Photosynthesis - Capturing Light Energy ---
        photosynthesis_title = Text("Photosynthesis: Light → Chemical Energy", font_size=40, color=GOLD_ACCENT).next_to(title, DOWN, buff=0.5)
        self.play(Transform(beat_title_1, photosynthesis_title))

        # Sun icon
        sun_core = Circle(radius=0.7, color=GOLD_ACCENT, fill_opacity=1).move_to(LEFT * 4 + UP * 0.5)
        sun_rays = VGroup(*[
            Line(sun_core.get_center(), sun_core.get_center() + 1.1 * complex_to_R3(np.exp(1j * angle)), color=GOLD_ACCENT)
            for angle in np.linspace(0, 2*PI, 12, endpoint=False)
        ]).set_stroke(width=3)
        sun_icon = VGroup(sun_core, sun_rays)
        self.play(Create(sun_icon))

        # Plant icon (simplified)
        plant_base = Rectangle(width=0.3, height=1.5, color=GREEN_PLANT, fill_opacity=1).next_to(sun_icon, RIGHT, buff=1.5)
        plant_leaves = VGroup(
            Ellipse(width=1.2, height=0.6, color=GREEN_PLANT, fill_opacity=0.8).rotate(PI/6).next_to(plant_base.get_top(), UP*0.2 + LEFT*0.3),
            Ellipse(width=1.2, height=0.6, color=GREEN_PLANT, fill_opacity=0.8).rotate(-PI/6).next_to(plant_base.get_top(), UP*0.2 + RIGHT*0.3)
        )
        plant_icon = VGroup(plant_base, plant_leaves).move_to(LEFT * 0.5)
        self.play(Create(plant_icon))

        # Light energy arrow
        light_arrow = Arrow(sun_icon.get_right(), plant_icon.get_left(), buff=0.3, color=WHITE)
        light_label = Text("Light Energy", color=GOLD_ACCENT, font_size=28).next_to(light_arrow, UP)
        self.play(GrowArrow(light_arrow), Write(light_label))

        # Reactants (CO2, H2O) and Products (Glucose, O2)
        co2_h2o_in = MathTex("CO_2", "+", "H_2O", font_size=38, color=WHITE).next_to(plant_icon, LEFT, buff=0.8)
        self.play(Write(co2_h2o_in))

        glucose_formula = MathTex("C_6H_{12}O_6", font_size=38, color=BLUE_ACCENT)
        o2_formula = MathTex("O_2", font_size=38, color=WHITE)
        
        # Represent glucose with a hexagon
        glucose_mol = RegularPolygon(n=6, color=BLUE_ACCENT, fill_opacity=0.8, stroke_color=BLUE_ACCENT).scale(0.5)
        glucose_label = VGroup(glucose_mol, glucose_formula.copy().scale(0.7).next_to(glucose_mol, RIGHT, buff=0.1))

        products_group = VGroup(glucose_label, o2_formula).arrange(DOWN, buff=0.8).next_to(plant_icon, RIGHT, buff=0.8)
        
        chemical_energy_label = Text("Chemical Energy", color=BLUE_ACCENT, font_size=28).next_to(products_group, DOWN, buff=0.3)
        
        self.play(
            FadeTransform(co2_h2o_in, co2_h2o_in.copy().scale(0.8).shift(UP*0.5+LEFT*0.5)), # Simulate input
            FadeIn(products_group, shift=RIGHT),
            Write(chemical_energy_label)
        )
        self.wait(1.5)


        # --- Beat 3: Cellular Respiration - Releasing Stored Energy ---
        cellular_respiration_title = Text("Cellular Respiration: Chemical → Usable Energy", font_size=40, color=BLUE_ACCENT).next_to(title, DOWN, buff=0.5)
        self.play(Transform(beat_title_1, cellular_respiration_title))

        self.play(FadeOut(sun_icon), FadeOut(light_arrow), FadeOut(light_label))
        self.play(plant_icon.animate.move_to(LEFT * 4)) # Move plant away for now

        # Cell/Mitochondria icon
        cell_body = Circle(radius=1.2, color=BACKGROUND_DARK, fill_opacity=0.7, stroke_color=WHITE, stroke_width=2).move_to(RIGHT * 3.5)
        mitochondria = Ellipse(width=1.5, height=0.8, color=RED_CELL, fill_opacity=0.8, stroke_color=RED_CELL).move_to(cell_body.get_center())
        mitochondria_inner = VGroup(
            Line(mitochondria.get_left() + UP*0.2, mitochondria.get_center() + LEFT*0.2 + UP*0.1),
            Line(mitochondria.get_left() + DOWN*0.2, mitochondria.get_center() + LEFT*0.2 + DOWN*0.1),
            Line(mitochondria.get_center() + UP*0.2, mitochondria.get_right() + UP*0.1),
            Line(mitochondria.get_center() + DOWN*0.2, mitochondria.get_right() + DOWN*0.1)
        ).set_stroke(color=DARK_GRAY, width=2)
        cell_icon = VGroup(cell_body, mitochondria, mitochondria_inner)
        self.play(Create(cell_icon))

        # Animate glucose and oxygen moving into the cell
        # Retain original objects for continuity, move their copies
        glucose_to_cell = glucose_label.copy().move_to(plant_icon.get_right()).scale(1.2)
        o2_to_cell = o2_formula.copy().move_to(plant_icon.get_right() + DOWN*0.5).scale(1.2)
        
        # Fade out previous labels and items that aren't moving
        self.play(
            FadeOut(co2_h2o_in),
            FadeOut(products_group),
            FadeOut(chemical_energy_label),
            FadeOut(plant_icon)
        )

        glucose_o2_label_in = Text("Glucose + O₂", color=WHITE, font_size=28).next_to(cell_icon, LEFT, buff=0.8)
        self.play(Write(glucose_o2_label_in))
        
        # Products of respiration (CO2, H2O, ATP)
        co2_h2o_out = MathTex("CO_2", "+", "H_2O", font_size=38, color=WHITE).next_to(cell_icon, RIGHT, buff=0.8)
        self.play(Write(co2_h2o_out))

        # ATP energy release (dots with glow effect)
        atp_label = Text("Usable Energy (ATP)", color=BLUE_ACCENT, font_size=28).next_to(cell_icon, DOWN, buff=0.5)
        atp_dots = VGroup(*[
            Dot(point=cell_icon.get_center(), radius=0.1, color=BLUE_ACCENT, fill_opacity=0.8).set_shadow(radius=0.2, color=BLUE_ACCENT)
            for _ in range(7)
        ])
        
        self.play(FadeIn(atp_label, shift=DOWN))
        self.play(
            LaggedStart(
                *[dot.animate.shift(np.random.rand(3)*3 - 1.5).set_opacity(0) for dot in atp_dots],
                lag_ratio=0.1, run_time=2,
            )
        )
        self.wait(1.5)


        # --- Beat 4: The Continuous Cycle ---
        cycle_title = Text("A Continuous Cycle", font_size=40, color=GOLD_ACCENT).next_to(title, DOWN, buff=0.5)
        self.play(Transform(beat_title_1, cycle_title))

        # Clear elements
        self.play(
            FadeOut(glucose_o2_label_in),
            FadeOut(co2_h2o_out),
            FadeOut(atp_label),
            FadeOut(atp_dots),
        )

        # Re-introduce simplified plant and cell icons
        plant_cycle_icon = VGroup(
            Rectangle(width=0.25, height=1.5, color=GREEN_PLANT, fill_opacity=1),
            Ellipse(width=1.5, height=0.7, color=GREEN_PLANT, fill_opacity=0.8).next_to(ORIGIN, UP*0.5)
        ).scale(0.7).move_to(LEFT * 3)
        plant_label_cycle = Text("Photosynthesis", font_size=28, color=GREEN_PLANT).next_to(plant_cycle_icon, DOWN, buff=0.3)

        cell_cycle_icon = VGroup(
            Circle(radius=1.0, color=BACKGROUND_DARK, fill_opacity=0.7, stroke_color=WHITE),
            Ellipse(width=1.0, height=0.6, color=RED_CELL, fill_opacity=0.8)
        ).scale(0.7).move_to(RIGHT * 3)
        cell_label_cycle = Text("Respiration", font_size=28, color=RED_CELL).next_to(cell_cycle_icon, DOWN, buff=0.3)

        self.play(
            FadeIn(plant_cycle_icon), FadeIn(plant_label_cycle),
            ReplacementTransform(cell_icon, cell_cycle_icon), # Transform existing cell icon
            FadeIn(cell_label_cycle)
        )

        # Draw cycle arrows and labels
        # From Plant (Glucose + O2) to Cell
        arrow_plant_to_cell = ArcBetweenPoints(
            plant_cycle_icon.get_right() + UP*0.5,
            cell_cycle_icon.get_left() + UP*0.5,
            angle=-PI/3, # Bend downwards
            stroke_color=BLUE_ACCENT,
            stroke_width=5
        ).add_tip(tip_length=0.2)
        label_plant_to_cell = Text("Glucose + O₂", font_size=28, color=BLUE_ACCENT).next_to(arrow_plant_to_cell, UP, buff=0.2)
        
        # From Cell (CO2 + H2O) to Plant
        arrow_cell_to_plant = ArcBetweenPoints(
            cell_cycle_icon.get_left() + DOWN*0.5,
            plant_cycle_icon.get_right() + DOWN*0.5,
            angle=-PI/3, # Bend downwards
            stroke_color=GOLD_ACCENT,
            stroke_width=5
        ).add_tip(tip_length=0.2)
        label_cell_to_plant = Text("CO₂ + H₂O", font_size=28, color=GOLD_ACCENT).next_to(arrow_cell_to_plant, DOWN, buff=0.2)

        self.play(
            Create(arrow_plant_to_cell), Write(label_plant_to_cell),
            Create(arrow_cell_to_plant), Write(label_cell_to_plant)
        )
        
        # Add labels for energy input/output
        light_energy_flow_label = Text("Light Energy", font_size=24, color=GOLD_ACCENT).next_to(plant_cycle_icon, UP, buff=0.3)
        atp_energy_flow_label = Text("Usable Energy (ATP)", font_size=24, color=BLUE_ACCENT).next_to(cell_cycle_icon, UP, buff=0.3)
        self.play(FadeIn(light_energy_flow_label, shift=UP), FadeIn(atp_energy_flow_label, shift=UP))
        
        self.wait(2)


        # --- Recap Card ---
        self.play(
            FadeOut(plant_cycle_icon), FadeOut(plant_label_cycle),
            FadeOut(cell_cycle_icon), FadeOut(cell_label_cycle),
            FadeOut(arrow_plant_to_cell), FadeOut(label_plant_to_cell),
            FadeOut(arrow_cell_to_plant), FadeOut(label_cell_to_plant),
            FadeOut(light_energy_flow_label), FadeOut(atp_energy_flow_label),
            Transform(beat_title_1, Text("Recap: Biological Energy Transformations", font_size=50, color=BLUE_ACCENT, weight=BOLD).to_edge(UP))
        )

        recap_points = VGroup(
            Text("- Organisms transform energy constantly.", font_size=36, color=WHITE),
            Text("- Photosynthesis: Light Energy → Chemical Energy (Glucose)", font_size=36, color=GOLD_ACCENT),
            Text("- Cellular Respiration: Chemical Energy → Usable Energy (ATP)", font_size=36, color=BLUE_ACCENT),
            Text("- These two processes form a continuous, interdependent cycle.", font_size=36, color=WHITE)
        ).arrange(DOWN, center=True, buff=0.8).next_to(beat_title_1, DOWN, buff=1)

        self.play(LaggedStart(*[FadeIn(point, shift=UP*0.5) for point in recap_points], lag_ratio=0.3))
        self.wait(3)
        self.play(FadeOut(VGroup(beat_title_1, recap_points, title))) # Fade out everything at the end