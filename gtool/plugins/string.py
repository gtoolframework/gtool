from gtool.types.core import CoreType

class String(CoreType):

    def __validate__(self, valuedict):
        _maxlength = valuedict.get('maxlength', None)
        maxlength = int(_maxlength) if _maxlength is not None else None
        if maxlength is not None:
            if len(self.__value__) > maxlength:
                raise ValueError('Was expecting a string no more than %s chars long '
                                 'but the string had a length of %s' % (maxlength, len(self.__value__)))
        return True

    @classmethod
    def __converter__(cls):
        return str

    def __init__(self, *args, **kwargs):
        self.__validators__ = ['maxlength']
        super().__init__(*args, valuetype=str, **kwargs)

def load():
    return String