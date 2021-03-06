from alliances.alliance_members import alliance_members
import pandas as pd
import sys
import networkx as nx
from MG_to_SG_function import MG_to_SG
import re

path = sys.argv[1]
save_path = sys.argv[2]

f = path.split('/')
edge_type = re.search('(\w*)-gml', f[-2], re.IGNORECASE).group(1)

# number of community with denisty = 0
zeros = pd.DataFrame(columns=["day", "zero_percentage"])
# iterate over days
for time in range (0, 30):
	# read the corrispondent graph
	M = nx.read_graphml(path + "{}-timestamped-2009-12-".format(edge_type) + str(time + 1) + ".graphml")
	G = MG_to_SG(M)

	# create output dataframe
	res = pd.DataFrame(columns=["alliance_name", "density", "reciprocity"])
	# iterate over alliances
	counter_density = 0
	counter_community = 0
	for alliance in alliance_members:
		# extract communities members
		community = list((alliance_members[alliance][time]))
		# consider only relevant communities
		if (len(community) > 9):
			counter_community += 1
			# extract the induced graph
			tmp = G.subgraph(community)
			# create a copy (otherwise G cannot be modified)
			SG = nx.DiGraph(tmp)
			# iterate over members
			for n in community:
				# add node if not present in the original graph
				# this could happen if in that day the player was offline
				if n not in SG.nodes:
					SG.add_node(n)
			# compute measures
			# if one of the measures fail, put it at 0
			density = 0
			try:
				density = nx.density(SG)
			except:
				pass
			reciprocity = 0
			try:
				reciprocity = nx.overall_reciprocity(SG)
			except:
				pass
			res.loc[len(res)] = [alliance, density, reciprocity]
			if density == 0:
				# count +1 of community with 0 density
				counter_density += 1
	zeros.loc[len(zeros)] = [time+1, counter_density / counter_community]
	res.to_csv(save_path + "/{}_community_density_reciprocity".format(edge_type) + str(time + 1) + ".csv", index = False)
zeros.to_csv(save_path + "/{}_zeroes_percentage.csv".format(edge_type), index = False)