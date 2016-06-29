from gtool.plugin import registerPlugin

def do_something_else():
    print('I am helping one')

class test1class():

    def do(self):
        print('I am helping one')

def register():
    registerPlugin('test1', test1class)

class plugin():

    def do(self):
        print('I am helping one')