#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_lib
* version: 20170424b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

from piRC_gpio import *
from time import sleep, time
import sys
import random as rd

timeSleepSensor = 0.1
timeTransient0 = 0.05
timeTransient1 = 0.2
timeTransient2 = 0.75
timeTransient3 = 1
minDistance = 15


#************************************
''' Obstacle Avoidance '''
''' ONLY FOR SONARS '''
''' to be rewritten after calibration'''
#************************************

def obstacleAvoidanceSonars(l,r,c):
    
    if c<15:                                          #Center sonar does not detect an object
        if r>minDistance and l<minDistance:           #Right sonar detects an object
            print('Obstacle detected on Left (l, r, c):',str(l),str(r),str(c))
            runMotor(0, 1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,-1)
            runMotor(1, 1)
        
        elif r<minDistance and l>minDistance:         #Left sonar detects an object
            print('Obstacle detected on Right (l, r, c):',str(l),str(r),str(c))
            runMotor(0, -1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,1)
            runMotor(1, 1)
    
        elif:
            if r>minDistance and l>minDistance:
                print('Obstacle detected Ahead (l, r, c):',str(l),str(r),str(c))
                #runMotor(0,0)
                #runMotor(1, -1)
                sleep(timeTransient1)
            if r<minDistance and l<minDistance:
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


#************************************
''' Obstacle Avoidance '''
''' ONLY FOR IR SENSORS '''
''' This will be deprecated when moving to sonars'''
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

        else:
            if r==0 and l==0:
            	print('Obstacle detected Ahead (l, r, c):',str(l),str(r),str(c))
            	runMotor(0,0)
            	runMotor(1, -1)
            	sleep(timeTransient1)
            if r!=0 and l!=0:
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
''' Read sonars '''
#************************************
def readAllSonars(TRIG, ECHO):
    trigSonar(TRIG)
    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(3)
    distances = pool.map(readEcho, ECHO)
    pool.close()
    pool.join()
    
    return distances[0], distances[2], distances[1],

def readEcho(ECHO):
    while GPIO.input(ECHO)==0:
        pulse_start = time()
    while GPIO.input(ECHO)==1:
        pulse_end = time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    GPIO.cleanup()
    #print("Distance:",distance,"cm")
    return distance

def trigSonar(TRIG):
    GPIO.output(TRIG, False)
    sleep(0.0001)
    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)


#************************************
''' Read IR sensors '''
''' This is obsolete) '''
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
