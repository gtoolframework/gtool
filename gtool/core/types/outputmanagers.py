# TODO collapse Filler and AttributeMatch then subclass

class Filler(object):
    def __init__(self, fillertext):
        self.__fillertext__ = fillertext

    def process(self):
        return '%s' % self.__fillertext__

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__fillertext__)


class AttributeMatch(object):
    def __init__(self, attrname):
        self.__concatmode__ = True if attrname[0] == '+' else False
        self.__attrname__ = attrname[1:] if self.__concatmode__ is True else attrname
        # print('__AttributeMatch:', self.__attrname__, 'concat mode:', self.__concatmode__)

    def __isdynamic__(self, obj):
        return getattr(obj, self.__attrname__).isdynamic

    @property
    def isconcatter(self):
        return self.__concatmode__

    def process(self, obj=None, sep=" ", outputscheme=None, flat=False):
        if obj is None:
            raise TypeError('Expected an object in obj kwarg')
        if not hasattr(obj, self.__attrname__):
            raise AttributeError('%s does not have a %s attribute as specified in the output format scheme:' % (
                obj.__class__, self.__attrname__))

        if not getattr(obj, self.__attrname__).isdynamic:
            return sep.join(['%s' % f for f in getattr(obj, self.__attrname__)])
        elif flat:
            return sep.join([f.output(outputscheme=outputscheme) for f in getattr(obj, self.__attrname__)])
        else:
            return


            # return sep.join(['%s' % f if not self.__isdynamic__(f) else f.output(outputscheme=outputscheme) for f in getattr(obj, self.__attrname__)])
            # return sep.join(['%s' % f for f in getattr(obj, self.__attrname__)])

    def process_to_list(self, obj=None, sep=" ", outputscheme=None):
        if hasattr(obj, self.__attrname__):
            """for g in getattr(obj, self.__attrname__):
                if isinstance(g,DynamicType):
                    print(type(g))
            """
            # return sep.join(['%s' % f if not isinstance(f,DynamicType) else f.outputaslist(outputscheme=outputscheme) for f in getattr(obj, self.__attrname__)])
            return [f for f in getattr(obj, self.__attrname__)]
        else:
            raise AttributeError('%s does not have a %s attribute as specified in the output format scheme:' % (
                obj.__class__, self.__attrname__))

    def __repr__(self):
        return '<%s>:%s' % (self.__class__, self.__attrname__)