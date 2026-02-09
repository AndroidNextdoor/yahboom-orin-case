# Yahboom CubeNano Case for Jetson Orin Nano

Easy setup for the Yahboom CubeNano aluminum case with OLED display, RGB lights, and cooling fan.

<p align="center">
  <img src="images/case-photo.jpg" alt="Yahboom CubeNano Case" width="400">
</p>

## What This Does

- **OLED Display**: Shows CPU usage, memory, disk space, IP address, and time
- **Cooling Fan**: Keeps your Jetson cool (auto-starts on boot)
- **RGB Lights**: 14 addressable LEDs with effects like breathing, rainbow, and more

## Quick Install (1 Command!)

Open a terminal and run:

```bash
curl -fsSL https://raw.githubusercontent.com/AndroidNextdoor/yahboom-orin-case/main/install.sh | bash
```

That's it! Reboot and everything works automatically.

## Manual Install

If you prefer to install step-by-step:

```bash
# 1. Clone this repository
git clone https://github.com/AndroidNextdoor/yahboom-orin-case.git
cd yahboom-orin-case

# 2. Run the installer
./install.sh
```

## What's on the OLED?

```
CPU:45%  14:32:05     <- CPU usage and current time
RAM:62% -> 7.5GB     <- Memory usage and total RAM
SDC:23% -> 128.0GB   <- Storage usage and total space
IPA:192.168.1.100    <- Your IP address
```

## Control the RGB Lights

```bash
# Turn on rainbow effect
yahboom-rgb rainbow

# Set breathing effect in blue
yahboom-rgb breathing blue

# Turn off lights
yahboom-rgb off

# See all options
yahboom-rgb --help
```

**Available Effects:**
| Effect | Description |
|--------|-------------|
| `off` | Turn off all lights |
| `breathing` | Slow fade in/out |
| `marquee` | Running lights |
| `rainbow` | Color cycling |
| `dazzle` | Fast color changes |
| `waterfall` | Flowing effect |
| `cycle` | Breathing with color cycle |

**Available Colors:**
`red`, `green`, `blue`, `yellow`, `purple`, `cyan`, `white`

## Control the Fan

```bash
# Turn fan on
yahboom-fan on

# Turn fan off
yahboom-fan off
```

## Key Hardware Details

> **Full specs:** See [HARDWARE.md](HARDWARE.md)

| Component | I2C Address | Bus (Orin Nano) |
|-----------|-------------|-----------------|
| OLED Display | `0x3c` | 4 |
| Fan/RGB Controller | `0x0e` | 7 |

**Verify connections:**
```bash
sudo i2cdetect -y 4   # Should show 3c (OLED)
sudo i2cdetect -y 7   # Should show 0e (controller)
```

**Permission setup:**
```bash
sudo usermod -aG i2c $USER
# Log out and back in
```

## Uninstall

```bash
cd yahboom-orin-case
./uninstall.sh
```

## Compatibility

| Device | Status |
|--------|--------|
| Jetson Orin Nano Super (8GB) | ✅ Tested |
| Jetson Orin Nano (4GB/8GB) | ✅ Should work |
| Jetson Orin NX | ⚠️ Untested |

**Tested on:** JetPack 6.x (Ubuntu 22.04)

## Support

- **Issues?** Open a [GitHub Issue](https://github.com/AndroidNextdoor/yahboom-orin-case/issues)
- **Case manual:** See the [Yahboom Wiki](http://www.yahboom.net/study/CubeNano-Case)

## License

MIT License - Feel free to modify and share!
