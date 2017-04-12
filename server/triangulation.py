#!/usr/bin/env python
#
# triangulation.py
# Grant Wade - 30 March 2017
# Calculates the intersection point of 4 spheres, input into calculate() as a json object
# 		[
#			{
#				Address: <MACAddress of AP>
#				Quality: <% quality as int>
#				Signal: <Signal strength (in dBm)>				
#			},
#			{
#				Address: <MACAddress of AP 2>
#				Quality: <% quality as int>
#				Signal: <Signal strength (in dBm)>				
#			},
#			...
#		]

from __future__ import division
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
		data = []

#"DB": [
#            35,
 #           89417479060,
  #          "nothing",
   #         "Nowhere",
    #        -48.0,
     #       -117.0,
      #      2000
       # ]

		for AP in APsInDB:
			thisAP = []
			thisAP.append(AP["DB"][4])
			thisAP.append(AP["DB"][5])
			thisAP.append(AP["DB"][6])
			AP["Client"]["Quality"] = float(AP["Client"]["Quality"])/100

#			AP["Client"]["Signal"] = float(AP["Client"]["Signal"].replace(" dBm", ""))
			AP["Client"]["Signal"] = (float(AP["Client"]["Signal"]) + 100) / 90
                        #signal scale is from -10 to -100

			signalDist = 1-(AP["Client"]["Signal"] * AP["Client"]["Quality"])
			AP["Client"]["DistanceRatio"] = signalDist
			
			data.append(thisAP)

		output = self.doCalc(data)
		print "Number of registered wifi received: %d" % len(data)
#		self.printObj(APsInDB)
		
		#dummy output
#		output = {}
#		output["Latitude"] = 15
#		output["Longitude"] = 25
#		output["Altitude"] = 2500

		return output


#doCalc()
#	APDataArray[
#			AP[
#				<Latitude(+- deg)>
#				<Longitude(+- deg)>
#				<Altitude(ft)>
#				<DistanceToAP(ratio)>
#			]
#			... (4x APs min)
#		]
	def doCalc(self, APDataArrayOrig):
		if len(APDataArrayOrig) < 4:
			return {};

		# Make a copy of the data, so not messing with the original
		APDataArray = json.JSONDecoder().decode(json.JSONEncoder().encode(APDataArrayOrig))

		#print "Original Data"
		#self.printObj(APDataArray)

		# Constants for around Latitude 46 43' N
		degPerFootLat = .00000274123
		degPerFootLong = 0.000003978864273
		#		 0.000004
		#		 0.0000039937
		# 365221 feet per degree at equator
		degPerFootLong = 1/ (math.cos(math.radians(APDataArray[0][0])) * 365221)
#		print "Degrees per foot longitude: %.10f" % degPerFootLong

		# Create offset, so we can move the first point to (0,0,0)
		offset = [APDataArray[0][0], APDataArray[0][1], APDataArray[0][2]]
		for key in APDataArray:
			# Move all points to relative to (0,0,0)
			for i in range(0,3):
				key[i] -= offset[i]
			# Convert lat/long degrees to feet relative to first point
			key[0] /= degPerFootLat
			key[1] /= degPerFootLong

		#Create easier-to-use variables
		x1 = APDataArray[0][1]
		x2 = APDataArray[1][1]
		x3 = APDataArray[2][1]
		x4 = APDataArray[3][1]
		y1 = APDataArray[0][0]
		y2 = APDataArray[1][0]
		y3 = APDataArray[2][0]
		y4 = APDataArray[3][0]
		z1 = APDataArray[0][2]
		z2 = APDataArray[1][2]
		z3 = APDataArray[2][2]
		z4 = APDataArray[3][2]
		r1 = APDataArray[0][3]
		r2 = APDataArray[1][3]
		r3 = APDataArray[2][3]
		r4 = APDataArray[3][3]

#		print "circle formulas After converting to feet and doing offset, before rotating:"
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x1, y1, r1)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x2, y2, r2)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x3, y3, r3)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x4, y4, r4)

#Rotate all points until the 2nd point is on the x axis
		degOfPoint2 = self.getDegreeOfPoint(x2, y2)
		degOfPoint2 *= -1
		p2 = self.rotatePointAboutOrigin(x2, y2, degOfPoint2)
		x2 = p2[0]
		y2 = p2[1]

		p3 = self.rotatePointAboutOrigin(x3, y3, degOfPoint2)
		x3 = p3[0]
		y3 = p3[1]

		p4 = self.rotatePointAboutOrigin(x4, y4, degOfPoint2)
		x4 = p4[0]
		y4 = p4[1]
		
