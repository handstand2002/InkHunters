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
