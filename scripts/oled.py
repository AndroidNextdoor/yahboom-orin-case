#!/usr/bin/env python3
"""
OLED Display for Yahboom CubeNano Case

Displays system stats: CPU, RAM, disk usage, IP address, and time.
Compatible with Jetson Orin Nano Super and other Jetson devices.
"""

import time
import os
import sys
import subprocess

try:
    import Adafruit_SSD1306 as SSD
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip3 install Adafruit-SSD1306 pillow")
    sys.exit(1)


class YahboomOLED:
    """OLED display controller for system stats."""

    # Common I2C buses on different Jetson models
    I2C_BUSES = [7, 1, 0, 8, 4]

    def __init__(self, i2c_bus="auto", debug=False):
        self._debug = debug
        self._bus_index = 0

        if i2c_bus == "auto":
            self._i2c_bus = self.I2C_BUSES[0]
        else:
            self._i2c_bus = int(i2c_bus)
            self._bus_index = 0xFF  # Don't auto-scan

        # Display dimensions
        self._width = 128
        self._height = 32

        # Create drawing surface
        self._image = Image.new('1', (self._width, self._height))
        self._draw = ImageDraw.Draw(self._image)
        self._font = ImageFont.load_default()

        # CPU calculation state
        self._total_last = 0
        self._idle_last = 0
        self._cpu_str = "CPU:0%"

        self._oled = None

    def connect(self):
        """Connect to the OLED display. Returns True on success."""
        try:
            self._oled = SSD.SSD1306_128_32(
                rst=None, i2c_bus=self._i2c_bus, gpio=1)
            self._oled.begin()
            self._oled.clear()
            self._oled.display()
            if self._debug:
                print(f"OLED connected on bus {self._i2c_bus}")
            return True
        except Exception as e:
            if self._debug:
                print(f"OLED not found on bus {self._i2c_bus}: {e}")

            # Try next bus if auto-scanning
            if self._bus_index != 0xFF:
                self._bus_index = (self._bus_index + 1) % len(self.I2C_BUSES)
                self._i2c_bus = self.I2C_BUSES[self._bus_index]
            return False

    def clear(self):
        """Clear the display buffer."""
        self._draw.rectangle((0, 0, self._width, self._height), fill=0)

    def write_text(self, x, y, text):
        """Write text at position."""
        self._draw.text((x, y - 2), str(text), font=self._font, fill=255)

    def write_line(self, line, text):
        """Write text on line 1-4."""
        y = 8 * (line - 1)
        self.write_text(0, y, text)

    def refresh(self):
        """Push buffer to display."""
        if self._oled:
            self._oled.image(self._image)
            self._oled.display()

    def get_cpu(self, phase):
        """Get CPU usage (call with phase 0, then 4 to calculate)."""
        try:
            with open('/proc/stat', 'r') as f:
                line = f.readline()

            values = [int(x) for x in line.split()[1:11]]
            total = sum(values)
            idle = values[3]

            if phase == 0:
                self._total_last = total
                self._idle_last = idle
            elif phase == 4 and self._total_last > 0:
                total_diff = total - self._total_last
                idle_diff = idle - self._idle_last
                if total_diff > 0:
                    usage = int(100 * (total_diff - idle_diff) / total_diff)
                    self._cpu_str = f"CPU:{usage}%"
                self._total_last = 0
                self._idle_last = 0
        except:
            pass
        return self._cpu_str

    def get_time(self):
        """Get current time."""
        try:
            return subprocess.check_output(
                "date +%H:%M:%S", shell=True).decode().strip()
        except:
            return "00:00:00"

    def get_ram(self):
        """Get RAM usage."""
        try:
            cmd = "free | awk 'NR==2{printf \"RAM:%2d%% -> %.1fGB\", 100*($2-$7)/$2, $2/1048576}'"
            return subprocess.check_output(cmd, shell=True).decode().strip()
        except:
            return "RAM: --"

    def get_disk(self):
        """Get disk usage."""
        try:
            cmd = "df -h / | awk 'NR==2{printf \"SDC:%s -> %.0fGB\", $5, $2}'"
            return subprocess.check_output(cmd, shell=True).decode().strip()
        except:
            return "SDC: --"

    def get_ip(self):
        """Get local IP address."""
        interfaces = ['eno1', 'eth0', 'wlP1p1s0', 'wlan0']
        for iface in interfaces:
            try:
                cmd = f"/sbin/ifconfig {iface} 2>/dev/null | grep 'inet ' | awk '{{print $2}}'"
                ip = subprocess.check_output(cmd, shell=True).decode().strip()
                if ip and len(ip) <= 15:
                    return ip
            except:
                continue
        return "No network"

    def show_welcome(self, message="Welcome!", duration=3):
        """Show a welcome message."""
        self.clear()
        # Center vertically
        self.write_line(2, message)
        self.refresh()
        time.sleep(duration)

    def run(self, show_welcome=True):
        """Main display loop."""
        # Try to connect
        while not self.connect():
            time.sleep(2)
            if self._bus_index == 0xFF:
                print("Could not connect to OLED")
                return False

        if show_welcome:
            self.show_welcome("Jetson Orin Ready!")

        phase = 0
        ram_str = ""
        disk_str = ""
        ip_str = ""

        try:
            while True:
                self.clear()

                # Get stats (RAM/disk/IP only on phase 0 to reduce load)
                cpu_str = self.get_cpu(phase)
                time_str = self.get_time()

                if phase == 0:
                    ram_str = self.get_ram()
                    disk_str = self.get_disk()
                    ip_str = "IPA:" + self.get_ip()

                # Draw display
                self.write_text(0, 0, cpu_str)
                self.write_text(50, 0, time_str)
                self.write_line(2, ram_str)
                self.write_line(3, disk_str)
                self.write_line(4, ip_str)

                self.refresh()

                phase = (phase + 1) % 5
                time.sleep(0.2)

        except KeyboardInterrupt:
            self.clear()
            self.refresh()
            print("\nOLED display stopped")
            return True


def main():
    debug = "debug" in sys.argv

    oled = YahboomOLED(debug=debug)

    # Retry loop for hot-plug support
    while True:
        try:
            if oled.run():
                break
        except Exception as e:
            if debug:
                print(f"Error: {e}")
        time.sleep(2)


if __name__ == "__main__":
    main()
