#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC
* version: 20170327a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import RPi.GPIO as GPIO
from time import sleep
import sys
import random as rd


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

GPIO.setwarnings(False)

timeSleepSensor = 0.1
timeTransient0 = 0.05
timeTransient1 = 0.2
timeTransient2 = 0.5

webFolder = "/var/www/html/pirc/"
steerFile = "steerStatus.txt"
powerFile = "powerStatus.txt"

#************************************
''' Main initialization routine '''
#************************************

def main():
    
    #make sure motors are stopped
    fullStop()
    
    while True:
        l, r = irSensors()
        obstacleAvoidance(l,r)

        runManualControls()

#************************************
''' Control Motors'''
#************************************
def runMotor(motor, state):
    if motor == 1:  # motor for powering vehicle
        in1 = 5
        in2 = 7
        #pwn = 3
    
    elif motor == 0:    # motor for steering
        in1 = 11
        in2 = 13
        #pwn = 6
    
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
    #GPIO.output(pwn, 255)


#************************************
''' RunManualControls '''
#************************************
def runManualControls():
    with open(webFolder+powerFile, 'r') as f:
        powerStatus = f.readlines()[0]
    print(powerStatus)
    sleep(timeTransient0)
    with open(webFolder+steerFile, 'r') as f:
        steerStatus = f.readlines()[0]
    print(steerStatus)

    if powerStatus=='UP':
        runMotor(1,1)
    elif powerStatus=='DOWN':
        runMotor(1,-1)
    elif powerStatus=='STOP':
        runMotor(1,0)

    if steerStatus=='ZERO':
        runMotor(0,0)
    else:
        if steerStatus=='LEFT':
            runMotor(0,1)
        elif steerStatus=='RIGHT':
            runMotor(0,-1)
        with open(webFolder+steerFile, 'w') as f:
            f.write("ZERO")
        sleep(timeTransient1)
        print('\t',steerStatus)
        runMotor(0,0)

#************************************
''' Obstacle Avoidance '''
#************************************
def obstacleAvoidance(l,r):
    if l==0 & r!=0:                                #Right IR sensor detects an object
        print('Obstacle detected on Left',str(l))
        runMotor(0, 1)
        runMotor(1, 1)
        sleep(timeSleepSensor)
    elif r==0 & l!=0:                              #Left IR sensor detects an object
        print('Obstacle detected on Right',str(r))
        runMotor(0, -1)
        runMotor(1, 1)
        sleep(timeSleepSensor)
    elif r==0 & l==0:
        print('Obstacle detected in front',str(r),'BRAKE!')
        randomDirection = int(rd.uniform(-2,2))
        runMotor(0,randomDirection)
        runMotor(1, -1)
        sleep(timeTransient1)
        runMotor(0,-randomDirection)
        runMotor(1, 1)
        sleep(timeTransient2)
    runMotor(0, 0)

#************************************
''' Read IR sensors '''
#************************************
def irSensors():
    l=GPIO.input(3)                         #Reading output of right IR sensor
    r=GPIO.input(16)                        #Reading output of left IR sensor
    return l, r

#************************************
''' Full Stop '''
#************************************
def fullStop():
    print('\nFULL STOP\n')
    with open(webFolder+steerFile, 'w') as f:
        f.write("ZERO")
    runMotor(0,0)
    with open(webFolder+powerFile, 'w') as f:
        f.write("STOP")
    runMotor(1,0)

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
