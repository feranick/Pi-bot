#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC
* version: 20170324a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import RPi.GPIO as GPIO
import time
import random as rd


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)                            #Right sensor connection
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left sensor connection

GPIO.setup(5,GPIO.OUT)   #Left motor input A
GPIO.setup(7,GPIO.OUT)   #Left motor input B
GPIO.setup(11,GPIO.OUT)  #Right motor input A
GPIO.setup(13,GPIO.OUT)  #Right motor input B

GPIO.setwarnings(False)

timeSleepSensor = 0.1
timeTransient1 = 0.2
timeTransient2 = 0.5


#************************************
''' Main initialization routine '''
#************************************

def main():
    
    runMotor(0,True)
    runMotor(0,False)
    
    while True:

        runMotor(1,True)
        runMotor(0,False)
        
        l, r = irSensors()
        obstacleAvoidance(l,r)



#************************************
''' Control Motors '''
#************************************
def runMotor(state, motor):
    if motor==True: # motor for powering vehicle
        m1 = 5
        m2 = 7
    else            # motor for steering
        m1 = 11
        m2 = 13

    if state == -1:
        GPIO.output(m1,0)
        GPIO.output(m2,1)
    if state == 0:
        GPIO.output(m1,0)
        GPIO.output(m2,0)
    if state == 1:
        GPIO.output(m1,1)
        GPIO.output(m2,0)

#************************************
''' Obstacle Avoidance '''
#************************************
def obstacleAvoidance(l,r):
    if l==0 & r!=0:                                #Right IR sensor detects an object
        print('Obstacle detected on Left',str(l))
        runMotor(1,True)
        runMotor(1,False)
        time.sleep(timeSleepSensor)
    elif r==0 & l!=0:                              #Left IR sensor detects an object
        print('Obstacle detected on Right',str(r))
        runMotor(1,True)
        runMotor(-1,False)
        time.sleep(timeSleepSensor)
    elif r==0 & l==0:
        print('Obstacle detected in front',str(r),'BRAKE!')
        runMotor(-1,True)
        runMotor(0,False)
        time.sleep(timeTransient1)
        randomDirection = int(rd.uniform(-2,2))
        runMotor(1,True)
        runMotor(int(rd.uniform(-2,2)),r)
        time.sleep(timeTransient2)
        runMotor(0,r)


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
