# Digital-World-1D

## Database module

The database module requires that a `credentials` file containing the database configuration be placed in the same folder as it is.
A Database object should be instantiated with a room ID, after which, the attributes .Occupied and .Bookings may be used to set or get the room occupancy status and list of bookings respectively.

Example:

```
from database import Database

roomID = '1_413-01'     # Room ID for mini think tank

room = Database(roomID)

room.Occupied = True     # To set the occupancy of 1_413-01 to occupied
bookings = room.Bookings     # To get the list of bookings of 1_413-01
