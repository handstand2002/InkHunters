# -*- coding: utf-8 -*-
# Original Code by Dipto Pratyaksa
# Code can be found at:
#http://www.linuxcircle.com/2015/04/12/how-to-play-piezo-buzzer-tunes-on-raspberry-pi-gpio-with-pwm/

# utf encoding added to make code python 2.7 compatible
# gpio pin changed from original


import RPi.GPIO as GPIO   #import the GPIO library
import time               #import the time library
import math

class Buzzer(object):
 def __init__(self):
  GPIO.setwarnings(False)  
  GPIO.setmode(GPIO.BCM)  
  self.buzzer_pin = 13 #set to GPIO pin 13
  GPIO.setup(self.buzzer_pin, GPIO.IN)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
#  print("buzzer ready")

 def __del__(self):
  class_name = self.__class__.__name__
#  print (class_name, "finished")

 def buzz(self,pitch, duration):   #create the function “buzz” and feed it the pitch and duration)
 
  if(pitch==0):
   time.sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave  
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):    #start a loop from 0 to the variable “cycles” calculated above
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

 def playAlert2(self, seconds):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0
  lowFreq = 100
  highFreq = 900
  totalTime = 1
  currentTime = 0
  timeInterval = .01
  while currentTime < seconds:
   freq = math.sin(math.pi*currentTime/totalTime)*(highFreq-lowFreq)+lowFreq
   self.buzz(freq, timeInterval)
   currentTime += timeInterval
  GPIO.setup(self.buzzer_pin, GPIO.IN)  

 def playAlert(self):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0
  duration = .5
  totalDuration = 0
  while totalDuration < 60:
   self.buzz(587, .5)
   self.buzz(392, .5)
   totalDuration += 1
  GPIO.setup(self.buzzer_pin, GPIO.IN)

#if __name__ == "__main__":
#  a = input("Enter Tune number 1-5:")
#  buzzer = Buzzer()
#  buzzer.play(int(a))
#  buzzer.playAlert()
