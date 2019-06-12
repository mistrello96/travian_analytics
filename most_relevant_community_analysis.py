from alliances.alliance_members import alliance_members
import sys
import networkx as nx
from MG_to_SG_function import MG_to_SG
import pandas as pd
import numpy as np
import re

path = sys.argv[1]
save_path = sys.argv[2]

f = path.split('/')
edge_type = re.search('(\w*)-gml', f[-2], re.IGNORECASE).group(1)

# import community dictionary and extract the most relevant community datas
community_members_over_time = alliance_members['alliance43']

# create dataframe for density and reciprocity 
measures = pd.DataFrame(columns=["day", "density", "reciprocity"])

community_set = set()
for x in community_members_over_time:
	community_set = community_set.union(x)

# node_centrality over time
ncov = dict()
for node in community_set:
	ncov[node] = {"indegree" : list(), "outdegree" : list(), "edgecount" : list(), "closeness" : list(), "betweenness" : list(), "pagerank" : list()}

for day in range(0,30):
	# create dataframe for node centrality measures
	node_measure = pd.DataFrame(columns=["node", "in-degree", "out-degree", "edge-count", "closeness", "betweenness", "pagerank"])
	# extract the meber of that date
	community_members = community_members_over_time[day]

	# read the multigraph of that day
	M = nx.read_graphml(path + "{}-timestamped-2009-12-".format(edge_type) + str(day + 1) + ".graphml")
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

	# compute aggregate measuers on the sub-graph
	density = nx.density(SG)
	reciprocity = nx.overall_reciprocity(SG)
	measures.loc[len(measures)] = [day + 1, density, reciprocity]

	# compute degreee and centralities
	indegree = SG.in_degree(weight = "weight")
	outdegree = SG.out_degree(weight = "weight")
	edgecount = SG.degree(weight = "weight")
	closeness = nx.closeness_centrality(SG)
	betweenness = nx.betweenness_centrality(SG, normalized=True, weight="weight")
	pagerank = nx.pagerank(SG, weight = "weight")

	# iterate over community node
	for node in community_members:
		# save the info
		node_measure.loc[len(node_measure)] = [node, indegree[node], outdegree[node], edgecount[node], closeness[node], betweenness[node], pagerank[node]]
		# store the info of the mean and std measures
		ncov[node]["indegree"].append(indegree[node])
		ncov[node]["outdegree"].append(outdegree[node])
		ncov[node]["edgecount"].append(edgecount[node])
		ncov[node]["closeness"].append(closeness[node])
		ncov[node]["betweenness"].append(betweenness[node])
		ncov[node]["pagerank"].append(pagerank[node])
	# save to file the centrality info
	node_measure.to_csv(save_path + "/{}_most_relevant_community_centrality".format(edge_type) + str(day + 1) + ".csv", index = False)

# save to file density and reciprocity
measures.to_csv(save_path + "/{}_most_relevant_community_density_reciprocity.csv".format(edge_type, index=False))

# create the dataframe for mean and std measures
aggregate_measure = pd.DataFrame(columns=["node", "in-degree-mean", "in-degree-std", "out-degree-mean", "out-degree-std", "edge-count-mean", "edge-count-std",  "closeness-mean", "closeness-std", "betweenness-mean", "betweenness-std", "pagerank-mean", "pagerank-std"])

# compute mean and std for the stored data
for node in community_set:
	aggregate_measure.loc[len(aggregate_measure)] = [node, np.mean(ncov[node]["indegree"]), np.std(ncov[node]["indegree"]), np.mean(ncov[node]["outdegree"]), np.std(ncov[node]["outdegree"]),
	np.mean(ncov[node]["edgecount"]), np.std(ncov[node]["edgecount"]), np.mean(ncov[node]["closeness"]), np.std(ncov[node]["closeness"]), 
	np.mean(ncov[node]["betweenness"]), np.std(ncov[node]["betweenness"]), np.mean(ncov[node]["pagerank"]), np.std(ncov[node]["pagerank"])]

aggregate_measure.to_csv(save_path + "/{}_most_relevant_community_node_centrality.csv".format(edge_type), index = False)