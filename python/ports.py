#!/usr/bin/env python3

import serial.tools.list_ports

ports = serial.tools.list_ports.grep("/dev/cu.usbmodem")
portList = []
for port in ports:
    portList.append(port)

print(portList[0])
