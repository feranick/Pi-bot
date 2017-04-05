#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_lib
* version: 20170404b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

from piRC_gpio import *
from time import sleep
import sys
import random as rd

# (d[cm],Voltage[V]) = (5,3.2);(12,2);(20,1.25);(28,1);(60,0.5)
# https://goo.gl/BiFYpK

#************************************
''' Obstacle Avoidance '''
#************************************
def obstacleAvoidance3(l,r,c):
    if c!=0:
        if r==0 and l!=0:                                #Right IR sensor detects an object
            print('Obstacle detected on Left (l, r, c):',str(l),str(r),str(c))
            runMotor(0, 1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,-1)
            runMotor(1, 1)
        
        elif r!=0 and l==0:                               #Left IR sensor detects an object
            print('Obstacle detected on Right (l, r, c):',str(l),str(r),str(c))
            runMotor(0, -1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,1)
            runMotor(1, 1)
        
        elif r==0 and l==0:
            print('Obstacle detected Ahead (l, r, c):',str(l),str(r),str(c))
            randomDirection = rd.choice([-1,1])
            runMotor(0,randomDirection)
            runMotor(1, 1)
            sleep(timeTransient2)
        
        elif r!=0 and l!=0:
            print('Surrounded by obstacles - BRAKE! (l, r, c):',str(l),str(r),str(c))
            runMotor(0,0)
            runMotor(1, -1)
            sleep(timeTransient2)
            randomDirection = rd.choice([-1,1])
            runMotor(0,randomDirection)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,-randomDirection)
            runMotor(1, 1)
            sleep(timeTransient3)

    else:
        print('All clear (l, r, c):',str(l),str(r),str(c))
        runMotor(0, 0)


''' Old 2 sensors version'''
def obstacleAvoidance2(l,r,c):
    if r==0 and l!=0:                                #Right IR sensor detects an object
        print('Obstacle detected on Left',str(l))
        runMotor(0, 1)
        runMotor(1, 1)
        sleep(timeTransient2)
    elif r!=0 and l==0:                               #Left IR sensor detects an object
        print('Obstacle detected on Right',str(r))
        runMotor(0, -1)
        runMotor(1, 1)
        sleep(timeTransient2)
    elif r!=0 and l!=0:
        print('Obstacle detected in front',str(r),'BRAKE!')
        randomDirection = rd.choice([-1,1])
        runMotor(0,randomDirection)
        runMotor(1, -1)
        sleep(timeTransient3)
        runMotor(0,-randomDirection)
        runMotor(1, 1)
        sleep(timeTransient3)
    elif r==0 and l==0:
        runMotor(0, 0)

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
''' Read IR sensors '''
#************************************
def irSensors():
    l = GPIO.input(IRl)                         #Reading output of right IR sensor
    r = GPIO.input(IRr)                        #Reading output of left IR sensor
    c = GPIO.input(IRc)
    return l, r, c

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
