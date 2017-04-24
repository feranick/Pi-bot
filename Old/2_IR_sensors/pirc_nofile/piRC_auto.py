#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - auto
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
        except:
            fullStop()
            return

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
