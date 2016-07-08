import pyparsing as p

teststring = "@attrib2:: test2\n" \
             "*output1 = @blah1 @blah2\n" \
             "*output2 = @attr1 @att2 || @attr3\n" \
             "@attrib1:: test\n"

teststring2 = "@attrib1:: test\n"

parser1 = p.Combine(p.LineStart() + p.Literal('*').suppress() + p.Word(p.printables)) + p.Literal('=').suppress() + p.restOfLine() + p.LineEnd().suppress()
parser2 = p.Combine(p.LineStart() + p.Literal('@').suppress() + p.Word(p.alphanums + '_-') + p.Suppress(p.Literal('::'))) + p.restOfLine() + p.LineEnd().suppress()

#x = parser1.parseString(teststring)
y = parser1.searchString(teststring)
a = parser2.searchString(teststring)
#b = parser2.parseString(teststring)
#q = parser2.searchString(teststring2)

#print(x)
print(y)
print(a)
#print(q)