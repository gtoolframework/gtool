from gtool.core.types.core import FunctionType
import codecs
import os.path as path

class Path(FunctionType):

    def __init__(self, obj, config=None):

        if config is not None:
            raise ValueError('Path method plugin does not accept a configuration')

        super(Path, self).__init__(obj, config=None)

        self.computable = True

    def compute(self):
        if self.computable:
            _result = codecs.decode(path.split(self.context['file'])[0], 'unicode_escape')
            self.__result__ = _result

def load():
    return Path
