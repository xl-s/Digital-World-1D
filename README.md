## Database module

_Update 5 April: login() and register() added_

_.Bookings assignment changed such that bookings should be added with addBooking()_

The database module requires that a `credentials` file containing the database configuration be placed in the same folder as it is.
A Database object should be instantiated with the room ID as the argument.
The occupancy status and list of bookings of the room may be accessed using the `.Occupied` and `.Bookings` attributes. The occupancy status may also be changed directly from this attribute.
However, addition of bookings to the database should be done with the `addBooking()` method.

Example:

```
from database import Database

roomID = '1_413-01'     # Room ID for mini think tank

room = Database(roomID)

room.Occupied = True     # To set the occupancy of 1_413-01 to occupied
bookings = room.Bookings     # To get the list of bookings of 1_413-01

newbooking = {'start':(2019, 4, 5, 17, 0), 'end':(2019, 4, 5, 18, 0), 'user':'foo'}
room.addBooking(newbooking)     # To add a new booking

```

The methods `login(username, password)` and `register(username, password)` have been implemented for convenient and secure authentication with the database. `login()` returns True if the login data is valid, and `register()` may be used to enroll new sets of login data with the database. `register()` returns True if the login data has been successfully enrolled, or False if it was not enrolled (i.e. the username already exists).
