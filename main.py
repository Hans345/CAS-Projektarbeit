# Read Data from Power Meter INEPRO METERING PRO380-MOD

# import
import pymodbus
import serial
from pymodbus.constants import Endian
from pymodbus.constants import Defaults
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer


# ------- functions -----------
def print_hi(name):
    print(f'Hi, {name}')


# -------- basic settings ----------
SERIAL = '/dev/ttyUSB0'  # type dmesg on rpi console
BAUD = 9600
MB_ID = 1

# -------- RS485 Setup ----------
client = ModbusClient(method='rtu', port=SERIAL, stopbits=1, bytesize=8, timeout=0.25, baudrate=BAUD, parity='E')

# -------- main ----------
if __name__ == '__main__':
    print_hi('PyCharm')
    try:
        if client.connect():
            result = client.read_holding_registers(address=0x6000, count=2, unit=0x03)
            decod = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)
            print("Result: ")
            print(decod)
        else:
            print("Port failed to open")
        client.close()
    except:
        print("An exception occured")
