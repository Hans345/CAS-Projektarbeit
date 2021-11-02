# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Bibliothek zur Kommunikation mit Engerie-Geräte
@author: Markus Markstaler/2017


    B+ weiss pin1 EX1309 oben lüftungsrillen
    A- grau  pin2 EX1309
    gnd-     pin5 EX1309

raspberry Interne UART
port = '/dev/ttyAMA0'

raspberry usb2rs485:
port = serial.Serial(port = '/dev/ttyUSB0', 
"""

import serial
import time
import socket
from struct import unpack
import datetime as dt
import numpy as np

def addCRC(data):  
    """
    Berechnet CRC-16 für Modubus und hängt sie an die Daten an.
    Daten als Integer-Array.
    Quelle: minimalmodbus.py von Jonas Berg auf github
    """    
    crc16tabelle = (
            0, 49345, 49537,   320, 49921,   960,   640, 49729, 50689,  1728,  1920, 
        51009,  1280, 50625, 50305,  1088, 52225,  3264,  3456, 52545,  3840, 53185, 
        52865,  3648,  2560, 51905, 52097,  2880, 51457,  2496,  2176, 51265, 55297, 
         6336,  6528, 55617,  6912, 56257, 55937,  6720,  7680, 57025, 57217,  8000, 
        56577,  7616,  7296, 56385,  5120, 54465, 54657,  5440, 55041,  6080,  5760, 
        54849, 53761,  4800,  4992, 54081,  4352, 53697, 53377,  4160, 61441, 12480, 
        12672, 61761, 13056, 62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721, 
        13760, 13440, 62529, 15360, 64705, 64897, 15680, 65281, 16320, 16000, 65089, 
        64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400, 10240, 59585, 59777, 
        10560, 60161, 11200, 10880, 59969, 60929, 11968, 12160, 61249, 11520, 60865, 
        60545, 11328, 58369,  9408,  9600, 58689,  9984, 59329, 59009,  9792,  8704, 
        58049, 58241,  9024, 57601,  8640,  8320, 57409, 40961, 24768, 24960, 41281, 
        25344, 41921, 41601, 25152, 26112, 42689, 42881, 26432, 42241, 26048, 25728, 
        42049, 27648, 44225, 44417, 27968, 44801, 28608, 28288, 44609, 43521, 27328, 
        27520, 43841, 26880, 43457, 43137, 26688, 30720, 47297, 47489, 31040, 47873, 
        31680, 31360, 47681, 48641, 32448, 32640, 48961, 32000, 48577, 48257, 31808, 
        46081, 29888, 30080, 46401, 30464, 47041, 46721, 30272, 29184, 45761, 45953, 
        29504, 45313, 29120, 28800, 45121, 20480, 37057, 37249, 20800, 37633, 21440, 
        21120, 37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568, 39937, 
        23744, 23936, 40257, 24320, 40897, 40577, 24128, 23040, 39617, 39809, 23360, 
        39169, 22976, 22656, 38977, 34817, 18624, 18816, 35137, 19200, 35777, 35457, 
        19008, 19968, 36545, 36737, 20288, 36097, 19904, 19584, 35905, 17408, 33985, 
        34177, 17728, 34561, 18368, 18048, 34369, 33281, 17088, 17280, 33601, 16640, 
        33217, 32897, 16448)
    """CRC-16 lookup table with 256 elements. Built with this code:           
        poly=0xA001; table = []
        for index in range(256):
            data = index << 1
            crc = 0
            for _ in range(8, 0, -1):
                data >>= 1
                if (data ^ crc) & 0x0001:
                    crc = (crc >> 1) ^ poly
                else:
                    crc >>= 1
            table.append(crc)
        output = ''
        for i, m in enumerate(table):
            if not i%11:
                output += "\n"
            output += "{:5.0f}, ".format(m)
        print output """
    register = 0xFFFF    
    for c in data:
        register = (register >> 8) ^ crc16tabelle[(register ^ c) & 0xFF]
    res = data[:]    
    res.append(register & 0xFF)
    res.append(register//256)
    return res   

###############################################################################
def hexStringToIntArray(ask):
    """
    wandelt Hex-String in Integer-Array (type: list) um.
    Hex-String besteht aus getrennten Hex (2 Zeichen) mit "-" Bindestrich oder 
    Leerzeichen '' oder kein Zeichen dazwischen. Z.B. 'AA-01-F3' oder '0101-65CD'
    """
    hex = ask.replace('-','')
    hex = hex.replace(' ','')
    res = []
    for h in range(0,len(hex)-1,2):
        hexVal = hex[h:h+2]
        intVal = int(hexVal,16)
        res.append(intVal)
    return res

###############################################################################
def comMod(port, adr, fkt, reg, leng, form):  
    """
    Führt Low-Level Kommunikation aus auf MODBUS (serial) inkl. ckeck-sum CRC-16 Modbus
    
    port  (Serial Object) COM-Port als Objekt
    adr   (hex String, 1 Byte 2 Zeichen) MODBUS-Adresse, z.B. '01'
    fkt   (hex String, 1 Byte 2 Zeichen) MODBUS Funktion. Typisch '03'
    reg   (hex String, 1 Byte 2 Zeichen) Startregister, z.B. '200A'
    leng  (hex String, 2 Byte 4 Zeichen) Länge/Anz. Register z.B. '0001' (1 Register = 2 Byte)
    form  (string) Formatierung der Antwortdaten
            Hukse Strahlung:   '>i':  > big endian, sign (4) Integer
            Hukse Temperatur:  '>h':  > big endian, sign short (2) Integer
            PRO380:            '>f':  > big endian, float (4)
            siehe: https://docs.python.org/3/library/struct.html
    """
    askStr = adr + fkt + reg + leng
    askInt = hexStringToIntArray(askStr)
    askIntcrc = addCRC(askInt)
    askB = bytes(askIntcrc)
    blen = 1 + 1 + 1 + (askInt[5] + askInt[4]*256)*2 + 2
    
    port.write(askB)
    answer = port.read(blen)
    
    try:    
        dataRAW = answer[3:2+answer[2]+1] # +1 weil letzter Index nicht genommen wird
        dataBuffer = unpack(form, dataRAW)
        data = dataBuffer[0]
    except:
        data = float('nan')

    return data

################################################################################
def comHukse(prt):
    """
    resH, resT = comHukse(prt)
    
    Führt Hukseflux-Kommunikation aus und gibt definiert Strahlung und Temperatur zurück
    
    B+ pin2 weiss
    A- pin5 grau
    vdc+ pin1 braun
    gnd- pin4 schwarz/grün

    """
    port = serial.Serial(port = prt,
        baudrate = 19200, \
        bytesize = 8, \
        parity = 'E', \
        stopbits = 1, \
        timeout = 0.5)
    adr  = '01'   # 1 Byte/2 Sign, hex-String 
    fkt  = '03'   # 1 Byte/2 Sign, hex-String 

    # Temperatur
    reg  = '0006' # 2 Byte/4 Sign, hex-String
    leng = '0001' # 2 Byte/4 Sign, hex-String
    form = '>h'   #  > big endian, sign shot (1) Integer
    resT = comMod(port, adr, fkt, reg, leng, form)
    
    # Strahlung
    reg  = '0002' # 2 Byte/4 Sign, hex-String.Starting Register 
    leng = '0002' # 2 Byte/4 Sign, hex-String. Length of Registers
    form = '>i'   #  > big endian, float (4)
    resH = comMod(port, adr, fkt, reg, leng, form)    
    port.close()
    
    dic = {'H':resH/100, 'T': resT/100 }
    
    return dic

################################################################################
def comPRO380(prt, adr):

    """
    Leistungsdaten (P)
    dic = comPRO380_P(port,'adr')
    
    Führt Kommunikation mit PRO380 aus
	
    """
    port = serial.Serial(port = prt,
        baudrate = 9600, \
        bytesize = 8, \
        parity = 'E', \
        stopbits = 1, \
        timeout = 0.5)
    time.sleep(0.01) # wird benötgit 
    fkt  = '03'   # 1 Byte/2 Sign, hex-String 
    form= '>f'
    reg  = '5002'   
    anzReg = 25
    leng = '%04x'%(anzReg*2)  # 30hex = 48 Bytes (96 hex stellen) 24 Register    
    askStr = adr + fkt + reg + leng
    askInt = hexStringToIntArray(askStr)
    askIntcrc = addCRC(askInt)
    askB = bytes(askIntcrc)
    blen = 1 + 1 + 1 + (askInt[5] + askInt[4]*256)*2 + 2
    port.write(askB)
    answer = port.read(blen)
    dataRAW = answer[3:-2] # +1 weil letzter Index nicht genommen wird
    data = np.zeros(anzReg)
    for i in range(anzReg):
        try:
            data[i] = unpack(form, dataRAW[i*4:(i+1)*4])[0]
        except:
            data[i] = float('nan')          
    dic = {
            'L1Volt'    :data[0], 
            'L2Volt'    :data[1],  
            'L3Volt'    :data[2],  
            'Freque'    :data[3],  
            'L1Curr'    :data[5], 
            'L2Curr'    :data[6], 
            'L3Curr'    :data[7], 
            'L1P'       :data[9], 
            'L2P'       :data[10], 
            'L3P'       :data[11], 
            'L1Q'       :data[13], 
            'L2Q'       :data[14], 
            'L3Q'       :data[15], 
            'L1cosp'    :data[21], 
            'L2cosp'    :data[22], 
            'L3cosp'    :data[23],
           }    
    reg  = '6006'   
    anzReg = 33
    leng = '%04x'%(anzReg*2)  # 30hex = 48 Bytes (96 hex stellen) 24 Register    
    askStr = adr + fkt + reg + leng
    askInt = hexStringToIntArray(askStr)
    askIntcrc = addCRC(askInt)
    askB = bytes(askIntcrc)
    blen = 1 + 1 + 1 + (askInt[5] + askInt[4]*256)*2 + 2
    port.write(askB)
    answer = port.read(blen)
    dataRAW = answer[3:-2] # +1 weil letzter Index nicht genommen wird
    data = np.zeros(anzReg)
    for i in range(anzReg):
        try:
            data[i] = unpack(form, dataRAW[i*4:(i+1)*4])[0]
        except:
            data[i] = float('nan')           
    dic.update({
            'L1WirkTot'    :data[0], 
            'L2WirkTot'    :data[1], 
            'L3WirkTot'    :data[2], 
            'L1WirkVor'    :data[6], 
            'L2WirkVor'    :data[7], 
            'L3WirkVor'    :data[8], 
            'L1WirkRue'    :data[12],
            'L2WirkRue'    :data[13], 
            'L3WirkRue'    :data[14], 
            'L1BlinTot'    :data[18], 
            'L2BlinTot'    :data[19], 
            'L3BlinTot'    :data[20], 
            'L1BlinVor'    :data[24], 
            'L2BlinVor'    :data[25], 
            'L3BlinVor'    :data[26], 
            'L1BlinRue'    :data[30],
            'L2BlinRue'    :data[31], 
            'L3BlinRue'    :data[32],
            })
    port.close()
    return(dic)


##################### End ######################################


port = '/dev/ttyUSB0'
slaveAdresse = '01'
print(comPRO380(port, slaveAdresse))

