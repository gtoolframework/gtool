from gtool.core.types.core import FunctionType
import codecs
import os.path as path


class Fullpath(FunctionType):
    """
    Will return the path, with filename, of the object the method is a part of
    """

    def __init__(self, obj, config=None):

        if config is not None:
            raise ValueError('Fullpath method plugin does not accept a configuration')

        super(Fullpath, self).__init__(obj, config=None)

        self.computable = True

    def compute(self):
        if self.computable:
            _result = codecs.decode(self.context['file'], 'unicode_escape')
            self.__result__ = _result

def load():
    return Fullpath
