import shutil
import os

def newproject(templatepath, newprojectpath):

    if not os.path.exists(templatepath):
        raise FileNotFoundError('template location does not exist')
    if not os.path.isdir(templatepath):
        raise NotADirectoryError('template location must be a directory')

    if not os.path.exists(newprojectpath):
        raise FileNotFoundError('project location does not exist')
    if not os.path.isdir(newprojectpath):
        raise NotADirectoryError('project location must be a directory')

    if templatepath == newprojectpath:
        raise ValueError

    try:
        shutil.copy(templatepath, newprojectpath)
    except Exception as err:
        raise Exception('Could not deploy the project template; received the following error:' % err)

    return True

