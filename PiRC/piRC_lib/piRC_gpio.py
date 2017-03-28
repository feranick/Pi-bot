#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_gpio library
* version: 20170328b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)                            #Right sensor connection
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left sensor connection

#these need to be fixed for TB6612
GPIO.setup(5,GPIO.OUT)   #AIN1 motor input A
GPIO.setup(7,GPIO.OUT)   #AIN2 motor input B
#GPIO.setup(5,GPIO.OUT)   #PWNA motor input B (power) - analog
GPIO.setup(11,GPIO.OUT)  #BIN1 motor input A
GPIO.setup(13,GPIO.OUT)  #BIN2 motor input B
#GPIO.setup(14,GPIO.OUT)   #PWNA motor input B (power) - analog

