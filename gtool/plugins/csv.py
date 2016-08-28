from gtool.core.types.output import GridOutput
from gtool.core.types.matrix import Matrix
import csv
from gtool.core.filewalker import StructureFactory


class Csv(GridOutput):

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
                    _outputdict[child.name] = super(Csv, self).__output__(child)
            else:
                raise Exception
        except Exception:
            csvname = '_' if projectstructure.name == '*' else projectstructure.name
            _outputdict[csvname] = super(Csv, self).__output__(projectstructure)

        try:
            self.__writecsv__(filename=output,outputdict=_outputdict)
        except Exception as err:
            raise Exception(err)

        return True

    def __writecsv__(self, filename="output.csv", outputdict={}):

        if outputdict is None:
            raise ValueError('An output argument was expected')

        if not isinstance(outputdict, dict):
            raise TypeError('Was expecting a dictionary for outputdict but got a %s' % type(dict))

        extension = '.csv'
        underscore = '_'
        if filename.endswith(extension):
            filenameprefix = filename[:-len(extension)] #filename += extension
        else:
            filenameprefix = filename

        #TODO check location and filename are valid

        _sheets = len(outputdict.items())

        for csvname, grid in sorted(outputdict.items()):

            if _sheets > 1:
                _filename = filenameprefix + underscore + csvname + extension
            else:
                _filename = filenameprefix + extension

            print('writing to', _filename)

            if not isinstance(grid, Matrix):
                raise TypeError('Expected a Matrix but got a %s' % type(grid))

            with open(_filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                #TODO fix quoting - unclear why it quotes when it does
                for row in grid:
                    csvwriter.writerow(row)
                csvfile.close()

        return True


def load():
    return Csv