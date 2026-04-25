# Fuzzy Graphing

A Python library for fuzzy logic inference using triangular (TriMF) and trapezoidal (TrapMF) membership functions, Mamdani-style rule evaluation, and centroid defuzzification. Includes two example applications: a one-shot driving-speed recommender (`main.py`) and a real-time temperature controller (`tempcontrol.py`).

## Setup
1. Clone the repository.
2. From the repository root, create a virtual environment: `python -m venv my_venv`
3. Activate the virtual environment.
4. Install dependencies: `python -m pip install -r requirements.txt`

## Running the examples

### `main.py` — driving-speed recommender
Given a temperature (°F) and cloud cover (%), prints the membership values, fires two rules (Sunny+Warm → Fast, Cloudy+Cool → Slow), and defuzzifies to a crisp speed. Opens an 8-plot matplotlib carousel showing each stage of the Mamdani pipeline (use Prev/Next buttons or left/right arrow keys to navigate).

```
python main.py --temp 65 --cover 25
```

Both arguments must be in the range 0-100.

### `tempcontrol.py` — fuzzy temperature controller
Simulates a controller that drives a randomized starting temperature toward a target. Each tick prints a table row showing target, current temperature, error, error_dot, and the action (Heat / Cool / No change). After the loop ends, opens a 4-plot carousel including a time-series chart of Temp + Error vs ticks.

```
python tempcontrol.py --target 25
```

By default the loop stops when `|error| < 0.1` for 5 consecutive ticks. Pass `--continuous` to run forever (until Ctrl+C):

```
python tempcontrol.py --target 25 --continuous
```
