import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from fuzzygraphing import FuzzyGraph, TrapMF, TriMF

def get_slope(p1, p2):
    """Calculate the slope of a line given two points.

    Args:
        p1: A tuple (x1, y1) for the first point.
        p2: A tuple (x2, y2) for the second point.

    Returns:
        The slope of the line connecting the two points.
    """
    x1, y1 = p1
    x2, y2 = p2
    if x2 - x1 == 0:
        raise ValueError("Cannot calculate slope for vertical line (x1 == x2).")
    return (y2 - y1) / (x2 - x1)

def get_intercept(p1, p2):
    """Calculate the y-intercept of a line given two points.

    Args:
        p1: A tuple (x1, y1) for the first point.
        p2: A tuple (x2, y2) for the second point.
    """
    x1, y1 = p1
    slope = get_slope(p1, p2)
    return y1 - slope * x1

def get_fast_strength(sunny_value, warm_value):
    """Evaluate Rule 1: IF Sunny AND Warm THEN Fast.

    Uses the fuzzy AND operator (min) to determine how strongly this rule fires.

    Args:
        sunny_value: Membership degree in the 'Sunny' fuzzy set (0.0 to 1.0).
        warm_value: Membership degree in the 'Warm' fuzzy set (0.0 to 1.0).

    Returns:
        The firing strength of the 'drive Fast' rule (0.0 to 1.0).
    """
    return min(sunny_value, warm_value)

def get_slow_strength(cloudy_value, cool_value):
    """Evaluate Rule 2: IF Partly Cloudy AND Cool THEN Slow.

    Uses the fuzzy AND operator (min) to determine how strongly this rule fires.

    Args:
        cloudy_value: Membership degree in the 'Partly Cloudy' fuzzy set (0.0 to 1.0).
        cool_value: Membership degree in the 'Cool' fuzzy set (0.0 to 1.0).

    Returns:
        The firing strength of the 'drive Slow' rule (0.0 to 1.0).
    """
    return min(cloudy_value, cool_value)

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

def draw_fuzzy_graph(ax, fuzzy_graph, x_min=0, x_max=100, input_value=None, xlabel="Value"):
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

def get_membership_temp(temp):
    if temp > 0 and temp < 30:
        freezing_membership = get_slope((0, 1), (30, 1)) * temp + get_intercept((0, 1), (30, 1))
        cool_membership = 0
        warm_membership = 0
        hot_membership = 0
    elif temp >= 30 and temp < 50:
        freezing_membership = get_slope((30, 1), (50, 0)) * temp + get_intercept((30, 1), (50, 0))
        cool_membership = get_slope((30, 0), (50, 1)) * temp + get_intercept((30, 0), (50, 1))
        warm_membership = 0
        hot_membership = 0
    elif temp >= 50 and temp < 70:
        freezing_membership = 0
        cool_membership = get_slope((50, 1), (70, 0)) * temp + get_intercept((50, 1), (70, 0))
        warm_membership = get_slope((50, 0), (70, 1)) * temp + get_intercept((50, 0), (70, 1))
        hot_membership = 0
    elif temp >= 70 and temp < 90:
        freezing_membership = 0
        cool_membership = 0
        warm_membership = get_slope((70, 1), (90, 0)) * temp + get_intercept((70, 1), (90, 0))
        hot_membership = get_slope((70, 0), (90, 1)) * temp + get_intercept((70, 0), (90, 1))
    elif temp >= 90:
        freezing_membership = 0
        cool_membership = 0
        warm_membership = 0
        hot_membership = 1
    return freezing_membership, cool_membership, warm_membership, hot_membership

