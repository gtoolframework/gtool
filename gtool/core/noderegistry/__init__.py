from gtool.core.utils.config import namespace
from collections import defaultdict
from gtool.core.utils.misc import striptoclassname

# --- statics ---

def nodeindex():
    __NODE_INDEX = '__objectindex'  # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins
    return __NODE_INDEX

def nodeindexreverse():
    __NODE_INDEX_REVERSE = '__objectindex_reversed'
    return __NODE_INDEX_REVERSE

def attribindex():
    __ATTRIB_INDEX = '__attribindex'
    return __ATTRIB_INDEX

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def convert(path):

    if '\\' in path:
        path = path.replace('\\', '/')
    if '//' in path:
        path = path.replace('//', '/')

    return path.lower()

def stripToUri(objectPath):
    if objectPath.endswith('.txt'):
        objectPath = objectPath[:-4]

    _dataroot = namespace().get('config', None).get('dataroot', '')
    if objectPath.startswith(_dataroot):
        objectPath = objectPath[len(_dataroot):]

    return objectPath

def registerObject(objectPath, obj):
    """
    if objectPath.endswith('.txt'):
        objectPath = objectPath[:-4]

    _dataroot = namespace().get('config', None).get('dataroot', '')
    if objectPath.startswith(_dataroot):
        objectPath = objectPath[len(_dataroot):]
    """

    objectPath = stripToUri(objectPath)

    if objectPath in nodenamespace(): # globals()[objectindex()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One node tried to overwrite an existing one. node name: %s' % objectPath)
    else:
        # store an object by URI
        nodenamespace()[convert(objectPath)] = obj
        # store all URI's by object
        _key = striptoclassname(type(obj)).lower()
        nodenamespacereverse()[_key].append(convert(objectPath))
        # store objects by attribute name
        for k, v in obj:
            if k.lower() not in attribnamespace():
                attribnamespace()[k.lower()].append(obj)
            else:
                _objlist = attribnamespace()[k.lower()]
                if obj not in _objlist:
                    attribnamespace()[k.lower()].append(obj)
        return True

# I want all the objects with a certain attribute
def searchByAttrib(attribname):
    return attribnamespace()[attribname.lower()]

# I want all the objects with a certain attribute but only of a certain type
def searchByAttribAndObjectType(attribname, objecttype):
    return [obj for obj in searchByAttrib(attribname) if striptoclassname(type(obj)).lower() == objecttype.lower()]

# return object at specific URI
def getObjectByUri(uri):
    return nodenamespace().get(convert(uri), None)

# return objects that match the URI fragment
def getObjectByUriElement(urielement):
    return [v for k, v in nodenamespace().items() if convert(urielement) in k]

# return objects that match the URI fragment only if they are of a specific type
def getObjectByUriElementAndType(urielement, objectype):
    return [obj for path, obj in nodenamespace().items() if convert(urielement) in path and striptoclassname(type(obj)).lower() == objectype.lower()]

def objectUri(obj):
    return convert(stripToUri(obj.__context__['file']))

# return Uris for a specific type
def getUrisByNodeType(nodetype):
    return nodenamespacereverse().get(nodetype.lower(), None)

# TODO implement object by parent
# TODO implement object by attribute value

def nodenamespace():
    # store an object by URI
    return globals()[nodeindex()]

def nodenamespacereverse():
    # stores all URI's by object
    return globals()[nodeindexreverse()]

def attribnamespace():
    # store objects by attribute name
    return globals()[attribindex()]

#--- initialize namespace
globals()[nodeindex()] = dict()
globals()[nodeindexreverse()] = defaultdict(list)
globals()[attribindex()] = defaultdict(list)