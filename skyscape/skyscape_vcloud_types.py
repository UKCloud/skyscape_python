__author__ = 'prossi'

from skyscape.skyscape_vm import VM
from skyscape.skyscape_vse import VSE
from skyscape.skyscape_orgvdc import ORGVDC
from skyscape.skyscape_vapp import VAPP


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



    def get_object(self, record):
        if self.cloudtype == 'VM':
            return VM(record, self.connection)
        elif self.cloudtype == 'VSE':
            return VSE(record, self.connection)
        elif self.cloudtype == 'VAPP':
            return VAPP(record, self.connection)
        elif self.cloudtype == 'ORGVDC':
            return ORGVDC(record, self.connection)