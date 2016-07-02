from gtool.filewalker import registerFileMatcher
from gtool.namespace import registerClass
from gtool.types.attributes import attribute
from distutils.util import strtobool
from .methods import *

# --- class methods that will be bound by factory ---
# must be outside of class factory or they get factory's context and not the manufactured objects
# TODO find a better plae to put these classmethods

@classmethod
def metas(cls):
    if hasattr(cls, '__metas__'):
        return cls.__metas__
    else:
        print('has no metas')
        return None

@classmethod
def classfile(cls):
    if 'file' in cls.metas():
        return cls.__metas__.get('file')
    else:
        return None

@classmethod
def register(cls, classname):
    # only register if a file prefix is provided
    if cls.classfile() is not None:
        registerFileMatcher(cls.classfile(), classname)

# --- end of class methods that will be bound by factory ---

class factory(object):
    """
    Generates classes given a class name and a correctly structured dictionary
    """

    # TODO look into overriding metaclass
    @staticmethod
    def generate(className, classDict, *args, **kwargs):
        """

        :param className: string containing name of class
        :param classDict: correctly structured dict from gtool.config
        :param args: arbitrary args
        :param kwargs: arbitrary keyword args
        :return: new manufactured class
        """
        # TODO do we need to call super().__new__()?

        x = factory.generateClass(className, classDict)
        return x # cls.generateClass(className, classDict)

    @staticmethod
    def merge_dicts(*args):
        _args = list(args)
        if len(_args) < 2:
            raise TypeError('expected at least 2 dicts')
        _retDict = _args.pop(0)
        for arg in _args:
            if not isinstance(arg, dict):
                raise TypeError('cannot merge %s into a dict' % type(arg))
            _retDict.update(arg)
        return _retDict

    # TODO check if these methods can be moved into CoreType


    # --- static methods use by class factory to generate new classes
    # TODO can all there methods be encapsulated to make this tidier?
    @staticmethod
    def methodbinder():
        methodsDict = {}
        methodsDict['__createattrs__'] = createattrs
        methodsDict['__init__'] = init
        # magic methods override = http://www.rafekettler.com/magicmethods.html
        methodsDict['__getattr__'] = getattr
        methodsDict['__setattr__'] = setattr
        methodsDict['dynamicproperties'] = dynamicproperties
        methodsDict['mandatoryproperties'] = mandatoryproperties
        methodsDict['missingproperties'] = missingproperties
        methodsDict['missingoptionalproperties'] = missingoptionalproperties
        methodsDict['classfile'] = classfile
        methodsDict['metas'] = metas
        methodsDict['register'] = register
        methodsDict['loads'] = loads
        methodsDict['load'] = load
        methodsDict['__repr__'] = repr
        methodsDict['__str__'] = str
        return methodsDict

    @staticmethod
    def attributes(className, classDict):
        attribsDict = {}
        attribsDict['__list_slots__'] = {}
        # TODO this could be computed by a method dynamically by looking for funcs/props that start with X
        attribsDict['__dynamic_properties__'] = []
        attribsDict['__mandatory_properties__'] = []
        attribsDict['__missing_mandatory_properties__'] = []
        attribsDict['__missing_optional_properties__'] = []
        for attributeName, attributeValues in classDict['attributes'].items():
            paramDict = {}
            if attributeValues['list']:
                paramDict['singleton'] = False
            elif not attributeValues['list']:
                paramDict['singleton'] = True
            else:
                # TODO all error messages should come from a standard library
                raise NotImplementedError('a class definition was processed '
                                          'improperly and is missing the list element from its dict')

            _kwargsdict = {i[0]:i[1] for i in attributeValues['args']['kwargs']}
            #print('kwargdict', _kwargsdict)
            try:
                paramDict['required'] = strtobool(_kwargsdict['required']) if 'required' in _kwargsdict else True
            except ValueError:
                raise ValueError('When parsing the required option for %s::%s got a value that could not be converted to a boolean' % (className, attributeName))

            # TODO would be better if the attribute was initialized by __init__
            attribsDict['__list_slots__'][attributeName] = \
                attribute(
                    #typeclass=globals()[attributeValues['type']],
                    typeclass=attributeValues['type'], # send over the name without accessing globals, let attribute handle that
                    singleton=paramDict['singleton'],
                    posargs=attributeValues['args']['posargs'] if 'posargs' in attributeValues['args'] else [],
                    kwargs=attributeValues['args']['kwargs'] if 'kwargs' in attributeValues['args'] else [],
                    parent=className,
                    attributename=attributeName,
                    required = paramDict['required']
                )
            attribsDict['__dynamic_properties__'].append(attributeName)

            # TODO make a method that dynamically queries dynamic prop list to determine in attribute is required
            if paramDict['required'] == True:
                attribsDict['__mandatory_properties__'].append(attributeName)
        return attribsDict

    @staticmethod
    def metasmaker(classDict):
        _retDict = {}
        if 'metas' in classDict:
            _retDict['__metas__'] = classDict['metas']
        return _retDict

    @staticmethod
    def maker(className, classDict, **kwargs):
        # TODO kwargs is never used... do we need it?

        return factory.merge_dicts(factory.attributes(className, classDict),
                                   factory.methodbinder(),
                                   factory.metasmaker(classDict)
                                   )

    @staticmethod
    def generateClassesDict(className, classDict, **kwargs):
        return factory.maker(className, classDict, **kwargs)

    @staticmethod
    def generateClass(className, classDict):
        return type(className, (), factory.generateClassesDict(className, classDict))


def generateClass(className, classDict):
    _newclass = factory.generate(className, classDict)
    registerClass(className, _newclass)
    # TODO no need to return the new class ist if registers correctly
    return _newclass