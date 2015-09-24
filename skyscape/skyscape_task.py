__author__ = 'prossi'
import skyscape


class TASK:
    def __init__(self, obj, connection):
        self.__dict__ = dict(obj.attrib)
        self.connection = connection

    def refresh_status(self):
        self.status = (self.connection.get_request(self.href)).status
        return self.status