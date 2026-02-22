from manim import *

class ExponentialGrowthModule(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = BLACK
        BLUE_ACCENT = BLUE_C
        GOLD_ACCENT = GOLD_A
        TEXT_COLOR = WHITE
        
        # --- Beat 1: Visual Hook - Rapid Multiplication Intuition ---
        # Title Card
        title = Text("Exponential Growth", font_size=50, color=BLUE_ACCENT)
        subtitle = Text("Understanding Rapid Change", font_size=30, color=GOLD_ACCENT).next_to(title, DOWN)
        self.play(FadeIn(title, shift=UP), FadeIn(subtitle, shift=DOWN))
        self.wait(1)
        self.play(FadeOut(title, shift=UP), FadeOut(subtitle, shift=DOWN))

        # Initial 'cell'
        initial_cell = Dot(point=LEFT * 3, radius=0.2, color=BLUE_ACCENT, z_index=1)
        initial_text = Text("Start", font_size=24, color=GOLD_ACCENT).next_to(initial_cell, DOWN)
        self.play(FadeIn(initial_cell, scale=0.5), FadeIn(initial_text))
        self.wait(0.5)

        # Simulate splitting
        cells = VGroup(initial_cell)
        num_splits = 3
        positions = [
            [LEFT * 4, UP * 1], [LEFT * 4, DOWN * 1], # 2 cells
            [LEFT * 2, UP * 2], [LEFT * 2, UP * 0], [LEFT * 2, DOWN * 0], [LEFT * 2, DOWN * 2], # 4 cells
            [RIGHT * 0, UP * 2.5], [RIGHT * 0, UP * 1.5], [RIGHT * 0, UP * 0.5], [RIGHT * 0, DOWN * 0.5],
            [RIGHT * 0, DOWN * 1.5], [RIGHT * 0, DOWN * 2.5], [RIGHT * 0, UP * 0], [RIGHT * 0, DOWN * 0] # 8 cells (not fully distinct positions but implies multiplication)
        ]
        
        # Simple animation of dots multiplying, implying division
        current_cells = VGroup(initial_cell)
        growth_text = Text("Rapid Multiplication!", font_size=30, color=GOLD_ACCENT).move_to(RIGHT * 3 + UP * 2)
        self.play(FadeIn(growth_text))

        for i in range(num_splits):
            new_cells = VGroup()
            for j, cell in enumerate(current_cells):
                if len(cells) < 16: # Limit for visual clarity
                    new_dot_1 = Dot(radius=0.15, color=BLUE_ACCENT, z_index=1).move_to(cell.get_center() + RIGHT * 0.5)
                    new_dot_2 = Dot(radius=0.15, color=BLUE_ACCENT, z_index=1).move_to(cell.get_center() + LEFT * 0.5)
                    
                    self.play(
                        Transform(cell, Dot(radius=0.1, color=BLUE_ACCENT).move_to(cell.get_center() + UP * 0.2)),
                        FadeIn(new_dot_1.next_to(cell, UP + RIGHT, buff=SMALL_BUFF)),
                        FadeIn(new_dot_2.next_to(cell, DOWN + LEFT, buff=SMALL_BUFF)),
                        run_time=0.4
                    )
                    new_cells.add(new_dot_1, new_dot_2)
            current_cells.add(new_cells)
            cells.add(new_cells)
            self.play(cells.animate.arrange_in_grid(rows=1, buff=0.2).scale(0.8).move_to(ORIGIN), run_time=0.8) # Keep them somewhat organized

        self.wait(1)
        self.play(FadeOut(cells), FadeOut(initial_text), FadeOut(growth_text))
        self.wait(0.5)

        # --- Beat 2: Linear vs. Exponential Growth (Comparison on Graph) ---
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 15, 2],
            x_length=6,
            y_length=5,
            axis_config={"color": GRAY_A},
            tips=False
        ).to_edge(LEFT, buff=0.8)

        labels = axes.get_axis_labels(x_label="Time (x)", y_label="Quantity (y)")
        self.play(Create(axes), Write(labels))

        # Linear function: y = x
        linear_graph = axes.plot(lambda x: x, color=GOLD_ACCENT)
        linear_label = MathTex(r"y = x", color=GOLD_ACCENT).next_to(linear_graph, UP + LEFT, buff=0.2)
        linear_text = Text("Linear Growth", color=GOLD_ACCENT, font_size=25).next_to(linear_graph, RIGHT, buff=0.5)
        
        # Exponential function: y = 1.5^x
        exp_graph = axes.plot(lambda x: 1.5**x, color=BLUE_ACCENT)
        exp_label = MathTex(r"y = 1.5^x", color=BLUE_ACCENT).next_to(exp_graph, UP + RIGHT, buff=0.2)
        exp_text = Text("Exponential Growth", color=BLUE_ACCENT, font_size=25).next_to(exp_graph, RIGHT, buff=0.5)
        
        self.play(Create(linear_graph), Write(linear_text), run_time=1.5)
        self.wait(0.5)
        self.play(
            Create(exp_graph), 
            ReplacementTransform(linear_text, exp_text), 
            run_time=2
        )
        self.wait(1)

        self.play(
            FadeOut(exp_text),
            FadeIn(linear_label),
            FadeIn(exp_label)
        )
        self.wait(1)

        # --- Beat 3: Formal Notation - The Formula ---
        formula_main = MathTex(r"y = a \cdot b^x", font_size=60, color=TEXT_COLOR).to_edge(RIGHT, buff=1)
        
        self.play(
            FadeTransform(linear_label, formula_main[0][0:1]), # y
            FadeTransform(exp_label, formula_main[0][2:])      # = ... b^x
        )
        self.play(Write(formula_main[0][1:2]), run_time=0.5) # =
        self.wait(0.5)

        # Highlight and explain components
        a_label = MathTex(r"a \text{ (initial amount)}", font_size=30, color=GOLD_ACCENT).next_to(formula_main, UP, buff=0.5).shift(LEFT*0.5)
        self.play(FadeToColor(formula_main[0][2], GOLD_ACCENT), Write(a_label))
        self.wait(0.8)
        self.play(FadeToColor(formula_main[0][2], TEXT_COLOR), FadeOut(a_label))

        b_label = MathTex(r"b \text{ (growth factor)}", font_size=30, color=BLUE_ACCENT).next_to(formula_main, UP, buff=0.5).shift(RIGHT*0.5)
        self.play(FadeToColor(formula_main[0][4], BLUE_ACCENT), Write(b_label))
        self.wait(0.8)
        self.play(FadeToColor(formula_main[0][4], TEXT_COLOR), FadeOut(b_label))
        
        x_label = MathTex(r"x \text{ (time/steps)}", font_size=30, color=GOLD_ACCENT).next_to(formula_main, DOWN, buff=0.5)
        self.play(FadeToColor(formula_main[0][6], GOLD_ACCENT), Write(x_label))
        self.wait(0.8)
        self.play(FadeToColor(formula_main[0][6], TEXT_COLOR), FadeOut(x_label))

        self.wait(1)
        
        # --- Beat 4: Parameter Effect - Growth Factor 'b' ---
        self.play(
            FadeOut(formula_main),
            axes.animate.to_edge(LEFT, buff=0.8), # Ensure axes are still prominent
            Uncreate(linear_graph),
            Uncreate(exp_graph) # Clear existing curves
        )

        initial_exp_graph = axes.plot(lambda x: 1.2**x, color=BLUE_ACCENT, stroke_width=4)
        initial_exp_label = MathTex(r"b = 1.2", font_size=30, color=BLUE_ACCENT).next_to(initial_exp_graph, UP + RIGHT, buff=0.2)
        
        self.play(Create(initial_exp_graph), Write(initial_exp_label))
        self.wait(0.5)

        # Transform to higher 'b'
        medium_exp_graph = axes.plot(lambda x: 1.8**x, color=BLUE_ACCENT, stroke_width=4)
        medium_exp_label = MathTex(r"b = 1.8", font_size=30, color=BLUE_ACCENT).next_to(medium_exp_graph, UP + RIGHT, buff=0.2)
        self.play(Transform(initial_exp_graph, medium_exp_graph), Transform(initial_exp_label, medium_exp_label))
        self.wait(0.5)

        # Transform to even higher 'b'
        fast_exp_graph = axes.plot(lambda x: 2.5**x, color=BLUE_ACCENT, stroke_width=4)
        fast_exp_label = MathTex(r"b = 2.5", font_size=30, color=BLUE_ACCENT).next_to(fast_exp_graph, UP + RIGHT, buff=0.2)
        self.play(Transform(initial_exp_graph, fast_exp_graph), Transform(initial_exp_label, fast_exp_label))
        self.wait(1)

        growth_factor_impact = Text("Larger 'b' means faster growth!", font_size=35, color=GOLD_ACCENT).move_to(RIGHT * 3.5 + UP * 2)
        self.play(Write(growth_factor_impact))
        self.wait(1.5)
        self.play(FadeOut(growth_factor_impact))

        # --- Beat 5: Bio Example - Bacterial Growth ---
        bio_title = Text("Bacterial Growth", font_size=40, color=BLUE_ACCENT).to_edge(UP, buff=0.5)
        
        self.play(
            FadeOut(initial_exp_label),
            FadeIn(bio_title)
        )
        self.wait(0.5)

        # Animate a growing circle along the curve
        colony = Circle(radius=0.1, color=BLUE_A, fill_opacity=0.8).move_to(axes.c2p(0, 1))
        
        colony_text = Text("Colony Size", font_size=25, color=GOLD_ACCENT).next_to(colony, RIGHT)
        self.play(FadeIn(colony), FadeIn(colony_text))
        
        # Animate colony growing along the exponential curve
        path = Line(axes.c2p(0, 1), axes.c2p(6, 2.5**6)).set_opacity(0) # Invisible path for movement
        
        def update_colony(mobj, alpha):
            x_val = 6 * alpha
            y_val = 2.5**x_val
            mobj.move_to(axes.c2p(x_val, y_val))
            mobj.set_width(0.1 + 0.05 * y_val) # Grow in size proportionally to y
            mobj.set_fill(color=interpolate_color(BLUE_A, BLUE_C, alpha)) # Change color slightly
        
        self.play(
            UpdateFromAlphaFunc(colony, update_colony),
            FadeOut(colony_text),
            run_time=4,
            rate_func=linear # Linear alpha for movement along x-axis
        )

        bio_label = Text("Rapid increase in cell count!", font_size=30, color=GOLD_ACCENT).move_to(RIGHT*3.5 + DOWN*2)
        self.play(Write(bio_label))
        self.wait(1.5)

        self.play(
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(initial_exp_graph),
            FadeOut(colony),
            FadeOut(bio_title),
            FadeOut(bio_label)
        )
        self.wait(0.5)

        # --- Recap Card ---
        recap_title = Text("Exponential Growth: Key Takeaways", font_size=45, color=BLUE_ACCENT).to_edge(UP, buff=0.8)

        bullet1 = BulletedList(
            "Describes rapid, accelerating growth.",
            font_size=35, color=TEXT_COLOR
        ).next_to(recap_title, DOWN, buff=0.8).align_to(LEFT, DR * 2).shift(LEFT * 1.5)
        
        bullet2 = BulletedList(
            "Defined by a 'growth factor' (b > 1).",
            font_size=35, color=TEXT_COLOR
        ).next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)

        bullet3 = BulletedList(
            "Crucial for understanding biology (populations, bacteria, viruses).",
            font_size=35, color=TEXT_COLOR
        ).next_to(bullet2, DOWN, buff=0.5).align_to(bullet1, LEFT)

        self.play(FadeIn(recap_title, shift=UP))
        self.play(LaggedStart(
            FadeIn(bullet1, shift=LEFT),
            FadeIn(bullet2, shift=LEFT),
            FadeIn(bullet3, shift=LEFT),
            lag_ratio=0.5
        ))
        self.wait(3)
        self.play(
            FadeOut(recap_title),
            FadeOut(bullet1),
            FadeOut(bullet2),
            FadeOut(bullet3)
        )
        self.wait(1)