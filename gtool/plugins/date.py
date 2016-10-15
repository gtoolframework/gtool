from datetime import datetime
from gtool.core.types.core import CoreType


class Date(CoreType):

    def __validate__(self, valuedict):

        _dateformat = valuedict.get('dateformat', None)
        if _dateformat is not None and  isinstance(_dateformat, str):
            self.dateformat = _dateformat

        _displayformat = valuedict.get('displayformat', None)
        if _displayformat is not None and isinstance(_displayformat, str):
            self.datedisplayformat = _displayformat

        try:
            self.__datevalue__ = datetime.strptime(self.__value__, self.dateformat).date()
        except ValueError:
            raise

        self.__value__ = self.__datevalue__.strftime(self.datedisplayformat)
        return True

    @classmethod
    def __converter__(cls):
        return str

    """
    def __str__(self):
        return self.__datevalue__.strftime(self.datedisplayformat)
    """

    def __init__(self, *args, **kwargs):
        self.__validators__ = ['dateformat', 'displayformat']
        self.dateformat = '%m/%d/%Y'
        self.datedisplayformat = '%m/%d/%Y'
        super().__init__(*args, valuetype=str, **kwargs)

def load():
    return Date