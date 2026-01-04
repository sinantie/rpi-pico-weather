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

# Function to render BMP images
def render_bmp(x_pos, y_pos, file):
    f=open(file, 'rb')
    if f.read(2) == b'BM':  #header
        dummy = f.read(8) #file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            print("BMP width:", width, "height:", height, "depth:", depth)
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                print("Image size:", width, "x", height)
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                w, h = width, height
                if w > 128: w = 128
                if h > 160: h = 160
                tft._setwindowloc((x_pos,y_pos),(x_pos + w - 1,y_pos + h - 1))
                for row in range(h):
                    if flip:
                        pos = offset + (height - 1 - row) * rowsize
                    else:
                        pos = offset + row * rowsize
                    if f.tell() != pos:
                        dummy = f.seek(pos)
                    for col in range(w):
                        bgr = f.read(3)
                        tft._pushcolor(TFTColor(bgr[0],bgr[1],bgr[2]))



#Today forecast
temp_min=float(forecast["daily"]["temperature_2m_min"][0])
temp_max=float(forecast["daily"]["temperature_2m_max"][0])
rain_qty=int(forecast["daily"]["precipitation_sum"][0])
weather_code=forecast["daily"]["weather_code"][0]
if weather_code not in weather_code_descr: weather_code = 100
weather_descr=weather_code_descr[weather_code]

# epd.text("Today's Weather", 2, 1, black)
tft.text((2, 1), "Today's Weather", TFT.BLACK, sysfont, 1)

render_bmp(0, 15, weather_descr+'.bmp')
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
