from gtool.core.types.matrix import Matrix
import gtool.core.types.outputmanagers as om
import pyparsing as p


def structureflatten(exp):
    def sub(exp, res):
        if type(exp) == dict:
            for k, v in exp.items():
                yield from sub(v, res + [k])
        elif type(exp) == list:
            for v in exp:
                yield from sub(v, res)
        else:
            yield "/".join(res + [exp])

    yield from sub(exp, [])

def checkalignment(project):
    s = set()

    for i in sorted(structureflatten(project.treestructure())):
        # print(i)
        s.add(i)

    #print(s)

    _maxlen = 0
    _longest = None
    for i in s:
        #print('length:', len(i))
        if len(i) > _maxlen:
            _longest = i
            _maxlen = len(_longest)

    #print(_longest)

    for i in s:
        if i not in _longest:
            _exception = 'Found an object structure {0} that does not align with the longest object structure {1}'.format(i, _longest)
            raise Exception(_exception)
        else:
            #print(i, 'is in', _longest)
            pass

    return True

def matrixflatten(matrix, sep=', '):
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

def descend(rootclass=None, recursionlist=[], recursionmembers=[], recusionlimit=0):
    if rootclass is None:
        raise ValueError('rootclass argument required but not provided')
    #detect recursion
    if rootclass in recursionlist and rootclass not in recursionmembers:
        raise RecursionError('The format string has caused a recursion. To allow limited recursion specify elements that can re')
    recursionlist.append(rootclass)

    return

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
