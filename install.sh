#!/bin/bash
# Yahboom CubeNano Case Installer for Jetson Orin Nano
# https://github.com/AndroidNextdoor/yahboom-orin-case

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Yahboom CubeNano Case Installer for Jetson Orin      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

INSTALL_DIR="/opt/yahboom-orin-case"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Please don't run as root. The script will ask for sudo when needed.${NC}"
    exit 1
fi

echo -e "${YELLOW}[1/6]${NC} Installing dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3-pip python3-pil python3-smbus i2c-tools > /dev/null

# Install Adafruit SSD1306 library
pip3 install --quiet Adafruit-SSD1306 2>/dev/null || pip3 install --quiet --break-system-packages Adafruit-SSD1306

echo -e "${GREEN}✓${NC} Dependencies installed"

echo -e "${YELLOW}[2/6]${NC} Installing to $INSTALL_DIR..."
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r "$SCRIPT_DIR/scripts/"* "$INSTALL_DIR/" 2>/dev/null || {
    # If running from curl pipe, download the scripts
    echo "    Downloading scripts..."
    sudo curl -fsSL -o "$INSTALL_DIR/cubenano.py" \
        "https://raw.githubusercontent.com/AndroidNextdoor/yahboom-orin-case/main/scripts/cubenano.py"
    sudo curl -fsSL -o "$INSTALL_DIR/oled.py" \
        "https://raw.githubusercontent.com/AndroidNextdoor/yahboom-orin-case/main/scripts/oled.py"
    sudo curl -fsSL -o "$INSTALL_DIR/rgb-control.py" \
        "https://raw.githubusercontent.com/AndroidNextdoor/yahboom-orin-case/main/scripts/rgb-control.py"
    sudo curl -fsSL -o "$INSTALL_DIR/fan-control.py" \
        "https://raw.githubusercontent.com/AndroidNextdoor/yahboom-orin-case/main/scripts/fan-control.py"
}
sudo chmod +x "$INSTALL_DIR"/*.py
echo -e "${GREEN}✓${NC} Scripts installed"

echo -e "${YELLOW}[3/6]${NC} Creating command shortcuts..."
# Create user-friendly commands
sudo tee /usr/local/bin/yahboom-rgb > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/yahboom-orin-case/rgb-control.py "$@"
EOF

sudo tee /usr/local/bin/yahboom-fan > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/yahboom-orin-case/fan-control.py "$@"
EOF

sudo chmod +x /usr/local/bin/yahboom-rgb /usr/local/bin/yahboom-fan
echo -e "${GREEN}✓${NC} Commands created: yahboom-rgb, yahboom-fan"

echo -e "${YELLOW}[4/6]${NC} Setting up OLED display service..."
sudo tee /etc/systemd/system/yahboom-oled.service > /dev/null << EOF
[Unit]
Description=Yahboom CubeNano OLED Display
After=multi-user.target

[Service]
Type=simple
User=$USER
ExecStart=/usr/bin/python3 $INSTALL_DIR/oled.py
WorkingDirectory=$INSTALL_DIR
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable yahboom-oled.service
echo -e "${GREEN}✓${NC} OLED service enabled"

echo -e "${YELLOW}[5/6]${NC} Setting up fan auto-start..."
sudo tee /etc/systemd/system/yahboom-fan.service > /dev/null << EOF
[Unit]
Description=Yahboom CubeNano Cooling Fan
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 $INSTALL_DIR/fan-control.py on
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable yahboom-fan.service
echo -e "${GREEN}✓${NC} Fan service enabled"

echo -e "${YELLOW}[6/6]${NC} Adding user to i2c group..."
sudo usermod -aG i2c "$USER" 2>/dev/null || true
echo -e "${GREEN}✓${NC} User added to i2c group"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Installation Complete! 🎉                   ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Starting services now..."
sudo systemctl start yahboom-fan.service
sudo systemctl start yahboom-oled.service

echo ""
echo "Commands available:"
echo "  yahboom-rgb rainbow    - Set rainbow LED effect"
echo "  yahboom-rgb off        - Turn off LEDs"
echo "  yahboom-fan on/off     - Control the fan"
echo ""
echo -e "${YELLOW}Note: Log out and back in for i2c group to take effect.${NC}"
echo ""
