from gtool.core.types.output import TreeOutput
import networkx
from gtool.core.utils.config import partialnamespace
from gtool.core.utils.runtime import runtimenamespace
from gtool.core.noderegistry import getObjectByUri
from gtool.core.utils.misc import striptoclassname
from distutils.util import strtobool

class Directedgraph(TreeOutput):

    def __init__(self):

        _scheme = runtimenamespace().get('outputscheme', None)
        if _scheme is None:
            raise ValueError('Output scheme is not defined')

        _outputconfig = partialnamespace('output').get(_scheme, None)
        if _outputconfig is None:
            raise ValueError('Output scheme configuration was not retrieved')

        _autolink = _outputconfig.get('autolink', None)
        if _autolink is not None:
            self.autolink = strtobool(_autolink)
        else:
            self.autolink = True

        _linkattribute = _outputconfig.get('link', None)
        if _linkattribute is None and not self.autolink:
            raise ValueError('a "link:" value must be set in [output.%s] '
                             'in gtool.cfg when using directedgraph output '
                             'and autolink is disabled' % _scheme)
        self.linkattribute = _linkattribute

        _linkproperties = _outputconfig.get('linkprops', None)
        if _linkproperties is not None:
            self.linkproperties = [l.strip() for l in _linkproperties.split(',')]
        else:
            self.linkproperties = []




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

        def _generatenetwork(tree, network=None):
            if isinstance(tree, list):
                return [_generatenetwork(item, network=network) for item in tree]
            elif isinstance(tree, dict):
                return {k: _generatenetwork(v, network=network) for k, v in tree.items()}
            else:
                _dict = self.convert(tree)
                nodename = tree.__context__['class']
                nodedict = _dict
                network.add_node(nodename, nodedict)
                if self.autolink:
                    # if autolink is false, only explicit links will be set
                    network.add_edge(tree.__context__['parent'].name, nodename)
                    #TODO what if parent doesn't exist?
                    #TODO add link properties to parent link

                _linkattribdict = {}

                for attrib in self.linkproperties:
                    _attrib = getattr(tree, attrib, None)
                    if _attrib is not None:
                        if hasattr(_attrib, '__iter__'):
                            if len(_attrib) > 1:
                                raise ValueError('%s in %s (%s) has multiple values and cannot '
                                                 'be used for link properties' % (attrib,
                                                                                  tree.__context__['class'],
                                                                                  striptoclassname(type(tree))
                                                                                  )
                                                 )
                            if hasattr(_attrib[0], '__convert__'):
                                #handles coretypes
                                _val = _attrib[0].__convert__(_attrib[0])
                            else:
                                _val = _attrib[0]
                        else:
                            _val = _attrib

                        _linkattribdict[attrib] = _val

                """
                for k in _linkattribdict.keys():
                    if k in _dict:
                        del(_dict[k])
                """

                if self.linkattribute is not None:
                    _link = getattr(tree, self.linkattribute, None)
                else:
                    _link = None
                if _link is not None:
                    for link in _link:
                        _obj = getObjectByUri('%s' % link)
                        network.add_edge(nodename, _obj.__context__['class'], attr_dict=_linkattribdict)

                return _dict

        def _sub(projectstructure):
            network = networkx.MultiDiGraph()
            _generatenetwork(projectstructure, network)
            return network

        return _sub(projectstructure)


def load():
    return Directedgraph
