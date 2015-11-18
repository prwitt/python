# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 22:58:53 2015

@author: prenato
"""

import getpass

def login():
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()

    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

    p1, p2 = pprompt()
    while p1 != p2:
        print('Passwords do not match. Try again')
        p1, p2 = pprompt()

    return user, p1

# Connecting to server
#server.connect("https://design-sso-00:9443/vsphere-client/","prenato@cisco.com",password)

"""
from pysphere import VIServer
server = VIServer()
server.connect("my.esx.host.com", "myusername", "secret")
vm = server.get_vm_by_path("[datastore] path/to/file.vmx")
vm.power_on()
print vm.get_status()
"""