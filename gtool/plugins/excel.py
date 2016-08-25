from gtool.core.types.output import GridOutput
import xlsxwriter

class Excel(GridOutput):

    def __output__(self, projectstructure, output=None):
        if output is None:
            raise ValueError('An outputfile argument was expected')
        # TODO call Super and use results
        """
        structure = projectstructure.dataasobject
        _grid = self.__gridoutput__(structure)
        _grid.trim()
        """
        _grid = super(Excel, self).__output__(projectstructure)
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        for i, row in enumerate(_grid):
            worksheet.write_row(i, 0, row)
        workbook.close()
        return True


def load():
    return Excel