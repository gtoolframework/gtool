import pyparsing as p

config = '@blah[3:7]'

attrexpr = (p.Literal('@') | p.Literal('!')).suppress() + p.Word(p.alphanums)
slicestartexpr = p.Literal('[').suppress() + p.Optional(p.Word(p.nums))
sliceendexpr =  p.Optional(p.Word(p.nums)) + p.Literal(']').suppress()

attrmatch = attrexpr.setResultsName('attribute') + \
            slicestartexpr.setResultsName('start') + \
            p.Suppress(p.Literal(':')) + \
            sliceendexpr.setResultsName('end')

s = attrmatch.parseString(config)

print(s.get('attribute', None))
print(s.start)
print(s.end)