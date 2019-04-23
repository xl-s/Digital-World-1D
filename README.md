### Overview

The database module provides a simplified API for the upload and download of data from the firebase server. The hardware module condenses all the requisite Raspberry Pi hardware and sensor related operations into a single accessible module requiring only two methods to interface with the sensors and LED indicators.

Before use, a `credentials` file containing the database URL and firebase API key in JSON format should be placed in the same folder as the `database.py` file. All sensors should also be functioning and properly connected to the Raspberry Pi. No other configuration is required.

The database is compartmentalized into three sections: An `APPDATA` section that contains all information relevant for interaction between the mobile Kivy application and the Raspberry Pi program; a `RAWDATA` section which stores sensor information from each room; and a `USERS` section which contains user login information.

Note that all of the database module functions are designed to prevent deletion of any data from the database. Should you wish to remove any data, please contact your database administrator.

##### Raspberry Pi Program Setup

To begin the running the Raspberry Pi program, change the `ROOMID` variable of the `main.py` file to the appropriate room ID. Note that the room ID should not contain periods (`.`), but can contain underscores (`_`) and dashes (`-`). The `PINS` and `LEDS` dictionaries should also be changed as needed if a different pin map is being used than the default one. Then simply run the `main.py` program.

#### Database Module Usage

###### Setup

A Database object should first be instantiated with the room ID, a unique string identifier, as a parameter:

```python
from database import Database

ROOMID = '57_653A'    # Room ID for Block 57 Level 6 Group Study Room
room = Database(ROOMID)
```

The Database instance will then correspond to the specified room and its relevant dataset, and can be used accordingly.

##### Accessing and updating application information

The `Database.pushAPP(content, directory)` and `Database.pullAPP(directory)` methods may be used to directly update and retrieve information from the `APPDATA` section of the database respectively. However, all relevant application-side functions have been condensed into the following functions:

###### `Database.Occupied`

`Database.Occupied` is a property which represents the occupancy status of the room which the `Database` instance corresponds to. It may be directly read from or assigned to to obtain or change the occupancy status. The occupancy status is represented by a boolean value, and may either be `True` (occupied) or `False` (unoccupied).

```python
occupancy = room.Occupied    # Get the occupancy status of 57.653A
room.Occupied = False    # Set the occupancy status of 57.653A to unoccupied
```

###### `Database.Bookings`

`Database.Bookings` is a read-only property which contains the booking information of the room. The booking information is represented as a list of dictionaries containing three key-value pairs: the start date and time of the booking (`'start'`), with the date and time represented as a tuple of integers from the year to the minute; the end date and time of the booking (`'end'`), in the same format as `'start'`, and the user who made the booking (`'user'`), represented as a string.

```python
bookings = room.Bookings    # Get the bookings of 57.653A
room.Bookings = bookings + new_booking    # Bad usage (and will not do anything)
```

###### `Database.addBooking(new_booking)`

To append new bookings to the database, the `Database.addBooking(new_booking)` method should be used.

```python
new_booking = {'start':(2019, 4, 25, 15, 0),
              'end':(2019, 4, 25, 16, 0),
              'user':'Tom'}
room.addBooking(new_booking)    # Add a booking on 2019-04-25 from 3:00 pm to 4:00 pm
```

###### `Database.login(username, password)`

The `Database.login(username, password)` method takes in a username and password pair as input. It returns `True` if the username-password pair is valid based on the login information in `USERS`, and `False` otherwise.

###### `Database.register(username, password)`

`Database.register(username, password)` is used to add new username-password pairs to the `USERS` database. It returns `True` if the user information enrollment is valid, and `False` otherwise (i.e. there is already another user with the same username).

##### Accessing and updating sensor information

Similarly to the `APPDATA` section, `Database.pushRAW(content, directory)` and `Database.pullRAW(directory)` may be used to directly update and retrieve information from the `RAWDATA` section.

###### `Database.pushRAW(content, directory='')`

The `Database.pushRAW(content, directory='')` method may be used to update sensor information for the room. Sensor data should be written as a dictionary, with the timestamp of sensor reading as keys and a dictionary of each sensor and its reading as values. For normal use, the `directory` parameter should be left blank.

```python
reading_1 = {'Human':1,    # Readings made at 2019-04-25 2:48:02 pm
         'Humidity':58,
         'Light':148.3333,
         'PIR':0,
         'Sound':0,
         'Temperature':24}
reading_2 = {'Human':1,    # Readings made at 2019-04-25 2:54:47 pm
            'Humidity':55,
            'Light':155,
            'PIR':0,
            'Sound':0,
            'Temperature':24}
new_readings = {'2019-04-25-14-48-02':reading_1,
               '2019-04-25-14-54-47':reading_2}
room.pushRAW(new_readings)    # Appends both readings to the database
```

###### `Database.saveRAW(filename='RAWDATA')`

The `Database.saveRAW(filename='RAWDATA')` method pulls all the data from the `RAWDATA` database and saves it to a local JSON file.

#### Hardware Module Usage

###### Setup

A Hardware object should be instantiated with two parameters: `leds` and `pins`. `leds` is a dictionary of the output pin numbers of the `'IN'` and `'OUT'` LEDs, where the `'IN'` is assigned to the led(s) within the room, and `'OUT'` is assigned to the led(s) outside the room. `pins` is a dictionary of the input pin numbers, and should contain the pin numbers for the `'PIR'`, `'Sound'`, `'HumidityTemperature'`, and `'Human'` sensors.

```python
from hardware import Hardware

LEDS = {'IN':19, 'OUT':20}
PINS = {'PIR':25, 'Sound':24, 'HumidityTemperature':23, 'Human':18}
raspberry = Hardware(LEDS, PINS)
```

###### `Hardware.update(booked, occupied)`

The `Hardware.update(booked, occupied)` method is used to update the states of LED indicators inside and outside the room, based on the booking and occupancy status of the room. The `booked` and `occupied` parameters are both boolean values, indicating respectively whether the room is currently booked and occupied.

```python
booked = False
occupied = True
raspberry.update(booked, occupied)    
# Changes light outside to indicate that the room is currently occupied
# and light inside to indicate that the room is not booked at the moment
```

###### `Hardware.download()`

The `Hardware.download()` method may be used to obtain sensor readings from the connected sensors. It returns a dictionary containing the scalar measurement value of each sensor.

```python
reading = raspberry.download()
print(reading)
# Example Output: {'Human':1, 'Humidity':58, 'Light':148.3333, 'PIR':0, 'Sound':0, 'Temperature':25}
```
