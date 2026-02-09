#!/usr/bin/env python3
"""
Fan Control for Yahboom CubeNano Case

Usage:
    yahboom-fan on     Turn fan on
    yahboom-fan off    Turn fan off
    yahboom-fan        Show current state (if possible)
"""

import sys
import os

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cubenano import CubeNano


def show_help():
    print("""
Yahboom Fan Control
===================

Usage: yahboom-fan <on|off>

Commands:
  on     Turn the cooling fan on
  off    Turn the cooling fan off

Examples:
  yahboom-fan on    Start the fan
  yahboom-fan off   Stop the fan
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command in ['-h', '--help', 'help']:
        show_help()
        return

    try:
        cube = CubeNano()

        if command == 'on':
            cube.fan_on()
            print("Fan: ON")
        elif command == 'off':
            cube.fan_off()
            print("Fan: OFF")
        else:
            print(f"Unknown command: {command}")
            print("Use 'on' or 'off'")

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure I2C is enabled and you have permission.")
        print("Try: sudo usermod -aG i2c $USER")


if __name__ == "__main__":
    main()
