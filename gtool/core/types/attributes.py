from gtool.core.namespace import namespace
from gtool.core.plugin import pluginnamespace

class attribute(object):

    def __init__(self, *pargs, typeclass=None, singleton=True, required=True,
                 posargs=None, kwargs=None, parent=None,
                 attributename=None, **keywordargs):

        self.args = pargs
        self.kwargs = keywordargs
        self.__init__ = dict()
        initdict = self.__init__
        initdict['singleton'] = singleton
        initdict['validatedict'] = None
        initdict['__class__'] = typeclass
        initdict['class'] = self.__lazyloadclass__
        initdict['posargs'] = posargs
        initdict['kwargs'] = kwargs # TODO should preprocess into dict
        # make each storage list unique, do not load with values on init
        self.__storage__ = [] # prevents weakly referenced shared list problem
        self.__parent__ = parent
        self.__attributename__ = attributename
        self.__required__ = required # TODO do something with this (in classgen have mandatoryproperties query this)

    @property
    def attrfilematch(self):
        _class = self.__init__['__class__']
        return namespace()[_class.upper()].classfile()

    @property
    def __validationrequired__(self):
        """
        Checks if validation is required during data load.
        Should always be true except for classes that handle their own validation
        :return: True if attribute validation routines should be called when data is loaded.
        """
        _class = self.__init__['__class__']
        if _class in globals():
            # user created class
            return True
        elif _class.upper() in namespace():
            # an attribute that is a user created class, it will handle it's own validation
            return False
        elif _class.upper() in pluginnamespace():
            # an attribute that relies on a plugin
            return True
        else:
            raise TypeError('I cannot find %s in the globals, plugins or class namespaces' % _class)


    def __lazyloadclass__(self):
        """
        defers evaluation of the attribute class. If it occured during init there would be unresolved dependencies
        :return: object
        """
        _class = self.__init__['__class__']
        if _class in globals():
            return globals()[_class]
        elif _class.upper() in namespace():
            return namespace()[_class.upper()]
        elif _class.upper() in pluginnamespace():
            return pluginnamespace()[_class.upper()]

    @property
    def attrtype(self):
        return self.__init__['class']()

    def __convert__(self, value):
        return self.__init__['class']().__converter__()(value) # return a type from type definition (such at gtool.types.common)

    def __validators__(self, item):
        # need to extract the provided validators but only return those that the type uses
        # kwargs will contain other values that aren't used for validation
        _kwargDict = {pair[0]:pair[1] for pair in self.__init__['kwargs']}
        validatorDict = {}
        for validator in item.__validators__:
            validatorDict[validator] = _kwargDict.get(validator, None)
        return validatorDict

    def __validate__(self, item):
        _class = self.__init__['class']()
        if not isinstance(item, _class):
            raise TypeError('%s can only hold %s but got %s' % (
                self.__context__(),
                self.__init__['class'](),
                type(item)
            )
                            )
        if self.__init__['kwargs'] is not None and  self.__validationrequired__ is True:
            try:
                item.__validate__(self.__validators__(item))
            except ValueError as verror:
                # TODO fix this error message generation, it doesn't look like the others
                errormsg = ('For {0}: {1}'.format(self.__context__(), verror))
                raise ValueError(errormsg)
        return True

    def __load__(self, item):
        # should be called by load from dynamically generated class
        # __load__ overwrites the storage while append adds to it
        # TODO merge/refactor __load__ and append
        _storage = []
        if isinstance(item, list):
            if self.issingleton() and len(item) > 1:
                raise ValueError('For %s: Cannot add multiple items to a singleton attribute' % self.__context__())
            for itemiter in item:
                self.__validate__(itemiter)
                _storage.append(itemiter)
        else:
            # TODO check if we still need this else block given the issingleton + len > 1 check
            self.__validate__(item)
            _storage.append(item)
        self.__storage__ = _storage
        return True

    def load(self, item):
        # wrapper method for loading directly into the attribute
        return self.__load__(item)

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
        return iter(self.__storage__)

    def __len__(self):
        return len(self.__storage__)

    """
    def __getattr__(self, attr):
        return self.init[attr]
    """

    def __repr__(self):
        #return '%s' % ['%s' % f for f in self.__storage__]
        return '%s' % self.__storage__

    def __cmp__(self, other):
        if len(self.__storage__) != len(other.__storage__):
            raise ValueError('comparison items are not the same length')
        retBool = True
        for i, item in enumerate(self.__storage__):
            if item != other.__store__[i]:
                retBool = False
                break
        return retBool

    def issingleton(self):
        return self.__init__['singleton']

    def __context__(self):
        return '%s::%s' % (self.__parent__, self.__attributename__)
