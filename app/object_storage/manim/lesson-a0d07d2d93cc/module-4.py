from manim import *

class EcologicalRolesAndNaturalSelection(Scene):
    def construct(self):
        # 1. Setup: Clean dark background with high-contrast blue and gold accents
        self.camera.background_color = BLACK
        
        # Define custom colors
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_C
        GREEN_PRODUCER = GREEN_C
        BROWN_DECOMPOSER = BROWN_D
        RED_PRESSURE = RED_C # For subtle hints of pressure/competition

        # --- Module Title ---
        title = Text("Ecological Roles & Natural Selection", font_size=50, color=WHITE).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        # --- BEAT 1: Ecosystem Introduction (Visual Hook & Energy Flow) ---
        # Strong visual hook: Random dots (organisms) forming an interconnected system
        ecosystem_intro_text = Text("Ecosystems: Interactions & Energy Flow", font_size=36, color=WHITE).next_to(title, DOWN, buff=0.7)
        
        # Initial chaotic state of 'organisms'
        num_initial_organisms = 80
        initial_organisms = VGroup(*[
            Dot(point=np.random.rand(3)*7 - 3.5, radius=0.08, color=GOLD_ACCENT).set_opacity(0.8) 
            for _ in range(num_initial_organisms)
        ])
        
        self.play(
            LaggedStart(*[FadeIn(dot, shift=UP*np.random.rand()) for dot in initial_organisms], lag_ratio=0.01),
            FadeIn(ecosystem_intro_text, shift=DOWN),
            run_time=2
        )
        self.wait(1)

        # Connect them to form a system, representing interactions and energy flow
        energy_lines = VGroup()
        for i in range(num_initial_organisms // 4): # Connect a subset to show emerging structure
            d1 = initial_organisms[np.random.randint(0, num_initial_organisms)]
            d2 = initial_organisms[np.random.randint(0, num_initial_organisms)]
            line = Line(d1.get_center(), d2.get_center(), color=BLUE_ACCENT, stroke_width=1).set_opacity(0.6)
            energy_lines.add(line)
        
        # Add some directional flow with arrows
        arrows = VGroup()
        for i in range(num_initial_organisms // 8):
            d1 = initial_organisms[np.random.randint(0, num_initial_organisms)]
            d2 = initial_organisms[np.random.randint(0, num_initial_organisms)]
            arrow = Arrow(d1.get_center(), d2.get_center(), color=BLUE_ACCENT, stroke_width=2, 
                          max_stroke_width_to_length_ratio=0.05, max_tip_length_to_length_ratio=0.2).set_opacity(0.7)
            arrows.add(arrow)

        self.play(
            Create(energy_lines, run_time=1.5),
            Create(arrows, run_time=1.5),
            initial_organisms.animate.shift(LEFT*0.5).scale(0.8), # slight transformation
            run_time=2
        )
        self.wait(1.5)

        self.play(
            FadeOut(energy_lines, shift=DOWN),
            FadeOut(arrows, shift=DOWN),
            FadeOut(initial_organisms, shift=UP),
            FadeOut(ecosystem_intro_text, shift=UP)
        )
        self.wait(0.5)

        # --- BEAT 2: Ecological Roles (Producers, Consumers, Decomposers) ---
        roles_text = Text("Ecological Roles: Producers, Consumers, Decomposers", font_size=36, color=WHITE).next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(roles_text, shift=DOWN))

        # Producers (base of the energy chain, often plants)
        sun = Circle(radius=0.5, color=GOLD_ACCENT, fill_opacity=1).move_to(LEFT * 4 + UP * 2.5)
        producer_group = VGroup()
        for i in range(5):
            producer_group.add(Dot(color=GREEN_PRODUCER, radius=0.15).move_to(LEFT*2.5 + DOWN*1.5 + RIGHT*i*0.8))
        producer_label = Text("Producers", font_size=24, color=GREEN_PRODUCER).next_to(producer_group, DOWN, buff=0.2)
        
        energy_from_sun = Arrow(sun.get_right(), producer_group.get_center() + UP*0.5, color=GOLD_ACCENT, buff=0.1, max_stroke_width_to_length_ratio=0.05, max_tip_length_to_length_ratio=0.2)
        
        self.play(FadeIn(sun), FadeIn(producer_group), FadeIn(producer_label), Create(energy_from_sun))
        self.wait(0.8)

        # Consumers (eat producers or other consumers)
        consumer_group = VGroup()
        for i in range(3):
            consumer_group.add(Dot(color=BLUE_ACCENT, radius=0.15).move_to(LEFT*2 + UP*0.5 + RIGHT*i*1))
        consumer_label = Text("Consumers", font_size=24, color=BLUE_ACCENT).next_to(consumer_group, DOWN, buff=0.2)
        
        energy_to_consumers = VGroup()
        for p_dot in producer_group:
            c_dot = consumer_group[np.random.randint(0, len(consumer_group))]
            energy_to_consumers.add(Arrow(p_dot.get_top(), c_dot.get_bottom(), color=BLUE_ACCENT, buff=0.1, max_stroke_width_to_length_ratio=0.05, max_tip_length_to_length_ratio=0.2))

        self.play(FadeIn(consumer_group), FadeIn(consumer_label), Create(energy_to_consumers))
        self.wait(0.8)

        # Decomposers (break down dead matter)
        decomposer_group = VGroup()
        for i in range(4):
            decomposer_group.add(Dot(color=BROWN_DECOMPOSER, radius=0.15).move_to(RIGHT*3 + DOWN*1.5 + LEFT*i*0.8))
        decomposer_label = Text("Decomposers", font_size=24, color=BROWN_DECOMPOSER).next_to(decomposer_group, DOWN, buff=0.2)

        energy_to_decomposers = VGroup()
        # From producers
        for p_dot in producer_group:
            d_dot = decomposer_group[np.random.randint(0, len(decomposer_group))]
            energy_to_decomposers.add(Arrow(p_dot.get_bottom(), d_dot.get_top(), color=BROWN_DECOMPOSER, buff=0.1, max_stroke_width_to_length_ratio=0.05, max_tip_length_to_length_ratio=0.2))
        # From consumers
        for c_dot in consumer_group:
            d_dot = decomposer_group[np.random.randint(0, len(decomposer_group))]
            energy_to_decomposers.add(Arrow(c_dot.get_bottom(), d_dot.get_top(), color=BROWN_DECOMPOSER, buff=0.1, max_stroke_width_to_length_ratio=0.05, max_tip_length_to_length_ratio=0.2))

        self.play(FadeIn(decomposer_group), FadeIn(decomposer_label), Create(energy_to_decomposers))
        self.wait(1.5)
        
        all_roles_mobjects = VGroup(sun, producer_group, producer_label, energy_from_sun,
                                    consumer_group, consumer_label, energy_to_consumers,
                                    decomposer_group, decomposer_label, energy_to_decomposers)
        self.play(FadeOut(all_roles_mobjects), FadeOut(roles_text, shift=UP))
        self.wait(0.5)

        # --- BEAT 3: Variation and Competition ---
        variation_text = Text("Variation & Competition", font_size=36, color=WHITE).next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(variation_text, shift=DOWN))

        # Represent a population with inherent variation (e.g., size, shape, 'fitness')
        population = VGroup()
        num_pop_members = 40
        for i in range(num_pop_members):
            size_factor = 0.5 + 0.8 * np.random.rand() # Vary size
            # Mix of circles and ellipses to show shape variation
            if np.random.rand() < 0.5: 
                member = Circle(radius=0.1 * size_factor, color=GOLD_ACCENT, fill_opacity=0.8)
            else:
                aspect_ratio = 0.7 + 0.6 * np.random.rand() 
                member = Ellipse(width=0.15 * size_factor, height=0.15 * size_factor * aspect_ratio, color=GOLD_ACCENT, fill_opacity=0.8)

            member.move_to(np.array([
                np.random.uniform(-4, 4),
                np.random.uniform(-2, 2),
                0
            ]))
            population.add(member)
        
        self.play(LaggedStart(*[FadeIn(p) for p in population], lag_ratio=0.02))
        self.wait(1)

        # Introduce limited resources / competition as an abstract 'resource zone'
        resource_zone = Rectangle(width=4, height=3, color=BLUE_ACCENT, fill_opacity=0.2, stroke_opacity=0.8).move_to(LEFT*1.5 + DOWN*0.5)
        resource_label = Text("Limited Resources", font_size=24, color=BLUE_ACCENT).next_to(resource_zone, DOWN, buff=0.2)
        
        self.play(FadeIn(resource_zone), FadeIn(resource_label))
        self.wait(1)

        # Animate some organisms 'competing' or trying to reach resources
        animations = []
        for i, member in enumerate(population):
            target_pos = member.get_center() # Default: no change
            if resource_zone.is_inside(member.get_center()):
                # Already in, maybe jiggle slightly (thriving)
                target_pos += np.random.rand(3)*0.05 - 0.025
            elif i % 4 == 0: # Some 'successful' ones move into the zone
                target_pos = resource_zone.get_center() + np.random.rand(3)*0.5 - 0.25 # Random spot within zone
            else: # Others 'fail' or move away slightly (less successful)
                target_pos += np.random.rand(3)*0.2 + DOWN*0.1 # Small drift away

            animations.append(member.animate.move_to(target_pos))
        
        self.play(LaggedStart(*animations, lag_ratio=0.01), run_time=2)
        self.wait(1)
        
        self.play(
            FadeOut(population), 
            FadeOut(resource_zone), 
            FadeOut(resource_label), 
            FadeOut(variation_text, shift=UP)
        )
        self.wait(0.5)

        # --- BEAT 4: Natural Selection (The "Filter" / "Transformation") ---
        selection_text = Text("Natural Selection", font_size=36, color=WHITE).next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(selection_text, shift=DOWN))

        # Represent traits on an Axes (like a linear algebra coordinate space)
        axes = Axes(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=8, y_length=6,
            axis_config={"color": GRAY_D, "stroke_width": 1},
            tips=False
        ).scale(0.8).shift(DOWN*0.5)
        
        x_label = axes.get_x_axis_label(MathTex(r"\text{Trait A}", color=WHITE), edge=RIGHT, direction=RIGHT, buff=0.4)
        y_label = axes.get_y_axis_label(MathTex(r"\text{Trait B}", color=WHITE), edge=UP, direction=UP, buff=0.4)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))
        self.wait(0.5)

        # Population of individuals, each a point representing a combination of traits
        trait_population = VGroup()
        for _ in range(50):
            x = np.random.normal(0, 1.5) # Gaussian distribution around center for traits
            y = np.random.normal(0, 1.0)
            dot = Dot(point=axes.c2p(x, y), radius=0.07, color=GOLD_ACCENT, fill_opacity=0.8)
            trait_population.add(dot)
        
        self.play(LaggedStart(*[FadeIn(d) for d in trait_population], lag_ratio=0.01))
        self.wait(1)

        # Introduce environmental pressure / selection as a 'favorable traits' region
        fit_region = Rectangle(width=3, height=2, color=BLUE_ACCENT, fill_opacity=0.2, stroke_opacity=0.8).move_to(axes.c2p(1.5, 0.5))
        fit_label = Text("Favorable Traits", font_size=24, color=BLUE_ACCENT).next_to(fit_region, UP, buff=0.2)
        
        self.play(FadeIn(fit_region), FadeIn(fit_label))
        self.wait(1)

        # Natural Selection in action: "filter" out less fit individuals
        survivors = VGroup()
        extinct = VGroup()
        for dot in trait_population:
            if fit_region.is_inside(dot.get_center()):
                survivors.add(dot)
            else:
                extinct.add(dot)
        
        # Animate the 'selection' (less fit fade out)
        self.play(FadeOut(extinct, run_time=1.5), 
                  survivors.animate.set_color(GREEN_PRODUCER).set_opacity(1).scale(1.2), # Favorable traits glow
                  run_time=1.5)
        self.wait(1)

        # Show reproduction/adaptation: survivors multiply and shift the population's trait distribution
        reproduced_population = VGroup()
        for survivor in survivors:
            for _ in range(np.random.randint(1, 4)): # Each survivor has 1-3 offspring
                # Offspring are slightly varied around parent's traits (mutation/recombination)
                offspring_x = axes.p2c(survivor.get_center())[0] + np.random.normal(0, 0.08)
                offspring_y = axes.p2c(survivor.get_center())[1] + np.random.normal(0, 0.08)
                offspring = Dot(point=axes.c2p(offspring_x, offspring_y), radius=0.07, color=GREEN_PRODUCER, fill_opacity=0.8)
                reproduced_population.add(offspring)

        # Geometric transformation: original survivors transform into a new, larger generation
        self.play(FadeOut(survivors), LaggedStart(*[FadeIn(d) for d in reproduced_population], lag_ratio=0.01), run_time=2)
        self.wait(1.5)

        self.play(
            FadeOut(reproduced_population), FadeOut(fit_region), FadeOut(fit_label), 
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label), 
            FadeOut(selection_text, shift=UP)
        )
        self.wait(0.5)

        # --- BEAT 5: Recap Card ---
        self.play(FadeOut(title)) # Fade out main title to make room for recap
        
        recap_title = Text("Recap", font_size=48, color=WHITE).to_edge(UP)
        bullet_list = BulletedList(
            "Ecosystems: Interconnected life & environment.",
            "Ecological Roles: Specialized functions (Producers, Consumers, Decomposers).",
            "Variation: Differences among individuals.",
            "Competition: For limited resources.",
            "Natural Selection: Favorable traits increase survival & reproduction.",
            font_size=32,
            color=WHITE
        ).scale(0.8).next_to(recap_title, DOWN, buff=0.5).to_edge(LEFT, buff=1)

        self.play(FadeIn(recap_title))
        self.play(LaggedStart(*[FadeIn(item, shift=LEFT) for item in bullet_list], lag_ratio=0.5))
        self.wait(4)
        self.play(FadeOut(recap_title), FadeOut(bullet_list))
        self.wait(1)