import time
import paho.mqtt.publish as publish
#import threading
import RPi.GPIO as GPIO
from usb_serial import UsbSerial
from game import Game
#import countdown_timer




class Grackle:

    @classmethod
    def run(cls):
        is_running = True

        shutdownp = 8
        start_pin = 32
        ada_start = 36
        comm_gnd = 37
        run_time = 30
        max_pin = 4
        ada_pins = 2

        ser_conf = {"port": "/dev/ttyACM0", "baud": 19200}

        timerPins = {'clk': 13, 'lat': 15, 'dat':11}
        scorePins = {'clk': 16, 'lat': 18, 'dat':22}
        hiScrPins = {'clk': 29, 'lat': 31, 'dat':33}


        timeConf = {'pins': timerPins, 'time': run_time}
        gameDict = {'gnd_pin': comm_gnd, 'serial': ser_conf, 'score_pins': scorePins, 'game_time': run_time, 'timeConf': timeConf}

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(start_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(ada_start, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(shutdownp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        while is_running:
            if GPIO.input(start_pin) == GPIO.HIGH:              
                gameDict['last_pin'] = max_pin
		publish.single("start")
                Game.start(gameDict)

            if GPIO.input(ada_start) == GPIO.HIGH:
                print("ada button input activated")
                gameDict['last_pin'] = ada_pins
		publish.single("start")
                Game.start(gameDict)

            if GPIO.input(shutdownp) == GPIO.HIGH:
                is_running = False
                print("shutting down")
                GPIO.cleanup()



Grackle.run()
