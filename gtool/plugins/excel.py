from gtool.core.types.output import GridOutput
import xlsxwriter

class Excel(GridOutput):

    def __output__(self, projectstructure):
        # TODO call Super and use results
        structure = projectstructure.dataasobject
        #return self.__gridoutput__(structure)
        _grid = self.__gridoutput__(structure)
        _grid.trim()
        workbook = xlsxwriter.Workbook('temp.xlsx')
        worksheet = workbook.add_worksheet()
        for i, row in enumerate(_grid):
            worksheet.write_row(i, 0, row)
        workbook.close()
        return True


def load():
    return Excel