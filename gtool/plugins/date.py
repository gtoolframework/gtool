from datetime import datetime
from gtool.core.types.core import CoreType


class Date(CoreType):

    """
    A date handling coretype. Reads in a string and converts it into
    a desired format. By default the date is expected in the normal
    local format (for North America that is MM/DD/YY) and will display
    as in the normal local format (for North America that is MM/DD/YY).

    @created:: single: Date (required = True)

    Two arguments are supported: dateformat and displayformat.

    Dateformat controls how the date should be entered.
    Displayformat controls how the date will be displayed.

    Format strings should be encapsulated in []. Examples include:

    @created:: single: Date (required = True, displayformat = [%B %d %Y])
    @created:: single: Date (required = True, dateformat = [%m/%d/%Y])
    @created:: single: Date (required = True, dateformat = [%m/%d/%Y], displayformat = [%B %d %Y])
    https://www.tutorialspoint.com/python/time_strptime.htm
    """

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
        self.dateformat = '%x'
        self.datedisplayformat = '%x'
        super().__init__(*args, valuetype=str, **kwargs)

def load():
    return Date