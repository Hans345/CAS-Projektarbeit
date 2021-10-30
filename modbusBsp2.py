import minimalmodbus

SERIAL = '/dev/ttyUSB0'  # type dmesg on rpi console
L3_Register = 5006
f_Register = 5008

# Set up instrument
instrument = minimalmodbus.Instrument(SERIAL, 1, mode=minimalmodbus.MODE_RTU)

# Make the settings explicit
instrument.serial.baudrate = 9600  # Baud
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout = 1  # seconds

# Good practice
instrument.close_port_after_each_call = True

instrument.clear_buffers_before_each_transaction = True

# Read temperatureas a float
# if you need to read a 16 bit register use instrument.read_register()
Vl3 = instrument.read_register(L3_Register)

# Read the humidity
f = instrument.read_register(f_Register)

# Pront the values
print('The Voltage is: %.1f V\r' % Vl3)
print('The Frequency is: %.1f Hz\r' % f)
