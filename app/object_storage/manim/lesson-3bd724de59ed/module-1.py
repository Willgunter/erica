from manim import *

class DataProcessing(Scene):
    def construct(self):
        # Define basic shapes for input, output, and processor
        input_data = Square(color=BLUE, stroke_width=7).scale(0.5)
        output_data = Circle(color=RED, stroke_width=7).scale(0.5)
        processor = Rectangle(width=2, height=1, color=WHITE, fill_opacity=0.1, stroke_opacity=0.5, stroke_width=5)
        
        # Position objects initially
        input_data.to_edge(LEFT, buff=1.5)
        processor.move_to(ORIGIN)
        
        # Animation sequence
        # 1. Input data appears
        self.play(Create(input_data), run_time=0.25)

        # 2. Processor appears
        self.play(FadeIn(processor), run_time=0.25)
        
        # 3. Input data moves towards the processor
        self.play(input_data.animate.move_to(processor.get_left()), run_time=0.3)
        
        # 4. Input enters processor and transforms (processor highlights)
        self.play(
            input_data.animate.move_to(processor.get_center()),
            FadeOut(input_data),
            processor.animate.set_stroke_opacity(1).set_stroke_width(7), # Highlight processor
            run_time=0.4
        )
        
        # 5. Output data emerges from the processor (processor returns to normal)
        self.play(
            FadeIn(output_data.move_to(processor.get_center())),
            processor.animate.set_stroke_opacity(0.5).set_stroke_width(5), # De-highlight processor
            run_time=0.4
        )
        
        # 6. Output data moves away
        self.play(output_data.animate.to_edge(RIGHT, buff=1.5), FadeOut(processor), run_time=0.3)

        # Ensure the scene lasts approximately 2 seconds
        # Total run_time: 0.25 + 0.25 + 0.3 + 0.4 + 0.4 + 0.3 = 1.9 seconds
        self.wait(0.1) # Short final pause