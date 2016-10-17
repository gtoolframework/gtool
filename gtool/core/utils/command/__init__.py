import click
from .process import processproject
from .listelements import listelements
from gtool.core.utils.scaffold import newproject
import sys, os

if sys.version_info[:2] < (3, 5):
    raise ImportError("Python 3.5 or later is required for G.Tool (%d.%d detected)." % sys.version_info[:2])

#TODO read from central version file (such as \projecttemplate)
VERSION='Version 0.1.2 BETA'

def __create__():
    pass

@click.group()
def cli():
    """G.Tool is a framework for creating and processing Governance, Risk and Compliance data structures."""
    pass

@click.command(short_help="Process a project into final output")
@click.argument('path',
                default='.',
                type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option('--scheme',
              prompt=True,
              help='[REQUIRED] one of the output schemes specified in gtool.cfg. '
                   'For outsceme output.1 write "gtool --scheme 1"')
@click.option('--output',
              type=click.Path(exists=False, file_okay=True, resolve_path=False),
              help='[OPTIONAL] location to output data (may be required by some output schemes)')
@click.option('--verbose',
              is_flag=True,
              help='[OPTIONAL] makes gtool more chatty')
@click.option('--silent',
              is_flag=True,
              help='[OPTIONAL] suppress all output except results (cannot use in combination with --verbose')
@click.option('--debug',
              is_flag=True,
              help='[OPTIONAL] not implemented yet')
def process(path, scheme, output, verbose, silent, debug):
    """gtool PROCESS will read a project folder located at the provided PATH location and generate an output."""
    #processproject(path, scheme, output, verbose, silent, debug)
    processproject(path=path,
                   output=output,
                   scheme=scheme,
                   verbose=verbose,
                   silent=silent,
                   debug=debug)
    sys.exit(0)

@click.command(short_help="Create a new project using the standard template")
@click.argument('path',
                default='.',
                type=click.Path(exists=False, file_okay=False, resolve_path=True))
def create(path):
    """gtool CREATE will create a new directory PATH containing a
    project scaffold that can be processed by G.Tool"""

    __TEMPLATEPATH__ = os.path.realpath(os.path.join(os.path.dirname(__file__), '..\\..\\projecttemplate\\'))

    try:
        newproject(__TEMPLATEPATH__, path)
    except Exception as err:
        click.echo('While attempting to create a new project, '
                   'an error occured and the following message was received: %s' % err)
        sys.exit(1)

    click.echo('New project created at %s' % os.path.realpath(os.path.join(os.getcwd(), path)))
    sys.exit(0)

@click.command(short_help="Display the version of g.tool")
def version():
    """Display version of g.tool you are running"""
    click.echo(VERSION)
    sys.exit(0)

@click.command(short_help="List non-data project elements")
@click.argument('path',
                default='.',
                type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option('--list-type',
              type=click.Choice(['aggregates', 'classes', 'outputplugins', 'types', 'methods', 'plugins']))
def list_elements(path, list_type):
    """List classes, aggregates, plugins, outputs and other non-data elements in the project.
    By default the current working directory will be used unless a PATH argument is supplied."""
    if listelements(path, list_type):
        sys.exit(0)
    else:
        sys.exit(1)

cli.add_command(process, name='process')
cli.add_command(create, name='create')
cli.add_command(version, name='version')
cli.add_command(list_elements, name='list')

if __name__ == '__main__':
    argv = sys.argv
    verbose = False
    silent = False
    debug = False

    processproject(argv[1], argv[2], verbose, silent, debug)