# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:54:02 2015

@author: prenato
"""

#import urllib2, time, yaml, json, os
import urllib2, time, json, subprocess
# from pprint import pprint

#define variables
dirname = '/Users/prenato/Downloads/'
file1 = 'bacalhau.json'
file2 = 'bacalhau2.json'
baca = 'baca.sh'
filename1 = dirname+file1
filename2 = dirname+file2
executavel = dirname+baca
inicio = time.ctime() #script start time
icfgetRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=userblue&password=userblue'
# admin icflistRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=admin&password=sv11abPW!'
# icflistAllVMs = "http://svl-icfd-1.cisco.com/app/api/rest?opName=Intercloud:userAPIGetAllVms"
icflistCatalog = "http://svl-icfd-1.cisco.com/app/api/rest?opName=userAPIGetCatalogsPerGroup&opData={param0:'blue'}"
icfCreateVM = "http://svl-icfd-1.cisco.com/app/api/rest?opName=Intercloud:userAPIProvisionVM&opData={param0:'CentOS63',param1:'CiscoCloudSvcs',param2:'Python'}"

response = urllib2.urlopen(icfgetRESTKey).read()
finalkey = (response.split('"')[1])
print finalkey

icfheader = 'X-Cloupia-Request-Key'
print icfheader

# Getting the request
request = urllib2.Request(icflistCatalog)
# Add Header
request.add_header(icfheader,finalkey)
# Getting the response
response2 = urllib2.urlopen(request)


# write script output
mp = response2.read()
with open(filename1, "wb") as xyz1:
	xyz1.write(mp)

#delete prvious file
subprocess.call(['rm','/Users/prenato/Downloads/bacalhau2.json'])
#cleanup original json file, leaving only needed information
subprocess.call(['/Users/prenato/Downloads/baca.sh'])

#read json file
with open(filename2) as f:
    data = f.read()
    jsondata = json.loads(data)

#print desired information
for row in jsondata['rows']:
    catalog_name = row['Catalog_Name']
    catalog_type = row['Catalog_Type']
    cloud_name = row['Cloud']
    image_type = row['Image']
    print 'Catalog Name: %s, Cloud Name: %s, Image Type: %s' % (catalog_name, cloud_name, image_type)

#
# The following commands creates new VM in the cloud
#
# Getting the request
request2 = urllib2.Request(icfCreateVM)
# Add Header
request2.add_header(icfheader,finalkey)
# Getting the response
urllib2.urlopen(request2)
