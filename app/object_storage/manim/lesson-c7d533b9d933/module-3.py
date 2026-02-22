from manim import *

class ParabolicNatureSolutions(Scene):
    def construct(self):
        # 1. Configuration: Dark background, high-contrast colors
        self.camera.background_color = "#1a1a1a" # Clean dark background
        BLUE_ACCENT = "#50d8ed" # Bright blue accent
        GOLD_ACCENT = "#ffc107" # Rich gold accent
        TEXT_COLOR = WHITE

        # --- Beat 1: The Parabola Emerges (Visual Hook) ---
        title = Text("Parabolic Nature & Solution Types", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create Axes for the graph
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 6, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": DARK_GRAY, "include_numbers": False},
        ).to_edge(DOWN).shift(UP * 0.5) # Position axes centrally at the bottom
        
        # Labels for axes
        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=DL).set_color(TEXT_COLOR)
        y_label = axes.get_y_axis_label("y", edge=UP, direction=UP).set_color(TEXT_COLOR)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # Initial parabola: y = x^2 (basic form)
        parabola_func = lambda x: x**2
        parabola = axes.get_graph(parabola_func, color=BLUE_ACCENT, stroke_width=5)
        
        # Text introduction
        intro_text = Text(
            "Every quadratic equation forms a parabola.", 
            font_size=32, 
            color=TEXT_COLOR
        ).next_to(title, DOWN, buff=0.5).to_edge(RIGHT)
        
        self.play(
            Create(parabola, run_time=2), # Strong visual hook: parabola drawing itself
            FadeIn(intro_text, shift=DOWN)
        )
        self.wait(1)

        # Introduce general form
        general_form = MathTex("y = ax^2 + bx + c", color=GOLD_ACCENT).next_to(intro_text, DOWN, buff=0.5)
        general_form.align_to(intro_text, LEFT)
        self.play(Write(general_form))
        self.wait(1.5)
        
        self.play(FadeOut(intro_text)) # Clean up intro text

        # --- Beat 2: Shape and Vertex (Coefficient 'a' and turning point) ---
        a_effect_text = Text(
            "Coefficient 'a' controls width & direction.", 
            font_size=28, 
            color=TEXT_COLOR
        ).to_edge(LEFT).shift(UP*1.5)
        
        # Show 'a' influence by transforming the parabola
        parabola_a1 = axes.get_graph(lambda x: 0.5 * x**2, color=BLUE_ACCENT, stroke_width=5) # Wider
        parabola_a2 = axes.get_graph(lambda x: 2 * x**2, color=BLUE_ACCENT, stroke_width=5)   # Narrower
        parabola_a3 = axes.get_graph(lambda x: -0.5 * x**2, color=BLUE_ACCENT, stroke_width=5) # Opens downwards

        self.play(FadeIn(a_effect_text, shift=LEFT))
        self.play(Transform(parabola, parabola_a1), run_time=1)
        self.wait(0.5)
        self.play(Transform(parabola, parabola_a2), run_time=1)
        self.wait(0.5)
        self.play(Transform(parabola, parabola_a3), run_time=1)
        self.wait(0.5)
        
        # Reset parabola and highlight the vertex
        parabola_reset = axes.get_graph(lambda x: x**2 - 1, color=BLUE_ACCENT, stroke_width=5) # Shifted down to cross x-axis
        vertex_dot = Dot(axes.c2p(0, -1), color=GOLD_ACCENT)
        vertex_label = MathTex("\\text{Vertex}", color=GOLD_ACCENT).next_to(vertex_dot, DR, buff=0.1)
        
        self.play(
            Transform(parabola, parabola_reset), 
            FadeOut(a_effect_text),
            run_time=1
        )
        self.wait(0.5)
        
        vertex_text = Text("The vertex is the turning point.", font_size=28, color=TEXT_COLOR).to_edge(LEFT).shift(UP*1.5)
        self.play(Create(vertex_dot), Write(vertex_label), FadeIn(vertex_text, shift=LEFT))
        self.wait(1.5)

        self.play(FadeOut(vertex_dot), FadeOut(vertex_label), FadeOut(vertex_text))
        
        # --- Beat 3: X-intercepts (Solutions/Roots) ---
        # Adjust general form position for new text
        self.play(general_form.animate.next_to(title, DOWN, buff=0.5).align_to(title, LEFT))
        
        roots_intro_text = Text(
            "Solutions are where the parabola crosses the x-axis.", 
            font_size=32, 
            color=TEXT_COLOR
        ).next_to(general_form, DOWN, buff=0.5).to_edge(RIGHT)
        
        # Highlight x-axis
        x_axis_highlight = axes.get_x_axis().copy().set_color(GOLD_ACCENT).set_stroke(width=4)
        
        self.play(FadeIn(roots_intro_text, shift=DOWN), Create(x_axis_highlight))
        self.wait(1)

        # Show two distinct real roots
        roots_p1 = Dot(axes.c2p(-1, 0), color=BLUE_ACCENT)
        roots_p2 = Dot(axes.c2p(1, 0), color=BLUE_ACCENT)
        
        self.play(FadeIn(roots_p1), FadeIn(roots_p2))
        self.wait(1)
        self.play(FadeOut(roots_intro_text)) # Clean up intro text

        # --- Beat 4: Three Types of Solutions ---
        # Case 1: Two distinct real solutions (already shown, just label it)
        case1_label = Text("Case 1: Two Real Solutions", font_size=32, color=GOLD_ACCENT).next_to(general_form, DOWN, buff=0.5).to_edge(RIGHT)
        self.play(Write(case1_label))
        self.wait(1.5)

        # Case 2: One real solution (parabola touches x-axis at vertex)
        parabola_one_root = axes.get_graph(lambda x: x**2, color=BLUE_ACCENT, stroke_width=5)
        # Transform current roots to a single one
        single_root_dot = Dot(axes.c2p(0, 0), color=BLUE_ACCENT)
        
        self.play(
            Transform(parabola, parabola_one_root),
            Transform(roots_p1, single_root_dot), # Move p1 to (0,0)
            FadeOut(roots_p2), # Fade out p2
            FadeOut(case1_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        case2_label = Text("Case 2: One Real Solution", font_size=32, color=GOLD_ACCENT).next_to(general_form, DOWN, buff=0.5).to_edge(RIGHT)
        self.play(Write(case2_label))
        self.wait(1.5)

        # Case 3: No real solutions (parabola above x-axis, doesn't intersect)
        parabola_no_roots = axes.get_graph(lambda x: x**2 + 1, color=BLUE_ACCENT, stroke_width=5)
        
        self.play(
            Transform(parabola, parabola_no_roots),
            FadeOut(single_root_dot), # The single dot also fades out
            FadeOut(case2_label),
            run_time=1.5
        )
        self.wait(0.5)

        case3_label = Text("Case 3: No Real Solutions", font_size=32, color=GOLD_ACCENT).next_to(general_form, DOWN, buff=0.5).to_edge(RIGHT)
        self.play(Write(case3_label))
        self.wait(2)
        
        self.play(FadeOut(case3_label))

        # --- Beat 5: Recap Card ---
        self.play(
            FadeOut(parabola), 
            FadeOut(x_axis_highlight), 
            FadeOut(axes), 
            FadeOut(x_label), 
            FadeOut(y_label),
            FadeOut(general_form),
            FadeOut(title)
        )
        self.wait(0.5)

        recap_title = Text("Recap: Parabolic Solutions", font_size=48, color=GOLD_ACCENT).to_edge(UP)
        
        bullet1 = MathTex("\\bullet \\text{ Quadratic Equations = Parabolas}", color=TEXT_COLOR).scale(0.8).next_to(recap_title, DOWN, buff=1.0).align_to(recap_title, LEFT)
        bullet1_form = MathTex("(y = ax^2 + bx + c)", color=GOLD_ACCENT).scale(0.8).next_to(bullet1, RIGHT, buff=0.2)
        
        bullet2 = MathTex("\\bullet \\text{ Solutions = X-intercepts}", color=TEXT_COLOR).scale(0.8).next_to(bullet1, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet3 = MathTex("\\bullet \\text{ Three Types:}", color=TEXT_COLOR).scale(0.8).next_to(bullet2, DOWN, buff=0.5).align_to(bullet1, LEFT)
        bullet3_sub1 = Text(" - Two Real", font_size=28, color=BLUE_ACCENT).next_to(bullet3, DOWN, buff=0.2).align_to(bullet3, LEFT).shift(RIGHT*0.5)
        bullet3_sub2 = Text(" - One Real", font_size=28, color=BLUE_ACCENT).next_to(bullet3_sub1, DOWN, buff=0.1).align_to(bullet3_sub1, LEFT)
        bullet3_sub3 = Text(" - No Real", font_size=28, color=BLUE_ACCENT).next_to(bullet3_sub2, DOWN, buff=0.1).align_to(bullet3_sub1, LEFT)

        self.play(
            Write(recap_title),
            LaggedStart(
                FadeIn(bullet1, shift=LEFT), FadeIn(bullet1_form, shift=LEFT),
                FadeIn(bullet2, shift=LEFT),
                FadeIn(bullet3, shift=LEFT),
                FadeIn(bullet3_sub1, shift=LEFT),
                FadeIn(bullet3_sub2, shift=LEFT),
                FadeIn(bullet3_sub3, shift=LEFT),
                lag_ratio=0.3
            )
        )
        self.wait(4)
        self.play(FadeOut(VGroup(recap_title, bullet1, bullet1_form, bullet2, bullet3, bullet3_sub1, bullet3_sub2, bullet3_sub3)))
        self.wait(1)