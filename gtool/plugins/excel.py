from gtool.core.types.output import Output

class Exceloutput(Output):

    def __init__(self):
        super(Exceloutput, self).__init__(aligned=True)

    def __output__(self):
        pass

    def __test__(self):
        pass

def load():
    return Exceloutput