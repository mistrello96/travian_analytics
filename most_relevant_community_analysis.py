from alliances.alliance_members import alliance_members
import sys
from os import walk
import networkx as nx
from MG_to_SG_function import MG_to_SG
import pandas as pd

path = sys.argv[1]
save_path = sys.argv[2]

# import community dictionary and extract the most relevant community datas
community_members_over_time = alliance_members['alliance43']

# create dataframe for density and reciprocity 
measures = pd.DataFrame(columns=["day", "density", "reciprocity"])

for day in range(0,30):
	# create dataframe for node centrality measures
	node_measure = pd.DataFrame(columns=["node", "in-degree", "out-degree", "edge-count", "closeness", "betweenness", "pagerank"])
	# extract the meber of that date
	community_members = community_members_over_time[day]

	# read the multigraph of that day
	M = nx.read_graphml(path + "messages-timestamped-2009-12-" + str(day+1) + ".graphml")
	#M = nx.read_graphml(path + "trades-timestamped-2009-12-" + str(day+1) + ".graphml")
	# convert the MG in a SG
	G = MG_to_SG(M)

	tmp = G.subgraph(community_members)
	# create a copy (otherwise G cannot be modified)
	SG = nx.DiGraph(tmp)
	# iterate over members
	for n in community_members:
		# add node if not present in the original graph
		# this could happen if in that day the player was offline
		if n not in SG.nodes:
			SG.add_node(n)

	# compute measuers on the sub-graph
	density = nx.density(SG)
	reciprocity = nx.overall_reciprocity(SG)
	measures.loc[len(measures)] = [day+1, density, reciprocity]

	in_degree = SG.in_degree(weight = "weight")
	out_degree = SG.out_degree(weight = "weight")
	edge_count = SG.degree(weight = "weight")
	closeness = nx.closeness_centrality(SG)
	betweenness = nx.betweenness_centrality(SG, normalized=True, weight="weight")
	pagerank = nx.pagerank(SG, weight = "weight")

	for node in community_members:
		node_measure.loc[len(node_measure)] = [node, in_degree[node], out_degree[node], edge_count[node], closeness[node], betweenness[node], pagerank[node]]

	node_measure.to_csv(save_path + "/messages_most_relevant_community_centrality" + str(day + 1) + ".csv", index=False)

measures.to_csv(save_path + "/messages_most_relevant_community_density_reciprocity.csv", index=False)
