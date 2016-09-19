from gtool.core.types.core import CoreType

class Ref(CoreType):
    """
    Ref expects an absolute reference in the form of /node1/node2. The reference must start with a / and end with an alpha value
    """

    def isReference(self, ref):
        separator = '/'
        emptysplit = ''

        if separator not in ref:
            return False
        _splitlist = ref.split(separator)

        # make sure that the ref starts with a /, has at least one node and doesn't end with /
        # rejection sieve
        if len(_splitlist) <= 1:
            # can't reference the root /
            return False
        if _splitlist[0] != emptysplit:
            # ref must start with /
            return False
        if ref.endswith(separator):
            # ref must not end with /
            return False

        for node in _splitlist:
            # node name's can't
            if not(node.isalpha()) and node != emptysplit:
                return False
        # end of rejection sieve
        # mmust be true then
        return True

    def __validate__(self, valuedict):
        # Ref doesn't have validation options
        if self.isReference(self.__value__):
            return True
        else:
            raise ValueError('Was expecting a valid reference URI of the form /node/node with alphanumeric node names but got %s' % self.__value__)

    @classmethod
    def __converter__(cls):
        return str

    def __init__(self, *args, **kwargs):
        # TODO should validate that the ref actually exists
        self.__validators__ = [] # Ref doesn't have validation options
        super().__init__(*args, valuetype=str, **kwargs)

def load():
    return Ref