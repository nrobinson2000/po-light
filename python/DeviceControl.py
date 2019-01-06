#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import subprocess
import time
from platform import system

class DeviceControl:

    def __init__(self, platform, portName):

        # Try dfu-util -l method first
        try:
            self.usbID = subprocess.check_output(["dfu-util", "--list"]).splitlines()[-1].split()[2][1:-1].decode('UTF-8').lower()
        except IndexError:
            pass
        else:
            if self.usbID == "2b04:d00e":
                self.platform = 'xenon'
                self.dfuAddress = "0x000d4000"
            elif self.usbID == "2b04:d00c":
                self.platform = 'argon'
                self.dfuAddress = "0x000d4000"
            elif self.usbID == "2b04:d00d":
                self.platform = 'boron'
                self.dfuAddress = "0x000d4000"
            elif self.usbID == "2b04:d006":
                self.platform = 'photon'
                self.dfuAddress = "0x080A0000"
            elif self.usbID == "2b04:d008":
                self.platform = 'P1'
                self.dfuAddress = "0x080A0000"
            elif self.usbID == "2b04:d00a":
                self.platform = 'electron'
                self.dfuAddress = "0x08080000"
            elif self.usbID =="1d50:607f":
                self.platform = 'core'
                self.dfuAddress = "0x08005000"
            elif self.usbID == "2b04:d058":
                self.platform = 'duo'
                self.dfuAddress = "0x80C0000"
            else:
                raise Exception("Invalid usbID!")

        if portName == "auto":
            if system() == "Darwin":
                ports = serial.tools.list_ports.grep("/dev/cu.usbmodem")
            elif system() == "Linux":
                ports = serial.tools.list_ports.grep("/dev/ttyACM")
            connectedPorts = []
            for port in ports:
                connectedPorts.append(port)
            if len(connectedPorts) < 1:
                raise Exception("Could not find a port!")
            devicePort = connectedPorts[0]
            self.portName = devicePort.device

            if platform == 'auto':
                self.platform = devicePort.product.split()[0].lower()
        else:
            self.portName = portName

            if platform == 'auto':
                ports = serial.tools.list_ports.grep(self.portName)
                connectedPorts = []
                for port in ports:
                    connectedPorts.append(port)
                if len(connectedPorts) < 1:
                    raise Exception("Could not determine platform!")
                devicePort = connectedPorts[0]
                self.platform = devicePort.product.split()[0].lower()
            else:
                self.platform = platform

        if self.platform == 'xenon':
            self.usbID = "2b04:d00e"
            self.dfuAddress = "0x000d4000"
        elif self.platform == 'argon':
            self.usbID = "2b04:d00c"
            self.dfuAddress = "0x000d4000"
        elif self.platform == 'boron':
            self.usbID = "2b04:d00d"
            self.dfuAddress = "0x000d4000"
        elif self.platform == 'photon':
            self.usbID = "2b04:d006"
            self.dfuAddress = "0x080A0000"
        elif self.platform == 'P1':
            self.usbID = "2b04:d008"
            self.dfuAddress = "0x080A0000"
        elif self.platform == 'electron':
            self.usbID = "2b04:d00a"
            self.dfuAddress = "0x08080000"
        elif self.platform == 'core':
            self.usbID = "1d50:607f"
            self.dfuAddress = "0x08005000"
        elif self.platform == 'duo':
            self.usbID = "2b04:d058"
            self.dfuAddress = "0x80C0000"
        elif self.platform == "none":
            pass
        else:
            print("Invalid platform!")

        self.neutralBaudRate = 9600
        self.dfuBaudRate = 14400
        self.listeningBaudRate = 28800

    def openDFU(self):
        try:
            ser = serial.Serial(self.portName, self.dfuBaudRate)
            ser.close()

        except serial.serialutil.SerialException:
            raise Exception("Could not open that serial port!")

        else:
            try:
                ser = serial.Serial(self.portName, self.neutralBaudRate)
                ser.close()

            except serial.serialutil.SerialException:
                #raise Exception("Invalid Serial Port!")
                pass

    def closeDFU(self):
        try:
            subprocess.run(["dfu-util", "-d", self.usbID, "-a", "0", "-i", "0", "-s", self.dfuAddress + ":leave", "-D", "/dev/null"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except AttributeError:
            raise Exception("Could not find a device in DFU!")

    def openListening(self):
        try:
            ser = serial.Serial(self.portName, self.listeningBaudRate)
            ser.close()

        except serial.serialutil.SerialException:
            raise Exception("Could not open that serial port!")

        else:
            try:
                ser = serial.Serial(self.portName, self.neutralBaudRate)
                ser.close()

            except serial.serialutil.SerialException:
                pass

    def closeListening(self):
        try:
            self.openDFU()
            time.sleep(1)
            self.closeDFU()
        except Exception as error:
            print(repr(error))

    def openSafe(self):
        try:
            self.openListening()
        except Exception as error:
            print(repr(error))
        else:
            ser = serial.Serial(self.portName, self.neutralBaudRate)
            ser.write(b'L')
            ser.close()
            time.sleep(10)
            ser = serial.Serial(self.portName, self.neutralBaudRate)
            ser.write(b'x')
            ser.close()

        # try:
        #     ser = serial.Serial(self.portName, self.neutralBaudRate)
        #     ser.write(b'L')
        #     time.sleep(4)
        #     ser = serial.Serial(self.portName, self.neutralBaudRate)
        #     ser.write(b'x')
        #     ser.close()
        #
        # except serial.serialutil.SerialException:
        #     pass
