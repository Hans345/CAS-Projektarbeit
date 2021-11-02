# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Bibliothek zur Kommunikation mit Engerie-Geräte
@author: Markus Markstaler/2017


    B+ weiss pin1 EX1309 oben lüftungsrillen
    A- grau  pin2 EX1309
    gnd-     pin5 EX1309

raspberry usb2rs485:
port = serial.Serial(port = '/dev/ttyUSB0', 

raspberry Interne UART
port = '/dev/ttyAMA0'
hierfür muss jedoch die interne UART freigelegt werden, da sie durchs Bluetooth besetzt ist.
Dies erfolgt durch


"""

import serial
import os
import time
from struct import unpack
import datetime as dt
import numpy as np


def addCRC(data):
    """ 
    data ist Modbusnachricht als String mit hex-Zeichen (2 Zeichen), getrennten mit "-" Bindestrich oder 
    Leerzeichen '' oder kein Zeichen dazwischen. Z.B. 'AA-01-F3' oder '0101-65CD'.
    
    oder: data kann auch vom Type Bytes sein (b'\x0a$\x12').
    
    Berechnet CRC-16 nach Modbus.org Beschreibung für Serial (Kapital 6.2.2) und hängt dies an die Nachricht an.
    Ausgabe ist ein Integer-Array mit den Zeichennr. der Modbusnachricht.
    """
    intArr = []
    if type(data) == bytes:
        for l in range(len(data)):
            intArr.append(data[l])
    else:
        hexStr = data.replace('-','')
        hexStr = hexStr.replace(' ','')
        for h in range(0,len(hexStr)-1,2):
            hexVal = hexStr[h:h+2]
            intVal = int(hexVal,16)
            intArr.append(intVal)      
    reg = 0xFFFF # 16 Bit alles 1
    for i in range(len(intArr)):   # Nachricht in 8-Bit Teile, d.h. 1 Byte=2 Hex
        reg = reg ^ intArr[i]      # XOR mit den den 8-Bit Eingangsdaten und dem Register "reg"
        for x in range(8):       
            if (reg & 1):   # examin/ermittelt LSB. Geht auch über Rest Funktion (np.mod(reg,2))
                reg = reg >> 1     # um 1 Bit nach rechts, Richtung LSB
                reg = reg ^ 0xA001 # XOR   
            else:
                reg = reg >> 1     # um 1 Bit nach rechts, Richtung LSB        
    intArr.append(reg & 0xFF)
    intArr.append(reg//256)
    return intArr

###############################################################################

## Zähler auslesen
adr = '01'
fkt = '03'
reg = '5002' # L1 Voltage
anzReg = 2
leng = '%04x'%(anzReg*2)  # 30hex = 48 Bytes (96 hex stellen) 24 Register
form = '>f'
askStr = adr + fkt + reg + leng
askIntcrc = addCRC(askStr)
ask = bytes(askIntcrc)
blen = 12

# Daten schreiben und
port = serial.Serial(port = '/dev/ttyUSB0',\
    baudrate = 9600, \
    bytesize = 8, \
    parity = 'E', \
    stopbits = 1, \
    timeout = 0.5, \
    xonxoff=False, \
    rtscts=False, \
    dsrdtr=False) # SW/HW/HW Flow-Control False, Ueberprüfung im Code
port.write(ask)
answer = port.read(blen)       # port.in_waiting # Nicht verwenden. port.read wartet automatisch in_wainting nicht!!
port.close()
print(answer)

# Daten umformatieren 
dataRAW = answer[3:-2]     
data = unpack(form, dataRAW)[0]
print(data)