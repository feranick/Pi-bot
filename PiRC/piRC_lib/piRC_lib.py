#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_lib
* version: 20170329b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

from piRC_gpio import *
from time import sleep
import sys
import random as rd

#************************************
''' Control Motors'''
#************************************
def runMotor(motor, state):
    if motor == 1:  # motor for powering vehicle
        in1 = AIN1
        in2 = AIN2
        pwn = PWNA
    
    elif motor == 0:    # motor for steering
        in1 = BIN1
        in2 = BIN2
        pwn = PWNB
    
    if state == -1:
        GPIO.output(in1,0)
        GPIO.output(in2,1)
    if state == 0:
        GPIO.output(in1,0)
        GPIO.output(in2,0)
    if state == 1:
        GPIO.output(in1,1)
        GPIO.output(in2,0)
    #full power
    GPIO.output(pwn, 255)

#************************************
''' Read IR sensors '''
#************************************
def irSensors():
    l=GPIO.input(IR1)                         #Reading output of right IR sensor
    r=GPIO.input(IR2)                        #Reading output of left IR sensor
    return l, r

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
