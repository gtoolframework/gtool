import pyparsing as p

def process(configstring):

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

    expr = p.OneOrMore(p.Group(aggregatorIdParser() + p.OneOrMore(aggregatorMetas())))

    match = expr.parseString(configstring)

    _retlist = []

    for m in match:
        _retdict = {}
        _retdict['id'] = m[0]
        for k, v in m.items():
            _retdict[k] = v
        _retlist.append(_retdict)

    return _retlist

def parseSelector(selectorstring):
    pass

def load(configstring):
    _retlist =process(configstring)
    for aggregatordict in _retlist:
        if 'select' in aggregatordict:
            selector = aggregatordict['select']
            aggregatordict['select'] = parseSelector(selector)
    return _retlist
