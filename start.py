# -*- coding: utf-8 -*
"""
Python-Code welcher bei Start ausgeführt wird
@author: markus markstaler
"""
# Display
import datetime as dt
import time
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import socket

# Temp. Sensor
import smbus2
import sgp30
import bme280

# Datenbank
import sqlite3
import os
import pandas as pd

# Initalize Display
i2c = busio.I2C(3,2) # Create the I2C with SCL = 3, SDA = 2.
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c) # Create class
image = Image.new('1', (128, 32)) # Create blank image for drawing.
draw = ImageDraw.Draw(image) # Get drawing object to draw on image
font = ImageFont.load_default() # Load default font.

# Initialize Temp. Sensor (sgp30)
bus = smbus2.SMBus(2)
bme280 = bme280.BME280(i2c_dev=bus)
sgp = sgp30.SGP30()
sgp._i2c_dev = bus

# Datenbank speichern in Datenbank
filename = 'messdaten.sqlite3'
if not(os.path.isfile(filename)):
    sql = '''CREATE TABLE tabelle (
        zeit DATETIME UNIQUE,
        temp REAL,
        humi REAL,
        prea REAL)'''
    db = sqlite3.connect(filename)
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()
    
while True:
    # Display
    zeit = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Ermittelt IP-Adresse
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # erstellt
    # Netzwerkverbindung
    s.connect(('1.1.1.1',1)) # fiktiver Internetzugriff
    ip = s.getsockname()[0] # ermittelt IP-Adresse
    # Display
    draw.rectangle((0, 0, 128, 32), outline=0, fill=0) # Draw box to clear

    #image
    draw.text((0, -2+0), 'IP: %s' %ip, font=font, fill=255)
    draw.text((0, -2+8), zeit, font=font, fill=255)
    draw.text((0, -2+16), '', font=font, fill=255)
    draw.text((0, -2+25), 'es funktioniert !', font=font, fill=255)
    disp.image(image)
    disp.show()

    print(ip)
    print(zeit)
    
    # Temp Sensor
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    #co2, voc = sgp.command('measure_air_quality')
    print('{:5.1f}°C {:5.0f}hPa {:5.0f}%'.format(temperature, pressure, humidity))
    
    # Daten speichern in Textdatei
    text = '{0:s}, {1:0.2f}, {2:0.2f}\n'.format(zeit, temperature, humidity, pressure)
    f = open('messdaten.csv','a+')
    f.write(text)
    f.close()
    
    # Daten speichern in Datenbank
    zeit = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = '''INSERT INTO tabelle (zeit, temp, humi, prea) VALUES (
        strftime("%Y-%m-%d %H:%M:%f", "{0:s}"),
        {1:0.2f},
        {2:0.2f},
        {3:0.2f})'''.format(zeit, temperature, humidity, pressure)
    db = sqlite3.connect(filename)
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()
    
    # Daten auslesen
    zeit = dt.datetime.now() - dt.timedelta(days=3) # Daten der letzten 3 Tage
    zeit = zeit.strftime('%Y-%m-%d')
    db = sqlite3.connect(filename)
    df = pd.read_sql_query('SELECT * FROM tabelle WHERE zeit>strftime("%Y-%m-%d","{0:s}")'.format(zeit), db)
    #print(list(df)) # get header name
    #print(df.zeit[:]) # get spalte zeit
    db.close()

    time.sleep(1)
