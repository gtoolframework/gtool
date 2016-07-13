from gtool.core.types.matrix import Matrix

m = Matrix(startwidth=10, startheight=2)

for x in m.data():
    print(x)

print(m.__v_utilization__())

print(m.__h_utlization__())

print(m.cursor)

m.insert(cursor=(2,1), datalist=['x'] * 20)

for x in m.data():
    print('len:', len(x), '-->', x)

m.bulk_insert(cursor=(2,2), rows = [['y'] * 10] * 3)

for x in m.data():
    print('len:', len(x), '-->', x)

print(m.__v_utilization__())

print(m.__h_utlization__())