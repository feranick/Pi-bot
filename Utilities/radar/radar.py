#!/usr/bin/python3
#
# Measure speed using Doppler.
# Uses: HB100 Doppler Speed Sensor
#
# version 20180103
#

import RPi.GPIO as GPIO
import time, os

RADIN = 24
NUM_CYCLES = 3
timeout = 100 #ms
minSpeed = 0.8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RADIN, GPIO.IN)

def getSpeed():
   GPIO.wait_for_edge(RADIN, GPIO.FALLING, timeout = timeout)
   start = time.time()
   for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(RADIN, GPIO.FALLING, timeout = timeout)
   duration = time.time() - start       # seconds to run loop
   frequency = NUM_CYCLES / duration    # in Hz
   speed = frequency * float(1.60934) / float(31.36)     # Hz to km/h from sensor datasheet
   if speed < minSpeed:
      speed = 0
   return speed

while True:
   speed = getSpeed()
   print("Speed: ", speed,"km/h\n")
   time.sleep(0.5)
