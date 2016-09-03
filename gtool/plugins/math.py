from gtool.core.types.core import FunctionType
import simpleeval as s
import pyparsing as p
import math as m


class Math(FunctionType):
    """
    Performs math on numeric attributes of the object as specified in the config string.
    Can only work attributes that are singleton ints. Will return None if any of the attributes
    in the config string are missing.
    """

    def __init__(self, obj, config=str()):
        
        self.names = {}
        super(Math, self).__init__(obj, config=config)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Math plugin function requires an expression string')

    def compute(self):

        def getname(obj, name):

            _val = None

            if hasattr(obj, name):
                _val = getattr(obj, name, None)

            if _val is None:
                return _val

            try:
                if not _val.issingleton():
                    raise ValueError('Math plugin cannot process multi value attributes in %s' % name)
            except AttributeError:
                raise TypeError('Expected an attribute but got a %s' % type(_val))

            num = _val[0].raw()
            if m.isnan(num):
                raise TypeError('Math plugin can only perform path on numeric '
                                'values but got a %s with a value of %s in %s' % (type(num), num, name))

            return num

        attrmatch = p.Literal('@').suppress() + p.Word(p.alphanums)

        for i in attrmatch.scanString(self.config):
            x = i[0][0]
            self.names[x] = getname(self.targetobject, x)

        if all(v is not None for v in self.names.values()):
            self.computable = True


        if self.computable:
            _expr = self.config.replace('@', '')
            self.__result__ = s.simple_eval(_expr, names=self.names)


def load():
    return Math
