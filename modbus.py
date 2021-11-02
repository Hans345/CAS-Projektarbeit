import minimalmodbus
import datetime as dt
import numpy as np
import pandas as pd


###############################################################################
def initModbus(prt, slaveAddress):
    """
    :param prt: type: string
    :param slaveAddress:  type: string
    :return: instrument: minimalmodbusobject
    """
    # Set up instrument
    instrument = minimalmodbus.Instrument(prt, slaveAddress, mode=minimalmodbus.MODE_RTU)
    # Make the settings explicit
    instrument.serial.baudrate = 9600  # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 0.1  # seconds
    # Good practice
    instrument.close_port_after_each_call = True
    instrument.clear_buffers_before_each_transaction = True

    return instrument


###############################################################################
def hex2int(a):
    """
    wandelt Hex-Value (type list) in numpy-Value um.
    """
    b = int(a, 16)
    return b


###############################################################################
def getAdrSpace(startAdr, endAdr, adrOffset):
    """
    :param startAdr: type: string in hex
    :param endAdr: type: string in hex
    :param adrOffset: type: string in hex
    :return: type: Adressraum in dezimal
    """
    integer_input = [hex2int(startAdr), hex2int(endAdr), hex2int(adrOffset)]
    l = int((integer_input[1] - integer_input[0]) / integer_input[2] + 1)

    curr_address = integer_input[0]
    integer_address = np.zeros(l)
    for i in range(l):
        integer_address[i] = curr_address
        curr_address = curr_address + integer_input[2]
    return integer_address


###############################################################################
def getDataRow(instrument, adrSpace, s):
    """
    :param instrument: type modbusObject
    :param adrSpace: type: ndarray
    :param s: type: list
    :return: type: DataFrame
    """

    l = s.__len__()
    # Check Input
    if (adrSpace.shape[0] == s.__len__()):
        # init Data Frame
        df = pd.DataFrame([], columns=["time",s])

        # read data Row
        df[0] = dt.datetime.now()
        for i in range(l):
            df[i+1] = instrument.read_float(adrSpace[i])

        #
    else:
        print('Inputparameter müssen die gleiche Grösse haben!')

    return df


# init Modbus
port = '/dev/ttyUSB0'
adr = '01'
modBus = initModbus(port,adr)

# calc Register Addresses
adrSpace = getAdrSpace("5000", "5030", "02")
print(adrSpace)

# read Data and Store to pandas Dataframe
s = (["V", "V_L1", "V_L2", "V_L3", "freq", "I", "I_L1", "I_L2", "I_L3", "p_sum", "p_L1", "p_L2", "p_L3", "q_sum", "q_L1",
      "q_L2", "q_L3", "s_sum", "s_L1", "s_L2", "s_L3", "pf", "pf_L1", "pf_L2", "pf_L3"])
data = getDataRow(modBus, adrSpace, s)
print(data)
