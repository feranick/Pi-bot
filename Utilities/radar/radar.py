#!/usr/bin/python3
#
# Measure speed using Doppler. 
# Uses: HB100 Doppler Speed Sensor
#

import RPi.GPIO as GPIO
import time, os

RADIN = 24
NUM_CYCLES = 2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RADIN, GPIO.IN)

def getSpeed():
   GPIO.wait_for_edge(RADIN, GPIO.FALLING)
   start = time.time()
   for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(RADIN, GPIO.FALLING)
   duration = time.time() - start       # seconds to run loop
   frequency = NUM_CYCLES / duration    # in Hz
   speed = frequency / float(31.36)     # Hz to MPH from sensor datasheet
   return speed

while True:
   print("Speed: ", getSpeed(),"MPH\n")
   sleep(0.5)
