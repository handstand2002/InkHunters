import socket
import sys
import json
import requestParse

requestParser = requestParse.requestParse()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 9801)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()

	allData = ""
	try:
		print >>sys.stderr, 'connection from', client_address
	
		# Receive the data in small chunks and retransmit it
		while True:
			data = connection.recv(16)
			if data:
				allData += data
				connection.sendall(data)
			else:
#				print >>sys.stderr, 'no more data from', client_address
				print >>sys.stderr, 'All Data: "%s"', allData
				allRequests = json.JSONDecoder().decode(allData)
				for request in allRequests:
					requestParser.takeAction(request)
				break
										
	finally:
		# Clean up the connection
		connection.close()
