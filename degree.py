import networkx as nx
import sys
import pandas as pd

file = sys.argv[1]

G = nx.read_graphml(file)

# compute measures
in_degree = G.in_degree(weight = "weight")
out_degree = G.out_degree(weight = "weight")
edge_count = G.degree(weight = "weight")

data = list()

# create output file
for n in G.nodes:
	data.append([n, in_degree[n], out_degree[n], edge_count[n]])

df = pd.DataFrame(data, columns=['node', 'in-degree', 'out-degree', 'edge-count'])
df.to_csv("degree.csv", index = False)
