# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:54:02 2015

@author: prenato
"""
#import urllib2, time, yaml, json, os
import urllib2, time, json
from tabulate import tabulate

#define variables
inicio = time.ctime() #script start time
icfgetRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=userblue&password=userblue'
# admin icflistRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=admin&password=sv11abPW!'
# icflistAllVMs = "http://svl-icfd-1.cisco.com/app/api/rest?opName=Intercloud:userAPIGetAllVms"
icflistCatalog = "http://svl-icfd-1.cisco.com/app/api/rest?opName=userAPIGetCatalogsPerGroup&opData={param0:'blue'}"
icflistAllVMs = "http://svl-icfd-1.cisco.com/app/api/rest?opName=Intercloud:userAPIGetAllVms"
icfCreateVM = "http://svl-icfd-1.cisco.com/app/api/rest?opName=Intercloud:userAPIProvisionVM&opData={param0:'CentOS63',param1:'CiscoCloudSvcs',param2:'Python'}"

response = urllib2.urlopen(icfgetRESTKey).read()
finalkey = (response.split('"')[1])
print finalkey

icfheader = 'X-Cloupia-Request-Key'
print icfheader

def list_Catalogs():
    #get ICF REST key
    response = urllib2.urlopen(icfgetRESTKey).read()
    finalkey = (response.split('"')[1])
    # list all VMs
    request = urllib2.Request(icflistCatalog)
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
        catalog_name = row['Catalog_Name']
        catalog_type = row['Catalog_Type']
        cloud_name = row['Cloud']
        image_type = row['Image']
        list_VM.append([catalog_name,catalog_type,cloud_name,image_type])
    #create output
    print tabulate(list_VM, headers=["Catalog Name", "Catalog Type", "Cloud", "Image Name"], tablefmt="rst")

list_Catalogs()

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


# The following commands creates new VM in the cloud
# Getting the request
request2 = urllib2.Request(icfCreateVM)
# Add Header
request2.add_header(icfheader,finalkey)
# Getting the response
urllib2.urlopen(request2)
