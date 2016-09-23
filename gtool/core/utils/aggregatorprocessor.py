import pyparsing as p
from gtool.core.types.core import AttrSelector, FullPathSelector, AttrByObjectSelector

"""
DESIGN NOTE: Aggregates are not data and therefore live outside the data structure
"""

def process(configstring):

    """

    :param configstring: string containing contents of aggregator config file
    :return: config dict

    AGGREGATORNAME::
    *name = friendly name
    *function = function that will be used
    *select = @attr1 | /tf1/@attr | @attr1//objtype <-- selector

    TOTAL1::
    *name = Sum of Sam
    *function = sum
    *select = @attr1//objtype


    AVERAGE1::
    *name = Average Andy
    *function = average
    *select = @attr1//objtype

    LIST1::
    *name = Lenny List
    *function = List
    *select = /tf1/@attr

    """



    def aggregatorIdParser():
        # --- class parser ---
        colon = p.Literal('::').suppress()
        aggregatorName = p.Word(p.alphas.upper() + p.nums)
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

    def attrexpr(selectorstring=None):
        attrmatch = p.Combine(p.Literal('@').suppress() + p.Word(p.alphanums))
        return attrmatch.searchString(selectorstring)[0][0]

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
    _selectorattr = attrexpr(selectorstring=selectorstring)

    return {
            'type': _selectortype[0],
            'config': _selectorconfig[:2], #TODO unclear why [0] returns only a subset of the matches
            'attribute': _selectorattr
    }

def loadaggregators(configstring):
    SELECT = 'select'
    _retlist =process(configstring)
    for aggregatordict in _retlist:
        if SELECT in aggregatordict:
            selector = aggregatordict[SELECT]
            aggregatordict[SELECT] = parseSelector(selector)
    return _retlist
