#!/usr/bin/env python
#
# requestParse.py
# Grant Wade - 30 March 2017
# Handles requests after being received from clients

import sys
import dbConnection
import triangulation

class requestParse:
	def __init__(self):
		self.dbLink = dbConnection.dbConnection();
		self.triangulate = triangulation.triangulation();

	def takeAction(self, object):
		if object["Action"] == "clientCheckin":
			self.clientCheckin(object)
#		print >> sys.stderr, 'Action: "%s"', object["Action"]
	
	def clientCheckin(self, object):
		loc = self.triangulate.calculate(object["Parameters"]["WifiData"])

		query = "SELECT DeviceID FROM DEVICE WHERE MAC=%s"
		values = (object["Parameters"]["MAC"])
		existingEntries = self.dbLink.queryDB(query, values)
		if len(existingEntries) == 0:
			query = "INSERT INTO DEVICE (MAC, Title, Detail) values(%s, %s, %s)"
			values = (object["Parameters"]["MAC"], "No Title", "No Details")
			self.dbLink.queryDB(query, values)

		query = "UPDATE DEVICE SET LastSeenTime=now(), LastSeenLatitude=%s, LastSeenLongitude=%s, LastSeenAltitude=%s where DeviceID=%s"
		values = (loc["Latitude"], loc["Longitude"], loc["Altitude"], existingEntries[0][0])
		self.dbLink.queryDB(query, values)