def get_membership_cover(cover):
    if cover > 0 and cover < 20:
        sunny_membership = get_slope((0, 1), (20, 1)) * cover + get_intercept((0, 1), (20, 1))
        partly_cloudy_membership = 0
        overcast_membership = 0
    elif cover >= 20 and cover < 25:
        sunny_membership = get_slope((0, 1), (20, 1)) * cover + get_intercept((0, 1), (20, 1))
        partly_cloudy_membership = get_slope((20, 0), (50, 1)) * cover + get_intercept((20, 0), (50, 1))
        overcast_membership = 0
    elif cover >= 25 and cover < 40:
        sunny_membership = get_slope((20, 1), (40, 0)) * cover + get_intercept((20, 1), (40, 0))
        partly_cloudy_membership = get_slope((20, 0), (50, 1)) * cover + get_intercept((20, 0), (50, 1))
        overcast_membership = 0
    elif cover >= 40 and cover < 50:
        sunny_membership = 0
        partly_cloudy_membership = get_slope((20, 0), (50, 1)) * cover + get_intercept((20, 0), (50, 1))
        overcast_membership = 0
    elif cover >= 50 and cover < 60:
        sunny_membership = 0
        partly_cloudy_membership = get_slope((50, 1), (80, 0)) * cover + get_intercept((50, 1), (80, 0))
        overcast_membership = 0
    elif cover >= 60 and cover < 80:
        sunny_membership = 0
        partly_cloudy_membership = get_slope((50, 1), (80, 0)) * cover + get_intercept((50, 1), (80, 0))
        overcast_membership = get_slope((60, 0), (80, 1)) * cover + get_intercept((60, 0), (80, 1))
    elif cover >= 80:
        sunny_membership = 0
        partly_cloudy_membership = 0
        overcast_membership = 1
    return sunny_membership, partly_cloudy_membership, overcast_membership

def get_membership_speed(x):
    if x >= 0 and x < 25:
        slow_membership = 1
        fast_membership = 0
    elif x >= 25 and x < 75:
        slow_membership = get_slope((25, 1), (75, 0)) * x + get_intercept((25, 1), (75, 0))
        fast_membership = get_slope((25, 0), (75, 1)) * x + get_intercept((25, 0), (75, 1))
    elif x >= 75:
        slow_membership = 0
        fast_membership = 1
    return slow_membership, fast_membership

def draw_clipped_mf(ax, xs, ys, title):
    ax.clear()
    ax.plot(xs, ys, color="red")
    ax.fill_between(xs, 0, ys, alpha=0.3, color="red")
    ax.set_title(title)
    ax.set_xlabel("Speed")
    ax.set_ylabel("Membership")
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(0, 100)
    ax.grid(True)

def draw_aggregated(ax, xs, ys, z, title):
    ax.clear()
    ax.plot(xs, ys, color="purple")
    ax.fill_between(xs, 0, ys, alpha=0.3, color="purple")
    ax.axvline(z, linestyle="--", color="black", label=f"z = {z:.2f}")
    ax.set_title(title)
    ax.set_xlabel("Speed")
    ax.set_ylabel("Membership")
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(0, 100)
    ax.legend()
    ax.grid(True)

def draw_mf_with_strength(ax, mf, strength, title, x_min=0, x_max=100):
    ax.clear()
    xs, ys = _extend_points(mf.points, x_min, x_max)
    ax.plot(xs, ys, label=mf.name)
    ax.axhline(strength, linestyle="--", color="red", label=f"firing strength = {strength:.4f}")
    ax.set_title(title)
    ax.set_xlabel("Speed")
    ax.set_ylabel("Membership")
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(x_min, x_max)
    ax.legend()
    ax.grid(True)

parser = argparse.ArgumentParser(description="Evaluate fuzzy membership for temperature and cloud cover values.")
parser.add_argument("--temp", type=float, required=True, help="Temperature value in degrees Fahrenheit")
parser.add_argument("--cover", type=float, required=True, help="Cloud cover percentage (0-100+)")
args = parser.parse_args()

temp_graph = FuzzyGraph("Temperature")
temp_graph.register_graph(TrapMF((0, 1), (30, 1), (50, 0), (100, 0), name="Freezing"))
temp_graph.register_graph(TriMF((30, 0), (50, 1), (70, 0), name="Cool"))
temp_graph.register_graph(TriMF((50, 0), (70, 1), (90, 0), name="Warm"))
temp_graph.register_graph(TrapMF((0, 0), (70, 0), (90, 1), (100, 1), name="Hot"))

