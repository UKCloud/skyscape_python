__author__ = 'prossi'
import skyscape


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


class VMTEMPLATE():
    def __init__(self, vmobject=None, connection=None):
        self.__dict__ = dict(vmobject.attrib)
        self.extensiondata = dict(vmobject.attrib)
        self.connection = connection
        self.obj = vmobject
        self.rawxml = skyscape.etree.tostring(vmobject)

    @lazy_property
    def network_connection(self):
        return self.obj.NetworkConnectionSection

    @lazy_property
    def guest_customisation(self):
        return self.obj.GuestCustomizationSection

    @lazy_property
    def virtual_hardware(self):
        alteredxml = self.rawxml.replace('ovf:', '')
        newobj = skyscape.objectify.fromstring(alteredxml)
        return newobj.VirtualHardwareSection