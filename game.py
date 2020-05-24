import time
import paho.mqtt.publish as publish
import random
from usb_serial import UsbSerial

global last_state
last_state=0


class Game:

    @classmethod
    def start(cls, conf):
        gnd = conf['gnd_pin']
        score = 0
        aList=[80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]
#,32,33,34,35,36,37,38,39,40,41,42,43,44,45,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,118,119,120,121,122,123,125,126]
        pins = range(80,95)
        ser = UsbSerial(conf['serial'])
        display = SegmentDriver(conf['score_pins'])
        game_time = conf['game_time']
        bounce = 18
        active_pin = random.choice(pins)
	##active_pin = 6
        timer = CountdownTimer(conf['timeConf'])       

        #trd = threading.Thread(target=countdown_timer.start_timer, args=(conf['timeConf'],))
        #trd.daemon = True
        
        GPIO.setup(gnd, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
       
        #ser.clear_all()
        ser.set(active_pin)
	#ser.clear(6)
        ser.set(active_pin+16)
        print('pin active at: '+str(active_pin) )
        display.showNum(score)
        
        
        update_time = time.time()
        end_time = time.time() + game_time

        #trd.start()
        print('starting cycle in game')
        while end_time > time.time() :
                global last_state
                if GPIO.input(gnd) == GPIO.HIGH and last_state==0:
                #if 1 == 1:
                        ser.clear(active_pin)
                        ser.clear(active_pin+16)
                        time.sleep(0.25)
                        score += 1
                        print('score: '+ str(score))
                        publish.single("score")
                        display.showNum(score)
                        active_pin = random.choice(pins)
                        #active_pin +=1
                        ser.set(active_pin)
                        ser.set(active_pin+16)
                        #time.sleep(1)
                        last_state=1
                        print('pin active at: '+str(active_pin) )
                        #while GPIO.input(gnd) == GPIO.HIGH:
                        # #	time.sleep(.1)

                if GPIO.input(gnd) == GPIO.LOW and last_state==1:
                        last_state=0
                        time.sleep(.25)

                rnd=2
                #rnd=random.randint(0,100000)
                if rnd==1:
                        ser.clear(active_pin)
                        ser.clear(active_pin+16)
                        ###active_pin = random.choice(pins)*2
                        active_pin +=1
                        ser.set(active_pin)
                        ser.set(active_pin+16)

                if time.time() > update_time:
                        update_time += 1
                        #update clock here
                        timer.update()
        
        
        #hiScor.compare(score)
        publish.single("stop")
        ser.set(active_pin)
        ser.clear(active_pin)
        ser.set(active_pin+16)
        ser.clear(active_pin+16)
        #ser.clear_all()
        print('end game')
        ser.close()
        #GPIO.cleanup(gnd)

