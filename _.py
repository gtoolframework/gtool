def test():
    a = [1,2,3,4]
    b = [5,6,7,8]
    for i in a:
        yield i
    for i in b:
        yield i

for i in test():
    print(i)