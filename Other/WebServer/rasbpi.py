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
    print(powerStatus[0])
    with open(steerFile, 'r') as f:
        steerStatus = f.readlines()
    print(steerStatus[0])
    sleep(0.1)
    if(steerStatus[0] != 'ZERO'):
        with open(steerFile, 'w') as f:
            f.write("ZERO")
        sleep(0.1)
        print(steerStatus[0])

    # This needs fixing with proper channels
    if powerStatus=='UP':
        GPIO.output(5,True)
    elif powerStatus=='DOWN':
        GPIO.output(5,False)
    elif powerStatus=='STOP':
        GPIO.output(5,False)

    if steerStatus=='LEFT':
        GPIO.output(5,True)
    elif steerStatus=='RIGHT':
        GPIO.output(5,False)
    elif steerStatus=='ZERO':
        GPIO.output(5,False)
