from alliances.alliance_members import alliance_members
import sys
from os import walk
import networkx as nx
from MG_to_SG_function import MG_to_SG
import matplotlib.patches as mpatch
import matplotlib.pyplot as plt

path = sys.argv[1]

# read the community member for each day
community_members_over_time = alliance_members['alliance43']

# iterate over days
for day in range(0,30):
	# extract the comminity nodes of that day
	community_members = community_members_over_time[day]
	M = nx.read_graphml(path + "attacks-timestamped-2009-12-" + str(day+1) + ".graphml")
	# pass to a graph
	G = MG_to_SG(M)
	attack_edges = set()
	active_community_members = set()
	# find the targets  of the community
	for cn in community_members:
		for n in G.nodes:
			if G.has_edge(cn, n):
				attack_edges.add((cn, n))
				active_community_members.add(cn)
	# induce a subgraph of the attackers-attacked ndes
	tmp = G.edge_subgraph(attack_edges)
	# create a copy (otherwise G cannot be modified)
	SG = nx.DiGraph(tmp)

	# count number of different attackers for each node
	# we don't want to use the weight because we just want to count how many different attackers was
	deg = dict(SG.in_degree())
	# find the most attacked node and print its info
	sorteddegree = [(k,v) for k, v in zip(deg.keys(), deg.values())]
	sorteddegree.sort(key = lambda x: x[1], reverse = True)
	print(sorteddegree[0])
	