import click
from gtool.core.utils import (loadconfig,
                              __loadplugins,
                              __configloader,
                              __loadclasses,
                              __loadaggregators
                              )
from gtool.core.plugin import pluginnamespace
from gtool.core.namespace import namespace as classnamespace
import gtool.core.types.core as coretypes
from gtool.core.types.output import Output
from gtool.core.aggregatorregistry import aggregatornamespace
import sys
import inspect

#'aggregates', 'classes', 'outputplugins', 'types', 'methods', 'plugins'

def listaggregates():
    # TODO add errors
    _base = inspect.getmro(coretypes.Aggregator)[0]

    for k, v in pluginnamespace().items():
        if _base in inspect.getmro(v):
            print(k.title())

    return True

def listclasses():
    # TODO add errors
    for k in classnamespace().keys():
        print(k)
    return True

def listoutputplugins():
    #TODO add errors

    _base = inspect.getmro(Output)[0]

    for k,v in pluginnamespace().items():
        if _base in inspect.getmro(v):
            print(k)

    return True

def listtypes():
    # TODO add errors
    _base = inspect.getmro(coretypes.CoreType)[0]

    for k, v in pluginnamespace().items():
        if _base in inspect.getmro(v):
            print(k.title())

    return True

def listmethods():
    # TODO add errors
    _base = inspect.getmro(coretypes.FunctionType)[0]

    for k, v in pluginnamespace().items():
        if _base in inspect.getmro(v):
            print(k.title())

    return True

def listplugins():
    # TODO add errors
    for k, v in pluginnamespace().items():
        print(k)
    return True

def listelements(path, list_type):

    verbose = False
    silent = True
    debug = False

    click.echo('Loading project from %s' % path)

    dbg = debug
    projectconfig = {}

    try:
        projectconfig = loadconfig(path)
    except Exception as err:
        click.echo('While processing bootstrap configuration directives '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        return False

    try:
        __loadplugins(projectconfig['root'], verbose=verbose, silent=silent)
    except Exception as err:
        click.echo('While loading plugins '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        return False

    try:
        __configloader(projectconfig['configpath'])
    except Exception as err:
        click.echo('While processing bootstrap configuration directives '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        return False

    try:
        __loadclasses(projectconfig['classes'], verbose=verbose, silent=silent, dbg=dbg)
    except Exception as err:
        click.echo('While loading user configured classes '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        return False

    try:
        __loadaggregators(projectconfig['aggregators'], verbose=verbose, silent=silent)
    except Exception as err:
        click.echo('While loading user configured aggregates '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        return False

    listfunctions = {
        'aggregates' : listaggregates,
        'classes': listclasses,
        'outputplugins': listoutputplugins,
        'types': listtypes,
        'methods': listmethods,
        'plugins': listplugins,
    }

    listfunc = listfunctions.get(list_type, None)

    if listfunc is None:
        click.echo('Unknown value provided to --list-type, please choose one of the following: aggregates, classes, outputplugins, types, methods, plugins')
        return False

    return listfunc()

if __name__ == '__main__':
    argv = sys.argv
    listelements(argv[1], argv[2])