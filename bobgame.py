# bob game
import RPi.GPIO as GPIO
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
common_gnd=26
GPIO.setup(common_gnd, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
from time import sleep
import serial
input_value = GPIO.input(common_gnd)

slp=.1

ser = serial.Serial('/dev/ttyACM0')  # open serial port
sleep(slp)

x='gpio clear 000r'

ser.write(x)
ser.write('gpio set 008r')
while input_value==0:
	input_value = GPIO.input(common_gnd)
	sleep(slp)
ser.write(b'gpio set 000r')
ser.write(b'gpio clear 008r')
sleep(slp)
ser.write(b'gpio set 010r')
ser.write(b'gpio clear 002r')
input_value = GPIO.input(common_gnd)
while input_value==0:
        input_value = GPIO.input(common_gnd)
        sleep(slp)
ser.write(b'gpio clear 010r')
ser.write(b'gpio set 002r')
sleep(slp)
ser.write(b'gpio set 012r')
ser.write(b'gpio clear 004r')
sleep(slp)
ser.write(b'gpio clear 012r')
ser.write(b'gpio set 004r')
sleep(slp)
ser.write(b'gpio set 014r')
ser.write(b'gpio clear 006r')
sleep(slp)
ser.write(b'gpio clear 014r')
ser.write(b'gpio set 006r')
sleep(slp)

#GPIO.cleanup()


ser.close()
exit()

