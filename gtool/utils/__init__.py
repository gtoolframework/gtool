from .classgen import generateClass
from .config import readConfig, processConfigAlt, debugConfig
import os

def loadconfig(configpath, dbg=False):
    """

    :param configpath: path to config file
    :param dbg: set to ttue to debug config load
    :return: True
    """
    if os.path.exists(configpath):
        # TODO check if file is readable
        f = open(configpath, 'r')
        # TODO try except for file read errors
        configString = f.read()
    else:
        raise FileNotFoundError('%s does not exist' % configpath)
    # TODO capture exceptions
    config = readConfig(configString)
    if dbg is True:
        debug(config)
    # TODO capture exceptions
    classDict = processConfigAlt(config)
    for k, v in classDict.items():
        # TODO capture exceptions
        generateClass(k, v)
    f.close()


def debug(config):
    print('--- conf debug ---')
    debugConfig(config)
    print('--- end of config debug ---')