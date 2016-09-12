import os

from gtool.core.filewalker import StructureFactory
from gtool.core.plugin import loadplugins
from .classgen import generateClass
from .classprocessor import readClass, processClass, debugClass
from .config import configloader, register
from gtool.core.namespace import namespace
from gtool.core.utils.output import parseformat, registerFormatter
from gtool.core.utils.runtime import registerruntimeoption

def projectloader(projectroot, dbg=False, outputscheme=None):

    PROJECTDATA = "data"
    PROJECTCLASS = "classes"
    PROJECTCONFIG = "gtool.cfg"
    PROJECTPLUGINS = "plugins"

    projectclassroot = os.path.join(projectroot, PROJECTCLASS)
    projectdataroot = os.path.join(projectroot, PROJECTDATA)
    projectconfigpath = os.path.join(projectroot, PROJECTCONFIG)
    projectpluginroot = os.path.join(projectroot, PROJECTPLUGINS)

    register('config', {'root': projectroot, 'classes': projectclassroot, 'dataroot': projectdataroot, 'configpath': projectconfigpath, 'plugin': projectpluginroot})
    loadplugins(projectpluginroot)
    configloader(projectconfigpath)

    if outputscheme is not None:
        registerruntimeoption('outputscheme', outputscheme) # TODO confirm outputscheme exists
    if dbg:
        registerruntimeoption('debug', dbg)

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
        _formatterdict = {}
        outputbasename = 'output'
        outputschemeseparator = '.'

        # use the specified outscheme but if not available use the default
        _outputscheme = outputbasename + outputschemeseparator + outputscheme
        formatstring = v.metas()[_outputscheme] if _outputscheme in v.metas() else v.metas().get(outputbasename, None)
        _formatter = parseformat(formatstring=formatstring) if formatstring is not None else None
        _formatterdict['format'] = _formatter

        headeroutputbasename = outputbasename + outputschemeseparator + 'headers'
        _headeroutputscheme = headeroutputbasename + outputschemeseparator + outputscheme

        _headers = None

        if _headeroutputscheme in v.metas():
            _headers = v.metas()[_headeroutputscheme]
        elif headeroutputbasename in v.metas():
            _headers = v.metas()[headeroutputbasename]

        if _headers is not None:
            _formatterdict['headers'] = _headers

        registerFormatter(k, _formatterdict)

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