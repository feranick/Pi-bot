#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep, time
import sys
import random as rd
import Adafruit_ADXL345  # Accelerometer ADXL345
import Adafruit_ADS1x15  # ADC ADS1115

#************************************
''' GPIO definitions '''
#************************************

AIN1 = 11
AIN2 = 13
PWNA = 15
BIN1 = 8
BIN2 = 10
PWNB = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(AIN1,GPIO.OUT)   #AIN1 motor input A
GPIO.setup(AIN2,GPIO.OUT)   #AIN2 motor input B
GPIO.setup(PWNA,GPIO.OUT)   #PWNA motor input B (power) - analog
GPIO.setup(BIN1,GPIO.OUT)  #BIN1 motor input A
GPIO.setup(BIN2,GPIO.OUT)  #BIN2 motor input B
GPIO.setup(PWNB,GPIO.OUT)   #PWNA motor input B (power) - analog


def main():
    runMotor(0,1)
    runMotor(1,1)
    sleep(1)
    runMotor(0,0)
    runMotor(1,0)
    sleep(1)
    runMotor(0,-1)
    runMotor(1,-1)
    sleep(1)
    runMotor(0,0)
    runMotor(1,0)
    sleep(1)
    
    runMotor(0,1)
    sleep(1)
    runMotor(0,0)
    sleep(1)
    runMotor(0,-1)
    sleep(1)
    runMotor(0,0)

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
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
