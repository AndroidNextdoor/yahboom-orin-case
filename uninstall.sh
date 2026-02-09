#!/bin/bash
# Yahboom CubeNano Case Uninstaller

echo "Uninstalling Yahboom CubeNano Case..."

# Stop and disable services
sudo systemctl stop yahboom-oled.service 2>/dev/null
sudo systemctl stop yahboom-fan.service 2>/dev/null
sudo systemctl disable yahboom-oled.service 2>/dev/null
sudo systemctl disable yahboom-fan.service 2>/dev/null

# Remove service files
sudo rm -f /etc/systemd/system/yahboom-oled.service
sudo rm -f /etc/systemd/system/yahboom-fan.service
sudo systemctl daemon-reload

# Remove commands
sudo rm -f /usr/local/bin/yahboom-rgb
sudo rm -f /usr/local/bin/yahboom-fan

# Remove installation directory
sudo rm -rf /opt/yahboom-orin-case

echo "Uninstall complete!"
echo "Note: Python packages (Adafruit-SSD1306) were not removed."
