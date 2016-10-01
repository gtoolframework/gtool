import click
from gtool.core.utils import (loadconfig,
                              __loadplugins,
                              __configloader,
                              __loadclasses,
                              __loadaggregators,
                              __outputparser,
                              __registeroption,
                              process)
from gtool.core.plugin import pluginnamespace
from gtool.core.utils.config import partialnamespace
import sys

def listelements(path, scheme, verbose, silent, debug):

    if verbose and silent:
        click.echo('cannot use both the --verbose and --silent options together.')
        sys.exit(1)

    if verbose:
        click.echo('[VERBOSE] Loading project from %s...' % path)
    elif not silent:
        click.echo('Loading project from %s...' % path)

    dbg = debug
    projectconfig = {}

    try:
        if verbose:
            click.echo('[VERBOSE] Loading bootstrap config...')
        projectconfig = loadconfig(path)
    except Exception as err:
        click.echo('While processing bootstrap configuration directives '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(status=1)

    try:
        if verbose:
            click.echo('[VERBOSE] Loading plugins from code base and %s\\plugins...' % projectconfig['root'])
        __loadplugins(projectconfig['root'], verbose=verbose, silent=silent)
    except Exception as err:
        click.echo('While loading plugins '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    try:
        if verbose:
            click.echo('[VERBOSE] Loading project config from %s...' % projectconfig['configpath'])
        __configloader(projectconfig['configpath'])
    except Exception as err:
        click.echo('While processing bootstrap configuration directives '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    try:
        if verbose:
            click.echo('[VERBOSE] Loading user defined classes from %s...' % projectconfig['classes'])
        __loadclasses(projectconfig['classes'], verbose=verbose, silent=silent, dbg=dbg)
    except Exception as err:
        click.echo('While loading user configured classes '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    try:
        if verbose:
            click.echo('[VERBOSE] Loading user defined aggregators from %s...' % projectconfig['aggregators'])
        __loadaggregators(projectconfig['aggregators'], verbose=verbose, silent=silent)
    except Exception as err:
        click.echo('While loading user configured aggregates '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    if verbose:
        click.echo('[VERBOSE] Registering run time options...')

    try:
        __registeroption('outputscheme', scheme)
    except Exception as err:
        click.echo('While registering the output scheme specified via the command line '
                   'switch an error occurred. '
                   'Please make sure that the section [output.%s] exists in gtool.cfg. '
                   'The following message was received during the error: %s' % (scheme, err))
        sys.exit(1)

    try:
        __registeroption('debug', dbg)
    except Exception as err:
        click.echo('While registering a runtime debug option an error occurred. '
                   'This error is internal and you need to file a bug report. '
                   'The following message was received during the error: %s' % err)
        sys.exit(1)

    try:
        __outputparser(outputscheme=scheme)
    except Exception as err:
        click.echo('While registering output schemes for user configured classes '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    dataobject = None

    try:
        if verbose:
            click.echo('[VERBOSE] Loading data from %s...' % projectconfig['dataroot'])
        dataobject = process(projectconfig['dataroot'])
    except Exception as err:
        click.echo('While processing the data structure an error occurred. '
                   'The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    outputprocessor = None

    if verbose:
        click.echo('[VERBOSE] Using output scheme %s...' % scheme)

    outputschemeconfig = partialnamespace('output').get(scheme, None)

    if outputschemeconfig is None:
        click.echo('Could not find [output.%s] in gtool.cfg.')
        sys.exit(1)

    outputschemeplugin = outputschemeconfig.get('plugin', None)

    if outputschemeplugin is None:
        click.echo('an output plugin is not specified in [output.%s] in gtool.cfg.')
        sys.exit(1)

    try:
        if verbose:
            click.echo('[VERBOSE] Preparing output processor...')
        outputprocessor = pluginnamespace()[outputschemeplugin.upper()]()
    except Exception as err:
        click.echo('While loading the output processor specified in gtool.cfg '
                   'for output scheme [output.%s] an error occurred. The '
                   'following message was received during the error: %s' % (scheme, err))
        sys.exit(1)

    result = None

    try:
        if verbose:
            click.echo('[VERBOSE] Processing the data...')
        result = outputprocessor.output(dataobject)
    except Exception as err:
        click.echo('While processing the data into output an error occurred. '
                   'The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    if verbose:
        click.echo('[VERBOSE] Rendering output...')

    if not isinstance(result, str) and hasattr(result, '__iter__'):
        for row in result:
            print(row)
    else:
        print(result)

    if not silent:
        click.echo('Done')
    sys.exit(0)