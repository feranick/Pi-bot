#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC
* version: 20170325a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import RPi.GPIO as GPIO
import time, sys
import random as rd


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)                            #Right sensor connection
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left sensor connection

#these need to be fixed for TB6612
GPIO.setup(5,GPIO.OUT)   #AIN1 motor input A
GPIO.setup(7,GPIO.OUT)   #AIN2 motor input B
GPIO.setup(9,GPIO.OUT)   #PWNA motor input B (power) - analog
GPIO.setup(11,GPIO.OUT)  #BIN1 motor input A
GPIO.setup(13,GPIO.OUT)  #BIN2 motor input B
GPIO.setup(14,GPIO.OUT)   #PWNA motor input B (power) - analog

GPIO.setwarnings(False)

timeSleepSensor = 0.1
timeTransient1 = 0.2
timeTransient2 = 0.5

#************************************
''' Main initialization routine '''
#************************************

def main():
    
    #make sure motors are stopped
    runMotor(1, 0)
    runMotor(0, 0)
    
    while True:

        #run power motor
        runMotor(1, 1)
        runMotor(0, 0)
        
        l, r = irSensors()
        obstacleAvoidance(l,r)

#************************************
''' Control Motors'''
#************************************
def runMotor(motor, state):
    if motor == 1:  # motor for powering vehicle
        in1 = 5
        in2 = 7
        pwn = 3
    
    elif motor == 0:    # motor for steering
        in1 = 11
        in2 = 13
        pwn = 6
    
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
''' Obstacle Avoidance '''
#************************************
def obstacleAvoidance(l,r):
    if l==0 & r!=0:                                #Right IR sensor detects an object
        print('Obstacle detected on Left',str(l))
        runMotor(0, 1)
        runMotor(1, 1)
        time.sleep(timeSleepSensor)
    elif r==0 & l!=0:                              #Left IR sensor detects an object
        print('Obstacle detected on Right',str(r))
        runMotor(0, -1)
        runMotor(1, 1)
        time.sleep(timeSleepSensor)
    elif r==0 & l==0:
        print('Obstacle detected in front',str(r),'BRAKE!')
        randomDirection = int(rd.uniform(-2,2))
        runMotor(0,randomDirection)
        runMotor(1, -1)
        time.sleep(timeTransient1)
        runMotor(0,-randomDirection)
        runMotor(1, 1)
        time.sleep(timeTransient2)
    runMotor(0, 0)

#************************************
''' Read IR sensors '''
#************************************
def irSensors():
    l=GPIO.input(3)                         #Reading output of right IR sensor
    r=GPIO.input(16)                        #Reading output of left IR sensor
    return l, r

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
