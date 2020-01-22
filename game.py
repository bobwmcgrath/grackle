import time
import paho.mqtt.publish as publish
import random
import threading
from countdown_timer import CountdownTimer
import RPi.GPIO as GPIO
from segment_driver import SegmentDriver
from usb_serial import UsbSerial

global last_state
last_state=0


class Game:

    @classmethod
    def start(cls, conf):
        gnd = conf['gnd_pin']
        score = 0
        pins = range(conf['last_pin'])
        ser = UsbSerial(conf['serial'])
        display = SegmentDriver(conf['score_pins'])
        game_time = conf['game_time']
        bounce = 18
        active_pin = random.choice(pins)*2
        timer = CountdownTimer(conf['timeConf'])       

        #trd = threading.Thread(target=countdown_timer.start_timer, args=(conf['timeConf'],))
        #trd.daemon = True
        
        GPIO.setup(gnd, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
       
        ser.clear_all()
        ser.clear(active_pin)
	ser.set(6)
	ser.set(active_pin+8)
        print('pin active at: '+str(active_pin) )
        display.showNum(score)
        
        
        update_time = time.time()
        end_time = time.time() + game_time

        #trd.start()
        print('starting cycle in game')
        while end_time > time.time() :
	    global last_state
            if GPIO.input(gnd) == GPIO.HIGH and last_state==0:
                ser.set(active_pin)
		ser.clear(active_pin+8)
                time.sleep(0.25)
                score += 1
                print('score: '+ str(score))
		publish.single("score")
                display.showNum(score)
                active_pin = random.choice(pins)*2
                ser.clear(active_pin)
		ser.set(active_pin+8)
		last_state=1
		#while GPIO.input(gnd) == GPIO.HIGH:
		#	time.sleep(.1)

            if GPIO.input(gnd) == GPIO.LOW and last_state==1:
		last_state=0
		time.sleep(.25)

	    rnd=random.randint(0,100000)
	    if rnd==1:
		ser.set(active_pin)
        	ser.clear(active_pin+8)
		active_pin = random.choice(pins)*2
		ser.clear(active_pin)
                ser.set(active_pin+8)

            if time.time() > update_time:
                update_time += 1
                #update clock here
                timer.update()
        
        
        #hiScor.compare(score)
	publish.single("stop")
        ser.set(active_pin)
        ser.clear(active_pin+8)
        print('end game')
        ser.close()
        #GPIO.cleanup(gnd)

