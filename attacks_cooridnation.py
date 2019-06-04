from alliances.alliance_members import alliance_members
import sys
from os import walk
import networkx as nx
from MG_to_SG_function import MG_to_SG
import matplotlib.patches as mpatch
import matplotlib.pyplot as plt

path = sys.argv[1]

community_members_over_time = alliance_members['alliance43']

for day in range(0,30):
	community_members = community_members_over_time[day]
	M = nx.read_graphml(path + "attacks-timestamped-2009-12-" + str(day+1) + ".graphml")
	
	G = MG_to_SG(M)
	attack_edges = set()
	active_community_members = set()
	# find the targets  of the community
	for cn in community_members:
		for n in G.nodes:
			if G.has_edge(cn, n):
				attack_edges.add((cn, n))
				active_community_members.add(cn)
	tmp = G.edge_subgraph(attack_edges)
	# create a copy (otherwise G cannot be modified)
	SG = nx.DiGraph(tmp)

	targets = set()
	for n in SG.nodes:
		if n not in active_community_members:
			targets.add(n)

	nodelist = [item for sublist in [list(active_community_members), list(targets)] for item in sublist]
	community_color = ["#ff0000"] * len(active_community_members)
	targets_color = ["#0a7e28"] * len(targets)
	colorlist = [item for sublist in [list(community_color), list(targets_color)] for item in sublist]

	# count number of different attackers
	deg = dict(SG.in_degree(weight = "weight"))
	#print(deg)
	sorteddegree = [(k,v) for k, v in zip(deg.keys(), deg.values())]
	sorteddegree.sort(key = lambda x: x[1], reverse = True)
	print(sorteddegree[0])
	