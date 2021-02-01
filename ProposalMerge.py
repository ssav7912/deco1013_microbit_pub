# CUBIT Code for DECO1013
# Soren Saville Scott 2020
# TODO:
# - Optimise for Microbit (ints only!)

#DONE:
# - Touch sensor library
# - Neopixel ring - custom micropython runtime
# - wireless communication

from microbit import *
import neopixel
from math import trunc

# This is a microbit micropython translation of the Arduino i2ctouchsensor Library, found here:
# https://github.com/Seeed-Studio/Grove_I2C_Touch_Sensor
# LGPL v2.1

from microbit import i2c
from micropython import const
import radio
import utime

class i2ctouchsensor:

	# #define registers
	# CONST_MHD_R = const(0x2B)
	# CONST_NHD_R = const(0x2C)
	# CONST_NCL_R = const(0x2D)
	# CONST_FDL_R = const(0x2E)

	# CONST_MHD_F = const(0x2F)
	# CONST_NHD_F = const(0x30)
	# CONST_NCL_F = const(0x31)
	# CONST_FDL_F = const(0x32)

	# #Electrode Threshold Registers: _T = Touch _R = Released
	# CONST_ELE0_T = const(0x41)
	# CONST_ELE0_R = const(0x42)
	# CONST_ELE1_T = const(0x43)
	# CONST_ELE1_R = const(0x44)
	# CONST_ELE2_T = const(0x45)
	# CONST_ELE2_R = const(0x46)
	# CONST_ELE3_T = const(0x47)
	# CONST_ELE3_R = const(0x48)
	# CONST_ELE4_T = const(0x49)
	# CONST_ELE4_R = const(0x4A)
	# CONST_ELE5_T = const(0x4B)
	# CONST_ELE5_R = const(0x4C)
	# CONST_ELE6_T = const(0x4D)
	# CONST_ELE6_R = const(0x4E)
	# CONST_ELE7_T = const(0x4F)
	# CONST_ELE7_R = const(0x50)
	# CONST_ELE8_T = const(0x51)
	# CONST_ELE8_R = const(0x52)
	# CONST_ELE9_T = const(0x53)
	# CONST_ELE9_R = const(0x54)
	# CONST_ELE10_T = const(0x55)
	# CONST_ELE10_R = const(0x56)
	# CONST_ELE11_T = const(0x57)
	# CONST_ELE11_R = const(0x58)

	# CONST_FIL_CFG = const(0x5D)

	# #Number of Electrodes register
	# CONST_ELE_CFG = const(0x5E)

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

		#filtering when Data > baseline (register block 1 - MHD_R)
		self.setregister(address, 0x2B, 0x01)
		self.setregister(address, 0x2C, 0x01)
		self.setregister(address, 0x2D, 0x00)
		self.setregister(address, 0x2E, 0x00)

		#filtering when data < baseline (register block 2 - MHD_F)
		self.setregister(address, 0x2F, 0x01)
		self.setregister(address, 0x30, 0x01)
		self.setregister(address, 0x31, 0xFF)
		self.setregister(address, 0x32, 0x02)

		#set Electrode thresholds (Register block 3 - ELE0_T)
		self.setregister(address, 0x41, self.TOU_THRESH)
		self.setregister(address, 0x42, self.REL_THRESH)

		self.setregister(address, 0x43, self.TOU_THRESH)
		self.setregister(address, 0x44, self.REL_THRESH)

		self.setregister(address, 0x45, self.TOU_THRESH)
		self.setregister(address, 0x46, self.REL_THRESH)

		self.setregister(address, 0x47, self.TOU_THRESH)
		self.setregister(address, 0x48, self.REL_THRESH)

		self.setregister(address, 0x49, self.TOU_THRESH)
		self.setregister(address, 0x4A, self.REL_THRESH)

		self.setregister(address, 0x4B, self.TOU_THRESH)
		self.setregister(address, 0x4C, self.REL_THRESH)

		self.setregister(address, 0x4D, self.TOU_THRESH)
		self.setregister(address, 0x4E, self.REL_THRESH)

		self.setregister(address, 0x4F, self.TOU_THRESH)
		self.setregister(address, 0x50, self.REL_THRESH)

		self.setregister(address, 0x51, self.TOU_THRESH)
		self.setregister(address, 0x52, self.REL_THRESH)

		self.setregister(address, 0x53, self.TOU_THRESH)
		self.setregister(address, 0x54, self.REL_THRESH)

		self.setregister(address, 0x55, self.TOU_THRESH)
		self.setregister(address, 0x56, self.REL_THRESH)

		self.setregister(address, 0x57, self.TOU_THRESH)
		self.setregister(address, 0x58, self.REL_THRESH)

		self.setregister(address, 0x5D, 0x04)

		#configure 12 electrodes.
		self.setregister(address, 0x5E, 0x0C)


