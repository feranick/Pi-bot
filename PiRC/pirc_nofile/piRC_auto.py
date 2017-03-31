#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - auto
* version: 20170331a
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

#************************************
''' Main initialization routine '''
#************************************

def main():
    #make sure motors are stopped
    fullStop()
    
    while True:
        try:
            l, r = irSensors()
            obstacleAvoidance(l,r)
        except:
            fullStop()
            return

#************************************
''' Obstacle Avoidance '''
#************************************
def obstacleAvoidance(l,r):
    if r==0 and l!=0:                                #Right IR sensor detects an object
        print('Obstacle detected on Left',str(l))
        runMotor(0, 1)
        runMotor(1, 1)
        sleep(timeTransient2)
    elif r!=0 and l==0:                              #Left IR sensor detects an object
        print('Obstacle detected on Right',str(r))
        runMotor(0, -1)
        runMotor(1, 1)
        sleep(timeTransient2)
    elif r!=0 and l!=0:
        print('Obstacle detected in front',str(r),'BRAKE!')
        randomDirection = rd.choice([-1,1])
        runMotor(0,randomDirection)
        runMotor(1, -1)
        sleep(timeTransient3)
        runMotor(0,-randomDirection)
        runMotor(1, 1)
        sleep(timeTransient3)
    elif r==0 and l==0:
        runMotor(0, 0)

#************************************
''' Full Stop '''
#************************************
def fullStop():
    print('\nFULL STOP\n')
    runMotor(0,0)
    runMotor(1,0)

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
