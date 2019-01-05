#!/usr/bin/env python3

from DeviceControl import DeviceControl as device


import serial.tools.list_ports
import sys

print(sys.argv)

photon = device("photon", "auto")

if sys.argv[1] == 'serial':
    if sys.argv[2] == 'open':
        try:
            portName = sys.argv[3]
        except IndexError:
            myDevice = device("none", "auto")
            myDevice.openListening()
        else:
            myDevice = device("none", portName)
            myDevice.openListening()
    if sys.argv[2] == 'close':
        try:
            portName = sys.argv[3]
        except IndexError:
            myDevice = device("none", "auto")
            myDevice.closeListening()
        else:
            myDevice = device("none", portName)
            myDevice.closeListening()

if sys.argv[1] == 'dfu':
    if sys.argv[2] == 'open':
        photon.openDFU()
    if sys.argv[2] == 'close':
        photon.closeDFU()
