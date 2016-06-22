mypath = 'test\\test11data'
import os

"""
class Inode(object):
    def __init__(self, nodepath=None, nodename=None, parent=None):
        if nodepath is not None:
            rootdir = nodepath.rstrip(os.sep)
            #print('nodepath:', rootdir)
            self.path = nodepath
        else:
            self.path = None

        self.__nodename__ = nodename
        if isinstance(parent, Directory):
            self.__parent__ = parent
            self.__parent__.addchild(self)
        else:
            self.__parent__ = None
        self.__children__ = []

    @property
    def parent(self):
        return self.__parent__

    @property
    def name(self):
        return self.__nodename__

    def addparent(self, parent):
        self.__parent__ = parent

    def __repr__(self):
        if self.parent is None:
            return '%s' % (self.__nodename__)
        else:
            return '%s\\%s' % (self.__parent__.__repr__(), self.__nodename__)

    def __str__(self):
        return '%s' % self.__nodename__

class File(Inode):

    def read(self):
        if self.path is None:
            raise AttributeError('The file path was not provided when the File object was created')
        with open(self.path, mode='r') as f:
            print(f.read())
            f.close()

class Directory(Inode):

    def __init__(self, nodename=None, parent=None, nodepath=None):
        super().__init__(nodename=nodename, parent=parent, nodepath=nodepath)
        self.__children__ = []

    @property
    def children(self):
        return self.__children__

    def addchild(self, child):
        self.__children__.append(child)
        child.addparent(self)

    def __repr__(self):
        if self.parent is None:
            return '%s' % (self.__nodename__)
        else:
            return '%s\\%s' % (self.__parent__.__repr__(), self.__nodename__)

    def __str__(self):
        return '%s' % self.__nodename__

    def tree(self):
        #print(self.__str__())
        for child in self.children:
            print(child.__repr__())
            if isinstance(child, Directory):
                child.tree()

class Structure(object):
    @property
    def name(self):
        return self.__name__

    def __str__(self):
        return self.__name__

    def __repr__(self):
        return '%s: %s' % (type(self), self.__name__)

    @property
    def children(self):
        raise NotImplementedError('Please implement the children property method in a subclass of Structure')

class Container(Structure):

    def __init__(self, name=None):
        self.__name__ = name
        self.__nodes__ = []

    def addnodes(self, node):
        if isinstance(node, list):
            for _node in node:
                self.__nodes__.append(_node)
                _node.__parent__ = self
        else:
            self.__nodes__.append(node)
            node.__parent__ = self

    @property
    def nodes(self):
        return self.__nodes__

    @property
    def children(self):
        return self.__nodes__

class Node(Structure):

    def __init__(self, name=None, fileobjects=None):
        self.__name__ = name
        self.__inodes__ = fileobjects
        self.__parent__ = None

    @property
    def fileobjects(self):
        return self.__inodes__

    @property
    def children(self):
        return self.__inodes__
"""

