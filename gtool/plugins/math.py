from gtool.core.types.core import FunctionType
import simpleeval as s
import pyparsing as p
import math as m
#from gtool.core.filewalker import striptoclassname
import sys

class Math(FunctionType):
    """
    Performs math on numeric attributes of the object as specified in the config string.
    Can only work attributes that are singleton numbers or method attributes that return numbers.
    Will return None if any of the attributes in the config string are missing.
    """

    def __init__(self, obj, config=str()):
        
        self.names = {}
        super(Math, self).__init__(obj, config=config)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Math plugin function requires an expression string')

    def compute(self):

        def getname(obj, name):

            _val = None

            #TODO move this method's error checking into base class (add a more for attribute only vs method and attribute)
            #TODO need more context to say which method has an invalid input config
            try:
                _val = getattr(obj, name)
            except AttributeError as a_err:
                raise AttributeError(a_err)
            except SyntaxError as s_err:
                print("Error in Math Plugin config:", SyntaxError(s_err))
                sys.exit(1)

            """
                if name in obj.__methods__.keys() and name not in obj.__method_results__.keys():
                    raise AttributeError('%s method in %s dynamic object has not initialized yet' % (name, striptoclassname(type(obj))))
                else:
                    raise AttributeError(err)
            """

            if isinstance(_val, int) or isinstance(_val, float): #if we get an a numeric value - the attrib is actual a method plugin output
                #print('got a number')
                return _val

            try:
                if not _val.issingleton():
                    raise ValueError('Math plugin cannot process multi value attributes in %s' % name)
            except AttributeError:
                raise TypeError('Expected an attribute but got a %s' % type(_val))

            num = _val[0].raw()
            """
            if m.isnan(num):
                raise TypeError('Math plugin can only perform path on numeric '
                                'values but got a %s with a value of %s in %s' % (type(num), num, name))
            """

            return num

        attrmarker = (p.Literal('@') | p.Literal('!'))
        attrmatch = attrmarker.suppress() + p.Word(p.alphanums)

        for i in attrmatch.scanString(self.config):
            x = i[0][0]
            self.names[x] = getname(self.targetobject, x)
            if m.isnan(self.names[x]):
                raise TypeError('Math plugin can only perform path on numeric '
                                'values but got a %s with a value of %s in %s'
                                % (type(self.names[x]), self.names[x], x))

        if all(v is not None for v in self.names.values()):
            self.computable = True


        if self.computable:
            _expr = self.config
            if '@' in _expr:
                _expr = _expr.replace('@', '')
            if '!' in _expr:
                _expr = _expr.replace('!', '')
            self.__result__ = s.simple_eval(_expr, names=self.names)


def load():
    return Math
