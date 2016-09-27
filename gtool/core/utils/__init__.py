import os

from gtool.core.filewalker import StructureFactory
from gtool.core.plugin import loadplugins
from .classgen import generateClass
from .classprocessor import readClass, processClass, debugClass
from .config import configloader, register
from gtool.core.utils.config import namespace as confignamespace
from gtool.core.namespace import namespace
from gtool.core.utils.output import parseformat, registerFormatter
from gtool.core.utils.runtime import registerruntimeoption
from gtool.core.utils.aggregatorprocessor import loadaggregators
from gtool.core.aggregatorregistry import registerAggregator

def loadconfig(projectroot):
    PROJECTDATA = "data"
    PROJECTCLASS = "classes"
    PROJECTCONFIG = "gtool.cfg"
    PROJECTPLUGINS = "plugins"
    PROJECTAGGREGATORS = "aggregates"

    projectclassroot = os.path.join(projectroot, PROJECTCLASS)
    projectdataroot = os.path.join(projectroot, PROJECTDATA)
    projectconfigpath = os.path.join(projectroot, PROJECTCONFIG)
    projectpluginroot = os.path.join(projectroot, PROJECTPLUGINS)
    projectaggregatespath = os.path.join(projectroot, PROJECTAGGREGATORS)

    register('config',
             {
                 'root': projectroot,
                 'classes': projectclassroot,
                 'dataroot': projectdataroot,
                 'configpath': projectconfigpath,
                 'plugin': projectpluginroot,
                 'aggregators': projectaggregatespath
             }
             )

    return confignamespace()['config']

def projectloader(projectroot, dbg=False, outputscheme=None):

    projectconfig = loadconfig(projectroot)

    __loadplugins(projectconfig['root'])
    __configloader(projectconfig['configpath'])

    if outputscheme is not None:
        __registeroption('outputscheme', outputscheme) # TODO confirm outputscheme exists

    if dbg:
        __registeroption('debug', dbg)

    __loadclasses(projectconfig['classes'], dbg=dbg)

    __loadaggregators(projectconfig['aggregators'])

    # loading output parser can only occur after all classes are loaded

    __outputparser(outputscheme=outputscheme) #TODO make this a functional style call <-- return namespace from __loadclasses
    return process(projectconfig['dataroot']) # returns the project data

def __registeroption(key, value):
    registerruntimeoption(key, value)

def __loadplugins(configpath, verbose=False, silent=False):
    loadplugins(configpath, verbose=verbose, silent=silent)

def __configloader(configpath):
    configloader(configpath)

def __loadclasses(classpath, verbose=False, silent=False, dbg=False):
    if os.path.isfile(classpath):
        __loadclass(classpath, verbose=verbose, silent=silent, dbg=dbg)
    elif os.path.isdir(classpath):
        for classfile in [f for f in os.listdir(classpath) if os.path.isfile(os.path.join(classpath, f))]:
            __loadclass(os.path.join(classpath, classfile), verbose=verbose, silent=silent, dbg=dbg)

def __outputparser(outputscheme=None):
    globalnamespace = namespace()
    if outputscheme is None:
        raise ValueError('An outputscheme was not provided, cannot build output format tree')
        #TODO implement a default outputscheme that displays everything in alpha order
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

def __loadclass(classpath, verbose=False, silent=False, dbg=False):
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
        generateClass(classname, classconfig, verbose=verbose)
    f.close()
    if not verbose and not silent:
        print('Registering %s user classes (use verbose mode to list them).' % len(classDict))

def __loadaggregators(aggregatespath, verbose=False, silent=False, dbg=False):
    if os.path.exists(aggregatespath):
        if os.path.isfile(aggregatespath):
            __loadaggregator(aggregatespath, verbose=verbose, dbg=dbg)
            if not verbose and not silent:
                print('Registering aggregators (use verbose mode to list them).')
        elif os.path.isdir(aggregatespath):
            aggregatefiles = [f for f in os.listdir(aggregatespath) if os.path.isfile(os.path.join(aggregatespath, f))]
            for aggregatefile in aggregatefiles:
                __loadaggregator(os.path.join(aggregatespath, aggregatefile), verbose=verbose, dbg=dbg)
            if not verbose and not silent:
                print('Registering %s aggregators (use verbose mode to list them).' % len(aggregatefiles))


def __loadaggregator(aggregatorpath, verbose=False, dbg=False):
    if os.path.exists(aggregatorpath):
        # TODO check if file is readable
        f = open(aggregatorpath, 'r')
        # TODO try except for file read errors
        aggregatorString = f.read()
    else:
        raise FileNotFoundError('%s does not exist' % aggregatorpath)
    # TODO capture exceptions
    aggregatorDataList =  loadaggregators(aggregatorString) #TODO get rid of \n by fixing attribute parser

    for aggregatorData in aggregatorDataList:
        if dbg is True:
            #debug(aggregatorData)
            print('aggregator debug not implemented yet')
        # TODO capture exceptions
        """
        for aggregatorname, aggregatorconfig in aggregatorData.items():
            # TODO capture exceptions
            print(aggregatorname,':', aggregatorconfig)
        """
        _id = aggregatorData['id']
        del aggregatorData['id']
        _config = aggregatorData
        registerAggregator(_id, _config, verbose=verbose)
    f.close()

def process(datapath):
    return StructureFactory.treewalk(datapath)

def debug(classdata):
    print('--- class debug ---')
    debugClass(classdata)
    print('--- end of class debug ---')