import configparser

# --- static ---

def namespacename():
    __NAME__ = '__CONFIG__'  # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins
    return __NAME__

def regtype():
    __TYPE__ = 'config sections'
    return __TYPE__

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def register(regname, regobject):
    #print(globals())
    if regname in globals()[namespacename()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One %s tried to overwrite an existing one named: %s' % (regtype(), regname))
    else:
        globals()[namespacename()][regname] = regobject
        return True

def namespace():
    return globals()[namespacename()]

def configloader(configpath):
    config = configparser.ConfigParser()
    config.read([configpath])
    for section in config.sections():
        if not register(section, {f[0]:f[1] for f in config.items(section)}):
            raise ValueError('attemped to register config section %s and encountered an error' % section)
        #else:
        #    print('%s config section registered' % section)

def partialnamespace(prefix):
    """
    returns a subset of the namespace that contains keys starting with the provided prefix
    :param prefix: string containing prefix
    :return: dict that is a subset of the config namespace
    """
    sep = '.' #TODO move constant to central library
    return {k[len(prefix + sep):]: v for k, v in namespace().items() if k.startswith(prefix + sep)}

#--- initialize namespace

globals()[namespacename()] = dict()