#! /usr/bin/env python2.7
"""
Created on Tue Feb 17 21:52:17 2015

@author: prenato
"""

import urllib2, json
from tabulate import tabulate
#from pprint import pprint

#define variables
icfheader = 'X-Cloupia-Request-Key'
icfgetRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=userblue&password=userblue'
#icfgetRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=admin&password=sv11abPW!'
icflistAllVMs = "http://svl-icfd-1.cisco.com/app/api/rest?opName=Intercloud:userAPIGetAllVms"
#icflistSRs = "http://svl-icfd-1.cisco.com/app/api/rest?opName=userAPIGetVMsForServiceRequest&opData={param0:'21'}"
#icfReboot = "http://svl-icfd-1.cisco.comapp/api/rest?opName=Intercloud:userAPIVmReboot&opData={param0:'540'}"
#icfSRlist = "http://svl-icfd-1.cisco.com/app/api/rest?opName=userAPIGetServiceRequests"

#inicio = time.ctime() #script execution duration


def list_VMs():
    #get ICF REST key
    response = urllib2.urlopen(icfgetRESTKey).read()
    finalkey = (response.split('"')[1])
    # list all VMs
    request = urllib2.Request(icflistAllVMs)
    # Add Header
    request.add_header(icfheader,finalkey)
    # Getting the response
    response2 = urllib2.urlopen(request)
    #read url output
    mp = response2.read()
    #decode json
    jsondata = json.loads(mp)
    #print desired information
    list_VM=[]
    for row in jsondata['serviceResult']['rows']:
        instance = row['Instance_ID']
        cloud = row['Cloud']
        ipaddress = row['IP_Address']
        list_VM.append([cloud,instance,ipaddress])
    #create output
    print tabulate(list_VM, headers=["Cloud", "VM Name", "IP Address"], tablefmt="rst")

list_VMs()

"""

def list_SRs():
    #get ICF REST key
    response = urllib2.urlopen(icfgetRESTKey).read()
    finalkey = (response.split('"')[1])
    # list all VMs
    requestSR = urllib2.Request(icflistSRs)
    # Add Header
    requestSR.add_header(icfheader,finalkey)
    # Getting the response
    responseSR = urllib2.urlopen(requestSR)
    #read url output
    mpSR = responseSR.read()
    #decode json  
    jsondataSR = json.loads(mpSR)
    #print desired information
    list_SR=[]
    for rowSR in jsondataSR['serviceResult']['vms']:
        IDvm = rowSR['vmId']
        instanceID = rowSR['instanceId']
        ipAddress = rowSR['ipAddress']
        powerstatus = rowSR['powerStatus']
        list_SR.append([IDvm,instanceID,ipAddress,powerstatus])
    #create output
    print tabulate(list_SR, headers=["VM ID", "Instance ID", "IP Address", "Power Status"], tablefmt="rst")

list_SRs()

def list_SRs2():
    #get ICF REST key
    response = urllib2.urlopen(icfgetRESTKey).read()
    finalkey = (response.split('"')[1])
    # list all VMs
    requestSR2 = urllib2.Request(icfSRlist)
    # Add Header
    requestSR2.add_header(icfheader,finalkey)
    # Getting the response
    responseSR2 = urllib2.urlopen(requestSR2)
    #read url output
    mpSR2 = responseSR2.read()
    #decode json  
    jsondataSR2 = json.loads(mpSR2)
    #print desired information
    list_SR2=[]
    for rowSR2 in jsondataSR2['serviceResult']['rows']:
        SRID = rowSR2['Service_Request_Id']        
        InitUser = rowSR2['Initiating_User']
        #VMSR2 = rowSR2['VM']
        RS2 = rowSR2['Request_Status']
        CWN = rowSR2['Catalog_Workflow_Name']
        list_SR2.append([SRID,InitUser,RS2,CWN])
    #create output
    print tabulate(list_SR2, headers=["SR ID", "User", "Status", "Workflow"], tablefmt="rst", missingval="-")

list_SRs2()
"""