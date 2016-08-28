from gtool.core.utils.output import formatternamespace
from gtool.core.filewalker import registerFileMatcher
from gtool.core.utils.misc import striptoclassname


class CoreType(object):
    """
    CoreType is the base object for all attribute types (except user created classes)
    """

    def __init__(self, *args, **kwargs):
        self.__valuetype__ = kwargs.pop('valuetype', None)
        if self.__valuetype__ == None:
            raise NotImplementedError('You need to specify a valuetype in keyword args')

        # assume singleton if not overridden
        # self.__singleton = kwargs.pop('singleton', True)

        initvalue = None
        if len(args) > 0:
            initvalue = args[0]
        self.__value__ = initvalue #None

    # TODO valid alternative repr requirements (if any)
    def __repr__(self):
        return '%s' % self.__value__

    def __str__(self):
        return '%s' % self.__value__

    def __validate__(self, validatedict):
        """
        Abstract Validation method, must be implemented by sub-classes.
        Must raise a ValueError if the value does not match the criteria
        Look at gtool.type.common for examples
        """
        raise NotImplementedError('Please implement a __validate__ method for your class %s' % self.__class__)

    @classmethod
    def __convert__(cls, item):
        try:
            return cls.__convertor__()(item)
        except ValueError:
            raise ValueError('cannot convert %s to type %s' %(item, cls.__convertor__()))


class DynamicType(object):
    """
    base object for dynamically generated classes
    """

    @classmethod
    def classfile(cls):
        if 'file' in cls.metas():
            return cls.__metas__.get('file')
        else:
            return None

    @classmethod
    def register(cls, classname):
        # only register if a file prefix is provided
        if cls.classfile() is not None:
            registerFileMatcher(cls.classfile(), classname)
        else:
            raise AttributeError('%s does not have a *file attribute defined' % classname)

    @classmethod
    def metas(cls):
        if hasattr(cls, '__metas__'):
            return cls.__metas__
        else:
            # print('has no metas')
            return None

    @classmethod
    def displayname(cls):
        return cls.metas()['displayname'] if 'displayname' in cls.metas() else '%s' % cls

    # TODO determine which methods from utils.classgen.methods can be moved in here

    def __classoutputscheme__(self):
        return formatternamespace()[striptoclassname(self.__class__)]

    def asdict(self):
        _retdict = {}
        for k, v in self:
            if not v.isdynamic:
                _v = ['%s' % i for i in v]
            else:
                _v = [i.asdict() for i in v]
            _retdict[k] = _v
        return _retdict

    def __iter__(self):
        for item in self.__list_slots__.keys():
            yield (item, self.__list_slots__[item])