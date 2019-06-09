import sys
from os import walk
import networkx as nx
from MG_to_SG_function import MG_to_SG
import pandas as pd
import numpy as np

# read path to 30-days folder
path_att = sys.argv[1]
path_mes = sys.argv[2]
path_tra = sys.argv[3]

# generate dataframes for attacks, messages, trades and sumof them
activity1 = pd.DataFrame(columns=["day", "nodes", "edges"])
activity2 = pd.DataFrame(columns=["day", "nodes", "edges"])
activity3 = pd.DataFrame(columns=["day", "nodes", "edges"])
activity_nodes = pd.DataFrame(columns=["day", "nnodes"])

# iterate over days
for day in range(0,30):
	# read the 3 activity graph
	M1 = nx.read_graphml(path_att + "attacks-timestamped-2009-12-" + str(day + 1) + ".graphml")
	M2 = nx.read_graphml(path_mes + "messages-timestamped-2009-12-" + str(day + 1) + ".graphml")
	M3 = nx.read_graphml(path_tra + "trades-timestamped-2009-12-" + str(day + 1) + ".graphml")

	# find wich node were present that day
	active_nodes_set = set()
	active_nodes_set.update(M1.nodes)
	active_nodes_set.update(M2.nodes)
	active_nodes_set.update(M3.nodes)

	# save number of activity performed
	activity1.loc[len(activity1)] = [day + 1, len(M1.nodes), len(M1.edges)]
	activity2.loc[len(activity2)] = [day + 1, len(M2.nodes), len(M2.edges)]
	activity3.loc[len(activity3)] = [day + 1, len(M3.nodes), len(M3.edges)]
	activity_nodes.loc[len(activity_nodes)] = [day + 1, len (active_nodes_set)]

# save to filr
activity1.to_csv("attacks_activity.csv", index=False)
activity2.to_csv("messages_activity.csv", index=False)
activity3.to_csv("trades_activity.csv", index=False)
activity_nodes.to_csv("nodes_activity.csv",index=False)