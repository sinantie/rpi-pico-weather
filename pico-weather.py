# Weather Information Center  Author: peppe8o
# Date: Jun 02nd, 2025
# Version: 2.2
# Modified for TFT 7735 1.8 inch 128 x 160 LCD

from netman import connect_wifi
import config
import urequests, json
import framebuf, time
from ST7735 import TFT, TFTColor
from sysfont import sysfont
from machine import SPI
from machine import deepsleep

# Initialize TFT display
spi = SPI(1, baudrate=8000000, polarity=0, phase=0)
# dc, rst, cs
tft=TFT(spi,aDC=8, aReset=12, aCS=9)
tft.init_7735(tabcolor=tft.GREENTAB, size=(128,160))
tft.rotation(0) # Portrait mode
tft.fill(TFT.WHITE)

# WiFi credentials loaded from config.py
wifi_connection = connect_wifi(config.ssid, config.password, config.country)
# Set variables for API Open-Meteo
lat="38.024467" # Home latitude
lon="23.814678" # Home longitude
timezone="Europe/Athens" #change it with your timezone

# Convert the weather code into descriptions.
# IMPORTANT NOTE: The description must match the icon name!
weather_code_descr={0:"Clear",\
1:"Clear",\
2:"Clouds",\
3:"Clouds",\
45:"Fog",\
48:"Fog",\
51:"Drizzle",\
53:"Drizzle",\
55:"Drizzle",\
56:"Drizzle",\
57:"Drizzle",\
61:"Rain",\
63:"Rain",\
65:"Rain",\
66:"Rain",\
67:"Rain",\
71:"Snow",\
73:"Snow",\
75:"Snow",\
77:"Snow",\
80:"Squall",\
81:"Squall",\
82:"Squall",\
85:"Snow",\
86:"Snow",\
95:"Thunderstorm",\
96:"Thunderstorm",\
99:"Thunderstorm",\
100:"Undefined"}


# Download the weather data

url_call="https://api.open-meteo.com/v1/forecast?latitude="+lat+\
        "&longitude="+lon+\
        "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&"+\
        "timezone="+timezone.replace("/","%2F")
 
w=urequests.get(url_call)
forecast=json.loads(w.content)
print("Received the following response:")
print(forecast)
print()
w.close()

'''
def pbm_draw(x_pos,y_pos,file):
    with open(file, 'rb') as f:
        f.readline() # The first 2 lines of PBM files are info not related to the image
        f.readline() # the 2 readlines remove these lines
        size = f.readline().decode('utf-8') # The 3rd row includes a byte with picture sizes that is decoded
        (x,y)=size.split("\n")[0].split(" ") # X variable gets the width, y variable gets the height
        data = bytearray(f.read())
    
    # Convert monochrome PBM data to RGB565 for TFT display
    width = int(x)
    height = int(y)
    # expected_bytes = (width * height) // 8
    # print(f"Loading image: {file}, size: {width}x{height}")
    # print(f"Data length: {len(data)}, expected: {expected_bytes}")
    # # Truncate data to expected length
    # data = data[:expected_bytes]
    # rgb_data = bytearray(width * height * 2)  # RGB565 is 2 bytes per pixel
    
    # for i in range(len(data)):
    #     byte = data[i]
    #     for bit in range(8):
    #         pixel = (byte >> bit) & 1  # Try LSB first instead of MSB
    #         color = 0xFFFF if pixel == 0 else 0x0000  # White for 0, Black for 1
    #         color = rgb565_to_bgr565(color)  # Convert to BGR565 for BLACKTAB
    #         idx = (i * 8 + bit) * 2
    #         if idx < len(rgb_data) - 1:
    #             rgb_data[idx] = color >> 8  # Big-endian
    #             rgb_data[idx + 1] = color & 0xFF
    '''
    # Display on TFT
    #tft.image(x_pos, y_pos, x_pos + width - 1, y_pos + height - 1, data)
    render_bmp(0,15,'Fog.bmp')
spi.deinit()


#Today forecast
temp_min=float(forecast["daily"]["temperature_2m_min"][0])
temp_max=float(forecast["daily"]["temperature_2m_max"][0])
rain_qty=int(forecast["daily"]["precipitation_sum"][0])
weather_code=forecast["daily"]["weather_code"][0]
if weather_code not in weather_code_descr: weather_code = 100
weather_descr=weather_code_descr[weather_code]

# epd.text("Today's Weather", 2, 1, black)
tft.text((2, 1), "Today's Weather", TFT.BLACK, sysfont, 1)

pbm_draw(0, 15, weather_descr+'.pbm')
tft.text((65, 15), " Max:{:.0f}C".format(temp_max), TFT.BLACK, sysfont, 1)
tft.text((65, 25), " Min:{:.0f}C".format(temp_min), TFT.BLACK, sysfont, 1)
tft.text((65, 35), "Rain:{:02d}mm".format(rain_qty), TFT.BLACK, sysfont, 1)

tft.text((0, 78), weather_descr, TFT.BLACK, sysfont, 1)

#Update time
tft.line((0, 90), (125, 90), TFT.BLACK)
today_date = forecast["daily"]["time"][0]
tft.text((0, 92), "now:"+today_date, TFT.BLACK, sysfont, 1)
tft.line((0, 101), (125, 101), TFT.BLACK)

start_line=105

# Forecasts for the following days
for day in range(0,2):
    d=day+1
    temp_min=float(forecast["daily"]["temperature_2m_min"][d])
    temp_max=float(forecast["daily"]["temperature_2m_max"][d])
    rain_qty=int(forecast["daily"]["precipitation_sum"][d])
    weather_code=forecast["daily"]["weather_code"][d]
    weather_descr=weather_descr=weather_code_descr[weather_code]
    line = start_line + 2 * day * 11
    
    tft.text((0, line), "+"+str(d)+" day> "+weather_descr, TFT.BLACK, sysfont, 1)
    tft.text((4, line+10), "Max:{:.0f}/Min:{:.0f}".format(temp_max,temp_min), TFT.BLACK, sysfont, 1)
    tft.text((82, line+10), "Rn:{:02d}mm".format(rain_qty), TFT.BLACK, sysfont, 1)


# tft.text((0, 242), "for Home use! ", TFT.BLACK, sysfont, 1)

# Add 10 seconds of nothing in order to be able to send interrupt before going to deepsleep
time.sleep(10)

# Turn to deepsleep for battery saving
# sleep_minutes=15
# sleep_time=sleep_minutes * 60 * 1000
# deepsleep(sleep_time)

