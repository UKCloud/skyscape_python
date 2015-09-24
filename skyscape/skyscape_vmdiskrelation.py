__author__ = 'prossi'


class VMDISKRELATION:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection

