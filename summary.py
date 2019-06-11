import networkx as nx
import sys
import numpy as np

file = sys.argv[1]

G = nx.read_graphml(file)
# print some aggregate measures
print("Density " + str(nx.density(G)))
print("Reciprocity " + str(nx.overall_reciprocity(G)))

deg = G.out_degree()
res = 0
for n in G.nodes:
	res += deg[n]
print("Mean number of neighbor" + str(res / len(G.nodes)))