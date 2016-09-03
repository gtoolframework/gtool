from gtool.core.types.core import FunctionType
#import codecs
import os.path as path


class Filename(FunctionType):
    """
    Will return the filename, without path, of the object the method is a part of
    """

    def __init__(self, obj, config=None):

        if config is not None:
            raise ValueError('Filename method plugin does not accept a configuration')

        super(Filename, self).__init__(obj, config=None)

        self.computable = True

    def compute(self):
        if self.computable:
            #_result = codecs.decode(self.context['file'], 'unicode_escape')
            _result = path.split(self.context['file'])[1]
            self.__result__ = _result

def load():
    return Filename
