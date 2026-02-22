from manim import *

class CellsAnimation(Scene):
    def construct(self):
        # --- Configuration ---
        self.camera.background_color = "#1a1a1a" # Clean dark background

        # --- Beat 1: The Visual Hook & Introduction ---
        self.beat_1_intro()

        # --- Beat 2: Cell Theory - Fundamental Unit & Origin ---
        self.beat_2_cell_theory()

        # --- Beat 3: Growth & Division (Geometric Transformation) ---
        self.beat_3_growth_division()

        # --- Beat 4: Specialization & Organization (Linear Algebra Analogy) ---
        self.beat_4_specialization_organization()

        # --- Beat 5: Recap & Call to Action ---
        self.beat_5_recap_and_practice()

    def beat_1_intro(self):
        # Initial scattered points/units - visual hook
        dots = VGroup(*[
            Dot(point=2*np.array([np.random.rand()-0.5, np.random.rand()-0.5, 0])).set_color(BLUE_A).scale(0.5)
            for _ in range(50)
        ])

        # Grid to emphasize structure and coordinates
        self.plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=6,
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.6},
            faded_line_style={"stroke_color": BLUE_D, "stroke_width": 0.5, "stroke_opacity": 0.4}
        ).shift(2 * LEFT + DOWN).scale(0.7) # Positioned to leave space for text
        self.plane.add_coordinates(font_size=20, color=BLUE_C)

        self.play(FadeIn(dots, shift=UP), run_time=1.5)
        self.play(FadeIn(self.plane, scale=0.5), dots.animate.shift(self.plane.get_center()))
        
        # A central "cell" shape emerges from the dots
        cell_outline = Circle(radius=1.3, color=GOLD, stroke_width=4).move_to(self.plane.get_center())
        central_cell_fill = Circle(radius=1.1, color=BLUE_E, fill_opacity=0.8).move_to(self.plane.get_center())
        self.cell_repr = VGroup(cell_outline, central_cell_fill)

        self.play(
            dots.animate.set_opacity(0).scale(0.1), # Dots fade out, shrinking
            Create(cell_outline),
            GrowFromCenter(central_cell_fill),
            run_time=2
        )
        self.remove(dots) # Clean up dots after they fade out

        # Title and objective
        title = Text("Cells: Life's Basic Building Blocks", font_size=50, color=GOLD).to_edge(UP)
        objective = Text("Understand & apply cells: life's basic building blocks", font_size=28, color=BLUE_B).next_to(title, DOWN)
        
        self.play(
            LaggedStart(
                Write(title),
                Write(objective),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.wait(1)
        self.current_title_group = VGroup(title, objective)

    def beat_2_cell_theory(self):
        self.play(FadeOut(self.current_title_group, shift=UP), run_time=0.8)

        cell_theory_text = MathTex(r"\text{The Cell: Fundamental Unit of Life}", color=GOLD).to_edge(UP)
        cell_theory_point1 = MathTex(r"\bullet \text{ All life is made of cells}", color=BLUE_A).next_to(cell_theory_text, DOWN, buff=0.5)
        cell_theory_point2 = MathTex(r"\bullet \text{ Cells come from pre-existing cells}", color=BLUE_A).next_to(cell_theory_point1, DOWN)

        self.play(Write(cell_theory_text))
        self.play(Write(cell_theory_point1))
        self.wait(0.5)

        # Animate "Cells come from pre-existing cells" by showing a cell dividing
        original_cell_pos = self.cell_repr.get_center()
        self.play(self.cell_repr.animate.shift(LEFT * 2))

        # Create a dividing line/plane
        dividing_line = Line(start=self.cell_repr.get_left() + UP * 0.5, end=self.cell_repr.get_right() + DOWN * 0.5, color=GOLD, stroke_width=2)
        
        # Show division as a transformation
        self.play(Create(dividing_line), run_time=0.7)
        
        # Create two new cell halves and transform the original cell into them
        # (Visually, the original cell splits into two slightly smaller ones)
        cell_1_half = Circle(radius=0.7, color=BLUE_E, fill_opacity=0.8, stroke_color=GOLD, stroke_width=4).shift(self.cell_repr.get_center() + LEFT * 0.8)
        cell_2_half = Circle(radius=0.7, color=BLUE_E, fill_opacity=0.8, stroke_color=GOLD, stroke_width=4).shift(self.cell_repr.get_center() + RIGHT * 0.8)
        
        self.play(
            ReplacementTransform(self.cell_repr, VGroup(cell_1_half, cell_2_half).arrange(RIGHT, buff=0.4)),
            FadeOut(dividing_line),
            run_time=1.5
        )
        self.current_cells_div = VGroup(cell_1_half, cell_2_half) # Store for cleanup

        self.play(Write(cell_theory_point2))
        self.wait(1.5)

        # Clean up for next beat, moving the initial cell back to center
        self.play(
            FadeOut(cell_theory_text, shift=UP),
            FadeOut(cell_theory_point1, shift=UP),
            FadeOut(cell_theory_point2, shift=UP),
            FadeOut(self.current_cells_div),
            self.cell_repr.animate.move_to(original_cell_pos), # Move original (now empty) VGroup back to reference
            run_time=1.5
        )
        # Re-establish self.cell_repr as a single cell for the next beat
        self.cell_repr = VGroup(Circle(radius=1.3, color=GOLD, stroke_width=4), Circle(radius=1.1, color=BLUE_E, fill_opacity=0.8)).arrange(ORIGIN).move_to(self.plane.get_center())

    def beat_3_growth_division(self):
        growth_title = MathTex(r"\text{Growth \& Division}", color=GOLD).to_edge(UP)
        self.play(Write(growth_title))
        self.wait(0.5)

        # Illustrate growth: a single cell expands and contracts
        self.play(self.cell_repr.animate.scale(1.2), run_time=0.8)
        self.play(self.cell_repr.animate.scale(1/1.2), run_time=0.8)

        # Visualize division leading to a cluster
        original_cell_for_division = self.cell_repr.copy().shift(LEFT * 2)
        self.play(Transform(self.cell_repr, original_cell_for_division)) # Move original to division starting point

        # Arrow for transformation
        arrow_to_divide = Arrow(start=original_cell_for_division.get_right(), end=original_cell_for_division.get_right() + RIGHT * 2, buff=0.1, color=BLUE)
        divide_text = MathTex(r"\text{Divide}", color=BLUE_A, font_size=36).next_to(arrow_to_divide, UP)
        self.play(GrowArrow(arrow_to_divide), Write(divide_text))

        # Create two new cells from the original
        cell_A = Circle(radius=0.7, color=BLUE_E, fill_opacity=0.8, stroke_color=GOLD, stroke_width=3)
        cell_B = Circle(radius=0.7, color=BLUE_E, fill_opacity=0.8, stroke_color=GOLD, stroke_width=3)
        initial_cluster = VGroup(cell_A, cell_B).arrange(RIGHT, buff=0.4).next_to(arrow_to_divide, RIGHT, buff=0.5)

        self.play(
            ReplacementTransform(original_cell_for_division, initial_cluster),
            FadeOut(arrow_to_divide, divide_text),
            run_time=2
        )
        self.wait(0.5)

        # Illustrate multiple divisions leading to a larger cluster
        cell_cluster = initial_cluster
        for _ in range(2): # Two more rounds of division for visual effect
            new_cells = VGroup()
            for cell in cell_cluster:
                # Simulate cell splitting into two slightly offset copies
                new_cells.add(cell.copy().shift(UP * 0.2 + LEFT * 0.2))
                new_cells.add(cell.copy().shift(DOWN * 0.2 + RIGHT * 0.2))
            
            # Arrange new cells into a denser cluster around the original center
            # Adjust scaling and spacing for a compact, growing cluster
            new_cells_arranged = new_cells.arrange_in_grid(rows=2 * len(cell_cluster) // 2, cols=2, buff=0.1).move_to(cell_cluster.get_center()).scale(0.8)
            
            self.play(
                Transform(cell_cluster, new_cells_arranged),
                run_time=1.5
            )
            cell_cluster = new_cells_arranged
            self.wait(0.5)

        self.current_cluster = cell_cluster # Store for cleanup

        self.play(
            FadeOut(growth_title, shift=UP),
            FadeOut(self.current_cluster),
            FadeOut(self.cell_repr), # Fade out the original cell_repr that moved
            run_time=1.5
        )

    def beat_4_specialization_organization(self):
        spec_org_title = MathTex(r"\text{Specialization \& Organization}", color=GOLD).to_edge(UP)
        self.play(Write(spec_org_title))
        self.wait(0.5)

        # Start with a grid of identical cells (like undifferentiated tissue)
        initial_cells_grid = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=0.7, color=BLUE_E, fill_opacity=0.8, stroke_color=GOLD).move_to(self.plane.c2p(i-1, j-1))
                initial_cells_grid.add(cell)
        
        self.play(FadeIn(initial_cells_grid.center().shift(LEFT*2)), run_time=1.5)

        # Transformation arrow for differentiation
        transform_arrow = Arrow(start=initial_cells_grid.get_right(), end=initial_cells_grid.get_right() + RIGHT*2, buff=0.1, color=BLUE)
        transform_text = MathTex(r"\text{Differentiate}", color=BLUE_A, font_size=36).next_to(transform_arrow, UP)

        self.play(GrowArrow(transform_arrow), Write(transform_text))

        # Show cells specializing and forming a new, organized structure
        # Each cell undergoes a unique geometric transformation (color, scale, rotation) and arrangement
        specialized_cells = VGroup()
        colors = [BLUE_D, BLUE_C, BLUE_B, GOLD_A, GOLD_B, GOLD_C, BLUE_A, GOLD, WHITE]
        shapes = [Circle, Triangle, Square]
        
        # Transform each initial cell into a specialized one
        for i, cell in enumerate(initial_cells_grid):
            new_shape = shapes[i % len(shapes)](
                stroke_color=colors[i],
                fill_color=colors[i],
                fill_opacity=0.7,
                side_length=cell.get_width() * (0.8 + 0.4 * (i % 3)) # Vary size
            ).rotate(i * PI/6).shift(self.plane.get_center() + RIGHT * 3 + UR * (i%3 -1)*0.5 + DL * (i//3 - 1)*0.5) # Arrange into a loose cluster
            specialized_cells.add(new_shape)

        specialized_cells.arrange_in_grid(rows=3, cols=3, buff=0.4).shift(RIGHT*3) # More structured arrangement

        self.play(
            ReplacementTransform(initial_cells_grid, specialized_cells),
            FadeOut(transform_arrow, transform_text),
            run_time=2.5
        )
        self.wait(1.5)

        self.play(
            FadeOut(spec_org_title, shift=UP),
            FadeOut(specialized_cells),
            FadeOut(self.plane), # Fade out the plane as well, no longer needed
            run_time=1.5
        )

    def beat_5_recap_and_practice(self):
        # Recap Card
        recap_card = Rectangle(width=6, height=4, color=GOLD, stroke_width=3, fill_color=BLUE_E, fill_opacity=0.7).center()
        recap_title = Text("Recap: Cells - Life's Basic Building Blocks", font_size=32, color=GOLD).move_to(recap_card.get_top() + DOWN*0.5)
        
        point1 = MathTex(r"\bullet \text{ Fundamental Unit of Life}", color=BLUE_A).next_to(recap_title, DOWN, buff=0.4).align_to(recap_card.get_left(), LEFT).shift(RIGHT*0.5)
        point2 = MathTex(r"\bullet \text{ Cells from Pre-existing Cells}", color=BLUE_A).next_to(point1, DOWN, buff=0.3).align_to(recap_card.get_left(), LEFT).shift(RIGHT*0.5)
        point3 = MathTex(r"\bullet \text{ Growth, Division, Organization}", color=BLUE_A).next_to(point2, DOWN, buff=0.3).align_to(recap_card.get_left(), LEFT).shift(RIGHT*0.5)
        
        self.play(Create(recap_card), FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(
            Write(point1),
            Write(point2),
            Write(point3),
            lag_ratio=0.5
        ), run_time=3)
        self.wait(1)

        # Call to Action: Flashcards & AI Spar
        call_to_action_title = Text("Test Your Knowledge!", font_size=40, color=GOLD).to_edge(UP)
        self.play(
            FadeOut(recap_card, shift=DOWN),
            FadeOut(recap_title, shift=DOWN),
            FadeOut(point1, shift=DOWN),
            FadeOut(point2, shift=DOWN),
            FadeOut(point3, shift=DOWN),
            FadeIn(call_to_action_title, shift=UP),
            run_time=1.5
        )

        # Flashcards representation
        flashcard_icon = Rectangle(width=2, height=1.5, color=BLUE_C, fill_opacity=0.8, stroke_width=2).shift(LEFT*2.5 + DOWN*0.5)
        flashcard_text = Text("Flashcards", font_size=28, color=WHITE).move_to(flashcard_icon)
        flashcard_label = Text("Review Concepts", font_size=24, color=BLUE_A).next_to(flashcard_icon, DOWN)
        
        self.play(
            Create(flashcard_icon),
            FadeIn(flashcard_text, shift=UP),
            FadeIn(flashcard_label, shift=UP)
        )
        self.wait(0.5)

        # AI Spar representation
        ai_icon_base = Circle(radius=0.8, color=GOLD, fill_opacity=0.8).shift(RIGHT*2.5 + DOWN*0.5)
        ai_text = Text("Erica AI", font_size=28, color=BLUE_C).move_to(ai_icon_base)
        question_mark = MathTex(r"\text{?}" , color=WHITE, font_size=60).move_to(ai_icon_base.get_top() + UP*0.3)
        ai_label = Text("Practice Exam Questions", font_size=24, color=GOLD_A).next_to(ai_icon_base, DOWN)

        self.play(
            Create(ai_icon_base),
            FadeIn(ai_text, shift=UP),
            GrowFromCenter(question_mark),
            FadeIn(ai_label, shift=UP)
        )
        self.wait(2)

        final_message = Text("Keep Exploring Life's Wonders!", font_size=36, color=BLUE_A).to_edge(DOWN)
        self.play(FadeIn(final_message, shift=UP))
        self.wait(2)

        self.play(
            FadeOut(self.mobjects), # Fade out everything
            run_time=2
        )