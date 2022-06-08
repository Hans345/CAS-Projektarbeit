"""
Kommunikation mit PRO380
@author: Raphael Baumeler/2021

Folgende funktion wird extern benötigt: get_data()
Es können nur floats gelesen werden.
Wenn neue Register gelesen werden sollen muss nur diese Funktion angepasst werden
"""

import datetime as dt
import minimalmodbus
import numpy as np
import pandas as pd


###############################################################################
def init_modbus(prt, slave_adr):
    """
    :param prt: type: string
    :param slave_adr:  type: string
    :return: instrument: minimalmodbusobject
    """
    # Set up instrument
    instrument = minimalmodbus.Instrument(prt, slave_adr, mode=minimalmodbus.MODE_RTU)
    # Make the settings explicit
    instrument.serial.baudrate = 9600  # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 0.2  # seconds
    # Good practice
    instrument.close_port_after_each_call = False
    instrument.clear_buffers_before_each_transaction = False

    return instrument


###############################################################################
def hex2int(a):
    """
    wandelt Hex-Value (type list) in numpy-Value um.
    """
    b = np.array(int(a, 16))
    return b


###############################################################################
def get_adr_space(start_adr, end_ard, adr_offset):
    """
    :param start_adr: type: string array in hex
    :param end_ard: type: string array in hex
    :param adr_offset: type: string array in hex
    :return: type: Adressraum in dezimal
    """
    integer_input = [hex2int(start_adr), hex2int(end_ard), hex2int(adr_offset)]
    l: int = int((integer_input[1] - integer_input[0]) / integer_input[2] + 1)

    curr_address = integer_input[0]
    integer_address = np.zeros(l, dtype=int)
    for i in range(l):
        integer_address[i] = curr_address
        curr_address = curr_address + integer_input[2]
    return integer_address


###############################################################################
def get_data_row(instrument, adr_space, s):
    """
    :param instrument: type modbusObject
    :param adr_space: type: ndarray
    :param s: type: list
    :return: type: DataFrame
    """

    l: object = s.__len__()
    # Check Input
    if adr_space.shape[0] == s.__len__():
        # read data Row
        data = np.array(np.zeros(l), dtype=float)[np.newaxis]  # Zeilenvektor
        for i in range(l):
            data[0, i] = np.round(instrument.read_float(int(adr_space[i])), decimals=3)
        # save to  Data Frame
        df = pd.DataFrame(data, columns=s)
    else:
        print('Inputparameter müssen die gleiche Grösse haben!')

    return df


###############################################################################
def del_data_col(data, s):
    """
    :param data: type: Data Frame
    :param s: type: string
    :return: type: Data Frame without cols, which named in s
    """
    return data.drop(columns=s)


###############################################################################
def get_data(port, adr):
    """
    :return: type: DataFrame
    """
    # init Modbus
    mod_bus = init_modbus(port, adr)

    # calc Register Addresses
    adr_space1 = get_adr_space("5000", "5030", "02")
    adr_space2 = get_adr_space("6000", "600A", "02")
    adr_space3 = get_adr_space("6024", "602E", "02")

    # read Data and Store to pandas Dataframe
    s1 = (["V", "V_L1", "V_L2", "V_L3", "freq", "I", "I_L1", "I_L2", "I_L3", "p_sum", "p_L1", "p_L2", "p_L3", "q_sum",
           "q_L1", "q_L2", "q_L3", "s_sum", "s_L1", "s_L2", "s_L3", "pf", "pf_L1", "pf_L2", "pf_L3"])
    s2 = (["eAct_Tot", "eAct_Tot1", "e_Act_Tot2", "eAct_L1", "eAct_L2", "eAct_L3"])
    s3 = (["eReact_Tot", "eReact_Tot1", "eReact_Tot2", "eReact_L1", "eReact_L2", "eReact_L3"])
    data1 = get_data_row(mod_bus, adr_space1, s1)
    data2 = get_data_row(mod_bus, adr_space2, s2)
    data3 = get_data_row(mod_bus, adr_space3, s3)

    data = pd.concat([data1, data2, data3], axis=1)
    # clear unrelevant Data Cols
    s_del = (["V", "I", "eAct_Tot1", "e_Act_Tot2", "eReact_Tot1", "eReact_Tot2"])
    # create final DataRow
    data = del_data_col(data, s_del)
    data = data.assign(time=dt.datetime.now())
    data = data.set_index('time', drop=True)

    return data