np = neopixel.NeoPixel(pin0, 16, 4)
touch = i2ctouchsensor(0x5A)
hue = 0
sat = 255
radio.on()
radio.config(length=8, queue=1, channel=64, data_rate=radio.RATE_250KBIT)

# Converts HSV value to RGB using formula at
# https://en.wikipedia.org/wiki/HSL_and_HSV
# hue < 360, sat < 1, val < 1
def hsvToRgb(hue, sat, val):
	# TO_OPTIMISE:
	# rewrite to use ints only? Assume 8 bits for HSV value...
	# Look into: https://www.vagrearg.org/content/hsvrgb

	magicnums = [5, 3, 1] #"magic" numbers to get correct values for each channel.
	RGB = [0, 0, 0]

	for i in range(3):
		n = magicnums[i]
		k = (n + (hue/60)) % 6
		RGB[i] = val - val * sat * max(0, min(k, 4 - k, 1))
		RGB[i] = trunc(remap(RGB[i], 0, 1, 0, 255)) #remaps and truncates floats into ints between 0 - 255, for compatibility and speed.
	return tuple(RGB)

# simple mapping function
def remap(val, fromStart, fromEnd, toStart, toEnd):
	return (val-fromStart) * (toEnd - toStart) / (fromEnd - fromStart) + toStart

	
#init LEDs
rgbw = hsvToRgb(hue, remap(sat, 0, 255, 0, 1), 1) + (0,)

for i in range(0, len(np)):
	np[i] = rgbw

np.show()	
	
	
# Main Loop.
# iterates over neopixel list and gradually cycles hues.
while True:
	touch.ReadTouch()
	hueold = hue
	satold = sat

	
	if touch.touchstates[0]:
		if hue > 1:
			hue -= 1
		else:
			hue = 0
	elif touch.touchstates[1]:
		if hue < 359:
			hue += 1
		else:
			hue = 360

	if touch.touchstates[2]:
		if sat > 1:
			sat -= 1
		else:
			sat = 255
	elif touch.touchstates[3]:
		if sat < 254:
			sat += 1
		else:
			sat = 0

	#aim to update state once every 100 miliseconds.
	if utime.ticks_ms() % 1000 == 0:
		# remap values to 8 bit ints for transfer - not efficient or accurate...
		hue = trunc(remap(hue, 0, 360, 0, 255))
		sat = trunc(remap(sat, 0, 255, 0, 255))
		hsvtuple = (hue,sat)
		
		radio.send_bytes(bytes(hsvtuple))
		try:
			hsvtuple = tuple(radio.receive_bytes())
			hue = hsvtuple[0]
			sat = hsvtuple[1]
			

		except:
			pass
			
		finally:
			#bring values back to correct ranges
			 hue = trunc(remap(hue, 0, 255, 0, 360))
	
	rgbw = hsvToRgb(hue,remap(sat, 0, 255, 0, 1),1) + (0,)	
	for i in range(0, len(np)):
		np[i] = rgbw
	
	#only run np.show() if colours have been updated.
	#Keeps things spry and prevents IRQ Disabled assembly code from running every tick.
	if hueold != hue or satold != sat:
		np.show()