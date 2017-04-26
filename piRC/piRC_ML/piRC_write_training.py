#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - write training file from sensors
* version: 20170425a
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
    
    #filename = 'Training_splrcbxyz' + str(datetime.now().strftime('_%Y-%m-%d_%H-%M-%S.txt'))
    filename = 'Training_splrcbxyz.txt'

    while True:
        try:
            l,r,c,b = readAllSonars(TRIG, ECHO)
            x,y,z = readAccel(True)
            s,p = statMotors()
            print(' S={0:.1f}, P={1:.1f}, L={2:.2f}, R={3:.2f}, C={4:.2f}, B={5:.2f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}'.format(s,p,l,r,c,b,x,y,z))
            with open(filename, "a") as sum_file:
                sum_file.write('{0:.1f}\t{1:.1f}\t{2:.2f}\t{3:.2f}\t{4:.2f}\t{5:.2f}\t{6:.3f}\t{7:.3f}\t{8:.3f}\n'.format(s,p,l,r,c,b,x,y,z))
        except:
            fullStop()
            GPIO.cleanup()
            return

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
