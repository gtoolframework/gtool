from gtool.core.types.core import FunctionType
import os.path as path


class Nodename(FunctionType):
    """
    Will return the filename, without path or extension, of the object the method is a part of
    """

    def __init__(self, obj, config=None):

        if config is not None:
            raise ValueError('Nodename method plugin does not accept a configuration')

        super(Nodename, self).__init__(obj, config=None)

        self.computable = True

    def compute(self):
        if self.computable:
            _filename = path.split(self.context['file'])[1]
            _result = _filename.split('.')

            _result = '.'.join(_result[:-1]) if len(_result) > 1 else _filename

            self.__result__ = _result

def load():
    return Nodename
