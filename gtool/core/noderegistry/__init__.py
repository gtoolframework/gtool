

# --- static ---
__OBJECT_INDEX = '__objectindex'  # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins

def objectindex():
    return __OBJECT_INDEX

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerObject(objectPath, obj):
    if objectPath in objectnamespace(): # globals()[objectindex()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One class tried to overwrite an existing one. Class name: %s' % objectPath)
    else:
        objectnamespace()[objectPath] = obj

        return True

def objectnamespace():
    return globals()[objectindex()]

#--- initialize namespace
globals()[objectindex()] = dict()
