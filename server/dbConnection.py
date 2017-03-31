#!/usr/bin/env python
#
# dbConnection.py
# Grant Wade - 30 March 2017
# Handles connection with the mysql database

import MySQLdb

class dbConnection:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="capstone", db="INKHUNTERS")

	def queryDB(self, query, values = []):
		self.link = self.db.cursor()
		self.link.execute(query, values)
		self.db.commit()
		
		output = []
		for row in self.link:
			output.append(row)

		self.link.close()
		return output
