# --- static ---
__NAMESPACE = 'runtimeoptions' # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins

def namespacename():
    return __NAMESPACE

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerruntimeoption(optionname, optionvalue):
    #print(globals())
    if optionname in globals()[namespacename()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One option name tried to overwrite an existing one. Option name: %s' % optionname)
    else:
        globals()[namespacename()][optionname] = optionvalue


        return True

def runtimenamespace():
    return globals()[namespacename()]

#--- initialize namespace
globals()[namespacename()] = dict()

