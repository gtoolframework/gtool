from .core import CoreType

class Number(CoreType):

    identifierRegex = "number regex"

    def __validate__(self, valuedict):
        _min = valuedict.get('min', None)
        _max = valuedict.get('max', None)
        min = int(_min) if _min is not None else None
        max = int(_max) if _max is not None else None
        if min is not None:
            if self.__value__ < min:
                raise ValueError('Values must be not be lower than %s but we got %s' % (min, self.__value__))
        if max is not None:
            if self.__value__ > max:
                raise ValueError('Values must not be higher than %s but we got %s' % (max, self.__value__))
        return True

    def __init__(self, *args, **kwargs):
        # _min = kwargs.get('min', None)
        # _max = kwargs.get('max', None)
        # self.min = int(_min) if _min is not None else None
        # self.max = int(_max) if _max is not None else None
        self.__validators__ = ['min', 'max']
        super().__init__(*args, valuetype=int, **kwargs)


class String(CoreType):

    identifierRegex = "string regex"

    def __validate__(self, valuedict):
        _maxlength = valuedict.get('maxlength', None)
        maxlength = int(_maxlength) if _maxlength is not None else None
        if maxlength is not None:
            if len(self.__value__) > maxlength:
                raise ValueError('Was expecting a string no more than %s chars long '
                                 'but the string had a length of %s' % (maxlength, len(self.__value__)))
        return True

    def __init__(self, *args, **kwargs):
        #_maxlength = kwargs.get('maxlength', None)
        #self.maxlength = int(_maxlength) if _maxlength is not None else None
        self.__validators__ = ['maxlength']
        super().__init__(*args, valuetype=str, **kwargs)


class Choice(CoreType):

    identifierRegex = "choice regex"

    def __validate__(self, valuedict):
        # TODO validate for choice
        # print('validate choice')
        # print(value)
        _choices = valuedict.get('choices', None)
        choices = _choices[1:-1].split(',') if _choices is not None else None
        if self.__value__ not in choices:
            raise ValueError('Was expecting either one of %s but got a %s' % (choices, self.__value__))
        return True

    def __init__(self, *args, **kwargs):
        #_choices = kwargs.get('choices', None)
        #self.choices = _choices[1:-1].split(',') if _choices is not None else None
        self.__validators__ = ['choices']
        super().__init__(*args, valuetype=str, **kwargs)



