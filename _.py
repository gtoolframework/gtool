import pyparsing as p
#from gtool.core.noderegistry import getObjectByUri, searchByAttribAndObjectType, searchByAttrib
from abc import abstractmethod

getObjectByUri = print
searchByAttribAndObjectType = print
searchByAttrib = print

x = """TOTAL::
*name = Sum of Sam
*function = sum
*select = @attr1//objtype

TOTALS::
*name = Sum of Sam
*function = sum
*select = @attr1

TOTALZ::
*name = Sum of Sam
*function = sum
*select = /obj/blah/@attr1
"""

class Selector():

    @property
    def method(self):
        _method = getattr(self, '__method__', None)
        if _method is None:
            raise NotImplemented('self.__method__ must be implemented by descendants of Selector class')
        return _method

class AttrSelector(Selector):

    def __init__(self):
        self.__method__ = searchByAttrib

class AttrByObjectSelector():

    def __init__(self):
        self.__method__ = searchByAttribAndObjectType

class FullPathSelector():

    def __init__(self):
        self.__method__ = getObjectByUri


def attrexpr():
    return p.Combine(p.Literal('@').suppress() + p.Word(p.alphanums))

def parseSelector(selectorstring):
    # *select = @attr1 | /tf1/@attr | @attr1//objtype

    """
    def enumtype(*args,**kwargs): #s, l, t, selectortype=None):
        print(args)
        selectortype = kwargs['selectortype']
        if selectortype is None or not isinstance(selectortype, str):
            raise ValueError('enumtype requires a selectortype string but got a', type(selectortype))
        return selectortype
    """

    def attrtype():
        return AttrSelector() # 'ATTRTYPE'

    def fullpathtype():
        return FullPathSelector() #'FULLPATH'

    def attrbyobjtype():
        return AttrByObjectSelector() #'ATTRBYOBJECT'



    def expr(selectorstring=None, returntype=False):
        attrmatch = p.Combine(p.Literal('@').suppress() + p.Word(p.alphanums))
        fullpathmatch = p.Combine(p.OneOrMore(p.Literal('/') + p.Word(p.alphanums))) + p.Literal(
            '/').suppress() + p.Combine(p.Literal('@').suppress() + p.Word(p.alphanums))
        attrbyobjmatch = p.Combine(p.Literal('@').suppress() + p.Word(p.alphanums)) + p.Literal('//').suppress() + p.Word(p.alphanums)

        matchgroup = (fullpathmatch | attrbyobjmatch | attrmatch)

        if returntype:
            attrmatch.setParseAction(attrtype)
            fullpathmatch.setParseAction(fullpathtype)
            attrbyobjmatch.setParseAction(attrbyobjtype)

        return matchgroup.parseString(selectorstring)

    _selectorconfig = expr(selectorstring=selectorstring)
    _selectortype = expr(selectorstring=selectorstring, returntype=True)

    return {
            'type': _selectortype[0],
            'config': _selectorconfig[:2] #TODO unclear why [0] returns only a subset of the matches
    }

def aggregatorIdParser():
    # --- class parser ---
    colon = p.Literal('::').suppress()
    aggregatorName = p.Word(p.alphas.upper())
    aggregatorDef = aggregatorName + colon + p.LineEnd().suppress()
    return aggregatorDef

aggregatorIdParser().setResultsName('id')

def aggregatorMetas():
    star = p.Literal('*').suppress()
    metaName = p.Word(p.alphanums)
    metaKeyword = p.Combine(star + metaName).setResultsName('key')
    equals = p.Literal('=').suppress()
    value = p.Word(p.printables + ' ')
    metaValue = (equals + value).setResultsName('value')
    metaDef = p.Dict(p.Group(metaKeyword + metaValue) + p.Optional(p.LineEnd().suppress()))
    return metaDef

aggregatorMetas()

expr = p.OneOrMore(p.Group(aggregatorIdParser() + p.OneOrMore(aggregatorMetas())))

a_expr = attrexpr()

a_match = a_expr.searchString(x)
print(a_match)

match = expr.parseString(x)

_retlist = []

for m in match:
    _retdict = {}
    _retdict['id'] = m[0]
    for k, v in m.items():
        _retdict[k] = v
    _retlist.append(_retdict)

print(_retlist)

for aggregatordict in _retlist:
    print(parseSelector(aggregatordict.get('select')))

