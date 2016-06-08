from .core import CoreType

class Number(CoreType):

    identifierRegex = "number regex"

    def __validate__(self, value):
        # TODO validate for number range
        if self.min is not None:
            if value < self.min:
                raise ValueError('Values must be not be lower than %s but we got %s' % (self.min, value))
        if self.max is not None:
            if value > self.max:
                raise ValueError('Values must not be higher than %s but we got %s' % (self.min, value))
        return True

    def __init__(self, *args, **kwargs):
        _min = kwargs.get('min', None)
        _max = kwargs.get('max', None)
        self.min = int(_min) if _min is not None else None
        self.max = int(_max) if _max is not None else None
        self.__validators__ = ['min', 'max']
        super().__init__(*args, listtype=int, **kwargs)


class String(CoreType):

    identifierRegex = "string regex"

    def __validate__(self, value):
        # TODO validate for string length
        if self.maxlength is not None:
            if len(value) > self.maxlength:
                raise ValueError('Was expecting a string no more than %s chars long '
                                 'but the string had a length of %s' % (self.maxlength, len(value)))
        return True

    def __init__(self, *args, **kwargs):
        _maxlength = kwargs.get('maxlength', None)
        self.maxlength = int(_maxlength) if _maxlength is not None else None
        self.__validators__ = ['maxlength']
        super().__init__(*args, listtype=str, **kwargs)


class Choice(CoreType):

    identifierRegex = "choice regex"

    def __validate__(self, value):
        # TODO validate for choice
        # print('validate choice')
        # print(value)
        if value not in self.choices:
            raise ValueError('Was expecting either one of %s but got a %s' % (self.choices, value))
        return True

    def __init__(self, *args, **kwargs):
        _choices = kwargs.get('choices', None)
        self.choices = _choices[1:-1].split(',') if _choices is not None else None
        self.__validators__ = ['choices']
        super().__init__(*args, listtype=str, **kwargs)



