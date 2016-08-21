from abc import ABC, abstractmethod
from gtool.core.utils.output import checkalignment
import sys
from gtool.core.filewalker import StructureFactory
from gtool.core.utils.output import outputconfigname #, formatternamespace
from gtool.core.utils.runtime import runtimenamespace
from gtool.core.utils.config import namespace as confignamespace
from gtool.core.types.outputmanagers import Filler, AttributeMatch
from gtool.core.types.matrix import Matrix

class Output(ABC):

    """
    Output object, override __aligned__ on init
    """

    def __init__(self, aligned=None):
        if aligned is None:
            raise NotImplemented('Output classes must explicitly see aligned as True or False')
        self.__aligned__ = aligned

    def output(self, projectstructure):
        """
        Final output generator, should not be overriden without a call to isaligned() and __output__()
        :param projectstructure: a structurefactory object
        :return:
        """

        if not isinstance(projectstructure, StructureFactory.Container):
            raise TypeError('Expected StructureFactory.Container as argument but got %s' % type(projectstructure))

        self.isaligned(projectstructure)

        return self.__output__(projectstructure)

    def isaligned(self, projectstructure):
        """
        Checks for alignment if this output model requires aligned data.
        Aligned data means that all of the folder/class structures are a
        subset of the longest folder/class structure.

        Aligned output is useful for grid like output, such as excel.
        Unaligned output is useful for graph like outputs, such as json.
        :param projectstructure: a structurefactory object
        :return:
        """
        if self.__aligned__:
            try:
                checkalignment(projectstructure)
            except ValueError as err:
                print(err)
                sys.exit()

    @abstractmethod
    def __output__(self, projectstructure):
        """
        transforms projectstructure into final format.
        Should use output format string to process data object
        :param projectstructure: StructureFactory.Container
        :return: data in desired final format
        """
        # TODO call formatter, integrater and __output__ from DynamicType (moving it over first)
        pass

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

    """
    @classmethod
    def formatter(cls):
        _classname = '{}'.format(cls)[6:-2].split('.')[
            -1]  # TODO this is hacky - removes '<class and >' - use striptoclassname
        # print('formatter: dynamic props', cls.__dynamic_properties__)
        # print('formatter: list slots:', cls.__list_slots__)
        # for k, v in cls.__list_slots__.items():
        #    print(k, ':', v.isdynamic) # isinstance(v.__lazyloadclass__()(), DynamicType))

        return formatternamespace()[_classname]
    """

    class Separator(object):

        def __repr__(self):
            return '||'

    def fillerprocess(self, fillerobj):
        return '%s' % fillerobj.__fillertext__

    def attribprocess(self, attribobj, obj=None, sep=" ", outputscheme=None, flat=False):
        if obj is None:
            raise TypeError('Expected an object in obj kwarg')
        # TODO type check object
        if not hasattr(obj, attribobj.__attrname__):
            raise AttributeError('%s does not have a %s attribute as specified in the output format scheme:' % (
                obj.__class__, attribobj.__attrname__))

        if not getattr(obj, attribobj.__attrname__).isdynamic:
            _ret = sep.join(['%s' % f for f in getattr(obj, attribobj.__attrname__)])

            return _ret
        else:
            # TODO make this raise assert
            raise AttributeError('attribprocess should not process dynamic properties')

    def integrate(self, obj, grid=Matrix(), formatlist=None, separator=" "): #, outputscheme=None, flat=False):

        def __integratemultiple__(cell, obj):

            q = []

            for element in cell:

                if isinstance(element, Filler):
                    _x = self.fillerprocess(element)
                    q.append(_x)

                if isinstance(element, AttributeMatch):
                    if getattr(obj, element.__attrname__).isdynamic:
                        _startrow = grid.currentrow
                        if len(getattr(obj, element.__attrname__)) > 0:
                            outputconfig = self.__outputconfig__()
                            mergekey = 'merge'
                            mergeconstant = '\n\n'
                            mergeseparator = self.__separatorstrip__(outputconfig[mergekey]) if mergekey in outputconfig else mergeconstant

                            for i, dynobj in enumerate(getattr(obj, element.__attrname__)):
                                _grid = self.__xoutput__(dynobj) #, grid=result)
                                _grid.trim()
                                if _grid.height > 1:
                                    # TODO make this an assert
                                    raise ValueError('dynamic object should only return a matrix with a height of 1')

                                if (i+1) < len(getattr(obj, element.__attrname__)) > 1:
                                    # prevent trailing merge separators
                                    _x = '\n'.join(_grid.row(0)) + mergeseparator
                                else:
                                    _x = '\n'.join(_grid.row(0))
                                q.append(_x)
                        else:
                            # an empty dynamic attribute
                            q.append("")
                        grid.currentrow = _startrow
                    else:
                        _x = self.attribprocess(element, obj=_obj, sep=separator)
                        q.append(_x)

            return q

        def __integratesingle__(element, obj, grid):
            print('in __integratesingle__')
            _startrow = grid.currentrow

            c = grid.cursor
            for i, dynobj in enumerate(getattr(obj, element.__attrname__)):
                _grid = self.__xoutput__(dynobj)  # , grid=result)
                _grid.trim()
                if _grid.height > 1:
                    # TODO make this an assert
                    raise ValueError('dynamic object should only return a matrix with a height of 1')

                _x = '\n'.join(_grid.row(0))
                grid.insert(datalist=[_x], cursor=c)
                grid.nextrow()
                c =grid.cursor
                # insert
                # pop
                # move grid cursor
                # print('here!!:', cell)

            return True

        _obj = obj
        c = grid.cursor
        """
        Design Note
        ===========
        In grid output mode there is an assumption that attributes which are complex object will be represented as a single cell in the grid.
        If the complex object attribute is alone in its output cell it will separate multiples in to a new cell beneath it
        If the complex object attribute is in a cell that contain other attributes it will be concatenated in
        To create multiple discrete cells, create an monster object that contains all the required attributes (at some point we'll introduce inheritance in dynamic objects... maybe)
        """
        _depth = 1
        for i, cell in enumerate(formatlist):

            #q = []

            # if dynamic attribute is by itself (and is not zero length) then we stack otherwise we merge

            if len(cell) == 1 \
                    and isinstance(cell[0], AttributeMatch) \
                    and getattr(getattr(obj, cell[0].__attrname__, None), 'isdynamic', False) \
                    and len(getattr(obj, cell[0].__attrname__)) > 0:
                _depth = __integratesingle__(cell[0], obj, grid)
            else:
                q = __integratemultiple__(cell, obj)
                """
                for element in cell:

                    if isinstance(element, Filler):
                        _x = self.fillerprocess(element)
                        q.append(_x)

                    if isinstance(element, AttributeMatch):
                        if getattr(obj, element.__attrname__).isdynamic:
                            _startrow = grid.currentrow
                            if len(getattr(obj, element.__attrname__)) > 0:
                                outputconfig = self.__outputconfig__()
                                mergekey = 'merge'
                                mergeconstant = '\n\n'
                                mergeseparator = outputconfig[mergekey] if mergekey in outputconfig else mergeconstant

                                for dynobj in getattr(obj, element.__attrname__):
                                    _grid = self.__xoutput__(dynobj) #, grid=result)
                                    _grid.trim()
                                    if _grid.height > 1:
                                        # TODO make this an assert
                                        raise ValueError('dynamic object should only return a matrix with a height of 1')

                                    # TODO check here if this dynamic is by itself

                                    # if dynamic is by itself then we stack otherwise we merge
                                    if len(cell) == 1: #contains only this element in the cell
                                        _x = '\n'.join(_grid.row(0))
                                        # push
                                        grid.insert(datalist=[_x], cursor=c) #<-- this won't work - need to make _q a grid or work directly in grid
                                        # insert
                                        # pop
                                        # move grid cursor
                                        #print('here!!:', cell)
                                        pass
                                    else:
                                        _x = '\n'.join(_grid.row(0)) + mergeseparator
                                        q.append(_x)

                                    # if by itself, layer cells verticals
                                    # also set a next row
                            else:
                                # an empty dynamic attribute
                                q.append("")
                            grid.currentrow = _startrow
                        else:
                            _x = self.attribprocess(element, obj=_obj, sep=separator) #, outputscheme=outputscheme)
                            q.append(_x)
                """

                _q = ''.join(q)
                grid.insert(datalist=[_q], cursor=c)

                c = grid.cursor

        grid.carriagereturn(_depth)

    def __outputconfig__(self):
        outputscheme_id = runtimenamespace()['outputscheme']
        outputconfig = confignamespace()[outputconfigname(outputscheme_id)]

        return outputconfig

    def __separatorstrip__(self, separator):
        if (separator.startswith('"') and separator.endswith('"')) or (separator.startswith("'") and separator.endswith("'")):
            _separator = bytes('%s' % separator[1:-1], "utf-8").decode("unicode_escape")  # prevent escaping
        else:
            _separator = bytes('%s' % separator, "utf-8").decode("unicode_escape")  # prevent escaping
        return _separator

    def __xoutput__(self, obj, separatoroverride=None, grid=None): #outputscheme=None, flat=False,

        """
        Processes data into a grid. Returns data via reference.

        :param obj: a DynamicType object that will be processed for output
        :param separatoroverride: string to use for separating output
        :param flat: Boolean; merge the output
        :param grid: Matrix object to write results into
        :return:
        """
        def sub(self, obj, separatoroverride=None, grid=None): #, flat=False):
            outputconfig = self.__outputconfig__()

            separatorname = 'separator'

            if separatorname in outputconfig and separatoroverride is None:
                separator = self.__separatorstrip__(outputconfig[separatorname])
                """
                if separator.startswith('"') and separator.endswith('"'):
                    #separator = '%s' % separator [1:-1]
                    separator = bytes('%s' % separator [1:-1], "utf-8").decode("unicode_escape") # prevent escaping
                    #print('in output: *%s*' % separator)
                """
            else:
                separator = separatoroverride

            _formatlist = obj.__classoutputscheme__()
            # TODO add a len() method to dynamic class type to help with matrix width sizing
            _ret = self.integrate(obj,
                                  formatlist=_formatlist,
                                  separator=separator,
                                  grid=grid)

        if grid is None:
            grid = Matrix(startheight=20, startwidth=20)
        if isinstance(obj, list):
            _ret = [sub(self, _obj,
                        separatoroverride=separatoroverride,
                        grid=grid) for _obj in obj]
        else:
            _ret = sub(self, obj,
                       separatoroverride=separatoroverride,
                       grid=grid)

        return grid #_ret

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