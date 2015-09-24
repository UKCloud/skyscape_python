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


class CATALOG:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection

    @lazy_property
    def catalog_data(self):
        return skyscape.objectify.fromstring(self.connection.get_link(self.href))

    @lazy_property
    def links(self):
        holder = []
        for link in self.catalog_data.Link:
            new_method = skyscape.skyscape_vcloud_methods.Vcloud_Method(link, self.connection)
            if new_method.description != "":
                holder.append(new_method)
        return holder

    def list_links(self):
        i = 0
        for a in self.links:
            outputstring = "ID {0}: {1} - {2} - {3}".format(i, a.rel, a.description, a.href)
            i += 1
            print outputstring

    @lazy_property
    def catalog_items(self):
        return self.connection.get_catalogitem(filters='catalog=={0}'.format(self.href))

    def list_catalog_items(self):
        i = 0
        for a in self.catalog_items:
            outputstring = "ID: {0}: {3} - {1} - {2}".format(i, a.name, a.href, a.entityType)
            i += 1
            print outputstring