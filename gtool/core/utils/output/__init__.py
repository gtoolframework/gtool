from gtool.core.types.matrix import Matrix
import gtool.core.types.outputmanagers as om
import pyparsing as p
from gtool.core.filewalker import StructureFactory
from gtool.core.utils.misc import striptoclassname
from gtool.core.utils.runtime import runtimenamespace
from gtool.core.utils.config import partialnamespace
from gtool.core.plugin import pluginnamespace
#import gtool.core.types.output as outputtypes

def outputconfigname(outputscheme=str()):
    return 'output.' + outputscheme

def structureflatten(exp):
    """
    flattens a list or dict in strings
    :param exp: list or dict
    :return: list of strings
    """
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


def structureflattentolist(exp):
    """
    flattens a list or dict in strings
    :param exp: list or dict
    :return: list of strings
    """

    def sub(exp, res):
        if type(exp) == dict:
            for k, v in exp.items():
                yield from sub(v, res + [k])
        elif type(exp) == list:
            if all(not isinstance(v, dict) and not isinstance(v, list) for v in exp):
                _exp = list(set(exp)) # make unique
                if len(_exp) > 1:
                    yield res + [sorted(_exp, key=str.lower)]
                else:
                    yield res + _exp
            else:
                for v in exp:
                    yield from sub(v, res)
        else:
            yield res + [exp]

    yield from sub(exp, [])

def findlongest(flatstructure):
    """
    From a set of unique strings returns the longest
    :param flatstructure: set of strings
    :return: longest string
    """
    if not isinstance(flatstructure, set):
        raise TypeError('findlongest function expected an arg'
                         'that is of type set but got a %s' % type(flatstructure))

    _maxlen = 0
    _longest = None

    for i in flatstructure:
        # print('length:', len(i))
        if len(i) > _maxlen:
            _longest = i
            _maxlen = len(_longest)

    # print(_longest)
    return _longest

def reversematch(project=None, matchstring=None):
    """
    Finds objects that meet the structure in the matchstring
    :param project: structurefactory object
    :param matchstring: string from structureflatten
    :return: list of paths
    """

    def sub(matchlist, node, result, numbering=True):
        #returns results via list reference
        if isinstance(node, StructureFactory.Container):
            _class = 'container'
        else:
            _class = striptoclassname(node.__objectmatch__())
        if _class == matchlist[0] and len(matchlist) == 1:
            if numbering:
                result.append('({0}) {1}'.format(len(result)+1, node.fileobject.path))
            else:
                result.append(node.fileobject.path)
        elif _class == matchlist[0] and len(matchlist) > 1 and len(node.children) > 0:
            for child in node.children:
                sub(matchlist[1:], child, result)


    if not isinstance(project, StructureFactory.Container):
        raise TypeError('function reversematch expected a project kwarg of type'
                        'StructureFactory.Container but received an object of type %s' % type(project))

    if not isinstance(matchstring, str):
        raise TypeError('function reversematch expected a matchstring kwarg of'
                        'type str but got a %s', type(matchstring))


    # remove quotes and brackets from this stringified list and convert it back into a list
    matchlist = ['{0}'.format(k).strip() for k in ''.join([a for a in matchstring[1:-1] if a is not "'"]).split(',')]
    #matchlist = matchstring.split('/')
    _matches = []
    for child in project.children:
        sub(matchlist[1:], child, _matches)

    return _matches

def recursioncheck(project):

    def flatten(pathlist):
        result = []
        for i in pathlist:
            if isinstance(i, list):
                result.append('[{0}]'.format(flatten(i)))
            else:
                result.append(i)
        return result

    def sub(currentbranch, seen):
        for i in currentbranch:
            if isinstance(i, list):
                sub(i, seen)
            else:
                if i in seen:
                    _longbranch = '/'.join(flatten(currentbranch))
                    _exception = 'A recursive loop has been detected in {0}. ' \
                                 'The class {1} is seen twice in the same path. ' \
                                 'Make sure that one class does not call itself, ' \
                                 'either directly or indirectly.'.format(_longbranch, i)
                    raise ValueError(_exception)
                else:
                    seen.append(i)

    if not isinstance(project, StructureFactory.Container):
        raise TypeError('function recursioncheck expected an arg of type StructureFactory.Container but received an object of type %s' % type(project))

    _tree = project.treestructure()

    for branch in structureflattentolist(_tree):
        sub(branch, [])

    return True


# TODO move checkalignment and supporting funcs over to type.output and embedded in Output class (may cause problems due to import of pluginnamespace
def checkalignment(project):

    if not isinstance(project, StructureFactory.Container):
        raise TypeError('function checkalignment expected an arg of type StructureFactory.Container but received an object of type %s' % type(project))

    uniquebranches = set()
    _tree = project.treestructure()

    for i in structureflattentolist(_tree):
        uniquebranches.add('%s' % i) #cheap hack to make list hashable

    _longest = findlongest(uniquebranches) #(s)

    if len(uniquebranches) == 1:
        return True

    for i in uniquebranches: #s:
        if i[1:-1] not in _longest[1:-1]:
            _nonmatching = '\n '.join(reversematch(project=project, matchstring=i))
            _outputplugin = partialnamespace('output')[runtimenamespace()['outputscheme']]['plugin']
            # have to compare strings instead of using isinstance to avoid circular imports
            _treeoutputplugins = '* ' + '\n *'.join(['%s' % k for k,v in pluginnamespace().items() if 'TreeOutput' in str(v.__bases__)])
            _exception = 'Found an object structure {0} ' \
                         'that does not align with the longest object structure {1}. ' \
                         'The non-aligned objects can be found at:\n{2}. ' \
                         '\n\nThis error occured because the output plugin, {3}, requires aligned output. ' \
                         'If you do not want to align your data structure, please use an output plugin ' \
                         'that does not require aligned data. Available plugins that do not require ' \
                         'aligned data include:\n\n{4}'.format(i, _longest, _nonmatching, _outputplugin, _treeoutputplugins)

            raise ValueError(_exception)

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

            _start = cell[prestart:start]
            if len(_start) > 0:
                # conditional logic avoids empty leading output cells
                _templist.append(om.Filler(_start))
            _templist.append(om.AttributeMatch(cell[start + 1:end])) #, classname=classname))
            prestart = end
            # print('templist:', _templist)
        _end = cell[end:]
        if len(_end) > 0:
            # conditional logic avoids empty trailing output cells
            _templist.append(om.Filler(cell[end:]))
        cells.append(_templist)

    return cells

"""
def descend(rootclass=None, recursionlist=[], recursionmembers=[], recusionlimit=0):
    if rootclass is None:
        raise ValueError('rootclass argument required but not provided')
    #detect recursion
    if rootclass in recursionlist and rootclass not in recursionmembers:
        raise RecursionError('The format string has caused a recursion. To allow limited recursion specify elements that can re')
    recursionlist.append(rootclass)

    return
"""
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
