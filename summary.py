import networkx as nx
import sys
import statistics as st

file = sys.argv[1]

G = nx.read_graphml(file)
print(nx.overall_reciprocity(G))
print(st.mean(nx.average_neighbor_degree(G, weight= "weight").values()))