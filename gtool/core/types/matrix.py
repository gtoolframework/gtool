class Matrix(object):

    def __init__(self, startwidth=100, startheight=100):
        self.__storage__ = [[None for i in range(startwidth)] for i in range(startheight)]
        self.__current_row__ = 0
        self.__current_col__ = 0
        self.__utilization_threshold__ = .75

    @property
    def cursor(self):
        # x,y position
        return (self.__current_col__, self.__current_row__)

    @property
    def currentrow(self):
        return self.__current_row__

    @property
    def currentcol(self):
        return self.__current_col__

    def __height__(self):
        return len(self.__storage__)

    @property
    def height(self):
        return self.__height__()

    def __width__(self):
        #assumes matrix is uniformly sized
        return len(self.__storage__[0])

    @property
    def width(self):
        return self.__width__()

    def dimensions(self):
        return (self.__width__(), self.__height__())

    def horitzontal_utlization(self):
        _result = 0
        rowlength = self.__width__()
        for row in self.__storage__:
            endoflist = 0
            for i, cell in enumerate(row):
                x = i+1
                if row[-x] is not None:
                    endoflist = rowlength - x
                    break # avoids unnecesary interations
            _result = max(endoflist, _result)
        # calculate utlization
        return round(_result/rowlength, 2)

    def vertical_utilization(self):
        colheight = len(self.__storage__)
        for i, row in enumerate(self.__storage__):
            if any(x is not None for x in self.__storage__[-i+1]):
                return round((colheight - (i+1))/colheight, 2)

    def utilization(self):
        # x,y
        return(self.horitzontal_utlization(),self.vertical_utilization())

    def append_cols(self, cols=10):
        rowlength = self.__width__()
        for i, row in enumerate(self.__storage__):
            if len(row) == rowlength:
                row.extend([None for x in range(cols)])
            else:
                raise IndexError('Row %s is not the same length as the other rows in the matrix' % i)
        return True

    def insert_cols(self, x, cols=10):
        # insert col at x
        if cols < 1:
            raise ValueError('cannot insert less than 1 column.')
        if x < 0 or x >= self.__width__():
            raise IndexError('cannot insert cols outside the x range of the matrix. Use append instead')
        try:
            for row in self.__storage__:
                row[x:x] = [None] * cols
        except:
            raise Exception('could not insert %s columns at column %s in the matrix' % (cols, x))

        return True

    def insert_rows(self, y, rows=10):
        #insert row at y
        if rows < 1:
            raise ValueError('cannot insert less than 1 row.')
        if y < 0 or y >= self.__height__():
            raise IndexError('cannot insert rows outside the y range of the matrix. Use append instead')
        try:
            self.__storage__[y:y] = [[None] * self.__width__()] * rows
            #.insert(y, [[None for j in range(self.width)] for i in range(rows)]):
        except:
            raise Exception('could not insert %s rows at row %s in the matrix' % (rows, y))

        return True


    def append_rows(self, rows=10):
        rowlength = self.__width__()
        _newrows = [[None for x in range(rowlength)] for y in range(rows)]
        self.__storage__.extend(_newrows)
        return True

    def getrow(self, y):
        return self.__storage__[y]

    def getcol(self, x):
        return [row[x] for row in self.__storage__]

    def getcell(self, x, y):
        return self.__storage__[y][x]

    def data(self):
        # return storage one row at a time iter generator
        return (row for row in self.__storage__)

    def insert(self, cursor=(0,0), datamatrix=None):
        x, y = cursor
        if datamatrix is None or not isinstance(datamatrix, list):
            raise ValueError('Was expecting to insert a list but got a %s' % type(datamatrix))
        if x < 0:
            raise IndexError('A coordinate outside the x axis of the matrix was provided')
        if y < 0:
            raise IndexError('A coordinate outside the y axis of the matrix was provided')

        if y > int(self.__height__() * self.__utilization_threshold__):
            # grow enough so that we're back to ~70% vertical utilization
            _delta = int(y / (self.__utilization_threshold__ - .05) - self.__height__()) + 1
            print(_delta)
            if not self.append_rows(rows=_delta):
                raise Exception('Could not append more rows to the matrix')

        if x + len(datamatrix) > self.__width__():
            print('expanding x')
            _delta = int(x / (self.__utilization_threshold__ - .05) - self.__width__()) + 1
            print(_delta)
            if not self.append_cols(cols=_delta):
                raise Exception('Could not append more columns to the matrix')

        # TODO secondary safety check to make sure we'll be in range

        _x_end = x + (len(datamatrix) - 1)
        self.__storage__[y][x:_x_end] = datamatrix

    def __matrixmap__(self):
        # returns a matrix of the same size but shows how much data is
        return [[len(x) if x is not None else 0 for x in y] for y in self.__storage__]