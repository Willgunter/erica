from manim import *

class EcologyAnimation(Scene):
    def construct(self):
        # 1. Configuration: Dark background, custom colors
        config.background_color = BLACK
        ORGANISM_COLOR = BLUE_C
        ENVIRONMENT_COLOR = GOLD_C
        TEXT_COLOR = WHITE
        INTERACTION_COLOR = RED_C
        PRODUCER_COLOR = GREEN_C # For producers
        ABIOTIC_COLOR = GRAY_A # For non-living elements like rock/soil

        # --- Scene 1: Visual Hook & Title ---
        # Strong visual hook: A swirling pattern of interconnected nodes,
        # reminiscent of complex systems or biological networks.

        num_nodes = 12
        nodes = VGroup(*[Dot(radius=0.1, color=ORGANISM_COLOR) for _ in range(num_nodes)])
        # Position nodes in a spiral or scattered for dynamic feel
        for i, node in enumerate(nodes):
            angle = i * (2 * PI / num_nodes) * 2 # Spiral effect
            node.move_to(np.array([np.cos(angle), np.sin(angle), 0]) * (2 + 0.5 * np.sin(angle*2)))
        nodes.move_to(ORIGIN)


        # Create connections (lines) between nodes - abstract network
        lines = VGroup()
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if np.random.rand() < 0.2: # Randomly connect some nodes
                    line = Line(nodes[i].get_center(), nodes[j].get_center(), stroke_width=1, color=ENVIRONMENT_COLOR)
                    lines.add(line)

        system = VGroup(nodes, lines).scale(0.7)

        # Animate the system's dynamic nature
        self.play(
            LaggedStart(*[
                node.animate.shift(np.random.rand(3) * 0.4 - 0.2).set_opacity(1).scale(1.1)
                for node in nodes
            ], lag_ratio=0.08, run_time=2),
            Create(lines, run_time=2),
            system.animate.rotate(TAU/12),
        )
        self.wait(0.5)

        # Title Introduction
        title = Text("Ecology & Environmental Interactions", font_size=50, color=TEXT_COLOR)
        subtitle = Text("The dance of life and its surroundings.", font_size=28, color=GOLD_C).next_to(title, DOWN)

        self.play(
            FadeOut(system),
            Write(title),
            FadeIn(subtitle, shift=UP),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(subtitle))


        # --- Scene 2: Concept 1 - Organisms and Their Environment ---
        # Build intuition first: A central organism interacting with its surroundings.

        organism_dot = Dot(point=ORIGIN, radius=0.2, color=ORGANISM_COLOR)
        organism_text = MathTex(r"\text{Organism}", color=TEXT_COLOR).next_to(organism_dot, DOWN, buff=0.3)

        # Environmental factors (Abiotic & Biotic)
        sun_icon = Dot(radius=0.15, color=GOLD_C).move_to([-2, 1, 0])
        sun_text = MathTex(r"\text{Sunlight}", color=TEXT_COLOR).next_to(sun_icon, UP)
        water_icon = Square(side_length=0.3, color=BLUE_A).move_to([2, 1, 0])
        water_text = MathTex(r"\text{Water}", color=TEXT_COLOR).next_to(water_icon, UP)
        food_icon = Triangle(fill_opacity=1, color=PRODUCER_COLOR).move_to([-2, -1, 0])
        food_text = MathTex(r"\text{Food}", color=TEXT_COLOR).next_to(food_icon, DOWN)
        rock_icon = Polygon(
            [-0.1, 0, 0], [0.1, 0, 0], [0.25, 0.2, 0], [0.05, 0.3, 0], [-0.2, 0.25, 0], [-0.3, 0.1, 0],
            color=ABIOTIC_COLOR, fill_opacity=1
        ).scale(0.8).move_to([2, -1, 0])
        rock_text = MathTex(r"\text{Shelter}", color=TEXT_COLOR).next_to(rock_icon, DOWN)

        environment_elements = VGroup(sun_icon, sun_text, water_icon, water_text, food_icon, food_text, rock_icon, rock_text)

        self.play(
            ReplacementTransform(title, organism_dot),
            FadeIn(organism_text, shift=DOWN)
        )
        self.wait(0.5)

        self.play(
            LaggedStartMap(FadeIn, environment_elements, shift=UR, stagger=0.1),
            organism_dot.animate.scale(1.2).set_color(ORGANISM_COLOR),
            run_time=1.5
        )

        # Arrows showing interaction
        arrow_sun = Arrow(sun_icon.get_right(), organism_dot.get_left(), buff=0.1, color=ENVIRONMENT_COLOR, tip_length=0.2)
        arrow_water = Arrow(water_icon.get_left(), organism_dot.get_right(), buff=0.1, color=ENVIRONMENT_COLOR, tip_length=0.2)
        arrow_food = Arrow(food_icon.get_up(), organism_dot.get_down(), buff=0.1, color=ENVIRONMENT_COLOR, tip_length=0.2)
        arrow_shelter = Arrow(organism_dot.get_bottom(), rock_icon.get_top(), buff=0.1, color=ENVIRONMENT_COLOR, tip_length=0.2) # organism using shelter

        self.play(
            Create(arrow_sun),
            Create(arrow_water),
            Create(arrow_food),
            Create(arrow_shelter),
            run_time=1.5
        )
        self.wait(0.5)

        # Formal definition
        ecology_def = MathTex(
            r"\text{Ecology:}", r"\text{ The study of how organisms}", r"\text{ interact with each other}",
            r"\text{ and their environment.}",
            color=TEXT_COLOR
        ).scale(0.7).to_edge(UP)

        self.play(
            FadeOut(organism_text), FadeOut(environment_elements), FadeOut(arrow_sun, arrow_water, arrow_food, arrow_shelter),
            organism_dot.animate.move_to(ecology_def[1].get_center() + DOWN*0.5).scale(0.5), # Organism dot moves towards its part of the def
            Write(ecology_def[0]),
            Write(ecology_def[1]),
            run_time=1
        )
        self.play(Write(ecology_def[2]), run_time=0.7)
        self.play(Write(ecology_def[3]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(ecology_def, organism_dot))

        # --- Scene 3: Concept 2 - Interactions: Populations & Communities ---
        # Visualizing multiple organisms and their interactions.

        # Populations
        population_group_1 = VGroup(*[Dot(radius=0.1, color=ORGANISM_COLOR).move_to(ORIGIN + np.random.rand(3)*1.5 - 0.75) for _ in range(8)])
        population_text_1 = MathTex(r"\text{Population A}", color=TEXT_COLOR).next_to(population_group_1, DOWN, buff=0.5)
        
        population_group_2 = VGroup(*[Dot(radius=0.1, color=RED_C).move_to(ORIGIN + np.random.rand(3)*1.5 - 0.75 + RIGHT*3) for _ in range(5)])
        population_text_2 = MathTex(r"\text{Population B}", color=TEXT_COLOR).next_to(population_group_2, DOWN, buff=0.5)

        self.play(
            LaggedStartMap(FadeIn, population_group_1, shift=UP, scale=1.1),
            Write(population_text_1)
        )
        self.wait(0.5)

        # Interaction (Predator-Prey example)
        # Shift population A to the left
        self.play(population_group_1.animate.shift(LEFT*1.5), population_text_1.animate.shift(LEFT*1.5))
        self.play(
            LaggedStartMap(FadeIn, population_group_2, shift=UP, scale=1.1),
            Write(population_text_2)
        )
        self.wait(0.5)

        # Draw arrows for interaction
        interaction_arrow_1 = Arrow(population_group_1.get_right(), population_group_2.get_left(), buff=0.2, color=INTERACTION_COLOR, tip_length=0.2)
        interaction_arrow_2 = Arrow(population_group_2.get_left(), population_group_1.get_right(), buff=0.2, color=INTERACTION_COLOR, tip_length=0.2)
        
        interaction_label = MathTex(r"\text{Interaction}", color=TEXT_COLOR).next_to(interaction_arrow_1, UP, buff=0.3)
        
        self.play(Create(interaction_arrow_1), Create(interaction_arrow_2), Write(interaction_label))
        self.wait(0.5)

        # Show population change
        self.play(
            population_group_1[0].animate.set_color(RED_D).scale(0.5).fade(0.8), # One gets 'consumed' or affected, fades out
            population_group_2[0].animate.set_color(PRODUCER_COLOR).scale(1.5), # One thrives
            run_time=1
        )
        self.wait(0.5)

        # Formal definition
        population_def = MathTex(r"\text{Population: A group of the same species.}", color=TEXT_COLOR).scale(0.7).to_edge(UP)
        community_def = MathTex(r"\text{Community: Interacting populations of different species.}", color=TEXT_COLOR).scale(0.7).next_to(population_def, DOWN)

        self.play(
            FadeOut(population_group_2, interaction_arrow_1, interaction_arrow_2, interaction_label, population_text_2),
            TransformMatchingTex(population_text_1, population_def),
            population_group_1.animate.scale(0.8).next_to(population_def, DOWN, buff=0.5)
        )
        self.wait(1)
        self.play(Write(community_def))
        # Bring back a generic second population to illustrate community
        temp_pop_2 = VGroup(*[Dot(radius=0.1, color=RED_C).move_to(population_group_1.get_center() + RIGHT*4 + np.random.rand(3)*1 - 0.5) for _ in range(4)]).scale(0.8)
        self.play(
            population_group_1.animate.shift(LEFT*2.5),
            LaggedStartMap(FadeIn, temp_pop_2, shift=UP)
        )
        self.wait(0.5)
        self.play(FadeOut(population_group_1, temp_pop_2, population_def, community_def))


        # --- Scene 4: Concept 3 - Ecosystems & Energy Flow ---
        # From specific interactions to a broader system.

        # Ecosystem: Abiotic + Biotic
        # Use a number plane abstractly for space/environment
        plane = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-3, 3, 1],
            x_length=12, y_length=7,
            background_line_style={"stroke_opacity": 0.2, "stroke_color": GRAY},
            axis_config={"stroke_opacity": 0.4, "color": GRAY},
        ).to_edge(DOWN, buff=0.5).scale(0.8) # Move it slightly down to make space for text
        self.play(Create(plane, run_time=1.5))
        
        # Abiotic factors
        sun = Dot(radius=0.2, color=GOLD_C).move_to(plane.coords_to_point(-4, 2.5))
        water_body = Rectangle(width=2, height=0.8, color=BLUE_A, fill_opacity=0.7).move_to(plane.coords_to_point(4, -2))
        air_waves = Arc(radius=0.8, start_angle=PI/4, angle=PI/2, color=WHITE, stroke_width=2).move_to(plane.coords_to_point(-2, 2.5)).shift(LEFT*0.5)
        air_waves_2 = Arc(radius=0.8, start_angle=PI/4, angle=PI/2, color=WHITE, stroke_width=2).move_to(plane.coords_to_point(-2, 2.5)).shift(RIGHT*0.5)

        abiotic_label = MathTex(r"\text{Abiotic Factors}", color=TEXT_COLOR).next_to(sun, UP*1.5).scale(0.7)

        self.play(
            FadeIn(sun),
            FadeIn(water_body),
            Create(air_waves), Create(air_waves_2),
            Write(abiotic_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Biotic (producers, consumers)
        producer = Triangle(fill_opacity=1, color=PRODUCER_COLOR).scale(0.5).move_to(plane.coords_to_point(0, -1))
        producer_text = MathTex(r"\text{Producer}", color=TEXT_COLOR).next_to(producer, DOWN)

        consumer_1 = Dot(radius=0.15, color=ORGANISM_COLOR).move_to(plane.coords_to_point(1.5, 0.5))
        consumer_text_1 = MathTex(r"\text{Consumer 1}", color=TEXT_COLOR).next_to(consumer_1, DOWN)

        consumer_2 = Dot(radius=0.2, color=RED_C).move_to(plane.coords_to_point(-1.5, 1.5))
        consumer_text_2 = MathTex(r"\text{Consumer 2}", color=TEXT_COLOR).next_to(consumer_2, DOWN)

        biotic_label = MathTex(r"\text{Biotic Factors}", color=TEXT_COLOR).next_to(producer, DOWN*3).scale(0.7)


        self.play(
            FadeIn(producer, producer_text),
            FadeIn(consumer_1, consumer_text_1),
            FadeIn(consumer_2, consumer_text_2),
            Write(biotic_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Energy Flow arrows
        arrow_sun_producer = Arrow(sun.get_bottom(), producer.get_top(), buff=0.1, color=GOLD_C, tip_length=0.2)
        arrow_producer_c1 = Arrow(producer.get_top(), consumer_1.get_bottom(), buff=0.1, color=INTERACTION_COLOR, tip_length=0.2)
        arrow_c1_c2 = Arrow(consumer_1.get_top(), consumer_2.get_bottom(), buff=0.1, color=INTERACTION_COLOR, tip_length=0.2)

        energy_flow_label = MathTex(r"\text{Energy Flow}", color=TEXT_COLOR).next_to(arrow_producer_c1, LEFT, buff=0.3)

        self.play(
            Create(arrow_sun_producer),
            Create(arrow_producer_c1),
            Create(arrow_c1_c2),
            Write(energy_flow_label),
            run_time=1.5
        )
        self.wait(0.5)

        ecosystem_def = MathTex(
            r"\text{Ecosystem:}", r"\text{ All biotic and abiotic factors}",
            r"\text{ interacting in an area.}",
            color=TEXT_COLOR
        ).scale(0.7).to_edge(UP)
        
        self.play(
            FadeOut(plane, abiotic_label, biotic_label, sun, water_body, air_waves, air_waves_2),
            FadeOut(producer, producer_text, consumer_1, consumer_text_1, consumer_2, consumer_text_2),
            FadeOut(arrow_sun_producer, arrow_producer_c1, arrow_c1_c2, energy_flow_label),
            Write(ecosystem_def[0]), Write(ecosystem_def[1]),
            run_time=1
        )
        self.play(Write(ecosystem_def[2]))
        self.wait(1)
        self.play(FadeOut(ecosystem_def))

        # --- Scene 5: Recap Card ---
        recap_title = Text("Recap: Key Concepts", font_size=40, color=GOLD_C).to_edge(UP)
        
        # Using bullet points
        bullet1 = MathTex(r"\bullet \text{ Ecology: Study of interactions.}", color=TEXT_COLOR).scale(0.8).next_to(recap_title, DOWN, buff=0.5)
        bullet2 = MathTex(r"\bullet \text{ Organisms interact with environment.}", color=TEXT_COLOR).scale(0.8).next_to(bullet1, DOWN)
        bullet3 = MathTex(r"\bullet \text{ Populations form communities.}", color=TEXT_COLOR).scale(0.8).next_to(bullet2, DOWN)
        bullet4 = MathTex(r"\bullet \text{ Ecosystems: Biotic + Abiotic interactions.}", color=TEXT_COLOR).scale(0.8).next_to(bullet3, DOWN)
        bullet5 = MathTex(r"\bullet \text{ Energy flows through ecosystems.}", color=TEXT_COLOR).scale(0.8).next_to(bullet4, DOWN)

        recap_bullets = VGroup(bullet1, bullet2, bullet3, bullet4, bullet5).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(LEFT*2)

        self.play(Write(recap_title))
        self.play(LaggedStart(*[FadeIn(bullet) for bullet in recap_bullets], lag_ratio=0.3, run_time=3))
        self.wait(2)

        self.play(FadeOut(recap_title, recap_bullets))