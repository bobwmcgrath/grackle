import serial
import time



class UsbSerial:

    def __init__(self, serial_conf):
        self.ser = serial.Serial(serial_conf['port'], serial_conf['baud'])

    def set(self, pin):
        self.ser.write("gpio set "   + ("000" + str(pin))[-3:] + "r")

    def clear(self, pin):
        self.ser.write("gpio clear " + ("000" + str(pin))[-3:] + "r")

    def readGPIO(self, pin):
        self.ser.write("gpio read " + ("000" + str(pin))[-3:] + "r")
        time.sleep(.1)
        return self.ser.read(1)

    def clear_all(self): 
        for i in range (0,128):
            self.ser.write("gpio set "   + ("000" + str(i))[-3:] + "r")
            print(i)
            
    def close(self):
        self.ser.close()

