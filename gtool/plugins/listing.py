from gtool.core.types.core import Aggregator


class Listing(Aggregator):

    def __init__(self, config=None):
        super(Listing, self).__init__(config=config)

    def compute(self):
        selectionDict = super(Listing, self).compute()

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

        print(values)
        return {'name':_name, 'result': values}


def load():
    return Listing