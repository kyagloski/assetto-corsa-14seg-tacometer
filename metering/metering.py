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

DO_LOGGING=False

if DO_LOGGING:
    sys.stdout=open(os.path.dirname(os.path.realpath(__file__))+"\\out.txt",'w+')
    sys.stderr=open(os.path.dirname(os.path.realpath(__file__))+"\\out.txt",'w+')

cf=os.path.dirname(os.path.realpath(__file__))+'\\com.cfg'
try: print('reading config file at: '+cf); f=open(cf)
except: raise Exception("ERROR: "+cf+" NOT FOUND"); sys.exit()
COM_PORT="".join(f.readlines()).split('=')[1].strip()

simInfo = SimInfo()
try: ser = Serial(COM_PORT,9600,timeout=0); ser.dtr=True; ser.write_timeout=0.1
except Exception as e: print("ERROR: COULD NOT FIND COM PORT, INVALID CONFIG\n\tfound ports: "+COM_PORT)
#raise Exception("ERROR: COULD NOT FIND COM PORT, INVALID CONFIG\n\tfound ports: "+COM_PORT)

globalTimer = 0
deltaTimer = 0
maxRpm = 0

def acMain(ac_version):
    global appWindow
    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, 1, 1)
    ac.addRenderCallback(appWindow, appGL)
    return appName

def appGL(deltaT):
    pass

def acUpdate(deltaT):
    global globalTimer
    global deltaTimer
    global maxRpm
    try:
        globalTimer += deltaT
        deltaTimer += deltaT
        if deltaTimer > 0.05:
            deltaTimer = 0
            blink = 0
            rpmValue = ac.getCarState(0, acsys.CS.RPM)
            gearValue = ac.getCarState(0, acsys.CS.Gear)
            speed1Value = int(ac.getCarState(0, acsys.CS.SpeedKMH))
            speed2Value = int((ac.getCarState(0, acsys.CS.SpeedKMH))*0.621371)
            if rpmValue > maxRpm: maxRpm = rpmValue
            if rpmValue > maxRpm*0.94 and globalTimer > 20: blink = 1
            data=str(int(rpmValue))+','+str(gearValue-1)+','+str(blink)+','+str(speed1Value)+','+str(speed2Value)+'\n'
            start_new_thread(send_msg,(data,))
    except Exception as e:
        print("ACUPDATE EXCEPTION:",e)

def send_msg(data):
    global ser
    try:
        print("writing:",str(data).strip(),"at time:",globalTimer)
        ser.write(data.encode('utf-8'))
        ser.flush()
    except Exception as e:
        print("SEND_MSG EXCEPTION:",e)
        try: ser = Serial(COM_PORT,9600,timeout=0); ser.dtr=True; ser.write_timeout=0.1
        except: print("could not reopen connection...")








