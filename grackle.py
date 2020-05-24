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

        run_time = 60
        max_pin = 50
        ada_pins = 25
        start = 4
        ada_start = 20

        ser_conf = {"port": "/dev/serial/by-id/usb-Numato_Systems_PVT_LTD_Numato_Lab_128_Channel_USB_GPIO_Module_NL12800000A19004-if00", "baud": 9600}
        NUMATO=UsbSerial(ser_conf)
        gameDict = {'serial': ser_conf, 'game_time': run_time}


        while is_running:
                print("poop")
                print NUMATO.readGPIO(start)
                if NUMATO.readGPIO(start)=="1":
                        print("go")
                        gameDict['last_pin'] = max_pin
                        publish.single("start")
                        Game.start(gameDict)

                if NUMATO.readGPIO(ada_start)=="1":
                        print("ada button input activated")
                        gameDict['last_pin'] = ada_pins
                        publish.single("start")
                        Game.start(gameDict)



Grackle.run()
