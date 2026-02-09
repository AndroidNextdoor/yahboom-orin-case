#!/usr/bin/env python3
"""
CubeNano Library - Control fan and RGB lights on Yahboom CubeNano case.

Works with Jetson Orin Nano Super and other Jetson devices.
"""

import smbus
import time


class CubeNano:
    """Control the Yahboom CubeNano case fan and RGB lights via I2C."""

    # RGB Effect constants
    EFFECT_OFF = 0
    EFFECT_BREATHING = 1
    EFFECT_MARQUEE = 2
    EFFECT_RAINBOW = 3
    EFFECT_DAZZLE = 4
    EFFECT_WATERFALL = 5
    EFFECT_CYCLE = 6

    # Color constants
    COLOR_RED = 0
    COLOR_GREEN = 1
    COLOR_BLUE = 2
    COLOR_YELLOW = 3
    COLOR_PURPLE = 4
    COLOR_CYAN = 5
    COLOR_WHITE = 6

    # Speed constants
    SPEED_LOW = 1
    SPEED_MEDIUM = 2
    SPEED_HIGH = 3

    def __init__(self, i2c_bus=7, debug=False):
        """
        Initialize the CubeNano controller.

        Args:
            i2c_bus: I2C bus number (default 7 for Orin Nano)
            debug: Enable debug output
        """
        self._debug = debug
        self._delay = 0.002
        self._bus = smbus.SMBus(int(i2c_bus))
        self._addr = 0x0E

        # Register addresses
        self._REG_LED_INDEX = 0x00
        self._REG_LED_RED = 0x01
        self._REG_LED_GREEN = 0x02
        self._REG_LED_BLUE = 0x03
        self._REG_EFFECT = 0x04
        self._REG_SPEED = 0x05
        self._REG_COLOR = 0x06
        self._REG_FAN = 0x08

    def _write(self, register, value):
        """Write a value to a register."""
        try:
            self._bus.write_byte_data(self._addr, register, value)
            time.sleep(self._delay)
            return True
        except Exception as e:
            if self._debug:
                print(f"I2C write error: {e}")
            return False

    # Fan control
    def fan_on(self):
        """Turn the cooling fan on."""
        return self._write(self._REG_FAN, 1)

    def fan_off(self):
        """Turn the cooling fan off."""
        return self._write(self._REG_FAN, 0)

    def set_fan(self, state):
        """Set fan state (True=on, False=off)."""
        return self._write(self._REG_FAN, 1 if state else 0)

    # RGB effect control
    def set_effect(self, effect):
        """
        Set RGB light effect.

        Args:
            effect: 0=off, 1=breathing, 2=marquee, 3=rainbow,
                   4=dazzle, 5=waterfall, 6=cycle
        """
        effect = max(0, min(6, effect))
        return self._write(self._REG_EFFECT, effect)

    def set_speed(self, speed):
        """
        Set effect animation speed.

        Args:
            speed: 1=slow, 2=medium, 3=fast
        """
        speed = max(1, min(3, speed))
        return self._write(self._REG_SPEED, speed)

    def set_color(self, color):
        """
        Set effect color.

        Args:
            color: 0=red, 1=green, 2=blue, 3=yellow, 4=purple, 5=cyan, 6=white
        """
        color = max(0, min(6, color))
        return self._write(self._REG_COLOR, color)

    # Convenience methods for effects
    def lights_off(self):
        """Turn off all RGB lights."""
        return self.set_effect(self.EFFECT_OFF)

    def breathing(self, color=None, speed=SPEED_MEDIUM):
        """Set breathing light effect."""
        self.set_effect(self.EFFECT_BREATHING)
        self.set_speed(speed)
        if color is not None:
            self.set_color(color)

    def rainbow(self, speed=SPEED_MEDIUM):
        """Set rainbow color cycling effect."""
        self.set_effect(self.EFFECT_RAINBOW)
        self.set_speed(speed)

    def marquee(self, color=None, speed=SPEED_MEDIUM):
        """Set marquee (running) light effect."""
        self.set_effect(self.EFFECT_MARQUEE)
        self.set_speed(speed)
        if color is not None:
            self.set_color(color)

    # Individual LED control
    def set_led(self, index, red, green, blue):
        """
        Set individual LED color.

        Args:
            index: LED index 0-13, or 255 for all LEDs
            red: Red value 0-255
            green: Green value 0-255
            blue: Blue value 0-255
        """
        # Turn off effects first
        self._write(self._REG_EFFECT, 0)

        self._write(self._REG_LED_INDEX, index & 0xFF)
        self._write(self._REG_LED_RED, red & 0xFF)
        self._write(self._REG_LED_GREEN, green & 0xFF)
        self._write(self._REG_LED_BLUE, blue & 0xFF)

    def set_all_leds(self, red, green, blue):
        """Set all LEDs to the same color."""
        self.set_led(255, red, green, blue)

    def get_version(self):
        """Get firmware version."""
        try:
            self._bus.write_byte(self._addr, 0x00)
            return self._bus.read_byte(self._addr)
        except:
            return None


# Quick test
if __name__ == "__main__":
    cube = CubeNano(debug=True)
    print("Testing fan...")
    cube.fan_on()
    time.sleep(1)
    print("Testing rainbow effect...")
    cube.rainbow()
    time.sleep(3)
    print("Done!")
