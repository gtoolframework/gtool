import warnings
from distutils.util import strtobool

from validators import url, ValidationFailure

from gtool.core.types.core import CoreType


class Url(CoreType):

    def __validate__(self, valuedict):
        _public = valuedict.get('public', None)
        if _public is None:
            public = 0 # False
        else:
            public = strtobool('%s' % _public)
            warnings.warn('public check does not currently work due a problem in the underlying validators library')
        try:
            url(self.__value__, public=public) # TODO public / private test doesn't work
        except ValidationFailure:
            raise ValueError('Was expecting a valid %s but got %s' % ('public URL' if public else 'URL', len(self.__value__)))
        return True

    @classmethod
    def __converter__(cls):
        return str

    def __init__(self, *args, **kwargs):
        self.__validators__ = ['public']
        super().__init__(*args, valuetype=str, **kwargs)

def load():
    return Url