import pyparsing as p

from gtool.core.utils.config import namespace as confignamespace
from gtool.core.types.matrix import Matrix
from gtool.core.utils.output import flatten, formatternamespace
from gtool.core.types.outputmanagers import Filler, AttributeMatch
from gtool.core.filewalker import registerFileMatcher


class CoreType(object):

    def __init__(self, *args, **kwargs):
        self.__valuetype__ = kwargs.pop('valuetype', None)
        if self.__valuetype__ == None:
            raise NotImplementedError('You need to specify a valuetype in keyword args')

        # assume singleton if not overridden
        # self.__singleton = kwargs.pop('singleton', True)

        initvalue = None
        if len(args) > 0:
            initvalue = args[0]
        self.__value__ = initvalue #None

    # TODO valid alternative repr requirements (if any)
    def __repr__(self):
        return '%s' % self.__value__

    def __str__(self):
        return '%s' % self.__value__

    def __validate__(self, validatedict):
        """
        Abstract Validation method, must be implemented by sub-classes.
        Must raise a ValueError if the value does not match the criteria
        Look at gtool.type.common for examples
        """
        raise NotImplementedError('Please implement a __validate__ method for your class %s' % self.__class__)

    @classmethod
    def __convert__(cls, item):
        try:
            return cls.__convertor__()(item)
        except ValueError:
            raise ValueError('cannot convert %s to type %s' %(item, cls.__convertor__()))

    # ==== MAGIC METHODS OVERRIDE ====
    """
    def append(self, item):
        print('append should not be a supported operation on types - attribute should handle lists of types')
        if self.issingleton() and len(self) > 0:
            raise TypeError('cannot add another item to a singleton')
        if self.listtype == None:
            raise NotImplementedError('You need to init self.listtype')
        if not isinstance(item, self.listtype):
            raise TypeError('item is not of type %s' % self.listtype)
        try:
            self.__validate__(item)
        except ValueError as err:
            raise ValueError(err)
        self.__list.append(item)  # append the item to itself (the list)

    # TODO implement other magic methods (if needed)


    def __getitem__(self, index):
        #print('index: ', index)
        if type(index) is not int:
            #print(tb.print_exc())
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            #print('caller name:', calframe[1][3])
            raise TypeError('indices must be integers or slides, not %s' % type(index))
        if not index + 1 < self.__len__():
            raise IndexError('index out of range')
        return self.__list[index]

    def __len__(self):
        return len(self.__list)

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('cannot add an other of type %s to a %s' % (type(other), type(self)))
        try:
            _ = iter(other)
        except TypeError:
            raise TypeError('In %s: %s is not iterable (contents: "%s")' % (type(other), other))
        if self.listtype == None:
            raise NotImplementedError('You need to init self.listtype')
        for i, item in enumerate(other):
            if not isinstance(item, self.listtype):
                raise TypeError('item %s in other list is not of type %s' % (i, self.listtype))
        _templist = copy(self.__list)
        _templist.extend(other)
        return type(self)(_templist)

        # TODO investigate if this is pattern is correct
        temp = copy(self)
        for item in other:
            temp.append(item)
        return temp

    def __radd__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('cannot add a %s to other of type %s to' % (type(self), type(other)))
        try:
            _ = iter(other)
        except TypeError:
            raise TypeError('In %s: %s is not iterable (contents: "%s")' % (type(other), other))
        if self.listtype == None:
            raise NotImplementedError('You need to init self.listtype')
        for i, item in enumerate(other):
            if not isinstance(item, self.listtype):
                raise TypeError('item %s in other list is not of type %s' % (i, self.listtype))
        # TODO investigate if this is pattern is correct
        _templist = copy(other.__list) #
        _templist.extend(self.__list)
        return type(self)(_templist)

    def __iadd__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('cannot add an other of type %s to a %s' % (type(other), type(self)))
        try:
            _ = iter(other)
        except TypeError:
            raise TypeError('In %s: %s is not iterable (contents: "%s")' % (type(other), other))
        if self.listtype == None:
            raise NotImplementedError('You need to init self.listtype')
        for i, item in enumerate(other):
            if not isinstance(item, self.listtype):
                raise TypeError('item %s in other list is not of type %s' % (i, self.listtype))
        self.__list.extend(other.__list)
        return self
    """

