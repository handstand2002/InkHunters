#!/usr/bin/env python
#
# triangulation.py
# Grant Wade - 30 March 2017
# Calculates the 

import dbConnection
import math
import json
import sys

class triangulation:
	def __init__(self):
		self.dbLink = dbConnection.dbConnection();

	def printObj(self, obj, level=1):
		print json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
		

	def calculate(self, data):
		data = json.JSONDecoder().decode(data)
		
		APsInDB = []
		# Print each of the APs data
		for AP in data:
			query = "SELECT * FROM APDETAIL where MAC=%s"
			addressHex = "0x" + AP["Address"].replace(":", "")
			values = (int(addressHex,0) )
			res = self.dbLink.queryDB(query, values)
			if not not res:
				APDetail = {}
				APDetail["Client"] = AP
				APDetail["DB"] = res[0]
				APsInDB.append(APDetail)

		latitude = 0
		longitude = 0
		altitude = 0
		numberNodes = 0
		totalDistance = 0
			
		for AP in APsInDB:
			print json.JSONEncoder().encode(AP)
			self.printObj(AP)
#			print "APs:",AP
			AP["Client"]["Quality"] = AP["Client"]["Quality"].replace(" ", "")
			AP["Client"]["Quality"] = float(AP["Client"]["Quality"])/100

			AP["Client"]["Signal"] = float(AP["Client"]["Signal"].replace(" dBm", ""))
			AP["Client"]["Signal"] = (AP["Client"]["Signal"] + 100) / 90
                        #signal scale is from -10 to -100

			signalDist = 1-(AP["Client"]["Signal"] * AP["Client"]["Quality"])
			print "Signal Distance: ", signalDist

			latitude += AP["DB"][4] * signalDist
			longitude += AP["DB"][5] * signalDist
			altitude += AP["DB"][6] * signalDist
			numberNodes += 1
			totalDistance += signalDist

		print "Lat total: ", latitude
		print "Lng total: ", longitude
		print "Alt total: ", altitude
		print "Total Dist: " , totalDistance
		print "numNodes: ", numberNodes
		print 
		latitude /= totalDistance
		longitude /= totalDistance
		altitude /= totalDistance
		
		print "Lat: ", latitude
		print "Lng: ", longitude
		print "Alt: ", altitude

		#dummy output
		output = {}
		output["Latitude"] = 15
		output["Longitude"] = 25
		output["Altitude"] = 2500

		return output

	def doCalc(self, APDataArray):
		degPerFootLat = .00000274123
		degPerFootLong = 0.000003978864273
		if len(APDataArray) < 4:
			return []
		
		offset = [APDataArray[0][0], APDataArray[0][1], APDataArray[0][2]]
		for key in APDataArray:
			for i in range(0,2):
				key[i] -= offset[i]
			key[0] /= degPerFootLat
			key[1] /= degPerFootLong
		r1 = APDataArray[0][3]
		r2 = APDataArray[1][3]
		r3 = APDataArray[2][3]
		r4 = APDataArray[3][3]
		d = APDataArray[1][1]
		i = APDataArray[2][1]
		j = APDataArray[2][0]

		x = (pow(r1,2) - pow(r2,2)+pow(d,2))/(2*d)
		y = ((pow(r1,2) - pow(r3,2) + pow(i,2) + pow(j,2) )/(2*j)) - ((i/j)*x)

		xDeg = x*degPerFootLong + offset[1]
		yDeg = y*degPerFootLat + offset[0]

		z = math.sqrt(pow(r1,2) - pow(x,2) -pow(y,2) )

		distToP41 = math.sqrt(pow(x - APDataArray[3][1],2) + pow(y - APDataArray[3][0],2) + pow(z - APDataArray[3][2],2))
		distToP42 = math.sqrt(pow(x - APDataArray[3][1],2) + pow(y - APDataArray[3][0],2) + pow((z*-1) - APDataArray[3][2],2))

		diff1 = abs(distToP41 - r4)
		diff2 = abs(distToP42 - r4)
		if diff1 < diff2:
		        z = offset[2] + z
		else:
		        z = offset[2] - z
		print "X,Y,Z: ", xDeg, ", ", yDeg, ", ", z, "ft"

