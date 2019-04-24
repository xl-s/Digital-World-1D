# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:04:03 2019

@author: Xu Liang
"""

from libdw import pyrebase
import json
import hashlib

class Database:
    
    def __init__(self, roomID):
        assert '.' not in roomID
        with open('credentials', 'r') as f:
            config = dict(json.load(f))
        self.roomID = roomID
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        
    def _transduce(self, pyredata):
        data = {}
        for dat in pyredata.each():
            data[dat.key()] = dat.val()
        return data
        # Translates pyredata object to dictionary

    def _push(self, directory, content):
        # Overwrite content only if it is a single value
        if hasattr(content, '__iter__'):
            self.db.child(directory).update(content)
        else:
            self.db.child(directory).set(content)

    def _pull(self, directory):
        # Return dictionary form or single value instead of pyreobject
        data = self.db.child(directory).get()
        if data.each():
            return self._transduce(data)
        else:
            return data.val()

    def _getHash(self, data):
        h = hashlib.sha256()
        h.update(bytes(data, encoding='utf-8'))
        return h.hexdigest()


    def _getOccupied(self):
        return self.pullAPP('OCCUPIED')

    def _setOccupied(self, occupancy):
        assert type(occupancy) == bool
        self.pushAPP(occupancy, 'OCCUPIED')

    def _getBookings(self):
        self.pushAPP(False, 'NEW')
        bookings = self.pullAPP('BOOKINGS')
        return [booking for booking in bookings.values()] if bookings else []
    
    def _setBookings(self, bookings):
        raise Exception('Please do not assign directly to the Bookings attribute. Instead, use the addBooking() method.')


    def pushRAW(self, content, directory=''):
        directory = '/RAWDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        self._push(directory, content)

    def pushAPP(self, content, directory=''):
        directory = '/APPDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        self._push(directory, content)

    def pushUSERS(self, content, directory=''):
        directory = '/USERS/{}'.format(directory.strip('/'))
        self._push(directory, content)

    def pullRAW(self, directory=''):
        directory = '/RAWDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        return self._pull(directory)
    
    def pullAPP(self, directory=''):
        directory = '/APPDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        return self._pull(directory)
    
    def pullUSERS(self, directory=''):
        directory = '/USERS/{}'.format(directory.strip('/'))
        return self._pull(directory)
        

    Bookings = property(_getBookings, _setBookings)
    Occupied = property(_getOccupied, _setOccupied)


    def addBooking(self, booking):
        self.db.child('/APPDATA/{}/BOOKINGS'.format(self.roomID)).push(booking)
        self.pushAPP(True, 'NEW')

    def cancelBooking(self, booking):
    	for k, v in self.pullAPP('BOOKINGS').items():
    		if v == booking:
    			self.db.child('/APPDATA/{}/BOOKINGS/{}'.format(self.roomID, k)).remove()
    			self.pushAPP(True, 'NEW')
    			return True
    	return False
    
    def login(self, username, password):
        p = self._getHash(password)
        u = self._getHash(username)
        pw = self.pullUSERS(u)
        return True if p == pw else False

    def register(self, username, password):
        p = self._getHash(password)
        u = self._getHash(username)
        if u not in self.pullUSERS().keys():
            self.pushUSERS({u:p})
            return True
        else:
            return False

    def new(self):
        return True if self.pullAPP('NEW') else False
    
    def saveRAW(self, filename='RAWDATA'):
        filename += '.json'
        data = self.pullRAW()
        jsondata = json.dumps(data)
        with open(filename, 'w+') as file:
            file.write(jsondata)
        # Use dict(json.load(file)) to convert .json to dictionary
        # It is also possible to operate on the json object itself.
    
    
