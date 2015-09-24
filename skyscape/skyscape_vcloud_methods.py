__author__ = 'prossi'
import skyscape


class Vcloud_Method():
    def __init__(self, linkref, connection):
        self.rel = linkref.attrib['rel']
        self.href = linkref.attrib['href']
        if linkref.get('type') is not None:
            self.type = linkref.attrib['type']
        else:
            self.type = ""
        lookup = skyscape.skyscape_lookups.Lookups()
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
        if self.type != "":
            contenttypeheader = {"Content-Type": self.type}
        else:
            contenttypeheader = {}

        if self.method == 'POST':
            res = self.connection.post_request(self.href, data, contenttypeheader)
        elif self.method == 'GET':
            res = self.connection.get_request(self.href)
        elif self.method == 'PUT':
            res = self.connection.put_request(self.href, data, contenttypeheader)
        elif self.method == 'DELETE':
            res = self.connection.delete_request(self.href)
        else:
            print "There is no VERB for this request"

        return res