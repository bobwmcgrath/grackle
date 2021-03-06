import time
import paho.mqtt.publish as publish
import random
from usb_serial import UsbSerial

class Game:

    @classmethod
    def start(cls, conf):
        score = 0                            #                             #         #ADA end
        inputs = [22,23,24,25,26,27,29,30,31,66,68,69,70,71,72,73,74,75,76,77,78,79, 67,28,64,65,48,49,50,51,52,53,54,55,56,57,58,59,60,61,104,106,107,100,101,102,103,108,109,110,111]
        outputs =[6 ,7 ,8 ,9 ,10,11,13,12,15,82,84,85,86,87,88,89,90,91,92,93,94,95, 83,14,80,81,32,33,34,35,36,37,38,39,40,41,42,43,44,45,116,118,119,120,121,122,123,124,125,126,127]
        pins = range(0,conf['last_pin'])
        NUMATO = UsbSerial(conf['serial'])
        active_pin = random.choice(pins)  

        game_time = conf['game_time']      
        end_time = time.time() + game_time

        NUMATO.clear(outputs[active_pin])
        print('starting cycle in game')
        print('pin active at: '+str(active_pin) )
        time.sleep(0.1)
        NUMATO.readGPIO(inputs[active_pin])
        while end_time > time.time() :
                rnd=random.randint(0,250)
                if NUMATO.readGPIO(inputs[active_pin])=="1": 
                        NUMATO.set(outputs[active_pin])
                        time.sleep(0.1)
                        score += 1
                        print('score: '+ str(score))
                        publish.single("score")
                        time.sleep(rnd/100)
                        while NUMATO.readGPIO(inputs[active_pin])=="1" and end_time > time.time():
                                time.sleep(0.1)
                        active_pin = random.choice(pins)
                        NUMATO.clear(outputs[active_pin])

                if rnd==1:
                        NUMATO.set(outputs[active_pin])
                        time.sleep(0.1)
                        active_pin = random.choice(pins)
                        NUMATO.clear(outputs[active_pin])
                        print("random")
                        time.sleep(0.1)

        
        
        publish.single("stop")
        NUMATO.set(outputs[active_pin])
        if score > 29:
                NUMATO.resetSLOW()                     
        NUMATO.reset()
        print('end game')

