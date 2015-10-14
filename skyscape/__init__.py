__author__ = 'prossi'

import base64
import requests
from lxml import objectify, etree
import skyscape_vapp
import skyscape_vcloud_methods
import skyscape_error
import skyscape_task
import skyscape_orgvdc
import skyscape_vappnetwork
import skyscape_vapptemplate
import skyscape_vcloud_types
import skyscape_vm
import skyscape_vmdiskrelation
import skyscape_apidefinition
import skyscape_catalog
import skyscape_catalogitem
import skyscape_disk
import skyscape_event
import skyscape_vse
import skyscape_lookups
import skyscape_group
import skyscape_media
import skyscape_storageprofile
import skyscape_service
import skyscape_user


class Connection:
    def __init__(self, username, org, password, url, apiversion):
        self.Accept = "application/*+xml;version={0}".format(apiversion)
        self.SkyscapeURL = url
        pair = "{username}:{password}".format(username='{0}@{1}'.format(username, org), password=password)
        encodedpair = base64.b64encode(pair)
        self.Authorization = 'Basic %s' % str(encodedpair)
        self.apiheaders = {"Authorization": self.Authorization, "Accept": self.Accept}
        self.xvCloudAuthorization = ""

    def login(self):
        res = requests.post(self.SkyscapeURL + '/sessions', headers=self.apiheaders, verify=True)
        self.xvCloudAuthorization = res.headers['x-vcloud-authorization']
        self.apiheaders = {"Authorization": self.Authorization, "Accept": self.Accept, 'x-vcloud-authorization': self.xvCloudAuthorization}

    def logout(self):
        res = requests.delete(self.SkyscapeURL + '/sessions', headers=self.apiheaders, verify=True)
        print res

    def connected(self):
        res = (requests.get(self.SkyscapeURL + '/session', headers=self.apiheaders, verify=True)).ok
        return res

    def get_link(self, url):
        res = requests.get(url, headers=self.apiheaders, verify=True)
        return res.content

    def get_computerequest(self, endpoint):
        res = requests.get(self.SkyscapeURL + '/' + endpoint, headers=self.apiheaders, verify=True)
        return res.content

    def format_list(self, data):
        for a in data:
            outputstring = "{0}: {1} - ".format(a, data[a])
            print outputstring

    def print_list(self, data):
        outputstring = ""
        for a in data:
            outputstring += "{0}: {1} - ".format(a, data[a])
        print outputstring

    def get_request(self, url):
        res = requests.get(url, headers=self.apiheaders, verify=True)
        return self.parse_object(objectify.fromstring(res.content))

    def post_request(self, url, data, additionalheaders={}):
        thisrequestheaders = self.apiheaders
        for header in additionalheaders:
            thisrequestheaders[header] = additionalheaders[header]

        res = requests.post(url, data, headers=thisrequestheaders, verify=True)
        return self.parse_object(objectify.fromstring(res.content))

    def put_request(self, url, data):
        res = requests.put(url, data, headers=self.apiheaders, verify=True)
        return self.parse_object(objectify.fromstring(res.content))

    def delete_request(self, url):
        res = requests.delete(url, headers=self.apiheaders, verify=True)
        return self.parse_object(objectify.fromstring(res.content))

    def parse_object(self, obj):
        if hasattr(obj, 'tag'):
            if 'Task' in obj.tag:
                return skyscape_task.TASK(obj, self)
            if 'Error' in obj.tag:
                return skyscape_error.VCLOUDERROR(obj, self)
            if 'VAppRecord' in obj.tag:
                return skyscape_vapp.VAPP(obj, self)
            if 'VAppTemplate' in obj.tag:
                return skyscape_vapptemplate.VAPPTEMPLATE(obj, self)
        return obj

    def search_cloud(self, cloudtype, name='', id='', filters='', printoutput=False):
        holder = []
        if name:
            if filters == '':
                res = objectify.fromstring(self.get_computerequest("query?type={0}&filter=(name==*{1}*)".format(cloudtype, name)))
            else:
                res = objectify.fromstring(self.get_computerequest("query?type={0}&filter=(name==*{1}*&{2})".format(cloudtype, name, filters)))

            recordholder = skyscape_vcloud_types.Vcloud_Types(res, self)
            for record in recordholder.data:
                holder.append(recordholder.get_object(record))
                if printoutput:
                    self.print_list(record.attrib)
        elif id:
            if filters == "":
                res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page=1&filter=(id=={1})".format(cloudtype, id)))
            else:
                res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page=1&filter=(id=={1}&{2})".format(cloudtype, id, filters)))
            recordholder = skyscape_vcloud_types.Vcloud_Types(res, self)
            for record in recordholder.data:
                holder.append(recordholder.get_object(record))
                if printoutput:
                    self.print_list(record.attrib)
        else:
            pagenumber = 1
            totalobjects = 0
            if filters == '':
                res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page=1".format(cloudtype)))
            else:
                res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page=1&filter=({1})".format(cloudtype, filters)))
            recordholder = skyscape_vcloud_types.Vcloud_Types(res, self)
            totalobjects += recordholder.count
            availableobjects = int(res.get('total'))
            for record in recordholder.data:
                holder.append(recordholder.get_object(record))
                if printoutput:
                    self.print_list(record.attrib)
            while totalobjects < availableobjects:
                pagenumber += 1
                if filters == '':
                    res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page={1}".format(cloudtype, pagenumber)))
                else:
                    res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page={1}&filter=({2})".format(cloudtype, pagenumber, filters)))
                recordholder = skyscape_vcloud_types.Vcloud_Types(res, self)
                totalobjects += recordholder.count
                for record in recordholder.data:
                    holder.append(recordholder.get_object(record))
                    if printoutput:
                        self.print_list(recordholder.attrib)
        return holder

    def get_edgegateway(self, name='', id='', filters='', printoutput=False):
        res = self.search_cloud(cloudtype='edgeGateway', name=name, id=id, filters=filters, printoutput=printoutput)
        return res

    def get_vm(self,name='', id='', filters='',printoutput=False):
        res = self.search_cloud(cloudtype='vm', name=name, id=id, filters=filters, printoutput=printoutput)
        return res

    def get_vapp(self, name='', id='', filters='', printoutput=False):
        res = self.search_cloud(cloudtype='vApp', name=name, id=id, filters=filters, printoutput=printoutput)
        return res

    def get_orgvdc(self, name='', id='', filters='', printoutput=False):
        res = self.search_cloud(cloudtype='orgVdc', name=name, id=id, filters=filters, printoutput=printoutput)
        return res

    def get_catalog(self, name='', id='', filters='', printoutput=False):
        res = self.search_cloud(cloudtype='catalog', name=name, id=id, filters=filters, printoutput=printoutput)
        return res

    def get_catalogitem(self, name='', id='', filters='', printoutput=False):
        res = self.search_cloud(cloudtype='catalogItem', name=name, id=id, filters=filters, printoutput=printoutput)
        return res

    def get_vapptemplate(self, href):
        res = objectify.fromstring(self.get_link(href))
        holder = []
        recordholder = skyscape_vcloud_types.Vcloud_Types(res, self)
        holder.append(recordholder.get_object(res))
        return holder