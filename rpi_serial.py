#!/usr/bin/env python3

import sys
import serial
import board
import busio
from adafruit_ht16k33 import segments, animations
from _thread import *
from time import *

i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg14x4(i2c, address=(0x70,0x72))
LED_TIMEOUT=0
DISPLAY_HIDDEN=0
HIDE_TIME=30

def display_init():
    global display
    print("initing display")
    display1 = segments.Seg14x4(i2c, address=0x70)
    display2 = segments.Seg14x4(i2c, address=0x72)
    a1=animations.Animation(display1)
    a2=animations.Animation(display2)
    start_new_thread(a1.enclosed_spinners, (0.05,10))
    start_new_thread(a2.enclosed_spinners, (0.05,10))
    sleep(2.5)
    del a1
    del a2
    del display1
    del display2
    display.set_digit_raw(6, 0b0100000000000000)
    display._put('G',4)
    display._put('0',5)
    display._put('0',0)
    display._put('0',1)
    display._put('0',2)
    display._put('0',3)
    display._put('0',7)
    display.blink_rate=0
    display.show()

display_init()

def set_rpm(i):
    global display
    s="{:>5}".format(str(i))
    il=[7,0,1,2,3]
    for i in range(5):
        if s[i] != " ":
            display._put(s[i], il[i])
            display.show()
        else:
            display._put('0', il[i])
            display.show()

def set_gear(i):
    global display
    display._put(str(i),5)
    display.show()

def display_shut():
    global display
    display1 = segments.Seg14x4(i2c, address=0x70)
    display2 = segments.Seg14x4(i2c, address=0x72)

    a1=animations.Animation(display1)
    a2=animations.Animation(display2)
    start_new_thread(a1.spinners, (0.05,5))
    start_new_thread(a2.spinners, (0.05,5))
    del a1
    del a2
    del display1
    del display2
    sleep(1)
    display.set_digit_raw(0, 0b00000000000000000)
    display.set_digit_raw(1, 0b00000000000000000)
    display.set_digit_raw(2, 0b00000000000000000)
    display.set_digit_raw(3, 0b00000000000000000)
    display.set_digit_raw(4, 0b00000000000000000)
    display.set_digit_raw(5, 0b00000000000000000)
    display.set_digit_raw(6, 0b00000000000000000)
    display.set_digit_raw(7, 0b00000000000000000)

def timeout():
    global LED_TIMEOUT
    global DISPLAY_HIDDEN
    global HIDE_TIME
    global display
    print("timeout started")
    i=0
    while i<HIDE_TIME:
        sleep(1)
        if LED_TIMEOUT: pass
        else: return
        i+=1
    DISPLAY_HIDDEN=1
    display_shut()
    print("shutting off display")

o=" "
ser = serial.Serial('/dev/ttyGS0', 9600, timeout=2)
while True:
    print("reading")
    while o != "":
        try:
            o = ser.readline().decode('utf-8').strip().split(',')
            if len(o) > 1: 
                if LED_TIMEOUT: 
                    LED_TIMEOUT=0
                    DISPLAY_HIDDEN=0
                    display_init()
                set_rpm(o[0])    
                set_gear(o[1])
                if o[2]=='1': 
                    print("setting blink")
                    display.blink_rate=1
                    display.show()
                else: display.blink_rate=0
            elif o==['']:
                print("no data")
                if not DISPLAY_HIDDEN:
                    set_rpm(0)
                    set_gear(0)
                if not LED_TIMEOUT: start_new_thread(timeout,())
                LED_TIMEOUT=1

        except Exception as e:
            print(e)
            print("retrying connection")
            ser.close()
            ser.open()
    o = " " 

