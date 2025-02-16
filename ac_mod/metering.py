#!/usr/bin/env python3

import os
from third_party.pyserial.serial import *
from time import *
from threading import Thread
import ac
import acsys
from third_party.sim_info import *

port=""
try:
    d=os.path.dirname(os.path.realpath(__file__))+'\\com.cfg'
    f=open(d)
except:
    raise Exception("ERROR: com.cfg NOT FOUND")
    sys.exit()
COM_PORT="".join(f.readlines()).split('=')[1]
appName = "Metering"
width, height = 1 , 1
simInfo = SimInfo()
try: s = Serial(COM_PORT)
except:
    raise Exception("ERROR: COULD NOT FIND COM PORT, INVALID CONFIG\n\tgot port: "+COM_PORT)
    sys.exit()
deltaTimer = 0
maxRpm = 0

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
    deltaTimer += deltaT
    if deltaTimer > 0.05:
        deltaTimer = 0
        blink=0
        rpmValue = ac.getCarState(0, acsys.CS.RPM)
        gearValue = ac.getCarState(0, acsys.CS.Gear)
        if rpmValue > maxRpm: maxRpm = rpmValue
        if rpmValue > maxRpm*0.94: blink=1
        d=str(int(rpmValue))+','+str(gearValue-1)+','+str(blink)+'\n'
        print(d)
        try:
            s.write(str.encode(d))
            s.flush()
        except Exception as e:
            print(e)
            s.close()
            s.open()







