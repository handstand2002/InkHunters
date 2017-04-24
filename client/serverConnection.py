#!/usr/bin/env python
#
# serverConnection.py
# Grant Wade - 30 March 2017
# Connects to the server, for object communication

import socket
import sys
import json

class serverConnection(object):
        def __init__(self):
                self.requestArray = []


        def addRequest(self, object):
                self.requestArray.append(object)


        def sendRequests(self):
                jsonText = json.JSONEncoder().encode(self.requestArray)
                self.requestArray = []
                resp = self.sendData(jsonText)
#		print "Response: "
#		print json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': '))
		return resp


        def sendData(self, data):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serverAddress = ('192.168.0.251', 9801)

                try:
                        print >> sys.stderr, 'connecting to %s:%s' % self.serverAddress
                        self.sock.connect(self.serverAddress)
                except:
                        print >> sys.stderr, "wasn't able to connect to %s:%s" % self.serverAddress
                        return

		jsonDecoder = json.JSONDecoder()
		decodedResponse = []
                try:
                        self.sock.sendall(data)

#                        received = 0
#                        expected = len(data)
			finishedResponse = False
			fullResponse = ""
                        while True:
                                response = self.sock.recv(16)
				fullResponse += response
				try:
					decodedResponse = json.JSONDecoder().decode(fullResponse)
					break
				except ValueError:
					temp = False
                finally:
                        print >> sys.stderr, 'closing socket'
                        self.sock.close()
		return decodedResponse
