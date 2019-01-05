#!/usr/bin/env python3

# Load completion script
# complete -F _po-util ./test.py

from DeviceControl import DeviceControl as device
import sys

print(sys.argv)

if sys.argv[1] == 'serial':
    if sys.argv[2] == 'open':
        try:
            portName = sys.argv[4]
        except IndexError:
            try:
                myDevice = device("auto", "auto")
                myDevice.openListening()
            except Exception as error:
                print(repr(error))
        else:
            try:
                myDevice = device("none", portName)
                myDevice.openListening()
            except Exception as error:
                print(repr(error))
    if sys.argv[2] == 'close':
        try:
            portName = sys.argv[4]
        except IndexError:
            try:
                myDevice = device("auto", "auto")
                myDevice.closeListening()
            except Exception as error:
                print(repr(error))
        else:
            try:
                myDevice = device("auto", portName)
                myDevice.closeListening()
            except Exception as error:
                print(repr(error))

if sys.argv[1] == 'dfu':
    if sys.argv[2] == 'open':
        try:
            portName = sys.argv[4]
        except IndexError:
            try:
                myDevice = device("auto", "auto")
                myDevice.openDFU()
            except Exception as error:
                print(repr(error))
        else:
            try:
                myDevice = device("none", portName)
                myDevice.openDFU()
            except Exception as error:
                print(repr(error))
    if sys.argv[2] == 'close':
        try:
            myDevice = device("none", "none")
            myDevice.closeDFU()
        except Exception as error:
            print(repr(error))

if sys.argv[1] == 'safe':
    if sys.argv[2] == 'open':
        try:
            portName = sys.argv[4]
        except IndexError:
            try:
                myDevice = device("auto", "auto")
                myDevice.openSafe()
            except Exception as error:
                print(repr(error))
        else:
            try:
                myDevice = device("none", portName)
                myDevice.openSafe()
            except Exception as error:
                print(repr(error))
