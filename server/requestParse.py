#!/usr/bin/env python
#
# requestParse.py
# Grant Wade - 30 March 2017
# Handles requests after being received from clients

import sys
import dbConnection
import triangulation
import request

class requestParse:
	def __init__(self):
		self.dbLink = dbConnection.dbConnection();
		self.triangulate = triangulation.triangulation();
		self.requests = request.request();

	def takeAction(self, object):
		returnRequest = False
		if object["Action"] == "clientCheckin":
			returnRequest = self.clientCheckin(object)
		
		return returnRequest
#		print >> sys.stderr, 'Action: "%s"', object["Action"]
	
	def clientCheckin(self, object):
		loc = self.triangulate.calculate(object["Parameters"]["WifiData"])

		print "Location Obj:"
		self.triangulate.printObj(loc)
		
		query = "SELECT DeviceID, BuzzerPending FROM DEVICE WHERE MAC=%s"
		values = (object["Parameters"]["MAC"])
		existingEntries = self.dbLink.queryDB(query, values)
		
		deviceID = 0
		buzzer = 0
		if len(existingEntries) > 0:
			deviceID = existingEntries[0][0]
			buzzer = existingEntries[0][1]

		if not not loc:
			if len(existingEntries) == 0:
				query = "INSERT INTO DEVICE (MAC, Title, Detail) values(%s, %s, %s)"
				values = (object["Parameters"]["MAC"], "No Title", "No Details")
				self.dbLink.queryDB(query, values)
				deviceID = self.dbLink.insert_id()
				print "Inserted ID: %s" % (deviceID)

			query = "UPDATE DEVICE SET LastSeenTime=now(), LastSeenLatitude=%s, LastSeenLongitude=%s, LastSeenAltitude=%s where DeviceID=%s"
			values = (loc["Latitude"], loc["Longitude"], loc["Altitude"], deviceID)
			self.dbLink.queryDB(query, values)
		
		query = "UPDATE DEVICE SET BuzzerPending=%s WHERE DeviceID=%s"
		values = (0, deviceID)
		self.dbLink.queryDB(query, values)
		
		returnValue = False
		if buzzer > 0:
			returnValue = self.requests.getBuzzerStart(buzzer)
		return returnValue
