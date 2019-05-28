import networkx as nx
import sys
import pandas as pd

file = sys.argv[1]

G = nx.read_graphml(file)

betweenness = nx.betweenness_centrality(G, normalized=True, weight="weight")
pagerank = nx.pagerank(G, weight = "weight")

data = list()

for n in G.nodes:
	data.append([n,	betweenness[n], pagerank[n]])

df = pd.DataFrame(data, columns=['node', 'betweenness', 'PageRank'])
df.to_csv("centrality.csv", index = False)
