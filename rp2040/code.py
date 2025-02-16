import sys
import usb_cdc
import board
import busio
import time
from lib.adafruit_ht16k33 import segments, animations

# DISPLAY PARAMETERS
REFRESH_RATE    = 1/100 # 100hz
DISPLAY_TIMEOUT = (1/REFRESH_RATE) * 20 # 20sec
DISPLAY_STATE   = 1  # on/off
DISPLAY_BLINK   = 0  # on/off


# HARDWARE DEFINITIONS
BOTTOM_LEFT     = 0x70
BOTTOM_RIGHT    = 0x71
TOP_LEFT        = 0x72
TOP_RIGHT       = 0x74
I2C_SCL_PIN     = board.GP27
I2C_SDA_PIN     = board.GP26

# HARDWARE ABSTRACTIONS
i2c = busio.I2C(I2C_SCL_PIN, I2C_SDA_PIN)
display1 = segments.Seg14x4(i2c, address=(BOTTOM_RIGHT, BOTTOM_LEFT))
display2 = segments.Seg14x4(i2c, address=(TOP_RIGHT, TOP_LEFT))
mindisp1 = segments.Seg14x4(i2c, address=BOTTOM_LEFT)
mindisp2 = segments.Seg14x4(i2c, address=BOTTOM_RIGHT)
mindisp3 = segments.Seg14x4(i2c, address=TOP_LEFT)
mindisp4 = segments.Seg14x4(i2c, address=TOP_RIGHT)
displays=[display1,display2]
mindisps=[mindisp1,mindisp2,mindisp3,mindisp4]

def init_displays():
    for mindisp in mindisps:
        anim=animations.Animation(mindisp)
        anim.chase_forward_and_reverse(delay=0.005,cycles=1)
    display1._put("G", 0)
    display1._put("0", 1)
    display1.set_digit_raw(2, 0b0100000000000000)
    display1._put("0", 3)
    display1._put("0", 4)
    display1._put("0", 5)
    display1._put("0", 6)
    display1._put("0", 7)
    display1.blink_rate = 0
    display1.show()

    display2._put("0",0)
    display2._put("0",1)
    display2._put("0",2)
    display2._put("k",3)
    display2._put("0",4)
    display2._put("0",5)
    display2._put("0",6)
    display2._put("m",7)
    display2.blink_rate = 0
    display2.show()

def set_rpm(num):
    s = f"{num:05d}"[:5]
    for i,v in enumerate(range(3,8)):
        display1._put(s[i],v)
        display1.show()


def set_gear(num):
    display1._put(str(num)[:1], 1)
    display1.show()


def set_kph(num):
    s = f"{num:03d}"[:3]
    for i,v in enumerate(range(0,3)):
        display2._put(s[i],v)
        display2.show()

def set_mph(num):
    s = f"{num:03d}"[:3]
    for i,v in enumerate(range(4,7)):
        display2._put(s[i],v)
        display2.show()


def set_blink(state):
    if state==1:
        display1.blink_rate = 1
        display1.show()
    else:
        display1.blink_rate = 0
        display1.show()


def timeout_displays():
    for mindisp in mindisps[::-1]:
        anim=animations.Animation(mindisp)
        anim.chase_forward_and_reverse(delay=0.005, cycles=1)
    #for display in displays:
    #    for i in range(0,8):
    #        display.set_digit_raw(i, 0b00000000000000000)
    #        display.show()


def display_test():
    init_displays()
    time.sleep(0.5)
    set_rpm(13222)
    time.sleep(0.5)
    set_gear(2)
    time.sleep(0.5)
    set_kph(12)
    time.sleep(0.5)
    set_mph(41111)
    time.sleep(0.5)
    timeout_displays()
    print("done!")
    

def serial_loop():
    global DISPLAY_STATE
    serial  = usb_cdc.console
    timeout = 0
    while 1:
        try:
            #if serial.in_waiting > 0:  # Check if data is available
            #print("attempting read wo/ waiting...")
            data = serial.read(serial.in_waiting).decode('utf-8').strip()
            #data = serial.readline().decode('utf-8').strip()

            if len(data) < 1: # got nothing move on
                timeout += 1

            else:
                if DISPLAY_STATE==0: # we got data come back
                    timeout = 0
                    init_displays()
                    DISPLAY_STATE=1

                input_array = [int(i) for i in data.split(',')]
                
                set_rpm(input_array[0])
                set_gear(input_array[1])
                set_blink(input_array[2])
                set_kph(input_array[3])
                set_mph(input_array[4])
    
                #print("received:", data)
        except Exception as e:
            print("got error:", e)
            timeout+=1

        if DISPLAY_STATE == 1 and timeout > DISPLAY_TIMEOUT:
            print("timing out displays...")
            timeout_displays()
            DISPLAY_STATE = 0

        if timeout%(1/REFRESH_RATE)==0: 
            print("timeout:", int(timeout*REFRESH_RATE)+1)
        if timeout>10000: timeout=11 # avoid overflow
        time.sleep(REFRESH_RATE)


if __name__ == "__main__":
    #display_test()
    init_displays()
    serial_loop()
