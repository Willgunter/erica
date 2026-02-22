from manim import *

class PhotosynthesisModule(Scene):
    def construct(self):
        # --- Scene 1: Title Card & Module Intro ---
        title = Text("Metabolism Photosynthesis: Plants Convert", font_size=56, color=BLUE_B).move_to(UP*1.5)
        objective = Text("Objective: Understand and Apply", font_size=36, color=WHITE).next_to(title, DOWN)

        plant_icon = SVGMobject("plant_icon.svg").scale(0.8).next_to(objective, DOWN, buff=0.8) # Assuming a simple plant icon SVG exists or using a Placeholder
        if not plant_icon.is_drawn(): # Placeholder if SVG is not found
            plant_icon = Circle(radius=0.5, color=GREEN_B, fill_opacity=0.8).next_to(objective, DOWN, buff=0.8)
            leaf1 = Polygon([plant_icon.get_top(), plant_icon.get_right() + UP*0.5, plant_icon.get_top() + LEFT*0.5], color=GREEN_A, fill_opacity=0.8).shift(RIGHT*0.3 + UP*0.1)
            leaf2 = Polygon([plant_icon.get_top(), plant_icon.get_left() + UP*0.5, plant_icon.get_top() + RIGHT*0.5], color=GREEN_A, fill_opacity=0.8).shift(LEFT*0.3 + UP*0.1)
            plant_icon = VGroup(plant_icon, leaf1, leaf2)


        self.play(Write(title))
        self.play(FadeIn(objective, shift=DOWN))
        self.play(Create(plant_icon))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, objective, plant_icon)))

        # --- Scene 2: Concept Walkthrough - Intro ---
        concept_title = Text("Concept Walkthrough", font_size=48, color=BLUE_C).to_edge(UP)
        intro_text = Text(
            "Photosynthesis: Plants convert light to chemical energy (glucose).",
            font_size=36, color=WHITE
        ).move_to(ORIGIN)

        sun = Circle(radius=0.5, color=YELLOW_A, fill_opacity=1).move_to(LEFT*4 + UP*1.5)
        sun_rays = VGroup(*[
            Line(sun.get_center(), sun.get_center() + 1.2 * rotate_vector(UP, TAU/8 * i), color=YELLOW_C)
            for i in range(8)
        ]).set_stroke(width=3)
        sun_group = VGroup(sun, sun_rays)

        plant_leaf = Polygon(
            [-1, -1, 0], [0, 1, 0], [1, -1, 0],
            color=GREEN_D, fill_opacity=0.7
        ).scale(0.8).move_to(LEFT*2.5 + DOWN*0.5)

        arrow_light = Arrow(sun_group.get_right(), plant_leaf.get_left(), buff=0.1, color=YELLOW)

        glucose_icon = Rectangle(width=1.5, height=1, color=ORANGE, fill_opacity=0.7).move_to(RIGHT*2.5 + DOWN*0.5)
        glucose_label = Text("Glucose (C₆H₁₂O₆)", font_size=24, color=WHITE).move_to(glucose_icon.get_center())
        glucose_group = VGroup(glucose_icon, glucose_label)

        arrow_energy = Arrow(plant_leaf.get_right(), glucose_group.get_left(), buff=0.1, color=ORANGE)

        self.play(Write(concept_title))
        self.play(FadeIn(sun_group, shift=LEFT), FadeIn(plant_leaf, shift=LEFT))
        self.play(Write(arrow_light))
        self.play(FadeIn(intro_text, shift=UP))
        self.play(Write(arrow_energy), FadeIn(glucose_group, shift=RIGHT))
        self.wait(2)
        self.play(FadeOut(VGroup(concept_title, intro_text, sun_group, plant_leaf, arrow_light, glucose_group, arrow_energy)))

        # --- Scene 3: Photosynthesis Equation Part 1 (Reactants) ---
        equation_label = Text("Equation:", font_size=36, color=BLUE_A).to_edge(UP + LEFT)

        co2_text = MathTex("6\\text{CO}_2", color=RED).move_to(LEFT*3)
        h2o_text = MathTex("6\\text{H}_2\\text{O}", color=BLUE).next_to(co2_text, RIGHT, buff=1)
        plus_sign = MathTex("+", color=WHITE).next_to(co2_text, RIGHT, buff=0.5)

        self.play(Write(equation_label))
        self.play(FadeIn(co2_text, shift=LEFT))
        self.play(FadeIn(plus_sign))
        self.play(FadeIn(h2o_text, shift=RIGHT))
        self.wait(1.5)

        # --- Scene 4: Photosynthesis Equation Part 2 (Energy & Products) ---
        reactants = VGroup(co2_text, plus_sign, h2o_text)

        arrow_eq = Arrow(reactants.get_right(), ORIGIN + RIGHT*1.5, buff=0.5, color=WHITE)
        light_energy_label = Text("Light Energy", font_size=24, color=YELLOW).next_to(arrow_eq, UP, buff=0.1)

        glucose_eq = MathTex("\\text{C}_6\\text{H}_{12}\\text{O}_6", color=ORANGE).next_to(arrow_eq, RIGHT, buff=0.5)
        o2_text = MathTex("6\\text{O}_2", color=GREEN).next_to(glucose_eq, RIGHT, buff=1)
        plus_sign2 = MathTex("+", color=WHITE).next_to(glucose_eq, RIGHT, buff=0.5)

        self.play(reactants.animate.shift(LEFT*2.5))
        self.play(GrowArrow(arrow_eq))
        self.play(FadeIn(light_energy_label, shift=UP))
        self.play(FadeIn(glucose_eq, shift=RIGHT))
        self.play(FadeIn(plus_sign2))
        self.play(FadeIn(o2_text, shift=RIGHT))

        full_equation = VGroup(reactants, arrow_eq, light_energy_label, glucose_eq, plus_sign2, o2_text)
        self.wait(2)
        self.play(FadeOut(VGroup(equation_label, full_equation)))

        # --- Scene 5: Guided Practice - Intro ---
        practice_title = Text("Guided Practice", font_size=48, color=BLUE_C).to_edge(UP)
        flashcard_prompt = Text("Review the flashcards for Metabolism Photosynthesis.", font_size=36, color=WHITE)

        card_base = Rectangle(width=4, height=2.5, color=GREY_BROWN, fill_opacity=0.8).move_to(ORIGIN)
        card_text_front = Text("Front of Card", font_size=30, color=BLACK).move_to(card_base.get_center())
        card_front = VGroup(card_base.copy(), card_text_front.copy().set_color(BLACK).set_opacity(0.6))
        
        cards = VGroup(
            card_front.copy().shift(DR*0.2).set_opacity(0.8),
            card_front.copy().shift(DR*0.1).set_opacity(0.9),
            card_front
        )
        cards.arrange(RIGHT, buff=0.1).move_to(ORIGIN)

        self.play(Write(practice_title))
        self.play(FadeIn(flashcard_prompt, shift=DOWN))
        self.play(FadeIn(cards))
        self.wait(1.5)
        self.play(FadeOut(flashcard_prompt), FadeOut(cards))

        # --- Scene 6: Guided Practice - Flashcard Example 1 ---
        card_front_q = Text("What is Photosynthesis?", font_size=30, color=BLACK).move_to(ORIGIN)
        card_rect_front = Rectangle(width=5, height=3, color=TEAL_A, fill_opacity=1)
        card1 = VGroup(card_rect_front, card_front_q)

        card_back_a = Text("Plants convert light energy\ninto chemical energy (glucose).", font_size=28, color=BLACK, t2c={'light energy':YELLOW, 'chemical energy':ORANGE, 'glucose':ORANGE}).move_to(ORIGIN)
        card_rect_back = Rectangle(width=5, height=3, color=TEAL_B, fill_opacity=1)
        card1_back = VGroup(card_rect_back, card_back_a)

        self.play(FadeIn(card1, shift=UP))
        self.wait(1.5)
        self.play(Transform(card1, card1_back,
                            run_time=1.5,
                            path_arc=TAU/2,
                            axis=LEFT)) # Simulates flip
        self.wait(1.5)
        self.play(FadeOut(card1))

        # --- Scene 7: Guided Practice - Flashcard Example 2 ---
        card_front_q2 = Text("Recall the Photosynthesis Equation.", font_size=30, color=BLACK).move_to(ORIGIN)
        card_rect_front2 = Rectangle(width=5, height=3, color=PURPLE_A, fill_opacity=1)
        card2 = VGroup(card_rect_front2, card_front_q2)

        card_back_a2 = MathTex(
            "6\\text{CO}_2 + 6\\text{H}_2\\text{O} \\xrightarrow{\\text{Light Energy}} \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2",
            font_size=28, color=BLACK
        ).move_to(ORIGIN)
        card_rect_back2 = Rectangle(width=5.5, height=3.5, color=PURPLE_B, fill_opacity=1)
        card2_back = VGroup(card_rect_back2, card_back_a2)

        self.play(FadeIn(card2, shift=UP))
        self.wait(1.5)
        self.play(Transform(card2, card2_back,
                            run_time=1.5,
                            path_arc=TAU/2,
                            axis=LEFT))
        self.wait(1.5)
        self.play(FadeOut(card2, practice_title))

        # --- Scene 8: AI Spar - Intro ---
        ai_title = Text("AI Spar", font_size=48, color=BLUE_C).to_edge(UP)
        ai_prompt = Text("Test your understanding with Erica.", font_size=36, color=WHITE).move_to(ORIGIN)

        robot_head = Circle(radius=0.7, color=GREY_BROWN, fill_opacity=1)
        robot_eye_l = Circle(radius=0.1, color=BLUE_E, fill_opacity=1).shift(LEFT*0.3 + UP*0.2)
        robot_eye_r = Circle(radius=0.1, color=BLUE_E, fill_opacity=1).shift(RIGHT*0.3 + UP*0.2)
        robot_mouth = Line(LEFT*0.3, RIGHT*0.3, color=WHITE).shift(DOWN*0.3)
        erica_avatar = VGroup(robot_head, robot_eye_l, robot_eye_r, robot_mouth).scale(0.8).next_to(ai_prompt, DOWN, buff=1)

        self.play(Write(ai_title))
        self.play(FadeIn(ai_prompt, shift=DOWN))
        self.play(Create(erica_avatar))
        self.wait(1.5)
        self.play(FadeOut(ai_prompt))

        # --- Scene 9: AI Spar - Question Example ---
        erica_avatar.animate.scale(0.7).to_corner(DR)

        erica_bubble = SVGMobject("bubble_left.svg").scale(2).next_to(erica_avatar, UP + LEFT, buff=0.1) # Assuming bubble SVG, else use a rounded rectangle
        if not erica_bubble.is_drawn():
            erica_bubble = RoundedRectangle(corner_radius=0.5, width=6, height=3, color=BLUE_A, fill_opacity=0.8).next_to(erica_avatar, UP + LEFT, buff=0.1)
        
        erica_q1_text = Text("Erica: What are the main reactants of photosynthesis?", font_size=28, color=BLACK).move_to(erica_bubble.get_center())
        erica_q1 = VGroup(erica_bubble, erica_q1_text)

        options_box = Rectangle(width=6, height=2.5, color=GREY_D, fill_opacity=0.9).move_to(LEFT*2.5)
        option_a = Text("A) Oxygen, Water", font_size=24, color=WHITE).next_to(options_box.get_top(), DOWN, buff=0.2).align_to(options_box.get_left(), LEFT).shift(RIGHT*0.5)
        option_b = Text("B) CO₂, Water", font_size=24, color=WHITE).next_to(option_a, DOWN, buff=0.2).align_to(option_a, LEFT)
        option_c = Text("C) Glucose, Oxygen", font_size=24, color=WHITE).next_to(option_b, DOWN, buff=0.2).align_to(option_a, LEFT)
        options_group = VGroup(options_box, option_a, option_b, option_c)

        self.play(FadeIn(erica_q1, shift=UP))
        self.play(FadeIn(options_group, shift=LEFT))
        self.wait(2)
        self.play(Indicate(option_b, color=GREEN_B))
        self.wait(1.5)
        self.play(FadeOut(erica_q1, options_group))

        # --- Scene 10: AI Spar - Guidance Example ---
        erica_q2_text = Text("Erica: Correct! Now, what is the primary product of photosynthesis?", font_size=28, color=BLACK).move_to(erica_bubble.get_center())
        erica_q2 = VGroup(erica_bubble.copy().set_color(BLUE_D), erica_q2_text)

        erica_response_text = Text("Erica: Great! It's Glucose. Keep going!", font_size=28, color=BLACK).move_to(erica_bubble.get_center())
        erica_response = VGroup(erica_bubble.copy().set_color(GREEN_A), erica_response_text)

        self.play(FadeIn(erica_q2, shift=UP))
        self.wait(2)
        self.play(Transform(erica_q2, erica_response)) # Simulate a quick thinking/response animation
        self.wait(2)
        self.play(FadeOut(VGroup(erica_q2, erica_avatar, ai_title)))
        self.wait(1)

# Placeholder SVG for Manim if not present:
# To use this script, you would need `plant_icon.svg` and `bubble_left.svg`
# For `plant_icon.svg`, a simple leaf or potted plant vector graphic.
# For `bubble_left.svg`, a speech bubble shape pointing to the left-bottom.
# If these SVGs are not available, Manim will use the fallback VGroup defined in the script.