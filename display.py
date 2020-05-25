#!/bin/python3

import sys
import time
import datetime
import fileinput

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

for line in fileinput.input():
    raw_list = line.rstrip()

sys.stdout.write(raw_list)

nicknames = []
last_index = 0
for i in range(raw_list.count("client_nickname")):
    raw_list = raw_list[raw_list.find("client_nickname=", last_index) + len("client_nickname="):]
    if not (raw_list.split(" ", 1)[0].startswith("ServerQuery") or raw_list.split(" ", 1)[0].startswith("rank_bot")):
        nicknames.append(raw_list.split(" ", 1)[0].replace("\s", " "))
        print(raw_list.split(" ", 1)[0])



# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
#disp.clear()
#disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font_size = 11
font = ImageFont.truetype('rusfont.ttf', font_size)
font_big = ImageFont.truetype('rusfont.ttf', font_size+2)
font_logo = ImageFont.truetype('rusfont.ttf', int(height/1.3))

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

currentDT = datetime.datetime.now()
formatted_time = str(currentDT.hour)+":"+str(currentDT.minute)

try:
    if len(nicknames) == 0:
        draw.text((0, top), "BENQ", font=font_logo, fill=255)
        draw.text((width-34, top), formatted_time, font=font_big, fill=255)
    else:
        draw.text((width-34, top), formatted_time, font=font_big, fill=255)

        draw.text((x, top), str("Online: " + str(len(nicknames))), font=font_big, fill=255)
        for i in range(len(nicknames)):
            if i < 4:
                draw.text((x, top+i*font_size+2+font_size+4), str(nicknames[i]), font=font, fill=255)
            else:
                draw.text((width-10, bottom-16), "v", font=font, fill=255)
                break

except:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, top), "ERR", font=font_logo, fill=255)
    draw.text((width-34, top), formatted_time, font=font_big, fill=255)

# Display image.
image = image.rotate(180)
disp.image(image)
disp.display()
