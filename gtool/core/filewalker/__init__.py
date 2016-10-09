import os

import patricia as pt

import gtool.core.namespace
from functools import lru_cache

# --- static ---
__DYNAMIC_CLASS = 'filematches'

def filematcher():
    return __DYNAMIC_CLASS

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerFileMatcher(fileExp, classObj):
    if fileExp in globals()[filematcher()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One class tried to overwrite the file registration of an existing one. Class name: %s' % classObj)
    else:
        globals()[filematcher()][fileExp] = classObj
        return True

def filematchspace():
    return globals()[filematcher()]

def filematch(exp):
    T = globals()[filematcher()]
    try:
        return gtool.core.namespace.namespace()[T[T.key(exp)]]
    except KeyError:
        return None

#--- classes ---

def striptoclassname(fullclassstring):
    return '{0}'.format(fullclassstring)[7:-2].split('.')[-1]

class StructureFactory(object):

    class Inode(object):
        def __init__(self, nodepath=None, nodename=None, parent=None):
            if nodepath is not None:
                rootdir = nodepath.rstrip(os.sep)
                # print('nodepath:', rootdir)
                self.path = nodepath
            else:
                self.path = None

            self.__nodename__ = nodename
            if isinstance(parent, StructureFactory.Directory):
                self.__parent__ = parent
                self.__parent__.addchild(self)
            else:
                self.__parent__ = None
            #self.__children__ = []

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
                _ret = f.readlines()
                f.close()
            return _ret


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
            # print(self.__str__())
            for child in self.children:
                print(child.__repr__())
                if isinstance(child, StructureFactory.Directory):
                    child.tree()

    class Node(object):

        def __init__(self, name=None, fileobject=None, parent=None, flattened=False):
            # TODO consolidate fileobjects and children
            # TODO implement logic for flattened mode (not sure it's needed)
            self.__name__ = name
            self.__inode__ = fileobject
            self.__parent__ = parent
            self.__children__ = []
            self.__flattened__ = flattened

        def addchildren(self, node):
            if isinstance(node, list):
                for _node in node:
                    self.__children__.append(_node)
                    _node.__parent__ = self
            else:
                self.__children__.append(node)
                node.__parent__ = self

        @property
        def fileobject(self):
            return self.__inode__

        @property
        def path(self):
            if self.__inode__ is not None:
                return self.__inode__.path
            else:
                return None

        @property
        def children(self):
            return self.__children__

        @property
        def haschildren(self):
            if len(self.__children__) > 0:
                return True
            else:
                return False

        @property
        def name(self):
            return self.__name__

        @property
        def parent(self):
            return self.__parent__

        def __str__(self):
            # TODO return number of children and type (file or dir)
            return self.__name__

        def __repr__(self):
            return '%s: %s' % (type(self), self.__name__)

        @property
        def uri(self):
            if self.__parent__ is not None:
                return  "%s\%s" % (self.__parent__.uri, self.__name__)
            else:
                return "%s" % self.__name__

        def __objectmatch__(self):
            _ret = filematch(self.name)
            if _ret is None:
                raise KeyError('%s at %s does not match any known class definition' % (self.name, self.path))
            return _ret

        @property
        def __data__(self):
            if isinstance(self.__inode__, StructureFactory.File):
                return ''.join(self.__inode__.read())
            else:
                raise TypeError('%s is not a file' % self.__inode__.path)

        @property
        def dataasobject(self):
            _retclass = self.__objectmatch__()
            _retobject = _retclass()
            context = {'file': self.path,
                       'parent': self.parent,
                       'class': self.name} #also set in core.DynamicObject.load and CNode below
            if _retobject.loads(self.__data__, context=context): # True if loadstring works
                return _retobject
            else:
                raise TypeError('Could not parse the data from %s into a %s class' % (self.path, type(_retobject)))

        def treestructure(self):
            if self.__parent__ is None:
                _currentnode = '*'
            elif self.__parent__ is not None and isinstance(self, StructureFactory.Container):
                _currentnode = 'container directory' #can't use self.name
            else:
                _currentnode = striptoclassname(self.__objectmatch__()) # if self.__parent__ is not None else '*'

            if len(self.children) == 0:
                return _currentnode
            else:
                return {_currentnode: [f.treestructure() for f in self.children]} # ret objectmatch?


    class Container(Node):

        """
        An inherited class for the purposes of type differentiaton and overriding the data methods
        """

        @property
        def dataasobject(self):
            # TODO is this right?
            return [child.dataasobject for child in self.children]

        @property
        def __data__(self):
            return '%s' % self.__name__

    class CNode(Node):

        """
        An inherited class for the purposes of type differentiaton and overriding the data methods
        """

        @property
        def __data__(self):
            """
            returns a string of the root node data but not of any attributes that are dynamic classes
            :return: str
            """
            _ret = str()
            _filelist = [f for f in self.fileobject.children if isinstance(f, StructureFactory.File)]
            # iterate to find the core file --> _.txt
            # TODO does not need to be a for loop - can just check if it exists
            _coredata = [f for f in _filelist if f.name == "_.txt"]
            if len(_coredata) == 1:
                _ret += ''.join(_coredata[0].read())
            else:
                raise FileNotFoundError('In %s the _.txt file was expected' % self.fileobject.path)

            # iterate files that contain a single attribute value
            for _file in (f for f in _filelist if f.name != "_.txt"):
                _data = ''.join(_file.read())
                if '@' not in _data[0]:
                    _ret += '\n@%s: ' % _file.name.split('.')[:-1][0]
                    _ret += _data
                #TODO find a way to reinstate this code block below (possibly move it into dataasobject)
                """
                else:
                    # standalone attribute files should just contain data
                    raise TypeError('Found an attribute declaration in %s but was not expecting one' % _file.path)
                """

            for subdir in (f for f in self.fileobject.children if isinstance(f, StructureFactory.Directory)):
                subfilelist = [subfile for subfile in subdir.children if isinstance(subfile, StructureFactory.File)]

                if '_.txt' not in (subfile.name for subfile in subfilelist) and any('@' not in subfile.read()[0] for subfile in subfilelist):
                    for subfile in subfilelist:
                        _data = ''.join(subfile.read())
                        #if '@' not in _data[0]: #implemented above in the 'any' condition
                        _ret += '\n@%s: ' % subdir.name
                        if not len(_data) > 0:
                            raise TypeError('The file %s has no data in it' % subfile.path)
                        _ret += _data

            return _ret

        def treestructure(self):
            #TODO make this recursive
            # TODO this would not be required in files inside cnode were turned into nodes

            def __treestructure__(obj=None , currentnode=None, dynamics=None):

                _children = []
                _missingoptional = obj.missingoptionalproperties  # we don't check missing mandatory properties because dataasobject would have thrown an error already

                for dynamicproperty in obj.dynamicproperties:
                    if dynamicproperty not in _missingoptional:
                        _prop = obj.__list_slots__[dynamicproperty].__lazyloadclass__()
                        if _prop in dynamics:
                            _obj = getattr(obj, dynamicproperty)
                            if _obj is not None:
                                for attribute in _obj:
                                    _children.append(__treestructure__(currentnode=striptoclassname(_prop),
                                                                        obj=attribute,
                                                                        dynamics=dynamics))


                return {currentnode: _children} if len(_children) > 0 else currentnode

            return __treestructure__(obj=self.dataasobject,
                                     currentnode=super().treestructure(),
                                     dynamics=list(gtool.core.namespace.namespace().values())
                                     )

        @property
        @lru_cache() # caches results for when .treestructure calls
        def dataasobject(self):
            _retclass = self.__objectmatch__()
            _retobject = _retclass()
            _softload = True
            # --- object initialization ---
            context = {'file': self.path,
                       'parent': self.__parent__,
                       'class': self.name}  # also set in core.DynamicObject.load and Node aboce
            if not _retobject.loads(self.__data__, softload=_softload, context=context) and len(self.__data__) > 0:
                # True if loadstring works but can only be false if self.__data__ has some content
                # TODO .loads should return true if it functioned correctly, even if self.__data__ is empty
                raise TypeError('Could not parse the data from %s into a %s class' % (self.path, type(_retobject)))
            if len(_retobject.missingproperties) == 0 and len(_retobject.missingoptionalproperties) == 0:
                return _retobject

            # --- load missing elements from subfiles if needed
            _filelist = [f for f in self.fileobject.children if isinstance(f, StructureFactory.File)]

            # TODO lots of spaghetti code in here, cleanup up and consolidate (Carefully)
            for _file in (f for f in _filelist if f.name != "_.txt"): # "_.txt" is already loadeded via self.__data__
                _data = ''.join(_file.read())
                if '@' in _data[0]:
                    # this is an attribute class object (not a common object)
                    _filenamewithoutext = _file.name.split('.')[:-1][0]
                    _attrclassobj = getattr(_retobject, _filenamewithoutext)

                    _attrclassname = _attrclassobj.attrfilematch
                    _attrobj = StructureFactory.Node(name=_attrclassname, fileobject=_file)
                    #setattr(_retobject, _filenamewithoutext, _attrobj.dataasobject)
                    getattr(_retobject, _filenamewithoutext).append(_attrobj.dataasobject)

                    if _filenamewithoutext in _retobject.missingproperties:
                        _retobject.__missing_mandatory_properties__.remove(_filenamewithoutext)
                    elif _filenamewithoutext in _retobject.missingoptionalproperties:
                        _retobject.__missing_optional_properties__.remove(_filenamewithoutext)
                    else:
                        raise TypeError('Got an attribute file %s that is not part of the %s class at %s' %
                                         (_file.name, self.name, self.path))

            # --- load missing elements from subdirs if needed (which are ignored by .__data__
            for subdir in (f for f in self.fileobject.children if isinstance(f, StructureFactory.Directory)):
                subfilelist = [subfile for subfile in subdir.children]
                #print('subfilelist:', subfilelist)

                # handles subdirectories with root file
                if '_.txt' in (subfile.name for subfile in subfilelist):
                    """
                    for subfile in subfilelist:
                        objectname = getattr(_retobject, subfile.parent.name).attrtype.classfile()
                        #TODO add conditions to check if directory has a _.txt ala condition1, condition2 above
                        if any(os.path.isdir(os.path.join(subdir.path, f)) for f in os.listdir(subdir.path)):
                            _attrobj = StructureFactory.CNode(name=objectname, fileobject=subfile)
                        else:
                            _attrobj = StructureFactory.Node(name=objectname, fileobject=subfile)
                        try:
                            getattr(_retobject, subfile.parent.name).append(_attrobj.dataasobject)
                            #_retobject[subfile.parent.name] = _attrobj.dataasobject #this will implicitly recurse if there are nested dynamic objects
                        except Exception as err:
                            raise Exception('While processing ', subfile.parent.name, 'the following error occured:', err)
                    """
                    objectname = getattr(_retobject, subdir.name).attrtype.classfile()
                    # TODO add conditions to check if directory has a _.txt ala condition1, condition2 above
                    #if any(os.path.isdir(os.path.join(subdir.path, f)) for f in os.listdir(subdir.path)):
                    _attrobj = StructureFactory.CNode(name=objectname, fileobject=subdir)
                    """
                    else:
                        _attrobj = StructureFactory.Node(name=objectname, fileobject=subdir)
                    """
                    try:
                        getattr(_retobject, subdir.name).append(_attrobj.dataasobject)
                        # _retobject[subfile.parent.name] = _attrobj.dataasobject #this will implicitly recurse if there are nested dynamic objects
                    except Exception as err:
                        raise Exception('While processing ', subdir.name, 'the following error occured:', err)
                    #------
                    _objectname = subdir.name #subfile.parent.name
                    if _objectname in _retobject.missingproperties:
                        _retobject.__missing_mandatory_properties__.remove(_objectname)
                    elif _objectname in _retobject.missingoptionalproperties:
                        _retobject.__missing_optional_properties__.remove(_objectname)
                    else:
                        raise TypeError('Got an attribute directory %s that is not part of the %s class at %s' %
                                        (_objectname, type(_retobject), self.path))

                # handles subdirectories without a root file

                else: #if any('@' in subfile.read()[0] for subfile in subfilelist if isinstance(subfile, StructureFactory.File)):
                    objectsInFiles = any('@' in subfile.read()[0] for subfile in subfilelist if
                        isinstance(subfile, StructureFactory.File))
                    objectsInDirectories = all(isinstance(subfile, StructureFactory.Directory) for subfile in subfilelist)
                    # TODO True and True probably should not happen - make a check
                    #print("objectsInDirectories:", objectsInDirectories)
                    #print("objectsInFiles:", objectsInFiles)
                    if objectsInFiles or objectsInDirectories:
                        for subfile in subfilelist:
                            objectname = getattr(_retobject, subfile.parent.name).attrtype.classfile()
                            if any(os.path.isdir(os.path.join(subdir.path, f)) for f in os.listdir(subdir.path)):
                                _attrobj = StructureFactory.CNode(name=objectname, fileobject=subfile)
                            else:
                                _attrobj = StructureFactory.Node(name=objectname, fileobject=subfile)
                            try:
                                getattr(_retobject, subfile.parent.name).append(_attrobj.dataasobject)
                            except Exception as err:
                                raise Exception('While processing ', subfile.parent.name, 'the following error occured:',
                                                err)
                        if subfile.parent.name in _retobject.missingproperties:
                            _retobject.__missing_mandatory_properties__.remove(subfile.parent.name)
                        elif subfile.parent.name in _retobject.missingoptionalproperties:
                            _retobject.__missing_optional_properties__.remove(subfile.parent.name)
                        else:
                            raise TypeError('Got an attribute directory %s that is not part of the %s class at %s' %
                                            (subfile.parent.name, type(_retobject), self.path))

            if len(_retobject.missingproperties) > 0:
                raise TypeError('The following mandatory attributes are missing %s for the %s class at %s' %
                                (_retobject.missingproperties, type(_retobject), self.path))

            return _retobject

        def dataaslist(self, returnmatrix):
            #returnmatrix is updated by reference, don't need to return it
            #implement in node and container too
            return True


    @staticmethod
    def __treewalk__(root):
        inodes = os.listdir(root.path)
        for inode in inodes:
            if not inode.startswith('!'):
                fullpath = os.path.join(root.path, inode)
                if os.path.isfile(fullpath):
                    _f = StructureFactory.File(nodename=inode, nodepath=fullpath)  # parent=root,
                    root.addchild(_f)
                elif os.path.isdir(fullpath):
                    _d = StructureFactory.Directory(nodename=inode, nodepath=fullpath)  # , parent=root
                    root.addchild(_d)
                    StructureFactory.__treewalk__(_d)

    @staticmethod
    def __walk__(location=None):

        def recursivewalk(location=None, isroot=False):
            #TODO deal with multiple files in a dir and multiple dirs at the root
            if isinstance(location, StructureFactory.Directory):
                if '_.txt' in [f.name for f in location.children]:
                    return StructureFactory.CNode(fileobject=location, name=location.name)
                else:
                    # special handler for root of structure
                    _locationname = location.name if isroot is False else '*'
                    _ret = StructureFactory.Container(name=_locationname, fileobject=location)
                    for child in location.children:
                        _ret.addchildren(recursivewalk(location=child))
                    return _ret
            elif isinstance(location, StructureFactory.File):
                _rootname = location.name.split('.')[0]
                return StructureFactory.Node(fileobject=location, name=_rootname)

        if not isinstance(location, StructureFactory.Directory):
            raise TypeError('start of file system must be a directory')

        return recursivewalk(location=location, isroot=True)

    # TODO make this the init call for the class so it can return a new node object with all data (more pythonic)
    @staticmethod
    def treewalk(rootpath):
        # TODO check this is a valid directory before proceeding
        rootdir = rootpath.rstrip(os.sep)
        rootobj = StructureFactory.Directory(nodename=rootdir, nodepath=rootpath)
        StructureFactory.__treewalk__(rootobj) # TODO make this return an actual object
        return StructureFactory.__walk__(location=rootobj)

#--- initialize namespace
globals()[filematcher()] = pt.trie('_')
