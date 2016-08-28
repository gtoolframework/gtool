from gtool.core.types.core import FunctionType

class Testfunc(FunctionType):
    print('TestFunc')

def load():
    return Testfunc