x = [1,2,3,4,5, [[61,7,8,9],
                 [62,7,8,9],
                 [63,7,8,9, 0, 0]
                 ]]

y = [1,2,3,4,5,6,7]
z = [1,2,3,4,5, [6,7,8]]

a = [1, 2, 3, 4, 5, [[61, 7, 8, 9],
                     [62, 7, 8, 9],
                     [63, 7, 8, 9, 0, [
                         [1,2,3],
                         [1,2,3],
                         [1,2,3]
                     ]]
                     ]]
def looper(iteritem, currentheight=1):
    height = currentheight
    width = 0

    print('len:',len(iteritem))
    if all(isinstance(f, list) for f in iteritem):
        height += len(iteritem)
        width += max([len(f) for f in iteritem])
    for i in iteritem:
        if not isinstance(i, list):
            width += 1
        elif isinstance(i, list):
            _tup = looper(i, currentheight=height)
            height = _tup[0]
            width += _tup[1]

    #height = max(1,height)
    return (height,width)

def recursive_len(item):
    if type(item) == list:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1

#print(looper(x))
#print(looper(y))
#print(looper(z))
print(looper(a))
print(recursive_len(a))

