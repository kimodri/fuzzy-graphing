import argparse
import random
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from fuzzygraphing import FuzzyGraph, TrapMF, TriMF

def get_slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x2 - x1 == 0:
        raise ValueError("Cannot calculate slope for vertical line (x1 == x2).")
    return (y2 - y1) / (x2 - x1)

def get_intercept(p1, p2):
    x1, y1 = p1
    slope = get_slope(p1, p2)
    return y1 - slope * x1

def _extend_points(points, x_min, x_max):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    if xs[0] > x_min:
        xs = [x_min] + xs
        ys = [ys[0]] + ys
    if xs[-1] < x_max:
        xs = xs + [x_max]
        ys = ys + [ys[-1]]
    return xs, ys

def draw_fuzzy_graph(ax, fuzzy_graph, x_min, x_max, input_value=None, xlabel="Value"):
    ax.clear()
    for mf in fuzzy_graph.graphs:
        xs, ys = _extend_points(mf.points, x_min, x_max)
        ax.plot(xs, ys, label=mf.name)
    if input_value is not None:
        ax.axvline(input_value, linestyle="--", color="gray")
    ax.set_title(fuzzy_graph.name)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Membership")
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(x_min, x_max)
    ax.legend()
    ax.grid(True)

def draw_time_series(ax, ticks, temps, errors, target):
    ax.clear()
    ax.plot(ticks, temps, label="Temp", color="tab:blue")
    ax.plot(ticks, errors, label="Error", color="tab:red")
    ax.axhline(target, linestyle="--", color="gray", label=f"Target = {target}")
    ax.axhline(0, linestyle=":", color="lightgray")
    ax.set_title("Error in Simple Control System")
    ax.set_xlabel("Time (ticks)")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True)

def get_membership_error(e):
    if e <= -4:
        neg, zero, pos = 1, 0, 0
    elif e < -2:
        neg, zero, pos = 1, 0, 0
    elif e < 0:
        neg = get_slope((-2, 1), (0, 0)) * e + get_intercept((-2, 1), (0, 0))
        zero = get_slope((-2, 0), (0, 1)) * e + get_intercept((-2, 0), (0, 1))
        pos = 0
    elif e < 2:
        neg = 0
        zero = get_slope((0, 1), (2, 0)) * e + get_intercept((0, 1), (2, 0))
        pos = get_slope((0, 0), (2, 1)) * e + get_intercept((0, 0), (2, 1))
    else:
        neg, zero, pos = 0, 0, 1
    return neg, zero, pos

def get_membership_error_dot(ed):
    if ed <= -10:
        neg, zero, pos = 1, 0, 0
    elif ed < -5:
        neg, zero, pos = 1, 0, 0
    elif ed < 0:
        neg = get_slope((-5, 1), (0, 0)) * ed + get_intercept((-5, 1), (0, 0))
        zero = get_slope((-5, 0), (0, 1)) * ed + get_intercept((-5, 0), (0, 1))
        pos = 0
    elif ed < 5:
        neg = 0
        zero = get_slope((0, 1), (5, 0)) * ed + get_intercept((0, 1), (5, 0))
        pos = get_slope((0, 0), (5, 1)) * ed + get_intercept((0, 0), (5, 1))
    else:
        neg, zero, pos = 0, 0, 1
    return neg, zero, pos

def get_membership_output(x):
    if x <= 0:
        cool, zero, heat = 1, 0, 0
    elif x < 50:
        cool, zero, heat = 1, 0, 0
    elif x < 100:
        cool = get_slope((50, 1), (100, 0)) * x + get_intercept((50, 1), (100, 0))
        zero = get_slope((50, 0), (100, 1)) * x + get_intercept((50, 0), (100, 1))
        heat = 0
    elif x < 150:
        cool = 0
        zero = get_slope((100, 1), (150, 0)) * x + get_intercept((100, 1), (150, 0))
        heat = get_slope((100, 0), (150, 1)) * x + get_intercept((100, 0), (150, 1))
    else:
        cool, zero, heat = 0, 0, 1
    return cool, zero, heat

parser = argparse.ArgumentParser(description="Evaluate fuzzy membership for error and change in error based on a given temperature value.")
parser.add_argument("--target", type=float, required=True, help="Target Temperature value in degrees Celcius")
parser.add_argument("--continuous", action="store_true",
                    help="Run until Ctrl+C instead of auto-stopping when stable.")
args = parser.parse_args()

starting_temp = random.randint(10, 40)
cooling_strength = 1 / 120
heating_strength = 1 / 120

error_graph = FuzzyGraph("Error")
error_graph.register_graph(TrapMF((-4, 1), (-2, 1), (0, 0), (4, 0), name="Negative"))
error_graph.register_graph(TriMF((-2, 0), (0, 1), (2, 0), name="Zero"))
error_graph.register_graph(TrapMF((-4, 0), (0, 0), (2, 1), (4, 1), name="Positive"))