class StructureFactory2(object):

    class Inode2(object):
        def __init__(self, nodepath=None, nodename=None, parent=None):
            if nodepath is not None:
                rootdir = nodepath.rstrip(os.sep)
                # print('nodepath:', rootdir)
                self.path = nodepath
            else:
                self.path = None

            self.__nodename__ = nodename
            if isinstance(parent, StructureFactory2.Directory):
                self.__parent__ = parent
                self.__parent__.addchild(self)
            else:
                self.__parent__ = None
            self.__children__ = []

        @property
        def parent(self):
            return self.__parent__

        @property
        def name(self):
            return self.__nodename__

        def addparent(self, parent):
            self.__parent__ = parent

        def __repr__(self):
            if self.parent is None:
                return '%s' % (self.__nodename__)
            else:
                return '%s\\%s' % (self.__parent__.__repr__(), self.__nodename__)

        def __str__(self):
            return '%s' % self.__nodename__

    class File(Inode2):

        def read(self):
            if self.path is None:
                raise AttributeError('The file path was not provided when the File object was created')
            with open(self.path, mode='r') as f:
                print(f.read())
                f.close()

    class Directory(Inode2):

        def __init__(self, nodename=None, parent=None, nodepath=None):
            super().__init__(nodename=nodename, parent=parent, nodepath=nodepath)
            self.__children__ = []

        @property
        def children(self):
            return self.__children__

        def addchild(self, child):
            self.__children__.append(child)
            child.addparent(self)

        def __repr__(self):
            if self.parent is None:
                return '%s' % (self.__nodename__)
            else:
                return '%s\\%s' % (self.__parent__.__repr__(), self.__nodename__)

        def __str__(self):
            return '%s' % self.__nodename__

        def tree(self):
            # print(self.__str__())
            for child in self.children:
                print(child.__repr__())
                if isinstance(child, StructureFactory2.Directory):
                    child.tree()

    class Node2(object):

        def __init__(self, name=None, fileobjects=None, parent=None):
            self.__name__ = name
            self.__inodes__ = fileobjects
            self.__parent__ = parent
            self.__children__ = []

        def addchildren(self, node):
            if isinstance(node, list):
                for _node in node:
                    self.__children.append(_node)
                    _node.__parent__ = self
            else:
                self.__children__.append(node)
                node.__parent__ = self

        @property
        def fileobjects(self):
            return self.__inodes__

        @property
        def children(self):
            return self.__children__

        @property
        def name(self):
            return self.__name__

        def __str__(self):
            return self.__name__

        def __repr__(self):
            return '%s: %s' % (type(self), self.__name__)

    @staticmethod
    def __treewalk__(root):
        inodes = os.listdir(root.path)
        for inode in inodes:
            fullpath = os.path.join(root.path, inode)
            if os.path.isfile(fullpath):
                _f = StructureFactory2.File(nodename=inode, nodepath=fullpath)  # parent=root,
                root.addchild(_f)
            elif os.path.isdir(fullpath):
                _d = StructureFactory2.Directory(nodename=inode, nodepath=fullpath)  # , parent=root
                root.addchild(_d)
                StructureFactory2.__treewalk__(_d)

    @staticmethod
    def __walk__(root):

        def recursivewalk(root):
            #TODO deal with multiple files in a dir and multiple dirs at the root
            if isinstance(root, StructureFactory2.Directory):
                if '_.txt' in [f.name for f in root.children]:
                    print('Node Container:', root.name)
                    return StructureFactory2.Node2(fileobjects=root.children, name=root.name)
                else:
                    print('Container:', root.name)
                    _ret = StructureFactory2.Node2(name=root.name)
                    for child in root.children:
                        _ret.addchildren(recursivewalk(child))
                    return _ret
            elif isinstance(root, StructureFactory2.File):
                print('Node:', root.name)
                return StructureFactory2.Node2(fileobjects=root, name=root.name)

        if not isinstance(root, StructureFactory2.Directory):
            raise TypeError('start of file system must be a directory')
        ret = StructureFactory2.Node2(name='*')
        ret.addchildren(recursivewalk(root))
        return ret

    # TODO make this the init call for the class so it can return a new node object with all data (more pythonic)
    @staticmethod
    def treewalk(rootpath):
        rootdir = rootpath.rstrip(os.sep)
        rootobj = StructureFactory2.Directory(nodename=rootdir, nodepath=rootpath)
        StructureFactory2.__treewalk__(rootobj) # TODO make this return an actual object
        return StructureFactory2.__walk__(rootobj)

"""
class StructureFactory(object):

    @staticmethod
    def walk(root):

        def recursivewalk(root):
            #TODO deal with multiple files in a dir and multiple dirs at the root
            if isinstance(root, Directory):
                if '_.txt' in [f.name for f in root.children]:
                    print('Node Container:', root.name)
                    return Node(fileobjects=root.children, name=root.name)
                else:
                    print('Container:', root.name)
                    _ret = Container(name=root.name)
                    for child in root.children:
                        _ret.addnodes(recursivewalk(child))
                    return _ret
            elif isinstance(root, File):
                print('Node:', root.name)
                return Node(fileobjects=root, name=root.name)

        if not isinstance(root, Directory):
            raise TypeError('start of file system must be a directory')
        ret = Container(name='*')
        ret.addnodes(recursivewalk(root))
        return ret

def treewalk(root):
    inodes = os.listdir(root.path)
    for inode in inodes:
        fullpath = os.path.join(root.path, inode)
        if os.path.isfile(fullpath):
            _f = File(nodename=inode, nodepath=fullpath) # parent=root,
            root.addchild(_f)
        elif os.path.isdir(fullpath):
            _d = Directory(nodename=inode, nodepath=fullpath) #, parent=root
            root.addchild(_d)
            treewalk(_d)
"""

"""
rootdir = mypath.rstrip(os.sep)
print(rootdir)
rootobj = Directory(nodename=rootdir, nodepath=mypath)
treewalk(rootobj)
rootobj.tree()
print(rootobj.children[0].children[0].parent.parent) #should display rootdir
print(rootobj.children[0].children[0].name) #should display testprop2
print(rootobj.children[0].children[0].path) #should display test\test11data\cr1\testprop2
print(rootobj.children[0])
"""
#sf = StructureFactory.walk(rootobj)
#sf2 = StructureFactory.walk(rootobj)

sf3 = StructureFactory2.treewalk(mypath)