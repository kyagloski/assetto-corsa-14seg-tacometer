#!/usr/bin/env python3

import os
from serial import *
from time import *
import ac
import acsys
from sim_info import *
from _thread import *

port=""
d=os.path.dirname(os.path.realpath(__file__))+'\\com.cfg'
try:
    print('reading config file at: '+d)
    f=open(d)
except:
    raise Exception("ERROR: "+d+" NOT FOUND")
    sys.exit()
COM_PORT="".join(f.readlines()).split('=')[1]
appName = "Metering"
width, height = 1 , 1 # width and height of the app's window
simInfo = SimInfo()
COM_PORT='COM3'
try: s = Serial(COM_PORT)
except:
    raise Exception("ERROR: COULD NOT FIND COM PORT, INVALID CONFIG\n\tgot port: "+COM_PORT)
    sys.exit()
deltaTimer = 0
maxRpm = 0
refreshRate=1/100

def acMain(ac_version):
    global appWindow
    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)
    ac.addRenderCallback(appWindow, appGL)
    return appName

def appGL(deltaT):
    pass

def acUpdate(deltaT):
    global deltaTimer
    global thread
    global maxRpm
    try:
        deltaTimer += deltaT
        if deltaTimer > refreshRate:
            deltaTimer = 0
            blink=0
            rpmValue = ac.getCarState(0, acsys.CS.RPM)
            gearValue = ac.getCarState(0, acsys.CS.Gear)
            speed1Value = int(ac.getCarState(0, acsys.CS.SpeedKMH))
            speed2Value = int((ac.getCarState(0, acsys.CS.SpeedKMH))*0.621371)
            if rpmValue > maxRpm: maxRpm = rpmValue
            if rpmValue > maxRpm*0.94: blink=1
            d=str(int(rpmValue))+','+str(gearValue-1)+','+str(blink)+','+str(speed1Value)+str(speed2Value)+'\n'
            start_new_thread(send_msg,(d,))
    except Exception as e:
        print("got exception:",e)

def send_msg(d):
    global s
    try:
        s.write(str.encode(d))
        s.flush()
    except Exception as e:
        print(e)
        # s.close()
        # s.open()







