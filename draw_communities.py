import networkx as nx
import sys
import pandas as pd
import matplotlib.pyplot as plt
from alliances.alliance_members import alliance_members
import matplotlib.patches as mpatch

file = sys.argv[1]

# import community members over time
community1_members_over_time = alliance_members['alliance43']
community2_members_over_time = alliance_members['alliance103']
community3_members_over_time = alliance_members['alliance38']
community4_members_over_time = alliance_members['alliance44']

# put community members in sets
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

# find shared nodes between communities
shared_set = (community1_set & community2_set) | (community1_set & community3_set) | (community1_set & community4_set) | (community2_set & community3_set) | (community2_set & community4_set) | (community3_set & community4_set)

# remove the shared nodes
community1_set = community1_set - shared_set
community2_set = community2_set - shared_set
community3_set = community3_set - shared_set
community4_set = community4_set - shared_set

# select a color for each community
community1_color = ["#ff0000"] * len(community1_set)
community2_color = ["#0a7e28"] * len(community2_set)
community3_color = ["#0000ff"] * len(community3_set)
community4_color = ["#7b7d7d"] * len(community4_set)
shared_color = ["#dcff17"] * len(shared_set)

# create list of nodes to be drawed
nodelist = [item for sublist in [list(community1_set), list(community2_set), list(community3_set), list(community4_set), list(shared_set)] for item in sublist]
colorlist = [item for sublist in [list(community1_color), list(community2_color), list(community3_color), list(community4_color), list(shared_color)] for item in sublist]

# extract the subgraph
G = nx.read_graphml(file)
tmp = G.subgraph(nodelist)
SG = nx.DiGraph(tmp)
# iterate over members
for n in nodelist:
	# add node if not present in the original graph
	# this could happen if in that day the player was offline
	if n not in SG.nodes:
		SG.add_node(n)

# draw the graph
plt.figure(figsize = (10, 10), dpi = 500)
plt.title("Messages", fontsize = 30)
nx.draw_kamada_kawai(SG, arrowsize=2, arrowstyle= mpatch.ArrowStyle("-|>", head_length=1, head_width=1), with_labels=False, node_size=50, nodelist = nodelist, node_color = colorlist)
#nx.draw_spring(SG, arrowsize=2, arrowstyle= mpatch.ArrowStyle("-|>", head_length=1, head_width=1), with_labels=False, node_size=50, nodelist = nodelist, node_color = colorlist)
plt.tight_layout()
plt.savefig("out.png", dpi=500)
plt.savefig("out.pdf", dpi=500)