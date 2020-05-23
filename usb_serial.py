import serial



class UsbSerial:

    def __init__(self, serial_conf):
        self.ser = serial.Serial(serial_conf['port'], serial_conf['baud'])

    def set(self, pin):
        self.ser.write("gpio set "   + ("000" + str(pin))[-3:] + "r")

    def clear(self, pin):
        self.ser.write("gpio clear " + ("000" + str(pin))[-3:] + "r")

    def read(self, pin):
        self.ser.write("gpio read " + ("000" + str(pin))[-3:] + "r")

    def clear_all(self): 
        #self.ser.write("gpio readall 00000000000000000000000011111111r")
	#self.ser.write("gpio readall 11111111111111111111111111111111r")
	self.ser.write("gpio setall r")
    def close(self):
        self.ser.close()

