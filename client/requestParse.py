#!/usr/bin/env python
#
# requestParse.py
# Grant Wade - 23 April 2017
# Handles requests after being received from server

import sys
import audio_ping

class requestParse:
	def __init__(self):
		self.buzzer = audio_ping.Buzzer()

	def takeAction(self, object):
		if object["ClientAction"] == "StartBuzzer":
			self.startBuzzer(object["Parameters"]["Seconds"])

	def startBuzzer(self, seconds):
		self.buzzer.playAlert2(seconds)
