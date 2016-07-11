#import pyparsing as p
#from gtool.utils.config import namespace as confignamespace

"""
#TODO collapse Filler and Attribute<atch then subclass
class Filler(object):

    def __init__(self, fillertext):
        self.__fillertext__ = fillertext

    def process(self):
        return '%s' % self.__fillertext__

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__fillertext__)

class AttributeMatch(object):

    def __init__(self, attrname):
        self.__attrname__ = attrname

    def process(self, obj=None, sep=" "):
        if hasattr(obj, self.__attrname__):
            return sep.join(['%s' % f for f in getattr(obj, self.__attrname__)])
        else:
            raise AttributeError('%s does not have a %s attribute as specified in the output format scheme:' % (obj.__class__, self.__attrname__))

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__attrname__)
"""

"""
def parseformat(formatstring):
    attribmarker = p.Literal('@').suppress()
    cellseparator = '||'

    attribgroup = attribmarker + p.Word(p.alphanums)

    cells = []

    _splitstring = [cell.strip() for cell in formatstring.split(cellseparator)]

    for cell in _splitstring:
        _scan = attribgroup.scanString(cell)
        _templist = []
        prestart = 0
        end = 0
        for match in _scan:
            start = match[1]
            end = match[2]

            _templist.append(Filler(cell[prestart:start]))
            _templist.append(AttributeMatch(cell[start + 1:end]))
            prestart = end
            # print('templist:', _templist)
        _templist.append(Filler(cell[end:]))
        cells.append(_templist)

    return cells

def integrate(self, formatlist=None, separator=" "):

    outstring = ""

    _obj = self

    for i, cell in enumerate(formatlist):
        for element in cell:
            if isinstance(element, Filler):
                outstring += element.process()

            if isinstance(element, AttributeMatch):
                outstring += element.process(obj=_obj, sep=separator)

        if (i + 1) == len(formatlist):
            pass
        else:
            outstring += '||'
    return outstring
"""

"""
def output(self, outputscheme=None):
    if not 'output' in confignamespace():
        raise AttributeError('An output section is not configured in the config file')
    if outputscheme == None:
        raise ValueError('No outputscheme provided for %s class' % self.__class__)
    if not outputscheme in confignamespace()['output']:
        raise NameError('%s is not configured in the [output] section in the config file' % outputscheme)
    _metas = self.metas() # assume metas() exist by virtue of class construction
    if not outputscheme in _metas:
        raise NameError('%s class does not have an output scheme called %s' % (self.__class__, outputscheme))
    # validation checks passed
    separatorname = outputscheme + '_separator'
    separator = " "
    if separatorname in confignamespace()['output']:
        separator = confignamespace()['output'][separatorname]
        if separator.startswith('"') and separator.endswith('"'):
            separator = separator [1:-1]

    print(confignamespace()['output'][outputscheme])
    return integrate(self, formatlist=parseformat(_metas[outputscheme]), separator=separator)
"""