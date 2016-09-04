import pyparsing as p

inputkeyword = 'input'

mappingkeyword = 'mapping'

attrexpr = p.Combine(p.Literal("'").suppress() + (p.Literal('@') | p.Literal('!')).suppress() + p.Word(p.alphanums) + p.Literal("'").suppress())

inputexpr = p.CaselessKeyword(inputkeyword).suppress() + p.Literal('=').suppress() + attrexpr


mappingexpr = p.CaselessKeyword(mappingkeyword).suppress() + p.Literal('=').suppress() + p.sglQuotedString()

expr = inputexpr + p.Literal(',').suppress() + mappingexpr


s="""input = '@text1', mapping = 'low = 1, medium = 2, high = 3'"""

for x in expr.scanString(s):

    mappingdict = {}

    for mapitem in x[0][1][1:-1].split(','):
        k, v = mapitem.split('=')
        mappingdict[k.strip()] = v.strip()

    print((x[0][0], mappingdict))