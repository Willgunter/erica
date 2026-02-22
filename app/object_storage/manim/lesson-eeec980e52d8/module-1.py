from manim import *

class CellStructureIntro(Scene):
    def construct(self):
        # Define a consistent color palette for clarity and visual appeal (CS-friendly)
        COLOR_TITLE = BLUE_C
        COLOR_TEXT = WHITE
        COLOR_HIGHLIGHT = YELLOW
        COLOR_CELL_MEMBRANE = GREEN_A
        COLOR_CYTOPLASM = GREY_BROWN # More neutral, 'program' background feel
        COLOR_NUCLEUS = RED_B
        COLOR_ARROW = ORANGE
        COLOR_STIMULUS = RED

        # --- Scene 1: Module Title & Introduction ---
        title = Text("Cell Structure and Fundamental Functions", font_size=50, color=COLOR_TITLE).to_edge(UP)
        subtitle = Text("The Smallest Units of Life", font_size=32, color=COLOR_TEXT).next_to(title, DOWN, buff=0.7)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait(2.5)
        self.play(FadeOut(title, shift=UP), FadeOut(subtitle, shift=UP))

        # --- Scene 2: What is a Cell? ---
        question = Text("What is a Cell?", font_size=40, color=COLOR_TITLE).to_edge(UP)
        answer = Text("The fundamental, smallest unit of life.", font_size=32, color=COLOR_TEXT).next_to(question, DOWN, buff=0.8)
        
        self.play(Write(question))
        self.wait(1)
        self.play(FadeIn(answer, shift=DOWN))
        
        # Simple cell representation: clean geometric shapes
        cell_outline = Circle(radius=1.5, color=COLOR_CELL_MEMBRANE, stroke_width=4)
        cell_fill = Circle(radius=1.45, color=COLOR_CYTOPLASM, fill_opacity=0.7)
        simple_nucleus = Circle(radius=0.5, color=COLOR_NUCLEUS, fill_opacity=0.8, stroke_color=COLOR_NUCLEUS).move_to(cell_outline)
        simple_cell = VGroup(cell_fill, cell_outline, simple_nucleus).scale(0.8).next_to(answer, DOWN, buff=1.0)
        
        self.play(Create(cell_outline), FadeIn(cell_fill), Create(simple_nucleus))
        self.wait(2)
        self.play(FadeOut(question, shift=LEFT), FadeOut(answer, shift=LEFT), FadeOut(simple_cell, shift=LEFT))

        # --- Scene 3: Hierarchy of Life (Illustrating "Smallest Unit") ---
        hierarchy_title = Text("Cells are the Building Blocks", font_size=40, color=COLOR_TITLE).to_edge(UP)
        self.play(FadeIn(hierarchy_title, shift=UP))

        # Simplified chain representing biological hierarchy, zooming into cell
        texts = [
            Text("Organism", color=COLOR_TEXT),
            Text("Organ System", color=COLOR_TEXT),
            Text("Organ", color=COLOR_TEXT),
            Text("Tissue", color=COLOR_TEXT),
            Text("Cell", color=COLOR_HIGHLIGHT)
        ]
        
        mobjects = []
        for i, text_obj in enumerate(texts):
            mobjects.append(text_obj.scale(0.7))
            if i < len(texts) - 1:
                mobjects.append(Arrow(start=LEFT, end=RIGHT, stroke_width=2, color=COLOR_ARROW))

        chain = VGroup(*mobjects).arrange(RIGHT, buff=0.4).scale(0.8).move_to(ORIGIN)

        self.play(FadeIn(chain[0])) # Organism
        self.play(GrowArrow(chain[1]), FadeIn(chain[2])) # Organ System
        self.play(GrowArrow(chain[3]), FadeIn(chain[4])) # Organ
        self.play(GrowArrow(chain[5]), FadeIn(chain[6])) # Tissue
        self.play(GrowArrow(chain[7]), FadeIn(chain[8])) # Cell
        self.wait(1.5)

        # Highlight and zoom in on the 'Cell'
        self.play(
            FadeOut(hierarchy_title),
            FadeOut(VGroup(*[chain[i] for i in [0,1,2,3,4,5,6,7]])), # Fade everything but 'Cell'
            chain[8].animate.scale(2.5).center() # Scale and center the 'Cell' text
        )
        highlight_circle = Circle(radius=1.5, color=COLOR_HIGHLIGHT, stroke_width=5).around(chain[8])
        self.play(Create(highlight_circle))
        self.wait(2)
        self.play(FadeOut(chain[8]), FadeOut(highlight_circle))

        # --- Scene 4: Basic Cell Structure - Overview & Membrane ---
        structure_title = Text("Basic Cell Structure", font_size=40, color=COLOR_TITLE).to_edge(UP)
        self.play(FadeIn(structure_title, shift=UP))

        cell_membrane_txt = Text("1. Cell Membrane", color=COLOR_TEXT).shift(UP*2 + LEFT*3.5)
        membrane_desc = Text("Outer boundary; controls what enters/leaves.", font_size=24, color=COLOR_TEXT).next_to(cell_membrane_txt, DOWN, aligned_edge=LEFT)
        
        cell_body = Circle(radius=2, color=COLOR_CELL_MEMBRANE, stroke_width=5).shift(RIGHT*2)
        
        self.play(Write(cell_membrane_txt))
        self.play(Create(cell_body))
        self.play(Write(membrane_desc))
        
        # Highlight membrane
        membrane_highlight = cell_body.copy().set_color(COLOR_HIGHLIGHT).set_stroke(width=8)
        self.play(FadeIn(membrane_highlight))
        self.wait(2)
        self.play(FadeOut(membrane_highlight))

        # --- Scene 5: Basic Cell Structure - Cytoplasm ---
        cytoplasm_txt = Text("2. Cytoplasm", color=COLOR_TEXT).next_to(cell_membrane_txt, DOWN, buff=1.0, aligned_edge=LEFT)
        cytoplasm_desc = Text("Gel-like substance; fills the cell, holds organelles.", font_size=24, color=COLOR_TEXT).next_to(cytoplasm_txt, DOWN, aligned_edge=LEFT)

        cytoplasm_fill = Circle(radius=1.9, color=COLOR_CYTOPLASM, fill_opacity=0.8).move_to(cell_body)
        
        self.play(Write(cytoplasm_txt))
        self.play(FadeIn(cytoplasm_fill)) # Fill the cell interior
        self.play(Write(cytoplasm_desc))
        
        # Highlight cytoplasm
        cytoplasm_highlight = cytoplasm_fill.copy().set_color(COLOR_HIGHLIGHT).set_opacity(0.5)
        self.play(FadeIn(cytoplasm_highlight))
        self.wait(2)
        self.play(FadeOut(cytoplasm_highlight))

        # --- Scene 6: Basic Cell Structure - Nucleus ---
        nucleus_txt = Text("3. Nucleus", color=COLOR_TEXT).next_to(cytoplasm_txt, DOWN, buff=1.0, aligned_edge=LEFT)
        nucleus_desc = Text("Control center; contains genetic material (DNA).", font_size=24, color=COLOR_TEXT).next_to(nucleus_txt, DOWN, aligned_edge=LEFT)

        nucleus_body = Circle(radius=0.7, color=COLOR_NUCLEUS, fill_opacity=0.8, stroke_color=COLOR_NUCLEUS, stroke_width=3).move_to(cell_body)
        dna_icon = Text("DNA", font_size=20, color=WHITE).move_to(nucleus_body)
        
        self.play(Write(nucleus_txt))
        self.play(Create(nucleus_body))
        self.play(FadeIn(dna_icon)) # Represent DNA as text inside
        self.play(Write(nucleus_desc))
        
        # Highlight nucleus
        nucleus_highlight = nucleus_body.copy().set_color(COLOR_HIGHLIGHT).set_opacity(0.5)
        self.play(FadeIn(nucleus_highlight))
        self.wait(2)

        # Clear structure elements for next section
        self.play(
            FadeOut(structure_title),
            FadeOut(cell_membrane_txt), FadeOut(membrane_desc),
            FadeOut(cytoplasm_txt), FadeOut(cytoplasm_desc),
            FadeOut(nucleus_txt), FadeOut(nucleus_desc),
            FadeOut(cell_body), FadeOut(cytoplasm_fill), FadeOut(nucleus_body), FadeOut(dna_icon), FadeOut(nucleus_highlight)
        )
        self.wait(0.5)

        # --- Scene 7: Fundamental Functions Overview ---
        functions_title = Text("Fundamental Functions", font_size=40, color=COLOR_TITLE).to_edge(UP)
        self.play(FadeIn(functions_title, shift=UP))

        # Re-introduce a simple cell
        function_cell_outline = Circle(radius=1.5, color=COLOR_CELL_MEMBRANE, stroke_width=4).to_edge(RIGHT, buff=1)
        function_cell_fill = Circle(radius=1.45, color=COLOR_CYTOPLASM, fill_opacity=0.7).move_to(function_cell_outline)
        function_cell = VGroup(function_cell_fill, function_cell_outline)
        
        self.play(Create(function_cell_outline), FadeIn(function_cell_fill))
        
        func1_txt = Text("1. Growth & Metabolism", color=COLOR_TEXT).to_edge(LEFT, buff=1).shift(UP*1.5)
        func2_txt = Text("2. Reproduction", color=COLOR_TEXT).next_to(func1_txt, DOWN, buff=0.8, aligned_edge=LEFT)
        func3_txt = Text("3. Response to Environment", color=COLOR_TEXT).next_to(func2_txt, DOWN, buff=0.8, aligned_edge=LEFT)

        self.play(Write(func1_txt))
        self.play(Write(func2_txt))
        self.play(Write(func3_txt))
        self.wait(2)

        self.play(FadeOut(func2_txt), FadeOut(func3_txt), FadeOut(function_cell))

        # --- Scene 8: Function - Growth & Metabolism ---
        self.play(func1_txt.animate.center().to_edge(UP, buff=1))

        # Visual: Cell taking in nutrients and expanding slightly
        growth_cell = Circle(radius=1.5, color=COLOR_CELL_MEMBRANE, stroke_width=4, fill_color=COLOR_CYTOPLASM, fill_opacity=0.7).center()
        self.play(FadeIn(growth_cell))
        
        nutrient_in = Square(side_length=0.4, color=COLOR_HIGHLIGHT, fill_opacity=1).next_to(growth_cell, LEFT, buff=1.5)
        arrow_in = Arrow(start=nutrient_in.get_right(), end=growth_cell.get_left(), color=COLOR_ARROW)
        
        self.play(FadeIn(nutrient_in), GrowArrow(arrow_in))
        self.play(
            Transform(nutrient_in, Circle(radius=0.1, color=COLOR_HIGHLIGHT, fill_opacity=1).move_to(growth_cell.get_center())),
            growth_cell.animate.scale(1.1) # Simulate growth
        )
        self.play(FadeOut(arrow_in))
        self.wait(1.5)
        self.play(FadeOut(func1_txt), FadeOut(nutrient_in), FadeOut(growth_cell))

        # --- Scene 9: Function - Reproduction ---
        self.play(functions_title.animate.to_edge(UP, buff=0.5)) 

        func2_txt_current = Text("2. Reproduction", color=COLOR_TEXT).center().shift(UP*1.5)
        self.play(Write(func2_txt_current))

        # Visual: One cell divides into two
        original_cell = VGroup(
            Circle(radius=1, color=COLOR_CELL_MEMBRANE, stroke_width=4), 
            Circle(radius=0.95, color=COLOR_CYTOPLASM, fill_opacity=0.7)
        ).center()
        self.play(FadeIn(original_cell))
        self.wait(1)

        # Simulating division by transforming one into two
        cell_left = original_cell.copy().shift(LEFT*1.5)
        cell_right = original_cell.copy().shift(RIGHT*1.5)

        self.play(
            Transform(original_cell, VGroup(cell_left, cell_right)) # Morph one into two
        )
        self.wait(2)
        self.play(FadeOut(func2_txt_current), FadeOut(original_cell))

        # --- Scene 10: Function - Response to Environment ---
        func3_txt_current = Text("3. Response to Environment", color=COLOR_TEXT).center().shift(UP*1.5)
        self.play(Write(func3_txt_current))

        # Visual: Cell reacts to a stimulus
        response_cell = VGroup(
            Circle(radius=1.5, color=COLOR_CELL_MEMBRANE, stroke_width=4), 
            Circle(radius=1.45, color=COLOR_CYTOPLASM, fill_opacity=0.7)
        ).center().shift(LEFT*1.5)
        stimulus_arrow = Arrow(start=RIGHT*3, end=response_cell.get_right(), color=COLOR_STIMULUS, stroke_width=6)
        stimulus_label = Text("Stimulus", font_size=24, color=COLOR_STIMULUS).next_to(stimulus_arrow, UP)

        self.play(FadeIn(response_cell))
        self.play(GrowArrow(stimulus_arrow), FadeIn(stimulus_label))
        
        # Cell recoils/shifts in response
        self.play(response_cell.animate.shift(LEFT*0.5), stimulus_arrow.animate.shift(LEFT*0.5), stimulus_label.animate.shift(LEFT*0.5))
        self.wait(1.5)
        self.play(FadeOut(func3_txt_current), FadeOut(response_cell), FadeOut(stimulus_arrow), FadeOut(stimulus_label))
        self.play(FadeOut(functions_title))

        # --- Scene 11: Recap / Conclusion ---
        recap_text1 = Text("Cells: The fundamental building blocks of life.", font_size=36, color=COLOR_TEXT)
        recap_text2 = Text("Next: Practice with flashcards or chat with Erica!", font_size=30, color=COLOR_HIGHLIGHT).next_to(recap_text1, DOWN, buff=1)
        
        self.play(Write(recap_text1))
        self.wait(2)
        self.play(FadeIn(recap_text2, shift=DOWN))
        self.wait(3)
        self.play(FadeOut(recap_text1, shift=UP), FadeOut(recap_text2, shift=UP))