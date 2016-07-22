from gtool.core.types.matrix import Matrix

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


