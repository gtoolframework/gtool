from gtool.types.core import CoreType

class Number(CoreType):

    def __validate__(self, valuedict):
        _min = valuedict.get('min', None)
        _max = valuedict.get('max', None)
        min = int(_min) if _min is not None else None
        max = int(_max) if _max is not None else None
        if min is not None:
            if self.__value__ < min:
                raise ValueError('Values must be not be lower than %s but we got %s' % (min, self.__value__))
        if max is not None:
            if self.__value__ > max:
                raise ValueError('Values must not be higher than %s but we got %s' % (max, self.__value__))
        return True

    @classmethod
    def __converter__(cls):
        return int

    def __init__(self, *args, **kwargs):
        self.__validators__ = ['min', 'max']
        super().__init__(*args, valuetype=int, **kwargs)

def load():
    return Number