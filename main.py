"""Fuzzy logic controller that recommends a driving speed based on weather conditions.

This script uses two input variables — temperature (°F) and cloud cover (%) — to
infer a recommended driving speed (mph) through a Mamdani-style fuzzy inference system.

Fuzzy Rules:
    Rule 1: IF Sunny AND Warm THEN drive Fast
    Rule 2: IF Partly Cloudy AND Cool THEN drive Slow

The AND operator is implemented as the minimum of the two membership values.
Defuzzification uses the centroid (center of gravity) method to produce a crisp
speed output from the aggregated fuzzy output set.

Usage:
    python main.py --temp 75 --cover 30
"""

import argparse
from fuzzygraphing import FuzzyGraph, TrapMF, TriMF


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


# --- Input fuzzy variable: Temperature (°F) ---
temp_graph = FuzzyGraph("Temperature Graph")
temp_graph.register_graph(TrapMF(0, 0, 30, 50, name="Freezing"))
temp_graph.register_graph(TriMF(30, 50, 70, name="Cool"))
temp_graph.register_graph(TriMF(50, 70, 90, name="Warm"))
temp_graph.register_graph(TrapMF(70, 90, 120, float('inf'), name="Hot"))

# --- Input fuzzy variable: Cloud Cover (%) ---
cover_graph = FuzzyGraph("Cover Graph")
cover_graph.register_graph(TrapMF(0, 0, 20, 40, name="Sunny"))
cover_graph.register_graph(TriMF(20, 50, 80, name="Partly Cloudy"))
cover_graph.register_graph(TrapMF(60, 80, 110, float('inf'), name="Overcast"))

# --- Output fuzzy variable: Speed (mph) ---
speed_graph = FuzzyGraph("Speed Graph")
speed_graph.register_graph(TrapMF(0, 0, 25, 75, name="Slow"))
speed_graph.register_graph(TrapMF(25, 75, 125, float('inf'), name="Fast"))


parser = argparse.ArgumentParser(description="Evaluate fuzzy membership for temperature and cloud cover values.")
parser.add_argument("--temp", type=float, required=True, help="Temperature value in degrees Fahrenheit")
parser.add_argument("--cover", type=float, required=True, help="Cloud cover percentage (0-100+)")
args = parser.parse_args()

# --- Step 1: Fuzzification — convert crisp inputs into membership degrees ---
temp_graph.print_membership(args.temp)
print()
cover_graph.print_membership(args.cover)

temperature_memberships = temp_graph.calculate_membership(args.temp)
cover_memberships = cover_graph.calculate_membership(args.cover)

# --- Step 2: Rule evaluation — determine how strongly each rule fires ---
sunny_value = cover_memberships.get("Sunny")
warm_value = temperature_memberships.get("Warm")

cloudy_value = cover_memberships.get("Partly Cloudy")
cool_value = temperature_memberships.get("Cool")

fast_strength = get_fast_strength(sunny_value, warm_value)
slow_strength = get_slow_strength(cloudy_value, cool_value)

def calculate_centroid_speed(speed_graph, rule_fast_strength, rule_slow_strength):
    """Defuzzify the output fuzzy set into a crisp speed value using the centroid method.

    The centroid (center of gravity) method computes:
        crisp_value = sum(x * mu(x)) / sum(mu(x))

    where mu(x) is the aggregated membership at each point x in the output universe.

    For each point x in the speed range, this function:
        1. Gets the raw membership heights from each output fuzzy set (Slow, Fast)
        2. Clips each height at the corresponding rule's firing strength (Mamdani implication)
        3. Aggregates by taking the max of the clipped values (fuzzy union)
        4. Accumulates the weighted sum for the centroid formula

    Args:
        speed_graph: FuzzyGraph containing the output membership functions (Slow, Fast).
        rule_fast_strength: Firing strength of Rule 1 (Sunny AND Warm -> Fast).
        rule_slow_strength: Firing strength of Rule 2 (Partly Cloudy AND Cool -> Slow).

    Returns:
        Crisp speed value in mph, or 0.0 if no rules fired.

    Example at x=25 (with rule_fast_strength=0.75, rule_slow_strength=0.1667):
        Raw:     Slow=1.0, Fast=0.0
        Clipped: Slow=min(1.0, 0.1667)=0.1667, Fast=min(0.0, 0.75)=0.0
        Aggregated mu(25) = max(0.1667, 0.0) = 0.1667
    """
    numerator = 0.0
    denominator = 0.0

    # TODO: Derive range dynamically from the graph's membership functions
    # instead of hardcoding the upper bound.
    for x in range(0, 126):

        # 1. Get raw membership heights at this speed value
        speed_memberships = speed_graph.calculate_membership(x)
        raw_slow = speed_memberships.get("Slow", 0.0)
        raw_fast = speed_memberships.get("Fast", 0.0)

        # 2. Clip each shape at its rule's firing strength (Mamdani implication)
        clipped_slow = min(raw_slow, rule_slow_strength)
        clipped_fast = min(raw_fast, rule_fast_strength)

        # 3. Aggregate: take the max to form the combined output shape
        mu_x = max(clipped_slow, clipped_fast)

        # 4. Accumulate for the centroid formula: sum(x * mu) / sum(mu)
        numerator += (x * mu_x)
        denominator += mu_x

    if denominator == 0:
        return 0.0
    return numerator / denominator

# --- Step 3: Defuzzification — convert fuzzy output into a crisp speed ---
final_crisp_speed = calculate_centroid_speed(speed_graph, fast_strength, slow_strength)

print(f"\nRule Strengths:")
print(f"Rule 1 (Fast) Strength: {fast_strength:.4f}")
print(f"Rule 2 (Slow) Strength: {slow_strength:.4f}")
print(f"\nFinal Defuzzified Output:")
print(f"Crisp Speed to drive: {final_crisp_speed:.2f} mph")