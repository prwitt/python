#!/usr/bin/python
'''
Author: shitpati
Date: June 19, 2014
'''

import icpep_rclient as rc
import uuid
import time
import sys
import os

def global_setup():
    global targetIp
    global userName
    global paword
    global tenantName
    global moduleName
    global cloudIp
    global cloudInstanceName
    global iid          #Image id this is id of image uploaded by PNSC	
    global region       #Region for current VPC
    global networkName  #Name of network under current VPC on which instance has to be launched
    global lName        #Region:AvailabilityZone needed for create server call
   
    targetIp="173.39.228.231"
    userName="prenato"
    cloudIp="us-texas-1.cisco.com"
    cloudInstanceName="ospNewCloudInst1pr_CCS"
    moduleName="OSP"
    paword="Por01sk8"
    tenantName="tenant"+genString(4)

    iid = "63556ef5-b9da-4048-a499-e058bc13843e"  #CentOs
    #iid = "a6a8229c-6ea0-42ed-a618-6f163e2541e3" #Cirros 
    #iid = "fdbc6040-b56c-4111-aba9-09a0156fc43a" #Ubuntu presice server
    region= "us-texas-1" 
    networkName = "privatenet" 
    lName = "us-texas-1:alln01-1-csx" 
    
# Helper ro generate a random string
def genString(string_length=15):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert uuid format to python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the uuid '-'.
    return random[0:string_length] # Return the random string.


# Set up all the globals
global_setup()

print "Testing ICPEP on:" + targetIp

#Get keys for admin
print rc.testIndex()
sp_header = rc.getKeys("admin", "admin", targetIp)
print sp_header

#provision cloud
print rc.testIndex()
cp = rc.postCloudProv(sp_header, cloudInstanceName, moduleName, cloudIp)
print cp


print rc.testIndex()
tenants = rc.postTenants(sp_header, tenantName, cloudInstanceName, userName, paword)
print tenants

#Now start the PNSC flows
print rc.testIndex()
pnscUser=userName+'@'+tenantName
header = rc.getKeys(pnscUser, paword, targetIp)
print header

print rc.testIndex()
locations = rc.getLocations(header)
print locations

print rc.testIndex()
cap = rc.getCapabilities(header)
print cap

print rc.testIndex()
providerId = rc.getVpcs(header)
print providerId

print rc.testIndex()
ips = rc.getPublicips(header)
print ips

print rc.testIndex()
tid=rc.postTemplates(header, iid, providerId,region)
print "Received template Id:"+tid

print rc.testIndex()
while True:
    status = rc.getTemplates(header, tid)
    print "get Templates returned:"+status
    if (status == "complete"):
        break;
    if (status == "failed"):
        # Cannot do much so get out
        sys.exit();
    if (status == "Unknown"):
        sys.exit()
    time.sleep(5)

print rc.testIndex()
servervm_name="server"+genString(4)
print "Using server Name:"+servervm_name
sid=rc.postServers(header, tid, servervm_name, providerId,networkName,lName)
print sid
	
print rc.testIndex()
while True:
    status = rc.getServers(header, sid)
    print "get Servers after post returned:"+status
    if (status == "Running"):
        break;
    if (status == "Failed"):
        break;
    if (status == "Unknown"):
        sys.exit()
    time.sleep(5)

print rc.testIndex()
print rc.postVmOps(header, sid, "Stop")

print rc.testIndex()
while True:
    status = rc.getServers(header, sid)
    print "get Servers after stop returned:"+status
    if (status == "Stopped"):
        break;
    time.sleep(5)


print rc.testIndex()
print rc.postVmOps(header, sid, "Start")

print rc.testIndex()
while True:
    status = rc.getServers(header, sid)
    print "get Servers after start returned:"+status
    if (status == "Running"):
        break;
    if (status == "Failed"):
        break;
    time.sleep(5)


print rc.testIndex()
print rc.postVmOps(header, sid, "Reboot")

print rc.testIndex()
while True:
    status = rc.getServers(header, sid)
    print "get Servers returned:"+status
    if (status == "Running"):
        break;
    if (status == "Failed"):
        break;
    time.sleep(5)


# Delete the Template    
print rc.testIndex()
print rc.delTemplates(header, tid)

print rc.testIndex()
while True:
    status = rc.getTemplates(header, tid)
    print "get Templates returned:"+status
    if (status == "deleted"):
        break;
    time.sleep(5)



# Delete the Server 
print rc.testIndex()
print rc.delServers(header, sid)

print rc.testIndex()
while True:
    status = rc.getServers(header, sid)
    print "get Servers returned:"+status
    if (status == "Deleted"):
        break;


    print "End VM Lifecycle Operations"

