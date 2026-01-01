# Weather Report on Raspberry Pi Pico W

A weather display application for the Raspberry Pi Pico W that shows current weather and forecasts on a 1.8" TFT LCD screen.

Based on the original work by [peppe8o](https://peppe8o.com).


## Features

- Displays current weather and 6-day forecast
- Uses Open-Meteo API for weather data
- Low-power deep sleep mode
- Configurable for any location worldwide

## Hardware Requirements

- Raspberry Pi Pico W
- 1.8" TFT LCD (128x160, ST7735 controller; using driver by [AntonHermann](https://github.com/AntonHermann/st7735-pico-micropython/tree/master))
- Appropriate wiring (SPI connection)

## Software Requirements

- MicroPython firmware for Raspberry Pi Pico W (tested with v1.22.0+)
- VS Code with MicroPico extension (for development)
- Python 3.10+ on host machine

## Installation

### 1. Flash MicroPython Firmware

1. Download the latest MicroPython UF2 file for Raspberry Pi Pico W from [micropython.org](https://micropython.org/download/rp2-pico-w/)
2. Put your Pico W into bootloader mode (hold BOOTSEL while plugging in)
3. Drag the UF2 file to the Pico's USB drive

### 2. Install Dependencies

Use the MicroPico extension in VS Code to upload the project files to your Pico W.

### 3. Configure WiFi

1. Copy `config_template.py` to `config.py`
2. Edit `config.py` with your WiFi credentials:

```python
ssid = 'your_wifi_ssid'
password = 'your_wifi_password'
country = 'US'  # or 'GR', 'GB', etc. based on your location
```

**Important:** `config.py` is gitignored to keep your credentials private. Never commit it to version control.

### 4. Set Up Your Location

Edit the latitude, longitude, and timezone in `pico-weather.py`:

```python
lat = "38.024467"  # Your latitude
lon = "23.814678"  # Your longitude
timezone = "Europe/Athens"  # Your timezone (use URL-encoded format)
```

To find coordinates for your city:
- Use Google Maps or OpenStreetMap
- Right-click on your location to get coordinates
- Timezone format: Use names like "Europe/London" or "America/New_York"

### 5. Upload and Run

1. Use MicroPico extension to upload all files to your Pico W
2. Run `pico-weather.py` on the Pico
3. The display will show the weather information

## Usage

- The device will display today's weather and a 6-day forecast
- It automatically enters deep sleep for 15 minutes between updates
- Press the reset button to wake it up

## Customization

- Weather icons: Place PBM format icon files in the project directory
- Display settings: Modify the TFT initialization in `pico-weather.py`
- Sleep duration: Change `sleep_minutes` variable

## License

Based on original code by peppe8o. See original repository for licensing details.

