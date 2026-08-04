from pathlib import Path

# Relative to the current script file
two_levels_up = Path(__file__).resolve().parents[2]

print(two_levels_up)