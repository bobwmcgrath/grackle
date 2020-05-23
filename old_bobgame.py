# bob game
import RPi.GPIO as GPIO
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
common_gnd=26
GPIO.setup(common_gnd, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
from time import sleep
import serial
input_value = GPIO.input(common_gnd)

slp=.5

ser = serial.Serial('/dev/ttyACM0')  # open serial port
sleep(slp)

ser.write(b'gpio clear 011r')
sleep(slp)
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
#ser.write(b'gpio clear 010r')
#sleep(slp)
#ser.write(b'gpio set 010r')
#sleep(slp)

#GPIO.cleanup()


ser.close()
exit()

