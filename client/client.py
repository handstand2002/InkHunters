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
import requestParse

server = serverConnection.serverConnection()

wl = wireless.wireless()

requestController = request.request()
requestParser = requestParse.requestParse()

clientID = 1
while True:

	wifiData = wl.scan()
	wifiData = json.JSONEncoder().encode(wifiData)

	req = requestController.getCheckinRequest(wifiData)
	clientID += 1
	server.addRequest(req)
	response = server.sendRequests()

	for action in response:
		if "ClientAction" in action:
			requestParser.takeAction(action)
	time.sleep(10)
