from gtool.core.types.output import GridOutput


class Grid(GridOutput):
    """
    Simple Grid output. Given a project structure it will return a matrix.
    Good for testing or as an intermediate processor.
    """

    def __output__(self, projectstructure):
        # TODO call Super and use results
        structure = projectstructure.dataasobject
        return self.__gridoutput__(structure)


def load():
    return Grid