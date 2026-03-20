# Fuzzy Graphing

A Python library for fuzzy logic inference. Supports triangular (TriMF) and trapezoidal (TrapMF) membership functions, Mamdani-style rule evaluation, and centroid defuzzification.

## Membership Functions

- **TriMF(a, b, c)** — Triangular membership function defined by three points. Membership is 0 at `a` and `c`, and 1 at `b`.
- **TrapMF(a, b, c, d)** — Trapezoidal membership function defined by four points. Membership is 0 at `a` and `d`, and 1 between `b` and `c`. Supports `float('inf')` for open-ended (shoulder) trapezoids.

## Usage

`main.py` implements a fuzzy controller that recommends a driving speed based on temperature and cloud cover.

```
python main.py --temp <value> --cover <value>
```

Both arguments are required:
- `--temp` — Temperature in degrees Fahrenheit
- `--cover` — Cloud cover percentage

### Fuzzy Rules

| Rule | Antecedent              | Consequent |
|------|-------------------------|------------|
| 1    | Sunny AND Warm          | Fast       |
| 2    | Partly Cloudy AND Cool  | Slow       |

### Example

```
python main.py --temp 75 --cover 30
```

Output:

```
Membership results for 75.0 in Temperature Graph:
0.00% of Freezing
0.00% of Cool
75.00% of Warm
25.00% of Hot

Membership results for 30.0 in Cover Graph:
50.00% of Sunny
33.33% of Partly Cloudy
0.00% of Overcast

Rule Strengths:
Rule 1 (Fast) Strength: 0.5000
Rule 2 (Slow) Strength: 0.0000

Final Defuzzified Output:
Crisp Speed to drive: 81.20 mph
```