class DynamicType(object):

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

    @classmethod
    def metas(cls):
        if hasattr(cls, '__metas__'):
            return cls.__metas__
        else:
            # print('has no metas')
            return None

    @classmethod
    def displayname(cls):
        return cls.metas()['displayname'] if 'displayname' in cls.metas() else '%s' % cls

    @classmethod
    def formatter(cls):
        _classname = '{}'.format(cls)[6:-2].split('.')[-1] #TODO this is hacky - removes '<class and >'
        #print('formatter: dynamic props', cls.__dynamic_properties__)
        #print('formatter: list slots:', cls.__list_slots__)
        #for k, v in cls.__list_slots__.items():
        #    print(k, ':', v.isdynamic) # isinstance(v.__lazyloadclass__()(), DynamicType))

        return formatternamespace()[_classname]

    # TODO determine which methods from utils.classgen.methods can be moved in here

    def integrate(self, formatlist=None, separator=" ", outputscheme=None):
        #print('integrate seperator: *%s*' % separator)
        outstring = ""

        _obj = self

        for i, cell in enumerate(formatlist):
            for element in cell:
                if isinstance(element, Filler):
                    outstring += element.process()

                if isinstance(element, AttributeMatch):
                    outstring += element.process(obj=_obj, sep=separator, outputscheme=outputscheme)

            if (i + 1) == len(formatlist):
                pass
            else:
                outstring += '||'
            #print(outstring)
        return outstring

    def _integrate(self, formatlist=None, separator=" ", outputscheme=None):
        #print('integrate seperator: *%s*' % separator)

        _retmatrix = Matrix(startheight=5,startwidth=10)

        _datalist = []

        _obj = self

        for i, cell in enumerate(formatlist):
            _outstring = ""

            notsingle = False if len(cell) == 1 else True

            for element in cell:
                if isinstance(element, Filler):
                    _outstring += element.process()

                if isinstance(element, AttributeMatch):
                    _outstring += element.process(obj=_obj, sep=separator, outputscheme=outputscheme, flatten=notsingle)
                #if len(cell) == 1 then... recurse as matrix else recurse as flattened string
                #returns matrix <-- need a flattener
            #_datalist.append(_outstring)
            _retmatrix.insert(cursor=(0,0),datalist=[_outstring])

        return _retmatrix

    def __output__(self, outputscheme=None, separatoroverride=None, listmode=False):
        #--- validation section ---
        if not 'output' in confignamespace():
            raise AttributeError('An output section is not configured in the config file')
        if outputscheme == None:
            raise ValueError('No outputscheme provided for %s class' % self.__class__)
        if not outputscheme in confignamespace()['output']:
            raise NameError('%s is not configured in the [output] section in the config file' % outputscheme)
        _metas = self.metas() # assume metas() exist by virtue of class construction
        if not outputscheme in _metas:
            raise NameError('%s class does not have an output scheme called %s' % (self.__class__, outputscheme))
        # validation checks passed

        #--- separator handler ---
        separatorname = outputscheme + '_separator'
        #separator = " " # default value
        if separatorname in confignamespace()['output'] and separatoroverride is None:
            separator = confignamespace()['output'][separatorname]
            if separator.startswith('"') and separator.endswith('"'):
                #separator = '%s' % separator [1:-1]
                separator = bytes('%s' % separator [1:-1], "utf-8").decode("unicode_escape") # prevent escaping
                #print('in output: *%s*' % separator)
        else:
            separator = separatoroverride

        #print(confignamespace()['output'][outputscheme])
        if listmode:
            pass

        _formatlist = self.formatter()
        return self.integrate(formatlist=_formatlist, outputscheme=outputscheme, separator=separator)

    def __output2__(self, outputscheme=None, separatoroverride=None, matrix=None):
        #--- validation section ---
        if not 'output' in confignamespace():
            raise AttributeError('An output section is not configured in the config file')
        if outputscheme == None:
            raise ValueError('No outputscheme provided for %s class' % self.__class__)
        if not outputscheme in confignamespace()['output']:
            raise NameError('%s is not configured in the [output] section in the config file' % outputscheme)
        _metas = self.metas() # assume metas() exist by virtue of class construction
        if not outputscheme in _metas:
            raise NameError('%s class does not have an output scheme called %s' % (self.__class__, outputscheme))
        if not isinstance(matrix, Matrix):
            raise TypeError('Was expecting a matrix object for matrix keyword but got a', type(matrix))
        # validation checks passed

        #--- separator handler ---
        separatorname = outputscheme + '_separator'
        #separator = " " # default value
        if separatorname in confignamespace()['output'] and separatoroverride is None:
            separator = confignamespace()['output'][separatorname]
            if separator.startswith('"') and separator.endswith('"'):
                #separator = '%s' % separator [1:-1]
                separator = bytes('%s' % separator [1:-1], "utf-8").decode("unicode_escape") # prevent escaping
                #print('in output: *%s*' % separator)
        else:
            separator = separatoroverride

        #print(confignamespace()['output'][outputscheme])
        formatlist = self.formatter()
        return self.integrate(formatlist=formatlist, outputscheme=outputscheme, separator=separator)

    def output(self, outputscheme=None):
        return self.__output__(outputscheme=outputscheme)

    """
    def outputaslist(self, outputscheme=None):
        # TODO make this more efficient - get an array from integrate instead of a string
        _integratedstring = self.__output__(outputscheme=outputscheme, separatoroverride="\n", listmode=True)
        return _integratedstring.split('||')

    def outputasmatrix(self, outputscheme=None, returnmatrix=Matrix(startwidth=10, startheight=5)):
        if not isinstance(returnmatrix, Matrix):
            raise TypeError('Was exoecting a matrix object for returnmatrix keyword but got a', type(returnmatrix))
        _retmatrix = returnmatrix
        self.__output2__(outputscheme=outputscheme, separatoroverride="\n", listmode=True)

    def asdict(self):
        _retdict = {}
        _retdict[type(self)] = {}
    """