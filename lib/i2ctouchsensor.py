# This is a microbit micropython translation of the Arduino i2ctouchsensor Library, found here:
# https://github.com/Seeed-Studio/Grove_I2C_Touch_Sensor
# LGPL v2.1

from microbit import i2c
from micropython import const

class i2ctouchsensor:

    #define registers
    MHD_R = const(0x2B)
    NHD_R = const(0x2C)
    NCL_R = const(0x2D)
    FDL_R = const(0x2E)

    MHD_F = const(0x2F)
    NHD_F = const(0x30)
    NCL_F = const(0x31)
    FDL_F = const(0x32)

    #Electrode Threshold Registers: _T = Touch _R = Released
    ELE0_T = const(0x41)
    ELE0_R = const(0x42)
    ELE1_T = const(0x43)
    ELE1_R = const(0x44)
    ELE2_T = const(0x45)
    ELE2_R = const(0x46)
    ELE3_T = const(0x47)
    ELE3_R = const(0x48)
    ELE4_T = const(0x49)
    ELE4_R = const(0x4A)
    ELE5_T = const(0x4B)
    ELE5_R = const(0x4C)
    ELE6_T = const(0x4D)
    ELE6_R = const(0x4E)
    ELE7_T = const(0x4F)
    ELE7_R = const(0x50)
    ELE8_T = const(0x51)
    ELE8_R = const(0x52)
    ELE9_T = const(0x53)
    ELE9_R = const(0x54)
    ELE10_T = const(0x55)
    ELE10_R = const(0x56)
    ELE11_T = const(0x57)
    ELE11_R = const(0x58)

    FIL_CFG = const(0x5D)

    #Number of Electrodes register
    ELE_CFG = const(0x5E)

    #define global vals
    TOU_THRESH = const(0x0F)
    REL_THRESH = const(0x0A)
    ADDRESS = 0x5A

    touchstates = []

    #write given value to mpr121 register
    def setregister(self, address, register, value):
        i2c.write(address, bytearray([register, value]))

    # read bytes from I2C bus, convert to list of boolean values
    def ReadTouch(self):
        readbytes = i2c.read(self.ADDRESS, 2)
        LSB = int(readbytes[0])
        MSB = int(readbytes[1])

        touched = ((MSB << 8) | LSB)

        for i in range(12):
            if touched & (1<<i):
                self.touchstates[i] = 1
            else:
                self.touchstates[i] = 0

    def __init__(self, address):
        self.ADDRESS = address

        for i in range(12):
            self.touchstates.append(0)

        #filtering when Data > baseline
        self.setregister(address, self.MHD_R, 0x01)
        self.setregister(address, self.NHD_R, 0x01)
        self.setregister(address, self.NCL_R, 0x00)
        self.setregister(address, self.FDL_R, 0x00)

        #filtering when data < baseline
        self.setregister(address, self.MHD_F, 0x01)
        self.setregister(address, self.NHD_F, 0x01)
        self.setregister(address, self.NCL_F, 0xFF)
        self.setregister(address, self.FDL_F, 0x02)

        #set Electrode thresholds
        self.setregister(address, self.ELE0_T, self.TOU_THRESH)
        self.setregister(address, self.ELE0_R, self.REL_THRESH)

        self.setregister(address, self.ELE1_T, self.TOU_THRESH)
        self.setregister(address, self.ELE1_R, self.REL_THRESH)

        self.setregister(address, self.ELE2_T, self.TOU_THRESH)
        self.setregister(address, self.ELE2_R, self.REL_THRESH)

        self.setregister(address, self.ELE3_T, self.TOU_THRESH)
        self.setregister(address, self.ELE3_T, self.REL_THRESH)

        self.setregister(address, self.ELE4_T, self.TOU_THRESH)
        self.setregister(address, self.ELE4_R, self.REL_THRESH)

        self.setregister(address, self.ELE5_T, self.TOU_THRESH)
        self.setregister(address, self.ELE5_R, self.REL_THRESH)

        self.setregister(address, self.ELE6_T, self.TOU_THRESH)
        self.setregister(address, self.ELE6_R, self.REL_THRESH)

        self.setregister(address, self.ELE7_T, self.TOU_THRESH)
        self.setregister(address, self.ELE7_R, self.REL_THRESH)

        self.setregister(address, self.ELE8_T, self.TOU_THRESH)
        self.setregister(address, self.ELE8_R, self.REL_THRESH)

        self.setregister(address, self.ELE9_T, self.TOU_THRESH)
        self.setregister(address, self.ELE9_R, self.REL_THRESH)

        self.setregister(address, self.ELE10_T, self.TOU_THRESH)
        self.setregister(address, self.ELE10_R, self.REL_THRESH)

        self.setregister(address, self.ELE11_T, self.TOU_THRESH)
        self.setregister(address, self.ELE11_R, self.REL_THRESH)

        self.setregister(address, self.FIL_CFG, 0x04)

        #configure 12 electrodes.
        self.setregister(address, self.ELE_CFG, 0x0C)