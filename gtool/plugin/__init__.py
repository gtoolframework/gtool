from pluginbase import PluginBase

def loadplugins(pluginbasepath):
    plugin_base = PluginBase(package='gtool.plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=__enumerateplugins(pluginbasepath), identifier='gtool', persist=True)
    for plugin_name in plugin_source.list_plugins():
        print('loading plug-in:', plugin_name)
        _plugin = plugin_source.load_plugin(plugin_name)
        registerPlugin(plugin_name.upper(), _plugin.load())

def __enumerateplugins(pluginbasepath):
    # TODO enumerate subdirs
    return [pluginbasepath]

# --- static ---

def plugins():
    __PLUGINS = '__plugins__'  # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins
    return __PLUGINS

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerPlugin(pluginName, pluginObj):
    #print(globals())
    if pluginName in globals()[plugins()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One plugin tried to overwrite an existing one. plugin name: %s' % pluginName)
    else:
        globals()[plugins()][pluginName] = pluginObj
        return True

def pluginnamespace():
    return globals()[plugins()]

#--- initialize namespace

globals()[plugins()] = dict()