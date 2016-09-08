from gtool.core.types.core import FunctionType


class Parent(FunctionType):
    """
    Will return the parent of the object the method is a part of
    """

    def __init__(self, obj, config=None):

        if config is not None:
            raise ValueError('Parent method plugin does not accept a configuration')

        super(Parent, self).__init__(obj, config=None)

        self.computable = True

    def compute(self):
        if self.computable:
            _result = '%s' % self.context['parent']
            self.__result__ = _result

def load():
    return Parent
