#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC
* version: 20170404a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import sys
sys.path.append('piRC_lib')

import piRC_gpio
from piRC_lib import *

from time import sleep
import random as rd

webFolder = "/var/www/html/pirc_file/WebServer/"
steerFile = "steerStatus.txt"
powerFile = "powerStatus.txt"

#************************************
''' Main initialization routine '''
#************************************

def main():
    #make sure motors are stopped
    fullStop()
    
    while True:
        try:
            l, r, c = irSensors()
            obstacleAvoidance3(l,r,c)
            #obstacleAvoidance2(l,r,c)
            runManualControls()
        except:
            fullStop()
            return

#************************************
''' RunManualControls '''
#************************************
def runManualControls():
    with open(webFolder+powerFile, 'r') as f:
        powerStatus = f.readlines()[0]
    print(powerStatus)
    sleep(timeTransient0)
    with open(webFolder+steerFile, 'r') as f:
        steerStatus = f.readlines()[0]
    print(steerStatus)

    if powerStatus=='STOP':
        runMotor(1,0)
        with open(webFolder+powerFile, 'w') as f:
            f.write("STOP")
        sleep(timeTransient1)
    else:
        if powerStatus=='DOWN':
            runMotor(1,-1)
        elif powerStatus=='UP':
            runMotor(1,1)

    if steerStatus=='ZERO':
        runMotor(0,0)
    else:
        if steerStatus=='LEFT':
            runMotor(0,-1)
        elif steerStatus=='RIGHT':
            runMotor(0,1)
        with open(webFolder+steerFile, 'w') as f:
            f.write("ZERO")
        sleep(timeTransient1)
        print('\t',steerStatus)
        runMotor(0,0)

#************************************
''' Full Stop '''
#************************************
def fullStop():
    print('\nFULL STOP\n')
    with open(webFolder+steerFile, 'w') as f:
        f.write("ZERO")
    runMotor(0,0)
    with open(webFolder+powerFile, 'w') as f:
        f.write("STOP")
    runMotor(1,0)

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
