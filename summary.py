import networkx as nx
import sys
import numpy as np

file = sys.argv[1]

G = nx.read_graphml(file)
# print some aggregate measures
print("Density " + str(nx.density(G)))
print("Reciprocity " + str(nx.overall_reciprocity(G)))
print("Mean neighbor degree " + str(np.mean(list(nx.average_neighbor_degree(G, weight= "weight").values()))))