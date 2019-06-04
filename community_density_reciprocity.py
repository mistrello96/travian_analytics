from alliances.alliance_members import alliance_members
import pandas as pd
import sys
from os import walk
import networkx as nx
from MG_to_SG_function import MG_to_SG

path = sys.argv[1]
save_path = sys.argv[2]
zeros = pd.DataFrame(columns=["day", "zero_percentage"])
# iterate over days
for time in range (0, 30):
	# read the corrispondent graph
	#M = nx.read_graphml(path + "trades-timestamped-2009-12-" + str(time+1) + ".graphml")
	M = nx.read_graphml(path + "messages-timestamped-2009-12-" + str(time+1) + ".graphml")
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
				counter_density += 1
	zeros.loc[len(zeros)] = [time+1, counter_density / counter_community]
	res.to_csv(save_path + "/messages_community_density_reciprocity" + str(time + 1) + ".csv", index=False)
zeros.to_csv(save_path + "/messages_zeroes_percentage.csv", index=False)