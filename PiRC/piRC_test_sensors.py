#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - test Sonars
* version: 20170424b
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
            l,r,c,b = readAllSonars(TRIG, ECHO)
            print(' L={0}, C={1}, R={2}, B={3}'.format(l,r,c,b))
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
