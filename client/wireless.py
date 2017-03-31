#!/usr/bin/env python
#
# iwlistparse.py
# Hugo Chargois - 17 jan. 2010 - v.0.1
# Parses the output of iwlist scan into a table
#
# Modified 30 March 2017 Grant Wade

import sys
import subprocess

class wireless:
	def __init__(self):
		self.interface = "wlan0"
# Here's a dictionary of rules that will be applied to the description of each
# cell. The key will be the name of the column in the table. The value is a
# function defined above.

		self.rules={"Name":self.get_name,
			"Quality":self.get_quality,
			"Channel":self.get_channel,
			"Encryption":self.get_encryption,
			"Address":self.get_address,
			"Signal":self.get_signal_level
		}

# You can choose which columns to display here, and most importantly in what order. Of
# course, they must exist as keys in the dict rules.
		self.columns=["Name","Address","Quality","Signal", "Channel","Encryption"]



	def scan(self):
		cells=[[]]
	        parsed_cells=[]

	        proc = subprocess.Popen(["iwlist", self.interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
	        out, err = proc.communicate()

	        for line in out.split("\n"):
	                cell_line = self.match(line,"Cell ")
	                if cell_line != None:
	                        cells.append([])
	                        line = cell_line[-27:]
	                cells[-1].append(line.rstrip())

		cells=cells[1:]

	        for cell in cells:
        	        parsed_cells.append(self.parse_cell(cell))
	        self.sort_cells(parsed_cells)
		return parsed_cells



# You can add or change the functions to parse the properties of each AP (cell)
# below. They take one argument, the bunch of text describing one cell in iwlist
# scan and return a property of that cell.

	def get_name(self, cell):
		return self.matching_line(cell,"ESSID:")[1:-1]

	def get_quality(self, cell):
		quality = self.matching_line(cell,"Quality=").split()[0].split('/')
		return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"

	def get_channel(self, cell):
		return self.matching_line(cell,"Channel:")

	def get_signal_level(self, cell):
	# Signal level is on same line as Quality data so a bit of ugly
	# hacking needed...
		return self.matching_line(cell,"Quality=").split("Signal level=")[1]


	def get_encryption(self, cell):
		enc=""
		if self.matching_line(cell,"Encryption key:") == "off":
			enc="Open"
		else:
			for line in cell:
				matching = self.match(line,"IE:")
			if matching!=None:
				wpa=self.match(matching,"WPA Version ")
				if wpa!=None:
					enc="WPA v."+wpa
		if enc=="":
			enc="WEP"
		return enc

	def get_address(self, cell):
		return self.matching_line(cell,"Address: ")


# Here you can choose the way of sorting the table. sortby should be a key of
# the dictionary rules.

	def sort_cells(self, cells):
		sortby = "Quality"
		reverse = True
		cells.sort(None, lambda el:el[sortby], reverse)


# Below here goes the boring stuff. You shouldn't have to edit anything below
# this point

	def matching_line(self, lines, keyword):
		"""Returns the first matching line in a list of lines. See match()"""
		for line in lines:
			matching=self.match(line,keyword)
			if matching!=None:
				return matching
		return None

	def match(self, line,keyword):
		"""If the first part of line (modulo blanks) matches keyword,
		returns the end of that line. Otherwise returns None"""
		line=line.lstrip()
		length=len(keyword)
		if line[:length] == keyword:
			return line[length:]
		else:
			return None

	def parse_cell(self, cell):
		"""Applies the rules to the bunch of text describing a cell and returns the
		corresponding dictionary"""
		parsed_cell={}
		for key in self.rules:
			rule=self.rules[key]
			parsed_cell.update({key:rule(cell)})
		return parsed_cell

	def print_table(self, table):
		widths=map(max,map(lambda l:map(len,l),zip(*table))) #functional magic

		justified_table = []
		for line in table:
			justified_line=[]
			for i,el in enumerate(line):
				justified_line.append(el.ljust(widths[i]+2))
			justified_table.append(justified_line)
		
		for line in justified_table:
			for el in line:
				print el,
			print

	def print_cells(self, cells):
		table=[self.columns]
		for cell in cells:
			cell_properties=[]
			for column in self.columns:
				cell_properties.append(cell[column])
			table.append(cell_properties)
		self.print_table(table)
	
