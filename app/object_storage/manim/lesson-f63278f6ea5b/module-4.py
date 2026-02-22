from manim import *

# Define custom colors for a 3Blue1Brown-inspired style
BLUE_ACCENT = ManimColor("#83D8FF") # Lighter blue for highlights
GOLD_ACCENT = ManimColor("#FFD700") # Gold for emphasis
GREEN_PRODUCER = ManimColor("#6B8E23") # Olive green for plants/producers
BLUE_CONSUMER = ManimColor("#4682B4") # Steel blue for primary consumers
RED_CARNIVORE = ManimColor("#B22222") # Firebrick red for secondary consumers
PURPLE_APEX = ManimColor("#800080") # Royal purple for tertiary/apex consumers

class EcosystemAnimation(Scene):
    def construct(self):
        # 1. Scene Setup & Title Hook
        self.camera.background_color = BLACK

        title = Text("Ecosystems, Trophic Levels, & Selection", font_size=50, color=GOLD_ACCENT)
        underline = Line(LEFT * 4, RIGHT * 4, color=BLUE_ACCENT).next_to(title, DOWN, buff=0.2)
        
        self.play(Write(title), Create(underline))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(underline))
        self.wait(0.5)

        # Beat 1: The Sun & Producers (Energy Source)
        sun = Circle(radius=0.8, color=GOLD_ACCENT, fill_opacity=1).shift(UP * 2.5 + LEFT * 4)
        sun_text = MathTex(r"\text{Sunlight}", color=GOLD_ACCENT).next_to(sun, UP, buff=0.1)

        producer_rects = VGroup(*[
            Rectangle(width=0.8, height=0.5, color=GREEN_PRODUCER, fill_opacity=0.8)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.8).shift(DOWN * 2 + LEFT * 0.5)

        producer_label = MathTex(r"\text{Producers}", color=GREEN_PRODUCER).next_to(producer_rects, DOWN, buff=0.5)

        self.play(
            FadeIn(sun, shift=UP),
            Write(sun_text),
            LaggedStart(*[GrowFromCenter(rect) for rect in producer_rects], lag_ratio=0.1),
            FadeIn(producer_label, shift=DOWN)
        )
        self.wait(0.5)

        sun_arrows = VGroup()
        for rect in producer_rects:
            arrow = Arrow(start=sun.get_bottom(), end=rect.get_top(), buff=0.1, color=GOLD_ACCENT, stroke_width=2)
            sun_arrows.add(arrow)
        
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in sun_arrows], lag_ratio=0.1))
        self.wait(1)
        
        # Beat 2: Primary Consumers
        primary_consumer_circles = VGroup(*[
            Circle(radius=0.3, color=BLUE_CONSUMER, fill_opacity=0.8)
            for _ in range(3)
        ]).arrange(RIGHT, buff=2).next_to(producer_rects, UP, buff=0.5)
        primary_consumer_label = MathTex(r"\text{Primary Consumers}", color=BLUE_CONSUMER).next_to(primary_consumer_circles, UP, buff=0.5)

        self.play(
            LaggedStart(*[GrowFromCenter(circle) for circle in primary_consumer_circles], lag_ratio=0.1),
            FadeIn(primary_consumer_label, shift=UP)
        )
        self.wait(0.5)

        producer_to_pc_arrows = VGroup()
        producer_map = {0: [0, 1], 1: [2], 2: [3, 4]} # Map consumers to producers below
        for i, pc_circle in enumerate(primary_consumer_circles):
            for idx in producer_map[i]:
                arrow = Arrow(start=producer_rects[idx].get_top(), end=pc_circle.get_bottom(), buff=0.1, color=BLUE_ACCENT, stroke_width=2)
                producer_to_pc_arrows.add(arrow)
        
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in producer_to_pc_arrows], lag_ratio=0.1))
        self.wait(1)

        # Beat 3: Secondary and Tertiary Consumers (Building the Food Chain)
        secondary_consumer_triangles = VGroup(*[
            Triangle(color=RED_CARNIVORE, fill_opacity=0.8).set(width=0.5)
            for _ in range(2)
        ]).arrange(RIGHT, buff=3).next_to(primary_consumer_circles, UP, buff=0.5).shift(LEFT*1)
        secondary_consumer_label = MathTex(r"\text{Secondary Consumers}", color=RED_CARNIVORE).next_to(secondary_consumer_triangles, UP, buff=0.5)

        self.play(
            LaggedStart(*[GrowFromCenter(tri) for tri in secondary_consumer_triangles], lag_ratio=0.1),
            FadeIn(secondary_consumer_label, shift=UP)
        )
        self.wait(0.5)

        pc_to_sc_arrows = VGroup()
        pc_map = {0: [0], 1: [1, 2]}
        for i, sc_tri in enumerate(secondary_consumer_triangles):
            for idx in pc_map[i]:
                arrow = Arrow(start=primary_consumer_circles[idx].get_top(), end=sc_tri.get_bottom(), buff=0.1, color=RED_CARNIVORE, stroke_width=2)
                pc_to_sc_arrows.add(arrow)
        
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in pc_to_sc_arrows], lag_ratio=0.1))
        self.wait(1)

        tertiary_consumer_star = Star(n=5, outer_radius=0.4, inner_radius=0.2, color=PURPLE_APEX, fill_opacity=0.8).next_to(secondary_consumer_triangles, UP, buff=0.5).shift(RIGHT*0.5)
        tertiary_consumer_label = MathTex(r"\text{Tertiary Consumers}", color=PURPLE_APEX).next_to(tertiary_consumer_star, UP, buff=0.5)

        self.play(
            GrowFromCenter(tertiary_consumer_star),
            FadeIn(tertiary_consumer_label, shift=UP)
        )
        self.wait(0.5)

        sc_to_tc_arrow = Arrow(start=secondary_consumer_triangles[1].get_top(), end=tertiary_consumer_star.get_bottom(), buff=0.1, color=PURPLE_APEX, stroke_width=2)
        self.play(GrowArrow(sc_to_tc_arrow))
        self.wait(1)

        # Group all organisms and labels
        all_organisms = VGroup(
            producer_rects, primary_consumer_circles, secondary_consumer_triangles, tertiary_consumer_star
        )
        all_labels = VGroup(
            producer_label, primary_consumer_label, secondary_consumer_label, tertiary_consumer_label
        )
        all_arrows = VGroup(
            sun_arrows, producer_to_pc_arrows, pc_to_sc_arrows, sc_to_tc_arrow
        )
        
        # Beat 4: Energy Flow & Pyramid (Intuition)
        self.play(
            FadeOut(sun_text), FadeOut(sun), FadeOut(all_arrows), 
            LaggedStartMap(FadeOut, all_labels),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Prepare pyramid levels as rectangles
        pyramid_base = Rectangle(width=8, height=1.2, color=GREEN_PRODUCER, fill_opacity=0.7).move_to(DOWN*2)
        pyramid_level2 = Rectangle(width=6, height=1.0, color=BLUE_CONSUMER, fill_opacity=0.7).next_to(pyramid_base, UP, buff=0)
        pyramid_level3 = Rectangle(width=4, height=0.8, color=RED_CARNIVORE, fill_opacity=0.7).next_to(pyramid_level2, UP, buff=0)
        pyramid_level4 = Rectangle(width=2, height=0.6, color=PURPLE_APEX, fill_opacity=0.7).next_to(pyramid_level3, UP, buff=0)

        pyramid_labels = VGroup(
            MathTex(r"\text{Producers (100%)}", color=WHITE).move_to(pyramid_base),
            MathTex(r"\text{Primary Consumers (10%)}", color=WHITE).move_to(pyramid_level2),
            MathTex(r"\text{Secondary Consumers (1%)}", color=WHITE).move_to(pyramid_level3),
            MathTex(r"\text{Tertiary Consumers (0.1%)}", color=WHITE).move_to(pyramid_level4),
        )
        # Adjust label colors for better contrast on the colored pyramid
        pyramid_labels[0].set_color(BLACK)
        pyramid_labels[1].set_color(BLACK)

        energy_flow_text = Text("Energy Decreases Up Each Level", font_size=35, color=GOLD_ACCENT).shift(UP*3.5)

        self.play(
            ReplacementTransform(producer_rects, pyramid_base),
            ReplacementTransform(primary_consumer_circles, pyramid_level2),
            ReplacementTransform(secondary_consumer_triangles, pyramid_level3),
            ReplacementTransform(tertiary_consumer_star, pyramid_level4),
            Write(energy_flow_text)
        )
        self.wait(0.5)

        self.play(
            LaggedStart(*[FadeIn(label, shift=UP) for label in pyramid_labels], lag_ratio=0.1)
        )
        self.wait(2)

        self.play(
            FadeOut(VGroup(pyramid_base, pyramid_level2, pyramid_level3, pyramid_level4)),
            FadeOut(pyramid_labels),
            FadeOut(energy_flow_text),
            run_time=1.5
        )
        self.wait(0.5)

        # Beat 5: Selection
        selection_title = Text("Selection", font_size=45, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(selection_title))

        population_size = 10
        organisms = VGroup()
        for i in range(population_size):
            radius = 0.2 + np.random.rand() * 0.1 # Slight size variation
            # Slight color variation around a base hue (e.g., blueish-green for primary consumers)
            hue_variation = 0.5 + (np.random.rand() - 0.5) * 0.1 # centered around blueish hue
            organism = Circle(radius=radius, color=ManimColor.from_hsv(hue_variation, 0.8, 0.8), fill_opacity=0.8)
            organisms.add(organism)
        
        organisms.arrange_in_grid(rows=2, cols=5, buff=0.7).shift(UP*0.5)

        pressure_text = MathTex(r"\text{Environmental Pressure}", color=RED_CARNIVORE).shift(DOWN*2.5)
        
        self.play(
            LaggedStart(*[GrowFromCenter(org) for org in organisms], lag_ratio=0.05),
            FadeIn(pressure_text, shift=DOWN)
        )
        self.wait(1)

        # Simulate selection: some organisms "survive" (thrive), others "perish" (fade out)
        survivors_indices = [0, 2, 5, 8, 9] 
        survivors = VGroup(*[organisms[i] for i in survivors_indices])
        non_survivors = VGroup(*[organisms[i] for i in range(population_size) if i not in survivors_indices])

        survivor_traits_text = MathTex(r"\text{Favorable Traits}", color=BLUE_ACCENT).scale(0.8).next_to(survivors, DOWN, buff=0.5)

        self.play(
            LaggedStartMap(FadeOut, non_survivors, shift=DOWN),
            LaggedStartMap(WiggleOutThenIn, survivors, lag_ratio=0.2), # Survivors show resilience
            FadeIn(survivor_traits_text)
        )
        self.wait(1.5)

        # Show the "next generation" (new organisms based on survivors)
        next_gen_organisms = VGroup()
        for survivor in survivors:
            for _ in range(np.random.randint(1, 3)): # Each survivor has 1-2 offspring
                offspring_radius = survivor.get_width() / 2 + (np.random.rand() - 0.5) * 0.05
                offspring_color = survivor.get_fill_color()
                new_org = Circle(radius=offspring_radius, color=offspring_color, fill_opacity=0.8)
                next_gen_organisms.add(new_org)
        
        next_gen_organisms.arrange_in_grid(rows=2, cols=len(next_gen_organisms)//2 + (len(next_gen_organisms)%2), buff=0.7).move_to(organisms.get_center())
        
        self.play(
            FadeOut(organisms),
            TransformMatchingTex(survivor_traits_text, MathTex(r"\text{Population Adapts}", color=GOLD_ACCENT).scale(0.8).move_to(survivor_traits_text.get_center())),
            FadeOut(pressure_text),
            FadeIn(next_gen_organisms.shift(DOWN*0.5))
        )
        self.wait(2)

        self.play(
            FadeOut(selection_title),
            FadeOut(next_gen_organisms),
            FadeOut(survivor_traits_text),
            run_time=1.5
        )
        self.wait(0.5)

        # 8. Recap Card
        recap_title = Text("Key Takeaways", font_size=45, color=GOLD_ACCENT).to_edge(UP)
        
        recap_points = VGroup(
            MathTex(r"\text{Ecosystems: Interacting life + environment}", color=BLUE_ACCENT),
            MathTex(r"\text{Trophic Levels: Hierarchy of energy flow}", color=GOLD_ACCENT),
            MathTex(r"\text{Selection: Environment shapes evolution}", color=BLUE_ACCENT)
        ).arrange(DOWN, buff=0.8).next_to(recap_title, DOWN, buff=1)

        self.play(
            Write(recap_title),
            LaggedStart(*[FadeIn(point, shift=LEFT) for point in recap_points], lag_ratio=0.3)
        )
        self.wait(3)
        self.play(FadeOut(VGroup(recap_title, recap_points)))
        self.wait(0.5)