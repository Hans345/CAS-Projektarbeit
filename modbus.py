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
    instrument.serial.timeout = 1  # seconds
    # Good practice
    instrument.close_port_after_each_call = True
    instrument.clear_buffers_before_each_transaction = True

    return instrument


###############################################################################
def hex2int(a):
    """
    wandelt Hex-Value (type list) in numpy-Value um.
    """
    b = np.array(int(a, 16))
    return b


###############################################################################
def getAdrSpace(startAdr, endArd, adrOffset):
    """
    :param startAdr: type: string array in hex
    :param endArd: type: string array in hex
    :param adrOffset: type: string array in hex
    :return: type: Adressraum in dezimal
    """
    integer_input = [hex2int(startAdr), hex2int(endArd), hex2int(adrOffset)]
    l = int((integer_input[1] - integer_input[0]) / integer_input[2] + 1)

    curr_address = integer_input[0]
    integer_address = np.zeros(l, dtype=int)
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
        # read data Row
        data = np.array(np.zeros(l), dtype=float)[np.newaxis] # Zeilenvektor
        t0 = dt.datetime.now()
        for i in range(l):
            data[0,i] = instrument.read_float(int(adrSpace[i]))
        t1 = dt.datetime.now()
        print('Time for reading: ' + str(t1 - t0))

        # save to  Data Frame
        df = pd.DataFrame(data, columns=s)
        # df = df.assign(time=dt.datetime.now())
        # df = df.set_index('time', drop=True)
    else:
        print('Inputparameter müssen die gleiche Grösse haben!')

    return df


###############################################################################
def delDataCol(data, s):
    """
    :param data: type: Data Frame
    :param s: type: string
    :return: type: Data Frame without cols, which named in s
    """
    return data.drop(columns=s)

def getData():
    """
    :return: type: DataFrame
    """
    # init Modbus
    port = '/dev/ttyUSB0'
    adr = 1
    modBus = initModbus(port, adr)

    # calc Register Addresses
    adrSpace1 = getAdrSpace("5000", "5030", "02")
    adrSpace2 = getAdrSpace("6006", "600A", "02")
    adrSpace3 = getAdrSpace("602A", "602E", "02")

    # read Data and Store to pandas Dataframe
    s1 = (["V", "V_L1", "V_L2", "V_L3", "freq", "I", "I_L1", "I_L2", "I_L3", "p_sum", "p_L1", "p_L2", "p_L3", "q_sum",
           "q_L1", "q_L2", "q_L3", "s_sum", "s_L1", "s_L2", "s_L3", "pf", "pf_L1", "pf_L2", "pf_L3"])
    s2 = (["eAct_L1", "eAct_L2", "eAct_L3"])
    s3 = (["eReact_L1", "eReact_L2", "eReact_L3"])
    data1 = getDataRow(modBus, adrSpace1, s1)
    data2 = getDataRow(modBus, adrSpace2, s2)
    data3 = getDataRow(modBus, adrSpace3, s3)

    # clear unrelevant Data Cols
    sDel = (["V", "I"])
    data1 = delDataCol(data1, sDel)

    # final DataRow
    data = pd.concat([data1, data2, data3], axis=1)
    data = data.assign(time=dt.datetime.now())
    data = data.set_index('time', drop=True)

    return data



# print all
# print("##########")
# print("Addressraum 1:\n" + str(adrSpace1))
# print("##########")
# print("Addressraum 2:\n" + str(adrSpace2))
# print("##########")
# print("Addressraum 3:\n" + str(adrSpace3))
# print("##########")
# print("##########")
# print("Data 1: \n" + str(data1.dtypes))
# print("Data 1: \n" + str(data1))
# print("##########")
# print("Data 2: \n" + str(data2.dtypes))
# print("Data 2: \n" + str(data2))
# print("##########")
# print("Data 3: \n" + str(data3.dtypes))
# print("Data 3: \n" + str(data3))

# test = pd.DataFrame([[data1.iloc[0]["V_L3"], data1.iloc[0]["I_L3"], data1.iloc[0]["pf_L3"], data1.iloc[0]["p_L3"],
#                       data2.iloc[0]["eAct_L3"],
#                       data3.iloc[0]["eReact_L3"]]])
# print("Relevant Data: \n" + str(test))

print("Final DataRow: \n" + str(getData()))



