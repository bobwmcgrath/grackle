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
        self.ser.flush()
        self.ser.write("gpio read " + ("000" + str(pin))[-3:] + "r")
        time.sleep(.1)
        x=self.ser.readline()
        x=self.ser.read(1)
        x=self.ser.read(1)
        y=self.ser.read(1)
        #time.sleep(.1)
        self.ser.flush()
        return x

    def reset(self): 
        inputs = range(16,32)+range(48,64)+range(64,80)+range(96,112)
        outputs = range(0,16)+range(32,48)+range(80,96)+range(112,128)
        pins = len(outputs)
        for i in outputs:
            self.ser.write("gpio set " + ("000" + str(i))[-3:] + "r")
            #print(i)
        for i in inputs:
            self.ser.flush()
            self.ser.write("gpio read " + ("000" + str(i))[-3:] + "r")
            time.sleep(.1)
            x=self.ser.readline()
            x=self.ser.read(1)
            x=self.ser.read(1)
            y=self.ser.read(1)
            #time.sleep(.1)
            self.ser.flush()

    def close(self):
        self.ser.close()




