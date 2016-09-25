from gtool.core.types.output import TreeOutput
import yaml

class Yaml(TreeOutput):

    def __output__(self, projectstructure, output=None):

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

        def _sub(tree):
            if isinstance(tree, list):
                return [_sub(item) for item in tree]
            elif isinstance(tree, dict):
                return {k: _sub(v) for k, v in tree.items()}
            else:
                return self.convert(tree)

        _tree = self.integrateaggregates(_sub(projectstructure))

        return yaml.safe_dump(_tree, indent=4, default_flow_style=False)


def load():
    return Yaml