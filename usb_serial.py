import serial
import time



class UsbSerial:

    def __init__(self, serial_conf):
        self.ser = serial.Serial(serial_conf['port'], serial_conf['baud'])
        time.sleep(1)

    def set(self, pin):
        self.ser.write("gpio set "   + ("000" + str(pin))[-3:] + "r")
        time.sleep(.01)
        x=self.ser.readline()

    def clear(self, pin):
        self.ser.write("gpio clear " + ("000" + str(pin))[-3:] + "r")
        time.sleep(.01)
        x=self.ser.readline()

    def readGPIO(self, pin):
        self.ser.flush()
        self.ser.write("gpio read " + ("000" + str(pin))[-3:] + "r")
        time.sleep(.01)
        x=self.ser.readline()
        x=self.ser.read(1)
        x=self.ser.read(1)
        y=self.ser.read(1)
        #time.sleep(.1)
        self.ser.flush()
        return x

    def reset(self): 
        inputs = []+range(16,32)+range(48,64)+range(64,80)+range(96,112)
        outputs = []+range(0,16)+range(32,48)+range(80,96)+range(112,128)
        pins = range(0,len(outputs))
        for i in outputs:
            #self.clear(i)
            #time.sleep(.5)
            self.set(i)
            time.sleep(.01)
            #print(i)
            time.sleep(.01)
            
        for i in inputs:
            self.readGPIO(i)
            time.sleep(.01)
    def test(self):
        inputs =  [20,21,22,23,24,25,26,27,28,29,30,31]+[48,49,50,51,52,53,54,55,56,57,58,59,60,61]+[64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79]+[104,106,107,100,101,102,103,108,109,110,111]#
        outputs = [4 ,5 ,6 ,7 ,8 ,9 ,10,11,14,13,12,15]+[32,33,34,35,36,37,38,39,40,41,42,43,44,45]+[80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]+[116,118,119,120,121,122,123,124,125,126,127]#
        pins = range(0,len(outputs))

        for i in pins:
            time.sleep(.01)
            self.clear(outputs[i])
            print(outputs[i])
            while self.readGPIO(inputs[i]) is not "1":
                #print self.readGPIO(inputs[i])
                time.sleep(.1)
            self.set(outputs[i])
            while self.readGPIO(inputs[i]) is "1":
                time.sleep(.1)
            





    def close(self):
        self.ser.close()


