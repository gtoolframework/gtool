class Matrix(object):

    def __init__(self, startwidth=100, startheight=50):
        self.__storage__ = [[None for i in range(startwidth)] for i in range(startheight)]
        self.__current_row__ = 0
        self.__current_col__ = 0
        self.__utilization_threshold__ = .75


    @property
    def cursor(self):
        return (self.__current_row__, self.__current_col__)

    @property
    def currentrow(self):
        return self.__current_row__

    @property
    def currentcol(self):
        return self.__current_col__

    def horitzontal_utlization(self):
        pass

    def vertical_utilization(self):
        pass

    def expand_vertical_space(self):
        pass

    def insert_vertical_space(self):
        pass

    def append_vertical_space(self):
        pass

    def expand_horizontal_space(self):
        pass

    def insert_horizontal_space(self):
        pass

    def append_horizontal_space(self):
        pass

    def update_row(self):
        pass

    def append_row(self):
        pass

    def update_col(self):
        pass

    def append_col(self):
        pass

    def data(self):
        #iter generator
        pass

    def append_cells_at_cursor(self):
        pass

    def append_row_below_cursor(self):
        pass