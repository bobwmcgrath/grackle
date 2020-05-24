import time
import paho.mqtt.publish as publish
import random
from usb_serial import UsbSerial

global last_state
last_state=0 #for buttons


class Game:

    @classmethod
    def start(cls, conf):
        score = 0
        aList=[80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]
#,32,33,34,35,36,37,38,39,40,41,42,43,44,45,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,118,119,120,121,122,123,125,126]
        pins = range(80,95)
        NUMATO = UsbSerial(conf['serial'])
        bounce = 18
        active_pin = random.choice(pins)  

        game_time = conf['game_time']      
        end_time = time.time() + game_time

        NUMATO.set(active_pin)
        print('starting cycle in game')
        print('pin active at: '+str(active_pin) )
        print NUMATO.readGPIO(active_pin)
        while end_time > time.time() :
                print NUMATO.readGPIO(active_pin)
                global last_state
                if NUMATO.readGPIO(active_pin+16)=="1": #and last_state==0:
                #if 1 == 1:
                        NUMATO.clear(active_pin)
                        time.sleep(0.1)
                        score += 1
                        print('score: '+ str(score))
                        publish.single("score")
                        active_pin = random.choice(pins)
                        NUMATO.set(active_pin)
                        #last_state=1
                        print('pin active at: '+str(active_pin) )
                        while NUMATO.readGPIO(active_pin+16)=="1":
                                time.sleep(0.1)

                #if GPIO.input(gnd) == GPIO.LOW and last_state==1:
                 #       last_state=0
                  #      time.sleep(.25)

                #rnd=2
                rnd=random.randint(0,100000)
                if rnd==1:
                        NUMATO.clear(active_pin)
                        active_pin = random.choice(pins)
                        NUMATO.set(active_pin)
                        print("random")

        
        
        publish.single("stop")
        NUMATO.clear(active_pin)
        NUMATO.reset()
        print('end game')
        NUMATO.close()

