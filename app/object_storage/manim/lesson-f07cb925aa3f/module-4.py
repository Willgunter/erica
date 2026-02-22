from manim import *

class EcologyAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = "#1a1a1a" # Dark background
        BLUE_ACCENT = "#42a5f5"
        GOLD_ACCENT = "#ffc107"
        TEXT_COLOR = WHITE

        # --- Opening Hook: Abstract Ecosystem Interaction ---
        organism_core = Circle(radius=0.5, color=GOLD_ACCENT, fill_opacity=0.8).move_to(ORIGIN)
        
        env_elements = VGroup(
            Square(side_length=0.4, color=BLUE_ACCENT, fill_opacity=0.6).shift(LEFT*2 + UP*1.5),
            Triangle(side_length=0.5, color=BLUE_ACCENT, fill_opacity=0.6).shift(RIGHT*1.8 + UP*1.2),
            Polygon([-0.5, -0.5, 0], [0.5, -0.5, 0], [0, 0.5, 0], color=BLUE_ACCENT, fill_opacity=0.6).shift(LEFT*1.5 + DOWN*1.5), # A simple triangle
            Ellipse(width=0.8, height=0.3, color=BLUE_ACCENT, fill_opacity=0.6).shift(RIGHT*2 + DOWN*1.3)
        )
        
        connections = VGroup()
        for elem in env_elements:
            connections.add(Arrow(organism_core.get_center(), elem.get_center(), buff=0.1, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.15))
            connections.add(Arrow(elem.get_center(), organism_core.get_center(), buff=0.1, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.15))

        # Initial subtle animation of interactions
        self.play(
            GrowFromCenter(organism_core),
            LaggedStart(*[FadeIn(elem) for elem in env_elements], lag_ratio=0.1),
            run_time=1.5
        )
        self.play(
            LaggedStart(*[GrowArrow(conn) for conn in connections], lag_ratio=0.05),
            run_time=2
        )
        
        # Title Card
        title = Tex("Ecology: Interactions and Evolution", font_size=50, color=BLUE_ACCENT).to_edge(UP)
        subtitle = Tex("Understanding Complex Systems", font_size=30, color=GOLD_ACCENT).next_to(title, DOWN, buff=0.2)
        
        self.play(
            FadeOut(VGroup(organism_core, env_elements, connections)),
            Write(title),
            FadeIn(subtitle),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 1: What is Ecology? (Organism-Environment Interaction) ---
        beat1_title = Tex("1. Organism-Environment Interaction", font_size=35, color=GOLD_ACCENT).to_edge(UP)
        self.play(
            ReplacementTransform(title, beat1_title),
            FadeOut(subtitle),
            run_time=0.8
        )
        
        organism_tex = MathTex("\\text{Organism}", color=GOLD_ACCENT).move_to(LEFT * 3)
        environment_tex = MathTex("\\text{Environment}", color=BLUE_ACCENT).move_to(RIGHT * 3)
        
        interaction_arrow_to = Arrow(organism_tex.get_right(), environment_tex.get_left(), buff=0.1, color=WHITE)
        interaction_arrow_from = Arrow(environment_tex.get_left(), organism_tex.get_right(), buff=0.1, color=WHITE)
        
        interaction_label = Tex("Ecology", color=TEXT_COLOR).next_to(VGroup(interaction_arrow_to, interaction_arrow_from), UP, buff=0.3)
        
        self.play(
            Write(organism_tex),
            Write(environment_tex),
            run_time=1
        )
        self.play(
            GrowArrow(interaction_arrow_to),
            GrowArrow(interaction_arrow_from),
            FadeIn(interaction_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Visualizing resource flow
        food_source = Circle(radius=0.3, color=GREEN_B, fill_opacity=0.7).next_to(environment_tex, UP, buff=0.5)
        water_source = Square(side_length=0.6, color=BLUE_B, fill_opacity=0.7).next_to(environment_tex, DOWN, buff=0.5)
        
        food_arrow = Arrow(food_source.get_left(), organism_tex.get_right(), buff=0.1, color=GREEN_A)
        water_arrow = Arrow(water_source.get_left(), organism_tex.get_right(), buff=0.1, color=BLUE_A)
        
        self.play(
            FadeIn(food_source, water_source),
            Create(food_arrow),
            Create(water_arrow),
            run_time=1.5
        )
        self.wait(1)
        
        # --- Beat 2: Population Dynamics (Growth & Carrying Capacity) ---
        beat2_title = Tex("2. Population Dynamics", font_size=35, color=GOLD_ACCENT).to_edge(UP)
        self.play(
            ReplacementTransform(beat1_title, beat2_title),
            FadeOut(VGroup(organism_tex, environment_tex, interaction_arrow_to, interaction_arrow_from, interaction_label, food_source, water_source, food_arrow, water_arrow)),
            run_time=1
        )
        
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=6, y_length=4,
            axis_config={"color": GRAY_A, "include_numbers": True},
            x_axis_config={"numbers_to_exclude": [0]},
            y_axis_config={"numbers_to_exclude": [0]}
        ).to_edge(DOWN).shift(UP*0.5)
        
        x_label = axes.get_x_axis_label(Tex("Time", color=TEXT_COLOR))
        y_label = axes.get_y_axis_label(Tex("Population Size", color=TEXT_COLOR), edge=LEFT, direction=UP)
        
        logistic_func = lambda x: (9.5 * (1 / (1 + np.exp(-0.8 * (x - 4)))))
        graph = axes.get_graph(logistic_func, x_range=[0, 9.5], color=BLUE_ACCENT)
        
        carrying_capacity_line = axes.get_horizontal_line(
            axes.c2p(0, 9.5), color=GOLD_ACCENT, line_func=Line, x_range=[0, 9.5]
        )
        carrying_capacity_label = MathTex("\\text{Carrying Capacity}", color=GOLD_ACCENT, font_size=25).next_to(carrying_capacity_line, RIGHT, buff=0.1)
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        self.play(
            Create(graph, run_time=2.5, rate_func=rate_functions.ease_out_sine)
        )
        self.play(
            Create(carrying_capacity_line),
            FadeIn(carrying_capacity_label),
            run_time=1.5
        )
        self.wait(1)

        # --- Beat 3: Interspecies Interactions ---
        beat3_title = Tex("3. Interspecies Interactions", font_size=35, color=GOLD_ACCENT).to_edge(UP)
        self.play(
            ReplacementTransform(beat2_title, beat3_title),
            FadeOut(VGroup(axes, x_label, y_label, graph, carrying_capacity_line, carrying_capacity_label)),
            run_time=1
        )

        predator_shape = Polygon([-0.8,0,0], [0.8,0,0], [0,1,0], color=GOLD_ACCENT, fill_opacity=0.8).scale(0.8).shift(LEFT*2.5)
        prey_shape = Circle(radius=0.4, color=BLUE_ACCENT, fill_opacity=0.8).shift(RIGHT*2.5)
        
        predator_label = Tex("Predator", color=GOLD_ACCENT).next_to(predator_shape, DOWN)
        prey_label = Tex("Prey", color=BLUE_ACCENT).next_to(prey_shape, DOWN)

        self.play(
            FadeIn(predator_shape, predator_label),
            FadeIn(prey_shape, prey_label),
            run_time=1.5
        )
        
        # Predator-Prey interaction
        self.play(
            predator_shape.animate.shift(RIGHT*1),
            prey_shape.animate.shift(LEFT*1),
            run_time=1
        )
        arrow_hunt = Arrow(predator_shape.get_right(), prey_shape.get_left(), buff=0.1, color=WHITE, max_tip_length_to_length_ratio=0.15)
        self.play(
            GrowArrow(arrow_hunt),
            run_time=0.5
        )
        self.play(
            FadeOut(prey_shape),
            FadeOut(prey_label),
            predator_shape.animate.scale(1.2), # Predator grows
            FadeOut(arrow_hunt),
            run_time=1
        )
        self.wait(0.5)

        # Symbiosis (Commensalism/Mutualism)
        symbiote1 = Circle(radius=0.4, color=BLUE_ACCENT, fill_opacity=0.8).move_to(LEFT*2)
        symbiote2 = Square(side_length=0.7, color=GOLD_ACCENT, fill_opacity=0.8).move_to(RIGHT*2)

        symbiosis_label = Tex("Symbiosis", color=TEXT_COLOR).to_edge(DOWN)
        
        self.play(
            FadeOut(VGroup(predator_shape, predator_label)), # Remove previous interaction
            FadeIn(symbiote1, symbiote2),
            Write(symbiosis_label),
            run_time=1.5
        )
        
        self.play(
            symbiote1.animate.shift(RIGHT*1),
            symbiote2.animate.shift(LEFT*1),
            run_time=1.5
        )
        # Indicate mutual benefit with small arrows/particles
        energy_exchange_a = Arrow(symbiote1.get_right(), symbiote2.get_left(), buff=0.1, color=GREEN_A)
        energy_exchange_b = Arrow(symbiote2.get_left(), symbiote1.get_right(), buff=0.1, color=GREEN_B)
        self.play(
            Create(energy_exchange_a),
            Create(energy_exchange_b),
            run_time=1
        )
        self.wait(1)

        # --- Beat 4: Evolution & Adaptation ---
        beat4_title = Tex("4. Evolution \& Adaptation", font_size=35, color=GOLD_ACCENT).to_edge(UP)
        self.play(
            ReplacementTransform(beat3_title, beat4_title),
            FadeOut(VGroup(symbiote1, symbiote2, symbiosis_label, energy_exchange_a, energy_exchange_b)),
            run_time=1
        )
        
        # Initial organism
        initial_organism = Circle(radius=0.6, color=BLUE_ACCENT, fill_opacity=0.7).move_to(LEFT*3)
        initial_label = Tex("Initial Form", color=BLUE_ACCENT).next_to(initial_organism, DOWN)
        
        # Environmental pressure (abstract)
        pressure_box = Rectangle(width=2, height=1.5, color=RED_C, fill_opacity=0.2).move_to(ORIGIN)
        pressure_label = Tex("Environmental\\nPressure", color=RED_C, font_size=25).move_to(pressure_box.get_center())
        
        self.play(
            FadeIn(initial_organism, initial_label),
            Create(pressure_box),
            Write(pressure_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Adaptation process
        # A diamond shape is a good geometric transformation from a circle
        adapted_organism = Polygon([0,-0.6,0], [0.6,0,0], [0,0.6,0], [-0.6,0,0], color=GOLD_ACCENT, fill_opacity=0.7).move_to(RIGHT*3)
        adapted_label = Tex("Adapted Form", color=GOLD_ACCENT).next_to(adapted_organism, DOWN)
        
        evolution_arrow = CurvedArrow(initial_organism.get_right(), adapted_organism.get_left(), angle=-PI/2, buff=0.5, color=WHITE)
        evolution_text = Tex("Adaptation over time", color=TEXT_COLOR).next_to(evolution_arrow, UP, buff=0.4)

        self.play(
            ReplacementTransform(initial_organism, adapted_organism),
            ReplacementTransform(initial_label, adapted_label),
            Create(evolution_arrow),
            Write(evolution_text),
            FadeOut(pressure_box, pressure_label),
            run_time=2.5
        )
        self.wait(1)
        
        # --- Recap Card ---
        self.play(
            FadeOut(VGroup(beat4_title, adapted_organism, adapted_label, evolution_arrow, evolution_text)),
            run_time=1
        )
        
        recap_title = Tex("Recap: Key Ecological Concepts", font_size=45, color=BLUE_ACCENT).to_edge(UP, buff=0.8)
        
        recap_points = VGroup(
            Tex("1. \\textbf{Ecology}: Organism-Environment Interactions", color=TEXT_COLOR),
            Tex("2. \\textbf{Population Dynamics}: Growth \& Carrying Capacity", color=TEXT_COLOR),
            Tex("3. \\textbf{Interspecies Interactions}: Predator-Prey, Symbiosis", color=TEXT_COLOR),
            Tex("4. \\textbf{Evolution}: Adaptation Over Time", color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).scale(0.8).next_to(recap_title, DOWN, buff=0.8)

        recap_points[0].set_color_by_tex("Ecology", GOLD_ACCENT)
        recap_points[1].set_color_by_tex("Population Dynamics", GOLD_ACCENT)
        recap_points[2].set_color_by_tex("Interspecies Interactions", GOLD_ACCENT)
        recap_points[3].set_color_by_tex("Evolution", GOLD_ACCENT)
        
        self.play(
            Write(recap_title),
            LaggedStart(*[FadeIn(point, shift=UP*0.5) for point in recap_points], lag_ratio=0.3),
            run_time=3
        )
        self.wait(3)