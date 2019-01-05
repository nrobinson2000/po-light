#!/usr/bin/env python3

# inputs
# Serial port
# number of readings

import serial
import sys

neutralBaudRate = 9600

try:
    portName = sys.argv[1]

except IndexError:
    print()
    print("Please provide a serial port!")
    print("Example: ")
    print(sys.argv[0] + " /dev/ttyACM0 14400")
    print()

else:
    try:
        baudRate = sys.argv[2]

    except IndexError:
        print()
        print("You must specify the baud rate!")
        print("Example: ")
        print(sys.argv[0] + " /dev/ttyACM0 14400")

    else:
        try:
            ser = serial.Serial(portName, baudRate)
            ser.close()

            ser = serial.Serial(portName, neutralBaudRate)
            ser.close()
        except serial.serialutil.SerialException:
            do = "nothing" # Do nothing
