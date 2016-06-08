import copy


def init(self):
    print('in init')
    #self.a = copy.copy(self.a)
    self.a = self.a

class Factory(object):

    init2 = init

    @staticmethod
    def generate(classname, xvar):
        return type(classname,(object,),{'a':xvar, '__init__': Factory.init2})


list1 = [1,2,3,4]
a = Factory.generate('one', list1)
b = Factory.generate('two', list1)
print(a.a)
print(b.a)
a.a[2] = 9
print(a.a)
print(b.a)
objA = a()
objB = b()
print(objA.a)
print(objB.a)
objA.a[2] = 7
print(objB.a)