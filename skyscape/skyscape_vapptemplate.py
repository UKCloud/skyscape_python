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


class VAPPTEMPLATE:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection
        self.rawxml = skyscape.etree.tostring(obj)
        self.obj = obj

    @lazy_property
    def vms(self):
        holder = []
        for vm in self.obj.Children.Vm:
            holder.append(skyscape.skyscape_vm.VM(vm))
        return holder


