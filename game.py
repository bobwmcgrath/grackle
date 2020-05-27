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
        inputs = []+range(16,32)+range(48,64)+range(64,80)+range(96,112)
        outputs = []+range(0,16)+range(32,48)+range(80,96)+range(112,128)
        pins = range(0,len(outputs))
        NUMATO = UsbSerial(conf['serial'])
        active_pin = random.choice(pins)  

        game_time = conf['game_time']      
        end_time = time.time() + game_time

        NUMATO.clear(outputs[active_pin])
        print('starting cycle in game')
        print('pin active at: '+str(active_pin) )
        while end_time > time.time() :
                #print NUMATO.readGPIO(inputs[active_pin])
                global last_state
                if NUMATO.readGPIO(inputs[active_pin])=="1": #and last_state==0:
                #if 1 == 1:
                        NUMATO.set(outputs[active_pin])
                        time.sleep(0.1)
                        score += 1
                        print('score: '+ str(score))
                        publish.single("score")
                        active_pin = random.choice(pins)
                        NUMATO.clear(outputs[active_pin])
                        #last_state=1
                        print('pin active at: '+str(active_pin) )
                        while NUMATO.readGPIO(inputs[active_pin])=="1" and end_time > time.time():
                                time.sleep(0.1)

                #if GPIO.input(gnd) == GPIO.LOW and last_state==1:
                 #       last_state=0
                  #      time.sleep(.25)

                #rnd=2
                rnd=random.randint(0,10000)
                if rnd==1:
                        NUMATO.setoutputs([active_pin])
                        active_pin = random.choice(pins)
                        NUMATO.clear(outputs[active_pin])
                        print("random")

        
        
        publish.single("stop")
        NUMATO.set(outputs[active_pin])
        NUMATO.reset()
        print('end game')
        NUMATO.close()

