import igraph as ig
import sys

file = sys.argv[1]
output = sys.argv[2]

mg = ig.Graph.Read_GraphML(file)
print(mg)
sg = mg.simplify(multiple=True, loops=True, combine_edges = dict(weight = "sum", timestamp = "ignore", source = "first", target = "first", type = "first"))
sg.write_graphml(output)