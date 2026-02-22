from manim import *

class EcologyTrophicEvolution(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        
        # Define a consistent color palette inspired by 3Blue1Brown
        COLOR_ACCENT = BLUE_A
        COLOR_HIGHLIGHT = GOLD_A
        COLOR_PRIMARY_TEXT = WHITE
        COLOR_SECONDARY_TEXT = BLUE_E # Slightly darker blue for connections
        COLOR_ENERGY = YELLOW_D
        COLOR_PRESSURE = RED_E

        # --- Beat 1: The Interconnected Web of Life (Ecology Intro) ---
        title = Text("Ecology: The Web of Life", font_size=50, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create initial scattered dots (organisms)
        num_organisms = 15
        # Place organisms in a grid and then slight randomize their positions for an organic feel
        initial_dots = VGroup(*[Dot(radius=0.12, color=COLOR_ACCENT) for _ in range(num_organisms)])
        initial_dots.arrange_in_grid(rows=3, cols=5, buff=0.8).move_to(ORIGIN)
        
        # Add slight random offset to each dot
        for dot in initial_dots:
            dot.shift(np.random.rand(3)*0.5 - 0.25) # Random shift [-0.25, 0.25] in x,y,z
        
        self.play(LaggedStart(*[FadeIn(o, scale=0.8) for o in initial_dots], lag_ratio=0.07), run_time=1.5)
        self.wait(0.5)

        # Create connections (relationships) - building the "web"
        connections = []
        for _ in range(25): # Number of connections
            start_node = np.random.choice(initial_dots)
            end_node = np.random.choice(initial_dots)
            if start_node != end_node:
                line = Line(start_node.get_center(), end_node.get_center(), color=COLOR_SECONDARY_TEXT, stroke_width=1.5)
                connections.append(line)
        
        web = VGroup(*connections)
        self.play(LaggedStart(*[Create(line) for line in connections], lag_ratio=0.03), run_time=2)
        self.wait(1)

        intro_text = Text(
            "Ecology: relationships between organisms and environment.",
            font_size=30, color=COLOR_PRIMARY_TEXT
        ).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(intro_text, shift=DOWN))
        self.wait(2)
        
        self.play(FadeOut(intro_text), FadeOut(web), FadeOut(initial_dots))
        self.wait(0.5)

        # --- Beat 2: Trophic Levels - Energy Flow Pyramid ---
        self.play(title.animate.become(Text("Trophic Levels: Energy Flow", font_size=50, color=COLOR_HIGHLIGHT).to_edge(UP)))
        self.wait(0.5)

        # Create the pyramid structure using stacked rectangles
        producer_rect = Rectangle(width=6, height=1.5, color=COLOR_HIGHLIGHT, fill_opacity=0.6, stroke_width=2).move_to(DOWN*2.5)
        producer_text = Text("Producers", font_size=30, color=COLOR_PRIMARY_TEXT).move_to(producer_rect.get_center())

        primary_consumer_rect = Rectangle(width=4, height=1.5, color=COLOR_ACCENT, fill_opacity=0.6, stroke_width=2).next_to(producer_rect, UP, buff=0)
        primary_consumer_text = Text("Primary Consumers", font_size=30, color=COLOR_PRIMARY_TEXT).move_to(primary_consumer_rect.get_center())

        secondary_consumer_rect = Rectangle(width=2.2, height=1.5, color=COLOR_GOLD_E, fill_opacity=0.6, stroke_width=2).next_to(primary_consumer_rect, UP, buff=0)
        secondary_consumer_text = Text("Secondary Consumers", font_size=30, color=COLOR_PRIMARY_TEXT).move_to(secondary_consumer_rect.get_center())

        pyramid = VGroup(producer_rect, primary_consumer_rect, secondary_consumer_rect)
        pyramid_labels = VGroup(producer_text, primary_consumer_text, secondary_consumer_text)

        self.play(LaggedStart(*[Create(m) for m in pyramid], lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[Write(m) for m in pyramid_labels], lag_ratio=0.2), run_time=1.5)
        self.wait(1)

        # Show energy flow with diminishing size
        # A larger energy block at the bottom
        energy_block_1 = Rectangle(width=producer_rect.width * 0.9, height=0.2, color=COLOR_ENERGY, fill_opacity=1).move_to(producer_rect.get_center() + DOWN*0.5)
        
        # Arrow indicating flow
        arrow_1 = Arrow(producer_rect.get_top(), primary_consumer_rect.get_bottom(), buff=0.1, color=COLOR_ENERGY, stroke_width=6)
        
        # Energy shrinking for the next level (transformed copy)
        energy_block_2 = Rectangle(width=primary_consumer_rect.width * 0.7, height=0.2, color=COLOR_ENERGY, fill_opacity=1).move_to(primary_consumer_rect.get_center() + DOWN*0.5)
        arrow_2 = Arrow(primary_consumer_rect.get_top(), secondary_consumer_rect.get_bottom(), buff=0.1, color=COLOR_ENERGY, stroke_width=6)

        energy_block_3 = Rectangle(width=secondary_consumer_rect.width * 0.5, height=0.2, color=COLOR_ENERGY, fill_opacity=1).move_to(secondary_consumer_rect.get_center() + DOWN*0.5)

        self.play(Create(energy_block_1), run_time=0.5)
        self.play(
            Create(arrow_1),
            ReplacementTransform(energy_block_1.copy().shift(UP * (producer_rect.height / 2 + primary_consumer_rect.height / 2)), energy_block_2),
            run_time=1
        )
        self.play(
            Create(arrow_2),
            ReplacementTransform(energy_block_2.copy().shift(UP * (primary_consumer_rect.height / 2 + secondary_consumer_rect.height / 2)), energy_block_3),
            run_time=1
        )
        self.wait(1.5)

        self.play(FadeOut(pyramid), FadeOut(pyramid_labels), FadeOut(arrow_1), FadeOut(arrow_2), FadeOut(energy_block_3))
        self.wait(0.5)

        # --- Beat 3: Evolution - Adaptation and Change ---
        self.play(title.animate.become(Text("Evolution: Adaptation & Change", font_size=50, color=COLOR_HIGHLIGHT).to_edge(UP)))
        self.wait(0.5)

        # Represent an initial simple organism (a 'blob' shape)
        initial_organism_points = [
            [-0.8, 0, 0], [-0.4, 0.7, 0], [0.4, 0.7, 0], [0.8, 0, 0],
            [0.4, -0.7, 0], [-0.4, -0.7, 0]
        ]
        initial_organism = Polygon(*initial_organism_points, color=COLOR_ACCENT, fill_opacity=0.7).scale(0.8).move_to(LEFT*3)
        self.play(Create(initial_organism))
        self.wait(0.5)

        # Environmental pressure (e.g., wind, current)
        pressure_arrow = Arrow(start=RIGHT*3 + UP*1.5, end=initial_organism.get_center() + LEFT*0.8, color=COLOR_PRESSURE, buff=0.1, stroke_width=7, tip_length=0.3)
        pressure_text = Text("Pressure (e.g., wind)", font_size=28, color=COLOR_PRESSURE).next_to(pressure_arrow.get_start(), UP)
        
        self.play(Create(pressure_arrow), Write(pressure_text))
        self.wait(1)

        # Organism adapts to become more streamlined (geometric transformation)
        adapted_organism_points = [
            [-1.0, 0, 0], [-0.5, 0.4, 0], [0.5, 0.6, 0], [1.0, 0, 0],
            [0.5, -0.6, 0], [-0.5, -0.4, 0]
        ]
        adapted_organism_shape = Polygon(*adapted_organism_points, color=COLOR_GOLD_A, fill_opacity=0.7).scale(0.7).move_to(LEFT*3)

        self.play(
            Transform(initial_organism, adapted_organism_shape),
            FadeOut(pressure_arrow),
            FadeOut(pressure_text),
            run_time=2
        )
        
        adapt_label = Text("Adaptation over time", font_size=30, color=COLOR_PRIMARY_TEXT).next_to(initial_organism, DOWN)
        self.play(Write(adapt_label))
        self.wait(1.5)
        
        self.play(FadeOut(initial_organism), FadeOut(adapt_label))
        self.wait(0.5)

        # --- Beat 4: Dynamic Ecosystems: Feedback Loops ---
        self.play(title.animate.become(Text("Dynamic Ecosystems: Feedback Loops", font_size=50, color=COLOR_HIGHLIGHT).to_edge(UP)))
        self.wait(0.5)

        # Reintroduce a simplified network of interacting species/elements
        # Using MathTex for labels for a more mathematical feel
        organism_A_label = MathTex("A", font_size=40, color=COLOR_GOLD_A)
        organism_A = Circle(radius=0.4, color=COLOR_GOLD_A, fill_opacity=0.7).move_to(LEFT*3 + UP*1.5).add(organism_A_label)
        organism_A_label.move_to(organism_A.get_center())

        organism_B_label = MathTex("B", font_size=40, color=COLOR_ACCENT)
        organism_B = Circle(radius=0.4, color=COLOR_ACCENT, fill_opacity=0.7).move_to(LEFT*1 + DOWN*1.5).add(organism_B_label)
        organism_B_label.move_to(organism_B.get_center())

        organism_C_label = MathTex("C", font_size=40, color=COLOR_BLUE_E)
        organism_C = Circle(radius=0.4, color=COLOR_BLUE_E, fill_opacity=0.7).move_to(RIGHT*3 + UP*1.5).add(organism_C_label)
        organism_C_label.move_to(organism_C.get_center())

        organism_D_label = MathTex("D", font_size=40, color=COLOR_GREEN_D)
        organism_D = Circle(radius=0.4, color=COLOR_GREEN_D, fill_opacity=0.7).move_to(RIGHT*1 + DOWN*1.5).add(organism_D_label)
        organism_D_label.move_to(organism_D.get_center())

        # Environment represented as a larger encompassing box
        environment_box = Rectangle(width=8, height=5, color=GREY_B, fill_opacity=0.1, stroke_opacity=0.5).move_to(ORIGIN)
        env_label = Text("Environment", font_size=24, color=GREY_B).next_to(environment_box, UP*0.5)

        eco_elements = VGroup(organism_A, organism_B, organism_C, organism_D, environment_box, env_label)
        self.play(Create(environment_box), FadeIn(env_label), LaggedStart(*[FadeIn(o, scale=0.8) for o in [organism_A, organism_B, organism_C, organism_D]], lag_ratio=0.1))
        self.wait(0.5)

        # Show initial relationships with arrows
        rel_AB = Arrow(organism_A.get_center(), organism_B.get_center(), color=COLOR_SECONDARY_TEXT, buff=0.1, tip_length=0.2)
        rel_BC = Arrow(organism_B.get_center(), organism_C.get_center(), color=COLOR_SECONDARY_TEXT, buff=0.1, tip_length=0.2)
        rel_CD = Arrow(organism_C.get_center(), organism_D.get_center(), color=COLOR_SECONDARY_TEXT, buff=0.1, tip_length=0.2)
        rel_DA = Arrow(organism_D.get_center(), organism_A.get_center(), color=COLOR_SECONDARY_TEXT, buff=0.1, tip_length=0.2)
        rel_BD = Arrow(organism_B.get_center(), organism_D.get_center(), color=COLOR_SECONDARY_TEXT, buff=0.1, tip_length=0.2)

        self.play(LaggedStart(*[Create(arr) for arr in [rel_AB, rel_BC, rel_CD, rel_DA, rel_BD]], lag_ratio=0.1), run_time=1.5)
        self.wait(0.5)

        # Show feedback loops: interaction causing change, then effect coming back
        # A affects B
        self.play(Indicate(organism_A), run_time=0.5)
        self.play(rel_AB.animate.set_color(COLOR_HIGHLIGHT).set_stroke(width=4), run_time=0.5)
        self.play(Indicate(organism_B), run_time=0.5)
        self.play(rel_AB.animate.set_color(COLOR_SECONDARY_TEXT).set_stroke(width=2))

        # Environment affects organism, organism affects environment (feedback)
        env_influence_A = Arrow(environment_box.get_left() + LEFT*0.5, organism_A.get_left(), color=COLOR_PRIMARY_TEXT, buff=0.1, stroke_width=3)
        A_influence_env = Arrow(organism_A.get_right(), environment_box.get_right() + RIGHT*0.5, color=COLOR_PRIMARY_TEXT, buff=0.1, stroke_width=3)
        
        self.play(Create(env_influence_A))
        self.wait(0.5)
        self.play(ReplacementTransform(env_influence_A, A_influence_env.copy().set_color(COLOR_HIGHLIGHT)), FadeOut(A_influence_env)) # Show A influencing env
        self.wait(0.5)
        self.play(FadeOut(env_influence_A))
        self.wait(1)

        # Emphasize "dynamic systems"
        dynamic_text = Text("Complex, Evolving Systems", font_size=30, color=COLOR_PRIMARY_TEXT).next_to(environment_box, DOWN, buff=0.5)
        self.play(Write(dynamic_text))
        self.wait(2)

        connections_group = VGroup(rel_AB, rel_BC, rel_CD, rel_DA, rel_BD)
        self.play(FadeOut(connections_group), FadeOut(eco_elements), FadeOut(dynamic_text))
        self.wait(0.5)

        # --- Beat 5: Recap Card ---
        self.play(title.animate.become(Text("Recap", font_size=60, color=COLOR_HIGHLIGHT).to_edge(UP)))
        self.wait(0.5)

        # Recap points
        recap_points = VGroup(
            Text("• Ecology: study of interconnected life.", font_size=35, color=COLOR_ACCENT),
            Text("• Trophic Levels: energy flows UP, decreasing.", font_size=35, color=COLOR_ACCENT),
            Text("• Evolution: organisms adapt to environment over time.", font_size=35, color=COLOR_ACCENT),
            Text("• Ecosystems are dynamic feedback systems.", font_size=35, color=COLOR_ACCENT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8).next_to(title, DOWN, buff=1).shift(LEFT*2) # Shift left for better alignment with bullets
        
        # Use LaggedStart for a nice reveal
        self.play(LaggedStart(*[FadeIn(point, shift=UP*0.5) for point in recap_points], lag_ratio=0.3), run_time=3)
        self.wait(3)

        self.play(FadeOut(VGroup(title, recap_points)))
        self.wait(1)