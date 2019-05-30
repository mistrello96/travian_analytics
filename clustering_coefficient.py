import networkx as nx
import sys
import pandas as pd

file = sys.argv[1]

G = nx.read_graphml(file)

# compute measure
clustering = nx.clustering(G, weight = "weight")

data = list()

# create results file
for n in G.nodes:
	data.append([n,	clustering[n]])

df = pd.DataFrame(data, columns=['node', 'clustering_coefficient'])
df.to_csv("clustering_coefficient.csv", index = False)