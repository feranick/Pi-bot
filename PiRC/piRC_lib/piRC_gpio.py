#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_gpio library
* version: 20170329a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

import RPi.GPIO as GPIO

IR1 = 3
IR2 = 5

AIN1 = 11
AIN2 = 13
PWNA = 15
BIN1 = 19
BIN2 = 21
PWNB = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IR1, GPIO.IN)                            #Right sensor connection
GPIO.setup(IR2, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left sensor connection

#these need to be fixed for TB6612
GPIO.setup(AIN1,GPIO.OUT)   #AIN1 motor input A
GPIO.setup(AIN2,GPIO.OUT)   #AIN2 motor input B
GPIO.setup(PWNA,GPIO.OUT)   #PWNA motor input B (power) - analog
GPIO.setup(BIN1,GPIO.OUT)  #BIN1 motor input A
GPIO.setup(BIN2,GPIO.OUT)  #BIN2 motor input B
GPIO.setup(PWNB,GPIO.OUT)   #PWNA motor input B (power) - analog

