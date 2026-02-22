from manim import *

class CellStructureAnimation(Scene):
    def construct(self):
        # Scene 1: Concept Walkthrough - Cells as Fundamental Building Blocks
        self.introduction_scene()
        self.wait(0.5)

        # Scene 2: Guided Practice - Flashcards
        self.guided_practice_scene()
        self.wait(0.5)

        # Scene 3: AI Spar - Test Your Knowledge with Erica
        self.ai_spar_scene()

    def introduction_scene(self):
        # Module Title
        module_title = Text("Understanding Cell Structure and Function", font_size=48, color=BLUE_B).to_edge(UP)
        self.play(Write(module_title), run_time=1.5)

        # Concept 1: Cells are fundamental building blocks
        concept_text = Text("Cells: Fundamental Building Blocks", font_size=40, color=WHITE).next_to(module_title, DOWN, buff=0.8)
        self.play(FadeIn(concept_text, shift=UP), run_time=1.5)

        # Visualizing a single cell block
        cell_block = Square(side_length=1.0, color=GREEN_C, fill_opacity=0.7, stroke_width=3).move_to(LEFT * 3)
        self.play(Create(cell_block), run_time=1)

        cell_label = Text("A Cell Unit", font_size=24, color=WHITE).next_to(cell_block, DOWN)
        self.play(FadeIn(cell_label), run_time=0.7)

        # Create a grid of cells to show "building blocks" forming a structure
        grid_group = VGroup()
        for i in range(3):
            for j in range(3):
                new_cell = cell_block.copy().shift(RIGHT * (i * 1.1) + UP * (j * 1.1) - LEFT * 3.5 + DOWN * 0.5)
                grid_group.add(new_cell)
        
        grid_group.move_to(RIGHT * 2 + DOWN * 0.5) # Center the grid visually

        self.play(
            LaggedStart(*[Transform(cell_block.copy(), cell) for cell in grid_group], lag_ratio=0.1),
            FadeOut(cell_block, cell_label), # Fade out the initial single cell
            run_time=2.5
        )
        
        # Add explanatory text for the grid
        expl_text = Text("The basic units of all living organisms.", font_size=30, color=LIGHT_GRAY).next_to(grid_group, DOWN, buff=0.7)
        self.play(FadeIn(expl_text, shift=DOWN), run_time=1.5)

        self.wait(0.5)
        self.play(FadeOut(module_title, concept_text, grid_group, expl_text))

    def guided_practice_scene(self):
        title = Text("Guided Practice: Flashcards", font_size=48, color=BLUE_B).to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # Flashcard outline
        flashcard_outline = Rectangle(width=6, height=4, color=YELLOW_C, stroke_width=4, fill_opacity=0.1).center()
        self.play(Create(flashcard_outline), run_time=1)

        # Front of the flashcard (question)
        card_front_text = Text("What is a Cell?", font_size=36, color=WHITE).move_to(flashcard_outline.get_center())
        self.play(Write(card_front_text), run_time=1.5)

        self.wait(1) # Pause to let the question register

        # Simulate card flip: fade out front, change card color, fade in back
        card_back_text = Text(
            "The basic structural and functional\nunit of all known organisms.",
            font_size=32, color=WHITE, t2c={"functional": GREEN_C, "structural": GREEN_C}
        ).move_to(flashcard_outline.get_center())

        self.play(
            FadeOut(card_front_text),
            flashcard_outline.animate.set_color(GREEN_C),
            FadeIn(card_back_text),
            run_time=2
        )

        # Prompt for user interaction
        prompt_text = Text("Review & Explain!", font_size=30, color=LIGHT_GRAY).next_to(flashcard_outline, DOWN, buff=0.7)
        self.play(FadeIn(prompt_text, shift=DOWN), run_time=1.5)

        self.wait(0.5)
        self.play(FadeOut(title, flashcard_outline, card_back_text, prompt_text))

    def ai_spar_scene(self):
        title = Text("AI Spar: Test Your Knowledge", font_size=48, color=BLUE_B).to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # AI Character (geometric and clean for CS aesthetic)
        ai_head = Circle(radius=0.7, color=GRAY_A, fill_opacity=0.8).shift(LEFT * 3 + UP * 0.5)
        ai_eye_left = Circle(radius=0.1, color=BLUE_E, fill_opacity=1).move_to(ai_head.get_center() + LEFT * 0.3 + UP * 0.2)
        ai_eye_right = Circle(radius=0.1, color=BLUE_E, fill_opacity=1).move_to(ai_head.get_center() + RIGHT * 0.3 + UP * 0.2)
        ai_mouth = Line(ai_head.get_center() + LEFT * 0.3 + DOWN * 0.3, ai_head.get_center() + RIGHT * 0.3 + DOWN * 0.3, color=WHITE, stroke_width=3)
        ai_char = VGroup(ai_head, ai_eye_left, ai_eye_right, ai_mouth)

        self.play(FadeIn(ai_char, shift=LEFT), run_time=1.5)

        ai_name = Text("Erica", font_size=36, color=YELLOW_C).next_to(ai_char, DOWN, buff=0.5)
        self.play(FadeIn(ai_name, shift=UP), run_time=0.7)

        # AI prompt bubble with a question
        question_bubble = SpeechBubble(direction=LEFT, height=2.5, width=5, color=GREY_A, fill_opacity=0.7).next_to(ai_char, RIGHT, buff=0.5)
        question_bubble_text = Text(
            "What is the primary function\nof the Mitochondria?",
            font_size=28, color=WHITE, t2c={"Mitochondria": GREEN_C}
        ).move_to(question_bubble.get_center())

        self.play(
            Create(question_bubble),
            FadeIn(question_bubble_text),
            run_time=2
        )

        # Guidance text for the user
        guidance_text = Text("She will ask you questions and guide your learning.", font_size=30, color=LIGHT_GRAY).next_to(question_bubble, DOWN, buff=0.7)
        self.play(FadeIn(guidance_text, shift=DOWN), run_time=1.5)

        self.wait(0.5)
        self.play(FadeOut(title, ai_char, ai_name, question_bubble, question_bubble_text, guidance_text))