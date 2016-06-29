from pluginbase import PluginBase

def loadplugins(pluginbasepath):
    plugin_base = PluginBase(package='gtool.plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=__enumerateplugins(pluginbasepath), identifier='gtool', persist=True)
    for plugin_name in plugin_source.list_plugins():
        print('plugin_name:', plugin_name)
        _plugin = plugin_source.load_plugin(plugin_name)
        registerPlugin(plugin_name, _plugin)

def __enumerateplugins(pluginbasepath):
    # TODO enumerate subdirs
    return [pluginbasepath]


def __loadplugins(pluginpath):
    pass

# --- static ---
__PLUGINS = 'plugins' # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins

def pluginnamespace():
    return __PLUGINS

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerPlugin(pluginName, pluginObj):
    #print(globals())
    if pluginName in globals()[pluginnamespace()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One plugin tried to overwrite an existing one. plugin name: %s' % pluginName)
    else:
        globals()[pluginnamespace()][pluginName] = pluginObj
        return True

def pluginspace():
    return globals()[pluginnamespace()]


#--- initialize namespace
globals()[pluginnamespace()] = dict()