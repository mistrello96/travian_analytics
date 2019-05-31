import networkx as nx
import sys
import pandas as pd
import matplotlib.pyplot as plt
from alliances.alliance_members import alliance_members

file = sys.argv[1]

community1_members_over_time = alliance_members['alliance43']
community2_members_over_time = alliance_members['alliance103']
community3_members_over_time = alliance_members['alliance38']
community4_members_over_time = alliance_members['alliance44']
community5_members_over_time = alliance_members['alliance73']
community6_members_over_time = alliance_members['alliance5']

community1_set = set()
for x in community1_members_over_time:
	community1_set = community1_set.union(x)

community2_set = set()
for x in community2_members_over_time:
	community2_set = community2_set.union(x)

community3_set = set()
for x in community3_members_over_time:
	community3_set = community3_set.union(x)

community4_set = set()
for x in community4_members_over_time:
	community4_set = community4_set.union(x)

community5_set = set()
for x in community5_members_over_time:
	community5_set = community5_set.union(x)

community6_set = set()
for x in community6_members_over_time:
	community6_set = community6_set.union(x)

community1_color = ["#ff0000"] * len(community1_set)
community2_color = ["#00ff00"] * len(community2_set)
community3_color = ["#0000ff"] * len(community3_set)
community4_color = ["#7b7d7d"] * len(community4_set)
community5_color = ["#512e5f"] * len(community5_set)
community6_color = ["#784212"] * len(community6_set)

nodelist = [item for sublist in [list(community1_set), list(community2_set), list(community3_set), list(community4_set), list(community5_set), list(community6_set)] for item in sublist]
colorlist = [item for sublist in [list(community1_color), list(community2_color), list(community3_color), list(community4_color), list(community5_color), list(community6_color)] for item in sublist]

G = nx.read_graphml(file)
tmp = G.subgraph(nodelist)
SG = nx.DiGraph(tmp)
# iterate over members
for n in nodelist:
	# add node if not present in the original graph
	# this could happen if in that day the player was offline
	if n not in SG.nodes:
		SG.add_node(n)


nx.draw_kamada_kawai(SG, arrowsize=2, with_labels=False, node_size=50, nodelist = nodelist, node_color = colorlist)
plt.savefig("test.png")