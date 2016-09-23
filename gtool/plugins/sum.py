from gtool.core.types.core import Aggregator


class Sum(Aggregator):

    def __init__(self, config=None):
        super(Sum, self).__init__(config=config)

    def compute(self):
        _selection = super(Sum, self).compute()
        values = []
        for val in _selection:
            _values = [v.raw() for v in getattr(val, self.targetattribute)]
            values.extend(_values)
        if len(values) == 0:
            return None
        _result = sum(values)
        """
        for num in values:
            _result += num.raw()
        """
        return _result


def load():
    return Sum