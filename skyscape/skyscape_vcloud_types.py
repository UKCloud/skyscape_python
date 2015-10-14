__author__ = 'prossi'

import skyscape


class Vcloud_Types:
    def __init__(self, data, connection):
        self.connection = connection
        if hasattr(data, 'VMRecord'):
            self.cloudtype = 'VM'
            self.data = data.VMRecord
            self.count = data.VMRecord.__len__()
        elif hasattr(data, 'EdgeGatewayRecord'):
            self.cloudtype = 'VSE'
            self.data = data.EdgeGatewayRecord
            self.count = data.EdgeGatewayRecord.__len__()
        elif hasattr(data, 'VAppRecord'):
            self.cloudtype = 'VAPP'
            self.data = data.VAppRecord
            self.count = data.VAppRecord.__len__()
        elif hasattr(data, 'OrgVdcRecord'):
            self.cloudtype = 'ORGVDC'
            self.data = data.OrgVdcRecord
            self.count = data.OrgVdcRecord.__len__()
        elif hasattr(data, 'CatalogRecord'):
            self.cloudtype = 'CATALOG'
            self.data = data.CatalogRecord
            self.count = data.CatalogRecord.__len__()
        elif hasattr(data, 'CatalogItemRecord'):
            self.cloudtype = 'CATALOGITEM'
            self.data = data.CatalogItemRecord
            self.count = data.CatalogItemRecord.__len__()
        elif hasattr(data, 'VAppTemplate'):
            self.cloudtype = 'VAPPTEMPLATE'
            self.data = data.VAppTemplate
            self.count = data.VAppTemplate.__len__()
        else:
            if hasattr(data, 'tag'):
                if "VAppTemplate" in data.tag:
                    self.cloudtype = "VAPPTEMPLATE"
                    self.data = data
                    self.count = 1
            self.count = 0
            self.data = []

    def get_object(self, record):
        if self.cloudtype == 'VM':
            return skyscape.skyscape_vm.VM(record, self.connection)
        elif self.cloudtype == 'VSE':
            return skyscape.skyscape_vse.VSE(record, self.connection)
        elif self.cloudtype == 'VAPP':
            return skyscape.skyscape_vapp.VAPP(record, self.connection)
        elif self.cloudtype == 'ORGVDC':
            return skyscape.skyscape_orgvdc.ORGVDC(record, self.connection)
        elif self.cloudtype == 'CATALOG':
            return skyscape.skyscape_catalog.CATALOG(record, self.connection)
        elif self.cloudtype == 'CATALOGITEM':
            return skyscape.skyscape_catalogitem.CATALOGITEM(record, self.connection)
        elif self.cloudtype == 'VAPPTEMPLATE':
            return skyscape.skyscape_vapptemplate.VAPPTEMPLATE(record, self.connection)