import os

from gtool.core.filewalker import StructureFactory
from gtool.core.plugin import loadplugins
from .classgen import generateClass
from .classprocessor import readClass, processClass, debugClass
from .config import configloader
from gtool.core.namespace import namespace
from gtool.core.utils.output import parseformat, registerFormatter

def projectloader(projectroot, dbg=False, outputscheme=None):

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

    __loadclasses(projectclassroot, dbg=dbg)
    # loading output parser can only occur after all classes are loaded
    __outputparser(namespace(), outputscheme=outputscheme) #TODO make this a functional style call <-- return namespace from __loadclasses
    return StructureFactory.treewalk(projectdataroot) # returns the project data

def __loadclasses(classpath, dbg=False):
    if os.path.isfile(classpath):
        __loadclass(classpath, dbg=dbg)
    elif os.path.isdir(classpath):
        for classfile in [f for f in os.listdir(classpath) if os.path.isfile(os.path.join(classpath, f))]:
            __loadclass(os.path.join(classpath, classfile), dbg=dbg)

def __outputparser(globalnamespace, outputscheme=None):
    if outputscheme is None:
        raise ValueError('An outputscheme was not provided, cannot build output format tree')
    #print('Namespace:...')
    for k, v in globalnamespace.items():
        #print(k, ':', v.metas()[outputscheme])
        registerFormatter(k, parseformat(classname=k, formatstring=v.metas()[outputscheme]))
        #print(parseformat(v.metas()[outputscheme]))

def __loadclass(classpath, dbg=False):
    """

    :param configpath: path to config file
    :param dbg: set to ttue to debug config load
    :return: True
    """

    if os.path.exists(classpath):
        # TODO check if file is readable
        f = open(classpath, 'r')
        # TODO try except for file read errors
        classString = f.read()
    else:
        raise FileNotFoundError('%s does not exist' % classpath)
    # TODO capture exceptions
    classData = readClass(classString + '\n') #TODO get rid of \n by fixing attribute parser
    if dbg is True:
        debug(classData)
    # TODO capture exceptions
    #classDict = processClass(classData)
    classDict = classData
    for classname, classconfig in classDict.items():
        # TODO capture exceptions
        generateClass(classname, classconfig)
    f.close()


def debug(classdata):
    print('--- class debug ---')
    debugClass(classdata)
    print('--- end of class debug ---')