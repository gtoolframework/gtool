from gtool.core.types.core import FunctionType
import pyparsing as p


class Combine(FunctionType):
    """
    Combines attributes of the object as specified in the config string.
    Will return None if any of the attributes in the config string are missing.
    Does not work with attributes that are dynamic objects.

    Example strings are:
    '@num1 @num2'
    '@num1 ++blah blah++ @num2'

    """

    def __init__(self, obj, config=str()):
        
        self.__attribs__ = {}
        super(Combine, self).__init__(obj, config=config)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Combine plugin function requires an formatting string')

    def substitute(self, s, l, t):
        if t[0] in self.__attribs__.keys():
            return self.__attribs__[t[0]]

    def compute(self):

        def getname(obj, name):

            _val = None

            if hasattr(obj, name):
                _val = getattr(obj, name, None)

            if _val is None:
                return _val

            try:
                if _val.isdynamic: #TODO make this work for non-attributes, non-dynamics (use .issingleton? - what about a concat mode?)
                    raise ValueError('Combine plugin cannot process %s because it contains a dynamic class' % name)
            except AttributeError:
                raise TypeError('Expected an attribute but got a %s' % type(_val))

            if _val.issingleton():
                _ret = '%s' % _val[0].raw()
            else:
                _ret = ', '.join(['%s' % v.raw() for v in _val])

            return _ret

        attrmarker = (p.Literal('@') | p.Literal('!'))
        attrmatch = attrmarker.suppress() + p.Word(p.alphanums)

        for i in attrmatch.scanString(self.config):
            x = i[0][0]
            self.__attribs__[x] = getname(self.targetobject, x)

        if all(v is not None for v in self.__attribs__.values()):
            self.computable = True

        if self.computable:

            attrmatch = p.Literal('@').suppress() + p.Word(p.alphanums)
            attrmatch.setParseAction(self.substitute)
            attrlist = p.ZeroOrMore(p.Optional(p.White()) + attrmatch + p.Optional(p.White()))

            self.__result__ = attrlist.transformString(self.config)


def load():
    return Combine
