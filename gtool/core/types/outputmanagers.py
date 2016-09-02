#from gtool.core.namespace import namespace

# TODO collapse Filler and AttributeMatch then subclass

class Filler(object):
    def __init__(self, fillertext):
        self.__fillertext__ = fillertext

    def __str__(self):
        return '%s' % self.__fillertext__

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__fillertext__)


class AttributeMatch(object):
    def __init__(self, attrname): #, classname=""):
        self.__concatmode__ = True if attrname[0] == '+' else False
        self.__attrname__ = attrname[1:] if self.__concatmode__ is True else attrname
        # print('__AttributeMatch:', self.__attrname__, 'concat mode:', self.__concatmode__)

    def __isdynamic__(self, obj):
        return getattr(obj, self.__attrname__).isdynamic

    @property
    def isconcatter(self):
        return self.__concatmode__

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__attrname__)