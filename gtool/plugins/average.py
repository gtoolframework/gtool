from gtool.core.types.core import Aggregator


class Average(Aggregator):

    def __init__(self, config=None):
        super(Average, self).__init__(config=config)

    def compute(self):
        selectionDict = super(Average, self).compute()

        _selection = [v for v in selectionDict.values()][0]
        _name = [k for k in selectionDict.keys()][0]
        values = []
        for val in _selection:
            selectedvalue = getattr(val, self.targetattribute)
            if hasattr(selectedvalue, '__iter__'):
                _values = [v.raw() for v in selectedvalue]
                values.extend(_values)
            else:
                values.append(selectedvalue)
        if len(values) == 0:
            _result = None
        else:
            _result = sum(values)/len(values)
        return {'name':_name, 'result': _result}


def load():
    return Average