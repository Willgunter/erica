from manim import *

class ComputerScienceProcessing(Scene):
    def construct(self):
        # Create a central 'processor' unit (a square)
        processor = Square(side_length=2).set_color(BLUE_D)
        
        # Create an input arrow
        input_arrow = Arrow(
            start=LEFT * 4, 
            end=processor.get_left(), 
            buff=0.1, 
            stroke_width=6, 
            max_tip_length_to_length_ratio=0.15
        ).set_color(YELLOW)
        
        # Create an output arrow
        output_arrow = Arrow(
            start=processor.get_right(), 
            end=RIGHT * 4, 
            buff=0.1, 
            stroke_width=6, 
            max_tip_length_to_length_ratio=0.15
        ).set_color(GREEN)
        
        # Animate the sequence: Processor appears, data flows in, processing happens, data flows out.
        self.play(Create(processor), run_time=0.5)
        self.play(Create(input_arrow), run_time=0.5)
        self.play(Indicate(processor, scale_factor=1.2, color=RED), run_time=0.4)
        self.play(Create(output_arrow), run_time=0.5)
        
        # Hold the final state briefly
        self.wait(0.1)