deployment_vdc = 'Skyscape (IL0-PROD-BASIC)'
deployment_catalog = 'Skyscape Catalog'
deployment_catalog_item = 'BLANK VM'
deployment_new_vapp_name = 'A TEST VAPP'
deployment_new_vapp_description = 'A TEST VAPP DESCRIPTION'
deployment_new_vm_base_name = 'A TEST VM'
deployment_num_vms_to_create = 5
deployment_network_name = 'TEST NETWORK'
deployment_network_parent = 'VDC Isolated'


import skyscape
import time
import getpass

skyscape_api_user_id = raw_input("Please enter your skyscape user id: ")
skyscape_api_user_password = getpass.getpass("Please enter your skyscape password: ")
skyscape_api_user_org = raw_input("Please enter your skyscape ORG id: ")

starttime = time.time()

c = skyscape.Connection(skyscape_api_user_id, skyscape_api_user_org, skyscape_api_user_password, 'https://api.vcd.portal.skyscapecloud.com/api', '5.6')
print "Logging in..."
c.login()
c.connected()

logintime = time.time()
logintimediff = int(logintime - starttime)
print "Login took {0} seconds".format(logintimediff)

print "Connected"
print "Getting VDCS for ORG"
before = time.time()
vdcs = c.get_orgvdc()

after = time.time()
timediff = int(after-before)
print "Getting all ORGS took {0} seconds".format(timediff)

print "Getting Catalogs for ORG"

before = time.time()
cats = c.get_catalog()
after = time.time()
timediff = int(after-before)
print "Getting all Catalogs took {0} seconds".format(timediff)

obj_deployment_vdc = None

print "Locating VDC {0}".format(deployment_vdc)
for vdc in vdcs:
    if vdc.name == deployment_vdc:
        obj_deployment_vdc = vdc

obj_deployment_catalog = None

print "Locating Catalog {0}".format(deployment_catalog)
for cat in cats:
    if cat.name == deployment_catalog:
        obj_deployment_catalog = cat

print "Locating Catalog Item {0}".format(deployment_catalog_item)
for item in obj_deployment_catalog.catalog_items:
    if item.name == deployment_catalog_item:
        obj_deployment_catalog_item = item.vapp[0].vms[0].href

print "Creating a new empty VAPP"
before = time.time()
newvapp = obj_deployment_vdc.compose_vapp(deployment_new_vapp_name, deployment_new_vapp_description)
after = time.time()
timediff = int(after-before)
print "Waiting for it to complete"
print "Creating empty VAPP took {0} seconds".format(timediff)
time.sleep(10)

if 'vapps' in obj_deployment_vdc.__dict__:
    del obj_deployment_vdc.vapps

obj_deployment_vapp = None

print "Finding our new VAPP"
for vapp in obj_deployment_vdc.vapps:
    if vapp.name == deployment_new_vapp_name:
        obj_deployment_vapp = vapp

print "Finding parent ORG Network {0}".format(deployment_network_parent)
for orgnetwork in vdc.orgnetworks:
    if orgnetwork.name == deployment_network_parent:
            obj_deployment_network_parent = orgnetwork.href

print "Creating new VAPP network {0}".format(deployment_network_name)
before = time.time()
res = obj_deployment_vapp.add_network(deployment_network_name, obj_deployment_network_parent, 'natRouted')
while not res.status == 'success':
    print "Waiting for network to complete..."
    res.refresh_status()
    time.sleep(2)
after = time.time()
timediff = int(after-before)
print "Creating new VAPP network took {0} seconds".format(timediff)

print "Creating an array of {0} VM's config...".format(deployment_num_vms_to_create)
vm_holder = []
for x in range(0, deployment_num_vms_to_create):
    this_name = '{0} {1}'.format(deployment_new_vm_base_name, x)
    this_input = [obj_deployment_catalog_item, this_name, deployment_network_name]
    vm_holder.append(this_input)

print "Creating VAPP with {0} VM's".format(deployment_num_vms_to_create)
before = time.time()
res = obj_deployment_vapp.add_vms(vm_holder)
while not res.status == 'success':
    after = time.time()
    timediff = int(after-before)
    print "Waiting for VAPP creation to complete... {0} seconds so far".format(timediff)
    res.refresh_status()
    time.sleep(2)
after = time.time()
timediff = int(after-before)
print "Creating a VAPP with {0} VM's took {1} seconds".format(deployment_num_vms_to_create, timediff)

#Adding an extra random VM that doesn't have a network connection
print "Adding an extra VM to the VAPP with no network connection..."
before = time.time()
res = obj_deployment_vapp.add_vm(obj_deployment_catalog_item,'An Extra VM NO NETWORK',None)
while not res.status == 'success':
    after = time.time()
    timediff = int(after-before)
    print "Waiting for VM addition to complete... {0} seconds so far".format(timediff)
    res.refresh_status()
    time.sleep(2)
after = time.time()
timediff = int(after-before)
print "Creating an additional VM with no network connection took {0} seconds".format(timediff)

#Adding another VM that has a network connection
print "Adding an extra VM to the VAPP with a network connection..."
before = time.time()
res = obj_deployment_vapp.add_vm(obj_deployment_catalog_item,'An Extra VM WITH NETWORK',deployment_network_name)
while not res.status == 'success':
    after = time.time()
    timediff = int(after-before)
    print "Waiting for VM addition to complete... {0} seconds so far".format(timediff)
    res.refresh_status()
    time.sleep(2)
after = time.time()
timediff = int(after-before)
print "Creating an additional VM with a network connection took {0} seconds".format(timediff)

after = time.time()
timediff = int(after-starttime)
print "Total script took {0} seconds to run".format(timediff)