#!/usr/bin/python
"""
Created on Tue Feb 17 21:52:17 2015

@author: prenato
"""

from pysphere import VIServer
server = VIServer()

server.connect("http://design-vc5-01.cisco.com/mob/?moid=ServiceInstance&method=retrieveContent", "svl-icf-vc.gen", "Cisco123!")

print server.get_server_type()

"""
HOST="http://design-vc5-01.cisco.com:8080/sdk"
USER="svl-icf-vc.gen"
PASSWORD="Cisco123!"

https://design-vc5-01.cisco.com/mob/?moid=ServiceInstance&method=retrieveContent
"""