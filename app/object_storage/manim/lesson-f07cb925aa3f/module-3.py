from manim import *

class EnergyConversionAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = BLACK
        # Custom colors inspired by 3Blue1Brown
        BLUE_ACCENT = "#50B0FF"  # Lighter blue for general text/input
        GOLD_ACCENT = "#FFD700"  # Gold for highlights/output
        DARK_BLUE = "#007FFF"   # Deeper blue for core processes
        DARK_GOLD = "#FFC107"   # Deeper gold for core processes
        GREEN_PLANT = "#228B22" # Forest Green for plant elements
        BLUE_ANIMAL = "#4682B4" # Steel Blue for animal elements

        # --- Beat 1: Strong Visual Hook & Introduction ---
        self.intro_scene(BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, GREEN_PLANT, BLUE_ANIMAL)

        # --- Beat 2: Photosynthesis Deep Dive ---
        self.photosynthesis_scene(BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, GREEN_PLANT)

        # --- Beat 3: Cellular Respiration Deep Dive ---
        self.respiration_scene(BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, BLUE_ANIMAL)

        # --- Beat 4: Interconnection & Cycle ---
        self.interconnection_scene(BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, GREEN_PLANT, BLUE_ANIMAL)

        # --- Beat 5: Recap ---
        self.recap_scene(BLUE_ACCENT, GOLD_ACCENT)

    def intro_scene(self, BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, GREEN_PLANT, BLUE_ANIMAL):
        title = Text("Energy Conversion in Living Systems", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Icons (simplified for Manim primitives)
        sun = Dot(radius=0.7, color=DARK_GOLD).shift(LEFT * 4 + UP * 2)
        plant_stem = Rectangle(width=0.2, height=1.0, color=GREEN_PLANT, fill_opacity=1)
        plant_leaves = Ellipse(width=1.5, height=0.7, color=GREEN_PLANT, fill_opacity=1).shift(UP*0.4)
        plant = VGroup(plant_stem, plant_leaves).move_to(LEFT * 1.5 + DOWN * 0.5)
        
        animal_body = Circle(radius=0.6, color=BLUE_ANIMAL, fill_opacity=1)
        animal_head = Circle(radius=0.3, color=BLUE_ANIMAL, fill_opacity=1).shift(RIGHT*0.6 + UP*0.3)
        animal = VGroup(animal_body, animal_head).move_to(RIGHT * 2.5 + DOWN * 0.5)

        self.play(FadeIn(sun, shift=UP), FadeIn(plant, shift=DOWN), FadeIn(animal, shift=DOWN))
        self.wait(0.5)

        # Energy flow arrows
        arrow_sun_plant = Arrow(start=sun.get_right(), end=plant.get_top(), color=DARK_GOLD, buff=0.1)
        arrow_plant_animal = Arrow(start=plant.get_right(), end=animal.get_left(), color=DARK_BLUE, buff=0.1)
        
        label_energy_sun = Text("Solar Energy", font_size=24, color=DARK_GOLD).next_to(arrow_sun_plant, UP, buff=0.1)
        label_energy_plant = Text("Chemical Energy", font_size=24, color=DARK_BLUE).next_to(arrow_plant_animal, UP, buff=0.1)

        self.play(Create(arrow_sun_plant), Write(label_energy_sun))
        self.wait(0.5)
        self.play(Create(arrow_plant_animal), Write(label_energy_plant))
        self.wait(1)

        # Hint at the cycle (CO2/H2O)
        arrow_animal_plant_hint = Arrow(start=animal.get_top(), end=plant.get_top() + LEFT*0.5, color=GREY_A, buff=0.1)
        arrow_animal_plant_hint.put_start_and_end_on(animal.get_top() + UP*0.5, plant.get_top() + LEFT*0.5 + UP*0.5).arc_above(0.8)
        label_co2_h2o = MathTex("CO_2, H_2O", color=GREY_A, font_size=30).next_to(arrow_animal_plant_hint, UP, buff=0.1)
        
        self.play(FadeIn(arrow_animal_plant_hint, shift=UP), FadeIn(label_co2_h2o))
        self.wait(1.5)

        self.play(
            FadeOut(title), FadeOut(sun), FadeOut(plant), FadeOut(animal),
            FadeOut(arrow_sun_plant), FadeOut(arrow_plant_animal),
            FadeOut(label_energy_sun), FadeOut(label_energy_plant),
            FadeOut(arrow_animal_plant_hint), FadeOut(label_co2_h2o)
        )

    def photosynthesis_scene(self, BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, GREEN_PLANT):
        photosynthesis_title = Text("1. Photosynthesis", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(photosynthesis_title))
        self.wait(0.5)

        # Plant icon for this scene
        plant_stem = Rectangle(width=0.2, height=1.0, color=GREEN_PLANT, fill_opacity=1)
        plant_leaves = Ellipse(width=1.5, height=0.7, color=GREEN_PLANT, fill_opacity=1).shift(UP*0.4)
        plant_icon = VGroup(plant_stem, plant_leaves).scale(0.8).move_to(ORIGIN)
        self.play(FadeIn(plant_icon))
        self.wait(0.5)

        # Inputs
        co2_in = MathTex("6CO_2", color=BLUE_ACCENT, font_size=35).shift(LEFT*3 + UP*1)
        h2o_in = MathTex("6H_2O", color=BLUE_ACCENT, font_size=35).shift(LEFT*3 + DOWN*1)
        light_in = Text("Light Energy", color=DARK_GOLD, font_size=30).shift(UP*2.5)

        arrow_co2 = Arrow(start=co2_in.get_right(), end=plant_icon.get_left(), color=BLUE_ACCENT)
        arrow_h2o = Arrow(start=h2o_in.get_right(), end=plant_icon.get_left(), color=BLUE_ACCENT)
        arrow_light = Arrow(start=light_in.get_bottom(), end=plant_icon.get_top(), color=DARK_GOLD)

        self.play(FadeIn(co2_in, shift=LEFT), Create(arrow_co2))
        self.play(FadeIn(h2o_in, shift=LEFT), Create(arrow_h2o))
        self.play(FadeIn(light_in, shift=UP), Create(arrow_light))
        self.wait(1)

        # Process and Outputs
        glucose_out = MathTex("C_6H_{12}O_6", color=GOLD_ACCENT, font_size=35).shift(RIGHT*3 + UP*1)
        o2_out = MathTex("6O_2", color=GOLD_ACCENT, font_size=35).shift(RIGHT*3 + DOWN*1)

        arrow_glucose = Arrow(start=plant_icon.get_right(), end=glucose_out.get_left(), color=GOLD_ACCENT)
        arrow_o2 = Arrow(start=plant_icon.get_right(), end=o2_out.get_left(), color=GOLD_ACCENT)

        self.play(
            FadeOut(arrow_co2), FadeOut(arrow_h2o), FadeOut(arrow_light),
            FadeOut(co2_in), FadeOut(h2o_in), FadeOut(light_in),
            FadeIn(glucose_out, shift=RIGHT), Create(arrow_glucose),
            FadeIn(o2_out, shift=RIGHT), Create(arrow_o2)
        )
        self.wait(1)

        # Chemical Equation
        equation_elements = [
            "6CO_2", " + ", "6H_2O", " + ", r"\text{Light Energy}", 
            r"\rightarrow ", 
            "C_6H_{12}O_6", " + ", "6O_2", " + ", r"\text{Heat}"
        ]
        equation = MathTex(*equation_elements, font_size=35).to_edge(DOWN)
        
        self.play(
            FadeOut(plant_icon), FadeOut(glucose_out), FadeOut(o2_out),
            FadeOut(arrow_glucose), FadeOut(arrow_o2)
        )
        self.play(Write(equation))
        self.wait(1)
        
        # Highlight energy transformation
        light_energy_text = equation.get_parts_by_tex(r"\text{Light Energy}")
        glucose_product = equation.get_parts_by_tex("C_6H_{12}O_6")
        
        energy_transform_label = Text("Light Energy ", color=DARK_GOLD, font_size=28).next_to(light_energy_text, UP, buff=0.2)
        to_label = Text(" converted to ", font_size=28).next_to(energy_transform_label, RIGHT, buff=0.1)
        chemical_energy_label = Text("Chemical Energy", color=DARK_BLUE, font_size=28).next_to(to_label, RIGHT, buff=0.1)
        energy_conversion_group = VGroup(energy_transform_label, to_label, chemical_energy_label).move_to(UP*1.5)

        self.play(
            LaggedStart(
                Indicate(light_energy_text, color=DARK_GOLD),
                Indicate(glucose_product, color=DARK_BLUE),
                Write(energy_conversion_group),
                lag_ratio=0.5
            )
        )
        self.wait(2)
        self.play(FadeOut(equation), FadeOut(energy_conversion_group), FadeOut(photosynthesis_title))


    def respiration_scene(self, BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, BLUE_ANIMAL):
        respiration_title = Text("2. Cellular Respiration", font_size=40, color=BLUE_ACCENT).to_edge(UP)
        self.play(Write(respiration_title))
        self.wait(0.5)

        # Animal icon for this scene
        animal_body = Circle(radius=0.6, color=BLUE_ANIMAL, fill_opacity=1)
        animal_head = Circle(radius=0.3, color=BLUE_ANIMAL, fill_opacity=1).shift(RIGHT*0.6 + UP*0.3)
        animal_icon = VGroup(animal_body, animal_head).scale(0.8).move_to(ORIGIN)
        self.play(FadeIn(animal_icon))
        self.wait(0.5)

        # Inputs
        glucose_in = MathTex("C_6H_{12}O_6", color=GOLD_ACCENT, font_size=35).shift(LEFT*3 + UP*1)
        o2_in = MathTex("6O_2", color=GOLD_ACCENT, font_size=35).shift(LEFT*3 + DOWN*1)

        arrow_glucose = Arrow(start=glucose_in.get_right(), end=animal_icon.get_left(), color=GOLD_ACCENT)
        arrow_o2 = Arrow(start=o2_in.get_right(), end=animal_icon.get_left(), color=GOLD_ACCENT)

        self.play(FadeIn(glucose_in, shift=LEFT), Create(arrow_glucose))
        self.play(FadeIn(o2_in, shift=LEFT), Create(arrow_o2))
        self.wait(1)

        # Process and Outputs
        co2_out = MathTex("6CO_2", color=BLUE_ACCENT, font_size=35).shift(RIGHT*3 + UP*1)
        h2o_out = MathTex("6H_2O", color=BLUE_ACCENT, font_size=35).shift(RIGHT*3 + DOWN*1)
        atp_out = Text("ATP (Usable Energy)", color=GOLD_ACCENT, font_size=30).shift(RIGHT*3 + UP*2.5)

        arrow_co2 = Arrow(start=animal_icon.get_right(), end=co2_out.get_left(), color=BLUE_ACCENT)
        arrow_h2o = Arrow(start=animal_icon.get_right(), end=h2o_out.get_left(), color=BLUE_ACCENT)
        arrow_atp = Arrow(start=animal_icon.get_top(), end=atp_out.get_bottom(), color=GOLD_ACCENT)

        self.play(
            FadeOut(arrow_glucose), FadeOut(arrow_o2),
            FadeOut(glucose_in), FadeOut(o2_in),
            FadeIn(co2_out, shift=RIGHT), Create(arrow_co2),
            FadeIn(h2o_out, shift=RIGHT), Create(arrow_h2o),
            FadeIn(atp_out, shift=UP), Create(arrow_atp)
        )
        self.wait(1)

        # Chemical Equation
        equation_elements = [
            "C_6H_{12}O_6", " + ", "6O_2", 
            r"\rightarrow ", 
            "6CO_2", " + ", "6H_2O", " + ", r"\text{ATP (Energy)}", " + ", r"\text{Heat}"
        ]
        equation = MathTex(*equation_elements, font_size=35).to_edge(DOWN)
        
        self.play(
            FadeOut(animal_icon), FadeOut(co2_out), FadeOut(h2o_out), FadeOut(atp_out),
            FadeOut(arrow_co2), FadeOut(arrow_h2o), FadeOut(arrow_atp)
        )
        self.play(Write(equation))
        self.wait(1)
        
        # Highlight energy transformation
        glucose_reactant = equation.get_parts_by_tex("C_6H_{12}O_6")
        atp_product = equation.get_parts_by_tex(r"\text{ATP (Energy)}")
        
        energy_transform_label = Text("Chemical Energy ", color=DARK_BLUE, font_size=28).next_to(glucose_reactant, UP, buff=0.2)
        to_label = Text(" converted to ", font_size=28).next_to(energy_transform_label, RIGHT, buff=0.1)
        usable_energy_label = Text("Usable Energy (ATP)", color=DARK_GOLD, font_size=28).next_to(to_label, RIGHT, buff=0.1)
        energy_conversion_group = VGroup(energy_transform_label, to_label, usable_energy_label).move_to(UP*1.5)

        self.play(
            LaggedStart(
                Indicate(glucose_reactant, color=DARK_BLUE),
                Indicate(atp_product, color=DARK_GOLD),
                Write(energy_conversion_group),
                lag_ratio=0.5
            )
        )
        self.wait(2)
        self.play(FadeOut(equation), FadeOut(energy_conversion_group), FadeOut(respiration_title))

    def interconnection_scene(self, BLUE_ACCENT, GOLD_ACCENT, DARK_BLUE, DARK_GOLD, GREEN_PLANT, BLUE_ANIMAL):
        interconnection_title = Text("3. The Interconnected Cycle", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(interconnection_title))
        self.wait(0.5)

        # Plant and Animal icons for the cycle
        plant_stem = Rectangle(width=0.2, height=1.0, color=GREEN_PLANT, fill_opacity=1)
        plant_leaves = Ellipse(width=1.5, height=0.7, color=GREEN_PLANT, fill_opacity=1).shift(UP*0.4)
        plant_icon = VGroup(plant_stem, plant_leaves).scale(0.8).shift(LEFT * 3)
        
        animal_body = Circle(radius=0.6, color=BLUE_ANIMAL, fill_opacity=1)
        animal_head = Circle(radius=0.3, color=BLUE_ANIMAL, fill_opacity=1).shift(RIGHT*0.6 + UP*0.3)
        animal_icon = VGroup(animal_body, animal_head).scale(0.8).shift(RIGHT * 3)

        self.play(FadeIn(plant_icon), FadeIn(animal_icon))
        self.wait(0.5)

        # Labels for processes
        photosynthesis_label = Text("Photosynthesis", font_size=30, color=DARK_GOLD).next_to(plant_icon, UP, buff=0.2)
        respiration_label = Text("Cellular Respiration", font_size=30, color=DARK_BLUE).next_to(animal_icon, UP, buff=0.2)
        self.play(Write(photosynthesis_label), Write(respiration_label))
        self.wait(0.5)

        # Flow from plant to animal (Glucose, O2)
        glucose_o2_text = MathTex("C_6H_{12}O_6", ",", "6O_2", color=GOLD_ACCENT, font_size=30).next_to(plant_icon, RIGHT).shift(UP*0.5)
        arrow_plant_animal = Arrow(start=plant_icon.get_right(), end=animal_icon.get_left(), color=GOLD_ACCENT, buff=0.1)
        self.play(FadeIn(glucose_o2_text), Create(arrow_plant_animal))
        self.wait(1)

        # Flow from animal to plant (CO2, H2O)
        co2_h2o_text = MathTex("6CO_2", ",", "6H_2O", color=BLUE_ACCENT, font_size=30).next_to(animal_icon, LEFT).shift(DOWN*0.5)
        arrow_animal_plant = Arrow(start=animal_icon.get_left(), end=plant_icon.get_right(), color=BLUE_ACCENT, buff=0.1)
        arrow_animal_plant.put_start_and_end_on(animal_icon.get_bottom() + LEFT*0.5, plant_icon.get_bottom() + RIGHT*0.5).arc_below(1.5)
        self.play(FadeIn(co2_h2o_text), Create(arrow_animal_plant))
        self.wait(1)

        # External energy input (Sun)
        sun_dot = Dot(radius=0.4, color=DARK_GOLD).to_corner(UL)
        arrow_sun_plant = Arrow(start=sun_dot.get_right(), end=plant_icon.get_top() + LEFT*0.5, color=DARK_GOLD, buff=0.1)
        arrow_sun_plant.put_start_and_end_on(sun_dot.get_bottom() + RIGHT*0.5, plant_icon.get_top() + UP*0.5 + LEFT*0.5).arc_below(1)
        solar_energy_text = Text("Solar Energy", font_size=24, color=DARK_GOLD).next_to(sun_dot, DOWN)
        self.play(FadeIn(sun_dot), FadeIn(solar_energy_text), Create(arrow_sun_plant))
        self.wait(1)

        # Usable energy output (ATP)
        atp_text = Text("ATP (Usable Energy)", font_size=24, color=GOLD_ACCENT).next_to(animal_icon, DOWN, buff=1)
        arrow_atp_out = Arrow(start=animal_icon.get_bottom(), end=atp_text.get_top(), color=GOLD_ACCENT)
        self.play(FadeIn(atp_text), Create(arrow_atp_out))
        self.wait(2)

        self.play(
            FadeOut(interconnection_title), FadeOut(plant_icon), FadeOut(animal_icon),
            FadeOut(photosynthesis_label), FadeOut(respiration_label),
            FadeOut(glucose_o2_text), FadeOut(arrow_plant_animal),
            FadeOut(co2_h2o_text), FadeOut(arrow_animal_plant),
            FadeOut(sun_dot), FadeOut(solar_energy_text), FadeOut(arrow_sun_plant),
            FadeOut(atp_text), FadeOut(arrow_atp_out)
        )

    def recap_scene(self, BLUE_ACCENT, GOLD_ACCENT):
        recap_card = Rectangle(width=8, height=4.5, color=GREY_C, fill_opacity=0.2, stroke_opacity=1, stroke_color=GOLD_ACCENT)
        recap_title = Text("Recap: Energy Conversion", font_size=45, color=GOLD_ACCENT).align_to(recap_card, UP).shift(UP*0.3)

        bullet1 = BulletedList(
            "Photosynthesis: Light Energy → Chemical Energy (Glucose)",
            font_size=30, color=WHITE
        ).next_to(recap_title, DOWN, buff=0.5).align_to(recap_card, LEFT).shift(RIGHT*0.5)
        
        bullet2 = BulletedList(
            "Cellular Respiration: Chemical Energy → Usable Energy (ATP)",
            font_size=30, color=WHITE
        ).next_to(bullet1, DOWN, buff=0.5).align_to(recap_card, LEFT).shift(RIGHT*0.5)
        
        bullet3 = BulletedList(
            "Life is an Interconnected Cycle: Matter Recycles, Energy Flows",
            font_size=30, color=WHITE
        ).next_to(bullet2, DOWN, buff=0.5).align_to(recap_card, LEFT).shift(RIGHT*0.5)

        recap_group = VGroup(recap_card, recap_title, bullet1, bullet2, bullet3).center()

        self.play(FadeIn(recap_card, scale=0.8), Write(recap_title))
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT) for b in bullet1], lag_ratio=0.5))
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT) for b in bullet2], lag_ratio=0.5))
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT) for b in bullet3], lag_ratio=0.5))
        self.wait(3)
        self.play(FadeOut(recap_group))
        self.wait(1)