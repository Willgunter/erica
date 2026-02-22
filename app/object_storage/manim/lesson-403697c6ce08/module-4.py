from manim import *
import random # Needed for random energy particle positions

class TrophicLevels(Scene):
    def construct(self):
        # --- Configuration for 3Blue1Brown style ---
        self.camera.background_color = BLACK
        default_color = WHITE
        accent_blue = BLUE_C # A slightly lighter blue for contrast
        accent_gold = GOLD_A # A slightly darker gold for contrast

        # --- Beat 1: The Foundation - Producers (approx. 8 seconds) ---
        # Visual Hook: Sun and energy flowing to a plant
        sun = Star(n_points=5, outer_radius=0.5, color=YELLOW_E, fill_opacity=1).shift(UP * 3.5 + LEFT * 4)
        sun_rays = VGroup(*[
            Line(sun.get_center(), sun.get_center() + 0.5 * RIGHT * np.cos(angle) + 0.5 * UP * np.sin(angle), color=YELLOW)
            for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False)
        ]).set_stroke(width=2)
        sun_group = VGroup(sun, sun_rays)

        plant_stem = Rectangle(width=0.2, height=1.5, color=GREEN_E, fill_opacity=1).shift(DOWN * 1.5)
        plant_leaves = VGroup(
            Triangle(color=GREEN_E, fill_opacity=1).scale(0.5).move_to(plant_stem.get_top() + LEFT * 0.3),
            Triangle(color=GREEN_E, fill_opacity=1).scale(0.5).move_to(plant_stem.get_top() + RIGHT * 0.3),
            Triangle(color=GREEN_E, fill_opacity=1).scale(0.5).move_to(plant_stem.get_center() + LEFT * 0.4),
            Triangle(color=GREEN_E, fill_opacity=1).scale(0.5).move_to(plant_stem.get_center() + RIGHT * 0.4)
        ).rotate(PI/2)
        plant = VGroup(plant_stem, plant_leaves).shift(DOWN * 0.5 + RIGHT * 4)
        
        self.play(FadeIn(sun_group, run_time=1))
        self.play(Create(plant, run_time=1))

        # Animate energy flowing from sun to plant
        energy_particles = VGroup(*[
            Dot(point=sun.get_center() + random.uniform(-0.3, 0.3) * UP + random.uniform(-0.3, 0.3) * RIGHT, color=YELLOW)
            for _ in range(30)
        ])
        
        self.play(
            LaggedStart(
                *[dot.animate.shift(plant.get_center() - sun.get_center() + UP * 0.5).set_opacity(0) for dot in energy_particles],
                lag_ratio=0.01,
                run_time=2
            )
        )
        self.wait(0.5)

        producer_text_concept = Text("Producers", color=accent_gold).scale(0.8).next_to(plant, UP)
        foundation_text = Text("The Foundation of Life", color=accent_blue).scale(0.6).next_to(producer_text_concept, DOWN)

        self.play(Write(producer_text_concept), Write(foundation_text), FadeOut(sun_group, shift=LEFT), run_time=1.5)
        self.wait(0.5)

        # Transition to generic block representation
        producer_block = Rectangle(width=5, height=1, color=GREEN_E, fill_opacity=0.8).move_to(plant.get_center())
        producer_block_label = Text("Producers", color=WHITE).move_to(producer_block.get_center())
        producer_block_full = VGroup(producer_block, producer_block_label)

        self.play(
            FadeOut(plant, run_time=0.5), # Fade out plant drawing
            Transform(producer_text_concept, producer_block_label), # Transform text label
            FadeOut(foundation_text),
            FadeIn(producer_block, run_time=0.5) # Fade in generic block at plant's original position
        )
        self.wait(0.5)


        # --- Beat 2: Primary Consumers (approx. 8 seconds) ---
        primary_consumer_block = Rectangle(width=4, height=1, color=accent_blue, fill_opacity=0.8)
        primary_consumer_label = Text("Primary Consumers", color=WHITE).move_to(primary_consumer_block.get_center())
        primary_consumer_full = VGroup(primary_consumer_block, primary_consumer_label)

        # Simple herbivore drawing
        herbivore_body = Circle(radius=0.4, color=WHITE, fill_opacity=1)
        herbivore_eyes = VGroup(
            Circle(radius=0.04, color=BLACK, fill_opacity=1).shift(LEFT*0.1 + UP*0.1),
            Circle(radius=0.04, color=BLACK, fill_opacity=1).shift(RIGHT*0.1 + UP*0.1)
        ).move_to(herbivore_body.get_center())
        herbivore = VGroup(herbivore_body, herbivore_eyes).next_to(producer_block, UP, buff=2) # Position above the producer block for the animation

        arrow1 = Arrow(start=producer_block.get_top(), end=herbivore.get_bottom(), color=accent_blue)
        eat_producer_text = Text("Eat Producers", color=accent_blue).scale(0.6).next_to(arrow1, UP, buff=0.1)

        self.play(FadeIn(herbivore, shift=UP), run_time=0.8)
        self.play(Create(arrow1), Write(eat_producer_text), run_time=1.5)
        self.wait(0.5)

        self.play(
            FadeOut(herbivore, shift=UP),
            FadeOut(arrow1),
            FadeOut(eat_producer_text),
            # Transform and position the new block
            primary_consumer_full.animate.next_to(producer_block_full, UP, buff=0.1),
            ReplacementTransform(producer_block_label.copy().move_to(primary_consumer_block.get_center()), primary_consumer_label), # Visual link for text
            FadeIn(primary_consumer_block, shift=UP)
        )
        self.wait(1)

        # --- Beat 3: Secondary Consumers & Energy Loss (approx. 8 seconds) ---
        secondary_consumer_block = Rectangle(width=3, height=1, color=accent_gold, fill_opacity=0.8)
        secondary_consumer_label = Text("Secondary Consumers", color=WHITE).move_to(secondary_consumer_block.get_center())
        secondary_consumer_full = VGroup(secondary_consumer_block, secondary_consumer_label)

        # Simple carnivore drawing
        carnivore_body = Triangle(color=WHITE, fill_opacity=1).scale(0.6)
        carnivore_eyes = VGroup(
            Circle(radius=0.04, color=BLACK, fill_opacity=1).shift(LEFT*0.1 + UP*0.1),
            Circle(radius=0.04, color=BLACK, fill_opacity=1).shift(RIGHT*0.1 + UP*0.1)
        ).move_to(carnivore_body.get_center())
        carnivore = VGroup(carnivore_body, carnivore_eyes).next_to(primary_consumer_block, UP, buff=2)

        arrow2 = Arrow(start=primary_consumer_block.get_top(), end=carnivore.get_bottom(), color=accent_gold)
        eat_primary_text = Text("Eat Primary Consumers", color=accent_blue).scale(0.6).next_to(arrow2, UP, buff=0.1)

        # Visual intuition for energy loss
        lost_energy_dots = VGroup(*[
            Dot(point=primary_consumer_block.get_center() + random.uniform(-1, 1) * RIGHT + random.uniform(-0.3, 0.3) * UP, color=RED_E)
            for _ in range(20)
        ])

        self.play(FadeIn(carnivore, shift=UP), run_time=0.8)
        self.play(
            Create(arrow2),
            Write(eat_primary_text),
            LaggedStart(*[FadeIn(dot, shift=UP*0.5) for dot in lost_energy_dots], lag_ratio=0.01, run_time=1.5)
        )
        self.wait(0.5)

        self.play(
            FadeOut(carnivore, shift=UP),
            FadeOut(arrow2),
            FadeOut(eat_primary_text),
            LaggedStart(*[FadeOut(dot, shift=UP*0.5) for dot in lost_energy_dots], lag_ratio=0.01, run_time=1),
            # Transform and position the new block
            secondary_consumer_full.animate.next_to(primary_consumer_full, UP, buff=0.1),
            ReplacementTransform(primary_consumer_label.copy().move_to(secondary_consumer_block.get_center()), secondary_consumer_label),
            FadeIn(secondary_consumer_block, shift=UP)
        )
        
        trophic_levels_title = Text("Trophic Levels", color=accent_gold).scale(0.9).to_edge(UP).shift(LEFT*3)
        self.play(Write(trophic_levels_title), run_time=1)
        self.wait(1)

        # --- Beat 4: The 10% Rule (approx. 8 seconds) ---
        all_blocks_current = VGroup(producer_block_full, primary_consumer_full, secondary_consumer_full)
        self.play(all_blocks_current.animate.center().to_edge(LEFT).shift(RIGHT*2), run_time=1)

        energy_100 = MathTex("100\%", color=WHITE).next_to(producer_block, LEFT, buff=0.5)
        energy_10 = MathTex("10\%", color=WHITE).next_to(primary_consumer_block, LEFT, buff=0.5)
        energy_1 = MathTex("1\%", color=WHITE).next_to(secondary_consumer_block, LEFT, buff=0.5)

        arrow_up1 = Arrow(start=producer_block.get_top(), end=primary_consumer_block.get_bottom(), color=WHITE)
        arrow_up2 = Arrow(start=primary_consumer_block.get_top(), end=secondary_consumer_block.get_bottom(), color=WHITE)
        
        rule_text = MathTex("\\approx 10\% \\text{ transferred}", color=accent_blue).scale(0.7).next_to(all_blocks_current, RIGHT, buff=1).shift(UP*0.5)
        lost_text = MathTex("90\% \\text{ lost as heat}", color=RED_E).scale(0.7).next_to(rule_text, DOWN, buff=0.3)

        self.play(
            Write(energy_100),
            Create(arrow_up1),
            Write(rule_text),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Write(energy_10),
            Write(lost_text),
            Create(arrow_up2),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Write(energy_1), run_time=0.8)
        self.wait(1)

        # --- Beat 5: The Energy Pyramid (approx. 8 seconds) ---
        energy_pyramid_title = Text("Energy Pyramid", color=accent_gold).scale(0.9).to_edge(UP).shift(RIGHT*3)

        # Fade out previous elements for clarity
        self.play(
            FadeOut(trophic_levels_title),
            FadeOut(rule_text),
            FadeOut(lost_text),
            FadeOut(arrow_up1),
            FadeOut(arrow_up2),
            run_time=1
        )
        
        # Animate blocks to adjust width and form pyramid
        # The labels and energy percentages will move with their respective blocks
        self.play(
            secondary_consumer_block.animate.set(width=2.5),
            primary_consumer_block.animate.set(width=4).next_to(secondary_consumer_block, DOWN, buff=0.1),
            producer_block.animate.set(width=6).next_to(primary_consumer_block, DOWN, buff=0.1),
            secondary_consumer_label.animate.move_to(secondary_consumer_block.get_center()),
            primary_consumer_label.animate.move_to(primary_consumer_block.get_center()),
            producer_block_label.animate.move_to(producer_block.get_center()),
            energy_1.animate.next_to(secondary_consumer_block, LEFT, buff=0.5),
            energy_10.animate.next_to(primary_consumer_block, LEFT, buff=0.5),
            energy_100.animate.next_to(producer_block, LEFT, buff=0.5),
            run_time=1.5
        )
        
        # Group the adjusted blocks and their labels for final pyramid positioning
        final_pyramid = VGroup(
            VGroup(secondary_consumer_block, secondary_consumer_label, energy_1),
            VGroup(primary_consumer_block, primary_consumer_label, energy_10),
            VGroup(producer_block, producer_block_label, energy_100)
        ).center() # Center the entire pyramid on the screen
        
        self.play(
            Write(energy_pyramid_title, run_time=1)
        )

        less_energy_text = Text("Less energy at higher levels", color=accent_blue).scale(0.6).next_to(final_pyramid, DOWN, buff=0.5)
        self.play(Write(less_energy_text), run_time=1)
        self.wait(2)

        # --- Recap Card (approx. 5 seconds) ---
        self.play(
            FadeOut(final_pyramid, shift=DOWN),
            FadeOut(energy_pyramid_title),
            FadeOut(less_energy_text),
            run_time=1
        )

        recap_title = Text("Recap:", color=accent_gold).scale(1).to_edge(UP)
        recap_points = VGroup(
            Text("• Producers: Convert light/chemical energy.", color=default_color).scale(0.7),
            Text("• Consumers: Eat other organisms for energy.", color=default_color).scale(0.7),
            Text("• Trophic Levels: Steps in an ecosystem's food chain.", color=default_color).scale(0.7),
            Text("• 10% Rule: Only ~10% of energy transfers to the next level.", color=default_color).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(recap_title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(point, shift=UP*0.5) for point in recap_points], lag_ratio=0.15, run_time=3))
        self.wait(3)
        self.play(FadeOut(recap_title, shift=UP), FadeOut(recap_points, shift=UP), run_time=1)
        self.wait(1)