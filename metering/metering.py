#!/usr/bin/env python3

import os
import sys
from serial import *
from time import *
import ac
import acsys
from sim_info import *
from _thread import *

appName = "Metering"

d=os.path.dirname(os.path.realpath(__file__))+'\\com.cfg'
sys.stdout=open(os.path.dirname(os.path.realpath(__file__))+"\\out.txt",'w+')
sys.stderr=open(os.path.dirname(os.path.realpath(__file__))+"\\out.txt",'w+')

try:
    print('reading config file at: '+d)
    f=open(d)
except:
    raise Exception("ERROR: "+d+" NOT FOUND")
    sys.exit()
COM_PORT="".join(f.readlines()).split('=')[1].strip()

width, height = 1 , 1 # width and height of the app's window
simInfo = SimInfo()
try: s = Serial(COM_PORT,9600,timeout=1)
except Exception as e: raise Exception("ERROR: COULD NOT FIND COM PORT, INVALID CONFIG\n\tfound ports: "+COM_PORT); sys.exit()

globalTimer = 0
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
    global globalTimer
    global deltaTimer
    global thread
    global maxRpm
    try:
        globalTimer += deltaT
        deltaTimer += deltaT
        if deltaTimer > 0.05:
            deltaTimer = 0
            blink=0
            rpmValue = ac.getCarState(0, acsys.CS.RPM)
            gearValue = ac.getCarState(0, acsys.CS.Gear)
            speed1Value = int(ac.getCarState(0, acsys.CS.SpeedKMH))
            speed2Value = int((ac.getCarState(0, acsys.CS.SpeedKMH))*0.621371)
            if rpmValue > maxRpm: maxRpm = rpmValue
            if rpmValue > maxRpm*0.94 and globalTimer>16: blink=1
            d=str(int(rpmValue))+','+str(gearValue-1)+','+str(blink)+','+str(speed1Value)+','+str(speed2Value)+'\n'
            start_new_thread(send_msg,(d,))
    except Exception as e:
        print("ACUPDATE EXCEPTION:",e)

def send_msg(d):
    global s
    try:
        print("writing:",str(d).strip(),"at time:",globalTimer)
        s.write(str.encode(d))
        s.flush()
    except Exception as e:
        print("SEND_MSG EXCEPTION:",e)
        try: s = Serial(COM_PORT,9600,timeout=1)
        except: print("could not reopen connection...")








