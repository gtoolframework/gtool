from gtool.core.types.output import TreeOutput
import networkx
from gtool.core.utils.config import partialnamespace
from gtool.core.utils.runtime import runtimenamespace

class Directedgraph(TreeOutput):

    def __init__(self):
        #TODO load from config args for link attribute name
        #TODO load from config arg for link name
        #TODO load from config args for link properties
        #TODO load from config node name
        #TODO load from config node properties

        _scheme = runtimenamespace().get('outputscheme', None)
        if _scheme is None:
            raise ValueError('Output scheme is not define')

        _outputconfig = partialnamespace('output').get(_scheme, None)
        if _outputconfig is None:
            raise ValueError('Output scheme configuration was not retrieved')

        self.linkattribute = _outputconfig.get('link', None)
        self.linkproperties = _outputconfig.get('linkprops', None)
        super(Directedgraph, self).__init__()

    def __output__(self, projectstructure, output=None):

        _graphoutput = super(Directedgraph, self).__output__(projectstructure)

        if output is None:
            raise ValueError('output file be specified for Multipgraph output')
        else:
            networkx.write_gml(_graphoutput, output)
            return True  # TODO inconsistent return json object vs true

    def filter(self, obj):
        return super(Directedgraph, self).filter(obj)

    def convert(self, obj):
        return super(Directedgraph, self).convert(obj)

    def outputprocessor(self, projectstructure):

        def _sub2(tree, network=None):
            if isinstance(tree, list):
                return [_sub2(item, network=network) for item in tree]
            elif isinstance(tree, dict):
                return {k: _sub2(v, network=network) for k, v in tree.items()}
            else:
                _dict = self.convert(tree)
                nodename = tree.__context__['class']
                nodedict = _dict
                network.add_node(nodename, nodedict)
                network.add_edge('*', nodename)
                return _dict

        def _sub(projectstructure):
            network = networkx.MultiDiGraph(name='test')
            _sub2(projectstructure, network)
            return network

        return _sub(projectstructure)


def load():
    return Directedgraph
