#!/usr/bin/python
'''
Author: shitpati
Date: June 19, 2014
'''

import os, re
import httplib
import time
from functools import wraps

count = 1
def testIndex():
    global count
    v=str(count)
    pscr = '########### Test:'+v + '  ##############'
    count += 1
    return pscr

def tmp_wrap(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        print "Executing:", func.__name__
        return func(*args, **kwargs)
    return tmp


def run_post(uri, request, head):
    start_time = time.time()
    conn = httplib.HTTPSConnection(icpep_base_url)
    print "URI is:", uri
    uri = uri.strip()
    conn.request("POST", uri, request, head)
    conn.send(request)
    response = conn.getresponse()
    elapsed=time.time() - start_time
    print "Time taken:", elapsed, "seconds"
    status = response.status
    reason = response.reason
    if (status == 200 ):
       return response.read()
    else:
       return str(status)

def run_get(uri, request, head):
    start_time = time.time()
    conn = httplib.HTTPSConnection(icpep_base_url)
    print "URI is:", uri
    conn.request("GET", uri, request, head)
    response = conn.getresponse()
    elapsed=time.time() - start_time
    print "Time taken:", elapsed, "seconds"
    status = response.status
    reason = response.reason
    if (status == 200 ):
       return response.read()
    else:
       return str(status)

def run_delete(uri, request, head):
    start_time = time.time()
    conn = httplib.HTTPSConnection(icpep_base_url)
    print "URI is:", uri
    conn.request("DELETE", uri, request, head)
    response = conn.getresponse()
    elapsed=time.time() - start_time
    print "Time taken:", elapsed, "seconds"
    status = response.status
    reason = response.reason
    if (status == 200 ):
       return response.read()
    else:
       return str(status)


# Get Keys first
@tmp_wrap
def getKeys(uname, pword, targetIp):
    global icpep_base_url
    icpep_base_url=targetIp
    headers = {'X-Capi-Request': '675A19E9F9AF44059CE3AFF49CAF30DD'}
    KEY_XML= """<GetKeys username="""+"'"+uname+"""' password="""+"'"+pword+"' expiration='-1' /> """.strip()
    print KEY_XML
    getkeys = run_post('/v1/capi/login', KEY_XML, headers)
    keylist = getkeys.split();
    key=keylist[5].strip('value=')
    key=key.strip('"')
    headers = {'X-Capi-Request': key}
    return headers

#Get locations
@tmp_wrap
def getLocations(header):
    resp = run_get('/v1/capi/locations', None, header)
    return resp

#Get Capabilities
@tmp_wrap
def getCapabilities(header):
    resp = run_get('/v1/capi/capabilities', None, header)
    return resp

#Get vpcs
@tmp_wrap
def getVpcs(header):
    resp = run_get('/v1/capi/vpcs', None, header)
    print resp
    for kv in resp.split(" "):
        if re.search('providerId', kv):
            # hack since normal strip was not working
            part = kv.strip('providerId=')
            part = re.sub(r'^"|"$', '', part)
            return part
    return "Unknown"

#Get publicips
@tmp_wrap
def getPublicips(header):
    resp = run_get('/v1/capi/publicips', None, header)
    return resp

#Get images
@tmp_wrap
def getImages(header, imageid):
    newString='/v1/capi/images/' + str(imageid)
    print "Get request:" + newString
    resp = run_get(newString, None, header)
    print resp
    match = re.search(r'status="(inprogress|active|deleted|deleting|failed)"', resp)
    if match:
        return match.group().strip('status=').strip('"')
    return "Unknown"

#Get templates
@tmp_wrap
def getTemplates(header, templateid):
    newString='/v1/capi/templates/' + str(templateid)
    resp = run_get(newString, None, header)
    print resp
    if resp == "405":
        return resp
    match = re.search(r'status="(failed|inprogress|complete|deleted|deleting|inactive)"', resp)
    if match:
        return match.group().strip('status=').strip('"')
    return "Unknown"


#Get templates
@tmp_wrap
def getServers(header, serverid):
    newString='/v1/capi/servers/' + str(serverid)
    resp = run_get(newString, None, header)
    print resp
    match = re.search(r'status="(Failed|Reboot|Rebooting|Creating|Running|Deleted|Deleting|Starting|Stopping|Stopped)"', resp)
    if match:
        return match.group().strip('status=').strip('"')
    return "Unknown"


@tmp_wrap
def postImages(header, filename):
    IMG_XML= ''' <Image name="testImg" imageId="" fileName="'''+filename+''' " fileSize="87898" osFamily="linux" osDistro="ubuntu" osDistroVersion="12,04" osArchitecture="x86" vNicCount="1" imageType="RAW" virtualizationType="HVM" ></Image> '''.strip()
    resp = run_post('/v1/capi/images', IMG_XML, header)
    print resp
    for kv in resp.split(" "):
        if re.search('imageId', kv):
            # hack since normal strip was not working
            part = kv.strip('imageId=')
            part = re.sub(r'^"|"$', '', part)
            part = re.sub(r'^"|/>$', '', part)
            part = re.sub(r'^"|"$', '', part)
            return part
    return "Unknown"


@tmp_wrap
def uploadImages(pathname, iid):
    os.system('scp "%s" "%s:%s"' % (pathname, "root@"+icpep_base_url, "/opt/capi-images/img"+iid+"/") )
    return 


@tmp_wrap
def postTemplates(header, imageid, providerId,region):
    imageString='imageId="'+imageid+'"'
    TMP_XML= ''' <CreateTemplate> <Image '''+imageString+ '''> </Image> <Template name="testimg_template1" providerVpcId="'''+ providerId+ '''"  templateId="" locationName="'''+region+'''"></Template> </CreateTemplate>'''.strip()
    print TMP_XML
    resp = run_post('/v1/capi/templates', TMP_XML, header)
    print resp
    for kv in resp.split(" "):
        if re.search('templateId', kv):
            part = kv.strip('templateId=')
            part = re.sub(r'^"|"$', '', part)
            part = re.sub(r'^"|/>$', '', part)
            part = re.sub(r'^"|"$', '', part)
            return part.rstrip()
    return "Unknown"

@tmp_wrap
def postServers(header, templateId, srvname, providerId,networkName,locName):
    #SRV_XML= ''' <ImportCloudVM name="'''+ srvname+ '''"><Template name="" templateId="'''+templateId+'''"/><Server name="'''+ srvname+'''"  providerId="'''+providerId+'''" templateId="'''+templateId + '''" locationName="'''+locName+'''" resourceCpu="2" resourceMem="1024"><Disks/><VnicInfoList><VnicInfo index="1" networkName="'''+networkName+'''"><VnicIpInfoList><VnicIpInfo isPrimary="true" assignPublicIp="false"/></VnicIpInfoList></VnicInfo></VnicInfoList><Tags><Tag>VNMC_RES_ID-0004f5b6-4000-4273-0004-f5b640004273</Tag></Tags><ParameterList><Parameter name="resource-id" value="0004f5b6-4000-4273-0004-f5b640004273"/></ParameterList></Server><SecurityGroup name="secgrp-vpc-1-1396063012"><SecurityRuleList/></SecurityGroup></ImportCloudVM> '''.strip()
    SRV_XML= ''' <ImportCloudVM name="'''+ srvname+ '''"><Template name="" templateId="'''+templateId+'''" locationName="'''+locName+'''"/><Server name="'''+ srvname+'''"  providerId="'''+providerId+'''" templateId="'''+templateId + '''" locationName="'''+locName+'''" resourceCpu="2" resourceMem="1024"><Disks/><VnicInfoList><VnicInfo index="1" networkName="'''+networkName+'''"><VnicIpInfoList><VnicIpInfo isPrimary="true" assignPublicIp="false"/></VnicIpInfoList></VnicInfo></VnicInfoList><Tags><Tag>VNMC_RES_ID-0004f5b6-4000-4273-0004-f5b640004273</Tag></Tags><ParameterList><Parameter name="resource-id" value="0004f5b6-4000-4273-0004-f5b640004273"/></ParameterList></Server><SecurityGroup name="secgrp-vpc-1-1396063012"><SecurityRuleList/></SecurityGroup></ImportCloudVM> '''.strip()
    print SRV_XML
    resp = run_post('/v1/capi/servers', SRV_XML, header)
    print resp
    for kv in resp.split(" "):
        if re.search('serverid', kv):
            part = kv.strip('serverid=')
            part = re.sub(r'^"|"$', '', part)
            part = re.sub(r'^"|/>$', '', part)
            part = re.sub(r'^"|"$', '', part)
            return part.rstrip()
    return "Unknown"


@tmp_wrap
def postVmOps(header, serverid, actiontype):
    SRV_XML= ''' <ActionType type="'''+actiontype+'''"/> '''.strip()
    print SRV_XML
    serverString='/v1/capi/servers/'+serverid.rstrip()+'/action'
    resp = run_post(serverString, SRV_XML, header)
    print resp
    result = resp.split();
    return result;

@tmp_wrap
@tmp_wrap
def delImages(header, id):
    temp='/v1/capi/images/'+id
    resp = run_delete(temp, None, header)
    result = resp.split();
    return result;

@tmp_wrap
def delTemplates(header, id):
    temp='/v1/capi/templates/'+id
    resp = run_delete(temp, None, header)
    result = resp.split();
    return result;

@tmp_wrap
def delServers(header, id):
    temp='/v1/capi/servers/'+id
    resp = run_delete(temp, None, header)
    result = resp.split();
    return result;

@tmp_wrap
def postCloudProv(header, name, modname, ipaddr):
    CLD_XML='''<CloudProvision instanceName="'''+name+'''" type="cisco"   moduleName="''' + modname + '''" > <CloudCredentials ipAddress="''' + ipaddr + '''" /> </CloudProvision>'''.strip()
    print CLD_XML
    mystring='/v1/capi/cloudprovision'
    resp = run_post(mystring, CLD_XML, header)
    return resp;

@tmp_wrap
def postTenants(header, tenantName, cloudInstName, uuser, password):
    TNT_XML='''<Tenants tenantName="''' + tenantName + '''" instanceName="''' + cloudInstName +'''"> <Accounts username="''' + uuser + '''" password="'''+ password + '''"/></Tenants> '''.strip()
    print TNT_XML
    mystring='/v1/capi/tenants'
    resp = run_post(mystring, TNT_XML, header)
    return resp;
