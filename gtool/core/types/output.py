from abc import ABC, abstractmethod
from gtool.core.utils.output import checkalignment, recursioncheck
import sys
from gtool.core.filewalker import StructureFactory
from gtool.core.utils.output import outputconfigname
from gtool.core.utils.runtime import runtimenamespace
from gtool.core.utils.config import namespace as confignamespace
from gtool.core.types.outputmanagers import Filler, AttributeMatch
from gtool.core.types.matrix import Matrix
from gtool.core.filewalker import striptoclassname

class Output(ABC):

    """
    Output object, override __aligned__ on init
    """

    def __init__(self, aligned=None):
        if aligned is None:
            raise NotImplemented('Output classes must explicitly set keyword arg aligned as True or False')
        self.__aligned__ = aligned

    def output(self, projectstructure, output=None):
        """
        Final output generator, should not be overriden without a call to isaligned() and __output__()
        :param projectstructure: a structurefactory object
        :param outputfile: destination file
        :return:
        """

        if not isinstance(projectstructure, StructureFactory.Container):
            raise TypeError('Expected StructureFactory.Container as argument but got %s' % type(projectstructure))

        self.isnotrecursive(projectstructure)
        self.isaligned(projectstructure)

        return self.__output__(projectstructure, output=output)

    def isnotrecursive(self, projectstructure):
        try:
            recursioncheck(projectstructure)
        except ValueError as err:
            print(err)
            sys.exit()

    def isaligned(self, projectstructure):
        """
        Checks for alignment if this output model requires aligned data.
        Aligned data means that all of the folder/class structures are a
        subset of the longest folder/class structure.

        Aligned output is useful for grid like output, such as excel.
        Unaligned output is useful for graph like outputs, such as json.
        :param projectstructure: a structurefactory object
        :return: None
        """
        if self.__aligned__:
            try:
                checkalignment(projectstructure)
            except ValueError as err:
                print(err)
                sys.exit()

    @abstractmethod
    def __output__(self, projectstructure, output=None):
        """
        transforms projectstructure into final format.
        Should use output format string to process data object
        :param projectstructure: StructureFactory.Container
        :param outputfile: destination file
        :return: data in desired final format
        """
        # TODO call formatter, integrater and __output__ from DynamicType (moving it over first)
        pass

    def __outputconfig__(self):
        outputscheme_id = runtimenamespace()['outputscheme']
        outputconfig = confignamespace()[outputconfigname(outputscheme_id)]

        return outputconfig

