#doCalc()
#       APDataArray[
#                       AP[
#                               <Latitude(+- deg)>
#                               <Longitude(+- deg)>
#                               <Altitude(ft)>
#                               <DistanceToAP(ratio)>
#                       ]
#                       ... (4x APs min)
#               ]

import triangulation

t = triangulation.triangulation()

data = []

AP1 = []
AP1.append(46.717108333333300  )		# Latitude
AP1.append(-116.971675000000000  )	# Longitude
AP1.append(2591)			# Altitude
AP1.append(708.04)			# Distance
data.append(AP1)

AP2 = []
AP2.append(46.716822222222200  )
AP2.append(-116.973625000000000  )
AP2.append(2585)
AP2.append(712.57)
data.append(AP2)

AP3 = []
AP3.append(46.717166666666700  )
AP3.append(-116.975325000000000  )
AP3.append(2586)
AP3.append(790.18)
data.append(AP3)

AP4 = []
AP4.append(46.718202777777800  )
AP4.append(-116.974725000000000  )
AP4.append(2598)
AP4.append(438.13)
data.append(AP4)

res = t.doCalc(data)

t.printObj(res)

t.printObj(data)

#t.rotatePointAboutOrigin(10, 0, 75);
#t.rotatePointAboutOrigin(10, 10, 90);
#t.rotatePointAboutOrigin(0, 10, 90);
#t.rotatePointAboutOrigin(-10, 10, 90);
#t.rotatePointAboutOrigin(-10, 0, 90);
#t.rotatePointAboutOrigin(-10, -10, 90);
#t.rotatePointAboutOrigin(0, -10, 90);
#t.rotatePointAboutOrigin(10, -10, 90);
