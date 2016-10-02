from gtool.core.types.output import TreeOutput
import networkx
from gtool.core.utils.config import partialnamespace
from gtool.core.utils.runtime import runtimenamespace
from gtool.core.noderegistry import getObjectByUri
from distutils.util import strtobool

class Directedgraph(TreeOutput):

    def __init__(self):

        _scheme = runtimenamespace().get('outputscheme', None)
        if _scheme is None:
            raise ValueError('Output scheme is not define')

        _outputconfig = partialnamespace('output').get(_scheme, None)
        if _outputconfig is None:
            raise ValueError('Output scheme configuration was not retrieved')

        _linkattribute = _outputconfig.get('link', None)
        if _linkattribute is None:
            raise ValueError('a "link:" value must be set in [output.%s] '
                             'in gtool.cfg when using directedgraph output' % _scheme)
        self.linkattribute = _linkattribute

        _linkproperties = _outputconfig.get('linkprops', None)
        if _linkproperties is not None:
            self.linkproperties = [l.strip() for l in _linkproperties.split(',')]
        else:
            self.linkproperties = None


        _autolink = _outputconfig.get('autolink', None)
        if _autolink is not None:
            self.autolink = strtobool(_autolink)
        else:
            self.autolink = True

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
                if self.autolink:
                    # if autolink is false, only explicit links will be set
                    network.add_edge(tree.__context__['parent'].name, nodename) #TODO what if parent doesn't exist?

                _link = getattr(tree, self.linkattribute, None)

                if _link is not None:

                    for link in _link:
                        #print('link:', link)
                        _obj = getObjectByUri('%s' % link)
                        #print(_obj)
                        network.add_edge(nodename, _obj.__context__['class'])

                for attrib in self.linkproperties:
                    _attrib = getattr(tree, attrib, None)
                    if _attrib is not None:
                        if hasattr(_attrib, '__iter__'):
                            for attr in _attrib:
                                print(attr)
                        else:
                            print(_attrib)
                #TODO read link attr
                #TODO read attr's for edge
                return _dict

        def _sub(projectstructure):
            network = networkx.MultiDiGraph(name='test')
            _sub2(projectstructure, network)
            return network

        return _sub(projectstructure)


def load():
    return Directedgraph
