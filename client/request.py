#!/usr/bin/env python
#
# request.py
# Grant Wade - 30 March 2017
# Fetches requests that can be used to communicate with server

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
