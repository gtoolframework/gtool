import patricia as pt
import gtool.namespace

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
        print('file match:', T.key(exp), 'has a value of', T[T.key(exp)])
        return gtool.namespace.namespace()[T[T.key(exp)]]
    except KeyError:
        return None


#--- initialize namespace
globals()[filematcher()] = pt.trie('_')
