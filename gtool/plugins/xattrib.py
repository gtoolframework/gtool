from gtool.core.types.core import FunctionType
import pyparsing as p
from gtool.core.noderegistry import getObjectByUri, nodenamespace


class Xattrib(FunctionType):
    """
    Retrieves an attribute from the object as specified in the config string.
    Will return None if the config string is missing or invalid.

    Example strings are:
    '/objectname@attrib1'
    '/container/objectname@attrib1'

    You can also read in the string from another attribute, examples are:
    '@attrib1'

    """

    def __init__(self, obj, config=str()):

        def process(config):
            pathexpr = p.Literal("'").suppress() + \
                       p.Optional(
                        p.Combine(
                            p.OneOrMore(p.Literal("/") + p.Word(p.alphanums)) + p.Literal("/").suppress())
                       ).setResultsName('path') + \
                       p.Combine(
                           (p.Literal('@').suppress() | p.Literal('!').suppress()) +
                           p.Word(p.alphanums) +
                           p.Literal("'").suppress()
                       ).setResultsName('attrib')

            expr = p.Group(pathexpr).setResultsName('search')

            match2 = expr.parseString(config)

            _ret = []

            if 'search' in match2:
                if 'path' in match2['search']:
                    _ret.append(match2['search']['path'])
                if 'attrib' in match2['search']:
                   _ret.append(match2['search']['attrib'])

            return _ret

        super(Xattrib, self).__init__(obj, config=config, defer=True)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Xattrib plugin function requires a config string')

        try:
            _result = process("'%s'" % self.config)
            if len(_result) == 2:
                self.targetobject, self.targetattribute = _result
            elif len(_result) == 1:
                _config = getattr(obj, _result[0], None)
                if _config is None:
                    raise ValueError('Xattrib plugin received an attribute name that does not exist')
                # TODO len check only required for attributes, but not method plugins
                if len(_config) > 1:
                    raise ValueError('Xattrib plugin received a attribute name that contains multiple values')
                self.targetobject, self.targetattribute = process("'%s'" % _config[0])
            else:
                raise Exception()
        except:
            raise ValueError('An error occured when processing the search string for the Xattrib plugin function')

    def compute(self):

        _obj = getObjectByUri(self.targetobject)

        if _obj is not None:
            self.computable = True

        if not self.computable:
            return False

        try:
            self.__result__ = getattr(_obj, self.targetattribute)
        except KeyError:
            self.__result__ = None


def load():
    return Xattrib
