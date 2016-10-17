from gtool.core.types.core import FunctionType
import pyparsing as p
import patricia as pt
from gtool.core.filewalker import striptoclassname

class Enum(FunctionType):
    """
    returns a numeric value for a specific string value.
    Best to use with a choice type but works with string type attributes too.
    Can also consume method outputs as long as they are string values.

    EXAMPLE Config string: input = '@text1', mapping = 'low = 1, medium = 2, high = 3'

    The internal matching using a patricia tree and forces everything to lower case,
    so it's actually better to use minimal mapping such as:

    input = '@text1', mapping = 'l = 1, m = 2, h = 3'

    """

    def __init__(self, obj, config=str()):

        #print(config)

        #_config = """input = '@text1', mapping = 'low = 1, medium = 2, high = 3'"""


        super(Enum, self).__init__(obj, config=config)

        #print(config)
        #print(self.config)
        #print(config == _config)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Enum plugin function requires a config string')

        inputkeyword = 'input'
        mappingkeyword = 'mapping'

        if not inputkeyword in self.config:
            raise ValueError('A input keyword argument must be specified for the Enum plugin function')

        if not mappingkeyword in self.config:
            raise ValueError('A mapping keyword argument must be specified for the Enum plugin function')

        attrexpr = p.Combine(
            p.Literal("'").suppress() + (p.Literal('@') | p.Literal('!')).suppress() + p.Word(p.alphanums) +
            p.Literal("'").suppress()
            )

        inputexpr = p.CaselessKeyword(inputkeyword).suppress() + p.Literal('=').suppress() + attrexpr

        mappingexpr = p.CaselessKeyword(mappingkeyword).suppress() + p.Literal('=').suppress() + p.sglQuotedString()

        expr = inputexpr + p.Literal(',').suppress() + mappingexpr

        self.input = None
        self.mapping = None

        _matches = []

        for x in expr.scanString(self.config):

            _matches.append(x)

        if len(_matches) > 1:
            raise IndexError('There should only be one input and mapping keyword set in the Enum plugin function\'s config but %s was received' % _matches)

        #print(_matches)

        rawconfig = _matches[0]

        mappingdict = {}

        for mapitem in rawconfig[0][1][1:-1].split(','):
            k, v = mapitem.split('=')
            mappingdict[k.strip()] = v.strip()

        self.input = rawconfig[0][0]
        self.mapping = pt.trie()
        for k, v in mappingdict.items():
            self.mapping[k.lower()] = v
        #self.mapping = mappingdict


    def compute(self):

        def num(s):
            try:
                return int(s)
            except ValueError:
                return float(s)

        def getname(obj, name):

            _inputval = getattr(obj, name, None)

            if _inputval is None:
                return None

            if isinstance(_inputval, str):  # if we get a string - the attrib is actually a method plugin output
                #print('got a string')
                return _inputval

            if hasattr(_inputval, 'issingleton') and not _inputval.issingleton():
                raise ValueError('Enum plugin cannot process multi value attributes in %s' % name)
            elif hasattr(_inputval, 'issingleton') and  _inputval.issingleton():
                return '%s' % _inputval[0]
            elif not hasattr(_inputval, 'issingleton'):
                return '%s' % _inputval

        _inputval = getname(self.targetobject, self.input)

        if _inputval is not None:
            self.computable = True

        if not self.computable:
            return False
        """
        if striptoclassname(type(_inputval)) == 'attribute':
            _inputval = '%s' % _inputval[0]
        else:
            _inputval = '%s' % _inputval
        """

        try:
            self.__result__ = num(self.mapping[self.mapping.key(_inputval.lower())])
        except ValueError:
            self.__result__ = self.mapping[self.mapping.key(_inputval.lower())]
        except KeyError:
            self.__result__ = None


def load():
    return Enum
