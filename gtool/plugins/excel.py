from gtool.core.types.output import GridOutput


class Excel(GridOutput):

    def __output__(self, projectstructure):
        #for child in projectstructure.children:
        #    print(child.dataasobject)
        print(projectstructure.dataasobject)

    def __test__(self):
        pass

def load():
    return Excel