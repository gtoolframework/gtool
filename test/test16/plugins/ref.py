from gtool.types.core import CoreType

class Ref(CoreType):
    """
    Ref expects an absolute reference in the form of /node1/node2. The reference must start with a / and end with an alpha value
    """

    def isReference(self, ref):
        separator = '/'
        if separator in ref:
            _splitlist = ref.split(separator)
            #print('in ref:', _splitlist)
            # make sure that the ref starts with a /, has at least one node and doesn't end with /
            if len(_splitlist) > 1 and len(_splitlist[0]) == 0 and len(_splitlist[-1:]) > 0:
                return True

        return False

    def __validate__(self, valuedict):
        # Ref doesn't have validation options
        if self.isReference(self.__value__):
            return True
        else:
            raise ValueError('Was expecting a valid reference URI of the form /node/node but got %s' % self.__value__)

    @classmethod
    def __converter__(cls):
        return str

    def __init__(self, *args, **kwargs):
        # TODO should validate that the ref is actually valid
        self.__validators__ = [] # Ref doesn't have validation options
        super().__init__(*args, valuetype=str, **kwargs)

def load():
    return Ref