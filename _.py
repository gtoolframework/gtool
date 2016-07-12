from gtool.core.types.matrix import Matrix

m = Matrix(startwidth=4, startheight=4)

for x in m.data():
    print(x)

print(m.vertical_utilization())

print(m.horitzontal_utlization())

print(m.cursor)

m.insert(cursor=(0,2), datamatrix=[1,2,3,4,5,6])

for x in m.data():
    print(x)

