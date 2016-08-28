from gtool.core.types.output import TreeOutput
from gtool.core.filewalker import StructureFactory
import yaml

class Yaml(TreeOutput):

    def __output__(self, projectstructure, output=None):

        _yamloutput = self.__yamloutput__(projectstructure)

        if output is None:
            return _yamloutput
        else:
            with open(output,mode='w') as f:
                f.write(_yamloutput)
                f.close()
            return True #TODO inconsistent return yaml object vs true

    def __yamloutput__(self, projectstructure):

        def sub(tree=StructureFactory.Container()):
            if tree.haschildren:
                return [sub(child) for child in tree.children]
            else:
                return {tree.name: tree.dataasobject.asdict()}

        _ret = sub(projectstructure)
        return yaml.safe_dump(_ret, indent=4)


def load():
    return Yaml