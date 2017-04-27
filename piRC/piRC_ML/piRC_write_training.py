#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - write training file from sensors
* (This will be soon integrated with the main ML program)
* version: 20170426c
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
from piRC_ML import *

from time import sleep
from datetime import datetime, date
import random as rd

#************************************
''' Main initialization routine '''
#************************************

def main():
    #make sure motors are stopped
    fullStop()
    
    #filename = 'Training_splrcbxyz' + str(datetime.now().strftime('_%Y-%m-%d_%H-%M-%S.txt'))
    filename = 'Training_splrcbxyz.txt'

    while True:
        try:
            l,r,c,b = readAllSonars(TRIG, ECHO)
            x,y,z = readAccel(True)
            s,p = statMotors()
            print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}'.format(s,p,l,r,c,b,x,y,z))
            with open(filename, "a") as sum_file:
                sum_file.write('{0:.0f}\t{1:.0f}\t{2:.0f}\t{3:.0f}\t{4:.0f}\t{5:.0f}\t{6:.3f}\t{7:.3f}\t{8:.3f}\n'.format(s,p,l,r,c,b,x,y,z))
        except:
            fullStop()
            GPIO.cleanup()
            return

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
