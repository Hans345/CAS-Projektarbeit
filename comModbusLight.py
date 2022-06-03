"""
Bibliothek zur Kommunikation mit Engerie-Geräte
@author: Raphael Baumeler/2022
"""

import minimalmodbus

# init Modbus
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1, mode=minimalmodbus.MODE_RTU, debug=True)
instrument.serial.baudrate = 9600  # Baud
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout = 4  # seconds
# Good practice
instrument.close_port_after_each_call = True
instrument.clear_buffers_before_each_transaction = True

# read Data
adr = 16388  # Baud rate

try:
    print(instrument.read_register(registeraddress=adr, functioncode=3, signed=True))

except IOError:
    print("Failed to read from Instrument")
