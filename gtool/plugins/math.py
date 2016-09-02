from gtool.core.types.core import FunctionType
import simpleeval as s
import pyparsing as p
import math as m


class Math(FunctionType):

    def __init__(self, obj, config=str(), context=None):

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
        
        self.targetobject = obj
        self.expression = config
        self.computable = False
        self.__result__ = None
        self.names = {}

        if self.expression is None or len(self.expression) < 1 or not isinstance(self.expression, str):
            raise ValueError('Math plugin function requires an expression string')

        attrmatch = p.Literal('@').suppress() + p.Word(p.alphanums)

        for i in attrmatch.scanString(self.expression):
            x = i[0][0]
            self.names[x] = getname(self.targetobject, x)

        if all(v is not None for v in self.names.values()):
            self.computable = True

    def compute(self):
        if self.computable:
            _expr = self.expression.replace('@', '')
            self.__result__ = s.simple_eval(_expr, names=self.names)

    @property
    def result(self):
        self.compute()
        return self.__result__

    def __repr__(self):
        return self.expression

    def __str__(self):
        self.compute()
        return self.__result__


def load():
    return Math
