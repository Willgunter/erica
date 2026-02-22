from manim import *

class EnergyFlowModuleIntro(Scene):
    def construct(self):
        # --- Scene 1: Module Title & Objective ---
        # Title and Module Name
        module_title_label = Text("Module Title:", font_size=36, color=GREY_C).to_edge(UP + LEFT)
        module_name = Text("Energy Flow and Cellular Metabolism", font_size=48, color=BLUE_C)
        module_name.next_to(module_title_label, DOWN, buff=0.5).align_to(module_title_label, LEFT)

        # Objective
        objective_label = Text("Objective:", font_size=32, color=GREY_C).next_to(module_name, DOWN, buff=1.0).align_to(module_title_label, LEFT)
        objective_text = Text("Understand and apply energy flow and cellular metabolism", font_size=40, color=WHITE, line_spacing=1.2)
        objective_text.next_to(objective_label, DOWN, buff=0.5).align_to(objective_label, LEFT)
        
        self.play(FadeIn(module_title_label, shift=UP))
        self.play(Write(module_name))
        self.wait(0.5)
        self.play(FadeIn(objective_label, shift=UP))
        self.play(Write(objective_text))
        self.wait(2) # Total ~6 seconds

        # --- Scene 2: Concept Walkthrough Intro ---
        # Clear previous elements
        self.play(
            FadeOut(VGroup(module_title_label, module_name, objective_label, objective_text), shift=UP),
            run_time=1
        )

        section_title_1 = Text("1. Concept Walkthrough", font_size=48, color=BLUE_C).to_edge(UP)
        description_1 = Text(
            "This module focuses on how living organisms acquire and use energy, "
            "a fundamental process for all life.",
            font_size=32, line_spacing=1.5
        ).scale(0.8).next_to(section_title_1, DOWN, buff=1.0)

        # Visual: Abstract System Block for Metabolism
        system_block = Rectangle(width=4.5, height=2.5, color=BLUE_D, fill_opacity=0.6).center()
        process_label = Text("Cellular Metabolism", font_size=28, color=WHITE).move_to(system_block.center)

        energy_in_arrow = Arrow(start=LEFT*4, end=system_block.get_left(), color=YELLOW_C, buff=0, stroke_width=7)
        energy_in_label = Text("Nutrients (Energy Input)", font_size=24, color=YELLOW_C).next_to(energy_in_arrow, UP)

        energy_out_arrow = Arrow(start=system_block.get_right(), end=RIGHT*4, color=RED_C, buff=0, stroke_width=7)
        energy_out_label = Text("Work + Heat (Energy Output)", font_size=24, color=RED_C).next_to(energy_out_arrow, UP)

        self.play(Write(section_title_1))
        self.play(FadeIn(description_1, shift=DOWN))
        self.wait(1)
        self.play(
            Create(system_block),
            Write(process_label),
            run_time=1.5
        )
        self.play(
            GrowArrow(energy_in_arrow),
            FadeIn(energy_in_label, shift=LEFT),
            run_time=1
        )
        self.play(
            GrowArrow(energy_out_arrow),
            FadeIn(energy_out_label, shift=RIGHT),
            run_time=1
        )
        self.wait(2) # Total ~8.5 seconds

        # --- Scene 3: Guided Practice Intro ---
        # Clear previous elements
        group_to_fade_out = VGroup(section_title_1, description_1, system_block, process_label, energy_in_arrow, energy_in_label, energy_out_arrow, energy_out_label)
        self.play(FadeOut(group_to_fade_out, shift=UP), run_time=1)

        section_title_2 = Text("2. Guided Practice", font_size=48, color=GREEN_C).to_edge(UP)
        description_2 = Text(
            "Review the flashcards for Energy Flow and Cellular Metabolism. "
            "Try to explain each concept back in your own words.",
            font_size=32, line_spacing=1.5
        ).scale(0.8).next_to(section_title_2, DOWN, buff=1.0)

        # Visual: Stack of Flashcards and a Speech Bubble
        flashcard_concept_label = Text("ATP Synthase", font_size=28, color=BLUE_A)
        
        flashcard_stack_visual = VGroup()
        for i in range(3):
            card = Rectangle(width=3.5, height=2.0, color=GREY_D, fill_opacity=0.7)
            card.shift(UR * 0.15 * i) # Slight offset for stack effect
            if i == 0: # Place text only on the topmost card
                card_with_text = VGroup(card, flashcard_concept_label.copy().move_to(card.center))
                flashcard_stack_visual.add(card_with_text)
            else:
                flashcard_stack_visual.add(card)
        flashcard_stack_visual.move_to(LEFT * 2.5 + DOWN * 0.5) # Position the stack

        speech_bubble = SpeechBubble(
            content=Text("Explain This!", font_size=28, color=WHITE),
            fill_color=YELLOW_D,
            tip_direction=LEFT
        ).next_to(flashcard_stack_visual, RIGHT, buff=1.0)

        self.play(Write(section_title_2))
        self.play(FadeIn(description_2, shift=DOWN))
        self.wait(1)
        self.play(Create(flashcard_stack_visual))
        self.play(FadeIn(speech_bubble, shift=LEFT))
        self.wait(2) # Total ~7 seconds

        # --- Scene 4: AI Spar Intro ---
        # Clear previous elements
        group_to_fade_out = VGroup(section_title_2, description_2, flashcard_stack_visual, speech_bubble)
        self.play(FadeOut(group_to_fade_out, shift=UP), run_time=1)

        section_title_3 = Text("3. AI Spar", font_size=48, color=YELLOW_C).to_edge(UP)
        description_3 = Text(
            "Test your understanding with Erica. She will ask you questions "
            "from the practice exam and guide you through challenging topics.",
            font_size=32, line_spacing=1.5
        ).scale(0.8).next_to(section_title_3, DOWN, buff=1.0)

        # Visual: Simple Robot/AI Avatar and Question Bubble
        robot_head = Circle(radius=0.7, color=GREY_C, fill_opacity=0.8).shift(LEFT*3 + DOWN*0.5)
        robot_eye_l = Circle(radius=0.1, color=BLUE_A).move_to(robot_head.get_center() + LEFT*0.3 + UP*0.2)
        robot_eye_r = Circle(radius=0.1, color=BLUE_A).move_to(robot_head.get_center() + RIGHT*0.3 + UP*0.2)
        robot_mouth = Line(start=robot_head.get_center() + LEFT*0.3 + DOWN*0.3, end=robot_head.get_center() + RIGHT*0.3 + DOWN*0.3, color=WHITE)
        robot_antenna = Line(start=robot_head.get_top(), end=robot_head.get_top() + UP*0.5, color=GREY_C).set_stroke(width=5)
        robot = VGroup(robot_head, robot_eye_l, robot_eye_r, robot_mouth, robot_antenna)

        ai_question_bubble = SpeechBubble(
            content=Text("What is Glycolysis?", font_size=28, color=WHITE),
            fill_color=BLUE_D,
            tip_direction=LEFT
        ).next_to(robot, RIGHT, buff=0.5)
        
        ai_guide_arrow = Arrow(ai_question_bubble.get_bottom() + DOWN*0.3, DOWN*2 + RIGHT*2, color=GREEN_C, buff=0.2, stroke_width=6)
        ai_guide_text = Text("Guidance", font_size=24, color=GREEN_C).next_to(ai_guide_arrow, DOWN)

        self.play(Write(section_title_3))
        self.play(FadeIn(description_3, shift=DOWN))
        self.wait(1)
        self.play(FadeIn(robot, shift=LEFT))
        self.play(Create(ai_question_bubble))
        self.play(Wiggle(robot_head, scale_factor=1.1, run_time=1))
        self.play(GrowArrow(ai_guide_arrow), FadeIn(ai_guide_text, shift=DOWN))
        self.wait(2) # Total ~8 seconds

        # --- Scene 5: Module Overview/Menu ---
        # Clear previous elements
        group_to_fade_out = VGroup(section_title_3, description_3, robot, ai_question_bubble, ai_guide_arrow, ai_guide_text)
        self.play(FadeOut(group_to_fade_out, shift=UP), run_time=1)

        module_overview_title = Text("Module Sections:", font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(module_overview_title))

        # Create interactive-looking buttons for each section
        button_width = 7.5
        button_height = 1.5

        concept_btn_text = Text("1. Concept Walkthrough", font_size=36, color=BLUE_C)
        concept_btn_rect = Rectangle(width=button_width, height=button_height, color=BLUE_C, fill_opacity=0.2).move_to(concept_btn_text)
        concept_group = VGroup(concept_btn_rect, concept_btn_text).next_to(module_overview_title, DOWN, buff=0.8)

        guided_btn_text = Text("2. Guided Practice", font_size=36, color=GREEN_C)
        guided_btn_rect = Rectangle(width=button_width, height=button_height, color=GREEN_C, fill_opacity=0.2).move_to(guided_btn_text)
        guided_group = VGroup(guided_btn_rect, guided_btn_text).next_to(concept_group, DOWN, buff=0.5)

        ai_btn_text = Text("3. AI Spar", font_size=36, color=YELLOW_C)
        ai_btn_rect = Rectangle(width=button_width, height=button_height, color=YELLOW_C, fill_opacity=0.2).move_to(ai_btn_text)
        ai_group = VGroup(ai_btn_rect, ai_btn_text).next_to(guided_group, DOWN, buff=0.5)

        self.play(GrowFromCenter(concept_group[0]), Write(concept_group[1]))
        self.play(GrowFromCenter(guided_group[0]), Write(guided_group[1]))
        self.play(GrowFromCenter(ai_group[0]), Write(ai_group[1]))
        self.wait(3) # Total ~7 seconds