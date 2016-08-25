from gtool.core.types.output import GridOutput
import xlsxwriter
from gtool.core.filewalker import StructureFactory

class Excel(GridOutput):

    def __output__(self, projectstructure, output=None):
        if output is None:
            raise ValueError('An output argument was expected')
        
        if isinstance(projectstructure, StructureFactory.Container):
            if all(isinstance(c, StructureFactory.Container) for c in projectstructure.children):
                print("turtles")

        _grid = super(Excel, self).__output__(projectstructure)
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        for i, row in enumerate(_grid):
            worksheet.write_row(i, 0, row)
        workbook.close()
        return True


def load():
    return Excel