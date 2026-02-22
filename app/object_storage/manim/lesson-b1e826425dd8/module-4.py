from manim import *

class EcologyAnimation(Scene):
    def construct(self):
        # 1. Configuration: Dark background, high-contrast colors
        self.camera.background_color = BLACK
        BLUE_ACCENT = BLUE_C 
        GOLD_ACCENT = GOLD_A 

        # --- BEAT 1: Visual Hook & Introduction to Interactions ---
        # Pacing: ~10 seconds

        # Hook: Abstract representation of interacting entities
        organism_A = Dot(point=LEFT * 3 + UP * 1, radius=0.3, color=BLUE_ACCENT)
        organism_B = Dot(point=RIGHT * 3 + DOWN * 1, radius=0.3, color=GOLD_ACCENT)
        organism_C = Dot(point=LEFT * 1 + DOWN * 2, radius=0.3, color=WHITE)
        organism_group = VGroup(organism_A, organism_B, organism_C)

        # Initial subtle movement and interaction lines (vectors of influence)
        interaction_AB = Arrow(organism_A.get_center(), organism_B.get_center(), buff=0.3, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1)
        interaction_BC = Arrow(organism_B.get_center(), organism_C.get_center(), buff=0.3, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.1)
        interaction_CA = Arrow(organism_C.get_center(), organism_A.get_center(), buff=0.3, color=WHITE, max_tip_length_to_length_ratio=0.1)
        
        interaction_group = VGroup(interaction_AB, interaction_BC, interaction_CA)

        self.play(
            FadeIn(organism_group, shift=UP),
            LaggedStart(
                Create(interaction_AB),
                Create(interaction_BC),
                Create(interaction_CA),
                lag_ratio=0.5
            ),
            run_time=2
        )

        # Dynamic movement, showing constant interaction
        self.play(
            organism_A.animate.shift(RIGHT * 0.5 + DOWN * 0.5),
            organism_B.animate.shift(LEFT * 0.5 + UP * 0.5),
            organism_C.animate.shift(RIGHT * 0.5 + UP * 0.5),
            UpdateFromFunc(interaction_AB, lambda m: m.become(Arrow(organism_A.get_center(), organism_B.get_center(), buff=0.3, color=GOLD_ACCENT, max_tip_length_to_length_ratio=0.1))),
            UpdateFromFunc(interaction_BC, lambda m: m.become(Arrow(organism_B.get_center(), organism_C.get_center(), buff=0.3, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.1))),
            UpdateFromFunc(interaction_CA, lambda m: m.become(Arrow(organism_C.get_center(), organism_A.get_center(), buff=0.3, color=WHITE, max_tip_length_to_length_ratio=0.1))),
            run_time=2
        )

        title = Text("Ecology & Evolutionary Principles", font_size=48).to_edge(UP).set_color(WHITE)
        self.play(FadeIn(title, shift=UP), run_time=1.5)

        intro_text_full = Text("Ecology examines how organisms interact with each other and their environment.", font_size=36).next_to(title, DOWN, buff=0.5).set_color(WHITE)
        self.play(Create(intro_text_full), run_time=2)
        
        vector_idea_text = Text("Think of these as 'vectors' of influence!", font_size=30).next_to(intro_text_full, DOWN, buff=0.5).set_color(BLUE_ACCENT)
        self.play(FadeIn(vector_idea_text, shift=UP), run_time=1.5)
        self.wait(1)

        # --- BEAT 2: Food Web - Directed Graph of Interactions ---
        # Pacing: ~10 seconds
        self.play(
            FadeOut(organism_group), 
            FadeOut(interaction_group),
            FadeOut(vector_idea_text),
            intro_text_full.animate.to_edge(UP).shift(DOWN*0.5).scale(0.8),
            run_time=1.5
        )
        
        food_web_title = Text("1. Food Webs: Who Eats Whom?", font_size=40).next_to(intro_text_full, DOWN, buff=0.5).set_color(GOLD_ACCENT)
        self.play(FadeIn(food_web_title, shift=UP))

        # Represent organisms as nodes (circles with labels)
        producer_circle = Circle(radius=0.7, color=GREEN_B, fill_opacity=0.7).shift(DOWN*2 + LEFT*4)
        producer_label = Text("Producer", font_size=28).next_to(producer_circle, DOWN, buff=0.2).set_color(WHITE)
        
        primary_circle = Circle(radius=0.7, color=YELLOW_B, fill_opacity=0.7).shift(UP*1 + LEFT*2)
        primary_consumer_label = Text("Primary Consumer", font_size=28).next_to(primary_circle, DOWN, buff=0.2).set_color(WHITE)

        secondary_circle = Circle(radius=0.7, color=RED_B, fill_opacity=0.7).shift(UP*2 + RIGHT*2)
        secondary_consumer_label = Text("Secondary Consumer", font_size=28).next_to(secondary_circle, DOWN, buff=0.2).set_color(WHITE)

        tertiary_circle = Circle(radius=0.7, color=PURPLE_B, fill_opacity=0.7).shift(UP*0 + RIGHT*4)
        tertiary_consumer_label = Text("Apex Predator", font_size=28).next_to(tertiary_circle, DOWN, buff=0.2).set_color(WHITE)

        node_group = VGroup(
            producer_circle, producer_label, primary_circle, primary_consumer_label,
            secondary_circle, secondary_consumer_label, tertiary_circle, tertiary_consumer_label
        )

        self.play(LaggedStart(
            GrowFromCenter(producer_circle), FadeIn(producer_label, shift=UP),
            GrowFromCenter(primary_circle), FadeIn(primary_consumer_label, shift=UP),
            GrowFromCenter(secondary_circle), FadeIn(secondary_consumer_label, shift=UP),
            GrowFromCenter(tertiary_circle), FadeIn(tertiary_consumer_label, shift=UP),
            lag_ratio=0.2,
            run_time=3
        ))
        
        # Add arrows for energy flow (directed graph edges)
        arrow1 = Arrow(producer_circle.get_top(), primary_circle.get_bottom(), buff=0.1, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.15)
        arrow2 = Arrow(primary_circle.get_top(), secondary_circle.get_left(), buff=0.1, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.15)
        arrow3 = Arrow(secondary_circle.get_right(), tertiary_circle.get_left(), buff=0.1, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.15)
        arrow4 = Arrow(producer_circle.get_right(), tertiary_circle.get_bottom(), buff=0.1, color=BLUE_ACCENT, max_tip_length_to_length_ratio=0.15) 
        arrow_group = VGroup(arrow1, arrow2, arrow3, arrow4)

        self.play(LaggedStart(
            Create(arrow1), Create(arrow2), Create(arrow3), Create(arrow4),
            lag_ratio=0.3,
            run_time=2
        ))
        
        food_web_explanation = Text("A directed graph of energy flow!", font_size=30).next_to(node_group, DOWN, buff=0.7).set_color(GOLD_ACCENT)
        self.play(FadeIn(food_web_explanation, shift=UP), run_time=1.5)
        self.wait(1)

        # --- BEAT 3: Predator-Prey Dynamics - Cycles and Vector Fields ---
        # Pacing: ~10 seconds
        self.play(
            FadeOut(food_web_title),
            FadeOut(food_web_explanation),
            FadeOut(arrow_group),
            FadeOut(node_group),
            intro_text_full.animate.to_edge(UP).shift(DOWN*0.5).scale(0.8),
            run_time=1.5
        )

        dynamics_title = Text("2. Predator-Prey Dynamics: Stability & Change", font_size=40).next_to(intro_text_full, DOWN, buff=0.5).set_color(GOLD_ACCENT)
        self.play(FadeIn(dynamics_title, shift=UP))

        # Use Axes to represent population numbers (phase plane)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [2, 4, 6, 8]},
            y_axis_config={"numbers_to_include": [2, 4, 6, 8]},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label(MathTex("Prey")).set_color(BLUE_ACCENT)
        y_label = axes.get_y_axis_label(MathTex("Predator")).set_color(GOLD_ACCENT).shift(RIGHT*0.5)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=2)

        # Represent predator and prey populations as a point moving on the phase plane (trajectory)
        initial_point_coords = [2, 3] # (Prey, Predator)
        population_dot = Dot(axes.coords_to_point(*initial_point_coords), color=WHITE, radius=0.15)
        
        # Define a simplified cyclical path for illustration
        points_on_path = [
            axes.coords_to_point(2, 3), 
            axes.coords_to_point(4, 2),
            axes.coords_to_point(8, 3),
            axes.coords_to_point(6, 6),
            axes.coords_to_point(3, 8),
            axes.coords_to_point(1, 4),
            axes.coords_to_point(2, 3) 
        ]
        # Create a smooth Bezier path
        path = VMobject()
        path.set_points_as_corners(points_on_path + [points_on_path[0]]) # Close the loop
        path.make_smooth()
        path.set_color(BLUE_ACCENT).set_stroke(width=3)

        self.add(population_dot)
        self.play(MoveAlongPath(population_dot, path), Create(path), run_time=5, rate_func=linear)

        dynamics_explanation = Text("Populations change over time, forming cycles or trends.", font_size=28).next_to(axes, RIGHT, buff=0.5).set_color(BLUE_ACCENT)
        self.play(FadeIn(dynamics_explanation, shift=UP), run_time=1.5)
        
        vector_field_idea = Text("These trajectories are directed by 'vector fields'!", font_size=28).next_to(dynamics_explanation, DOWN, buff=0.5).set_color(GOLD_ACCENT)
        self.play(FadeIn(vector_field_idea, shift=UP), run_time=1.5)
        self.wait(1)

        # --- BEAT 4: Environmental Influence - External Factors ---
        # Pacing: ~10 seconds
        self.play(
            FadeOut(dynamics_title),
            FadeOut(dynamics_explanation),
            FadeOut(vector_field_idea),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(population_dot),
            FadeOut(path),
            intro_text_full.animate.to_edge(UP).shift(DOWN*0.5).scale(0.8),
            run_time=1.5
        )

        environment_title = Text("3. Environmental Factors: Shaping the System", font_size=40).next_to(intro_text_full, DOWN, buff=0.5).set_color(GOLD_ACCENT)
        self.play(FadeIn(environment_title, shift=UP))

        # Represent the ecosystem as a central group of interacting dots
        system_center = ORIGIN + DOWN * 1
        system_dots = VGroup(*[Dot(system_center + complex_to_R3(np.exp(1j * angle)) * 0.8, radius=0.15, color=random_bright_color()) for angle in np.linspace(0, 2 * PI, 6, endpoint=False)])
        system_label = Text("Ecosystem", font_size=30).next_to(system_dots, DOWN, buff=0.5).set_color(WHITE)
        self.play(FadeIn(system_dots), FadeIn(system_label), run_time=2)

        # Represent environment as a large rectangle
        environment_box = Rectangle(width=FRAME_WIDTH * 0.8, height=FRAME_HEIGHT * 0.7, color=GRAY_A, stroke_width=2, fill_opacity=0.1).center()
        environment_label = Text("Environment", font_size=36).next_to(environment_box, UP, buff=0.2).set_color(GRAY_A)
        self.play(Create(environment_box), FadeIn(environment_label, shift=UP), run_time=1.5)
        
        # Show an "environmental perturbation" as a vector
        perturbation_vector = Arrow(LEFT * 4 + UP * 2, LEFT * 2 + UP * 1, buff=0, color=BLUE_ACCENT, stroke_width=6, max_tip_length_to_length_ratio=0.2)
        perturbation_label = Text("Climate Shift", font_size=28).next_to(perturbation_vector.get_end(), RIGHT, buff=0.2).set_color(BLUE_ACCENT)
        
        self.play(Create(perturbation_vector), FadeIn(perturbation_label, shift=UP), run_time=1.5)
        self.wait(0.5)

        # Show the effect of the perturbation on the system (e.g., slight shift or distortion)
        self.play(
            system_dots.animate.shift(RIGHT * 0.5 + UP * 0.2),
            system_label.animate.shift(RIGHT * 0.5 + UP * 0.2),
            Transform(perturbation_vector, Arrow(LEFT * 4 + UP * 2, system_center + RIGHT * 0.5 + UP * 0.2, buff=0, color=GOLD_ACCENT, stroke_width=6, max_tip_length_to_length_ratio=0.2)),
            FadeOut(perturbation_label), 
            run_time=2
        )
        impact_text = Text("External factors apply 'forces' or 'transformations' to the system.", font_size=28).next_to(environment_box, DOWN, buff=0.5).set_color(GOLD_ACCENT)
        self.play(FadeIn(impact_text, shift=UP), run_time=2)
        self.wait(1)

        # --- RECAP CARD ---
        self.play(
            FadeOut(intro_text_full),
            FadeOut(environment_title),
            FadeOut(system_dots),
            FadeOut(system_label),
            FadeOut(environment_box),
            FadeOut(environment_label),
            FadeOut(perturbation_vector),
            FadeOut(impact_text),
            run_time=2
        )

        recap_title = Text("Ecology: Key Principles", font_size=50).to_edge(UP).set_color(WHITE)
        self.play(FadeIn(recap_title, shift=UP), run_time=1.5)

        # Recap points as bullet points
        recap_point1 = Text("• Interactions: Organisms influence each other (vectors, graphs).", font_size=32).shift(UP*1.5 + LEFT*0.5).align_to(LEFT, edge=LEFT + 1).set_color(BLUE_ACCENT)
        recap_point2 = Text("• Dynamics: Systems change over time (trajectories, vector fields).", font_size=32).next_to(recap_point1, DOWN, buff=0.7).align_to(recap_point1, LEFT).set_color(GOLD_ACCENT)
        recap_point3 = Text("• Environment: External factors shape outcomes (parameters, transformations).", font_size=32).next_to(recap_point2, DOWN, buff=0.7).align_to(recap_point1, LEFT).set_color(BLUE_ACCENT)

        self.play(LaggedStart(
            FadeIn(recap_point1, shift=LEFT),
            FadeIn(recap_point2, shift=LEFT),
            FadeIn(recap_point3, shift=LEFT),
            lag_ratio=0.7,
            run_time=4
        ))
        self.wait(3)