error_dot_graph = FuzzyGraph("Error Dot")
error_dot_graph.register_graph(TrapMF((-10, 1), (-5, 1), (0, 0), (10, 0), name="Negative"))
error_dot_graph.register_graph(TriMF((-5, 0), (0, 1), (5, 0), name="Zero"))
error_dot_graph.register_graph(TrapMF((-10, 0), (0, 0), (5, 1), (10, 1), name="Positive"))

output_graph = FuzzyGraph("Output")
output_graph.register_graph(TrapMF((0, 1), (50, 1), (100, 0), (200, 0), name="Cool"))
output_graph.register_graph(TriMF((50, 0), (100, 1), (150, 0), name="Zero"))
output_graph.register_graph(TrapMF((0, 0), (100, 0), (150, 1), (200, 1), name="Heat"))


# RULES
"""
If error is Negative and error dot is Negative then output is Cool
If error is Negative and error dot is Zero then output is Cool
If error is Negative and error dot is Positive then output is Cool
If error is Zero and error dot is Negative then output is Heat
If error is Zero and error dot is Zero then output is Zero
If error is Zero and error dot is Positive then output is Cool
If error is Positive and error dot is Negative then output is Heat
If error is Positive and error dot is Zero then output is Heat
If error is Positive and error dot is Positive then output is Heat
"""

current_temp = float(starting_temp)
prev_error = 0.0
stable_ticks = 0
tick = 0
tick_history = []
temp_history = []
error_history = []
error_dot_history = []

print(f"Target: {args.target:.2f}  |  Starting temp: {current_temp:.2f}")
print(f"{'Target':>7} | {'Temperature':>11} | {'Error':>7} | {'Error Dot':>9} | Action")
print("-" * 60)

try:
    while True:
        error = args.target - current_temp
        error_dot = error - prev_error

        neg_e, zero_e, pos_e = get_membership_error(error)
        neg_ed, zero_ed, pos_ed = get_membership_error_dot(error_dot)

        cap_cool = max(
            min(neg_e, neg_ed),
            min(neg_e, zero_ed),
            min(neg_e, pos_ed),
            min(zero_e, pos_ed),
        )
        cap_zero = min(zero_e, zero_ed)
        cap_heat = max(
            min(zero_e, neg_ed),
            min(pos_e, neg_ed),
            min(pos_e, zero_ed),
            min(pos_e, pos_ed),
        )

        sum_xy = 0.0
        sum_y = 0.0
        for x in range(0, 201):
            cool_x, zero_x, heat_x = get_membership_output(x)
            mu = max(min(cool_x, cap_cool), min(zero_x, cap_zero), min(heat_x, cap_heat))
            sum_xy += x * mu
            sum_y += mu
        z = sum_xy / sum_y if sum_y != 0 else 100.0

        pct = z - 100.0

        if pct > 0:
            action = "Heat"
            current_temp += heating_strength * pct
        elif pct < 0:
            action = "Cool"
            current_temp -= cooling_strength * abs(pct)
        else:
            action = "No change"

        print(f"{args.target:7.2f} | {current_temp:11.2f} | {error:7.2f} | {error_dot:9.2f} | {action}")

        tick_history.append(tick)
        temp_history.append(current_temp)
        error_history.append(error)
        error_dot_history.append(error_dot)
        tick += 1

        if not args.continuous and abs(error) < 0.1:
            stable_ticks += 1
            if stable_ticks >= 10:
                print("Stabilized.")
                break
        else:
            stable_ticks = 0

        prev_error = error
        time.sleep(1.0)
except KeyboardInterrupt:
    print("\nInterrupted.")

final_error = error_history[-1] if error_history else 0
final_error_dot = error_dot_history[-1] if error_dot_history else 0

renderers = [
    lambda ax: draw_fuzzy_graph(ax, error_graph, x_min=-4, x_max=4,
                                input_value=final_error, xlabel="Error"),
    lambda ax: draw_fuzzy_graph(ax, error_dot_graph, x_min=-10, x_max=10,
                                input_value=final_error_dot, xlabel="Error Dot"),
    lambda ax: draw_fuzzy_graph(ax, output_graph, x_min=0, x_max=200, xlabel="Output"),
    lambda ax: draw_time_series(ax, tick_history, temp_history, error_history, args.target),
]

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
current = [0]

def show_current():
    renderers[current[0]](ax)
    fig.canvas.draw_idle()

def next_plot(event=None):
    current[0] = (current[0] + 1) % len(renderers)
    show_current()

def prev_plot(event=None):
    current[0] = (current[0] - 1) % len(renderers)
    show_current()

ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])
btn_prev = Button(ax_prev, "Prev")
btn_next = Button(ax_next, "Next")
btn_prev.on_clicked(prev_plot)
btn_next.on_clicked(next_plot)

def on_key(event):
    if event.key == "left":
        prev_plot()
    elif event.key == "right":
        next_plot()

fig.canvas.mpl_connect("key_press_event", on_key)
show_current()
plt.show()
