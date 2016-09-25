from gtool.core.types.core import Aggregator


class Sum(Aggregator):

    def __init__(self, config=None):
        super(Sum, self).__init__(config=config)

    def compute(self):
        selectionDict = super(Sum, self).compute()

        _selection = [v for v in selectionDict.values()][0]
        _name = [k for k in selectionDict.keys()][0]
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
        return {_name: _result}


def load():
    return Sum