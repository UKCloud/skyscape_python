__author__ = 'prossi'


class APIDEFINITION:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection

