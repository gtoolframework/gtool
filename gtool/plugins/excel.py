from gtool.core.types.output import GridOutput


class Excel(GridOutput):

    def __output__(self, projectstructure):
        # TODO call Super and use results
        structure = projectstructure.dataasobject
        return self.__gridoutput__(structure)

def load():
    return Excel