
# --- static ---
__DYNAMIC_CLASS = 'dynamicclasses' # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins

def dynamicclass():
    return __DYNAMIC_CLASS

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerClass(className, classObj):
    #print(globals())
    if className in globals()[dynamicclass()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One class tried to overwrite an existing one. Class name: %s' % className)
    else:
        globals()[dynamicclass()][className] = classObj

        #print(dir(globals()[dynamicclass()][className]))
        globals()[dynamicclass()][className].register(className)
        """
        registerFileMatcher(
            globals()[dynamicclass()][className].classfile(),
            globals()[dynamicclass()][className]
        )
        """
        return True

def namespace():
    return globals()[dynamicclass()]


#--- initialize namespace
globals()[dynamicclass()] = dict()

