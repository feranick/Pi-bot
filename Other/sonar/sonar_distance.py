#!/usr/bin/env python3

#https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 

if sys.argv[1] == "1":
  # Front sonar
  type = "front"
  TRIG = 38
  ECHO = 40
elif sys.argv[1] == "2":
    # Left sonar
  type = "left"
  TRIG = 31
  ECHO = 33
elif sys.argv[1] == "3":
  # Right sonar
  type = "right"
  TRIG = 35
  ECHO = 37
else:
  # Back sonar
  type = "back"
  TRIG = 29
  ECHO = 32

pulse = 0.0002

pulse_start = 0.0
pulse_end = 0.0

print('Distance Measurement In Progress')

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

while True: 
  GPIO.output(TRIG, False)
  #print('Waiting For Sensor To Settle')
  time.sleep(0.1)

  GPIO.output(TRIG, True)
  time.sleep(pulse)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  #print('Duration',pulse_duration)
  distance = pulse_duration * 17150

  distance = round(distance,2)
  print("Distance (",type," sensor):",distance,"cm")

GPIO.cleanup()
