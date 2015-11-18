# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 15:42:27 2015

@author: prenato
"""

HOST="http://design-vc5-01.cisco.com:8080/sdk"
USER="svl-icf-vc.gen"
PASSWORD="Cisco123!"


from pysphere import VIServer
from pysphere.resources import VimService_services as VI

#Create an object to work with
server = VIServer()

#Connect to the server
server.connect(HOST,USER,PASSWORD)

#Get the list of all VMs (their VMX paths) in the vCenter that are powered on.
vmlist = server.get_registered_vms(status='poweredOn')

#For each path….
for vmpath in vmlist:
#Get the current performance manager object (it changes, so we can’t just instatiate it once)
        pm = server.get_performance_manager()
        #Get an actual VM object from the path
        vm = server.get_vm_by_path(vmpath)
        #Get the managed object reference for the VM, because the performance manager only accepts MoRefs
        mor = vm._mor
        #Get all the counters and their current values for that VM.
        counterValues = pm.get_entity_counters(mor)
         #print counterValues
        #Do some quick math on the values.
        #They come to us in a convienent dictionary form.
        #Values are descrobed here: http://www.vmware.com/support/developer/vc-sdk/visdk41pubs/ApiReference/virtual_disk_counters.html
        IOPs = counterValues['virtualDisk.numberReadAveraged'] + counterValues['virtualDisk.numberWriteAveraged']
        BandwidthKBs = counterValues['virtualDisk.read'] + counterValues['virtualDisk.write']
        ReadLatency = counterValues['virtualDisk.totalReadLatency']
        WriteLatency = counterValues['virtualDisk.totalWriteLatency']
        CpuReady=counterValues['cpu.ready']
        CpuUsage=counterValues['cpu.usage']
        MemUsage=counterValues['mem.usage']
        MemCtl=counterValues['mem.vmmemctl']
        MemSwapIn=counterValues['mem.swapin']
        MemSwapOut=counterValues['mem.swapout']
        #print them out.
        print vm.get_property('name'),IOPs,BandwidthKBs,ReadLatency,WriteLatency,CpuReady,CpuUsage,MemUsage,MemCtl,MemSwapIn,MemSwapOut