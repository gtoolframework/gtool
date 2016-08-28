from gtool.core.types.output import TreeOutput
from gtool.core.filewalker import StructureFactory
import json

class Json(TreeOutput):

    def __output__(self, projectstructure, output=None):
        #projectstructure = StructureFactory.Container()
        return json.dumps(self.__jsonoutput__(projectstructure))

    def __jsonoutput__(self, projectstructure):

        def sub(tree=StructureFactory.Container()):
            if tree.haschildren:
                return [sub(child) for child in tree.children]
            else:
                return tree.dataasobject.asdict()


        _ret = sub(projectstructure)
        return _ret


def load():
    return Json