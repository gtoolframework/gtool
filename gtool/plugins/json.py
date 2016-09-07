from gtool.core.types.output import TreeOutput
from gtool.core.filewalker import StructureFactory
import json


class Json(TreeOutput):

    def __output__(self, projectstructure, output=None):

        _jsonoutput = self.__jsonoutput__(projectstructure)

        if output is None:
            return _jsonoutput
        else:
            with open(output, mode='w') as f:
                f.write(_jsonoutput)
                f.close()
            return True  # TODO inconsistent return json object vs true

    def __jsonoutput__(self, projectstructure):

        def sub(tree=StructureFactory.Container()):
            if tree.haschildren:
                return [sub(child) for child in tree.children]
            else:
                return {tree.name: tree.dataasobject.asdict()}

        _ret = sub(projectstructure)
        return json.dumps(_ret, sort_keys=True, indent=4)


def load():
    return Json