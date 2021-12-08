# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:47:50 2021

@author: raphael.baumeler
"""

# -*- coding: utf-8 -*
"""
Python-Code welcher bei Start ausgeführt wird
@author: markus markstaler
"""
import datetime as dt
import time
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import socket
# Initalize Display
i2c = busio.I2C(3, 2) # Create the I2C with SCL = 3, SDA = 2.
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c) # Create class
image = Image.new('1', (128, 32)) # Create blank image for drawing.
draw = ImageDraw.Draw(image) # Get drawing object to draw on image
font = ImageFont.load_default() # Load default font.
while True:
    zeit = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Ermittelt IP-Adresse
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # erstellt Netzwerkverbindung
    s.connect(('1.1.1.1',1)) # fiktiver Internetzugriff
    ip = s.getsockname()[0] # ermittelt IP-Adresse
    # Display
    draw.rectangle((0, 0, 128, 32), outline=0, fill=0) # Draw box to clear image
    draw.text((0, -2+0), 'IP: %s' %ip, font=font, fill=255)
    draw.text((0, -2+8), zeit, font=font, fill=255)
    draw.text((0, -2+16), '', font=font, fill=255)
    draw.text((0, -2+25), 'es funktioniert !', font=font, fill=255)
    disp.image(image)
    disp.show()
    print(ip)
    print(zeit)
    time.sleep(5)