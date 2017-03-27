#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)
true = 1

steerFile = "steerStatus.txt"
powerFile = "powerStatus.txt"

while(true):
    with open(powerFile, 'r') as f:
        powerStatus = f.readlines()
    print(powerStatus)
    with open(steerFile, 'r') as f:
        steerStatus = f.readlines()
    print(steerStatus)
    speep(0.2)
    if(steerStatus != 'ZERO'):
        with open(fileName, 'ab') as f:
            f.write("ZERO")
    	sleep(0.2)
    	print(steerStatus)

    # This needs fixing with proper channels
    if powerStatus=='UP':
        GPIO.output(5,True)
    elif powerStatus=='DOWN':
        GPIO.output(5,False)
    elif powerStatus=='STOP'
        GPIO.output(5,False)

    if steerStatus=='LEFT':
        GPIO.output(5,True)
    elif steerStatus=='RIGHT':
        GPIO.output(5,False)
    elif steerStatus=='ZERO'
        GPIO.output(5,False)
