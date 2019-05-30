import networkx as nx
import sys
import numpy as np

file = sys.argv[1]

G = nx.read_graphml(file)
# print some aggregate measures
print(nx.overall_reciprocity(G))
print(np.mean(nx.average_neighbor_degree(G, weight= "weight").values()))