class GridOutput(Output):
    """
    Output subclass for output that has aligned columns. Must override self.__output__

    Example
    =======

    x y z
    x y
    x
    """

    def __init__(self):
        super(GridOutput, self).__init__(aligned=True)

    @abstractmethod
    def __output__(self, projectstructure, output=None):
        """
        transforms projectstructure into final format.
        Should use output format string to process data object
        :param projectstructure: StructureFactory.Container
        :param outputfile: destination file
        :return: data in desired final format
        """
        structure = projectstructure.dataasobject
        _grid = self.__gridoutput__(structure)
        _grid.trim()
        return _grid

    class Separator(object):

        def __repr__(self):
            return '||'

    def __getheaders__(self, obj):
        """
        Generates headers from a formatlist (non-resursive)
        :param formatlist: list of output managers
        :return: list of header strings
        """

        _formatdict = obj.__classoutputscheme__() #TODO if headers exists then use that instead

        formatlist = _formatdict['format']

        formatheaders = None

        if 'headers' in _formatdict:
            formatheaders = _formatdict['headers']

        # use the headers provided by the user
        if formatheaders is not None:
            _headers = [header.strip() for header in formatheaders.split('||')]
            _retlist = []

            if len(_headers) != len(formatlist):
                raise ValueError('Class %s has an output.header definition that '
                                 'is not the same number of cells as the '
                                 'output format string' % striptoclassname(type(obj)))

            for i, cell in enumerate(formatlist):
                for element in cell:
                    if isinstance(element, AttributeMatch):
                        if not element.isconcatter and getattr(getattr(obj, element.__attrname__, None), 'isdynamic',
                                                               False):
                            attr = getattr(obj, element.__attrname__, None)
                            _attrtype = attr.attrtype()
                            _retlist.extend(self.__getheaders__(_attrtype))
                        else:
                            _retlist.append(_headers[i])
                    elif isinstance(element, Filler) and len(cell) == 1:
                        _retlist.append(_headers[i])
            return _retlist


        # generate headers if the user didn't provide headers
        if formatheaders is None:
            _retlist = []

            for cell in formatlist:
                for element in cell:
                    if isinstance(element, AttributeMatch):
                        if not element.isconcatter and getattr(getattr(obj, element.__attrname__, None), 'isdynamic', False):
                            attr = getattr(obj, element.__attrname__, None)
                            _attrtype = attr.attrtype()
                            _retlist.extend(self.__getheaders__(_attrtype))
                        else:
                            _retlist.append(element.__attrname__)
                    elif isinstance(element, Filler) and len(cell) == 1:
                        # handle formatting cells that only contain static Filler text
                        _retlist.append('')
            return _retlist

    def fillerprocess(self, fillerobj):
        return '%s' % fillerobj.__fillertext__

    def attribprocess(self, attribobj, obj=None, sep=" "):
        if obj is None:
            raise TypeError('Expected an object in obj kwarg')
        # TODO type check object
        if not hasattr(obj, attribobj.__attrname__):
            raise AttributeError('%s does not have a %s attribute as specified in the output format scheme:' % (
                obj.__class__, attribobj.__attrname__))

        #if not getattr(obj, attribobj.__attrname__).isdynamic:
        _attrib = getattr(obj, attribobj.__attrname__)
        if  striptoclassname(type(_attrib)) == 'attribute':
            _ret = sep.join(['%s' % f for f in _attrib])
        else:
            _ret = '%s' % _attrib
        return _ret
        #else:
        #    # TODO make this raise assert
        #    raise AttributeError('attribprocess should not process dynamic properties')

    def dynattribprocess(self, obj, element):
        """
        Process a dynamic attribute into a single string and then returns as a list
        :param obj: object for processing
        :param element: formatting element
        :return: list of strings
        """
        q = []
        if len(getattr(obj, element.__attrname__)) > 0:
            outputconfig = self.__outputconfig__()
            mergekey = 'merge'
            mergeconstant = '\n\n'
            mergeseparator = self.__separatorstrip__(
                outputconfig[mergekey]) if mergekey in outputconfig else mergeconstant

            for i, dynobj in enumerate(getattr(obj, element.__attrname__)):
                _grid = self.__gridoutput__(dynobj, headers=False)  # , grid=result)
                _grid.trim()
                if _grid.height > 1:
                    # TODO make this an assert
                    raise ValueError('dynamic object should only return a matrix with a height of 1')

                if (i + 1) < len(getattr(obj, element.__attrname__)):  # > 1:
                    # prevent trailing merge separators
                    _x = '\n'.join(_grid.row(0)) + mergeseparator
                else:
                    _x = '\n'.join(_grid.row(0))
                q.append(_x)
        else:
            # an empty dynamic attribute
            q.append("")
        return q #TODO should this be returning a joined string instead of a list

    def integrate(self, obj, grid=Matrix(), formatlist=None, separator=" "):
        """
        Process an object into grid structure

        :param obj: the input object, must from StructureFactory
        :param grid: Maxtrix object, where the results are written
        :param formatlist: A list of lists containing outmanagers
        :param separator:
        :return:
        """

        """
        Design Note
        ===========
        In grid output mode there is an assumption that attributes which are complex object will be represented as a single cell in the grid.
        If the complex object attribute is alone in its output cell it will separate multiples in to a new cell beneath it
        If the complex object attribute is in a cell that contain other attributes it will be concatenated in
        To create multiple discrete cells, create an monster object that contains all the required attributes (at some point we'll introduce inheritance in dynamic objects... maybe)
        """

        def __integratemultiple__(cell, obj):

            q = []

            for element in cell:
                _x = None
                if isinstance(element, Filler):
                    _x = self.fillerprocess(element)
                elif isinstance(element, AttributeMatch):
                    _attrib = getattr(obj, element.__attrname__)
                    attribIsDynamic = False

                    try:
                        attribIsDynamic = _attrib.isdynamic
                    except:
                        pass
                    if attribIsDynamic:
                        _x = self.dynattribprocess(obj, element)
                        q.extend(_x) #TODO this should be consistent with the appends below
                    else:
                        _x = self.attribprocess(element, obj=obj, sep=separator) # TODO <-- fix use of separator
                        q.append(_x)
                else:
                    raise TypeError('element in formatting cell is neither a Filler or an Attribute')
            return q

        def __integratesingle__(element, obj, grid):
            _startrow = grid.y

            c = grid.cursor
            _obj = getattr(obj, element.__attrname__)


            for i, dynobj in enumerate(_obj):
                _grid = self.__gridoutput__(dynobj, headers=False)  # , grid=result)
                _grid.trim()
                if _grid.height > 1:
                    # TODO make this an assert
                    raise ValueError('dynamic object should only return a matrix with a height of 1')
                if element.isconcatter:
                    _x = ['\n'.join(_grid.row(0))]
                else:
                    _x = _grid.row(0)
                grid.insert(datalist=_x, cursor=c)
                if (i+1) < len(_obj):
                    grid.nextrow()
                    grid.x -= len(_x)
                c = grid.cursor

            _endrow = grid.y
            depth = _endrow - _startrow
            return depth

        def __integrateemptysingle__(element, obj, grid):
            count = 0
            c = grid.cursor
            if element.isconcatter:
                _x = ['']
            else:
                _obj = getattr(obj, element.__attrname__)
                _attrtype = _obj.attrtype()
                _formatlist = _attrtype.__classoutputscheme__()
                for _element in _formatlist:
                    count += 1
                _x = [''] * count
            grid.insert(datalist=_x, cursor=c)

        #_obj = obj
        c = grid.cursor
        _depth = 1
        for cell in formatlist:
            # if dynamic attribute is by itself (and is not zero length) then we stack otherwise we merge
            if len(cell) == 1 \
                    and isinstance(cell[0], AttributeMatch) \
                    and getattr(getattr(obj, cell[0].__attrname__, None), 'isdynamic', False):
                if len(getattr(obj, cell[0].__attrname__)) > 0:
                    _depth = __integratesingle__(cell[0], obj, grid)
                    if _depth > 0:
                        grid.y -= _depth
                        _depth *= 2
                    else:
                        _depth = 1
                else:
                    __integrateemptysingle__(cell[0], obj, grid)
                c = grid.cursor
            else:
                q = __integratemultiple__(cell, obj)
                _q = ''.join(q)
                grid.insert(datalist=[_q], cursor=c)

                c = grid.cursor

        grid.carriagereturn(_depth)
        return True

    def __separatorstrip__(self, separator):
        if (separator.startswith('"') and separator.endswith('"')) or (separator.startswith("'") and separator.endswith("'")):
            _separator = bytes('%s' % separator[1:-1], "utf-8").decode("unicode_escape")  # prevent escaping
        else:
            _separator = bytes('%s' % separator, "utf-8").decode("unicode_escape")  # prevent escaping
        return _separator

    def __gridoutput__(self, obj, separatoroverride=None, grid=None, headers=True): #TODO is grid kwarg needed?

        """
        Processes data into a grid. Returns data via reference.

        :param obj: a DynamicType object that will be processed for output
        :param separatoroverride: string to use for separating output
        :param flat: Boolean; merge the output
        :param grid: Matrix object to write results into
        :return:
        """
        def sub(self, obj, separatoroverride=None, grid=None):
            outputconfig = self.__outputconfig__()

            separatorname = 'separator'

            if separatorname in outputconfig and separatoroverride is None:
                separator = self.__separatorstrip__(outputconfig[separatorname])
            else:
                separator = separatoroverride

            _formatlist = obj.__classoutputscheme__()['format']
            # TODO add a len() method to dynamic class type to help with matrix width sizing
            self.integrate(obj, formatlist=_formatlist, separator=separator, grid=grid)

        if grid is None:
            grid = Matrix(startheight=20, startwidth=20)

        if isinstance(obj, list) and headers:
                grid.insert(datalist=self.__getheaders__(obj[0]))
                grid.carriagereturn()
        elif headers:
                grid.insert(datalist=self.__getheaders__(obj))
                grid.carriagereturn()

        if isinstance(obj, list):
            for _obj in obj:
                sub(self, _obj, separatoroverride=separatoroverride, grid=grid)
        else:
            sub(self, obj, separatoroverride=separatoroverride, grid=grid)

        return grid

