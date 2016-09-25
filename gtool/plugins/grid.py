from gtool.core.types.output import GridOutput


class Grid(GridOutput):
    """
    Simple Grid output. Given a project structure it will return a matrix.
    Good for testing or as an intermediate processor.
    """

    def __output__(self, projectstructure, output=None):
        """
        Returns a grid
        :param projectstructure: StructureFactory object
        :param outputfile: Must be None
        :return: Matrix type
        """
        if output is not None:
            raise ValueError('Grid does not output a file to disk but an output location was provided.')

        return super(Grid, self).__output__(projectstructure)


def load():
    return Grid