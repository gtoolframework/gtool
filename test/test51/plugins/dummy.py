class Dummy():

    #inherit from any class
    #check from gtool.core.types.core for different base classes

    def __init__(self):
        pass

    def __test__(self):
        pass

def load():
    #load() must return the name of the plugin class without initializing it
    return Dummy