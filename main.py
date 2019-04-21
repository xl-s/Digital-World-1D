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
PINS = {'PIR':25, 'Sound':24, 'HumidityTemperature':23}
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
    data = raspberry.download()
    RAW = {now.strftime('%Y-%m-%d-%H-%M-%S'):data}
    occupied = checkOccupied(data)
    # Retrieve bookings, if there are any new ones
    if room.new():
        bookings = room.Bookings
    # Check if room is currently being booked. NOTE: Bookings should be made up to the minute!
    booked = checkBooked(bookings, (now.year, now.month, now.day, now.hour, now.minute))
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
    raspberry = Hardware(LEDS, PINS)
    bookings = room.Bookings


if __name__ == '__main__':
    init()
    loop()


'''

Database usage structure:
    db.child('/') accesses root. Applying .get() returns a dictionary-like object
    with .key() and .val().
    So to find the value of '/RAWDATA/DATA', use db.child('RAWDATA').child('DATA').get().val().
    Use db.child().child().set() to set a value in a subfolder.
    For example, to write '/RAWDATA/DATA' as 10, use db.child('RAWDATA').child('DATA').set(10).
    

Save time-series data (RAWDATA) separately from data required by app (APPDATA).
APPDATA should be updated regularly (same refresh rate as RAWDATA is collected?)
RAWDATA can be stored using .write() inside the raspberry itself, or we could just store
within the program itself. However, still good to keep a local backup.
Periodically push the data to the database at certain time intervals - but not
too often so that the database doesn't get bogged down (probably not a major
concern but still).
The information contained within APPDATA will also be used to update the lights
(and screen, if any), so that we do not need to work with RAWDATA on the I/O
side. However, we will be needing RAWDATA for later improvement on detection
accuracy.

Sensors:
    - PIR (motion)
    - Humidity
    - Sound
    - ?
    - ?
    
PIR will be used as the main method to determine whether there are any people
in the room first. We can place a camera within the room / door to determine
whether there are any people inside? Otherwise PIR may not be 100% accurate itself.
Once we have maybe a week's data as well as the accurate data on the room occupancy,
we can then proceed with building a kNN model and see if it can determine the 
room occupancy more accurately (as compared to using the PIR sensor itself).
If so, we can implement it.
The second data analysis part would be predicting whether or not the room will
be occupied at a certain time and day - for this, we assume that the main factors
affecting whether this is the case are only day of week and the time. Or we can
do some data mining to see if there are other variables (but abit out of scope).

Components of APPDATA:
    /APPDATA:
        /ROOM1ID:
            DESCR - Static string describing the room - set manually
            OCCUPIED - Boolean, True if occupied
            BOOKINGS - Dictionary containing time of bookings
        /ROOM2ID:
            DESCR - Static string describing the room - set manually
            OCCUPIED - Boolean, True if occupied
            BOOKINGS - Dictionary containing time of bookings
        /...

Components of RAWDATA:
    /RAWDATA:
        /ROOM1ID:
            /Timestamp:
                ACCOCCUPIED - Boolean, accurate occupancy status. Otherwise None
                PIR - Float, PIR sensor data
                HUMIDITY - Float, humidity sensor data
                SOUND - Float, sound sensor data
                ...
                (The assumption is that all the sensors give scalar data;
                otherwise this may be changed relatively easily)
            /...
        /ROOM2ID:
            /Timestamp:
                ACCOCCUPIED - Boolean, accurate occupancy status. Otherwise None
                PIR - Float, PIR sensor data
                HUMIDITY - Float, humidity sensor data
                SOUND - Float, sound sensor data
                ...
            /...
        /...

Note that if there are storage / upload limits on firebase, we can periodically
download the data to a local storage database or lower the data update period.
Storage limit: 1 GB

On the hardware side, we assume that there are two lights we need to control:
The light inside (INLIGHT), which indicates whether the room is booked, and
the light outside (OUTLIGHT), which indicates whether the room is occupied.
The lights can be either RED (Booked/Occupied) or GREEN.
There may also be a third light located outside which also reflects the
booking status of the room - this may be treated to be the same as INLIGHT.

Code structure:
    main.py (this one) - handles the overall system, transduces inputs and outputs
    between app, sensors and hardware.
    
    hardware.py - handles input and output of hardware (i.e. sensors), as well as
    the lights.
    
    database.py - handles upload and download of data from firebase
    
    hardware and database will each contain a hardware and database class.
    These class objects will perform all of the necessary functions under
    their jurisdiction.
    
Each raspberry (and therefore each room) will have the program, distinguished by their
unique ROOMID. This should be the only difference between the code for each raspberry.


'''
