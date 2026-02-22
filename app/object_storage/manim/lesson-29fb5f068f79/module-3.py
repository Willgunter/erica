from manim import *

# Configuration for colors (consistent with 3B1B dark theme)
BLUE_DARK = ManimColor("#3D84D9") # A slightly darker blue than BLUE_A, similar to 3B1B
GOLD_LIGHT = ManimColor("#FFD700") # Gold color
TEXT_COLOR = WHITE

# Helper function to create a quadratic curve
def get_quadratic_curve(a, b, c, x_range=(-5.5, 5.5, 0.01), color=BLUE_DARK):
    return FunctionGraph(
        lambda x: a * x**2 + b * x + c,
        x_range=x_range,
        color=color
    )

class TheDiscriminantAnimation(Scene):
    def construct(self):
        # 0. Initial Setup
        self.camera.background_color = BLACK

        # Title
        title = Text("The Discriminant: Solutions and Geometry", font_size=50, color=GOLD_LIGHT).to_edge(UP)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(0.5)

        # 1. Visual Hook - Introduce Parabola and Roots
        # Axes and NumberPlane
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": LIGHT_GRAY, "stroke_opacity": 0.5},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).shift(0.5*DOWN) # Shift down to make space for title later
        
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False
        ).shift(0.5*DOWN)

        x_axis_label = Text("x", color=WHITE, font_size=30).next_to(axes.x_axis.get_end(), RIGHT)
        y_axis_label = Text("y", color=WHITE, font_size=30).next_to(axes.y_axis.get_end(), UP)
        axes_labels = VGroup(x_axis_label, y_axis_label)

        self.play(Create(plane), Create(axes), Create(axes_labels), run_time=2)
        self.wait(0.5)

        # Initial parabola with two roots (a=1, b=0, c=-2)
        parabola_initial = get_quadratic_curve(1, 0, -2)
        
        # Calculate roots for display
        root1_coord = axes.c2p(-np.sqrt(2), 0)
        root2_coord = axes.c2p(np.sqrt(2), 0)
        
        root1_dot_initial = Dot(root1_coord, color=GOLD_LIGHT, radius=0.1)
        root2_dot_initial = Dot(root2_coord, color=GOLD_LIGHT, radius=0.1)
        
        roots_dots_initial = VGroup(root1_dot_initial, root2_dot_initial)

        intro_text = Text("A parabola can have...", font_size=40, color=TEXT_COLOR).next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(intro_text), run_time=1)
        self.play(Create(parabola_initial), FadeIn(roots_dots_initial), run_time=2)
        self.wait(1)
        
        # 2. Case 1: Two Real Solutions (Discriminant > 0)
        two_solutions_text = Text("Two Real Solutions", font_size=45, color=GOLD_LIGHT).next_to(title, DOWN, buff=0.8)
        
        # Construct b^2 - 4ac > 0 using Text objects
        b_squared_gt = VGroup(
            Text("b", font_size=40, color=BLUE_DARK),
            Text("2", font_size=20, color=BLUE_DARK).shift(0.2*UP + 0.1*RIGHT),
        ).arrange(RIGHT, buff=0.01) # Use a small buff to make 'b' and '2' close
        discriminant_gt_0_text = VGroup(
            b_squared_gt,
            Text(" - 4ac > 0", font_size=40, color=BLUE_DARK)
        ).arrange(RIGHT, buff=0.1).next_to(two_solutions_text, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(intro_text, two_solutions_text),
            FadeIn(discriminant_gt_0_text), # Fade in the whole VGroup
            run_time=1.5
        )
        self.wait(0.5)

        # Emphasize roots
        self.play(
            roots_dots_initial.animate.scale(1.5).set_color(BLUE_DARK),
            run_time=0.5
        )
        self.play(
            roots_dots_initial.animate.scale(1/1.5).set_color(GOLD_LIGHT),
            run_time=0.5
        )
        self.wait(1)

        # 3. Case 2: One Real Solution (Discriminant = 0)
        # Parabola that touches x-axis at one point (a=1, b=0, c=0)
        parabola_one_root = get_quadratic_curve(1, 0, 0)
        root_coord_one = axes.c2p(0, 0)
        root_dot_one = Dot(root_coord_one, color=GOLD_LIGHT, radius=0.1)

        one_solution_text = Text("One Real Solution", font_size=45, color=GOLD_LIGHT).next_to(title, DOWN, buff=0.8)
        
        # Construct b^2 - 4ac = 0
        b_squared_eq = VGroup(
            Text("b", font_size=40, color=BLUE_DARK),
            Text("2", font_size=20, color=BLUE_DARK).shift(0.2*UP + 0.1*RIGHT),
        ).arrange(RIGHT, buff=0.01)
        discriminant_eq_0_text = VGroup(
            b_squared_eq,
            Text(" - 4ac = 0", font_size=40, color=BLUE_DARK)
        ).arrange(RIGHT, buff=0.1).next_to(one_solution_text, DOWN, buff=0.5)
        
        self.play(
            Transform(parabola_initial, parabola_one_root),
            ReplacementTransform(two_solutions_text, one_solution_text),
            FadeOut(roots_dots_initial),
            FadeIn(root_dot_one),
            ReplacementTransform(discriminant_gt_0_text, discriminant_eq_0_text),
            run_time=2
        )
        self.wait(1)

        # Emphasize the single root
        self.play(
            root_dot_one.animate.scale(1.5).set_color(BLUE_DARK),
            run_time=0.5
        )
        self.play(
            root_dot_one.animate.scale(1/1.5).set_color(GOLD_LIGHT),
            run_time=0.5
        )
        self.wait(1)

        # 4. Case 3: No Real Solutions (Discriminant < 0)
        # Parabola that does not intersect x-axis (a=1, b=0, c=2)
        parabola_no_roots = get_quadratic_curve(1, 0, 2)
        
        no_solutions_text = Text("No Real Solutions", font_size=45, color=GOLD_LIGHT).next_to(title, DOWN, buff=0.8)
        
        # Construct b^2 - 4ac < 0
        b_squared_lt = VGroup(
            Text("b", font_size=40, color=BLUE_DARK),
            Text("2", font_size=20, color=BLUE_DARK).shift(0.2*UP + 0.1*RIGHT),
        ).arrange(RIGHT, buff=0.01)
        discriminant_lt_0_text = VGroup(
            b_squared_lt,
            Text(" - 4ac < 0", font_size=40, color=BLUE_DARK)
        ).arrange(RIGHT, buff=0.1).next_to(no_solutions_text, DOWN, buff=0.5)

        self.play(
            Transform(parabola_one_root, parabola_no_roots),
            ReplacementTransform(one_solution_text, no_solutions_text),
            FadeOut(root_dot_one),
            ReplacementTransform(discriminant_eq_0_text, discriminant_lt_0_text),
            run_time=2
        )
        self.wait(1.5)

        # Introduce the Discriminant expression explicitly as "the Discriminant"
        b_squared_final = VGroup(
            Text("b", font_size=50, color=BLUE_DARK),
            Text("2", font_size=25, color=BLUE_DARK).shift(0.25*UP + 0.12*RIGHT),
        ).arrange(RIGHT, buff=0.01)
        discriminant_formula_text_final = VGroup(
            b_squared_final,
            Text(" - 4ac", font_size=50, color=BLUE_DARK)
        ).arrange(RIGHT, buff=0.1).shift(0.5*UP)
        
        discriminant_label_final = Text("The Discriminant", font_size=40, color=TEXT_COLOR).next_to(discriminant_formula_text_final, DOWN, buff=0.5)

        # Fade out existing elements to focus on the formula
        self.play(
            FadeOut(no_solutions_text),
            FadeOut(discriminant_lt_0_text),
            FadeOut(parabola_no_roots),
            FadeOut(plane),
            FadeOut(axes),
            FadeOut(axes_labels),
            # Transition the last discriminant text (which is discriminant_lt_0_text) to the focused formula
            Transform(discriminant_lt_0_text.copy().clear_updaters(), discriminant_formula_text_final),
            FadeIn(discriminant_label_final),
            run_time=1.5
        )
        # Remove the old discriminant_lt_0_text now that its copy has transformed
        self.remove(discriminant_lt_0_text)
        self.wait(2)


        # 5. Recap Card
        self.play(
            FadeOut(title),
            FadeOut(discriminant_formula_text_final),
            FadeOut(discriminant_label_final),
            run_time=1
        )
        
        recap_title = Text("Recap: The Discriminant", font_size=50, color=GOLD_LIGHT).to_edge(UP)
        
        # Case 1 Recap Text
        b_squared_recap1 = VGroup(
            Text("b", font_size=35, color=BLUE_DARK),
            Text("2", font_size=18, color=BLUE_DARK).shift(0.2*UP + 0.09*RIGHT),
        ).arrange(RIGHT, buff=0.01)
        case1_text = VGroup(
            b_squared_recap1,
            Text(" - 4ac > 0:", font_size=35, color=BLUE_DARK),
            Text(" Two Real Solutions", font_size=35, color=TEXT_COLOR)
        ).arrange(RIGHT, buff=0.05)

        # Case 2 Recap Text
        b_squared_recap2 = VGroup(
            Text("b", font_size=35, color=BLUE_DARK),
            Text("2", font_size=18, color=BLUE_DARK).shift(0.2*UP + 0.09*RIGHT),
        ).arrange(RIGHT, buff=0.01)
        case2_text = VGroup(
            b_squared_recap2,
            Text(" - 4ac = 0:", font_size=35, color=BLUE_DARK),
            Text(" One Real Solution", font_size=35, color=TEXT_COLOR)
        ).arrange(RIGHT, buff=0.05)

        # Case 3 Recap Text
        b_squared_recap3 = VGroup(
            Text("b", font_size=35, color=BLUE_DARK),
            Text("2", font_size=18, color=BLUE_DARK).shift(0.2*UP + 0.09*RIGHT),
        ).arrange(RIGHT, buff=0.01)
        case3_text = VGroup(
            b_squared_recap3,
            Text(" - 4ac < 0:", font_size=35, color=BLUE_DARK),
            Text(" No Real Solutions", font_size=35, color=TEXT_COLOR)
        ).arrange(RIGHT, buff=0.05)

        recap_group = VGroup(case1_text, case2_text, case3_text).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        self.play(FadeIn(recap_title), run_time=1)
        self.play(LaggedStart(
            FadeIn(case1_text),
            FadeIn(case2_text),
            FadeIn(case3_text),
            lag_ratio=0.5,
            run_time=3
        ))
        self.wait(3)

        self.play(FadeOut(recap_title), FadeOut(recap_group), run_time=1)