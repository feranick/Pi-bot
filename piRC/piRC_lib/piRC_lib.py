#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_lib
* version: 20170427c
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

from piRC_gpio import *
from time import sleep, time
import sys
import random as rd
import Adafruit_ADXL345  # Accelerometer ADXL345
import Adafruit_ADS1x15  # ADC ADS1115

SCALE_MULTIPLIER = 0.004
EARTH_GRAVITY_MS2  = 9.80665

timeSleepSensor = 0.1
timeTransient0 = 0.05
timeTransient1 = 0.2
timeTransient2 = 0.75
timeTransient3 = 1
minDistanceL = 15
minDistanceR = 15
minDistanceC = 15
minDistanceB = 10

#************************************
''' Obstacle Avoidance '''
''' ONLY FOR SONARS '''
''' to be rewritten after calibration'''
#************************************

def obstacleAvoidanceSonars(l,r,c,b):
    
    if c<minDistanceC:                                  #Center sonar does not detect an object
        if r>minDistanceR and l<minDistanceL:           #Right sonar detects an object
            print('Obstacle detected on Left (l, r, c):',str(l),str(r),str(c))
            runMotor(0, 1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,-1)
            runMotor(1, 1)
        
        elif r<minDistanceR and l>minDistanceL:         #Left sonar detects an object
            print('Obstacle detected on Right (l, r, c):',str(l),str(r),str(c))
            runMotor(0, -1)
            runMotor(1, -1)
            sleep(timeTransient3)
            runMotor(0,1)
            runMotor(1, 1)
    
        else:
            if r>minDistanceR and l>minDistanceL:
                print('Obstacle detected Ahead (l, r, c):',str(l),str(r),str(c))
                #runMotor(0,0)
                #runMotor(1, -1)
                sleep(timeTransient1)
            if r<minDistanceR and l<minDistanceL:
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

    if b<minDistanceB:
        runMotor(1, 1)

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
    pool = ThreadPool(len(ECHO))
    distances = pool.starmap(readSonar, zip(TRIG,ECHO))
    pool.close()
    pool.join()
    return distances[0], distances[1], distances[2], distances[3]

def readSonar(TRIG,ECHO):
    pulse_start = 0.0
    pulse_end = 0.0
    
    GPIO.output(TRIG, False)
    sleep(0.001)
    GPIO.output(TRIG, True)
    sleep(0.0002)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time()
    while GPIO.input(ECHO)==1:
        pulse_end = time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

#************************************
''' Read Accelerometer '''
#************************************
def readAccel(isG):
    accel = Adafruit_ADXL345.ADXL345(address=0x53,busnum=1)
    accel.set_range(Adafruit_ADXL345.ADXL345_RANGE_2_G)
    x, y, z = [r*SCALE_MULTIPLIER for r in accel.read()]
    if isG is False:
        (x, y, z) = tuple(r*EARTH_GRAVITY_MS2 for r in (x,y,z))
    return x, y, z

#************************************
''' Read Status Motors '''
#************************************
def statMotors():
    adc = Adafruit_ADS1x15.ADS1115(address=0x48,busnum=1)
    GAIN = 1
    FACTOR = 5/32000 # using a 1.5MOhm
    s1 = (adc.read_adc(0, gain=GAIN, data_rate=128)-adc.read_adc(0, gain=GAIN, data_rate=128))*FACTOR
    p1 = (adc.read_adc(2, gain=GAIN, data_rate=128)-adc.read_adc(3, gain=GAIN, data_rate=128))*FACTOR
    if s1 > 2:
        s = 1
    elif s1<-2:
        s = -1
    else:
        s = 0
    if p1 > 2:
        p = 1
    elif p1<-2:
        p = -1
    else:
        p = 0
    return s, p

#************************************
''' Full Stop '''
#************************************
def fullStop():
    print('\nFULL STOP\n')
    runMotor(0,0)
    runMotor(1,0)

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
