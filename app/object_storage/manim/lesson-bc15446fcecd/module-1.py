from manim import *

class ComputerScienceConcept(Scene):
    def construct(self):
        # Create a central "processor" square
        processor = Square(side_length=2).set_fill(GREY_D, opacity=0.8).set_stroke(WHITE, width=2)
        self.add(processor)

        # Create input and output data representations (circles)
        input_data = Circle(radius=0.2, color=BLUE_A).next_to(processor, LEFT, buff=0.8)
        output_data = Circle(radius=0.2, color=GREEN_A).next_to(processor, RIGHT, buff=0.8)

        # 1. Input appears and moves into the processor
        self.play(
            FadeIn(input_data, shift=LEFT * 0.5), # Input data fades in from the left
            run_time=0.3
        )
        self.play(
            input_data.animate.move_to(processor.center), # Input data moves into the center of the processor
            run_time=0.5,
            rate_func=linear
        )
        self.remove(input_data) # The input data is "processed" and disappears inside

        # 2. Processor animates to indicate processing
        self.play(
            processor.animate.set_fill(YELLOW, opacity=0.8), # Processor flashes yellow
            run_time=0.2
        )
        self.play(
            processor.animate.set_fill(GREY_D, opacity=0.8), # Processor returns to original color
            run_time=0.2
        )

        # 3. Output emerges from the processor
        self.play(
            FadeIn(output_data, shift=RIGHT * 0.5), # Output data fades in and moves to the right
            run_time=0.5
        )
        
        self.wait(0.3) # Hold the final state briefly