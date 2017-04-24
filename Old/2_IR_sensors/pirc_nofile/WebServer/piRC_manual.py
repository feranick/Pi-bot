#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_manual
* version: 20170330a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
#print(__doc__)

import sys
sys.path.append('../piRC_lib')

import piRC_gpio
from piRC_lib import *
from time import sleep

timeSleepSensor = 0.1
timeTransient0 = 0.05
timeTransient1 = 0.2
timeTransient2 = 0.75

#************************************
''' Main initialization routine '''
#************************************
def main():
    if len(sys.argv) > 1:
        runManualControls(sys.argv[1])
    else:
        return

#************************************
''' RunManualControls '''
#************************************
def runManualControls(status):
    print(status)
    if status=='UP':
        runMotor(1,1)
    elif status=='DOWN':
        runMotor(1,-1)
    elif status=='STOP':
        runMotor(1,0)
    elif status=='ZERO':
        runMotor(0,0)
    else:
        if status=='LEFT':
            runMotor(0,1)
        if status=='RIGHT':
            runMotor(0,-1)
        sleep(timeTransient1)
        runMotor(0,0)

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
