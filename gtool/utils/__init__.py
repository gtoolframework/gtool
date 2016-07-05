from .classgen import generateClass
from .classprocessor import readClass, processClass, debugClass
from gtool.filewalker import StructureFactory
from gtool.plugin import loadplugins
from .config import configloader
import os

def load():
    pass

def projectloader(projectroot, dbg=False):

    PROJECTDATA = "data"
    PROJECTCLASS = "classes"
    PROJECTCONFIG = "gtool.cfg"
    PROJECTPLUGINS = "plugins"

    projectclassroot = os.path.join(projectroot, PROJECTCLASS)
    projectdataroot = os.path.join(projectroot, PROJECTDATA)
    projectconfigpath = os.path.join(projectroot, PROJECTCONFIG)
    projectpluginroot = os.path.join(projectroot, PROJECTPLUGINS)

    loadplugins(projectpluginroot)
    configloader(projectconfigpath)

    """
    print('plugins:', pluginnamespace())
    for pluginname, pluginobj in pluginnamespace().items():
        print('executing plugin: ', pluginname)
        x = pluginobj()
        print(type(x))
    """

    __loadclasses(projectclassroot, dbg=dbg)
    return StructureFactory.treewalk(projectdataroot)

def __loadclasses(classpath, dbg=False):
    if os.path.isfile(classpath):
        __loadclass(classpath, dbg=dbg)
    elif os.path.isdir(classpath):
        for classfile in [f for f in os.listdir(classpath) if os.path.isfile(os.path.join(classpath, f))]:
            __loadclass(os.path.join(classpath, classfile), dbg=dbg)

def __loadclass(classpath, dbg=False):
    """

    :param configpath: path to config file
    :param dbg: set to ttue to debug config load
    :return: True
    """
    print(classpath)
    if os.path.exists(classpath):
        # TODO check if file is readable
        f = open(classpath, 'r')
        # TODO try except for file read errors
        classString = f.read()
    else:
        raise FileNotFoundError('%s does not exist' % classpath)
    # TODO capture exceptions
    classData = readClass(classString)
    if dbg is True:
        debug(classprocessor)
    # TODO capture exceptions
    classDict = processClass(classData)
    for classname, classconfig in classDict.items():
        # TODO capture exceptions
        generateClass(classname, classconfig)
    f.close()


def debug(classdata):
    print('--- class debug ---')
    debugClass(classdata)
    print('--- end of class debug ---')