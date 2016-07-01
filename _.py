def __init__(self):
    pass

def __repr__(self):
    if hasattr(self, 'x'):
        return "%s::%s" % (self.__class__, self.x)
    else:
        return "%s::%s" % (self.__class__, [])

class test(object):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.x = []

    def __repr__(self):
        if hasattr(self, 'x'):
            return "%s::%s" % (self.__class__, self.x)
        else:
            return "%s::%s" % (self.__class__, [])

typedict1 = {
    '__init__':__init__,
    '__repr__':__repr__,
    'x': []
}

typedict2 = {
    '__init__':__init__,
    '__repr__':__repr__,
    'x': []
}

classdict = {}

classdict['testx'] = type('testx', (object,), typedict1)
classdict['testy'] = type('testy', (object,), typedict2)


test1 = test()
test1.x.append(5)
test2 = test()
print(id(test1), "::", test1)
print(id(test2), "::", test2)

objectlist = []
testa = classdict['testx']()
objectlist.append(testa)
testb = classdict['testx']()
objectlist.append(testb)
testc = classdict['testy']()
objectlist.append(testc)
testd = classdict['testy']()
objectlist.append(testd)

testa.x.append(1)
testc.x.append(2)
print('-----')
print(id(testa) ,"::", testa)
print(id(testa) ,"::", testb)
print(id(testa) ,"::", testc)
print(id(testa) ,"::", testd)

print(testa)
print(testb)
print(testc)
print(testd)
