#!/usr/bin/env python
#
# request.py
# Grant Wade - 21 April 2017
# Fetches requests that can be used to communicate with client

class request:
	def getBuzzerStart(self, seconds):
		request = {}
		request["ClientAction"] = "StartBuzzer"
		request["Parameters"] = {}
		request["Parameters"]["Seconds"] = seconds
		return request
		
