__author__ = 'prossi'
from lxml import objectify

from skyscape_orgvdc import ORGVDC
from skyscape.skyscape_vcloud_methods import Vcloud_Method


class lazy_property(object):
    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value


class VM():
    def __init__(self, vmobject, connection):
        self.__dict__ = dict(vmobject.attrib)
        self.extensiondata = dict(vmobject.attrib)
        self.connection = connection

    @lazy_property
    def vdc_data(self):
        return ORGVDC(objectify.fromstring(self.connection.get_link(self.vdc)))

    @lazy_property
    def vm_data(self):
        return objectify.fromstring(self.connection.get_link(self.href))

    @lazy_property
    def links(self):
        holder = []
        for link in self.vm_data.Link:
            new_method = Vcloud_Method(link, self.connection)
            if new_method.description != "":
                holder.append(new_method)
        return holder

    def list_links(self):
        i = 0
        for a in self.links:
            outputstring = "ID {0}: {1} - {2} - {3}".format(i, a.rel, a.description, a.href)
            i += 1
            print outputstring

    def refresh(self):
        self.__init__(self.vm_data, self.connection)


