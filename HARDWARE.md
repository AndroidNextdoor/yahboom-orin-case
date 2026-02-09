# Hardware Details

## I2C Configuration

The Yahboom CubeNano case uses two I2C addresses on different buses:

| Component | Address | Bus (Orin Nano) | Bus (Older Jetsons) |
|-----------|---------|-----------------|---------------------|
| OLED Display (SSD1306) | `0x3c` | **4** | 1 or 0 |
| Fan/RGB Controller | `0x0e` | **7** | 1 or 0 |

**Verify with:**
```bash
sudo i2cdetect -y 4   # OLED
sudo i2cdetect -y 7   # Fan/RGB controller
```

## Network Interfaces

Orin Nano uses different interface names:

| Type | Orin Nano | Older Jetsons |
|------|-----------|---------------|
| Ethernet | `eno1` | `eth0` |
| WiFi | `wlP1p1s0` | `wlan0` |

## Pin Connections

The case connects via the 40-pin GPIO header:

| Pin | Function |
|-----|----------|
| 3 | I2C SDA |
| 5 | I2C SCL |
| 1 | 3.3V Power |
| 6 | Ground |

## Controller Registers

Fan/RGB controller at `0x0e`:

| Register | Function | Values |
|----------|----------|--------|
| `0x00` | LED index | 0-13, 255=all |
| `0x01` | LED red | 0-255 |
| `0x02` | LED green | 0-255 |
| `0x03` | LED blue | 0-255 |
| `0x04` | RGB effect | 0=off, 1=breathing, 2=marquee, 3=rainbow, 4=dazzle, 5=waterfall, 6=cycle |
| `0x05` | Effect speed | 1=slow, 2=medium, 3=fast |
| `0x06` | Effect color | 0=red, 1=green, 2=blue, 3=yellow, 4=purple, 5=cyan, 6=white |
| `0x08` | Fan | 0=off, 1=on |

## Permissions

Requires `i2c` group membership:
```bash
sudo usermod -aG i2c $USER
# Log out and back in
```
