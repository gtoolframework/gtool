from gtool.core.types.core import FunctionType
import os

class Artefacts(FunctionType):
    """
    Will return a list of artefacts (relative path)
    """

    def __init__(self, obj, config=None):

        if config is not None:
            raise ValueError('Artefacts method plugin does not accept a configuration')

        super(Artefacts, self).__init__(obj, config=None)

        self.computable = True

    def compute(self):
        if self.computable:
            path = self.context['file']
            if os.path.isdir(path):
                _result = [f for f in os.listdir(path) if f.startswith('!')]
            elif os.path.isfile(path):
                _result = [f for f in os.listdir(os.path.split(path)[0]) if f.startswith('!')]
            self.__result__ = _result


def load():
    return Artefacts