# WARNING DO NOT RENAME THIS CLASS - there is a static text value in
# core.utils.output.checkalignment that is used to determine class lineage
# without a circular import occuring
class TreeOutput(Output):
    """
    Output subclass for hierarchical output that may not be aligned. Must override self.__output__

    Example
    =======

    a
     b
      b
       c
    c
     b
      a
    """

    def __init__(self):
        super(TreeOutput, self).__init__(aligned=False)

    def integrate(self, obj):
        """
        Read the format string in the class and output a list of attributes

        :param obj: DynamicType
        :return: list of attributes
        """

        formatlist = obj.__classoutputscheme__()['format']
        if formatlist is None:
            return None

        _keylist = []

        for cell in formatlist:
            if len(cell) > 1:
                raise ValueError('Tree based output plugins do not '
                                 'support multiple attributes in a single '
                                 'cell; found in %s' % striptoclassname(type(obj)))

            for element in cell:
                if isinstance(element, Filler):
                    _filler = '%s' % element
                    if not _filler.isspace():
                        raise ValueError('Tree based output plugins do not '
                                         'support non-attribute values, such '
                                         'as %s in %s, in the format string' % (element, striptoclassname(type(obj))))
                elif isinstance(element, AttributeMatch):
                    _keylist.append(element.__attrname__)
                else:
                    raise TypeError('Received an unexpected value of '
                                    'type %s in class %s\'s format '
                                    'string' % (type(element), striptoclassname(type(obj))))

        return _keylist

    @abstractmethod
    def filter(self, obj):
        """
        Override this method in your output plugin to change how format string is handled

        :param obj: a DynamicType
        :return: a list of attributes, read from the class formatter, to render in outputprocessor
        """

        _filteredattribs = self.integrate(obj)
        _retlist = _filteredattribs

        return _retlist

    def headers(self, obj):
        _retlist = None
        _ret = obj.__classoutputscheme__().get('headers', None)
        if _ret is not None:
            _retlist = [i.strip() for i in _ret.split('||')]
            pass
        return _retlist

    @abstractmethod
    def outputprocessor(self, projectstructure):

        """
        Takes the tree structure read by __output__ and converts into a final form.
        :param projectstructure: must be a list or a dict containing DynamicType objects
        :return:
        """
        # TODO implement a type validator
        raise NotImplemented('output processor must be implemented ')

    @abstractmethod
    def convert(self, obj): #, filterfunction=None):
        """
        Converts dynamictype object into dict.
        self.filter is called from within if the class format string is used.
        Override if different behaviour required.
        :param obj: dynamictype object
        :return: nested dict of values
        """

        attrlist = [k for k, v in obj]

        if hasattr(self, 'filter'):
            _filterlist = self.filter(obj)
            if not isinstance(_filterlist, list) and _filterlist is not None:
                raise TypeError(
                    'filter method in "%s" did not return a list, '
                    'it returned a %s' % (striptoclassname(type(self)), type(_filterlist)))

        headers = None
        if _filterlist is not None:
            attrlist = _filterlist
            headers = self.headers(obj)

        if headers is not None:
            if len(attrlist) != len(headers):
                raise ValueError('headers and output format in class %s '
                                 'are not the same length' % striptoclassname(type(obj)))

        _retdict = {}
        for i, k in enumerate(attrlist): #, v in obj:
            v = getattr(obj, k)
            if striptoclassname(type(v)) == 'attribute':
                if not v.isdynamic:
                    _v = [attr.raw() for attr in v]
                    _v = _v[0] if len(_v) == 1 else _v
                else:
                    _v = [self.convert(_obj) for _obj in v]
                    _v = _v[0] if len(_v) == 1 else _v
            else:
                _v = v

            key = k if headers is None else headers[i]
            _retdict[key] = _v
        return _retdict

    def __output__(self, projectstructure, output=None): # TODO use output

        """
        Processes data into a tree in accordance with outputscheme.

        :param obj: a DynamicType object that will be processed for output
        :param output: Output target location (not used by base class, should be used by inheriting class)
        :return: list or dict
        """

        def _sub(tree):
            if tree.haschildren:
                return [_sub(child) for child in tree.children]
            else:
                _obj = tree.dataasobject
                return {tree.name: _obj}

        _output = _sub(projectstructure)

        return self.outputprocessor(_output)

class TemplatedOutput(Output):
    pass