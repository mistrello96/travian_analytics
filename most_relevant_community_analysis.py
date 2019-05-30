from alliances.alliance_members import alliance_members
import sys
from os import walk
import networkx as nx
from MG_to_SG_function import MG_to_SG

# import community dictionary and extract the most relevant community datas
community_members_over_time = alliance_members['alliance43']

for day in range(0,30):
	# extract the meber of that date
	community_members = community_members_over_time[day]

	# read the multigraph of that day
	#M = nx.read_graphml(path + "messages-timestamped-2009-12-" + str(day+1) + ".graphml")
	M = nx.read_graphml(path + "trades-timestamped-2009-12-" + str(day+1) + ".graphml")
	# convert the MG in a SG
	G = MG_to_SG(M)
