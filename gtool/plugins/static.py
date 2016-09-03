from gtool.core.types.core import FunctionType


class Static(FunctionType):
    """
    returns the static value in the config string
    """

    def __init__(self, obj, config=str()):

        super(Static, self).__init__(obj, config=config)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Static plugin function requires an static string')


    def compute(self):
        self.__result__ = '%s' % self.config


def load():
    return Static
