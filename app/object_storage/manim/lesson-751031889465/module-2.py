from manim import *

class GeneticsIntro(Scene):
    def construct(self):
        # Scene 1: Module Title Introduction
        self.camera.background_color = "#282828" # Dark background for CS feel

        title = Text("Module: Basics of Genetics and Heredity", font_size=48, color=BLUE_C).move_to(UP*2)
        concept_intro = Text("Let's define Genetics!", font_size=36, color=LIGHT_GRAY).next_to(title, DOWN)

        self.play(
            Write(title, run_time=1.5),
            FadeIn(concept_intro, shift=DOWN, run_time=1)
        )
        self.wait(1.5)

        genetics_word = Text("GENETICS", font_size=84, color=YELLOW_D).move_to(ORIGIN)
        self.play(
            Transform(concept_intro, Text("The Core Concept:", font_size=36, color=LIGHT_GRAY).next_to(genetics_word, UP*1.5)),
            Transform(title, genetics_word)
        )
        self.wait(1.5)
        self.play(FadeOut(concept_intro))

        # Scene 2: Defining Genetics (Part 1 - Scientific Study)
        genetics_definition_start = Text("is the scientific study of", font_size=32, color=GREEN_E)
        genetics_brace = Brace(title, LEFT, buff=0.2)
        genetics_label = genetics_definition_start.next_to(genetics_brace, RIGHT, buff=0.2)

        science_icon_circle = Circle(radius=0.5, color=BLUE_A, fill_opacity=0.5).move_to(genetics_label.get_center() + RIGHT * 4)
        science_icon_line1 = Line(science_icon_circle.get_top(), science_icon_circle.get_bottom(), color=BLUE_A)
        science_icon_line2 = Line(science_icon_circle.get_left(), science_icon_circle.get_right(), color=BLUE_A)
        science_icon = VGroup(science_icon_circle, science_icon_line1, science_icon_line2)

        self.play(
            Create(genetics_brace),
            Write(genetics_label, run_time=2)
        )
        self.play(FadeIn(science_icon, scale=0.5))
        self.wait(2)

        # Scene 3: Defining Genetics (Part 2 - Traits)
        current_mobjects = VGroup(genetics_brace, genetics_label, science_icon)
        self.play(
            current_mobjects.animate.shift(LEFT*5).fade(0.5), # Make previous elements less prominent
            title.animate.shift(LEFT*5).scale(0.7) # Also shift the 'GENETICS' word
        )

        traits_word = Text("TRAITS", font_size=60, color=RED_C).move_to(ORIGIN + RIGHT*2.5)
        self.play(Write(traits_word, run_time=1.5))

        # Visual elements for traits - simplified shapes for CS appeal
        square_trait = Square(side_length=1, color=BLUE_B, fill_opacity=0.7).move_to(LEFT*2 + UP*1.5)
        circle_trait = Circle(radius=0.6, color=GREEN_B, fill_opacity=0.7).move_to(LEFT*2)
        triangle_trait = Triangle(color=PURPLE_B, fill_opacity=0.7).scale(0.8).move_to(LEFT*2 + DOWN*1.5)

        trait_examples = Text("(e.g., eye color, hair type)", font_size=24, color=LIGHT_GRAY).next_to(traits_word, DOWN)

        self.play(
            Create(square_trait),
            Create(circle_trait),
            Create(triangle_trait),
            run_time=2
        )
        self.play(FadeIn(trait_examples, shift=DOWN*0.5))
        self.wait(2)

        # Scene 4: Defining Genetics (Part 3 - Parents to Offspring)
        self.play(
            FadeOut(square_trait, circle_trait, triangle_trait, trait_examples),
            traits_word.animate.shift(LEFT*2).scale(0.7).fade(0.5)
        )

        parent_a = Text("Parent A", font_size=36, color=BLUE_C).move_to(LEFT*4 + UP*1)
        parent_b = Text("Parent B", font_size=36, color=BLUE_C).move_to(LEFT*4 + DOWN*1)
        offspring = Text("Offspring", font_size=36, color=GREEN_C).move_to(RIGHT*4)

        arrow_a = Arrow(parent_a.get_right(), offspring.get_left() + UP*0.5, buff=0.1, color=LIGHT_GRAY, max_tip_length_to_length_ratio=0.1)
        arrow_b = Arrow(parent_b.get_right(), offspring.get_left() + DOWN*0.5, buff=0.1, color=LIGHT_GRAY, max_tip_length_to_length_ratio=0.1)
        passing_text = Text("passing of", font_size=28, color=YELLOW_D).next_to(arrow_a, UP*0.5)

        self.play(
            Write(parent_a),
            Write(parent_b),
            FadeIn(offspring, shift=RIGHT)
        )
        self.play(
            Create(arrow_a),
            Create(arrow_b),
            Write(passing_text)
        )

        # Simulate a trait being passed (simple block of color)
        trait_block = Rectangle(width=0.8, height=0.4, color=RED_C, fill_opacity=0.8).move_to(parent_a.get_center())
        trait_block_2 = Rectangle(width=0.8, height=0.4, color=GREEN_B, fill_opacity=0.8).move_to(parent_b.get_center())
        
        self.play(FadeIn(trait_block, shift=LEFT), FadeIn(trait_block_2, shift=LEFT))
        self.play(
            trait_block.animate.move_to(offspring.get_center() + UP*0.5),
            trait_block_2.animate.move_to(offspring.get_center() + DOWN*0.5),
            rate_func=linear,
            run_time=2
        )
        self.wait(1.5)

        # Scene 5: Defining Genetics (Part 4 - Heredity)
        self.play(
            FadeOut(parent_a, parent_b, offspring, arrow_a, arrow_b, passing_text, trait_block, trait_block_2),
            current_mobjects.animate.fade(1), # Fade out previous components
            title.animate.fade(1),
            traits_word.animate.fade(1)
        )

        heredity_word = Text("HEREDITY", font_size=84, color=YELLOW_D).move_to(ORIGIN + UP*1.5)
        heredity_def = Text("is the process by which traits are passed\nfrom parents to offspring.", font_size=36, color=GREEN_E).next_to(heredity_word, DOWN*1.5)

        self.play(
            Write(heredity_word, run_time=1.5),
            FadeIn(heredity_def, shift=DOWN)
        )

        # Small arrow to link back to the passing concept
        link_arrow = Arrow(heredity_def.get_top(), heredity_word.get_bottom(), buff=0.1, color=LIGHT_GRAY, max_tip_length_to_length_ratio=0.1)
        link_text = Text("This process is...", font_size=24, color=LIGHT_GRAY).next_to(link_arrow, LEFT)

        self.play(GrowArrow(link_arrow), Write(link_text))
        self.wait(2)
        self.play(FadeOut(link_arrow, link_text))


        # Scene 6: Summary
        self.play(
            FadeOut(heredity_word, heredity_def)
        )

        summary_title = Text("Genetics Defined:", font_size=48, color=BLUE_C).move_to(UP*3)
        summary_definition = VGroup(
            Text("Genetics", font_size=40, color=YELLOW_D),
            Text(" is the ", font_size=40, color=LIGHT_GRAY),
            Text("scientific study", font_size=40, color=GREEN_E),
            Text(" of how ", font_size=40, color=LIGHT_GRAY),
            Text("traits", font_size=40, color=RED_C),
            Text(" are passed from ", font_size=40, color=LIGHT_GRAY),
            Text("parents to offspring", font_size=40, color=BLUE_C),
            Text(", known as ", font_size=40, color=LIGHT_GRAY),
            Text("heredity", font_size=40, color=YELLOW_D)
        ).arrange(RIGHT, buff=0.1).next_to(summary_title, DOWN*1.5).scale(0.8)

        # Break into multiple lines if too long
        summary_line1 = VGroup(summary_definition[0], summary_definition[1], summary_definition[2], summary_definition[3]).arrange(RIGHT, buff=0.1)
        summary_line2 = VGroup(summary_definition[4], summary_definition[5], summary_definition[6]).arrange(RIGHT, buff=0.1)
        summary_line3 = VGroup(summary_definition[7], summary_definition[8]).arrange(RIGHT, buff=0.1)
        
        full_summary = VGroup(summary_line1, summary_line2, summary_line3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)


        self.play(Write(summary_title))
        self.play(
            LaggedStart(
                Write(summary_line1, run_time=2),
                Write(summary_line2, run_time=2),
                Write(summary_line3, run_time=1.5),
                lag_ratio=0.5
            )
        )
        self.wait(3)

        # Final fade out for a clean exit
        self.play(FadeOut(summary_title, full_summary))
        self.wait(0.5)