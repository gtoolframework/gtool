import pyparsing as p

from gtool.core.utils.config import namespace as confignamespace
from gtool.core.types.matrix import Matrix
from gtool.core.utils.output import flatten


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
    # TODO collapse Filler and AttributeMatch then subclass
    class __Filler(object):
        def __init__(self, fillertext):
            self.__fillertext__ = fillertext

        def process(self):
            return '%s' % self.__fillertext__

        def __repr__(self):
            return '<%s>:%s' % (self.__class__, self.__fillertext__)

    class __AttributeMatch(object):
        def __init__(self, attrname):
            self.__concatmode__ = True if attrname[0] == '+' else False
            self.__attrname__ = attrname[1:] if self.__concatmode__ is True else attrname
            #print('__AttributeMatch:', self.__attrname__, 'concat mode:', self.__concatmode__)

        def __isdynamic__(self, obj):
            return getattr(obj, self.__attrname__).isdynamic

        @property
        def isconcatter(self):
            return self.__concatmode__

        def process(self, obj=None, sep=" ", outputscheme = None, flat=False):
            if obj is None:
                raise TypeError('Expected an object in obj kwarg')
            if not hasattr(obj, self.__attrname__):
                raise AttributeError('%s does not have a %s attribute as specified in the output format scheme:' % (
                    obj.__class__, self.__attrname__))

            if not getattr(obj, self.__attrname__).isdynamic:
                return sep.join(['%s' % f for f in getattr(obj, self.__attrname__)])
            elif flat:
                return sep.join([f.output(outputscheme=outputscheme) for f in getattr(obj, self.__attrname__)])
            else:
                return


            #return sep.join(['%s' % f if not self.__isdynamic__(f) else f.output(outputscheme=outputscheme) for f in getattr(obj, self.__attrname__)])
            #return sep.join(['%s' % f for f in getattr(obj, self.__attrname__)])


        def process_to_list(self, obj=None, sep=" ", outputscheme=None):
            if hasattr(obj, self.__attrname__):
                """for g in getattr(obj, self.__attrname__):
                    if isinstance(g,DynamicType):
                        print(type(g))
                """
                # return sep.join(['%s' % f if not isinstance(f,DynamicType) else f.outputaslist(outputscheme=outputscheme) for f in getattr(obj, self.__attrname__)])
                return [f for f in getattr(obj, self.__attrname__)]
            else:
                raise AttributeError('%s does not have a %s attribute as specified in the output format scheme:' % (
                    obj.__class__, self.__attrname__))

        def __repr__(self):
            return '<%s>:%s' % (self.__class__, self.__attrname__)

    # TODO determine which methods from utils.classgen.methods can be moved in here
    def parseformat(self, formatstring):
        attribmarker = p.Literal('@').suppress()
        cellseparator = '||'
        concatmarker = p.Optional(p.Literal('+'))

        attribgroup = attribmarker + concatmarker + p.Word(p.alphanums)

        cells = []

        _splitstring = [cell.strip() for cell in formatstring.split(cellseparator)]

        for cell in _splitstring:
            _scan = attribgroup.scanString(cell)
            _templist = []
            prestart = 0
            end = 0
            for match in _scan:
                start = match[1]
                end = match[2]

                _templist.append(self.__Filler(cell[prestart:start]))
                _templist.append(self.__AttributeMatch(cell[start + 1:end]))
                prestart = end
                # print('templist:', _templist)
            _templist.append(self.__Filler(cell[end:]))
            cells.append(_templist)

        return cells

    def integrate(self, formatlist=None, separator=" ", outputscheme=None):
        #print('integrate seperator: *%s*' % separator)
        outstring = ""

        _obj = self

        for i, cell in enumerate(formatlist):
            for element in cell:
                if isinstance(element, self.__Filler):
                    outstring += element.process()

                if isinstance(element, self.__AttributeMatch):
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
                if isinstance(element, self.__Filler):
                    _outstring += element.process()

                if isinstance(element, self.__AttributeMatch):
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
        return self.integrate(formatlist=self.parseformat(_metas[outputscheme]),
                                  outputscheme=outputscheme,
                                  separator=separator)

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
        formatlist = self.parseformat(_metas[outputscheme])
        return self.integrate(formatlist=formatlist, outputscheme=outputscheme, separator=separator)

    def output(self, outputscheme=None):
        return self.__output__(outputscheme=outputscheme)

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