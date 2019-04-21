# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:04:08 2019

@author: Xu Liang
"""

import RPi.GPIO as GPIO
from gpiozero import DigitalInputDevice
import Adafruit_DHT
from smbus import SMBus
from sys import argv

class Hardware:

    def __init__(self, leds, pins):
        self.leds = leds
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.leds.values(), GPIO.OUT)

        self.HumidityTemperature = Adafruit_DHT.DHT11

        self.lightAddress = 0x23
        self.lightMode = 0x20
        self.Light = SMBus(1)

        GPIO.setup(self.pins['PIR'], GPIO.IN)
        GPIO.add_event_detect(self.pins['PIR'], GPIO.RISING, callback=self._onPIR)
        self.PIRON = False

        GPIO.setup(self.pins['Sound'], GPIO.IN)
        GPIO.add_event_detect(self.pins['Sound'], GPIO.RISING, callback=self._onSound)
        self.SOUNDON = False

    def _set(self, led, state):
    	pass

    def _getHumidityTemperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.HumidityTemperature, self.pins['HumidityTemperature'])
        # Consider using read_retry instead if consistently returning None
        return humidity, temperature

    def _getLight(self):
        reading = self.Light.read_i2c_block_data(self.lightAddress, self.lightMode)
        def convertToNumber(data):
            return (data[1] + (256 * data[0]))/1.2
        return convertToNumber(reading)

    def _onPIR(self, *args):
        self.PIRON = True

    def _getPIR(self):
        if self.PIRON:
            self.PIRON = False
            return 1
        else:
            return 0

    def _onSound(self, *args):
        self.SOUNDON = True

    def _getSound(self):
        if self.SOUNDON:
            self.SOUNDON = False
            return 1
        else:
            return 0

    def _getTemperature(self):
        reading = self.Temperature.read_word_data(self.temperatureAddress, 0) & 0xFFFF
        reading = ((reading << 8) & 0xFF00) + (reading >> 8)
        return (reading / 32.0) / 8.0


    def update(self, booked, occupied):
        self._set(self.leds['IN'], booked)
        self._set(self.leds['OUT'], occupied)
        # Sets the appropriate lighting/screen based on the booked and occupied status

    def download(self):
        data = {}
        data['Humidity'], data['Temperature'] = self._getHumidityTemperature()
        data['Light'] = self._getLight()
        data['Sound'] = self._getSound()
        data['PIR'] = self._getPIR()
        return data
        # Returns dictionary of sensors and their respective values



'''

Human Radar Sensor:
    from gpiozero import DigitalInputDevice
    inputPin = # input pin number
    radar = DigitalInputDevice(inputPin, pull_up=False, bounce_time=2.0)
    def detect():
        # Actions on detection
    radar.when_activated = detect

Humidity Sensor:
    import Adafruit_DHT
    sensor = Adafruit_DHT.DHT11
    inputPin = # input pin number

    humidity, temperature = Adafruit_DHT.read_retry(sensor, inputPin)
    # The above line retries up to 15 times with a 2 second wait to get a reading.
    # Can also use Adafruit_DHT.read(sensor, inputPin) for a single read attempt.

Light Sensor:
    import smbus
    device = 0x23
    mode = 0x20
    # refer to bh1750.py to change mode
    bus = smbus.SMBus(1)

    data = bus.read_i2c_block_data(device, mode)
    def convertToNumber(data):
        return (data[1] + (256 * data[0]))/1.2
    lightlevel = convertToNumber(data)

PIR Sensor:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    inputPin = # input pin number
    GPIO.setup(inputPin, GPIO.IN)

    motion = GPIO.input(inputPin)
    # High (== 1) when someone is detected, other wise Low (== 0)

Sound Sensor:
    import RPI.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    inputPin = # input pin number
    GPIO.setup(inputPin, GPIO.IN)
    def detect():
        # Actions on detection
    GPIO.add_event_detect(inputPin, GPIO.BOTH, bouncetime=300)
    GPIO.add_event_callback(inputPin, detect)
    # The above two lines detect when the input goes from High to Low.

Temperature Sensor:
    import smbus
    import sys
    device = 0x48
    if len(sys.argv):
        device = int(sys.argv[1], 16)
        # Check if another device address is specified.
    bus = smbus.SMBus(1)

    data = bus.read_word_data(device, 0) & 0xFFFF
    data = ((data << 8) & 0xFF00) + (data >> 8)
    temperature = (data / 32.0) / 8.0

'''
