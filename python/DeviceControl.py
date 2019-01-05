#!/usr/bin/env python3

import serial
import subprocess
import time

class DeviceControl:

    def __init__(self, platform, portName):
        self.platform = platform

        if platform is "xenon":
            self.usbID = "2b04:d00e"
            self.dfuAddress = "0x000d4000"
        elif platform is "argon":
            self.usbID = "2b04:d00c"
            self.dfuAddress = "0x000d4000"
        elif platform is "boron":
            self.usbID = "2b04:d00d"
            self.dfuAddress = "0x000d4000"
        elif platform is "photon":
            self.usbID = "2b04:d006"
            self.dfuAddress = "0x080A0000"
        elif platform is "P1":
            self.usbID = "2b04:d008"
            self.dfuAddress = "0x080A0000"
        elif platform is "electron":
            self.usbID = "2b04:d00a"
            self.dfuAddress = "0x08080000"
        elif platform is "core":
            self.usbID = "1d50:607f"
            self.dfuAddress = "0x08005000"
        elif platform is "duo":
            self.usbID = "2b04:d058"
            self.dfuAddress = "0x80C0000"
        elif platform is "none":
            pass
        else:
            print("Invalid platform!")

        if portName == "auto":
            ports = serial.tools.list_ports.grep("/dev/cu.usbmodem")
            connectedPorts = []
            for port in ports:
                connectedPorts.append(port.device)
            if len(connectedPorts) < 1:
                print("Could not find a port!")
                quit()
            self.portName = connectedPorts[0]
        else:
            self.portName = portName


        self.neutralBaudRate = 9600
        self.dfuBaudRate = 14400
        self.listeningBaudRate = 28800

    def openDFU(self):
        try:
            ser = serial.Serial(self.portName, self.dfuBaudRate)
            ser.close()

        except serial.serialutil.SerialException:
            print("Invalid Serial Port!")
            quit()
            
        else:
            try:
                ser = serial.Serial(self.portName, self.neutralBaudRate)
                ser.close()

            except serial.serialutil.SerialException:
                pass

    def closeDFU(self):
        subprocess.run(["dfu-util", "-d", self.usbID, "-a", "0", "-i", "0", "-s", self.dfuAddress + ":leave", "-D", "/dev/null"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def openListening(self):
        try:
            ser = serial.Serial(self.portName, self.listeningBaudRate)
            ser.close()

        except serial.serialutil.SerialException:
            print("Invalid Serial Port!")
            quit()

        else:
            try:
                ser = serial.Serial(self.portName, self.neutralBaudRate)
                ser.close()

            except serial.serialutil.SerialException:
                pass

    def closeListening(self):
        self.openDFU()
        time.sleep(1)
        self.closeDFU()
