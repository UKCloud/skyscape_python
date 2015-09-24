__author__ = 'prossi'


class MEDIA:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection
