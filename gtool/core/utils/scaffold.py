import shutil
import os

def newproject(templatepath, newprojectpath):

    if not os.path.exists(templatepath):
        raise FileNotFoundError('template location does not exist')
    if not os.path.isdir(templatepath):
        raise NotADirectoryError('template location must be a directory')

    if os.path.exists(newprojectpath):
        #os.makedirs(newprojectpath)
        raise Exception('project location already exists')

    if templatepath == newprojectpath:
        raise ValueError

    try:
        shutil.copytree(templatepath, newprojectpath)
    except Exception as err:
        raise Exception('Could not deploy the project template; received the following error: %s' % err)

    return True

