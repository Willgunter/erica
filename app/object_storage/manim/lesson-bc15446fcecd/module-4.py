from manim import *

class EcosystemInteractions(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Color Palette ---
        COLOR_ORGANISM_A = BLUE_E
        COLOR_ORGANISM_B = GOLD_E
        COLOR_ENVIRONMENT = GREY_BROWN
        COLOR_TEXT = WHITE
        COLOR_ACCENT = BLUE_C # Used for general text, secondary highlights
        COLOR_HIGHLIGHT = GOLD_C # Used for primary highlights, main emphasis
        COLOR_RED_ACCENT = RED_E # For 'pressure' or negative interaction

        # --- Beat 1: Visual Hook & Introduction to Ecology ---
        current_title = Text("Ecosystem Interactions", font_size=50, color=COLOR_HIGHLIGHT).to_edge(UP)
        subtitle = Text("The Dance of Life and Environment", font_size=30, color=COLOR_ACCENT).next_to(current_title, DOWN)
        
        self.play(FadeIn(current_title, shift=UP), FadeIn(subtitle, shift=UP))
        self.wait(0.5)

        # A network of interacting "organisms" represented by dots and lines
        nodes = VGroup(*[Dot(radius=0.15, color=COLOR_ORGANISM_A).move_to(3*RIGHT*np.cos(i*PI/3) + 2*UP*np.sin(i*PI/3) + 0.5*np.random.rand(3)) for i in range(6)])
        
        # A central "environment" represented by a circle
        environment_circle = Circle(radius=2.5, color=COLOR_ENVIRONMENT, fill_opacity=0.3).move_to(ORIGIN)
        
        connections = VGroup()
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                line = Line(nodes[i].get_center(), nodes[j].get_center(), stroke_color=GREY_A, stroke_width=1.5)
                connections.add(line)
        
        system = VGroup(environment_circle, connections, nodes).shift(DOWN*0.5)

        self.play(LaggedStart(
            FadeIn(environment_circle, scale=0.8),
            Create(connections, run_time=1.5),
            FadeIn(nodes, shift=UP, scale=0.5),
            lag_ratio=0.1,
            run_time=2.5
        ))
        self.wait(0.5)

        # Introduce text explaining Ecology concepts
        intro_text1 = Text("Ecology: Organisms & Environment", font_size=35, color=COLOR_ACCENT).next_to(system, UP, buff=0.8)
        intro_text2 = Text("Intricate Relationships", font_size=35, color=COLOR_HIGHLIGHT).next_to(intro_text1, DOWN)
        
        self.play(FadeIn(intro_text1, shift=DOWN))
        self.play(FadeIn(intro_text2, shift=DOWN))

        self.wait(1.5)

        # Clear beat 1 visuals and subtitle, keep main title for transformation
        self.play(
            FadeOut(system, shift=DOWN),
            FadeOut(intro_text1, intro_text2, subtitle, shift=UP),
            run_time=1.5
        )

        # --- Beat 2: Basic Interactions - Competition & Cooperation ---
        new_title = Text("Interactions: Competition", font_size=45, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(ReplacementTransform(current_title, new_title))
        current_title = new_title # Update current_title for next transform
        
        # Competition: Two organisms (spheres) move towards a resource, one gets pushed back/shrinks
        competitor_A = Sphere(radius=0.5, resolution=(10, 10), color=COLOR_ORGANISM_A, fill_opacity=0.8).move_to(2.5 * LEFT + DOWN*0.5)
        competitor_B = Sphere(radius=0.5, resolution=(10, 10), color=COLOR_ORGANISM_B, fill_opacity=0.8).move_to(2.5 * RIGHT + DOWN*0.5)
        resource = Dot(radius=0.2, color=GOLD, stroke_color=GOLD, stroke_width=3).move_to(ORIGIN + DOWN*0.5)
        
        self.play(FadeIn(competitor_A, competitor_B, resource))
        self.wait(0.5)

        self.play(
            competitor_A.animate.shift(1.5 * RIGHT),
            competitor_B.animate.shift(1.5 * LEFT),
            run_time=1.5
        )
        self.play(
            competitor_A.animate.shift(0.5 * LEFT), # A 'wins' a bit
            competitor_B.animate.shift(0.5 * RIGHT + UP), # B is pushed back
            competitor_B.animate.scale(0.7).set_color(GREY_B), # B shrinks and fades
            run_time=1.5
        )
        self.wait(1)

        # Cooperation: Two organisms (square and circle) move together and both benefit (grow/change color)
        new_title = Text("Interactions: Cooperation", font_size=45, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(
            FadeOut(competitor_A, competitor_B, resource, shift=DOWN),
            ReplacementTransform(current_title, new_title)
        )
        current_title = new_title

        cooperator_A = Square(side_length=1, color=COLOR_ORGANISM_A, fill_opacity=0.8).move_to(2 * LEFT + DOWN*0.5)
        cooperator_B = Circle(radius=0.6, color=COLOR_ORGANISM_B, fill_opacity=0.8).move_to(2 * RIGHT + DOWN*0.5)
        
        self.play(FadeIn(cooperator_A, cooperator_B))
        self.wait(0.5)
        
        self.play(
            cooperator_A.animate.shift(1 * RIGHT),
            cooperator_B.animate.shift(1 * LEFT),
            run_time=1.5
        )
        self.play(
            cooperator_A.animate.scale(1.2).set_color(COLOR_ACCENT), # Grow and change color
            cooperator_B.animate.scale(1.2).set_color(COLOR_HIGHLIGHT), # Grow and change color
            run_time=1.5
        )
        self.wait(1)

        self.play(FadeOut(cooperator_A, cooperator_B, shift=DOWN))

        # --- Beat 3: Dynamics - Predator-Prey ---
        new_title = Text("Dynamics: Predator-Prey", font_size=45, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(ReplacementTransform(current_title, new_title))
        current_title = new_title

        # NumberPlane for plotting population over time
        plane = NumberPlane(
            x_range=(0, 10, 1), y_range=(0, 10, 1),
            x_length=7, y_length=5,
            axis_config={"color": GREY_A, "stroke_width": 2},
            background_line_style={"stroke_color": GREY_B, "stroke_width": 0.5, "stroke_opacity": 0.6}
        ).add_coordinates(font_size=20).shift(DOWN*0.5)

        x_label = MathTex("\\text{Time}", color=COLOR_ACCENT).next_to(plane.x_axis, RIGHT, buff=0.1)
        y_label = MathTex("\\text{Population}", color=COLOR_HIGHLIGHT).next_to(plane.y_axis, UP, buff=0.1)

        self.play(Create(plane), FadeIn(x_label, y_label), run_time=1.5)

        # Plot Lotka-Volterra like oscillating functions
        def prey_func(t):
            return 5 + 3 * np.sin(t * 0.5)

        def predator_func(t):
            return 5 + 3 * np.cos(t * 0.5 + PI/2) # Predator population lags behind prey

        prey_graph = ParametricFunction(
            lambda t: plane.coords_to_point(t, prey_func(t)),
            t_range=[0, 9.5, 0.05], color=COLOR_ORGANISM_A, stroke_width=4
        )
        predator_graph = ParametricFunction(
            lambda t: plane.coords_to_point(t, predator_func(t)),
            t_range=[0, 9.5, 0.05], color=COLOR_ORGANISM_B, stroke_width=4
        )

        prey_label_mob = MathTex("\\text{Prey}", color=COLOR_ORGANISM_A).next_to(plane.coords_to_point(9.5, prey_func(9.5)), RIGHT, buff=0.1)
        predator_label_mob = MathTex("\\text{Predator}", color=COLOR_ORGANISM_B).next_to(plane.coords_to_point(9.5, predator_func(9.5)), RIGHT, buff=0.1)

        self.play(
            Create(prey_graph, run_time=3),
            FadeIn(prey_label_mob)
        )
        self.play(
            Create(predator_graph, run_time=3),
            FadeIn(predator_label_mob)
        )
        self.wait(1)

        self.play(FadeOut(plane, x_label, y_label, prey_graph, predator_graph, prey_label_mob, predator_label_mob, shift=DOWN))

        # --- Beat 4: Evolution - Adaptation & Change ---
        new_title = Text("Evolution: Adaptation", font_size=45, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(ReplacementTransform(current_title, new_title))
        current_title = new_title

        # Original "organism" shape (simple square)
        original_shape = Square(side_length=2, color=COLOR_ORGANISM_A, fill_opacity=0.8).shift(DOWN*0.5)
        self.play(FadeIn(original_shape))
        self.wait(0.5)

        # "Environmental pressure" arrow and text
        pressure_arrow = Arrow(UP*1.5, DOWN*1.5, color=COLOR_RED_ACCENT, buff=0.5).next_to(original_shape, UP, buff=1)
        pressure_text = Text("Environmental Pressure", font_size=25, color=COLOR_RED_ACCENT).next_to(pressure_arrow, UP)
        
        self.play(GrowArrow(pressure_arrow), Write(pressure_text), run_time=1.5)
        self.wait(0.5)

        # Adapted "organism" shape (a taller, thinner rectangle)
        adapted_shape = Rectangle(width=1.5, height=2.5, color=COLOR_HIGHLIGHT, fill_opacity=0.8).move_to(original_shape.get_center())
        
        evolution_text = Text("Adaptation & Change", font_size=35, color=COLOR_ACCENT).next_to(adapted_shape, DOWN, buff=1.0)
        
        self.play(
            Transform(original_shape, adapted_shape), # Geometric transformation
            FadeOut(pressure_arrow, pressure_text, shift=UP),
            Write(evolution_text),
            run_time=2
        )
        self.wait(1.5)

        self.play(FadeOut(original_shape, evolution_text, shift=DOWN))

        # --- Recap Card ---
        self.play(FadeOut(current_title, shift=UP)) # Fade out the last title

        recap_title = Text("Key Concepts:", font_size=45, color=COLOR_HIGHLIGHT).to_edge(UP)
        
        # Use MathTex for cleaner alignment and consistent font style for list items
        recap_point1 = MathTex(r"\bullet \text{ Ecology: Organisms + Environment}", font_size=35, color=COLOR_ACCENT).next_to(recap_title, DOWN, buff=0.5).align_to(LEFT, edge=LEFT + 2*LEFT)
        recap_point2 = MathTex(r"\bullet \text{ Interactions: Competition \& Cooperation}", font_size=35, color=COLOR_ACCENT).next_to(recap_point1, DOWN, buff=0.3).align_to(recap_point1, LEFT)
        recap_point3 = MathTex(r"\bullet \text{ Dynamics: Predator-Prey Cycles}", font_size=35, color=COLOR_ACCENT).next_to(recap_point2, DOWN, buff=0.3).align_to(recap_point1, LEFT)
        recap_point4 = MathTex(r"\bullet \text{ Evolution: Adaptation over Time}", font_size=35, color=COLOR_ACCENT).next_to(recap_point3, DOWN, buff=0.3).align_to(recap_point1, LEFT)

        self.play(Write(recap_title))
        self.wait(0.5)
        self.play(LaggedStart(
            FadeIn(recap_point1, shift=LEFT),
            FadeIn(recap_point2, shift=LEFT),
            FadeIn(recap_point3, shift=LEFT),
            FadeIn(recap_point4, shift=LEFT),
            lag_ratio=0.3,
            run_time=3
        ))
        self.wait(3)
        self.play(FadeOut(recap_title, recap_point1, recap_point2, recap_point3, recap_point4))
        
        self.wait(1)