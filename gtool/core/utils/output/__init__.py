from gtool.core.types.matrix import Matrix
import gtool.core.types.outputmanagers as om
import pyparsing as p

def flatten(matrix, sep=', '):
    """
    Takes a matrix and flattens it into a list. Matrix must have contiguous vertical use.
    :param matrix: Matrix
    :return: list
    """

    def __iscontiguous__(matrix):

        if not isinstance(matrix, Matrix):
            raise TypeError('__iscontiguous__ function expects a matrix but got a', type(matrix))
        mmap = matrix.__matrixmap__()

        for i in range(1, len(mmap)):
            toprow = mmap[i-1]
            bottomrow = mmap[i]
            for k in enumerate(toprow):
                if toprow[k] == 0 and bottomrow[k] == 1:
                    return False

        return True

    if not isinstance(matrix,Matrix):
        raise TypeError('flatten function expects a matrix but got a', type(matrix))
    matrix.trim()
    if not __iscontiguous__(matrix):
        raise ValueError('matrix is not contiguous')

    _retlist = []

    for x in range(matrix.width):
        _retlist.append(sep.join(matrix.col(x)))

    return _retlist


def parseformat(classname=None, formatstring=None):
    attribmarker = p.Literal('@').suppress()
    cellseparator = '||'
    concatmarker = p.Optional(p.Literal('+'))

    attribgroup = attribmarker + concatmarker + p.Word(p.alphanums)

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

            _templist.append(om.Filler(cell[prestart:start]))
            _templist.append(om.AttributeMatch(cell[start + 1:end], classname=classname))
            prestart = end
            # print('templist:', _templist)
        _templist.append(om.Filler(cell[end:]))
        cells.append(_templist)

    return cells

# --- static ---

def formatters():
    __FORMATTERS = '__FORMATTERS__'  # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins
    return __FORMATTERS

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerFormatter(formatterName, formatter):
    #print(globals())
    if formatterName in globals()[formatters()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One formatter tried to overwrite an existing one. Formatter name: %s' % formatterName)
    else:
        globals()[formatters()][formatterName] = formatter
        return True

def formatternamespace():
    return globals()[formatters()]

#--- initialize namespace

globals()[formatters()] = dict()
