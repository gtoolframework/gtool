from gtool.core.types.output import GridOutput
from gtool.core.types.matrix import Matrix
import xlsxwriter
from gtool.core.filewalker import StructureFactory


class Excel(GridOutput):

    def __output__(self, projectstructure, output=None):
        if output is None:
            raise ValueError('An output argument was expected')

        _outputdict = {}
        if isinstance(projectstructure, StructureFactory.Container):
            pass

        try:
            if not isinstance(projectstructure, StructureFactory.Container):
                raise Exception
            if all(isinstance(c, StructureFactory.Container) for c in projectstructure.children):
                for child in projectstructure.children:
                    _outputdict[child.name] = super(Excel, self).__output__(child)
            else:
                raise Exception
        except Exception:
            worksheetname = '_' if projectstructure.name == '*' else projectstructure.name
            _outputdict[worksheetname] = super(Excel, self).__output__(projectstructure)

        try:
            self.__writexls__(filename=output,outputdict=_outputdict)
        except Exception as err:
            raise Exception(err)

        return True

    def __writexls__(self, filename="output.xlsx", outputdict={}):

        if outputdict is None:
            raise ValueError('An output argument was expected')

        if not isinstance(outputdict, dict):
            raise TypeError('Was expecting a dictionary for outputdict but got a %s' % type(dict))

        extension = '.xlsx'
        if not filename.endswith(extension):
            filename += extension

        #TODO check location and filename are valid

        workbook = xlsxwriter.Workbook(filename)

        for sheet, grid in sorted(outputdict.items()):
            worksheet = workbook.add_worksheet(name=sheet[:32]) #worksheet name cannot be more than 32 chars long
            if not isinstance(grid, Matrix):
                raise TypeError('Expected a Matrix but got a %s' % type(grid))
            for i, row in enumerate(grid):
                worksheet.write_row(i, 0, row)

        workbook.close()

        return True


def load():
    return Excel