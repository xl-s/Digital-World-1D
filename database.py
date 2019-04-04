# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:04:03 2019

@author: Xu Liang
"""

from libdw import pyrebase
import json

class Database:

    with open('credentials', 'r') as f:
        config = dict(json.load(f))
    
    def __init__(self, roomID):
        self.roomID = roomID
        firebase = pyrebase.initialize_app(self.config)
        self.db = firebase.database()
        
    def transduce(self, pyredata):
        data = {}
        for dat in pyredata.each():
            data[dat.key()] = dat.val()
        return data
        
    def _push(self, directory, content):
        self.db.child(directory).set(content)
    
    def _pull(self, directory):
        return self.db.child(directory).get()
    
    def pushRAW(self, content, directory=''):
        directory = '/RAWDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        existing = self.transduce(self.pullRAW)
        existing.update(content)
        self._push(directory, existing)
    
    def pushAPP(self, content, directory=''):
        directory = '/APPDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        self._push(directory, content)
        
    def pullRAW(self, directory=''):
        directory = '/RAWDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        return self._pull(directory)
    
    def pullAPP(self, directory=''):
        directory = '/APPDATA/{}/{}'.format(self.roomID, directory.strip('/'))
        return self._pull(directory)
    
    def _getBookings(self):
        return self.pullAPP('BOOKINGS').val()
    
    def _setBookings(self, bookings):
        self.pushAPP(bookings, 'BOOKINGS')
    
    def _getOccupied(self):
        return self.pullAPP('OCCUPIED').val()
    
    def _setOccupied(self, occupancy):
        self.pushAPP(occupancy, 'OCCUPIED')
        
    Bookings = property(_getBookings, _setBookings)
    Occupied = property(_getOccupied, _setOccupied)
    
    def saveRAW(self, filename='RAWDATA'):
        filename += '.json'
        data = self.transduce(self.pullRAW())
        jsondata = json.dumps(data)
        with open(filename, 'w+') as file:
            file.write(jsondata)
        # Use dict(json.load(file)) to convert .json to dictionary
        # It is also possible to operate on the json object itself.
    
    
    
