#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output
import re
import json


class wireless:
	def __init__(self):
		self.no_results = re.compile(r"wlan0\s+No scan results")
		self.quality = re.compile(r"(Address.*)|(Quality.*)")
		self.line1 = re.compile(r"[0-9A-f:]{17}")
		self.line2 = re.compile(r"\d{2}/\d{2}")
		self.line3 = re.compile(r"-\d+")
		self.qualityCalc = re.compile(r"(\d+)\/(\d+)")

	def scan(self):
		
		wifiData = []
		for i in range(1, 20):
			scanData = self.singleScan()
			for newAP in scanData:
				apExist = False
				for existAP in wifiData:
					if newAP["Address"] == existAP["Address"]:
						# Increment counter, Add to Quality and Signal
						existAP["NumPing"] += 1
						existAP["Quality"] += float(newAP["Quality"])
						existAP["Signal"] += float(newAP["Signal"])
						apExist = True
						break
				if apExist == False:
					newAP["Quality"] = float(newAP["Quality"])
					newAP["Signal"] = float(newAP["Signal"])
					newAP["NumPing"] = 1
					wifiData.append(newAP)
		for ap in wifiData:
			ap["Quality"] = ap["Quality"] / ap["NumPing"]
			ap["Signal"] = ap["Signal"] / ap["NumPing"]
			del ap["NumPing"]
#		print "Number of APs caught: %d" % (len(wifiData))
		return wifiData
	
	def singleScan(self):
		while True:
			output = check_output(["iwlist", "wlan0", "scan"])
			if self.no_results.search(output) is None:
				break

		inbetween = ''
		for line in output.splitlines():
			match = self.quality.search(line)
			if match:
				inbetween += (match.group(0)+"\n")     
		x = 0
		d = {}
		datum = []

		for line in inbetween.splitlines():
			match = self.line1.search(line)
			if match:
				d['Address'] = match.group(0)
			match = self.line2.search(line)
			if match:
				d['Quality'] = match.group(0)
				calcMatch = self.qualityCalc.match(d['Quality'])
				d['Quality'] = float(calcMatch.group(1)) / float(calcMatch.group(2)) * 100
			match = self.line3.search(line)
			if match:
				d['Signal'] = match.group(0)
				
				datum.append(d)
				d = {}
		return datum
