# Copyright (c) 2014 GhostSonic
# Licensed under the MIT License
# See LICENSE.txt for details

import serial
import time
import os
from tkinter import filedialog, Tk
import sys

ser =  serial.Serial("COM3", 115200) #Make sure you change the COM port to whatever it is on your setup.

root = Tk()
root.withdraw()

tasFilePath = filedialog.askopenfilename(filetypes = [('SNES TAS r16m dump', '.r16m'), ('All files','.*')])

tasFile = open(tasFilePath,'rb')
tasFileSize = int((os.stat(tasFilePath).st_size)/16) #gets the file size, divided by 2 for 2 input per frame.

time.sleep(1)
ser.write([0x10])

lookup = [0x0, 0x8, 0x4, 0xc, 0x2, 0xa, 0x6, 0xe, 0x1, 0x9, 0x5, 0xd, 0x3, 0xb, 0x7, 0xf]

def reverse(n): return (lookup[int(n)&0b00001111]<<4) | lookup[n>>4];

print('Ready...')

def main():
	for i in range(int(sys.argv[1])):
		ser.write([0x00])
		ser.write([0x00])
	amountRead = 0
	endOfFile = False
	while 1:
		#os.system("title " + ('Frame Counter: ' + str(amountRead) + '/' + str(tasFileSize))) #This is just pretty. But it seems to cause desyncs if it's active, uncomment at your own risk.
		
		if (convertToInt(ser.read(size=1)) == 0x12): #Receives the byte from the Arduino upon latch
			if (not endOfFile):
				#frame=tasFile.read(16)
				SNESData2 = tasFile.read(1)#reverse(frame[1])
				SNESData1 = tasFile.read(1)#reverse(frame[2])
				ser.write(SNESData1)
				ser.write(SNESData2)
				tasFile.read(14)
				print ("%d: %s %s" % (amountRead, hex(int.from_bytes(SNESData1,'little')), hex(int.from_bytes(SNESData2,'little'))))
				amountRead += 1
			else:
				ser.write([0x00])
				ser.write([0x00]) 					# Send 0 if the end of file is reached
			if (amountRead >= tasFileSize and not endOfFile):
				endOfFile = True
				print("End of File!")
		else:
			pass

def convertToInt(arrayInput):
	return int(ord(arrayInput[:1]))
	
def freeze():
	while 1:
		pass
		
if __name__ == "__main__":
	main()
