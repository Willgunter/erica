from manim import *

class EcosystemsAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        BLUE_ACCENT = BLUE_E  # Vibrant blue
        GOLD_ACCENT = GOLD_E  # Rich gold
        TEXT_COLOR = WHITE    # White for general text clarity

        # --- Beat 1: Visual Hook & Introduction ---
        self.camera.background_color = BLACK # Dark background

        # Visual hook: Abstract shapes representing organisms/elements interacting
        shapes = VGroup(
            Circle(radius=0.5, color=BLUE_ACCENT, fill_opacity=0.8).shift(LEFT*2 + UP),
            Square(side_length=1, color=GOLD_ACCENT, fill_opacity=0.8).shift(RIGHT*2 + DOWN),
            Triangle(color=BLUE_ACCENT, fill_opacity=0.8).scale(0.7).shift(UP*1.5 + RIGHT),
            Polygon([-1, -1, 0], [1, -1, 0], [0, 1, 0], color=GOLD_ACCENT, fill_opacity=0.8).scale(0.6).shift(DOWN*1.5 + LEFT)
        )
        
        # A subtle NumberPlane to represent the environment/space
        env_plane = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            x_length=14, y_length=8,
            axis_config={"color": GRAY_A, "stroke_width": 1},
            background_line_style={"stroke_color": GRAY_B, "stroke_width": 0.5, "stroke_opacity": 0.3}
        )
        env_plane.set_opacity(0.1) # Keep it subtle

        title = Text("Ecosystems: A Dance of Interactions", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        intro_text = Text("Ecology explores the interactions...", font_size=36, color=TEXT_COLOR).next_to(title, DOWN, buff=0.8)
        intro_text[0:7].set_color(BLUE_ACCENT) # Highlight 'Ecology'

        self.add(env_plane) # Add the environment plane immediately
        self.play(
            LaggedStart(*[FadeIn(shape, shift=np.random.rand(3)*2 - 1) for shape in shapes]), # Staggered entry for shapes
            run_time=2
        )
        self.play(
            # Animate the shapes moving and changing to show interaction
            shapes[0].animate.shift(RIGHT*1.5 + DOWN*0.5).set_color(GOLD_ACCENT),
            shapes[1].animate.shift(LEFT*1.5 + UP*0.5).set_color(BLUE_ACCENT),
            shapes[2].animate.rotate(PI/2).shift(LEFT*0.5).scale(1.2),
            shapes[3].animate.rotate(-PI/2).shift(RIGHT*0.5).scale(1.2),
            run_time=2
        )
        self.play(
            FadeIn(title, shift=UP),
            FadeIn(intro_text, shift=DOWN)
        )
        self.wait(1.5)

        # --- Beat 2: Biotic Components (Living) ---
        biotic_title_old = intro_text # Old title for transformation
        biotic_title = Text("Biotic Factors: The Living Components", font_size=40, color=GOLD_ACCENT).next_to(title, DOWN, buff=0.8)
        biotic_title[0:6].set_color(BLUE_ACCENT) # Highlight 'Biotic'
        
        self.play(
            ReplacementTransform(biotic_title_old, biotic_title), # Smooth transition of text
            FadeOut(title)
        )
        self.wait(0.5)

        # Represent different types of biotic factors with simple shapes and colors
        producer = Dot(radius=0.3, color=GREEN_E, fill_opacity=1).set_x(-3).set_y(1)
        consumer_herb = Circle(radius=0.4, color=BLUE_ACCENT, fill_opacity=0.8).set_x(-1).set_y(0)
        consumer_carn = Square(side_length=0.7, color=RED_E, fill_opacity=0.8).set_x(1).set_y(1)
        decomposer = Polygon([0,0,0],[0.7,0.3,0],[0,-0.7,0],[-0.7,0.3,0], color=BROWN, fill_opacity=0.8).set_x(3).set_y(-1)
        
        biotic_group = VGroup(producer, consumer_herb, consumer_carn, decomposer)

        # Labels for clarity using MathTex
        prod_label = MathTex("\\text{Producers}", font_size=28, color=TEXT_COLOR).next_to(producer, DOWN)
        herb_label = MathTex("\\text{Herbivores}", font_size=28, color=TEXT_COLOR).next_to(consumer_herb, DOWN)
        carn_label = MathTex("\\text{Carnivores}", font_size=28, color=TEXT_COLOR).next_to(consumer_carn, DOWN)
        decomp_label = MathTex("\\text{Decomposers}", font_size=28, color=TEXT_COLOR).next_to(decomposer, DOWN)
        
        labels_group = VGroup(prod_label, herb_label, carn_label, decomp_label)

        # Transform abstract shapes into specific biotic representations
        self.play(
            LaggedStart(
                Transform(shapes[0], producer),
                Transform(shapes[1], consumer_herb),
                Transform(shapes[2], consumer_carn),
                Transform(shapes[3], decomposer),
                lag_ratio=0.3
            ),
            FadeIn(labels_group, shift=DOWN),
            run_time=2
        )
        self.wait(0.5)

        # Show energy flow using arrows
        arrow1 = Arrow(producer.get_right(), consumer_herb.get_left(), buff=0.1, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1)
        arrow2 = Arrow(consumer_herb.get_right(), consumer_carn.get_left(), buff=0.1, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1)
        arrow3 = Arrow(VGroup(producer, consumer_herb, consumer_carn).get_center(), decomposer.get_center(), buff=1.0, color=GRAY_D, max_tip_length_to_length_ratio=0.1)
        
        energy_flow_label = Text("Energy Flow", font_size=24, color=GOLD_ACCENT).next_to(arrow1, UP, buff=0.1)
        energy_flow_label_g = Text("Decomposition", font_size=24, color=GRAY_D).next_to(arrow3, UP, buff=0.1)

        self.play(
            Create(arrow1), Create(arrow2),
            FadeIn(energy_flow_label),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Create(arrow3),
            FadeIn(energy_flow_label_g),
            run_time=1
        )
        self.wait(1)

        # --- Beat 3: Abiotic Components (Non-Living) ---
        self.play(
            FadeOut(biotic_title),
            FadeOut(labels_group),
            FadeOut(energy_flow_label),
            FadeOut(energy_flow_label_g),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3)
        )
        self.wait(0.2)
        
        abiotic_title = Text("Abiotic Factors: The Non-Living Environment", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        abiotic_title[0:7].set_color(BLUE_ACCENT) # Highlight 'Abiotic'
        self.play(FadeIn(abiotic_title, shift=UP))

        # Re-position biotic elements to one side to make room for abiotic
        self.play(
            biotic_group.animate.shift(LEFT*4).scale(0.7)
        )
        self.wait(0.5)

        # Represent abiotic factors with geometric shapes and relevant colors
        sun = Dot(radius=0.6, color=YELLOW_E, fill_opacity=1).set_x(3).set_y(2.5)
        water = Rectangle(width=4, height=1.5, color=BLUE_ACCENT, fill_opacity=0.6).set_x(3).set_y(-2.5)
        soil = Rectangle(width=4, height=1, color=BROWN_E, fill_opacity=1).set_x(3).set_y(-3.5)
        air = Circle(radius=2.5, color=GREY_B, fill_opacity=0.1).set_x(3).set_y(0).set_stroke(GREY_B, width=1, opacity=0.5) # Representing air as a transparent circle

        sun_label = MathTex("\\text{Sunlight}", font_size=28, color=TEXT_COLOR).next_to(sun, UP)
        water_label = MathTex("\\text{Water}", font_size=28, color=TEXT_COLOR).next_to(water, DOWN)
        soil_label = MathTex("\\text{Soil/Nutrients}", font_size=28, color=TEXT_COLOR).next_to(soil, DOWN)
        air_label = MathTex("\\text{Air/Gases}", font_size=28, color=TEXT_COLOR).next_to(air, UP)

        abiotic_group = VGroup(sun, water, soil, air)
        abiotic_labels_group = VGroup(sun_label, water_label, soil_label, air_label)

        self.play(
            LaggedStart(
                FadeIn(sun, shift=UP),
                FadeIn(water, shift=DOWN),
                FadeIn(soil, shift=DOWN),
                FadeIn(air, scale=0.5),
                lag_ratio=0.2
            ),
            LaggedStart( # Staggered entry for labels
                FadeIn(sun_label), FadeIn(water_label), FadeIn(soil_label), FadeIn(air_label),
                lag_ratio=0.2
            ),
            run_time=2
        )
        self.wait(1.5)

        # --- Beat 4: Ecosystem Emergence ---
        self.play(
            FadeOut(abiotic_title),
            FadeOut(abiotic_labels_group)
        )

        ecosystem_title = Text("Ecosystem: Biotic + Abiotic Interactions", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        ecosystem_title[0:9].set_color(BLUE_ACCENT) # Highlight 'Ecosystem'
        self.play(FadeIn(ecosystem_title, shift=UP))

        # Re-position biotic and abiotic elements closer for interaction visualization
        self.play(
            biotic_group.animate.scale(1/0.7).move_to(LEFT*2 + UP*1), # Reset scale and move to center-left
            abiotic_group.animate.move_to(RIGHT*2 + DOWN*1.5) # Move to center-right
        )
        self.wait(0.5)

        # Show connections: biotic uses abiotic
        conn_arrow1 = Arrow(sun.get_bottom(), biotic_group[0].get_top(), buff=0.1, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1) # Sun to Producer
        conn_arrow2 = Arrow(water.get_top(), biotic_group[0].get_bottom(), buff=0.1, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.1) # Water to Producer
        conn_arrow3 = Arrow(air.get_center(), biotic_group[2].get_center(), buff=0.1, color=GRAY_A, max_tip_length_to_length_ratio=0.1) # Air (gases) to Consumer (e.g., respiration)

        self.play(
            Create(conn_arrow1),
            Create(conn_arrow2),
            Create(conn_arrow3),
            run_time=1.5
        )
        self.wait(1)

        # Formal notation for Ecosystem
        ecosystem_eq = MathTex(
            "\\text{Ecosystem} = \\text{Biotic Components} + \\text{Abiotic Factors}",
            font_size=38, color=TEXT_COLOR
        ).next_to(ecosystem_title, DOWN, buff=0.8)
        ecosystem_eq[0][0:9].set_color(BLUE_ACCENT) # 'Ecosystem'
        ecosystem_eq[0][12:28].set_color(GREEN_E)   # 'Biotic Components'
        ecosystem_eq[0][31:].set_color(YELLOW_E)    # 'Abiotic Factors'

        self.play(
            FadeIn(ecosystem_eq, shift=DOWN)
        )
        self.wait(2)

        # --- Beat 5: Dynamic Systems & Evolutionary Forces Hint ---
        self.play(
            FadeOut(ecosystem_eq),
            FadeOut(ecosystem_title),
            FadeOut(conn_arrow1), FadeOut(conn_arrow2), FadeOut(conn_arrow3),
            biotic_group.animate.scale(0.8).shift(LEFT*1),
            abiotic_group.animate.scale(0.8).shift(RIGHT*1)
        )

        dynamic_title = Text("Dynamic Systems: Constant Change", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        dynamic_title[0:7].set_color(BLUE_ACCENT) # Highlight 'Dynamic'
        self.play(FadeIn(dynamic_title, shift=UP))
        
        # Animate slight changes/flux within the system
        self.play(
            biotic_group[0].animate.scale(1.1).set_color(GREEN_D), # Producer growth/change
            biotic_group[1].animate.shift(UP*0.3).set_color(BLUE_D), # Consumer movement/response
            sun.animate.shift(LEFT*0.2 + UP*0.2), # Sun position shift
            water.animate.set_height(1.8).set_opacity(0.7), # Water level change
            run_time=1.5
        )
        self.wait(0.5)

        evolution_hint = Text(
            "These interactions drive adaptation and evolutionary forces.",
            font_size=32, color=TEXT_COLOR
        ).next_to(dynamic_title, DOWN, buff=0.8)
        evolution_hint[34:54].set_color(GOLD_ACCENT) # Highlight 'evolutionary forces'

        self.play(FadeIn(evolution_hint, shift=DOWN))
        self.wait(2)

        # --- Recap Card ---
        self.play(
            FadeOut(dynamic_title),
            FadeOut(evolution_hint),
            FadeOut(biotic_group),
            FadeOut(abiotic_group),
            FadeOut(env_plane)
        )

        recap_title = Text("Recap: Ecosystem Fundamentals", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(recap_title, shift=UP))

        recap_points = VGroup(
            Text("•  Ecology: Study of organism-environment interactions.", font_size=32, color=TEXT_COLOR).shift(UP*1.5 + LEFT*0.5),
            Text("•  Biotic Factors: Living components (Producers, Consumers, Decomposers).", font_size=32, color=TEXT_COLOR).shift(UP*0.5 + LEFT*0.5),
            Text("•  Abiotic Factors: Non-living components (Sunlight, Water, Soil, Air).", font_size=32, color=TEXT_COLOR).shift(DOWN*0.5 + LEFT*0.5),
            Text("•  Ecosystem: The entire system of interacting biotic & abiotic factors.", font_size=32, color=TEXT_COLOR).shift(DOWN*1.5 + LEFT*0.5)
        )
        # Highlight key terms in the recap
        recap_points[0][3:10].set_color(BLUE_ACCENT) 
        recap_points[1][3:9].set_color(GREEN_E) 
        recap_points[2][3:10].set_color(YELLOW_E) 
        recap_points[3][3:12].set_color(BLUE_ACCENT) 

        self.play(
            LaggedStart(*[FadeIn(point, shift=LEFT) for point in recap_points]),
            lag_ratio=0.3, # Staggered entry for recap points
            run_time=3
        )
        self.wait(3)

        self.play(
            FadeOut(recap_title),
            FadeOut(recap_points)
        )
        self.wait(1)