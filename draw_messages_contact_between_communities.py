import networkx as nx
import sys
import pandas as pd
import matplotlib.pyplot as plt
from alliances.alliance_members import alliance_members
import matplotlib.patches as mpatch

file = sys.argv[1]
G = nx.read_graphml(file)

community1_members_over_time = alliance_members['alliance43']
community2_members_over_time = alliance_members['alliance103']
community3_members_over_time = alliance_members['alliance38']
community4_members_over_time = alliance_members['alliance44']

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

cs1 = set()
cs2 = set()
cs3 = set()
cs4 = set()
es = set()

for n1 in community1_set:
	for n2 in community2_set:
		if G.has_edge(n1, n2):
			cs1.add(n1)
			cs2.add(n2)
			es.add((n1, n2))
	for n2 in community3_set:
		if G.has_edge(n1, n2):
			cs1.add(n1)
			cs3.add(n2)
			es.add((n1, n2))
	for n2 in community4_set:
		if G.has_edge(n1, n2):
			cs1.add(n1)
			cs4.add(n2)
			es.add((n1, n2))
for n1 in community2_set:
	for n2 in community1_set:
		if G.has_edge(n1, n2):
			cs2.add(n1)
			cs1.add(n2)
			es.add((n1, n2))
	for n2 in community3_set:
		if G.has_edge(n1, n2):
			cs2.add(n1)
			cs3.add(n2)
			es.add((n1, n2))
	for n2 in community4_set:
		if G.has_edge(n1, n2):
			cs2.add(n1)
			cs4.add(n2)
			es.add((n1, n2))

for n1 in community3_set:
	for n2 in community1_set:
		if G.has_edge(n1, n2):
			cs3.add(n1)
			cs1.add(n2)
			es.add((n1, n2))
	for n2 in community2_set:
		if G.has_edge(n1, n2):
			cs3.add(n1)
			cs2.add(n2)
			es.add((n1, n2))
	for n2 in community4_set:
		if G.has_edge(n1, n2):
			cs3.add(n1)
			cs4.add(n2)
			es.add((n1, n2))
for n1 in community4_set:
	for n2 in community1_set:
		if G.has_edge(n1, n2):
			cs4.add(n1)
			cs1.add(n2)
			es.add((n1, n2))
	for n2 in community2_set:
		if G.has_edge(n1, n2):
			cs4.add(n1)
			cs2.add(n2)
			es.add((n1, n2))
	for n2 in community3_set:
		if G.has_edge(n1, n2):
			cs4.add(n1)
			cs3.add(n2)
			es.add((n1, n2))

cc1 = ["#ff0000"] * len(cs1)
cc2 = ["#0a7e28"] * len(cs2)
cc3 = ["#0000ff"] * len(cs3)
cc4 = ["#7b7d7d"] * len(cs4)

nodelist = [item for sublist in [list(cs1), list(cs2), list(cs3), list(cs4)] for item in sublist]
colorlist = [item for sublist in [list(cc1), list(cc2), list(cc3), list(cc4)] for item in sublist]

tmp = G.subgraph(nodelist)
SG = nx.DiGraph(tmp)
# iterate over members
for n in nodelist:
	# add node if not present in the original graph
	# this could happen if in that day the player was offline
	if n not in SG.nodes:
		SG.add_node(n)

plt.figure(figsize = (7, 7), dpi = 500)
plt.title("Messages", fontsize = 30)
nx.draw_kamada_kawai(SG, arrowsize=2, arrowstyle= mpatch.ArrowStyle("-|>", head_length=1, head_width=1), with_labels=False, node_size=50, nodelist = nodelist, node_color = colorlist, edgelist=list(es))
plt.savefig("communities_contact.png", dpi=500)
plt.savefig("communities_contact.pdf", dpi=500)
