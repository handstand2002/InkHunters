from uuid import getnode as get_mac

class request:

	def getCheckinRequest(self, wifiData):
		mac = get_mac()

		request = {}
		request["Action"] = "clientCheckin"
		request["Parameters"] = {}
		request["Parameters"]["MAC"] = mac
		request["Parameters"]["WifiData"] = wifiData
		return request