#		circleFormula1 = "(x - (" + x1 + ") )^2 + (y - (" + y1 + ") )^2 = (" + r1 + ")^2"
#		print "circle formulas after rotation:"
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x1, y1, r1)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x2, y2, r2)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x3, y3, r3)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x4, y4, r4)

		toSqRt = -1
		attempt = 0
		while (toSqRt < 0) and (attempt < 1000):
			x = (pow(r1,2) - pow(r2,2) + pow(x2,2) ) / (2 * x2)
			y = ((pow(r1,2) - pow(r3,2) + pow(x3,2) + pow(y3,2) )/(2*y3)) - ((x3/y3)*x)

		
			toSqRt = pow(r1,2) - pow(x,2) - pow(y,2)
	#		print "trying to square root (%.4f)" % toSqRt
	#		print "Running equation: sqrt(pow(%.4f, 2) -pow(%.4f, 2) -pow(%.4f, 2) )" % (r1, x, y)
	#		print "Running equation: sqrt( (%.4f) - (%.4f) - (%.4f) )" % (pow(r1,2), pow(x,2), pow(y,2))
			
			factor = .00001
			if toSqRt < 0:
				r1 *= (1+factor)
				r2 *= (1+factor)
				r3 *= (1+factor)
				r4 *= (1+factor)
			attempt += 1

#		print "circle formulas after making bigger:"
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x1, y1, r1)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x2, y2, r2)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x3, y3, r3)
#		print "	(x - (%.4f) )^2 + (y - (%.4f) )^2 = (%.4f)^2" % (x4, y4, r4)

		if (toSqRt < 0) and (toSqRt > -5):
			toSqRt = 0
		if (toSqRt >= 0):
			z = math.sqrt( toSqRt )
		else:
			z = 0

#		if attempt > 1:
#			z = 0

#		print "Found (x,y,z) = (%.2f, %.2f, %.2f) after %d attempts" % (x, y, z, attempt)

#		Rotate back to original positions
		degOfPoint2 *= -1
		p2 = self.rotatePointAboutOrigin(x2, y2, degOfPoint2)
		x2 = p2[0]
		y2 = p2[1]

		p3 = self.rotatePointAboutOrigin(x3, y3, degOfPoint2)
		x3 = p3[0]
		y3 = p3[1]

		p4 = self.rotatePointAboutOrigin(x4, y4, degOfPoint2)
		x4 = p4[0]
		y4 = p4[1]

		destP = self.rotatePointAboutOrigin(x, y, degOfPoint2)
		x = destP[0]
		y = destP[1]

#		print "End result, before offsetting: (%.2f, %.2f, %.2f)" % (x, y, z)

#		Return to original offset
		xDeg = x*degPerFootLong + offset[1]
		yDeg = y*degPerFootLat + offset[0]
		
		distToP41 = math.sqrt(pow(x - APDataArray[3][1],2) + pow(y - APDataArray[3][0],2) + pow(z - APDataArray[3][2],2))
		distToP42 = math.sqrt(pow(x - APDataArray[3][1],2) + pow(y - APDataArray[3][0],2) + pow((z*-1) - APDataArray[3][2],2))

		diff1 = abs(distToP41 - r4)
		diff2 = abs(distToP42 - r4)
		if diff1 < diff2:
		        z = offset[2] + z
		else:
		        z = offset[2] - z
		
#		print "(x, y, z) = (%f, %f, %f)" % (xDeg, yDeg, z)
		return {"Latitude": yDeg, "Longitude":xDeg, "Altitude":z}


	def rotatePointAboutOrigin(self, x, y, degrees):
		vectorLength = self.getDistanceFromOrigin(x, y)
		origDegree = self.getDegreeOfPoint(x, y)
		newDegree = (origDegree + degrees + 360) % 360
#		print "old degree: %f, New Degree: %f" % (origDegree, newDegree)
		newX = vectorLength * round(math.cos(math.radians(newDegree)),15)
		newY = vectorLength * round(math.sin(math.radians(newDegree)),15)
#		print "Old pos: (%.2f, %.2f)	new pos: (%.2f, %.2f)" % (x, y, newX, newY)
		return [newX, newY]

	def getDistanceFromOrigin(self, x, y):
		return math.sqrt( pow(x,2) + pow(y,2) )

	def getQuadrantOfPoint(self, x, y):
		quadrant = 1
		if (y > 0) and (x <= 0):
			quadrant = 2
		elif (y <= 0) and (x < 0):
			quadrant = 3
		elif (y < 0) and (x >= 0):
			quadrant = 4
		return quadrant
		

	def getDegreeOfPoint(self, x, y):
		quadrant = self.getQuadrantOfPoint(x, y)

		deg = 0
		if x == 0:
			if y > 0:
				deg = 90
			elif y < 0:
				deg = 270
		else:
			deg = math.degrees(math.atan(y/x))
			if (quadrant == 2) or (quadrant == 3):
				deg = 180 + deg
			elif quadrant == 4:
				deg = 360 + deg

#		print "point(%d, %d) is in Q%d and has %f degrees" % (x, y, quadrant, deg)
		return deg
