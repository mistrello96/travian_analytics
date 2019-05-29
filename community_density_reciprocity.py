from alliances.alliance_members import alliance_members
import pandas as pd
import sys
from os import walk
import networkx as nx
import csv

file = sys.argv[1]
time = int(sys.argv[2])

M = nx.read_graphml(file)

for n1, n2, d in M.edges(data=True):
	d.pop('edgetime', None)

G = nx.DiGraph()
for u,v,data in M.edges(data=True):
    w = data['weight'] if 'weight' in data else 1.0
    if G.has_edge(u,v):
        G[u][v]['weight'] += w
    else:
        G.add_edge(u, v, weight=w)

res = pd.DataFrame(columns=["alliance_name", "density", "reciprocity"])

for alliance in alliance_members:
	community = list((alliance_members[alliance][time]))
	if (len(community) > 9):
		tmp = G.subgraph(community)
		SG = nx.DiGraph(tmp)
		for n in community:
			if n not in SG.nodes:
				SG.add_node(n)
		try:
			res.loc[len(res)] = [alliance, nx.density(SG), nx.overall_reciprocity(SG)]

		except:
			res.loc[len(res)] = [alliance, 0 , 0]

res.to_csv("community_density_reciprocity.csv", index=False)