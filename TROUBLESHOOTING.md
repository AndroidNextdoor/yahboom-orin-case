# Troubleshooting Guide

This guide documents common issues with the Yahboom CubeNano case on Jetson Orin Nano and how to fix them.

## Issue: OLED Display Not Working

### Symptoms
- OLED screen stays black
- Service fails to start
- "OLED not found" errors

### Diagnosis

**Step 1: Find which I2C bus your OLED is on**

The OLED can be on different I2C buses depending on your Jetson model. Scan all buses:

```bash
# Check common buses (0, 1, 4, 7, 8)
for bus in 0 1 4 7 8; do
    echo "=== Bus $bus ==="
    sudo i2cdetect -y $bus 2>/dev/null || echo "Bus $bus not available"
done
```

Look for address `3c` (the SSD1306 OLED) in the output:

```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
...
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
```

**Common bus locations:**
| Device | OLED Bus | Fan/RGB Bus |
|--------|----------|-------------|
| Orin Nano Super | 4 | 7 |
| Orin Nano | 4 or 7 | 7 |
| Older Jetsons | 1 or 0 | 1 or 0 |

**Step 2: Check the controller board**

The fan/RGB controller is at address `0e`:

```bash
sudo i2cdetect -y 7
```

You should see:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00: -- -- -- -- -- -- -- -- -- -- -- -- -- -- 0e --
```

### Solution

The script auto-scans buses `[4, 7, 1, 0, 8]` in order. If your OLED is on a different bus, you can:

**Option 1: Restart the service** (it will scan all buses)
```bash
sudo systemctl restart yahboom-oled
```

**Option 2: Force a specific bus**

Edit `/opt/yahboom-orin-case/oled.py` line 29:
```python
# Change from auto to your bus number
def __init__(self, i2c_bus=4, debug=False):  # Change 4 to your bus
```

---

## Issue: IP Address Shows "No network" or "x.x.x.x"

### Cause

The Orin Nano uses different network interface names than older Jetsons:

| Interface | Orin Nano | Older Jetsons |
|-----------|-----------|---------------|
| Ethernet | `eno1` | `eth0` |
| WiFi | `wlP1p1s0` | `wlan0` |

### Diagnosis

Check your interface names:
```bash
ip link show
```

### Solution

The script already checks multiple interface names. If yours is different, edit `/opt/yahboom-orin-case/oled.py` line 146:

```python
interfaces = ['eno1', 'eth0', 'wlP1p1s0', 'wlan0', 'YOUR_INTERFACE']
```

---

## Issue: Permission Denied Errors

### Symptoms
```
Error: [Errno 13] Permission denied
```

### Solution

Add your user to the `i2c` group:
```bash
sudo usermod -aG i2c $USER
```

Then **log out and log back in** (or reboot).

Verify:
```bash
groups | grep i2c
```

---

## Issue: Service Won't Start

### Diagnosis

Check the service status:
```bash
sudo systemctl status yahboom-oled
```

Check logs:
```bash
journalctl -u yahboom-oled -n 50
```

### Common Fixes

**Missing dependencies:**
```bash
pip3 install Adafruit-SSD1306 pillow
# Or on newer systems:
pip3 install --break-system-packages Adafruit-SSD1306 pillow
```

**Wrong Python path:**
```bash
which python3  # Should be /usr/bin/python3
```

**Script not executable:**
```bash
sudo chmod +x /opt/yahboom-orin-case/*.py
```

---

## Issue: Fan Not Working

### Diagnosis

Check if the controller is detected:
```bash
sudo i2cdetect -y 7 | grep "0e"
```

### Solution

If `0e` is not detected:
1. Check cable connections to the controller board
2. Try a different I2C bus
3. Make sure the ribbon cable is fully seated

Test manually:
```bash
yahboom-fan on
```

---

## Issue: RGB Lights Not Responding

Same as fan - the RGB and fan share the same controller at address `0x0e`.

Test manually:
```bash
yahboom-rgb rainbow
yahboom-rgb off
```

---

## Still Having Issues?

1. **Run with debug mode:**
   ```bash
   python3 /opt/yahboom-orin-case/oled.py debug
   ```

2. **Check I2C is enabled:**
   ```bash
   ls /dev/i2c-*
   ```
   You should see multiple I2C devices.

3. **Open an issue:** [GitHub Issues](https://github.com/AndroidNextdoor/yahboom-orin-case/issues)

Include:
- Your Jetson model (Orin Nano Super 8GB, etc.)
- JetPack version (`cat /etc/nv_tegra_release`)
- Output of `i2cdetect` commands
- Error messages from `journalctl`
