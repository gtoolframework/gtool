import gtool.utils.config as conf
import gtool.utils.classgen as gen
import gtool.types.common as t
from gtool.namespace import namespace, registerClass
from gtool.filewalker import filematch, filematchspace

# TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins

generatedClasses = [] # this should be a singleton Class/Object - http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
generatedClassesActual = []

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

def testCode3(k):
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

def test3():
    f = open('test\\test3.txt', 'r')
    testString = f.read()
    config = conf.readConfig(testString)
    # debug(config)
    classDict = conf.processConfigAlt(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode3(k)

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
    config = conf.readConfig(testString)
    # debug(config)
    classDict = conf.processConfigAlt(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode5(k)

def test6():
    def testCode6(k):
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
        """
        for k,v in x.testprop2.validators.items():
            print(k, "matches:", v == getattr(x.testprop2, k))
        print(x.testprop2.issingleton())
        print(x.testprop2)
        """
        try:
            x.testprop2.append(2)
        except Exception as err:
            print(err)
        print(x.testprop2)
        print('--- test 6 ends ---')

    f = open('test\\test6.txt', 'r')
    testString = f.read()
    config = conf.readConfig(testString)
    # debug(config)
    classDict = conf.processConfigAlt(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode6(k)

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
    config = conf.readConfig(testString)
    # debug(config)
    classDict = conf.processConfigAlt(config)
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
        """
        for k,v in x.testprop2.validators.items():
            print(k, "matches:", v == getattr(x.testprop2, k))
        print(x.testprop2.issingleton())
        print(x.testprop2)
        """
        try:
            x.testprop2.append(2)
        except Exception as err:
            print(err)
        print(x.testprop2)
        print('--- test 8 ends ---')

    f = open('test\\test8.txt', 'r')
    testString = f.read()
    config = conf.readConfig(testString)
    # debug(config)
    classDict = conf.processConfigAlt(config)
    for k, v in classDict.items():
        gen.generateClass(k, v)
        testCode8(k)

def debug(config):
    print('--- conf debug ---')
    conf.debugConfig(config)
    print('--- test ---')

if __name__ == '__main__':
    test8()

# TODO === FEATURE #1 === read config, parse file and emit dict object containing tree structure/data
# TODO switch classgen lists to lists of repeating objects
# TODO class metas to set/override key functions during class gen
# TODO read multiple args from child data files
# TODO multiple args in data file
# TODO regex for class to recognize files that match. Criteria Class --> criteria.txt, Control Class --> c#.txt
# TODO mandatory/optional flag for attributes (in keyword args)
# TODO automated reader from file
# TODO decide when related files should be in same directory and when in subdir
# TODO should first line of data file be class type? or is that extra work?
# TODO special keyword to identify subfile (or behaviour to go looking for subfiles/subdirs
# TODO chained file reader
# TODO dynamic class imports
# TODO method/plugin imports
# TODO optional/required for class models


# TODO === FEATURE #1.1 === cleanup
# TODO config generates a dict and then classgen parses and generates another dict - can I simplify?
# TODO review all inline code TODOs
# TODO replace classgen's methodbinder with a registration decorator that takes the name of the func it should be bound to
# TODO context for error messages (pseudo stack tracing)
# TODO args for classes (set behaviour) --> pass parser for args in CoreType --> implement better args parser
# TODO make config (pyparsing return properly structured dict
# TODO unified error message library and useful error reporting
# TODO testing framework


# TODO === FEATURE #2.0 === structured data extraction
# TODO file reader that reads a specific file from a specific location
# http://stackoverflow.com/questions/122277/how-do-you-translate-this-regular-expression-idiom-from-perl-into-python
# TODO file structure walker


# TODO === FEATURE #2.1 === core refinements
# TODO multi-type attributes e.g. Number | String | Choice
# TODO decimal or float type for number (not int)
# TODO generic validator that handles both types and choices
# TODO safe and human parser ---> C(Alpha[0:3]).txt <-- between brackets is an expression matching CA.txt C.txt CABA.txt
# TODO enhance safe and human parser with a tokenizer - C|(Alpha[0:3])|.txt --> | separates tokens
# TODO use safe regexer for reading file matcher
# TODO piping - populate attributes automatically with outputs of certain methods. E.G. attrname: single: string: #ID --> queries .id() for a value during .__init__()
# TODO use safe regexer for piping E.G. attrname: single: string: #pipe(#filematcher(C|(Alpha[0:3])|.txt): 1,2) - C|(Alpha[0:3])|.txt --> | separates tokens
# TODO Inheritance for user defined models CLASSNAME::(PARENTCLASS)

# TODO === FEATURE #3 === basic reporting
# TODO basic reporting module (CSV output)
# TODO basic reporting module (Word output)


# TODO === FEATURE #4 === automation core
# TODO evidence file / generic file handler
# TODO simple transforms
# TODO pipe transforms into reporting
# TODO graph reporting (node diagram)
# TODO graph reporting (dashboard)

# TODO === FEATURE #5 === automation core
# TODO event queue
# TODO event subscription
# TODO headless web browser
# TODO wget
# TODO file system copier
# TODO SFTP / SCP copier
# TODO generic job framework

# TODO === FEATURE #6 ===
# TODO untangle classgen and make it more object oriented for easier future maintenance (objects that contain their own parsers, validators etc...)

