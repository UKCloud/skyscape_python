__author__ = 'prossi'


class CATALOGITEM:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection

    def get_vms(self):
        return self.connection.get_vapptemplate(self.entity)
