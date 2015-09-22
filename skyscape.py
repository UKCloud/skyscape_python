import requests
import base64
from lxml import etree
from lxml import objectify


SkyscapeURL = "https://api.vcd.portal.skyscapecloud.com/api"
Authorization = ""
Accept = "application/*+xml;version=5.1"
xvCloudAuthorization = ""


def new_computelogin(username, password):
    global Authorization
    global Accept
    global SkyscapeURL
    global xvCloudAuthorization
    pair = "{username}:{password}".format(username=username, password=password)
    encodedpair = base64.b64encode(pair)
    Authorization = 'Basic %s' % str(encodedpair)
    apiheaders = {"Authorization": Authorization, "Accept": Accept}
    res = requests.post(SkyscapeURL + '/sessions', headers=apiheaders, verify=False)
    xvCloudAuthorization = res.headers['x-vcloud-authorization']


def get_computerequest(endpoint):
    global Authorization
    global Accept
    global SkyscapeURL
    global xvCloudAuthorization
    apiheaders = {"Accept": Accept, "x-vcloud-authorization": xvCloudAuthorization}
    res = requests.get(SkyscapeURL + '/' + endpoint, headers=apiheaders, verify=False)
    return res.content


def get_vdc():
    vdc_res = objectify.fromstring(get_computerequest("query?type=orgVdc"))
    return vdc_res


def get_vm(urn='all'):
    vmholder = []
    pagenumber = 1
    availablevms = 0
    totalvms = 0
    if urn == 'all':
        vm_res = objectify.fromstring(get_computerequest("query?type=vm&pageSize=100&Page=1"))
        totalvms += vm_res.VMRecord.__len__()
        availablevms = int(vm_res.get('total'))
        vmholder += vm_res.VMRecord
        while (totalvms < availablevms):
            print("Currently have {0} VMS".format(totalvms))
            pagenumber += 1
            vm_res = objectify.fromstring(get_computerequest("query?type=vm&pageSize=100&Page={0}".format(pagenumber)))
            totalvms += vm_res.VMRecord.__len__()
            vmholder += vm_res.VMRecord
    else:
        vm_res = objectify.fromstring(get_computerequest("/vm/{0}".format(urn)))
        vmholder = vm_res.VMRecord
    return vmholder

# login to vcloud

# demo query, get all VM's and print them to screen
#vdc = get_vdc()

#print vdc

vm = get_vm()

print vm

