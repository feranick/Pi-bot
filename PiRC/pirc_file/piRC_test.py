#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC-test
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

timeSleepSensor = 0.1
timeTransient0 = 0.05
timeTransient1 = 0.2
timeTransient2 = 0.75
timeTransient3 = 1

# (d[cm],Voltage[V]) = (5,3.2);(12,2);(20,1.25);(28,1);(60,0.5)
# https://goo.gl/BiFYpK
minSafeDistanceVoltage = 1.25

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
            obstacleAvoidance(l,r,c)
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
''' Obstacle Avoidance '''
#************************************
def obstacleAvoidance(l,r,c):
    if c>minSafeDistanceVoltage:
        if r==0 and l!=0:                                #Right IR sensor detects an object
            print('Obstacle detected on Left (l, r, c):',str(l),str(r),str(c))
            runMotor(0, 1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,-1)
            runMotor(1, 1)

        elif r!=0 and l==0:                               #Left IR sensor detects an object
            print('Obstacle detected on Right (l, r, c):',str(l),str(r),str(c))
            runMotor(0, -1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,1)
            runMotor(1, 1)

        elif r==0 and l==0:
            print('Obstacle detected Ahead (l, r, c):',str(l),str(r),str(c))
            randomDirection = rd.choice([-1,1])
            runMotor(0,randomDirection)
            runMotor(1, 1)
            sleep(timeTransient2)
                
        elif r!=0 and l!=0:
            print('Surrounded by obstacles - BRAKE! (l, r, c):',str(l),str(r),str(c))
            runMotor(0,0)
            runMotor(1, -1)
            sleep(timeTransient2)
            randomDirection = rd.choice([-1,1])
            runMotor(0,randomDirection)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,-randomDirection)
            runMotor(1, 1)
            sleep(timeTransient3)

    else:
        print('All clear (l, r, c):',str(l),str(r),str(c))
        runMotor(0, 0)

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
