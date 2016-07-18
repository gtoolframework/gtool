from collections import defaultdict
from copy import deepcopy

import pyparsing as p

from gtool.core.filewalker import registerFileMatcher
from gtool.core.types.core import DynamicType


def init(self, **kwargs):
    # Deepcopy required otherwise list gets shared across instances of generated objects
    self.__list_slots__ = deepcopy(self.__list_slots__)
    self.kwargs = kwargs
    self.__createattrs__(self.kwargs)
    if not (isinstance(self, DynamicType)):
        # all dynamic classes must inherit from gtool's Dynamic type found in gtool.types.core
         raise TypeError('The dynamic class %s was generated that does not inherit from gtool.types.core.DynamicType' % self.__class__)
    #print('mandatory properties for %s' % type(self), self.__mandatory_properties__)


def new(cls):
    pass

# --- class methods that will be bound by factory ---
# must be outside of class factory or they get factory's context and not the manufactured objects
# TODO find a better plae to put these classmethods

@classmethod
def metas(cls):
    if hasattr(cls, '__metas__'):
        return cls.__metas__
    else:
        #print('has no metas')
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


# TODO __createattrs__ code is similar to setattr code, can probably be shared

def paramparser(params):
    # print(params)
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


def createattrs(self, kwargs):
    for attribClass in self.__list_slots__.keys():
        # TODO these should be explicity passed in
        # TODO __line_slots__ should be a class to ensure data integrity
        # TODO we're assuming that that attribclass is properly setup... need to check before reading
        base = self.__list_slots__[attribClass]
        classObject = base.attrtype

        if attribClass in kwargs.keys():
            # if passed in arguments contains initialization data for an attribute, continue...
            args = self.kwargs[attribClass]
            try:
                # if the init data is actually an object of the correct class
                base.__load__(args)
            except TypeError as terr:
                raise TypeError('In %s initialization of %s excepted %s but got %s and received: %s' % (
                type(self), attribClass, classObject, type(args), terr))


# TODO return some info about attribs
def repr(self):
    _dict = {prop: getattr(self, prop) for prop in self.dynamicproperties}
    return '%s: %s' % (self.__class__, _dict)


# TODO return some info about attribs
def str(self):
    strclass = "%s" % self.__class__
    strclass = strclass.split('.')[-1:][0][:-2]
    _dict = {prop: getattr(self, prop) for prop in self.dynamicproperties}
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
        return self.__list_slots__[attr]
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


@property
def mandatoryproperties(self):
    return self.__mandatory_properties__


@property
def missingproperties(self):
    return self.__missing_mandatory_properties__


@property
def missingoptionalproperties(self):
    return self.__missing_optional_properties__


def loads(self, loadstring, softload=False):
    """
    Method to read in a correctly structured string and load it into the object attributes
    :param loadstring:
    :return: True if data loaded
    """

    def parseLoadstring(loadstring):
        attributeStartMarker = p.LineStart() + p.Literal('@')
        attributeStopMarker = p.Literal(':')
        exp = attributeStartMarker.suppress() + p.Word(p.alphanums + '_') + attributeStopMarker.suppress()

        # ret = {}
        ret = defaultdict(list)

        for index, line in enumerate(loadstring.splitlines()):
            # print(line)
            # TODO switch from scanString to full parsing
            result = list(exp.scanString(line))
            if len(result) > 0:
                # TODO this is kludgy
                attribname = result[0][0][0]
                matchstart = result[0][1]
                matchend = result[0][2] + 1
                if matchstart == 0:
                    # print('matched on line %s' % index)
                    # print('%s: %s' % (attribname, line[matchend:]))
                    ret[attribname].append(line[matchend:])
                else:
                    raise Exception('attrib not at the start of the line')
            else:
                # print('no match on line %s' % index)
                # last = len(ret) - 1
                ret[attribname][-1:] = [ret[attribname][-1:][0] + "" + line.strip()]

        return ret

    def convertandload(_self, attrname, attrval):
        cfunc = _self.__list_slots__[attrname].__convert__
        attrfunc = _self.__list_slots__[attrname].attrtype

        return [attrfunc(cfunc(s.strip())) for s in attrval]

    ret = parseLoadstring(loadstring)
    attriblist = [k for k in ret.keys()]
    # check if all attribs required by class definition are in the data file
    for prop in self.__dynamic_properties__:
        # TODO don't raise for non-mandatory attribs
        if prop not in attriblist:
            if prop in self.__mandatory_properties__ and softload is False:
                raise AttributeError('attribute %s required by %s class definition file but not found' %
                                     (prop, self.__class__))
            if prop in self.__mandatory_properties__ and softload is True:
                self.__missing_mandatory_properties__.append(prop)
            if prop not in self.__mandatory_properties__:
                self.__missing_optional_properties__.append(prop)
    # reverse check of above and to ensure only attributes required by class file are present in data file
    for attrname, attrval in ret.items():
        if attrname not in self.__dynamic_properties__:
            raise AttributeError('attribute %s found in string but not in %s class definition file' %
                                 (attrname, self.__class__))
        else:
            # TODO load into object attribs
            # TODO pass in args (also refactor load so dict args are correct)
            try:
                self.__list_slots__[attrname].__load__(convertandload(self, attrname, attrval))
            except Exception as err:
                raise TypeError('got an error when trying to load data for %s: %s' % (self.__class__, err))

    return True if len(ret) > 0 else False


def load(self, loadfile, softload=False):
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
            _ret = self.loads(f.read(), softload=softload)
        except AttributeError as err:
            raise Exception('Reading %s: %s' % (loadfile, err))
        f.close()
        return _ret
