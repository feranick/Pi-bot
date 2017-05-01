#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - auto
* version: 20170430b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import sys
import piRC_lib

from time import sleep
import random as rd

#************************************
''' Main initialization routine '''
#************************************

def main():
    #make sure motors are stopped
    piRC_libfullStop(False)
    
    while True:
        try:
            l,r,c,b = piRC_lib.readAllSonars(TRIG, ECHO)
            piRC_libobstacleAvoidanceSonars(l,r,c,b)
        except:
            piRC_lib.fullStop(True)
            return

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
