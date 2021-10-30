import pymodbus
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

SERIAL = '/dev/ttyUSB0'
baudrate = 9600
client = ModbusClient(
    method='rtu'
    , port=SERIAL
    , stopbits=1
    , bytesize=8
    , baudrate=baudrate
    , parity='E'
    , timeout=0.25
)
connection = client.connect()
registers = client.read_holding_registers(5000, 10, unit=1)  # start_address, count, slave_id
print(registers.registers)
