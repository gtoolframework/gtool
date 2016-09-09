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

        """
        def sub(tree=StructureFactory.Container()):
            if tree.haschildren:
                return [sub(child) for child in tree.children]
            else:
                return {tree.name: tree.dataasobject.asdict()}
        """

        def _sub(tree):
            if isinstance(tree, list):
                return [_sub(item) for item in tree]
            elif isinstance(tree, dict):
                return {k: _sub(v) for k, v in tree.items()}
            else:
                return tree.asdict()

        pass
        _output = self.__treeoutput__(projectstructure)
        _tree = _sub(_output)
        #_ret = sub(projectstructure)
        #if y == _ret:
        #    print('match!')
        return json.dumps(_tree, sort_keys=True, indent=4)


def load():
    return Json