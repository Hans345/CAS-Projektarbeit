# -*- coding: utf-8 -*
"""
Python-Code welcher bei Start ausgeführt wird
@author: Raphael Baumeler
"""
# Display
import time
import datetime as dt
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class PiOLED:
    def __init__(self):
        # init Display
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)
        self.image = Image.new('1', (128, 32))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

        # Get IP
        cmd = "hostname -I | cut -d' ' -f1"
        self.ip = subprocess.check_output(cmd, shell=True).decode("utf-8")

        # Get Time
        self.zeit = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Clear display.
        self.disp.fill(0)
        self.disp.show()

        # Draw Display
        self.draw.rectangle((0, 0, 128, 32), outline=0, fill=0)  # Draw box to clear
        self.draw.text((0, -2 + 0), 'IP: %s' % self.ip, font=self.font, fill=255)
        self.draw.text((0, -2 + 8), self.zeit, font=self.font, fill=255)
        self.draw.text((0, -2 + 16), '', font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()

        # sleep
        time.sleep(1)

    def set_string(self, s):
        # Clear display.
        self.draw.rectangle((0, 0, 128, 32), outline=0, fill=0)

        # Draw new text
        self.draw.text((0, -2 + 0), 'IP: %s' % self.ip, font=self.font, fill=255)
        self.draw.text((0, -2 + 8), self.zeit, font=self.font, fill=255)
        self.draw.text((0, -2 + 20), s, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()

        # Print
        print(self.ip)
        print(self.zeit)
