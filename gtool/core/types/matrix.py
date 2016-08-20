class Matrix(object):

    def __init__(self, startwidth=100, startheight=100, threshold=.75):
        self.__storage__ = [[None for i in range(startwidth)] for i in range(startheight)]
        self.__current_row__ = 0
        self.__current_col__ = 0
        self.__utilization_threshold__ = threshold

    @property
    def cursor(self):
        # x,y position
        return (self.__current_col__, self.__current_row__)

    def get_currentrow(self):
        return self.__current_row__

    def set_currentrow(self, y):
        if not isinstance(y, int):
            raise TypeError('y arg to set current cursor row must be an int but got a', type(y))
        if y > self.__height__() - 1:
            raise IndexError('y is outside of matrix vertical bounds')
        self.__current_row__ = y

    currentrow = property(get_currentrow, set_currentrow)
    y = property(get_currentrow, set_currentrow)

    def get_currentcol(self):
        return self.__current_col__

    def set_currentcol(self, x):
        if not isinstance(x, int):
            raise TypeError('x arg to set current cursor column must be an int but got a', type(x))
        if x > self.__width__() - 1:
            raise IndexError('x is outside of matrix horizontal bounds')
        self.__current_row__ = x

    currentcol = property(get_currentcol, set_currentcol)
    x = property(get_currentcol, set_currentcol)

    def __height__(self):
        return len(self.__storage__)

    @property
    def height(self):
        return self.__height__()

    def __width__(self):
        #assumes matrix is uniformly sized
        if len(self.__storage__) > 0:
            return len(self.__storage__[0])
        else:
            return 0

    @property
    def width(self):
        return self.__width__()

    def dimensions(self):
        return (self.__width__(), self.__height__())

    def __h_utilization__(self):
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
        if _result is None:
            _result = 0
        return _result

    def __h_utilization_percentage__(self):
        return round(self.__h_utilization__() / self.__width__(), 2)

    def __v_utilization__(self):
        colheight = len(self.__storage__)
        for i, row in enumerate(self.__storage__):
            if any(x is not None for x in self.__storage__[-(i+1)]):
                return colheight - (i+1)
        return 0 #default if no utilization

    def __v_utilization_percentage__(self):
        colheight = self.__v_utilization__()
        if colheight == 0:
            return 0
        else:
            return round(colheight/ colheight, 2)

    def utilization(self):
        # return x,y utilization
        return(self.__h_utilization_percentage__(), self.__v_utilization_percentage__())

    def healthcheck(self):
        # check utilization and if above threshold append more rows or columns to matrix

        _h_use = self.__h_utilization_percentage__()
        _v_use = self.__v_utilization_percentage__()
        threshold = self.__utilization_threshold__

        if _v_use > threshold:
            if not self.append_rows(rows=(int(_v_use / (threshold - .05))) - self.__height__()):
                raise Exception('could not expand the matrix with additional rows')

        if _h_use > threshold:
            if not self.append_cols(cols=(int(_h_use / (threshold - .05))) - self.__width__()):
                raise Exception('could not expand the matrix with additional columns')

        return True

    def trim(self):
        """
        Trims unused space from the right (highest X coord) and bottom (highest Y coord) sides of the matrix.
        Will prevent the matrix from being destroyed by trimming to zero width and length
        :return: True if trimming occurred.
        """

        h_use = self.__h_utilization__()
        v_use = self.__v_utilization__()
        _ret = False #default return value

        if v_use == 0:
            raise IndexError('Cannot trim an empty matrix. Use delete instead.')

        if v_use < self.__height__():
            _ret = True
            try:
                del self.__storage__[v_use:]
            except:
                raise IndexError('Could not delete row %s from the matrix' % v_use)

        if h_use < self.__width__():
            _ret = True
            for i, row in enumerate(self.__storage__):
                try:
                    del row[h_use+1:]
                except:
                    raise IndexError('Could not delete columns in row %s from the matrix' % i)

        """
        # check that Matrix still exists and if not rebuild it to a single column and cell
        # TODO this is a possible edge case, perhaps should through an error if trim called on empty matrix
        if not self.__height__() > 0:
            self.__storage__ = [[None]]
        """

        # make sure cursor is back in Y bounds
        if self.__height__() - 1 < self.__current_row__:
            self.__current_row__ = self.__height__() - 1

        # make sure cursor is back in X bounds
        if self.__width__() -1 < self.__current_col__:
            self.__current_col__ = self.__width__()

        #TODO check if self.cursor is out of bounds

        return _ret

    def append_cols(self, cols=10):
        rowlength = self.__width__()
        for i, row in enumerate(self.__storage__):
            if len(row) == rowlength:
                row.extend([None] * cols)
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
        _newrows = [[None] * rowlength] * rows
        self.__storage__.extend(_newrows)
        return True

    def getrow(self, y):
        return self.__storage__[y]

    def getcol(self, x):
        return [row[x] for row in self.__storage__]

    def getcell(self, x, y):
        return self.__storage__[y][x]

    def __iter__(self):
        # return storage one row at a time iter generator
        for row in self.__storage__:
            yield row

    def insert(self, cursor=(0,0), datalist=None, healthcheck=True):
        """
        Inserts datalist at location specified by cursor.
        If no cursor if provided, default cursor of 0,0 will be assumed
        :param cursor: tuple (x,y)
        :param datalist: list
        :param healthcheck: Boolean
        :return: string
        """
        x, y = cursor
        if datalist is None or not isinstance(datalist, list):
            raise ValueError('Was expecting to insert a list but got a %s' % type(datalist))
        if not len(datalist) > 0:
            raise ValueError('Cannot insert a datalist of 0 length')
        if x < 0:
            raise IndexError('A coordinate outside the x axis of the matrix was provided')
        if y < 0:
            raise IndexError('A coordinate outside the y axis of the matrix was provided')

        # grow columns if needed
        if y > int(self.__height__() * self.__utilization_threshold__):
            # grow enough so that we're back to ~70% vertical utilization
            _delta = int(y / (self.__utilization_threshold__ - .05) - self.__height__()) + 1
            #print(_delta)
            if not self.append_rows(rows=_delta):
                raise Exception('Could not append more rows to the matrix')

        # grow rows if needed
        if x + len(datalist) > self.__width__():
            #print('expanding x')
            _delta = int((x + len(datalist)) / (self.__utilization_threshold__ - .05) - self.__width__()) + 1
            #print(_delta)
            if not self.append_cols(cols=_delta):
                raise Exception('Could not append more columns to the matrix')

        # TODO secondary safety check to make sure we'll be in range
        # TODO call healthcheck (don't if being called by bulk_insert)

        _x_end = x + (len(datalist))
        try:
            self.__storage__[y][x:_x_end] = datalist
        except:
            raise Exception('An error occured when attempting to insert data into the matrix')

        # update cursor
        self.__current_row__ = y
        self.__current_col__ = x + len(datalist) # + 1

        if healthcheck is True:
            self.healthcheck()
        return True

    def bulk_insert(self, cursor=(0,0), rows=None):
        # TODO can we make bulk insert more efficient, currently it's just a wrapper
        #insert multiple rows, all must start at the same column
        x, y = cursor
        if rows is None or not (isinstance(rows, list) or isinstance(rows, Matrix)):
            raise ValueError('Was expecting to insert a list or Matrix but got a %s' % type(rows))
        if not all(isinstance(row, list) for row in rows):
            raise ValueError('Was expecting a list of lists to be passed through param rows')
        for i, row in enumerate(rows):
            if not len(row) > 0:
                raise ValueError('Cannot insert row %s as it has zero length' % i)
            if not self.insert(cursor=(x,y+i), datalist=row, healthcheck=False):
                raise Exception('Could not insert row %s into the matrix' % i)

        self.healthcheck() #do healthcheck here instead of inside insert so that we don't call healthcheck repeatedly
        return True

    def col(self, x):
        """
        Returns the column of a matrix
        :param x: x coordinate of column you want returned
        :return: list containing column values
        """
        if not isinstance(x, int):
            raise TypeError('Was expecting an integer but got a', type(x))
        return [row[x] for row in self.__storage__]

    def row(self, y):
        """
        Returns the column of a matrix
        :param y: y coordinate of row you want returned
        :return: list containing row values
        """
        if not isinstance(y, int):
            raise TypeError('Was expecting an integer but got a', type(y))
        return self.__storage__[y]

    def nextrow(self):
        """
        Go to the next row, same column (syntactic sugar)
        :return:
        """
        self.__current_row__ += 1

    def returntofirst(self):
        """
        Go to first column but stay in current row (syntactic sugar)
        :return:
        """
        self.__current_col__ = 0

    def carriagereturn(self):
        """
        Go to first column, next row (synactic sugar)
        :return:
        """
        self.nextrow()
        self.returntofirst()

    def __matrixmap__(self, trim=True):
        # returns a matrix of the same size but shows how much data is
        _retmatrix = Matrix(startwidth=self.__h_utilization__(), startheight=self.__v_utilization__())
        _mmap = [[len(x) if x is not None else 0 for x in y] for y in self.__storage__]

        _retmatrix.bulk_insert(rows=_mmap)
        if trim:
            _retmatrix.trim()
            _retmatrix.trim()
        return _retmatrix

    def __repr__(self):
        return '<Matrix> Height: {0}, Width: {1}'.format(
            self.__height__(), self.__width__())

    @property
    def isempty(self):
        return True if self.__v_utilization__() == 0 else False