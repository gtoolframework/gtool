import pyparsing as p

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
*select = /obj/@attr1
"""

def parseSelector(selectorstring):
    #*select = @attr1 | /tf1/@attr | @attr1//objtype
    attrmatch = p.Combine(p.Literal('@') + p.Word(p.alphanums))
    fullpathmatch = p.Combine(p.OneOrMore(p.Literal('/') + p.Word(p.alphanums))) + p.Literal('/').suppress() + p.Combine(p.Literal('@').suppress() + p.Word(p.alphanums))
    attrbyobjmatch = p.Combine(p.Literal('@') + p.Word(p.alphanums)) + p.Literal('//').suppress() + p.Word(p.alphanums)

    return (fullpathmatch | attrbyobjmatch | attrmatch).parseString(selectorstring)

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

