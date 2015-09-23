__author__ = 'prossi'


class VAPP:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection