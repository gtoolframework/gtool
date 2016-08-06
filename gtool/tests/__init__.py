import gtool.core.utils.classprocessor as conf
#import gtool.utils.classgen as gen
#import gtool.types.common as t
#from gtool.types.attributes import attribute
#from gtool.namespace import namespace, registerClass
#from gtool.filewalker import filematch, filematchspace, StructureFactory
from gtool.core.utils import projectloader


def debug(config):
    print('--- conf debug ---')
    conf.debugClass(config)
    print('--- test ---')


"""
def testCode1(k):
    print('test 1 checks it object magic methods works')
    print('---- testing 1 begins ----')
    x = globals()[k]()
    print(x.__list_slots__)
    x.testprop1 = 'hello'
    print(x.testprop1)
    x.testprop1 = 'world'
    print(x.testprop1)
    x.testprop1 = 'remove this'
    print(x.testprop1)
    x.testprop1 = 'remove'
    print(x.testprop1)
    print("----------")
    x.testprop1 += ['this']
    print(x.testprop1)
    print(x.dynamicproperties())

def testCode2():
    print('test 2 further checks it object magic methods works')
    print('--- test  2 starts ---')
    print('--- number ---')
    x = t.Number()
    y = t.Number()
    y.append(9)
    print(x.listtype)
    print(x)
    x.append(1)
    x += y
    print(x)
    print(type(x))
    z = t.Number()
    print(type(z))
    z.append(3)
    z.append(4)
    c = z + x
    print(c)
    print(type(c))
    print('--- string ---')
    h = t.String()
    print(h.listtype)
    print(h)
    h.append('1')
    try:
        # this should file
        h += ['str', 'str2']
    except Exception as err:
        print(err)
    i = t.String()
    i.append('2')
    i.extend(['3','4'])
    h += i
    print(h)
    print('--- test ends ---')

def testcode4():
    print('test 4 checks it basic object creation works')
    x = t.Number([1,2,3])
    print(len(x))
    y = t.Number()
    print(y)

def test3():
    def testCode(k):
        print('test 3 is an earlier alternative of test 6')
        print('---- testing 3 begins ----')
        print('--- test prop 1 ---')
        dClass = namespace()[k]
        x = dClass(
            testprop1=['test0', 'test1'],
            testprop2=t.Number([9], singleton=True, min=0, max=9)
        )
        # property already exists
        x.testprop1.append('test2')
        try:
            # this should file
            x.testprop1.append(1)
        except Exception as err:
            print(err)
        x.testprop1.append('test3')
        x.testprop1.append('test4')
        print(x.testprop1)
        print('--- test prop 2 ---')
        print(x.testprop2.issingleton())
        print(x.testprop2)
        try:
            x.testprop2.append(2)
        except Exception as err:
            print(err)
        print(x.testprop2)
        print('--- test prop 4 ---')
        print(x.testprop4)
        try:
            x.testprop4.append(9)
        except ValueError:
            print("tried to add a value greater than %s" % x.testprop4.max)
        x.testprop4.append(7)
        print(x.testprop4)

        print(x)
        print('--- test 3 ends ---')

    f = open('test\\test3.txt', 'r')
    testString = f.read()
    config = conf.readClass(testString)
    # debug(config)
    classDict = conf.processClass(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode(k)

def testCode5(k):
    print('test 5 will check if data loading works correctly')
    print('---- testing 5 begins ----')
    testFile = 'test\\testdata5.txt'

    dClass = namespace()[k]
    x = dClass()
    print('--- test data loaded ---')
    x.load(testFile)
    print(x)
    print('--- test 5 ends ---')

def test5():
    f = open('test\\test5.txt', 'r')
    testString = f.read()
    config = conf.readClass(testString)
    # debug(config)
    classDict = conf.processClass(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode5(k)

# use tests 6+

def test6():
    def testCode(k):
        print(
            'test 6 will determine if validation works properly and also includes first introduction of metas in conf')
        print('---- testing 6 begins ----')
        print('--- test prop 1 ---')
        dClass = namespace()[k]
        x = dClass(
            testprop2=t.Number([8], singleton=True, max=8),
            testprop1=['test0', 'test1']
        )
        print('maxlength:', x.testprop1.maxlength)
        # property already exists
        x.testprop1.append('test2')
        try:
            # this should fail
            x.testprop1.append(1)
        except Exception as err:
            print(err)
        x.testprop1.append('test3')
        try:
            x.testprop1.append('test4aa')
        except ValueError:
            print('attempted to add a value that was longer than permitted')
        print(x.testprop1)
        print('--- test prop 2 ---')
        try:
            x.testprop2.append(2)
        except Exception as err:
            print(err)
        print(x.testprop2)
        print('--- test 6 ends ---')

    f = open('test\\test6.txt', 'r')
    testString = f.read()
    config = conf.readClass(testString)
    # debug(config)
    classDict = conf.processClass(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode(k)

def test7():

    def testCode7(k):
        dClass = namespace()[k]
        x = dClass(
            testprop1=[1, 2, 3, 4]
        )
        print(x.metas)
        print(x.classfile)
        print(filematchspace())

    print('test 7 verifies metas in conf')
    print('---- testing 7 begins ----')
    f = open('test\\test7.txt', 'r')
    testString = f.read()
    config = conf.readClass(testString)
    # debug(config)
    classDict = conf.processClass(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        #registerClass(k, classObject)
        # testCode7(k)
    #print('given \'criteria\' I match for:', filematch('criteria'))
    #print('given \'cr1\' I match for:', filematch('cr1'))

    #print('namespace:', namespace())
    print('--- walk file system ---')
    mypath = 'test\\test7data'
    from os import listdir
    from os.path import isfile, join
    print('filematch space:', filematchspace())
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for filename in onlyfiles:
        print('\n*** file: ', filename, ' processing start ***')
        fname = filename.split('.')[0]
        #print('inside for loop:', namespace())
        _class = filematch(fname)
        if _class is not None:
            d = _class()
            d.load(mypath + '\\' + filename)
            print(d)
    print('--- test 7 ends ---')

def test8():
    def testCode8(k):
        print(
            'test 8 will determine if the new format of multiple (non-singletons) attribs as members of a list works')
        print('---- testing 8 begins ----')
        print('--- test prop 1 ---')
        dClass = namespace()[k]
        x = dClass(
            testprop2=t.Number([8], singleton=True, max=8),
        )
        print(x.testprop2)
        print('--- test 8 ends ---')

    f = open('test\\test8.txt', 'r')
    testString = f.read()
    config = conf.readClass(testString)
    # debug(config)
    classDict = conf.processClass(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode8(k)

def test9():
    print('test 9 checks if basic type creation works with the new attribute structure')
    x = t.Number(9)
    y = t.Number(4)
    print(x)
    print('attribute object test')
    a = attribute(typeclass=t.Number,
                  singleton=True,
                  parent='Parent1',
                  attributename='testprop1',
                  kwargs={'max':8}
                  )
    try:
        a.__load__(x) # should raise an Error
    except Exception as err:
        print(err)
    try:
        a.__load__([y,y]) # should raise an Error
    except Exception as err:
        print(err)
    a.__load__(y) # should work

    print(a)
    b = attribute(typeclass=t.Number,
                  singleton=False,
                  parent='Parent1',
                  attributename='testprop1',
                  kwargs={'max':10}
                  )
    b.__load__([x,y]) # should work
    print(b)

def test10():
    def testCode(k):
        print(
            'test 10 will determine if validation works properly as well as classgen with new attribute structure')
        print('---- testing 10 begins ----')
        print('should work...')
        dClass = namespace()[k]
        x = dClass(
            testprop1=t.Number(9),
            testprop2=[t.Number(8),t.Number(1)],
        )
        print(x)

        print('\nshould throw an error...')
        try:
            y = dClass(
                testprop1=t.Number(11),
                testprop2=[t.Number(8), t.Number(1)],
            )
            print(y)
        except Exception as err:
            print('...it did')
            print('got the following error message:', err)
        print('--- test 10 ends ---')

    f = open('test\\test10.txt', 'r')
    testString = f.read()
    config = conf.readClass(testString)
    # debug(config)
    classDict = conf.processClass(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode(k)

def test11():

    print('test 11 loads data that contains multiples in the property field')
    print('---- testing 11 begins ----')
    f = open('test\\test11.txt', 'r')
    testString = f.read()
    config = conf.readClass(testString)
    # debug(config)
    classDict = conf.processClass(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        #registerClass(k, classObject)
        # testCode7(k)
    #print('given \'criteria\' I match for:', filematch('criteria'))
    #print('given \'cr1\' I match for:', filematch('cr1'))

    #print('namespace:', namespace())
    print('--- walk file system ---')
    mypath = 'test\\test11data'
    from os import listdir
    from os.path import isfile, join
    print('filematch space:', filematchspace())
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for filename in onlyfiles:
        print('\n*** file: ', filename, ' processing start ***')
        fname = filename.split('.')[0]
        #print('inside for loop:', namespace())
        _class = filematch(fname)
        if _class is not None:
            d = _class()
            d.load(mypath + '\\' + filename)
            print(d)
    print('--- test 11 ends ---')

def test12():

    print('test 12 validates auto loading from simple files, multi item data loads and new required arg')
    print('---- testing 12 begins ----')
    __loadclasses('test\\test12.txt', dbg=False)

    print('--- walk file system ---')
    mypath = 'test\\test12data'
    sf3 = StructureFactory.treewalk(mypath)

    print('--- explore results ---')
    for child in sf3.children:
        print(child.dataasobject)

    print('--- test 12 ends ---')

def test13():

    print('test 13 validates auto loading from complex folder structures')
    print('---- testing 13 begins ----')
    __loadclasses('test\\test13.txt', dbg=False)

    print('--- walk file system ---')
    mypath = 'test\\test13data'
    sf3 = StructureFactory.treewalk(mypath)

    print('--- explore results ---')
    for child in sf3.children:
        print(child.dataasobject)

    print('--- test 13 ends ---')

def test14():

    print('test 14 validates chained config and chained data reading')
    print('---- testing 14 begins ----')
    __loadclasses('test\\test14.txt', dbg=False)

    print('--- walk file system ---')
    mypath = 'test\\test14data'
    sf = StructureFactory.treewalk(mypath)

    print('--- explore results ---')
    for child in sf.children:
        print(child.dataasobject)

    print('--- test 14 ends ---')
"""

#--- old tests pre 15 won't work without refactoring to use new project structure

def test15():

    print('test 15 validates loading multiple class files from a predefined directory and the new plugin loader')
    print('---- testing 15 begins ----')
    sf = projectloader('test\\test15', dbg=False)

    print('--- explore results ---')
    for child in sf.children:
        print('-----')
        print(child.dataasobject)

    print('--- test 15 ends ---')

def test16():

    print('test 16 common type plugins')
    print('---- testing 16 begins ----')
    sf = projectloader('test\\test16', dbg=False)

    print('--- explore results ---')
    for child in sf.children:
        print('-----')
        print(child.dataasobject)

    print('--- test 16 ends ---')

def test17():
    outputscheme = 'output1'
    print('test 17 validates output format strings and config works')
    print('---- testing 17 begins ----')

    sf = projectloader('test\\test17', dbg=False)

    print('--- explore results ---')
    for child in sf.children:
        #print(child)

        _x = child.dataasobject
        print(_x.output(outputscheme=outputscheme))

    print('--- test 17 ends ---')

def test18sub1():
    print('test 18sub1 validates the matrix class works')
    print('---- testing 18sub1 begins ----')
    from gtool.core.types.matrix import Matrix

    m = Matrix(startwidth=10, startheight=2)

    for x in m:
        print(x)

    print(m.__v_utilization__())

    print(m.__h_utilization__())

    print(m.cursor)

    m.insert(cursor=(2, 1), datalist=['x'] * 20)

    for x in m:
        print('len:', len(x), '-->', x)

    m.bulk_insert(cursor=(2, 2), rows=[['y'] * 10] * 3)

    m.trim()

    print('m v util:',m.__v_utilization__())

    print('m h util:',m.__h_utilization__())

    print('m cursor:',m.cursor)

    for x in m:
        print('len:', len(x), '-->', x)

    print('column 3:', m.col(3))
    mmap = m.__matrixmap__()
    print('*' * 20)
    for x in mmap:
        print(x)

    print('mmap v util:', mmap.__v_utilization__())

    print('mmap h util:', mmap.__h_utilization__())

    print('mmap cursor:',mmap.cursor)

    for x in mmap:
        print('len:', len(x), '-->', x)
    print('--- test 18sub1 ends ---')


def test18():

    def flatten(exp):

        def sub(exp, res):
            if type(exp) == dict:
                for k, v in exp.items():
                    yield from sub(v, res + [k])
            elif type(exp) == list:
                for v in exp:
                    yield from sub(v, res)
            else:
                yield "/".join(res + [exp])

        yield from sub(exp, [])


    outputscheme = 'output1'
    print('test 18 validates list generation works and excel/word outputs work')
    print('---- testing 18 begins ----')

    sf = projectloader('test\\test18', dbg=False, outputscheme=outputscheme)

    #print(sf.treestructure())

    s = set()

    for i in sorted(flatten(sf.treestructure())):
        #print(i)
        s.add(i)

    print(s)

    print('--- explore results ---')
    for child in sf.children:
        print(child)

        print(child.treestructure())
        #_x = child.dataasobject
        #print(_x.output(outputscheme=outputscheme))

    print('--- test 18 ends ---')