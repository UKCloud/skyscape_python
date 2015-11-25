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
    def storage_profiles(self):
        return self.connection.get_storageprofile(filters='vdc=={0}'.format(self.vdc))

    @lazy_property
    def vms(self):
        return self.connection.get_vm(filters='container=={0}'.format(self.href))

    def list_storage_profiles(self):
        i = 0
        for a in self.storage_profiles:
            outputstring = "ID {0}: Name: {1} - Default: {4} - Storage Limit: {2} - Storage Used: {3}".format(i, a.name, a.storageLimitMB, a.storageUsedMB, a.isDefaultStorageProfile)
            i += 1
            print outputstring

    def list_vms(self):
        i = 0
        for a in self.vms:
            outputstring = "ID {0}: Name: {1} - Status: {4} - CPUs: {2} - MemoryMB: {3}".format(i, a.name, a.numberOfCpus, a.memoryMB, a.status)
            i += 1
            print outputstring

    def add_network(self, networkname, parenthref, fencemode):
        recomposexml = """
        <RecomposeVAppParams
        xmlns="http://www.vmware.com/vcloud/v1.5"
        xmlns:ns2="http://schemas.dmtf.org/ovf/envelope/1"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1"
        xmlns:environment_1="http://schemas.dmtf.org/ovf/environment/1">
            <Description> "api deployed vm" </Description>
            <InstantiationParams>
                <NetworkConfigSection>
                    <ovf:Info>Configuration parameters for logical networks</ovf:Info>
                    <NetworkConfig networkName="{0}">
                        <Configuration>
                            <ParentNetwork href="{1}" />
                            <FenceMode>{2}</FenceMode>
                        </Configuration>
                    </NetworkConfig>
                </NetworkConfigSection>
            </InstantiationParams>
        </RecomposeVAppParams>
        """.format(networkname, parenthref, fencemode)

        #print recomposexml
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

    def add_vm(self, catalogitemhref, name, networkhref):
        recomposexml = """
        <RecomposeVAppParams
          xmlns="http://www.vmware.com/vcloud/v1.5"
          xmlns:ns2="http://schemas.dmtf.org/ovf/envelope/1"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1"
          xmlns:environment_1="http://schemas.dmtf.org/ovf/environment/1">
          <Description> "api deployed vm" </Description>
          <SourcedItem sourceDelete="false">
            <Source type="application/vnd.vmware.vcloud.vm+xml" name="{1}" href="{0}"/>
        """.format(catalogitemhref, name)

        if networkhref is not None:
            recomposexml += """
                <InstantiationParams>
                    <NetworkConnectionSection
                    xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1"
                type="application/vnd.vmware.vcloud.networkConnectionSection+xml"
                href="{0}/networkConnectionSection/"
                ovf:required="false">
                <ovf:Info />
                        <PrimaryNetworkConnectionIndex>0</PrimaryNetworkConnectionIndex>
                        <NetworkConnection
                            network="{1}">
                            <NetworkConnectionIndex>0</NetworkConnectionIndex>
                            <IsConnected>true</IsConnected>
                            <IpAddressAllocationMode>DHCP</IpAddressAllocationMode>
                        </NetworkConnection>
                    </NetworkConnectionSection>
                </InstantiationParams>
                """.format(catalogitemhref, networkhref)

        recomposexml += """
          </SourcedItem>
        </RecomposeVAppParams>
        """.format(catalogitemhref, name)
        #print recomposexml
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

    def add_vms(self, details):
        recomposexml = """
        <RecomposeVAppParams
          xmlns="http://www.vmware.com/vcloud/v1.5"
          xmlns:ns2="http://schemas.dmtf.org/ovf/envelope/1"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1"
          xmlns:environment_1="http://schemas.dmtf.org/ovf/environment/1">
          <Description> "api deployed vm" </Description>
        """

        for item in details:
            recomposexml += """
            <SourcedItem sourceDelete="false">
                <Source type="application/vnd.vmware.vcloud.vm+xml" name="{0}" href="{1}"/>
            """.format(item[1], item[0])

            if item.__len__() == 3:
                recomposexml += """
                <InstantiationParams>
                    <NetworkConnectionSection
                    xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1"
                type="application/vnd.vmware.vcloud.networkConnectionSection+xml"
                href="{0}/networkConnectionSection/"
                ovf:required="false">
                <ovf:Info />
                        <PrimaryNetworkConnectionIndex>0</PrimaryNetworkConnectionIndex>
                        <NetworkConnection
                            network="{1}">
                            <NetworkConnectionIndex>0</NetworkConnectionIndex>
                            <IsConnected>true</IsConnected>
                            <IpAddressAllocationMode>DHCP</IpAddressAllocationMode>
                        </NetworkConnection>
                    </NetworkConnectionSection>
                </InstantiationParams>
                """.format(item[0], item[2])

            recomposexml += """
            </SourcedItem>
            """

        recomposexml += """
        </RecomposeVAppParams>
        """
        #print recomposexml
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