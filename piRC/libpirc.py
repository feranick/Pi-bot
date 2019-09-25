#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* libpirc
* version: 20190925b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''

import RPi.GPIO as GPIO
from time import sleep, time
import sys
import random as rd
import Adafruit_ADXL345  # Accelerometer ADXL345
import Adafruit_ADS1x15  # ADC ADS1115
from PIL import Image
import picamera
import numpy as np

#************************************
''' GPIO definitions '''
#************************************

#TRIG = [31,35,38,29]
#ECHO = [33,37,40,32]

TRIG = [31,35,29,38]
ECHO = [33,37,32,40]

AIN1 = 11
AIN2 = 13
PWNA = 15
BIN1 = 8
BIN2 = 10
PWNB = 12

RADIN = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

for i in range(len(ECHO)):
    GPIO.setup(TRIG[i],GPIO.OUT)
    GPIO.setup(ECHO[i],GPIO.IN)

GPIO.setup(AIN1,GPIO.OUT)   #AIN1 motor input A
GPIO.setup(AIN2,GPIO.OUT)   #AIN2 motor input B
GPIO.setup(PWNA,GPIO.OUT)   #PWNA motor input B (power) - analog
GPIO.setup(BIN1,GPIO.OUT)   #BIN1 motor input A
GPIO.setup(BIN2,GPIO.OUT)   #BIN2 motor input B
GPIO.setup(PWNB,GPIO.OUT)   #PWNA motor input B (power) - analog

GPIO.setup(RADIN, GPIO.IN)  #Radar

#************************************
''' General definitions '''
#************************************
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

filename = 'Training_splrcbxyz.txt'

maxSonarRange = 1000 # max set distance in cm

radNumCycles = 3 # number of cycles to average for radar
radTimeout = 100 #ms
radMinSpeed = 0.22

img_size = (320, 320)
resized_size = (10,10)

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
    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(len(ECHO))
    distances = pool.starmap(readSonar, zip(TRIG,ECHO))
    pool.close()
    pool.join()
    return distances[0], distances[1], distances[2], distances[3]

def readSonar(TRIG,ECHO):
    pulse_start = 0.0
    pulse_end = 0.0
    initTime = time()
    
    GPIO.output(TRIG, False)
    sleep(0.001)
    GPIO.output(TRIG, True)
    sleep(0.0002)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time()
    
    while GPIO.input(ECHO)==1:
        pulse_end = time()
        if time() - initTime > 0.5:
            break
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if distance > maxSonarRange:
        distance = maxSonarRange
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
    s1 = (adc.read_adc(0, gain=GAIN, data_rate=128)-adc.read_adc(1, gain=GAIN, data_rate=128))*FACTOR
    p1 = (adc.read_adc(3, gain=GAIN, data_rate=128)-adc.read_adc(2, gain=GAIN, data_rate=128))*FACTOR
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
''' Read Speed via Radar Doppler '''
#************************************
def getSpeedRadar():
   GPIO.wait_for_edge(RADIN, GPIO.FALLING, timeout = radTimeout)
   start = time()
   for impulse_count in range(radNumCycles):
      GPIO.wait_for_edge(RADIN, GPIO.FALLING, timeout = radTimeout)
   duration = time() - start       # seconds to run loop
   frequency = radNumCycles / duration    # in Hz
   speed = frequency * float(0.44704) / float(31.36)     # Hz to km/h from sensor datasheet
   if speed < radMinSpeed:
      speed = 0
   return speed

#************************************
''' Camera methods '''
#************************************
class Camera():
    def __init__(self, parent=None):
        #print("Initializing camera")
        self.cam = picamera.PiCamera()
        self.cam.resolution = img_size
        self.cam.vflip = True
        self.cam.hflip = True

    def getImage(self):
        output = np.empty((img_size[0], img_size[1],3), dtype=np.uint8)
        self.cam.capture(output, 'rgb')
        img = Image.fromarray(output).convert('L')
        img_resized = img.resize(resized_size, Image.ANTIALIAS)
        data = np.asarray( img_resized, dtype="int32" ).flatten()
        #print(data)
        return data

    def saveImage(self, npdata, outfilename ) :
        self.img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
        self.img.save( outfilename )

cam = Camera()

#************************************
''' Read All sensors '''
#************************************
def readAllSensors(useCamera):
    l,r,c,b = readAllSonars(TRIG, ECHO)
    x,y,z = readAccel(True)
    s,p = statMotors()
    v = getSpeedRadar()
    data = np.asarray((s,p,l,r,c,b,x,y,z,v))
    if useCamera == True:
        img = cam.getImage()
        data = np.append(data, img)
        #print(data)
    return data

#************************************
''' Full Stop '''
#************************************
def fullStop(end):
    runMotor(0,0)
    runMotor(1,0)
    if end is True:
        print('\nFULL STOP - Ending\n')
        GPIO.cleanup()
    else:
        print('\nFULL STOP - Starting...\n')

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
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
