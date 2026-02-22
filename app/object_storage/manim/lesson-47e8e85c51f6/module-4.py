from manim import *

# Define custom colors for 3B1B inspired style
BLUE_ACCENT = ManimColor("#8FBCBB") # A cool, slightly desaturated blue
GOLD_ACCENT = ManimColor("#EBCB8B") # A warm, muted gold
PRIMARY_TEXT_COLOR = WHITE
SECONDARY_TEXT_COLOR = ManimColor("#A3BE8C") # A light green/teal for contrast

class EcologicalRelationships(Scene):
    def construct(self):
        # 1. Configuration for clean dark background
        self.camera.background_color = BLACK

        # 2. Strong Visual Hook - Interconnectedness
        title = Text("Ecological Systems", font_size=50, color=BLUE_ACCENT).to_edge(UP).shift(LEFT*0.5)
        subtitle = Text("Relationships & Adaptation", font_size=36, color=GOLD_ACCENT).next_to(title, DOWN).align_to(title, LEFT)
        
        self.play(
            LaggedStart(
                FadeIn(title, shift=UP),
                FadeIn(subtitle, shift=UP),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)

        # Create a dynamic grid of dots representing various organisms
        dots_group = VGroup()
        num_rows, num_cols = 5, 8
        for i in range(num_rows):
            for j in range(num_cols):
                dot = Dot(radius=0.08, color=random.choice([BLUE_ACCENT, GOLD_ACCENT, SECONDARY_TEXT_COLOR]),
                          z_index=1)
                dots_group.add(dot)
        
        dots_group.arrange_in_grid(rows=num_rows, cols=num_cols, buff=0.8).scale(0.8).center().shift(DOWN*0.5)

        # Animate dots appearing with random shifts
        initial_dots_animation = []
        for dot in dots_group:
            initial_dots_animation.append(FadeIn(dot, shift=random.choice([LEFT, RIGHT, UP, DOWN])*0.5))

        self.play(LaggedStart(*initial_dots_animation, lag_ratio=0.04), run_time=2)
        self.wait(0.5)

        # Show transient connections to represent interactions
        connections = VGroup()
        for _ in range(25): # Number of random connections
            dot1 = random.choice(dots_group)
            dot2 = random.choice(dots_group)
            if dot1 != dot2:
                line = Line(dot1.get_center(), dot2.get_center(), color=PRIMARY_TEXT_COLOR, stroke_opacity=0.6, stroke_width=1)
                connections.add(line)
        
        system_intro_text = Text("Life: An Interconnected Web", color=PRIMARY_TEXT_COLOR, font_size=30).to_edge(DOWN)
        
        self.play(
            Create(connections, run_time=1.5), 
            FadeIn(system_intro_text, shift=DOWN)
        )
        self.wait(1)
        
        # Fade out initial elements for the next beat
        self.play(
            FadeOut(dots_group),
            FadeOut(connections),
            FadeOut(system_intro_text),
            FadeOut(subtitle)
        )
        self.wait(0.5)

        # Beat 2: Predator-Prey Dynamics
        beat_title1 = Text("1. Predator-Prey Dynamics", font_size=40, color=GOLD_ACCENT).next_to(title, DOWN).align_to(title, LEFT)
        self.play(ReplacementTransform(title, title.copy().shift(UP*1.5), run_time=0.5), FadeIn(beat_title1, shift=UP)) # Shift title up, replace with copy
        
        # Intuition first: a simple prey-predator interaction visual
        prey_dots = VGroup(*[Dot(radius=0.1, color=SECONDARY_TEXT_COLOR) for _ in range(10)]).arrange(RIGHT, buff=0.3).shift(LEFT*3)
        predator_dot = Dot(radius=0.15, color=BLUE_ACCENT).next_to(prey_dots, RIGHT, buff=0.5)
        
        intuition_text = Text("Populations influence each other", font_size=28, color=PRIMARY_TEXT_COLOR).next_to(predator_dot, UP*2)
        
        self.play(FadeIn(prey_dots), FadeIn(predator_dot), FadeIn(intuition_text))
        self.wait(0.5)
        self.play(
            predator_dot.animate.shift(LEFT*1.5),
            FadeOut(prey_dots.submobjects[0:3]), # Simulate some prey being caught
            run_time=1
        )
        self.wait(0.5)
        self.play(FadeOut(prey_dots), FadeOut(predator_dot), FadeOut(intuition_text))
        
        # Formal notation: Axes for population dynamics
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=6, y_length=4,
            axis_config={"color": SECONDARY_TEXT_COLOR, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [2, 4, 6, 8], "font_size": 20, "color": GOLD_ACCENT},
            y_axis_config={"numbers_to_include": [2, 4, 6, 8], "font_size": 20, "color": BLUE_ACCENT}
        ).to_edge(RIGHT).shift(LEFT*0.5 + UP*0.5)
        
        x_label = axes.get_x_axis_label(MathTex(r"\text{Prey Population}", color=GOLD_ACCENT).scale(0.6), edge=DOWN, direction=DOWN*1.2)
        y_label = axes.get_y_axis_label(MathTex(r"\text{Predator Population}", color=BLUE_ACCENT).scale(0.6), edge=LEFT, direction=LEFT*1.2)
        
        self.play(
            LaggedStart(
                Create(axes),
                FadeIn(x_label),
                FadeIn(y_label),
                lag_ratio=0.3, run_time=1.5
            )
        )
        self.wait(0.5)

        # Simplified Lotka-Volterra cycle path (elliptical approximation)
        curve_points_func = lambda t: axes.c2p(5 + 3*np.cos(t), 5 + 3*np.sin(t*1.5))
        path = ParametricFunction(curve_points_func, t_range=[0, 2*PI, 0.01], color=PRIMARY_TEXT_COLOR, stroke_width=3)
        
        path_dot = Dot(path.points[0], radius=0.1, color=PRIMARY_TEXT_COLOR)
        
        dynamics_text = Text("Cyclical Fluctuations", color=PRIMARY_TEXT_COLOR, font_size=28).next_to(axes, LEFT).align_to(axes, UP)

        self.play(FadeIn(dynamics_text), Create(path), MoveAlongPath(path_dot, path), run_time=3, rate_func=linear)
        self.wait(1)

        self.play(
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(path),
            FadeOut(path_dot), FadeOut(dynamics_text), FadeOut(beat_title1)
        )
        self.wait(0.5)

        # Beat 3: Competition for Resources
        beat_title2 = Text("2. Resource Competition", font_size=40, color=BLUE_ACCENT).next_to(title, DOWN).align_to(title, LEFT)
        self.play(FadeIn(beat_title2, shift=UP))

        resource_pool = Square(side_length=1.5, color=SECONDARY_TEXT_COLOR, fill_opacity=0.6, z_index=0).center().shift(DOWN*0.5)
        resource_label = Text("Limited Resource", color=PRIMARY_TEXT_COLOR, font_size=24).next_to(resource_pool, UP)

        competitor_A = VGroup(*[Dot(radius=0.1, color=BLUE_ACCENT) for _ in range(15)]).arrange_in_grid(rows=3, cols=5, buff=0.4)
        competitor_B = VGroup(*[Dot(radius=0.1, color=GOLD_ACCENT) for _ in range(15)]).arrange_in_grid(rows=3, cols=5, buff=0.4)

        competitor_A.next_to(resource_pool, LEFT, buff=1.5)
        competitor_B.next_to(resource_pool, RIGHT, buff=1.5)

        self.play(
            FadeIn(resource_pool),
            FadeIn(resource_label),
            LaggedStart(
                FadeIn(competitor_A, shift=LEFT),
                FadeIn(competitor_B, shift=RIGHT),
                lag_ratio=0.2
            )
        )
        self.wait(0.5)

        competition_text = Text("Struggling for Survival", color=PRIMARY_TEXT_COLOR, font_size=28).to_edge(UP, buff=1.5)
        self.play(FadeIn(competition_text))

        # Animate competitors moving towards the resource
        self.play(
            competitor_A.animate.shift(RIGHT*0.8),
            competitor_B.animate.shift(LEFT*0.8),
            run_time=1.5
        )
        
        # Simulate differential success (some of A and more of B fade out)
        self.play(
            AnimationGroup(
                FadeOut(competitor_B.submobjects[::2], shift=UP*0.5), # More of B fades
                FadeOut(competitor_A.submobjects[::4], shift=DOWN*0.5), # Less of A fades
                lag_ratio=0.1, run_time=1.5
            )
        )
        self.wait(1)

        self.play(
            FadeOut(resource_pool),
            FadeOut(resource_label),
            FadeOut(competitor_A),
            FadeOut(competitor_B),
            FadeOut(competition_text),
            FadeOut(beat_title2)
        )
        self.wait(0.5)

        # Beat 4: Adaptation
        beat_title3 = Text("3. Adaptation & Evolution", font_size=40, color=GOLD_ACCENT).next_to(title, DOWN).align_to(title, LEFT)
        self.play(FadeIn(beat_title3, shift=UP))

        # Initial organism shape
        organism_shape = Polygon(
            [-0.5, -0.5, 0], [0.5, -0.5, 0], [0, 0.5, 0],
            color=GOLD_ACCENT, fill_opacity=0.8, stroke_width=3
        ).scale(1.5).center()
        
        self.play(Create(organism_shape))
        self.wait(0.5)

        # Environmental pressure visual
        pressure_arrow = Arrow(
            start=LEFT * 2.5 + UP * 1.5,
            end=organism_shape.get_center() + RIGHT * 0.5,
            color=BLUE_ACCENT, stroke_width=5, buff=0.5
        )
        pressure_text = Text("Selective Pressure", color=BLUE_ACCENT, font_size=28).next_to(pressure_arrow, UP)

        self.play(Create(pressure_arrow), FadeIn(pressure_text))
        self.wait(0.5)

        # Define the target adapted shape, placed at the organism's current center
        adapted_shape = Polygon(
            [-0.7, -0.3, 0], [0.3, -0.7, 0], [0.7, 0, 0], [-0.3, 0.7, 0], # A more complex, "resilient" shape
            color=GOLD_ACCENT, fill_opacity=0.8, stroke_width=3
        ).scale(1.5).move_to(organism_shape.get_center())

        adaptation_info_text = Text("Evolving for Survival", color=PRIMARY_TEXT_COLOR, font_size=28).next_to(organism_shape, DOWN*2)
        
        self.play(FadeIn(adaptation_info_text))

        # Animate the transformation to the adapted shape
        self.play(
            Transform(organism_shape, adapted_shape), # Organism transforms in place
            FadeOut(pressure_arrow),
            FadeOut(pressure_text),
            run_time=3
        )
        self.wait(1)

        self.play(
            FadeOut(organism_shape),
            FadeOut(adaptation_info_text),
            FadeOut(beat_title3)
        )
        self.wait(0.5)

        # Final Recap Card
        self.play(FadeOut(title)) # Remove the main title that was persistent
        
        recap_title = Text("Key Takeaways", font_size=50, color=BLUE_ACCENT).to_edge(UP)
        self.play(FadeIn(recap_title, shift=UP))

        recap_points = VGroup(
            Text("• Ecological systems are dynamic and interconnected.", color=PRIMARY_TEXT_COLOR, font_size=32),
            Text("• Predator-Prey dynamics show oscillating populations.", color=PRIMARY_TEXT_COLOR, font_size=32),
            Text("• Competition for resources shapes species' success.", color=PRIMARY_TEXT_COLOR, font_size=32),
            Text("• Adaptation enables organisms to thrive in changing environments.", color=PRIMARY_TEXT_COLOR, font_size=32)
        ).arrange(DOWN, buff=0.7, alignment=LEFT).center()
        
        recap_points.set_color_by_gradient(GOLD_ACCENT, SECONDARY_TEXT_COLOR)

        self.play(LaggedStart(*[FadeIn(point, shift=LEFT) for point in recap_points], lag_ratio=0.3, run_time=3))
        self.wait(3)
        self.play(FadeOut(recap_title), FadeOut(recap_points))
        self.wait(1)