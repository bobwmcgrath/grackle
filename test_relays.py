# bob game
import RPi.GPIO as GPIO
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
common_gnd=26
GPIO.setup(common_gnd, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
from time import sleep
import serial
input_value = GPIO.input(common_gnd)

slp=2

ser = serial.Serial('/dev/ttyACM0')  # open serial port
sleep(slp)
pin=input()
#pin=str(pin)
ser.write("gpio set " + ("000" + str(pin))[-3:] + "r")
sleep(slp)
ser.write("gpio read " + ("000" + str(pin))[-3:] + "r")
#ser.write("gpio read " + ("000" + str(pin+16))[-3:] + "r")
#s = ser.read(10)        # read up to ten bytes (timeout)
#print(s)
#sleep(slp)
#ser.write(b'gpio clear 010r')
#sleep(slp)
#ser.write(b'gpio set 010r')
#sleep(slp)
#ser.write(b'gpio clear 010r')
#sleep(slp)
#ser.write(b'gpio set 010r')
#sleep(slp)
#ser.write(b'gpio clear 010r')
#sleep(slp)
#ser.write(b'gpio set 010r')
#sleep(slp)

#GPIO.cleanup()


ser.close()
exit()

