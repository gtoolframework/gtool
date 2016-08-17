from abc import ABC, abstractmethod
from gtool.core.utils.output import checkalignment
import sys
from gtool.core.filewalker import StructureFactory
from gtool.core.utils.output import formatternamespace

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

        self.__output__(projectstructure)

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

    @classmethod
    def formatter(cls):
        _classname = '{}'.format(cls)[6:-2].split('.')[
            -1]  # TODO this is hacky - removes '<class and >' - use striptoclassname
        # print('formatter: dynamic props', cls.__dynamic_properties__)
        # print('formatter: list slots:', cls.__list_slots__)
        # for k, v in cls.__list_slots__.items():
        #    print(k, ':', v.isdynamic) # isinstance(v.__lazyloadclass__()(), DynamicType))

        return formatternamespace()[_classname]

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

    def __xoutput__(self, outputscheme=None, separatoroverride=None, listmode=False):
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