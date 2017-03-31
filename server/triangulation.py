#!/usr/bin/env python
#
# triangulation.py
# Grant Wade - 30 March 2017
# Calculates the 

import dbConnection
import json
import sys

class triangulation:
	def __init__(self):
		self.dbLink = dbConnection.dbConnection();

	def calculate(self, data):
		data = json.JSONDecoder().decode(data)
		
		# Print each of the APs data
		for AP in data:
			print >>sys.stderr, "AP: ", AP
			
		#dummy output
		output = {}
		output["Latitude"] = 15
		output["Longitude"] = 25
		output["Altitude"] = 2500

		return output
