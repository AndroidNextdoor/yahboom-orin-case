#!/usr/bin/env python3
"""
RGB Light Control for Yahboom CubeNano Case

Usage:
    yahboom-rgb off              Turn off lights
    yahboom-rgb breathing [color] [speed]
    yahboom-rgb marquee [color] [speed]
    yahboom-rgb rainbow [speed]
    yahboom-rgb dazzle [speed]
    yahboom-rgb waterfall [color] [speed]
    yahboom-rgb cycle [speed]

Colors: red, green, blue, yellow, purple, cyan, white
Speed: slow, medium, fast (default: medium)
"""

import sys
import os

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cubenano import CubeNano


EFFECTS = {
    'off': 0,
    'breathing': 1,
    'marquee': 2,
    'rainbow': 3,
    'dazzle': 4,
    'waterfall': 5,
    'cycle': 6,
}

COLORS = {
    'red': 0,
    'green': 1,
    'blue': 2,
    'yellow': 3,
    'purple': 4,
    'cyan': 5,
    'white': 6,
}

SPEEDS = {
    'slow': 1,
    'medium': 2,
    'fast': 3,
}


def show_help():
    print("""
Yahboom RGB Light Control
=========================

Usage: yahboom-rgb <effect> [color] [speed]

Effects:
  off         Turn off all lights
  breathing   Slow fade in/out
  marquee     Running lights
  rainbow     Color cycling (no color option)
  dazzle      Fast color changes
  waterfall   Flowing effect
  cycle       Breathing with color cycle

Colors: red, green, blue, yellow, purple, cyan, white
Speeds: slow, medium, fast

Examples:
  yahboom-rgb rainbow           Rainbow effect at medium speed
  yahboom-rgb breathing blue    Blue breathing effect
  yahboom-rgb marquee red fast  Fast red marquee
  yahboom-rgb off               Turn off lights
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return

    effect_name = sys.argv[1].lower()

    if effect_name not in EFFECTS:
        print(f"Unknown effect: {effect_name}")
        print(f"Available effects: {', '.join(EFFECTS.keys())}")
        return

    # Parse optional color and speed
    color = None
    speed = SPEEDS['medium']

    for arg in sys.argv[2:]:
        arg = arg.lower()
        if arg in COLORS:
            color = COLORS[arg]
        elif arg in SPEEDS:
            speed = SPEEDS[arg]

    # Apply settings
    try:
        cube = CubeNano()
        cube.set_effect(EFFECTS[effect_name])

        if effect_name != 'off':
            cube.set_speed(speed)
            if color is not None and effect_name not in ['rainbow', 'cycle']:
                cube.set_color(color)

        print(f"RGB: {effect_name}", end="")
        if color is not None:
            color_name = [k for k, v in COLORS.items() if v == color][0]
            print(f" ({color_name})", end="")
        speed_name = [k for k, v in SPEEDS.items() if v == speed][0]
        if effect_name != 'off':
            print(f" @ {speed_name} speed")
        else:
            print()

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure I2C is enabled and you have permission.")
        print("Try: sudo usermod -aG i2c $USER")


if __name__ == "__main__":
    main()
