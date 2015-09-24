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


class VAPP:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection
        self.rawxml = skyscape.etree.tostring(obj, pretty_print=True)

    @lazy_property
    def vapp_data(self):
        return skyscape.objectify.fromstring(self.connection.get_link(self.href))

    @lazy_property
    def links(self):
        holder = []
        for link in self.vapp_data.Link:
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
    def vdc_data(self):
        return skyscape.skyscape_orgvdc.ORGVDC(objectify.fromstring(self.connection.get_link(self.vdc)))

    def delete(self):
        return self.connection.delete_request(self.href)

    @lazy_property
    def vms(self):
        return self.connection.get_vm(filters='container=={0}'.format(self.href))

    def list_vms(self):
        i = 0
        for a in self.vms:
            outputstring = "ID {0}: Name: {1} - Status: {4} - CPUs: {2} - MemoryMB: {3}".format(i, a.name, a.numberOfCpus, a.memoryMB, a.status)
            i += 1
            print outputstring

    def add_vm(self, catalogitemhref, name):
        recomposexml = """
        <RecomposeVAppParams
          xmlns="http://www.vmware.com/vcloud/v1.5"
          xmlns:ns2="http://schemas.dmtf.org/ovf/envelope/1"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1"
          xmlns:environment_1="http://schemas.dmtf.org/ovf/environment/1">
          <Description> "api deployed vm" </Description>
              <SourcedItem sourceDelete="false">
                  <Source href="{0}" name="{1}"/>
              </SourcedItem>
          <AllEULAsAccepted>true</AllEULAsAccepted>
        </RecomposeVAppParams>
        """.format(catalogitemhref, name)

        recomposevapplink = ""
        for link in self.links:
            if 'recomposeVApp' in link.href:
                recomposevapplink = link

        if recomposevapplink != "":
            res = recomposevapplink.invoke(recomposexml)
            return res
        else:
            print "could not find recomposeVApp method on this VAPP"
            return None
