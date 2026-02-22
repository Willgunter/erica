from manim import *

class BiologyStudyGuideAnimation(Scene):
    def construct(self):
        # --- Colors and general styling for a tech-savvy learner ---
        # A primary blue, a secondary green/yellow, white/light grey for text on a dark background.
        BLUE_PRIMARY = "#2a9d8f"  # Teal-ish blue
        GREEN_ACCENT = "#e9c46a"  # Golden yellow-orange
        TEXT_COLOR = WHITE
        SUBTLE_GREY = "#4a4a4a"

        # --- Scene 1: Module Title & Objective (approx 6-7 seconds) ---
        title_text = Text("Biology Fundamentals Study Guide", font_size=56, color=BLUE_PRIMARY).to_edge(UP)
        objective_text = Text("Objective: Understand and apply biology fundamentals", font_size=36, color=TEXT_COLOR)
        objective_text.next_to(title_text, DOWN, buff=0.8)

        self.play(Write(title_text), run_time=1.5)
        self.wait(0.7)
        self.play(FadeIn(objective_text, shift=UP), run_time=1.5)
        self.wait(2.0)

        # --- Transition out Scene 1 (approx 1 second) ---
        self.play(
            FadeOut(title_text, shift=LEFT),
            FadeOut(objective_text, shift=RIGHT),
            run_time=1
        )
        self.wait(0.5) 

        # --- Scene 2: Concept Walkthrough - Cell Biology (approx 9-10 seconds) ---
        concept_title = Text("Concept Walkthrough", font_size=48, color=GREEN_ACCENT).to_edge(UP)
        cell_biology_intro = Text("1. Cell Biology: The Building Blocks of Life", font_size=36, color=TEXT_COLOR)
        cell_biology_intro.next_to(concept_title, DOWN, buff=0.5)

        # Simple cell representation
        cell_body = Circle(radius=1.5, color=BLUE_PRIMARY, fill_opacity=0.3, stroke_width=4).shift(LEFT * 2)
        nucleus = Dot(radius=0.4, color=GREEN_ACCENT).move_to(cell_body.get_center() + RIGHT * 0.5 + UP * 0.2)
        cell_label = Text("Cell", font_size=28, color=TEXT_COLOR).next_to(cell_body, DOWN, buff=0.3)
        
        cell_group = VGroup(cell_body, nucleus, cell_label)

        all_organisms_text = Text("All living organisms are composed of cells.", font_size=32, color=TEXT_COLOR).next_to(cell_group, RIGHT, buff=1)
        all_organisms_text.align_to(cell_biology_intro, LEFT) 

        self.play(Write(concept_title), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(cell_biology_intro, shift=UP), run_time=1)
        self.wait(0.5)
        self.play(Create(cell_body), Create(nucleus), FadeIn(cell_label), run_time=2)
        self.play(Write(all_organisms_text), run_time=2)
        self.wait(2.0)

        # --- Transition out Scene 2 (approx 1 second) ---
        self.play(
            FadeOut(concept_title, shift=LEFT),
            FadeOut(cell_biology_intro, shift=LEFT),
            FadeOut(cell_group, shift=LEFT),
            FadeOut(all_organisms_text, shift=RIGHT),
            run_time=1
        )
        self.wait(0.5)

        # --- Scene 3: Guided Practice - Flashcards (approx 9-10 seconds) ---
        practice_title = Text("Guided Practice", font_size=48, color=GREEN_ACCENT).to_edge(UP)
        
        # Flashcard stack representation
        card_width = 4
        card_height = 2.5
        flashcard_stack = VGroup(*[
            Rectangle(width=card_width, height=card_height, color=SUBTLE_GREY, fill_opacity=0.1, stroke_width=2).shift(0.05 * i * UP + 0.05 * i * LEFT)
            for i in range(3)
        ]).center()

        top_card_front_text = Text("Concept: Mitosis", font_size=30, color=TEXT_COLOR)
        top_card_back_text = Text("Process of cell division\nthat results in two\nidentical daughter cells.", font_size=24, color=TEXT_COLOR, line_spacing=1.2)

        top_card_rect = Rectangle(width=card_width, height=card_height, color=BLUE_PRIMARY, fill_opacity=0.8, corner_radius=0.1).move_to(flashcard_stack.get_center() + RIGHT*0.2 + UP*0.2)
        top_card_front_text.move_to(top_card_rect.get_center())

        review_text = Text("Review flashcards for Biology Fundamentals.", font_size=32, color=TEXT_COLOR).to_edge(DOWN).shift(UP*1.5)
        explain_text = Text("Explain each concept back in your own words.", font_size=32, color=TEXT_COLOR).next_to(review_text, DOWN, buff=0.5)

        self.play(Write(practice_title), run_time=1)
        self.wait(0.5)
        self.play(Create(flashcard_stack), run_time=1.5)
        self.play(
            FadeIn(top_card_rect, shift=UP),
            Write(top_card_front_text),
            run_time=1.5
        )
        self.wait(1)
        
        # Simulate flipping the card: fade out front, rotate card, fade in back
        self.play(
            FadeOut(top_card_front_text, scale=0.1),
            Transform(top_card_rect, Rectangle(width=card_width, height=card_height, color=BLUE_PRIMARY, fill_opacity=0.8, corner_radius=0.1).move_to(top_card_rect.get_center()).rotate(PI_2, axis=UP)), # Rotate partially
            run_time=0.75
        )
        self.play(
            Transform(top_card_rect, Rectangle(width=card_width, height=card_height, color=BLUE_PRIMARY, fill_opacity=0.8, corner_radius=0.1).move_to(top_card_rect.get_center()).rotate(PI, axis=UP)), # Complete rotation
            FadeIn(top_card_back_text.move_to(top_card_rect.get_center()), scale=0.1),
            run_time=0.75
        )
        self.wait(1)

        self.play(FadeIn(review_text, shift=UP), run_time=1)
        self.play(FadeIn(explain_text, shift=UP), run_time=1)
        self.wait(1.5)

        # --- Transition out Scene 3 (approx 1 second) ---
        self.play(
            FadeOut(practice_title, shift=LEFT),
            FadeOut(flashcard_stack, shift=LEFT),
            FadeOut(top_card_rect, shift=LEFT),
            FadeOut(top_card_back_text, shift=LEFT),
            FadeOut(review_text, shift=RIGHT),
            FadeOut(explain_text, shift=RIGHT),
            run_time=1
        )
        self.wait(0.5)

        # --- Scene 4: AI Spar - Erica (approx 9-10 seconds) ---
        ai_spar_title = Text("AI Spar", font_size=48, color=GREEN_ACCENT).to_edge(UP)

        # Erica character/avatar (a simple circle with an initial)
        erica_avatar = Circle(radius=0.6, color=BLUE_PRIMARY, fill_opacity=0.8, stroke_width=0).to_edge(LEFT).shift(UP*1)
        erica_initial = Text("E", font_size=40, color=WHITE, weight=BOLD).move_to(erica_avatar.get_center())
        erica_name = Text("Erica", font_size=32, color=TEXT_COLOR).next_to(erica_avatar, DOWN, buff=0.3)
        erica_group = VGroup(erica_avatar, erica_initial, erica_name)
        
        # Simulated chat bubble
        chat_bubble_erica = Rectangle(width=6, height=1.5, color=SUBTLE_GREY, fill_opacity=0.8, corner_radius=0.3)
        erica_question = Text("What is the primary function of ribosomes?", font_size=28, color=TEXT_COLOR, disable_ligatures=True)
        
        chat_bubble_erica.to_edge(RIGHT).shift(UP*1)
        erica_question.move_to(chat_bubble_erica.get_center())

        guidance_text = Text("She will ask you questions from the practice exam and guide you.", font_size=32, color=TEXT_COLOR).to_edge(DOWN).shift(UP*1.5)

        self.play(Write(ai_spar_title), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(erica_group, shift=LEFT), run_time=1.5) 
        self.wait(0.5)
        self.play(
            Create(chat_bubble_erica),
            Write(erica_question),
            run_time=2
        )
        self.wait(1.0)
        self.play(FadeIn(guidance_text, shift=UP), run_time=1.5)
        self.wait(2.0)

        # --- Final Transition / End (approx 1 second) ---
        self.play(
            FadeOut(ai_spar_title, shift=LEFT),
            FadeOut(erica_group, shift=LEFT), 
            FadeOut(chat_bubble_erica, shift=LEFT),
            FadeOut(erica_question, shift=LEFT),
            FadeOut(guidance_text, shift=RIGHT),
            run_time=1
        )
        self.wait(1.0)