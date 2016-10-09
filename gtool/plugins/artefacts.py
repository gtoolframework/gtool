from gtool.core.types.core import FunctionType
import os
from gtool.core.utils.misc import striptoclassname
from distutils.util import strtobool

FILEONLY = 'fileonly'

class Artefacts(FunctionType):
    """
    Will return a list of artefacts (relative path)
    If fileonly == True is passed in then only filenames will be listed
    """

    def __init__(self, obj, config=None):

        _config = {FILEONLY: False}

        if config is not None:
            _configlist = [c.strip().lower() for c in config.split('=')]

            if len(_configlist) == 2 and _configlist[0] == FILEONLY:
                _config[FILEONLY] = strtobool(_configlist[1])
            else:
                raise ValueError('Artefact method plugin (used in user defined class %s) accepts a single argument of either '
                                 '"fileonly = True" or "fileonly = False". By default fileonly mode is False '
                                 'and does not need to be specified' % striptoclassname(type(obj)))

        super(Artefacts, self).__init__(obj, config=_config)

        self.computable = True

    def compute(self):
        # TODO make this plugin recurse into subdirectories (if recurse param is set to True)

        def listfiles(path):
            _ret = [f for f in os.listdir(path) if f.startswith('!')]
            if self.config[FILEONLY]:
                _ret = [os.path.join(path, f) for f in _ret]
            return _ret

        if self.computable:
            path = self.context['file']
            if os.path.isdir(path):
                self.__result__ = listfiles(path)
            elif os.path.isfile(path):
                self.__result__ = listfiles(os.path.split(path)[0])


def load():
    return Artefacts
