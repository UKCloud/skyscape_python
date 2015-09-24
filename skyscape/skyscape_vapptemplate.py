__author__ = 'prossi'


class VAPPTEMPLATE:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection

