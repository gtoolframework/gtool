from gtool.types.common import Number, String, Choice
# TODO replace with plugin importer
import pyparsing as p
# import traceback as tb
# from gtool.namespace import namespace
from gtool.filewalker import registerFileMatcher
from gtool.namespace import registerClass
from copy import copy
from gtool.types.attributes import attribute

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
    # print('in register: classname is', self.__class__, 'and classfile is', self.classfile)
    # only register if a file prefix is provided
    if cls.classfile() is not None:
        registerFileMatcher(cls.classfile(), classname)

# --- end of class methods that will be bound by factory ---

class factory(object):
    """
    Generates classes given a class name and a correctly structured dictionary
    """

    # TODO look into overriding metaclass
    def __new__(cls, className, classDict, *args, **kwargs):
        """

        :param className: string containing name of class
        :param classDict: correctly structured dict from gtool.config
        :param args: arbitrary args
        :param kwargs: arbitrary keyword args
        :return: new manufactured class
        """
        # TODO do we need to call super().__new__()?
        return cls.generateClass(className, classDict)

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

    def init(self, **kwargs):
        self.__list_slots__ = copy(self.__list_slots__)
        self.__list_slots2__ = copy(self.__list_slots__)
        #self.__register__()
        self.kwargs = kwargs
        #print('init:', id(self.__list_slots__)) #why is this object shared across classes?
        self.__createattrs__(self.kwargs)
        self.__createattrsalt__(self.kwargs)


    # TODO __createattrs__ code is similar to setattr code, can probably be shared

    @staticmethod
    def paramparser(params):
        #print(params)
        # TODO this is a lot of work we should really do in gtool.utils.config with pyparsing and return proper dicts
        _retDict = {}

        if 'kwargs' in params.keys():
            _retDict['kwargs'] = {k[0]: k[1] for k in params['kwargs']}
        else:
            _retDict['kwargs'] = {}

        # parallel implemtation, get rid of the kwargs.singleton once complete
        if 'singleton' in params.keys():
            _retDict['kwargs']['singleton'] = params['singleton']
            _retDict['singleton'] = params['singleton']

        if 'posargs' in params.keys():
            _retDict['posargs'] = [k for k in params['posargs']]

        return _retDict

    def __createattrs__(self, kwargs):
        for attribClass in self.__list_slots2__.keys():
            # TODO these should be explicity passed in
            # TODO __line_slots__ should be a class to ensure data integrity
            # TODO we're assuming that that attribclass is properly setup... need to check before reading
            print('\nin createattralt: new loop')
            # print(self.__list_slots__[attribClass])
            base = self.__list_slots2__[attribClass]['init']
            classObject = base['class']
            params = base['args']

            if attribClass in kwargs.keys():
                # if passed in arguments contains initialization data for an attribute, continue...
                print('in createattralt new routine: matched to kwargs')
                args = self.kwargs[attribClass]
                if isinstance(args, classObject):
                    # if the init data is actually an object of the correct class
                    print('in createattralt new routine: got an instance')
                    pass
                    if args.issingleton() != params['singleton']:
                        # the object ordinality you attempted to add didn't match what the config required
                        raise TypeError('singleton state mismatch')
                    self.__list_slots2__[attribClass] = args
            else:
                # if passed in arguments do not initialization data for an attribute...
                # ... then create an empty attribute using init instructions
                print('in createattralt new routine: didn\'t matched to kwargs')
                _params = factory.paramparser(params)
                _obj = attribute(typeclass=classObject,
                                 singleton=_params['singleton'],
                                 posargs=_params['posargs'],
                                 kwargs=_params['kwargs']
                                 )
                #_obj = classObject(*_params['posargs'], **_params['kwargs'])
                self.__list_slots2__[attribClass] = _obj

    def __createattrsprime__(self, kwargs):
        for attribClass in self.__list_slots__.keys():
            # TODO these should be explicity passed in
            # TODO __line_slots__ should be a class to ensure data integrity
            # TODO we're assuming that that attribclass is properly setup... need to check before reading

            #print(self.__list_slots__[attribClass])
            base = self.__list_slots__[attribClass]['init']
            classObject = base['class']
            params = base['args']

            # check if objects are being passed into the attribs
            # check if passed kwarg matches the name of an attribute
            if attribClass in kwargs.keys():
                args = self.kwargs[attribClass]
                # check if passed object is correct type
                if isinstance(args, classObject):
                    # check if passed object has correct constraints and ordinality
                    _params = factory.paramparser(params)['kwargs']
                    for validator in [k for k in args.validators.keys()]:
                        validatorvalue = _params.get(validator, None)
                        if validatorvalue is not None:
                            validatorvalue = args.convert(validatorvalue)
                        if validatorvalue != args.validators[validator]:
                            raise TypeError('The %s constraint was expected to %s but we got %s' % (validator, validatorvalue, args.validators[validator]))
                    # TODO --- call validate but with the metas
                    if args.issingleton() != params['singleton']:
                        raise TypeError('singleton state mismatch')
                    self.__list_slots__[attribClass] = args
                else:
                    # initialize the object and replace the dict containing build instructions
                    _params = factory.paramparser(params)
                    self.__list_slots__[attribClass] = classObject(args, **_params['kwargs'])
            else:
                # initialize the object and replace the dict containing build instructions
                _params = factory.paramparser(params)
                _obj = classObject(*_params['posargs'], **_params['kwargs'])
                self.__list_slots__[attribClass] = _obj

    # TODO return some info about attribs
    def repr(self):
        _dict = {prop: getattr(self, prop) for prop in self.dynamicproperties}
        return '%s: %s' % (self.__class__, _dict)

    # TODO return some info about attribs
    def str(self):
        strclass = "%s" % self.__class__
        strclass = strclass.split('.')[-1:][0][:-2]
        _dict = {prop: getattr(self,prop) for prop in self.dynamicproperties}
        return '%s: %s' % (strclass, _dict)

    def getattr(self, attr):
        """
        an "anonymous" function that will be included into the dynamically generated class to made dynamically
        generated properties exist.
        :param self: object instance
        :param attr: name of object attribute after the dot notation
        :return: list
        """
        if attr in self.__list_slots__:
            return self.__list_slots__[attr].__value__
        elif attr in self.__dict__:
            return self.__dict__[attr]
        else:
            raise AttributeError('%s does not exist' % attr)

    def setattr(self, attr, item):
        """
        Replace an existing dynamic property or set it. Will only allow the property to set with a fully
        formed object instance that matches the required dynamic properties set by classgen
        :param self:
        :param attr:
        :param item:
        :return:
        """

        # TODO flatten/simplify nested logic
        # TODO this code is partially shared with __createattrs__ code for doing the same thing
        if attr in self.__list_slots__.keys():
            self.__list_slots__[attr].__set__(item)
        else:
            # setting a method using dot notation (self.attr) will trigger recursion unless we have this
            # else handler
            self.__dict__[attr] = item

    @property
    def dynamicproperties(self):
        return self.__dynamic_properties__

    """
    @classmethod
    def metas(cls):
        #print(dir(cls))
        if hasattr(cls, '__metas__'):
            print('has metas')
            return cls.__metas__
        else:
            print('has no metas')
            return None

    @classmethod
    def classfile(cls):
        print('in classfile:', cls.metas())
        if 'file' in cls.metas():
            return cls.__metas__.get('file')
        else:
            return None


    @classmethod
    def register(cls, classname):
        #print('in register: classname is', self.__class__, 'and classfile is', self.classfile)
        registerFileMatcher(cls.classfile(), classname)
    """

    def loads(self, loadstring):
        attributeStartMarker = p.LineStart() + p.Literal('@')
        attributeStopMarker = p.Literal(':')
        exp = attributeStartMarker.suppress() + p.Word(p.alphanums + '_') + attributeStopMarker.suppress()

        ret = {}

        for index, line in enumerate(loadstring.splitlines()):
            # print(line)
            result = list(exp.scanString(line))
            if len(result) > 0:
                attribname = result[0][0][0]
                matchstart = result[0][1]
                matchend = result[0][2] + 1
                if matchstart == 0:
                    # print('matched on line %s' % index)
                    # print('%s: %s' % (attribname, line[matchend:]))
                    ret[attribname] = line[matchend:]
                else:
                    raise Exception('attrib not at the start of the line')
            else:
                # print('no match on line %s' % index)
                last = len(ret) - 1
                ret[attribname] += " " + line.strip()

        attriblist = [k for k in ret.keys()]


        # print('--- mandatory attribute check ---')
        # check if all attribs required by class definition are in the data file
        for prop in self.__dynamic_properties__:
            # TODO don't raise for non-mandatory attribs
            if prop not in attriblist:
                raise AttributeError('attribute %s required by %s class definition file but not found' %
                                     (prop, self.__class__))

        # print('--- attribute load ---')
        # reverse check of above and to ensure only attributes required by class file are present in data file
        for attrname, attrval in ret.items():
            if attrname not in self.__dynamic_properties__:
                raise AttributeError('attribute %s found in string but not in %s class definition file' %
                                     (attrname, self.__class__))
            else:
                # TODO load into object attribs
                # print('%s: %s' % (attrname, attrval))
                # TODO pass in args (also refactor load so dict args are correct)
                try:
                    #self.__createattrs__(ret)
                    # TODO why is is this an instance already and not the class?
                    _validated = self.__list_slots__[attrname].prepare(attrval)
                    self.__list_slots__[attrname].append(_validated)
                except Exception as err:
                    #print(tb.print_exc())
                    print('got an error when trying to load data for %s: %s' % (self.__class__, err))
        return True if len(ret) > 0 else False

    def load(self, loadfile):

        _ret = False

        # TODO make sure we can read file (in case it's large)
        try:
            f = open(loadfile, mode='r')
        except FileNotFoundError:
            raise FileNotFoundError('%s does not exist' % loadfile)
        except IOError:
            raise IOError('could not open %s' % loadfile)
        except Exception:
            raise Exception('attempted to to read %s and got an exception' % loadfile)
        else:
            try:
                _ret = self.loads(f.read())
            except AttributeError as err:
                raise Exception('Reading %s: %s' % (loadfile, err))
            f.close()
            return _ret

    # --- static methods use by class factory to generate new classes
    # TODO can all there methods be encapsulated to make this tidier?
    @staticmethod
    def methodbinder():
        methodsDict = {}
        methodsDict['__createattrs__'] = factory.__createattrs__
        methodsDict['__createattrsalt__'] = factory.__createattrsalt__
        methodsDict['__init__'] = factory.init
        # magic methods override = http://www.rafekettler.com/magicmethods.html
        methodsDict['__getattr__'] = factory.getattr
        methodsDict['__setattr__'] = factory.setattr
        methodsDict['dynamicproperties'] = factory.dynamicproperties
        methodsDict['classfile'] = classfile
        methodsDict['metas'] = metas
        methodsDict['register'] = register
        methodsDict['loads'] = factory.loads
        methodsDict['load'] = factory.load
        methodsDict['__repr__'] = factory.repr
        methodsDict['__str__'] = factory.str
        return methodsDict

    @staticmethod
    def attributes(classDict):
        attribsDict = {}
        attribsDict['__list_slots__'] = {}
        # TODO this could be computed by a method dynamically by looking for funcs/props that start with X
        attribsDict['__dynamic_properties__'] = []
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
            """
            attribsDict['__list_slots__'][attributeName] = \
                {
                    'init': {
                        'class': globals()[attributeValues['type']],
                        'args': {
                            'singleton': paramDict['singleton'],
                            'posargs': attributeValues['args']['posargs'] if 'posargs' in attributeValues['args'] else [],
                            'kwargs': attributeValues['args']['kwargs'] if 'kwargs' in attributeValues['args'] else [],
                        },
                    'store': []
                    }
                }
            """
            attribsDict['__list_slots__'][attributeName] = \
                attribute(
                    typeclass=globals()[attributeValues['type']],
                    singleton=paramDict['singleton'],
                    posargs=attributeValues['args']['posargs'] if 'posargs' in attributeValues['args'] else [],
                    kwargs=attributeValues['args']['kwargs'] if 'kwargs' in attributeValues['args'] else []
                )
            attribsDict['__dynamic_properties__'].append(attributeName)
        return attribsDict

    @staticmethod
    def metasmaker(classDict):
        _retDict = {}
        if 'metas' in classDict:
            _retDict['__metas__'] = classDict['metas']
        #print('in metamaker:', _retDict)
        return _retDict

    @staticmethod
    def maker(classDict, **kwargs):
        # TODO kwargs is never used... do we need it?

        return factory.merge_dicts(factory.attributes(classDict),
                                   factory.attributes2(classDict),
                                   factory.methodbinder(),
                                   factory.metasmaker(classDict)
                                   )

    @staticmethod
    def generateClassesDict(classDict, **kwargs):
        return factory.maker(classDict, **kwargs)

    @staticmethod
    def generateClass(className, classDict):
        return type(className, (), factory.generateClassesDict(classDict))


def generateClass(className, classDict):
    #print(type(factory(className, classDict)()))
    #_newclass = factory.generateClass(className, classDict)
    _newclass = factory(className, classDict)
    registerClass(className, _newclass)
    #_newclass.register(className)
    return _newclass