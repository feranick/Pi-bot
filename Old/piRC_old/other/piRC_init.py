#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_init
* version: 20170510a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

import RPi.GPIO as GPIO

#************************************
''' GPIO definitions '''
#************************************

TRIG = [31,35,38,29]
ECHO = [33,37,40,32]

AIN1 = 11
AIN2 = 13
PWNA = 15
BIN1 = 8
BIN2 = 10
PWNB = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

for i in range(len(ECHO)):
    GPIO.setup(TRIG[i],GPIO.OUT)
    GPIO.setup(ECHO[i],GPIO.IN)

GPIO.setup(AIN1,GPIO.OUT)   #AIN1 motor input A
GPIO.setup(AIN2,GPIO.OUT)   #AIN2 motor input B
GPIO.setup(PWNA,GPIO.OUT)   #PWNA motor input B (power) - analog
GPIO.setup(BIN1,GPIO.OUT)  #BIN1 motor input A
GPIO.setup(BIN2,GPIO.OUT)  #BIN2 motor input B
GPIO.setup(PWNB,GPIO.OUT)   #PWNA motor input B (power) - analog
