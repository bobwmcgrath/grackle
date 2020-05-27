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
            self.ser.write("gpio set " + ("000" + str(i))[-3:] + "r")
            time.sleep(.01)
            x=self.ser.readline()
            #print(i)
            time.sleep(.01)
        for i in inputs:
            self.ser.flush()
            self.ser.write("gpio read " + ("000" + str(i))[-3:] + "r")
            time.sleep(.01)
            x=self.ser.readline()
            x=self.ser.read(1)
            x=self.ser.read(1)
            y=self.ser.read(1)
            #time.sleep(.1)
            self.ser.flush()
            time.sleep(.01)
    def test(self):
        inputs = []+range(16,32)+range(48,64)+range(64,80)+range(96,112)
        outputs = []+range(0,16)+range(32,48)+range(80,96)+range(112,128)
        pins = range(0,len(outputs))

        for i in pins:
            self.clear(outputs[i])
            print(outputs[i])
            while self.readGPIO(inputs[i]) is not "1":
                #print self.readGPIO(inputs[i])
                time.sleep(.1)





    def close(self):
        self.ser.close()

ser_conf = {"port": "/dev/ttyACM0", "baud": 115200}
NUMATO=UsbSerial(ser_conf)
NUMATO.reset()
NUMATO.test()
#print NUMATO.readGPIO(17)
#
#
#inputs = []+range(16,32)+range(48,64)+range(64,80)+range(96,112)
#len = len(inputs)

#print (inputs)
