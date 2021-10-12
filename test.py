import pylab
import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.digraph import DiGraph

edge_list = [(1, 2), (2, 1), (2, 3), (3, 5), (5, -4), (-4, 3), (3, 4), (-4, -3),
             (-3, 4), (-3, -2), (4, -5), (-5, -3), (-2, -1), (-1, -2)]

# add_nodes_from([2, 3, 4, 5])
g = DiGraph(edge_list)

nx.draw(g)
pylab.show()

x = nx.kosaraju_strongly_connected_components(g)

for y in x:
    print(y)
