from gtool.core.types.core import FunctionType
import os
from gtool.core.utils.misc import striptoclassname
from distutils.util import strtobool
import codecs

FILEONLY = 'fileonly'

class Artefacts(FunctionType):
    """
    Will return a list of artefacts (relative path) inside directories starting with !
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

        def walkartefactdir(basepath):

            def scantree(path):
                """Recursively yield DirEntry objects for given directory."""
                for entry in os.scandir(path):
                    if entry.is_dir(follow_symlinks=False):
                        yield from scantree(entry.path)
                    else:
                        yield entry

            _retlist = []
            _container = os.path.split(basepath)[-1]
            for direntry in scantree(basepath):
                if self.config[FILEONLY]:
                    _retlist.append(direntry.name)
                elif direntry.path == basepath:
                    _retlist.append(os.path.join(_container, direntry.name)) #direntry.path[len(basepath)+1:])
                else:
                    _relpath = os.path.relpath(os.path.dirname(direntry.path), basepath)
                    _retlist.append(os.path.normpath(os.path.join(_container, _relpath, direntry.name)).replace('\\\\', '\\'))

            return _retlist

        def listfiles(path):

            artefact_direntries = [f for f in os.scandir(path) if f.is_dir(follow_symlinks=False) and f.name.startswith('!')]
            _ret = []
            for f in artefact_direntries:
                _path = os.path.normpath(os.path.join(path, f.name))
                _ret.extend(walkartefactdir(_path))

            return _ret

        if self.computable:
            path = self.context['file']
            if os.path.isdir(path):
                self.__result__ = listfiles(path)
            elif os.path.isfile(path):
                self.__result__ = listfiles(os.path.split(path)[0])


def load():
    return Artefacts
