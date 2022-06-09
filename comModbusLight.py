"""
Bibliothek zur Kommunikation mit Enegerie-Geräte
@author: Raphael Baumeler/2022
"""

import minimalmodbus
import numpy as np
from datetime import datetime

# init Modbus
instrument1 = minimalmodbus.Instrument('/dev/ttyUSB0', 1, mode=minimalmodbus.MODE_RTU, debug=False)
instrument1.serial.baudrate = 9600  # Baud
instrument1.serial.bytesize = 8
instrument1.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument1.serial.stopbits = 1
instrument1.serial.timeout = 4  # seconds
# Good practice
instrument1.close_port_after_each_call = True
instrument1.clear_buffers_before_each_transaction = True

# init Modbus
instrument2 = minimalmodbus.Instrument('/dev/ttyUSB0', 2, mode=minimalmodbus.MODE_RTU, debug=False)
instrument2.serial.baudrate = 9600  # Baud
instrument2.serial.bytesize = 8
instrument2.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument2.serial.stopbits = 1
instrument2.serial.timeout = 4  # seconds
# Good practice
instrument2.close_port_after_each_call = True
instrument2.clear_buffers_before_each_transaction = True

# read Data at Adress (dezimal):
V_L1 = 20482
V_L2 = 20484
V_L3 = 20486

try:
    print("Daten am: " + str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
    print("Prüfstand Ecke: ")
    print("V_L1: " + str(np.round(instrument2.read_float(registeraddress=V_L1, functioncode=3),2)) + "V")
    print("V_Pruefstand1: " + str(np.round(instrument2.read_float(registeraddress=V_L2, functioncode=3))) + "V")
    print("V_Pruefstand2: " + str(np.round(instrument2.read_float(registeraddress=V_L3, functioncode=3))) + "V")
    print("---------------------------")   
    print("Prüfstand rechts vom Lift: ")
    print("V_L1: " + str(np.round(instrument1.read_float(registeraddress=V_L1, functioncode=3),2)) + "V")
    print("V_Pruefstand1: " + str(np.round(instrument1.read_float(registeraddress=V_L2, functioncode=3))) + "V")
    print("V_Pruefstand2: " + str(np.round(instrument1.read_float(registeraddress=V_L3, functioncode=3))) + "V")
    
except IOError:
    print("Failed to read from Instrument")
