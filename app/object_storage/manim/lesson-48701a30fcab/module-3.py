from manim import *

class CellularEnergy(Scene):
    def construct(self):
        # 1. Setup: Dark background, high-contrast blue and gold accents
        self.camera.background_color = "#1a1a1a"
        BLUE_ACCENT = BLUE_E
        GOLD_ACCENT = GOLD_C
        TEXT_COLOR = WHITE
        
        # Overall module title
        module_title = Text("Cellular Energy Production & Use", font_size=50, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(module_title))
        self.wait(0.5)

        # --- BEAT 1: The Energy Problem (Visual Hook) ---
        beat1_title = Text("The Need for Energy", font_size=40, color=GOLD_ACCENT).move_to(module_title.get_center())
        self.play(Transform(module_title, beat1_title))

        cell_body = Circle(radius=1.5, color=BLUE_ACCENT, fill_opacity=0.2).shift(DOWN * 0.5)
        cell_label = Text("Cell", color=TEXT_COLOR, font_size=30).next_to(cell_body, UP, buff=0.2)
        cell_group = VGroup(cell_body, cell_label)
        self.play(Create(cell_body), Write(cell_label))

        work_text = Text("Cellular Work: Grow, Move, Repair...", font_size=30, color=TEXT_COLOR).to_edge(LEFT).shift(UP*0.5)
        self.play(Write(work_text))
        self.wait(0.5)
        
        # Simulate energy depletion visually
        energy_bar = Rectangle(height=0.3, width=3, color=GREEN_C, fill_opacity=0.8).next_to(cell_body, DOWN, buff=0.5)
        energy_label = Text("Energy Level", font_size=25, color=TEXT_COLOR).next_to(energy_bar, LEFT, buff=0.1)
        self.play(Create(energy_bar), Write(energy_label))
        self.wait(0.5)

        red_energy_bar = Rectangle(height=0.3, width=3, color=RED_E, fill_opacity=0.8).next_to(cell_body, DOWN, buff=0.5)
        self.play(
            ReplacementTransform(energy_bar, red_energy_bar),
            cell_body.animate.set_color(RED_E).set_opacity(0.4),
            FadeOut(work_text, shift=UP),
            run_time=1.5
        )
        needs_energy_text = Text("Energy Depleted!", font_size=40, color=RED_E).move_to(red_energy_bar).shift(UP*0.8)
        self.play(Write(needs_energy_text))
        self.wait(1)

        self.play(
            FadeOut(red_energy_bar, energy_label, needs_energy_text, cell_group),
            FadeOut(module_title) 
        )
        self.wait(0.5)

        # --- BEAT 2: ATP - The Energy Currency (Intuition First) ---
        beat2_title = Text("ATP: The Energy Currency", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        self.play(FadeIn(beat2_title))

        atp_coin = Circle(radius=0.8, color=GOLD_ACCENT, fill_opacity=0.8, stroke_width=2)
        atp_label = Text("ATP", color=BLACK, font_size=40).move_to(atp_coin)
        atp_group = VGroup(atp_coin, atp_label)
        self.play(GrowFromCenter(atp_group))
        self.wait(0.5)

        work_box = Rectangle(height=1.5, width=2.5, color=BLUE_ACCENT, fill_opacity=0.1, stroke_width=2).shift(RIGHT * 3)
        work_label = Text("Cellular Work", font_size=30, color=TEXT_COLOR).move_to(work_box)
        work_group = VGroup(work_box, work_label)
        self.play(FadeIn(work_group))

        arrow1 = Arrow(start=atp_group.get_right() + LEFT*0.2, end=work_group.get_left() + RIGHT*0.2, color=GOLD_ACCENT, buff=0.1)
        self.play(GrowArrow(arrow1))
        self.wait(0.5)

        # Create geometric representation for ADP and Pi for the split animation
        adp_shape_split = Circle(radius=0.7, color=BLUE_ACCENT, fill_opacity=0.6, stroke_width=2).shift(LEFT * 2.2)
        adp_label_split = Text("ADP", color=BLACK, font_size=30).move_to(adp_shape_split)
        adp_visual_split = VGroup(adp_shape_split, adp_label_split)

        pi_shape_split = Dot(radius=0.25, color=BLUE_ACCENT, fill_opacity=0.8).shift(LEFT * 1.2)
        pi_label_split = Text("P", color=BLACK, font_size=25).move_to(pi_shape_split)
        pi_visual_split = VGroup(pi_shape_split, pi_label_split)

        energy_burst = Dot(color=BLUE_ACCENT, radius=0.2).move_to(arrow1.get_end()).set_opacity(0)
        energy_burst_anim = AnimationGroup(
            energy_burst.animate.scale(5).set_opacity(1),
            energy_burst.animate.scale(0.1).set_opacity(0),
            lag_ratio=0.5
        )
        
        # Animate ATP splitting and releasing energy
        self.play(
            Transform(atp_group, VGroup(adp_visual_split, pi_visual_split)), # ATP transforms to ADP and Pi visuals
            energy_burst_anim,
            arrow1.animate.set_color(BLUE_ACCENT), # Arrow changes color to indicate energy flow
            run_time=1.5
        )
        
        # Keep ADP and Pi visuals for next beat
        adp_remaining = adp_visual_split
        pi_remaining = pi_visual_split
        
        self.wait(1)
        self.play(
            FadeOut(work_group, shift=RIGHT),
            FadeOut(arrow1, shift=RIGHT)
        )
        self.wait(0.5)


        # --- BEAT 3: ATP Structure (Formal Notation/Briefly) ---
        beat3_title = Text("ATP Structure & Energy Release", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        self.play(Transform(beat2_title, beat3_title))

        # Position ADP and Pi for transformation, then fade out
        self.play(
            adp_remaining.animate.shift(LEFT * 1).scale(0.8),
            pi_remaining.animate.shift(LEFT * 0.5).scale(0.8),
            run_time=1
        )
        self.play(FadeOut(adp_remaining, pi_remaining))


        # Simplified ATP structure components: Adenosine-Ribose-P1-P2-P3
        adenosine_text = Text("Adenosine", font_size=25, color=TEXT_COLOR)
        ribose_text = Text("Ribose", font_size=25, color=TEXT_COLOR)
        p1_tex = MathTex("P_1", color=BLUE_ACCENT, font_size=35)
        p2_tex = MathTex("P_2", color=BLUE_ACCENT, font_size=35)
        p3_tex = MathTex("P_3", color=BLUE_ACCENT, font_size=35)

        # Create components group first to arrange
        atp_component_labels = VGroup(adenosine_text, ribose_text, p1_tex, p2_tex, p3_tex).arrange(RIGHT, buff=0.5).shift(LEFT * 0.5)

        # Create bonds based on arranged positions
        bonds_for_atp = VGroup()
        for i in range(len(atp_component_labels) - 1):
            bond = Line(atp_component_labels[i].get_right(), atp_component_labels[i+1].get_left(), color=WHITE, stroke_width=2)
            bonds_for_atp.add(bond)
        
        # Group ADP structure (Adenosine-Ribose-P1-P2 and their bonds)
        adp_structural_part = VGroup(atp_component_labels[0], atp_component_labels[1], atp_component_labels[2], atp_component_labels[3],
                                 bonds_for_atp[0], bonds_for_atp[1], bonds_for_atp[2])
        adp_structural_part.shift(LEFT*0.5) # Adjust position after grouping components and bonds
        
        self.play(FadeIn(adp_structural_part)) # Show ADP structure
        self.wait(0.5)

        # Now introduce the final phosphate and its bond to complete ATP
        p3_and_bond = VGroup(bonds_for_atp[3], atp_component_labels[4]).next_to(adp_structural_part, RIGHT, buff=0.1)
        self.play(FadeIn(p3_and_bond))
        
        # Full ATP structure group for later
        atp_full_structural_group = VGroup(adp_structural_part, p3_and_bond)
        self.wait(0.5)

        # Highlight high-energy bond
        high_energy_bond_rect = SurroundingRectangle(p3_and_bond, color=RED_E, buff=0.1, stroke_width=3)
        bond_label = Text("High-Energy Bond", font_size=25, color=RED_E).next_to(high_energy_bond_rect, UP, buff=0.1)
        self.play(Create(high_energy_bond_rect), Write(bond_label))
        self.wait(1)

        # ATP -> ADP + Pi + Energy Formula
        energy_release_formula = MathTex(
            "\\text{ATP}", r"\rightarrow", "\\text{ADP}", "+ P_i", "+ \\text{Energy}",
            font_size=45, color=TEXT_COLOR
        ).shift(DOWN*2.5)

        self.play(Write(energy_release_formula))
        self.wait(0.5)

        # Animate bond breaking and Pi detaching
        energy_symbol = MathTex("\\text{E}", color=BLUE_ACCENT, font_size=50).move_to(atp_component_labels[4]) # Energy comes from P3 position

        self.play(
            FadeOut(high_energy_bond_rect),
            FadeOut(bond_label),
            Transform(atp_component_labels[4], energy_symbol), # P3 transforms into energy symbol
            FadeOut(bonds_for_atp[3]), # Bond breaks
            run_time=1.5
        )
        self.wait(1)
        
        # --- BEAT 4: The ATP Cycle (Flow) ---
        self.play(FadeOut(energy_release_formula))
        self.play(FadeOut(energy_symbol)) # Energy symbol fades out, used up
        self.play(atp_full_structural_group.animate.move_to(ORIGIN).scale(0.7)) # Shrink and center for transition

        beat4_title = Text("The ATP Cycle: Recycling Energy", font_size=40, color=GOLD_ACCENT).to_edge(UP)
        self.play(Transform(beat2_title, beat4_title))
        
        # Create distinct mobjects for ATP and ADP+Pi states for clear FadeIn/FadeOut
        adp_pi_group_left = MathTex("\\text{ADP}", "+ P_i", font_size=60, color=TEXT_COLOR).shift(LEFT*3)
        atp_group_right = MathTex("\\text{ATP}", font_size=60, color=GOLD_ACCENT).shift(RIGHT*3)
        
        self.play(
            FadeOut(atp_full_structural_group), # Fade out the structural representation
            FadeIn(adp_pi_group_left) # Introduce the textual representation for the cycle
        )
        self.wait(0.5)

        # ATP Production: ADP + Pi -> ATP
        production_arrow = CurvedArrow(adp_pi_group_left.get_bottom(), atp_group_right.get_bottom(), angle=-PI/2, color=BLUE_ACCENT, tip_length=0.2)
        energy_input_text = Text("Energy Input (e.g., from food)", font_size=25, color=BLUE_ACCENT).next_to(production_arrow, DOWN, buff=0.1)
        
        self.play(
            Create(production_arrow),
            Write(energy_input_text)
        )
        self.play(
            FadeOut(adp_pi_group_left, shift=RIGHT*0.5), # ADP+Pi fades out
            FadeIn(atp_group_right, shift=LEFT*0.5), # ATP fades in
            run_time=1.5
        )
        self.wait(1)
        
        # ATP Use: ATP -> ADP + Pi + Energy
        use_arrow = CurvedArrow(atp_group_right.get_top(), adp_pi_group_left.get_top(), angle=PI/2, color=GOLD_ACCENT, tip_length=0.2)
        energy_output_text = Text("Energy Output (for Cellular Work)", font_size=25, color=GOLD_ACCENT).next_to(use_arrow, UP, buff=0.1)
        
        # We need to create new instances of the mobjects for the FadeIn/FadeOut cycle to work correctly
        # This prevents issues with mobjects being 'removed' or 'transformed' state.
        adp_pi_group_left_cycle = MathTex("\\text{ADP}", "+ P_i", font_size=60, color=TEXT_COLOR).shift(LEFT*3)

        self.play(
            Create(use_arrow),
            Write(energy_output_text)
        )
        self.play(
            FadeOut(atp_group_right, shift=LEFT*0.5), # ATP fades out
            FadeIn(adp_pi_group_left_cycle, shift=RIGHT*0.5), # ADP+Pi fades in
            run_time=1.5
        )
        self.wait(1.5) 
        
        # --- BEAT 5: Recap Card ---
        self.play(
            FadeOut(adp_pi_group_left_cycle, atp_group_right, production_arrow, energy_input_text, use_arrow, energy_output_text),
            FadeOut(beat2_title) 
        )
        
        recap_card = Rectangle(
            width=8, height=4.5, color=BLUE_ACCENT, fill_opacity=0.1, stroke_width=2
        ).scale(0.8).move_to(ORIGIN)
        recap_title = Text("Recap: Cellular Energy", font_size=45, color=GOLD_ACCENT).to_edge(UP)

        bullet1 = Text("1. ATP is the cell's main energy currency.", font_size=30, color=TEXT_COLOR)
        bullet2 = Text("2. Energy is released when ATP converts to ADP + Pi.", font_size=30, color=TEXT_COLOR)
        bullet3 = Text("3. Cells constantly recycle ADP + Pi back into ATP.", font_size=30, color=TEXT_COLOR)
        bullet4 = Text("4. This ATP cycle fuels all cellular activities!", font_size=30, color=TEXT_COLOR)
        
        recap_bullets = VGroup(bullet1, bullet2, bullet3, bullet4).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(ORIGIN)
        recap_bullets.shift(UP * 0.5)

        self.play(FadeIn(recap_title))
        self.play(
            Create(recap_card),
            LaggedStart(
                Write(bullet1),
                Write(bullet2),
                Write(bullet3),
                Write(bullet4),
                lag_ratio=0.5,
                run_time=3
            )
        )
        self.wait(4)
        self.play(FadeOut(VGroup(recap_card, recap_bullets, recap_title)))
        self.wait(1)