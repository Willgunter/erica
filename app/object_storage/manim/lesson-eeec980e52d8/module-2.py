from manim import *

class GeneticsModuleAnimation(Scene):
    def construct(self):
        # Scene 1: Introduction to Genetics Module
        title = Text("Genetics, DNA, and Cell Reproduction", font_size=60, color=BLUE_C).move_to(UP*1.5)
        objective = Text("Understand and apply genetics, DNA, and cell reproduction", font_size=36, color=WHITE).next_to(title, DOWN)

        self.play(
            Write(title),
            run_time=2
        )
        self.play(
            FadeIn(objective, shift=DOWN),
            run_time=1.5
        )
        self.wait(2)
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(objective, shift=DOWN),
            run_time=1.5
        )

        # Scene 2: Concept Walkthrough - What is Genetics?
        header = Text("Concept Walkthrough", font_size=48, color=GREEN_C).to_edge(UP + LEFT)
        self.play(FadeIn(header, shift=UP + LEFT), run_time=1)

        intro_text = Text(
            "Genetics: The study of how traits are inherited.",
            font_size=40,
            color=WHITE,
            line_spacing=1.2
        ).center()
        self.play(Write(intro_text), run_time=2.5)
        self.wait(0.5)

        # Visual for inheritance
        parent = Circle(radius=0.8, color=BLUE_D, fill_opacity=0.7).move_to(LEFT * 3)
        child = Circle(radius=0.8, color=BLUE_D, fill_opacity=0.7).move_to(RIGHT * 3)
        trait_square = Square(side_length=0.5, color=YELLOW, fill_opacity=1).move_to(parent.get_top() + DOWN * 0.2)
        arrow = Arrow(start=parent.get_right(), end=child.get_left(), color=WHITE)
        inherit_text = Text("Inheritance", font_size=24, color=WHITE).next_to(arrow, UP)

        self.play(FadeOut(intro_text, shift=UP), run_time=1)
        self.play(Create(parent), Create(child), run_time=1.5)
        self.play(FadeIn(trait_square), run_time=0.5)
        self.play(
            Transform(trait_square, trait_square.copy().move_to(child.get_top() + DOWN * 0.2)),
            Create(arrow),
            FadeIn(inherit_text),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(FadeOut(VGroup(parent, child, trait_square, arrow, inherit_text, header)), run_time=1)

        # Scene 3: DNA Introduction
        dna_title = Text("DNA: The Blueprint of Life", font_size=48, color=BLUE_C).to_edge(UP)
        self.play(FadeIn(dna_title, shift=UP), run_time=1)

        # Simplified 2D Helix
        left_curve = VMobject().set_points_as_corners([
            np.array([-1, -2, 0]), np.array([-0.8, -1.5, 0]), np.array([-1, -1, 0]), np.array([-0.8, -0.5, 0]),
            np.array([-1, 0, 0]), np.array([-0.8, 0.5, 0]), np.array([-1, 1, 0]), np.array([-0.8, 1.5, 0]),
            np.array([-1, 2, 0])
        ]).set_color(BLUE_C).set_stroke(width=6)
        right_curve = VMobject().set_points_as_corners([
            np.array([1, -2, 0]), np.array([0.8, -1.5, 0]), np.array([1, -1, 0]), np.array([0.8, -0.5, 0]),
            np.array([1, 0, 0]), np.array([0.8, 0.5, 0]), np.array([1, 1, 0]), np.array([0.8, 1.5, 0]),
            np.array([1, 2, 0])
        ]).set_color(BLUE_C).set_stroke(width=6)

        dna_rungs = VGroup(*[
            Line(
                left_curve.get_point_from_percentage((i+1)/5),
                right_curve.get_point_from_percentage((i+1)/5),
                color=GREEN_D, stroke_width=3
            ) for i in range(4)
        ])
        dna_viz = VGroup(left_curve, right_curve, dna_rungs).scale(1.5).center()
        
        self.play(Create(left_curve), Create(right_curve), run_time=2)
        self.play(Create(dna_rungs), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(dna_title, shift=UP), FadeOut(dna_viz, shift=DOWN), run_time=1)

        # Scene 4: Cell Reproduction
        cell_repro_title = Text("Cell Reproduction: Passing on the blueprint", font_size=42, color=YELLOW_C).to_edge(UP)
        self.play(FadeIn(cell_repro_title, shift=UP), run_time=1)

        cell = Circle(radius=1.5, color=BLUE_D, fill_opacity=0.7)
        self.play(Create(cell), run_time=1.5)
        self.wait(0.5)

        # Elongate and split
        elongated_cell = Ellipse(width=3.5, height=1.5, color=BLUE_D, fill_opacity=0.7)
        self.play(Transform(cell, elongated_cell), run_time=1.5)
        self.wait(0.5)

        daughter_cell1 = Circle(radius=1, color=BLUE_D, fill_opacity=0.7).move_to(LEFT * 1.5)
        daughter_cell2 = Circle(radius=1, color=BLUE_D, fill_opacity=0.7).move_to(RIGHT * 1.5)
        
        self.play(
            Transform(cell, VGroup(daughter_cell1, daughter_cell2)),
            run_time=2
        )
        self.wait(1)
        self.play(FadeOut(cell_repro_title, shift=UP), FadeOut(VGroup(daughter_cell1, daughter_cell2)), run_time=1)

        # Scene 5: Guided Practice - Flashcards
        header = Text("Guided Practice", font_size=48, color=GREEN_C).to_edge(UP + LEFT)
        self.play(FadeIn(header, shift=UP + LEFT), run_time=1)

        intro_text = Text(
            "Review flashcards & explain concepts.",
            font_size=36,
            color=WHITE
        ).move_to(UP*1.5)
        self.play(Write(intro_text), run_time=2)

        # Flashcard stack
        flashcard_back = RoundedRectangle(width=4, height=2.5, corner_radius=0.2, color=BLUE_D, fill_opacity=0.8)
        flashcard_mid = flashcard_back.copy().shift(DOWN*0.1 + RIGHT*0.1).set_opacity(0.6)
        flashcard_front = flashcard_back.copy().shift(DOWN*0.2 + RIGHT*0.2).set_opacity(0.4)
        flashcards = VGroup(flashcard_front, flashcard_mid, flashcard_back).center()
        
        self.play(Create(flashcards), run_time=1.5)
        self.wait(0.5)

        concept_text = Text("What is DNA?", font_size=32, color=BLACK)
        revealed_card = flashcard_back.copy().set_fill(WHITE, opacity=1).set_color(WHITE).set_stroke(color=GRAY_E, width=2)
        
        # Position text on the card
        concept_text.move_to(revealed_card.get_center())
        
        self.play(
            flashcards.animate.shift(LEFT*2),
            Transform(flashcard_back, revealed_card),
            FadeIn(concept_text)
            , run_time=2
        )
        self.wait(1)
        self.play(FadeOut(header), FadeOut(intro_text), FadeOut(flashcards), FadeOut(revealed_card), FadeOut(concept_text), run_time=1)

        # Scene 6: AI Spar - Introduction
        header = Text("AI Spar", font_size=48, color=YELLOW_C).to_edge(UP + RIGHT)
        self.play(FadeIn(header, shift=UP + RIGHT), run_time=1)

        # AI Icon (simple robot head)
        robot_head = Circle(radius=1.2, color=GRAY_A, fill_opacity=0.8)
        robot_eye_left = Circle(radius=0.2, color=BLUE_E, fill_opacity=1).shift(LEFT * 0.5 + UP * 0.2)
        robot_eye_right = Circle(radius=0.2, color=BLUE_E, fill_opacity=1).shift(RIGHT * 0.5 + UP * 0.2)
        robot_mouth = Rectangle(width=1, height=0.1, color=GRAY_B, fill_opacity=1).shift(DOWN * 0.5)
        
        erica_icon = VGroup(robot_head, robot_eye_left, robot_eye_right, robot_mouth).scale(0.8).move_to(LEFT * 3)
        erica_name = Text("Erica", font_size=36, color=WHITE).next_to(erica_icon, DOWN)

        ai_text = Text("Test your understanding with Erica.", font_size=36, color=WHITE).move_to(RIGHT*2)
        
        self.play(Create(erica_icon), run_time=1.5)
        self.play(FadeIn(erica_name, shift=DOWN), run_time=0.5)
        self.play(Write(ai_text), run_time=2)
        self.wait(1.5)
        self.play(FadeOut(header), FadeOut(erica_icon), FadeOut(erica_name), FadeOut(ai_text), run_time=1)

        # Scene 7: AI Spar - Interaction
        # Re-create Erica icon for this isolated scene
        robot_head = Circle(radius=1.2, color=GRAY_A, fill_opacity=0.8)
        robot_eye_left = Circle(radius=0.2, color=BLUE_E, fill_opacity=1).shift(LEFT * 0.5 + UP * 0.2)
        robot_eye_right = Circle(radius=0.2, color=BLUE_E, fill_opacity=1).shift(RIGHT * 0.5 + UP * 0.2)
        robot_mouth = Rectangle(width=1, height=0.1, color=GRAY_B, fill_opacity=1).shift(DOWN * 0.5)
        erica_icon = VGroup(robot_head, robot_eye_left, robot_eye_right, robot_mouth).scale(0.7).to_edge(LEFT + DOWN)
        erica_name = Text("Erica", font_size=28, color=WHITE).next_to(erica_icon, UP)
        self.add(erica_icon, erica_name)

        intro_text = Text(
            "Erica asks questions & guides you.",
            font_size=36,
            color=WHITE
        ).to_edge(UP)
        self.play(Write(intro_text), run_time=2)

        # Erica's speech bubble
        erica_question_content = Text("What is a gene?", font_size=32, color=BLACK)
        speech_bubble = SpeechBubble(
            content=erica_question_content,
            fill_color=WHITE,
            tip_direction=DL,
            height=2.5, width=4
        ).next_to(erica_icon, UP, buff=0.5)
        
        question_group = VGroup(speech_bubble, erica_question_content)
        self.play(FadeIn(question_group, shift=UP), run_time=1.5)

        # User's thought bubble
        user_response_content = Text("A unit of heredity.", font_size=28, color=BLACK)
        thought_bubble = ThoughtBubble(
            content=user_response_content,
            fill_color=LIGHT_GRAY,
            tip_direction=DR,
            height=2, width=3.5
        ).to_edge(RIGHT + DOWN).shift(UP*1.5)
        
        response_group = VGroup(thought_bubble, user_response_content)
        self.play(FadeIn(response_group, shift=DOWN), run_time=1.5)
        self.wait(1.5)
        self.play(
            FadeOut(intro_text), 
            FadeOut(question_group), 
            FadeOut(response_group), 
            FadeOut(erica_icon), 
            FadeOut(erica_name), 
            run_time=1
        )