cover_graph = FuzzyGraph("Cloud Cover")
cover_graph.register_graph(TrapMF((0, 1), (20, 1), (40, 0), (100, 0), name="Sunny"))
cover_graph.register_graph(TriMF((20, 0), (50, 1), (80, 0), name="Partly Cloudy"))
cover_graph.register_graph(TrapMF((0, 0), (60, 0), (80, 1), (100, 1), name="Overcast"))

temp = args.temp
cover = args.cover

freezing_membership, cool_membership, warm_membership, hot_membership = get_membership_temp(temp)
sunny_membership, partly_cloudy_membership, overcast_membership = get_membership_cover(cover)

rule_1 = get_fast_strength(sunny_membership, warm_membership)
rule_2 = get_slow_strength(partly_cloudy_membership, cool_membership)

print(f"\n-- Temperature memberships (temp = {temp}) --")
print(f"  Freezing       : {freezing_membership:.4f}")
print(f"  Cool           : {cool_membership:.4f}")
print(f"  Warm           : {warm_membership:.4f}")
print(f"  Hot            : {hot_membership:.4f}")

print(f"\n-- Cloud Cover memberships (cover = {cover}) --")
print(f"  Sunny          : {sunny_membership:.4f}")
print(f"  Partly Cloudy  : {partly_cloudy_membership:.4f}")
print(f"  Overcast       : {overcast_membership:.4f}")

print(f"\n-- Rule firing strengths --")
print(f"  Rule 1 (Sunny AND Warm -> Fast)        : {rule_1:.4f}")
print(f"  Rule 2 (Partly Cloudy AND Cool -> Slow): {rule_2:.4f}")
print()

# Create Speed Graph
speed_graph = FuzzyGraph("Speed")
speed_graph.register_graph(TrapMF((0, 1), (25, 1), (75, 0), (100, 0), name="Slow"))
speed_graph.register_graph(TrapMF((0, 0), (25, 0), (75, 1), (100, 1), name="Fast"))
slow_mf = speed_graph.graphs[0]
fast_mf = speed_graph.graphs[1]

# Create values necessary for defuzzification and visualization of clipped membership functions
xs = list(range(0, 101))
actual_slow_ys = []
actual_fast_ys = []
for x in xs:
    slow, fast = get_membership_speed(x)
    actual_slow_ys.append(min(slow, rule_2))
    actual_fast_ys.append(min(fast, rule_1))
max_ys = [max(s, f) for s, f in zip(actual_slow_ys, actual_fast_ys)]

# Calculate centroid for defuzzification
xy = np.array(xs) * np.array(max_ys)
sum_xy = sum(xy)
sum_y = sum(max_ys)
z = sum_xy / sum_y if sum_y != 0 else 0
print(f"Defuzzified speed (centroid): {z:.2f}")

# All about visualization: create a series of plots that the user can navigate through to see the different stages of the fuzzy logic evaluation process
renderers = [
    lambda ax: draw_fuzzy_graph(ax, temp_graph, input_value=temp, xlabel="Temperature"),
    lambda ax: draw_fuzzy_graph(ax, cover_graph, input_value=cover, xlabel="Cloud Cover"),
    lambda ax: draw_fuzzy_graph(ax, speed_graph, xlabel="Speed"),
    lambda ax: draw_mf_with_strength(ax, slow_mf, rule_2, title="Slow (Rule 2 firing strength)"),
    lambda ax: draw_mf_with_strength(ax, fast_mf, rule_1, title="Fast (Rule 1 firing strength)"),
    lambda ax: draw_clipped_mf(ax, xs, actual_slow_ys, title="Actual Slow (clipped by rule_2)"),
    lambda ax: draw_clipped_mf(ax, xs, actual_fast_ys, title="Actual Fast (clipped by rule_1)"),
    lambda ax: draw_aggregated(ax, xs, max_ys, z, title="Aggregated (max of Slow & Fast) with centroid z"),
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



