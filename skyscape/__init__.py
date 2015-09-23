__author__ = 'prossi'

import base64

import requests
from lxml import objectify

from skyscape.skyscape_vcloud_types import Vcloud_Types


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
        return res.content

    def post_request(self, url, data):
        res = requests.post(url, data, headers=self.apiheaders, verify=True)
        return res.content

    def put_request(self, url, data):
        res = requests.put(url, data, headers=self.apiheaders, verify=True)
        return res.content

    def delete_request(self, url):
        res = requests.delete(url, headers=self.apiheaders, verify=True)
        return res.content

    def search_cloud(self, cloudtype, name='', id='', printoutput=False):
        holder = []
        if name:
            res = objectify.fromstring(self.get_computerequest("query?type={0}&filter=(name==*{1}*)".format(cloudtype, name)))
            recordholder = Vcloud_Types(res, self)
            for record in recordholder.data:
                holder.append(recordholder.get_object(record))
                if printoutput:
                    self.print_list(record.attrib)
        elif id:
            res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page=1&filter=(id=={1})".format(cloudtype, id)))
            recordholder = Vcloud_Types(res, self)
            for record in recordholder.data:
                holder.append(recordholder.get_object(record))
                if printoutput:
                    self.print_list(record.attrib)
        else:
            pagenumber = 1
            totalobjects = 0
            res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page=1".format(cloudtype)))
            recordholder = Vcloud_Types(res, self)
            totalobjects += recordholder.count
            availableobjects = int(res.get('total'))
            for record in recordholder.data:
                holder.append(recordholder.get_object(record))
                if printoutput:
                    self.print_list(record.attrib)
            while totalobjects < availableobjects:
                pagenumber += 1
                res = objectify.fromstring(self.get_computerequest("query?type={0}&pageSize=100&Page={1}".format(cloudtype, pagenumber)))
                recordholder = Vcloud_Types(res, self)
                totalobjects += recordholder.count
                for record in recordholder.data:
                    holder.append(recordholder.get_object(record))
                    if printoutput:
                        self.print_list(recordholder.attrib)
        return holder

    def get_edgegateway(self, name='', id='', printoutput=False):
        res = self.search_cloud(cloudtype='edgeGateway', name=name, id=id, printoutput=printoutput)
        return res

    def get_vm(self,name='',id='',printoutput=False):
        res = self.search_cloud(cloudtype='vm', name=name, id=id, printoutput=printoutput)
        return res





