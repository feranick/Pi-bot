#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - write Learning file from sensors
* version: 20170424c
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
from datetime import datetime, date
import random as rd


#************************************
''' Main initialization routine '''
#************************************

def main():
    #make sure motors are stopped
    fullStop()
    
    #filename = 'Training_lrcbxyzsp' + str(datetime.now().strftime('_%Y-%m-%d_%H-%M-%S.txt'))
    filename = 'Training_lrcbxyzsp.txt'

    while True:
        try:
            l,r,c,b = readAllSonars(TRIG, ECHO)
            x,y,z = readAccel(True)
            s, p = statMotors()
            print(' L={0:.2f}, R={1:.2f}, C={2:.2f}, B={3:.2f}, X={4:.2f}, Y={5:.2f}, Z={6:.2f}, S={7:.1f}, P={7:.1f}'.format(l,r,c,b,x,y,z,s,p))
            with open(filename, "a") as sum_file:
                sum_file.write('{0:.2f},{1:.2f},{2:.2f},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7:.1f},{8:.1f}\n'.format(l,r,c,b,x,y,z,s,p))
        except:
            #fullStop()
            GPIO.cleanup()
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
