from gtool.core.types.output import TreeOutput
from gtool.core.utils.config import partialnamespace
from gtool.core.utils.runtime import runtimenamespace
#from gtool.core.noderegistry import getObjectByUri
#from gtool.core.utils.misc import striptoclassname
import pydot

class Decisiontree(TreeOutput):

    def __init__(self):

        def getconfigelement(config, key, scheme):
            _retval = config.get(key, None)
            if _retval is not None:
                return _retval
            else:
                raise ValueError('a "%s:" value must be set in [output.%s] in '
                                 'gtool.cfg when using decisiontree output' % (key, scheme))

        _scheme = runtimenamespace().get('outputscheme', None)
        if _scheme is None:
            raise ValueError('Output scheme is not defined')

        _outputconfig = partialnamespace('output').get(_scheme, None)
        if _outputconfig is None:
            raise ValueError('Output scheme configuration was not retrieved')

        self.layout = _outputconfig.get('layout', None)
        self.class_goal = getconfigelement(_outputconfig, 'class_goal', _scheme)
        self.class_node = getconfigelement(_outputconfig, 'class_node', _scheme)
        self.class_and = getconfigelement(_outputconfig, 'class_and', _scheme)
        self.attribute_node = getconfigelement(_outputconfig, 'attribute_node', _scheme)
        self.attribute_and = getconfigelement(_outputconfig, 'attribute_and', _scheme)
        self.attribute_tooltip = _outputconfig.get('attribute_tooltip', None)
        self.attribute_url = _outputconfig.get('attribute_url', None)

        self.__aligned__ = False
        self.__recursionpermitted__ = True
        #super(Decisiontree, self).__init__()

    def __output__(self, projectstructure, output=None):

        _decisiontree = super(Decisiontree, self).__output__(projectstructure)

        if output is None:
            raise ValueError('output file must be specified for Decision Tree output')
        else:
            _decisiontree.write(output)
            return True

    def filter(self, obj):
        return super(Decisiontree, self).filter(obj)

    def convert(self, obj):
        return super(Decisiontree, self).convert(obj)

    def outputprocessor(self, projectstructure):

        def _generatenetwork(tree, decisiontree, parent=None, identifier=None):

            if isinstance(tree, list):
                return [_generatenetwork(item, decisiontree, parent=parent, identifier=identifier) for item in tree]
            elif isinstance(tree, dict):
                return {k: _generatenetwork(v, decisiontree, parent=parent, identifier=identifier) for k, v in tree.items()}
            else:
                _dict = self.convert(tree)
                #nodename = tree.__context__['class']
                #nodedict = _dict

                _title = "%s" % tree.title[0] if not isinstance(tree.title, str) else tree.title
                nodetitle = (identifier[0],) #_title,)
                nodeconfig = {}
                nodeconfig['id'] = identifier[0]
                nodeconfig['label'] = _title

                _shape = tree.metas().get('shape', None)
                if _shape is not None:
                    nodeconfig['shape'] = _shape

                if self.attribute_tooltip is not None:
                    _tooltip = getattr(tree, self.attribute_tooltip, None)
                    if _tooltip is not None:
                        try:
                            _tooltip = _tooltip[0] if hasattr(_tooltip, '__iter__') else _tooltip
                            nodeconfig['tooltip'] = "%s" % _tooltip
                        except IndexError:
                            pass

                if self.attribute_url is not None:
                    _url = getattr(tree, self.attribute_url, None)
                    if _url is not None:
                        try:
                            _url = _url[0] if hasattr(_url, '__iter__') else _url
                            nodeconfig['URL'] = "%s" % _url
                        except IndexError:
                            pass

                decisiontree.add_node(pydot.Node(*nodetitle, **nodeconfig))

                if parent is not None:
                    decisiontree.add_edge(pydot.Edge(src=parent, dst=identifier[0])) #'%s' % _title))

                _parent = identifier[0] #'%s' % _title
                identifier[0] += 1


                for node in getattr(tree, self.attribute_node):
                    _generatenetwork(node, decisiontree, parent=_parent, identifier=identifier)
                    identifier[0] += 1

                for _and in getattr(tree, self.attribute_and):
                    _generatenetwork(_and, decisiontree, parent=_parent, identifier=identifier)
                    identifier[0] += 1



        def _sub(projectstructure):
            decisiontree = pydot.Dot()
            counter = [0]

            _generatenetwork(projectstructure, decisiontree, identifier=counter)
            return decisiontree

        return _sub(projectstructure)


def load():
    return Decisiontree
