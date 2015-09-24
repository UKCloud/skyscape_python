__author__ = 'prossi'


class VAPPNETWORK:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection

