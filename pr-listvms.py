#! /usr/bin/env python2.7
"""
Created on Tue Feb 17 21:52:17 2015

@author: prenato
"""

import urllib2, json, subprocess
from tabulate import tabulate
#from pprint import pprint

#define variables
dirname = '/Users/prenato/Downloads/' #workdir
file1 = 'bacalhau.json' #raw json file
file2 = 'bacalhau2.json' #cleaned json file
baca = 'baca.sh' #awk script to cleanup json file
filename1 = dirname+file1
filename2 = dirname+file2
executavel = dirname+baca
icfheader = 'X-Cloupia-Request-Key'
icfgetRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=userblue&password=userblue'
#admin icfgetRESTKey = 'http://svl-icfd-1.cisco.com/app/api/rest?opName=getRESTKey&user=admin&password=sv11abPW!'
icflistAllVMs = "http://svl-icfd-1.cisco.com/app/api/rest?opName=Intercloud:userAPIGetAllVms"
#tempo = time.ctime() #script execution duration

#get ICF REST key
response = urllib2.urlopen(icfgetRESTKey).read()
finalkey = (response.split('"')[1])

# list all VMs
request = urllib2.Request(icflistAllVMs)
# Add Header
request.add_header(icfheader,finalkey)
# Getting the response
response2 = urllib2.urlopen(request)
 
# write output
mp = response2.read()
with open(filename1, "w") as ficheiro1:
	ficheiro1.write(mp)

#delete prvious working file file
subprocess.call(['rm','/Users/prenato/Downloads/bacalhau2.json'])
#cleanup original json file, leaving only needed information
"""
used script for json file cleanup baca.sh:
#! /bin/sh
/usr/bin/awk -F\"serviceResult\"\: '{ print $NF }' /Users/prenato/Downloads/bacalhau.json | \
/usr/bin/awk -F\,\"columnMetaData '{ print $1 }' | \
/usr/bin/awk '{ print $0"\}" }' > /Users/prenato/Downloads/bacalhau2.json
"""
subprocess.call(['/Users/prenato/Downloads/baca.sh'])

#read json file
with open(filename2) as f:
    data = f.read()
    jsondata = json.loads(data)


#print desired information
list_VM=[]
for row in jsondata['rows']:
    instance = row['Instance_ID']
    cloud = row['Cloud']
    ipaddress = row['IP_Address']
    list_VM.append([cloud,instance,ipaddress])

print tabulate(list_VM, headers=["Cloud", "VM Name", "IP Address"], tablefmt="rst")

    
