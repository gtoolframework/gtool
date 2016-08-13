from gtool.core.utils.output import checkalignment  #utils.output as uo
import sys

class Output(object):

    """
    Output object, override __aligned__ on init
    """

    def __init__(self, aligned=None):
        if aligned is None:
            raise NotImplemented('Output classes must explicitly see aligned as True or False')
        self.__aligned__ = aligned

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
            except Exception as err:
                print(err)
                sys.exit()

    def __output__(self, projectstructure):
        raise NotImplementedError('Output classes must implement __output__')

    def output(self, projectstructure):
        """
        Final output generator, should not be overriden without a call to __output__()
        :param projectstructure: a structurefactory object
        :return:
        """
        self.__output__(projectstructure)
