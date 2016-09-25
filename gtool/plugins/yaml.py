from gtool.core.types.output import TreeOutput
from gtool.core.filewalker import StructureFactory
import yaml

class Yaml(TreeOutput):

    def __output__(self, projectstructure, output=None):

        #_yamloutput = self.__yamloutput__(projectstructure)
        _yamloutput = super(Yaml, self).__output__(projectstructure)

        if output is None:
            return _yamloutput
        else:
            with open(output,mode='w') as f:
                f.write(_yamloutput)
                f.close()
            return True #TODO inconsistent return yaml object vs true

    def filter(self, obj):
        return super(Yaml, self).filter(obj)

    def convert(self, obj):
        return super(Yaml, self).convert(obj)

    def outputprocessor(self, projectstructure):

        def sub(tree=StructureFactory.Container()):
            if tree.haschildren:
                return [sub(child) for child in tree.children]
            else:
                return {tree.name: tree.dataasobject.asdict()}

        _tree = sub(projectstructure)
        if isinstance(_tree, dict):
            for i in self.aggregates():
                _tree.update(i)
        elif isinstance(_tree, list):
            _tree.extend(self.aggregates())
        else:
            raise TypeError('unknown type in _tree')
        return yaml.safe_dump(_tree, indent=4)


def load():
    return Yaml