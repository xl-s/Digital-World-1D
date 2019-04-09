# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:04:08 2019

@author: Xu Liang
"""

#import RPi.GPIO as GPIO

class Hardware:

    def __init__(self, leds):
        self.leds = leds
        GPIO.setup(self.leds.values(), GPIO.OUT)

    def _set(self, led, state):
    	pass

    def update(self, booked, occupied):
        self._set(self.leds['IN'], booked)
        self._set(self.leds['OUT'], occupied)
        # Sets the appropriate lighting/screen based on the booked and occupied status

    def download(self):
        pass
        # Returns dictionary of sensors and their respective values