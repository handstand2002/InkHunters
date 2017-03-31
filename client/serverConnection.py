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
                self.sendData(jsonText)


        def sendData(self, data):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serverAddress = ('192.168.0.251', 9801)

                try:
                        print >> sys.stderr, 'connecting to %s:%s' % self.serverAddress
                        self.sock.connect(self.serverAddress)
                except:
                        print >> sys.stderr, "wasn't able to connect to %s:%s" % self.serverAddress
                        return

                try:
                        self.sock.sendall(data)

                        received = 0
                        expected = len(data)

                        while received < expected:
                                response = self.sock.recv(16)
                                received += len(response)
                finally:
                        print >> sys.stderr, 'closing socket'
                        self.sock.close()
