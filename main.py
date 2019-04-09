# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:08:16 2019

@author: Xu Liang
"""

from database import Database
from hardware import Hardware
from time import sleep, strftime
from datetime import datetime

#NOTE: Modules containing libdw should be imported before Kivy!


ROOMID = '1_413-01'
LEDS = {}

period = 1
bookings = {}


def before(first, second):
    # Returns true if first is before second (or they are the same)
    for k, val in enumerate(first):
        if second[k] < val:
            return False
        if val < second[k]:
            return True
    return True


def checkBooked(books, now):
    # Condition: Starts before and ends after now.
    for booking in books:
        print(booking)
        if before(booking['start'], now) and before(now, booking['end']):
            return True
    return False


def checkOccupied(data):
    pass


def main():
    global bookings
    # Get and process timestamp
    now = datetime.now()
    # Retrieve (and process) sensor data - Hardware side
    data = raspberry.download() ###
    RAW = {now.strftime('%Y-%m-%d-%H-%M-%S'):data}
    occupied = checkOccupied(data) ###
    # Retrieve bookings, if there are any new ones
    if room.new():
        bookings = room.Bookings
    # Check if room is currently being booked. NOTE: Bookings should be made up to the minute!
    booked = checkBooked(bookings, (now.year, now.month, now.day, now.hour, now.minute)) ###
    # NOTE: Ensure that app side checks for booking conflicts.
    # Update lights as appropriate
    raspberry.update(booked, occupied) ###
    # Update database with occupancy
    room.Occupied = occupied
    # Update database with raw data
    room.pushRAW(RAW)


def loop():
    while True:
        main()
        sleep(period)


def init():
    global room
    global raspberry
    global bookings
    room = Database(ROOMID)
    raspberry = Hardware(LEDS)
    bookings = room.Bookings


if __name__ == '__main__':
    init()
    loop()
