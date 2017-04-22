#!/usr/bin/env python
#
# server.py
# Grant Wade - 30 March 2017
# Primary script to be run to listen for requests from clients

import socket
import sys
import json
import requestParse
import request

requestParser = requestParse.requestParse()
requests = request.request()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.251', 9801)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()

	jsonDecoder = json.JSONDecoder()
	decodedRequests = []
	allData = ""
	clientRequests = []
	try:
		print >>sys.stderr, 'connection from', client_address

		# Receive the data in small chunks until a full json string is received
		while True:
			data = connection.recv(16)
#			print "Received '%s'" % (data)
			allData += data

			try:
				decodedRequests = jsonDecoder.decode(allData)
				clientRequests = []
				for request in decodedRequests:
					actionResponse = requestParser.takeAction(request)
					if not not actionResponse:
						clientRequests.append(actionResponse)
				break;
			except ValueError:
				finished = False

	finally:
#		decodedRequests.append(requests.getBuzzerStart(5))
		for request in clientRequests:
			decodedRequests.append(request)
		txt = json.JSONEncoder().encode(decodedRequests)
		connection.sendall(txt)
		# Clean up the connection
		connection.close()
