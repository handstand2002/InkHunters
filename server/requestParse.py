import sys

class requestParse:

	def takeAction(self, object):
		print >> sys.stderr, 'Action: "%s"', object["Action"]
