#!/usr/bin/env python
#
# client.py
# Grant Wade - 30 March 2017
# main script to be run on client to handle timed checkins with server

import serverConnection
import wireless
import request
import json
import time

#obj = {}
#obj["foo"] = []
#obj["foo"].append("bar")
#obj["foo"].append("baz")
#t = json.JSONEncoder().encode(obj)

#print(t)

#j = json.JSONDecoder().decode(t)

#print(j["foo"][0])


server = serverConnection.serverConnection()

wl = wireless.wireless()

requestController = request.request()

clientID = 1
#while True:

wifiData = wl.scan()
wifiData = json.JSONEncoder().encode(wifiData)

req = requestController.getCheckinRequest(wifiData)
clientID += 1
server.addRequest(req)
server.sendRequests()
time.sleep(1)
