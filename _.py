import pyparsing as p

class Filler(object):

    def __init__(self, fillertext):
        self.__fillertext__ = fillertext

    def process(self):
        return self.__fillertext__

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__fillertext__)

class AttributeMatch(object):

    def __init__(self, attrname):
        self.__attrname__ = attrname

    def process(self):
        return globals()[self.__attrname__]

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__attrname__)


attribmarker = p.Literal('@').suppress()
cellseparator = '||'

teststring = "(@attrib1) || (@attrib2) C-@attrib3 (@attrib4)"
print(teststring)

attrib1 = 'test 1'
attrib2 = 'A.2'
attrib3 = '3'
attrib4 = 'book'

attribgroup = attribmarker + p.Word(p.alphanums)

test = attribgroup.scanString(teststring)

cells = []

_splitstring = [cell.strip() for cell in teststring.split(cellseparator)]

for cell in _splitstring:
    #_cell = cell.strip()
    _scan = attribgroup.scanString(cell)
    _templist = []
    prestart = 0
    for match in _scan:
        start = match[1]
        end = match[2]

        _templist.append(Filler(cell[prestart:start]))
        _templist.append(AttributeMatch(cell[start+1:end]))
        prestart = end
        #print('templist:', _templist)
    _templist.append(Filler(cell[end:]))
    cells.append(_templist)



#print('cells:', cells)
#print('**************')

outstring = ""

for i, cell in enumerate(cells):
    #print('cell:', cell)
    for element in cell:
        #print('element:', element)

        if isinstance(element, Filler) or isinstance(element,AttributeMatch):
            outstring += element.process()

    if (i+1) == len(cells):
        pass
    else:
        outstring += '||'

print(outstring)


