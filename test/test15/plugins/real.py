from gtool.core.types.core import CoreType

class Real(CoreType):

    def __validate__(self, valuedict):
        _min = valuedict.get('min', None)
        _max = valuedict.get('max', None)
        min = float(_min) if _min is not None else None
        max = float(_max) if _max is not None else None
        if min is not None:
            if self.__value__ < min:
                raise ValueError('Values must be not be lower than %s but we got %s' % (min, self.__value__))
        if max is not None:
            if self.__value__ > max:
                raise ValueError('Values must not be higher than %s but we got %s' % (max, self.__value__))
        return True

    @classmethod
    def __converter__(cls):
        return float

    def __init__(self, *args, **kwargs):
        self.__validators__ = ['min', 'max']
        super().__init__(*args, valuetype=float, **kwargs)

def load():
    return Real

