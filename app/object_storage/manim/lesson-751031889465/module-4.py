from manim import *

class EcologyIntro(Scene):
    def construct(self):
        # Color palette inspired by modern UI/UX for CS learners
        title_color = BLUE_E          # Deep blue for main titles
        concept_color = GREEN_SCREEN  # Bright green for key concepts
        text_color = WHITE            # Standard white for general text
        shape_organism_color = BLUE_A # Light blue for organism nodes
        shape_environment_color = GRAY_B # Medium gray for environment containers
        arrow_color = WHITE           # White for interaction lines
        highlight_color = YELLOW_A    # Bright yellow for emphasis

        # Scene 1: Module Title and Concept Walkthrough Introduction
        # Animation: Write for title, FadeIn for subtitle
        title = Text("Introduction to Ecology and Evolution", font_size=55, color=title_color)
        module_text = Text("Module: Concept Walkthrough", font_size=35, color=text_color).next_to(title, DOWN, buff=0.8)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(module_text, shift=DOWN), run_time=1)
        self.wait(2)
        self.play(FadeOut(title, shift=UP), FadeOut(module_text, shift=UP), run_time=1)
        # Scene duration: ~5.5 seconds

        # Scene 2: What is Ecology? (Part 1 - Definition Start)
        # Animation: FadeIn for title, Write for definition fragment
        what_is_ecology_title = Text("What is Ecology?", font_size=48, color=title_color).to_edge(UP)
        definition_part1 = Text("Ecology is the study of how organisms interact...", font_size=38, color=concept_color)

        self.play(FadeIn(what_is_ecology_title, shift=UP), run_time=1)
        self.play(Write(definition_part1), run_time=2)

        # Visual: A single organism node (like a system component)
        organism_A = Circle(radius=0.5, color=shape_organism_color, fill_opacity=0.8).shift(LEFT*2.5 + DOWN*0.5)
        label_A = Text("Organism (Node)", font_size=20, color=text_color).next_to(organism_A, DOWN, buff=0.1)

        self.play(Create(organism_A), FadeIn(label_A), run_time=1.5)
        self.wait(1.5)
        # Scene duration: ~6 seconds

        # Scene 3: What is Ecology? (Part 2 - Completing Definition & Basic Interaction)
        # Animation: Definition continues, new elements FadeIn and Create
        self.play(definition_part1.animate.to_edge(UP, buff=1), FadeOut(what_is_ecology_title), FadeOut(label_A), run_time=1)

        definition_part2 = Text("...with each other and their environment.", font_size=38, color=concept_color)
        definition_full = VGroup(definition_part1, definition_part2).arrange(RIGHT, buff=0.1).to_edge(UP, buff=1)
        
        # Visual: Multiple organisms and an environment container
        organism_B = Circle(radius=0.5, color=TEAL_A, fill_opacity=0.8).shift(RIGHT*2.5 + DOWN*0.5)
        organism_A.move_to(LEFT*2.5 + DOWN*0.5) # Reposition Organism A slightly

        environment_box = Rectangle(width=FRAME_WIDTH - 1, height=4, color=shape_environment_color, fill_opacity=0.2).move_to(DOWN*0.5)
        env_label = Text("Environment (System)", font_size=24, color=text_color).next_to(environment_box.get_top(), UP, buff=0.2)
        
        self.play(
            Transform(definition_part1, definition_full), # Transform existing part and add new part
            Create(organism_B),
            Create(environment_box), FadeIn(env_label),
            run_time=2.5
        )

        # Visual: Arrows depicting interactions (like data flow in a network)
        interaction_AB = Arrow(organism_A.get_right(), organism_B.get_left(), buff=0.1, color=arrow_color)
        interaction_AE = Arrow(organism_A.get_top(), environment_box.get_left(), buff=0.1, color=arrow_color).shift(UP*0.5+RIGHT*0.5)
        interaction_BE = Arrow(organism_B.get_top(), environment_box.get_right(), buff=0.1, color=arrow_color).shift(UP*0.5+LEFT*0.5)
        
        self.play(Create(interaction_AB), Create(interaction_AE), Create(interaction_BE), run_time=2)
        self.wait(2.5)
        # Scene duration: ~8 seconds

        # Scene 4: Key Interactions Visual (A more complex network)
        # Animation: FadeOut old elements, FadeIn new title, Transform/Create new objects
        self.play(
            FadeOut(definition_full, shift=UP),
            FadeOut(env_label),
            FadeOut(interaction_AB), FadeOut(interaction_AE), FadeOut(interaction_BE), # Fade out old arrows
            run_time=1
        )

        key_interactions_title = Text("Key Interactions (Network)", font_size=48, color=title_color).to_edge(UP)
        self.play(FadeIn(key_interactions_title, shift=UP), run_time=1)

        # Reposition and shrink elements for a cleaner diagram
        org_A_new = organism_A.copy().move_to(LEFT*2.5 + UP*0.5)
        org_B_new = organism_B.copy().move_to(RIGHT*2.5 + UP*0.5)
        env_box_new = environment_box.copy().set_width(FRAME_WIDTH - 2).set_height(3).move_to(DOWN*1.5)

        # Additional Organism C (another node)
        organism_C = Circle(radius=0.4, color=shape_organism_color, fill_opacity=0.8).move_to(LEFT*0.8 + UP*1.5)
        
        self.play(
            Transform(organism_A, org_A_new),
            Transform(organism_B, org_B_new),
            Transform(environment_box, env_box_new),
            Create(organism_C),
            run_time=2
        )

        # New arrows for the refined diagram (complex network connections)
        arrows = VGroup(
            Arrow(org_A_new.get_right(), org_B_new.get_left(), buff=0.1, color=arrow_color),
            Arrow(organism_C.get_bottom(), org_A_new.get_top(), buff=0.1, color=arrow_color),
            Arrow(organism_C.get_bottom(), org_B_new.get_top(), buff=0.1, color=arrow_color),
            Arrow(org_A_new.get_bottom(), env_box_new.get_top(), buff=0.1, color=arrow_color),
            Arrow(org_B_new.get_bottom(), env_box_new.get_top(), buff=0.1, color=arrow_color),
            Arrow(organism_C.get_bottom(), env_box_new.get_top(), buff=0.1, color=arrow_color),
            Arrow(org_B_new.get_top(), organism_C.get_right(), buff=0.1, color=arrow_color), # Bidirectional example
        )

        self.play(Create(arrows), run_time=2.5)
        self.wait(2.5)
        # Scene duration: ~9 seconds

        # Scene 5: Environment Components (Biotic vs Abiotic Factors)
        # Animation: FadeOut previous, FadeIn new title, Transform environment box, FadeIn labels and icons
        self.play(
            FadeOut(key_interactions_title, shift=UP),
            FadeOut(organism_A), FadeOut(organism_B), FadeOut(organism_C),
            FadeOut(arrows),
            run_time=1
        )

        env_components_title = Text("Environment Components", font_size=48, color=title_color).to_edge(UP)
        self.play(FadeIn(env_components_title, shift=UP), run_time=1)

        # Focus on the environment box and expand it
        env_box_focused = environment_box.copy().center().set_width(FRAME_WIDTH - 2).set_height(4)
        self.play(Transform(environment_box, env_box_focused), run_time=1.5)

        # Split into Biotic and Abiotic sections with a separator
        biotic_label = Text("Biotic Factors", font_size=32, color=highlight_color).shift(LEFT*2.5 + UP*0.5)
        abiotic_label = Text("Abiotic Factors", font_size=32, color=highlight_color).shift(RIGHT*2.5 + UP*0.5)
        line_separator = Line(env_box_focused.get_top() + DOWN*0.5, env_box_focused.get_bottom() + UP*0.5, color=WHITE).rotate(PI/2)

        self.play(
            FadeIn(biotic_label, shift=LEFT),
            FadeIn(abiotic_label, shift=RIGHT),
            Create(line_separator),
            run_time=1.5
        )

        # Simple geometric icons for Biotic Factors (Living components)
        # Tree-like shape
        tree_top = Triangle(color=GREEN, fill_opacity=1).scale(0.2).shift(LEFT*2.5 + DOWN*0.5)
        tree_trunk = Rectangle(width=0.1, height=0.3, color=BROWN, fill_opacity=1).next_to(tree_top, DOWN, buff=0)
        tree_group = VGroup(tree_top, tree_trunk)

        # Animal-like shape
        animal_body = Circle(radius=0.2, color=RED_E, fill_opacity=1).shift(LEFT*2.5 + DOWN*1.5)
        animal_head = Circle(radius=0.1, color=RED_E, fill_opacity=1).next_to(animal_body, UP*0.5, buff=0)
        animal_group = VGroup(animal_body, animal_head)

        # Simple geometric icons for Abiotic Factors (Non-living components)
        # Sun-like shape
        sun_icon = Circle(radius=0.3, color=YELLOW, fill_opacity=1).shift(RIGHT*2.5 + DOWN*0.5)
        # Water-like shape
        water_icon = Rectangle(width=0.6, height=0.3, color=BLUE_C, fill_opacity=1).shift(RIGHT*2.5 + DOWN*1.5)

        self.play(
            FadeIn(tree_group), FadeIn(animal_group),
            FadeIn(sun_icon), FadeIn(water_icon),
            run_time=1.5
        )
        self.wait(2)
        # Scene duration: ~8.5 seconds