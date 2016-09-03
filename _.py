import pyparsing as p

testexpr = p.nestedExpr()

s="""!test2:: Math('1 * 2')"""

_match=[]

for x in testexpr.scanString(s):
    _start = x[1] + 1
    _end = x[2] - 1
    _match.append(s[_start:_end])

print(_match[0])

if _match[0].startswith("'"):
    _match[0] = _match[0][1:]

if _match[0].endswith("'"):
    _match[0] = _match[0][:-1]

print(_match[0])
