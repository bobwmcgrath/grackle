import RPi.GPIO as GPIO
import time
from time import sleep



class SegmentDriver: 

    def __init__(self, pins):
        #GPIO.setmode(GPIO.BOARD)
        self.clk = pins['clk']
        self.lat = pins['lat']
        self.dat = pins['dat']

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.clk, GPIO.OUT, initial=0)
        GPIO.setup(self.lat, GPIO.OUT, initial=0)
        GPIO.setup(self.dat, GPIO.OUT, initial=0)

        #GPIO.output(segClk, GPIO.LOW)
        #GPIO.output(segLat, GPIO.LOW)
        #GPIO.output(segDat, GPIO.LOW)

        self.num = 0

    def showNumber(self, val):
        self.num = abs(val)
        x = 0
        while(x<2):
            remainder = self.num % 10
            self.postNum(remainder)
            self.num /= 10
            x += 1
        GPIO.output(self.lat, GPIO.LOW)
        GPIO.output(self.lat, GPIO.HIGH)


    def showNum(self, val):
        self.num = abs(val)
        for i in reversed(str(self.num)):
            self.postNum(int(i))
        GPIO.output(self.lat, GPIO.LOW)
        GPIO.output(self.lat, GPIO.HIGH)


    def postNum(self, num):
        segments = bytes()
        a=1<<0
        b=1<<6
        c=1<<5
        d=1<<4
        e=1<<3
        f=1<<1
        g=1<<2
        dp=1<<7

        if   self.num == 1: segments = b | c                
        elif self.num == 2: segments = a | b | d | e | g
        elif self.num == 3: segments = a | b | c | d | g
        elif self.num == 4: segments = b | c | f | g
        elif self.num == 5: segments = a | c | d | f | g
        elif self.num == 6: segments = a | c | d | e | f | g
        elif self.num == 7: segments = a | b | c 
        elif self.num == 8: segments = a | b | c | d | e | f | g
        elif self.num == 9: segments = a | b | c | d | f | g
        elif self.num == 0: segments = a | b | c | d | e | f    
        elif self.num == ' ': segments = 0
        elif self.num == 'c': segments = d | e | g
        elif self.num == '-': segments = g
        else : segments = False
    
        y=0
        while(y<8):
            GPIO.output(self.clk, GPIO.LOW)
            GPIO.output(self.dat, segments & (1<<(7-y)))
            GPIO.output(self.clk, GPIO.HIGH)
            y += 1
    
