import pyparsing as p

s = '@num1 || @num2'

d = {
    'num1': 'boulder iron',
    'num2': 'feather'
}

def substituteMacro(s,l,t):
    if t[0] in d:
        print(s)
        print(l)
        print(t)
        return d[t[0]]

attrmatch = p.Literal('@').suppress() + p.Word(p.alphanums)
attrmatch.setParseAction( substituteMacro )
attrlist = p.ZeroOrMore(p.Optional(p.White()) + attrmatch + p.Optional(p.White()))

print(attrlist.transformString(s))