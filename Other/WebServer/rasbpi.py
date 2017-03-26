#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)
true = 1

fileName = "buttonStatus.txt"

while(true):
    with open(fileName, 'r') as f:
        status = f.readlines()
    if(status != 'ZERO'):
        with open(fileName, 'ab') as f:
            f.write("ZERO")
    sleep(0.2)
    print(status)

    # This needs fixing with proper channels
    if status=='UP':
        GPIO.output(5,True)
    elif status=='DOWN':
        GPIO.output(5,False)

