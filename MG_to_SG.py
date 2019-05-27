import networkx as nx
import sys
import statistics as st

file = sys.argv[1]

M = nx.read_edgelist(file, comments='#', delimiter=',', create_using=nx.MultiDiGraph, data = [('type', str), ('weight',int), ('timestamp', int)])

for n1, n2, d in M.edges(data=True):
	d.pop('timestamp', None)

# create weighted graph from M
G = nx.DiGraph()
for u,v,data in M.edges(data=True):
    w = data['weight'] if 'weight' in data else 1.0
    t = data['type']
    if G.has_edge(u,v):
        G[u][v]['weight'] += w
    else:
        G.add_edge(u, v, weight=w, type = t)

nx.write_graphml(M, "./MG.graphml")
nx.write_graphml(G, "./SG.graphml")