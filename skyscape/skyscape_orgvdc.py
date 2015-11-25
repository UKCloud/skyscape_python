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


class ORGVDC:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection
        self.rawxml = skyscape.etree.tostring(obj, pretty_print=True)

    @lazy_property
    def orgvdc_data(self):
        return skyscape.objectify.fromstring(self.connection.get_link(self.href))

    @lazy_property
    def links(self):
        holder = []
        for link in self.orgvdc_data.Link:
            new_method = skyscape.skyscape_vcloud_methods.Vcloud_Method(link, self.connection)
            if new_method.description != "":
                holder.append(new_method)
        return holder

    def list_vapps(self):
        i = 0
        for a in self.vapps:
            outputstring = "ID {0}: Name: {1} - Status: {2} - Number of VMs: {3}".format(i, a.name, a.status, a.numberOfVMs)
            i += 1
            print outputstring

    def list_orgnetworks(self):
        i = 0
        for a in self.orgnetworks:
            outputstring = "ID {0}: Name: {1} - Gateway: {2}".format(i, a.name, a.gateway)
            i += 1
            print outputstring

    def list_storage_profiles(self):
        i = 0
        for a in self.storage_profiles:
            outputstring = "ID {0}: Name: {1} - Default: {4} - Storage Limit: {2} - Storage Used: {3}".format(i, a.name, a.storageLimitMB, a.storageUsedMB, a.isDefaultStorageProfile)
            i += 1
            print outputstring

    @lazy_property
    def storage_profiles(self):
        return self.connection.get_storageprofile(filters='vdc=={0}'.format(self.href))

    @lazy_property
    def vapps(self):
        return self.connection.get_vapp(filters='vdc=={0}'.format(self.href))

    @lazy_property
    def orgnetworks(self):
        return self.connection.get_orgnetwork()

    def list_links(self):
        i = 0
        for a in self.links:
            outputstring = "ID {0}: {1} - {2} - {3}".format(i, a.rel, a.description, a.href)
            i += 1
            print outputstring

    def compose_vapp(self, name, description):
        composevapplink = ""
        for link in self.links:
            if 'composeVApp' in link.href:
                composevapplink = link

        if composevapplink != "":
            composexml = """
            <ComposeVAppParams xmlns="http://www.vmware.com/vcloud/v1.5" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" name="{0}">
               <Description>{1}</Description>
               <AllEULAsAccepted>true</AllEULAsAccepted>
            </ComposeVAppParams>
            """.format(name, description)
            res = composevapplink.invoke(composexml)
            return res
        else:
            print "could not find composeVApp method on this VDC"
            return None
