#wack a grackle root file
#by Shawn and Bob for Bridgewater Studios
#this files calls game.py for most of the game mechanics
#the pi communicates with 3 arduinos over MQTT to run 2 digit 7 segment displays
import time
import paho.mqtt.publish as publish
#import threading
import RPi.GPIO as GPIO
from usb_serial import UsbSerial
from game import Game
import serial
#import countdown_timer

ser = serial.Serial('/dev/ttyACM0')  # open serial port
time.sleep(2)



class Grackle:

    @classmethod
    def run(cls):
        is_running = True

        shutdownp = 8
        start_pin = 33
	start_button=0
	ada_start_button=0
        ada_start = 36
        comm_gnd = 32
        run_time = 600
        max_pin = 128
        ada_pins = 2

        ser_conf = {"port": "/dev/ttyACM0", "baud": 19200}

        timerPins = {'clk': 13, 'lat': 15, 'dat':11}
        scorePins = {'clk': 16, 'lat': 18, 'dat':22}
        hiScrPins = {'clk': 29, 'lat': 31, 'dat':37}


        timeConf = {'pins': timerPins, 'time': run_time}
        gameDict = {'gnd_pin': comm_gnd, 'serial': ser_conf, 'score_pins': scorePins, 'game_time': run_time, 'timeConf': timeConf}

        GPIO.setmode(GPIO.BOARD)
	GPIO.setup(comm_gnd, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(start_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(ada_start, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(shutdownp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	time.sleep(1)

        while is_running:
	    ser.write("gpio set " + ("004r"))
	    ser.write("gpio set " + ("020r"))
	    time.sleep(.5)
	    if 1==1:
	    #if GPIO.input(comm_gnd) == GPIO.HIGH:
		ser.write("gpio read " + ("004r")) 
		ser.write("gpio read " + ("005r"))
                ser.write("gpio read " + ("020r"))
                gameDict['last_pin'] = max_pin
		publish.single("start")
                Game.start(gameDict)
		#is_running= False

	    #ser.write("gpio read " + ("004r"))
	    ser.write("gpio read " + ("020r"))
	    ser.write("gpio set " + ("005r"))
	    ser.write("gpio set " + ("021r"))
	    time.sleep(.5)
            if GPIO.input(comm_gnd) == GPIO.HIGH:
		ser.write("gpio read " + ("004r"))
		ser.write("gpio read " + ("005r"))
                ser.write("gpio read " + ("021r"))
                print("ada button input activated")
                gameDict['last_pin'] = ada_pins
		publish.single("start")
                Game.start(gameDict)
		#is_running=False

	    #ser.write("gpio read " + ("005r"))
	    ser.write("gpio read " + ("021r"))
            if GPIO.input(shutdownp) == GPIO.HIGH:
                is_running = False
                print("shutting down")
                GPIO.cleanup()



Grackle.run()
