__author__ = 'prossi'


class VCLOUDERROR:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection
