#wack a grackle root file
#by Shawn and Bob for Bridgewater Studios
#this files calls game.py for most of the game mechanics
#the pi communicates with 3 arduinos over MQTT to run 2 digit 7 segment displays
import time
import paho.mqtt.publish as publish
from usb_serial import UsbSerial
from game import Game
import serial


class Grackle:

    @classmethod
    def run(cls):

        is_running = True

        run_time = 30
        max_pin = 51
        ada_pins = 25
        start = 21
        ada_start = 20
        ser_conf = {"port": "/dev/ttyACM0", "baud": 115200}
        NUMATO=UsbSerial(ser_conf)
        gameDict = {'serial': ser_conf, 'game_time': run_time}
        NUMATO.reset()
        NUMATO.clear(4)
        NUMATO.clear(5)

        while is_running:
                if NUMATO.readGPIO(start)=="1":
                        NUMATO.set(4)
                        NUMATO.set(5)
                        print("go")
                        gameDict['last_pin'] = max_pin
                        publish.single("start")
                        Game.start(gameDict)
                        NUMATO.clear(4)
                        NUMATO.clear(5) 

                if NUMATO.readGPIO(ada_start)=="1":
                        NUMATO.set(4)
                        NUMATO.set(5)
                        print("ada button input activated")
                        gameDict['last_pin'] = ada_pins
                        publish.single("start")
                        Game.start(gameDict)
                        NUMATO.clear(4)
                        NUMATO.clear(5) 
Grackle.run()
