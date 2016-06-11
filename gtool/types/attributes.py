class attribute(object):

    def __init__(self, *pargs, typeclass=None, singleton=True,
                 posargs=None, kwargs=None, parent=None,
                 attributename=None, **keywordargs):

        print('attrib init: start')
        self.args = pargs
        self.kwargs = keywordargs
        self.__init__ = dict()
        initdict = self.__init__
        initdict['singleton'] = singleton
        initdict['validatedict'] = None
        initdict['class'] = typeclass
        initdict['posargs'] = posargs
        initdict['kwargs'] = kwargs
        # make each storage list unique, do not load with values on init
        self.__storage__ = [] # prevents weakly referenced shared list problem
        self.__parent__ = parent
        self.__attributename__ = attributename

        print('attrib init: end')

    @property
    def attrtype(self):
        return self.__init__['class']

    def __convert__(self, value):
        return self.__init__['class'].__converter__()

    def __validators__(self, item):
        validatorDict = {}
        for validator in item.__validators__:
            validatorDict[validator] = self.__init__['kwargs'].get(validator, None)
        return validatorDict

    def __validate__(self, item):
        if not isinstance(item, self.__init__['class']):
            raise TypeError('%s can only hold %s but got %s' % (
                self.__context__(),
                self.__init__['class'],
                type(item)
            )
                            )
        if self.__init__['kwargs'] is not None:
            try:
                item.__validate__(self.__validators__(item))
            except ValueError as verror:
                errormsg = ('For {0}: {1}'.format(self.__context__(), verror))
                raise ValueError(errormsg)
        return True

    def __load__(self, item):
        # should be called by load from dynamically generated class
        # __load__ overwrites the storage while append adds to it
        # TODO merge/refactor __load__ and append
        _storage = []
        if isinstance(item, list):
            if self.issingleton():
                raise ValueError('For %s: Cannot add multiple items to a singleton attribute' % self.__context__())
            for itemiter in item:
                self.__validate__(itemiter)
                _storage.append(itemiter)
        else:
            self.__validate__(item)
            _storage.append(item)

        self.__storage__ = _storage
        return True

    def load(self, item):
        return self.__load__()

    def __set__(self, item):
        self.__validate__(item)
        self.__storage__ = [item]

    def append(self, item):
        if self.issingleton() and len(self.__storage__) > 0:
            raise ValueError('In %s: Cannot add multiple items to a singleton attribute' % self.__context__())
        # limited recursion
        if isinstance(item, list):
            if self.issingleton() and len(item) > 1:
                raise ValueError('In %s: Cannot add multiple items to a singleton attribute' % self.__context__())
            for itemiter in item:
                self.append(itemiter)
        self.__validate__(item)
        self.__storage__.append(item)


    def __iter__(self):
        return self.__storage__

    """
    def __getattr__(self, attr):
        return self.init[attr]
    """

    def __repr__(self):
        return '%s' % self.__storage__

    def __cmp__(self, other):
        if len(self.__storage__) != len(other.__storage__):
            raise ValueError('comparison items are not the same length')
        retBool = True
        for i, item in enumerate(self.__storage__):
            if item != other.store[i]:
                retBool = False
                break
        return retBool


    def issingleton(self):
        return self.__init__['singleton']

    def __context__(self):
        return '%s::%s' % (self.__parent__, self.__attributename__)
