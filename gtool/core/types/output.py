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
        #elif flat:
        #    return sep.join([f.output(outputscheme=outputscheme) for f in getattr(obj, self.__attrname__)])
        else:
            #raise NotImplementedError('still working on Attributematch.process')
            return 'monkey'

    def integrate(self, obj, grid=Matrix(), formatlist=None, separator=" "): #, outputscheme=None, flat=False):
        #print('integrate seperator: *%s*' % separator)
        #outstring = ""

        _obj = obj

        #print(result.cursor)

        c = grid.cursor
        """
        Design Note
        ===========
        In grid output mode there is an assumption that attributes which are complex object will be represented as a single cell in the grid.
        If the complex object attribute is alone in its output cell it will separate multiples in to a new cell beneath it
        If the complex object attribute is in a cell that contain other attributes it will be concatenated in
        To create multiple discrete cells, create an monster object that contains all the required attributes (at some point we'll introduce inheritance in dynamic objects... maybe)
        """
        for i, cell in enumerate(formatlist):
            #_outstring = ""
            q = []
            for element in cell:
                if isinstance(element, Filler):
                    _x = self.fillerprocess(element)
                    q.append(_x)
                    #_outstring += _x

                if isinstance(element, AttributeMatch):
                    if getattr(obj, element.__attrname__).isdynamic:
                        _startrow = grid.currentrow
                        #print('current row:', _startrow)
                        if len(getattr(obj, element.__attrname__)) > 0:
                            outputconfig = self.__outputconfig__()
                            mergekey = 'merge'
                            mergeconstant = '\n\n'
                            mergeseparator = outputconfig[mergekey] if mergekey in outputconfig else mergeconstant

                            for dynobj in getattr(obj, element.__attrname__):
                                _grid = self.__xoutput__(dynobj) #, grid=result)
                                _grid.trim()
                                #print(_x.__v_utilization__())
                                #for row in _grid:
                                #    print(row)
                                #print(_grid.row(0))
                                if _grid.height > 1:
                                    # TODO make this an assert
                                    raise ValueError('dynamic object should only return a matrix with a height of 1')
                                _x = '\n'.join(_grid.row(0)) + mergeseparator
                                q.append(_x)

                                # if by itself, layer cells verticals
                                # also set a next row
                        else:
                            print('empty dynamic')
                        #print('height', grid.height)
                        grid.currentrow = _startrow
                    else:
                        _x = self.attribprocess(element, obj=_obj, sep=separator) #, outputscheme=outputscheme)
                        q.append(_x)
                        #_outstring += _x

            _q = ''.join(q)
            grid.insert(datalist=[_q], cursor=c)

            c = grid.cursor

            #outstring += _outstring
            """
            if (i + 1) == len(formatlist):
                pass
            else:
                #outstring += '||'
                q.append(self.Separator())
            """

            #print(outstring)
        #print('q:', q)
        grid.carriagereturn()
        #return q

    def __outputconfig__(self):
        outputscheme_id = runtimenamespace()['outputscheme']
        #outputscheme = outputconfigname(outputscheme_id)
        outputconfig = confignamespace()[outputconfigname(outputscheme_id)]

        return outputconfig

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
            """
            outputscheme_id = runtimenamespace()['outputscheme']
            outputscheme = outputconfigname(outputscheme_id)
            outputconfig = confignamespace()[outputconfigname(outputscheme_id)]
            """
            outputconfig = self.__outputconfig__()

            separatorname = 'separator'

            if separatorname in outputconfig and separatoroverride is None:
                separator = outputconfig[separatorname]
                if separator.startswith('"') and separator.endswith('"'):
                    #separator = '%s' % separator [1:-1]
                    separator = bytes('%s' % separator [1:-1], "utf-8").decode("unicode_escape") # prevent escaping
                    #print('in output: *%s*' % separator)
            else:
                separator = separatoroverride

            #if flat:
            #    pass

            #_formatlist = self.formatter()
            _formatlist = obj.__classoutputscheme__()
            # TODO add a len() method to dynamic class type to help with matrix width sizing
            #_result = Matrix(startheight=10, startwidth=10)
            _ret = self.integrate(obj,
                                  formatlist=_formatlist,
                                  #outputscheme=outputscheme,
                                  separator=separator,
                                  grid=grid)#,
                                  #flat=flat)
            #for row in results:
            #    print(row)
            #return _ret

        if grid is None:
            grid = Matrix(startheight=20, startwidth=20)
        if isinstance(obj, list):
            _ret = [sub(self, _obj,
                        separatoroverride=separatoroverride,
                        #flat=flat,
                        grid=grid) for _obj in obj]
        else:
            _ret = sub(self, obj,
                       separatoroverride=separatoroverride,
                       #flat=flat,
                       grid=grid)

        #print(_ret)
        #for row in grid:
        #    print(row)

        #if not grid.isempty:
        #    grid.trim()
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