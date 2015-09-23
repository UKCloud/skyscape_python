__author__ = 'prossi'
from lxml import objectify

from skyscape.skyscape_lookups import Lookups


class Vcloud_Method():
    def __init__(self, linkref, connection):
        self.rel = linkref.attrib['rel']
        self.href = linkref.attrib['href']
        lookup = Lookups()
        relinfo = lookup.get_relationship(self.rel)
        if relinfo.__len__() == 0:
            self.description = ""
            self.method = ""
        else:
            self.description = relinfo[1]
            self.method = relinfo[2]
        self.connection = connection

    def invoke(self, data=''):
        res = ""
        if self.method == 'POST':
            res = objectify.fromstring(self.connection.post_request(self.href, data))
        elif self.method == 'GET':
            res = objectify.fromstring(self.connection.get_request(self.href))
        elif self.method == 'PUT':
            res = objectify.fromstring(self.connection.put_request(self.href, data))
        elif self.method == 'DELETE':
            res = objectify.fromstring(self.connection.delete_request(self.href))
        else:
            print "There is no VERB for this request"
        return res