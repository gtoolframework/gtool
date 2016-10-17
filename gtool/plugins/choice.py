from gtool.core.types.core import CoreType

class Choice(CoreType):

    def __validate__(self, valuedict):
        _choices = valuedict.get('choices', None)
        choices = [c.strip() for c in _choices.split(',')] if _choices is not None else None
        if self.__value__ not in choices:
            raise ValueError('Was expecting either one of %s but got a %s' % (choices, self.__value__))
        return True

    @classmethod
    def __converter__(cls):
        return str

    def __init__(self, *args, **kwargs):
        self.__validators__ = ['choices']
        super().__init__(*args, valuetype=str, **kwargs)

def load():
    return Choice