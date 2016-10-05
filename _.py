import pydot

G = pydot.Dot(splines='ortho')


#G = pydot.Graph()

ROOT = '*'

G.add_node(pydot.Node(ROOT))

for n in ['A', 'B', 'C', 'D']:
    _node = pydot.Node(n, shape='square')
    G.add_node(_node)
    G.add_edge(pydot.Edge(ROOT, n))


G.add_edge(pydot.Edge('B', 'D'))

for e in G.get_edges():
    print(e.obj_dict['points'])

for n in G.get_nodes():
    print(n.obj_dict['name'])

G.write('x.dot')