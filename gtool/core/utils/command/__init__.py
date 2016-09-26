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
import sys

VERSION='version 0.1 BETA'

def version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()

def outputscheme(ctx, param, value):
    return value

def __cli__(path, scheme, verbose, debug):
    # debug mode (read err)
    # load output mode
    click.echo('Loading project configuration and data from %s' % path)
    click.echo('Using output scheme %s' % scheme)

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

    if verbose:
        click.echo('[VERBOSE] Bootstrap config loaded.')

    try:
        __loadplugins(projectconfig['root'])
    except Exception as err:
        click.echo('While loading plugins '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    try:
        __configloader(projectconfig['configpath'])
    except Exception as err:
        click.echo('While processing bootstrap configuration directives '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    try:
        __loadclasses(projectconfig['classes'], dbg=dbg)
    except Exception as err:
        click.echo('While loading user configured classes '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    try:
        __loadaggregators(projectconfig['aggregators'])
    except Exception as err:
        click.echo('While loading user configured aggregates '
                   'an error occurred. The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

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
        dataobject = process(projectconfig['dataroot'])
    except Exception as err:
        click.echo('While processing the data structure an error occurred. '
                   'The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    outputprocessor = None

    try:
        outputprocessor = pluginnamespace()['JSON']()
    except Exception as err:
        click.echo('While loading the output processor specified in gtool.cfg '
                   'for output scheme output.%s an error occurred. The '
                   'following message was received during the error: %s' % (scheme, err))
        sys.exit(1)

    result = None

    try:
        result = outputprocessor.output(dataobject)
    except Exception as err:
        click.echo('While processing the data into output an error occurred. '
                   'The following message was received '
                   'during the error: %s' % err)
        sys.exit(1)

    if not isinstance(result, str) and hasattr(result, '__iter__'):
        for row in result:
            print(row)
    else:
        print(result)

    # sf = projectloader(project, dbg=False, outputscheme=scheme)
    click.echo('Done')
    sys.exit(0)

@click.command()
@click.argument('path',
                default='.',
                type=click.Path(exists=True, file_okay=False, resolve_path=True),
                callback=outputscheme)
@click.option('--scheme',
              prompt=True,
              help='[REQUIRED] one of the output schemes specified in gtool.cfg. '
                   'For outsceme output.1 write "gtool --scheme 1"')
@click.option('--version',
              is_flag=True,
              callback=version,
              expose_value=False,
              is_eager=True,
              help='[OPTIONAL] displays the version of gtool and exits')
@click.option('--verbose',
              is_flag=True,
              help='[OPTIONAL] makes gtool more chatty')
@click.option('--debug',
              is_flag=True,
              help='[OPTIONAL] not implemented yet')
def cli(path, scheme, verbose, debug):
    """gtool processes a project folder located at the provided PATH location."""
    __cli__(path,scheme,verbose, debug)

if __name__ == '__main__':
    __cli__('test\\test42', '1', False)