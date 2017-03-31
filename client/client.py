import serverConnection
import request
import json
import time

#obj = {}
#obj["foo"] = []
#obj["foo"].append("bar")
#obj["foo"].append("baz")
#t = json.JSONEncoder().encode(obj)

#print(t)

#j = json.JSONDecoder().decode(t)

#print(j["foo"][0])


server = serverConnection.serverConnection()

requestController = request.request()

clientID = 1
#while True:

req = requestController.getCheckinRequest("NOWIFIDATA")
clientID += 1
server.addRequest(req)
server.sendRequests()
time.sleep(1)
