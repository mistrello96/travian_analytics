import sys
from os import walk
import networkx as nx
from MG_to_SG_function import MG_to_SG
import pandas as pd
import numpy as np

path = sys.argv[1]

activity = pd.DataFrame(columns=["day", "nodes", "edges"])

for day in range(0,30):
	M = nx.read_graphml(path + "trades-timestamped-2009-12-" + str(day + 1) + ".graphml")
	print(len(M.nodes))
	print(len(M.edges))

	activity.loc[len(activity)] = [day + 1, len(M.nodes), len(M.edges)]

activity.to_csv("activity.csv", index=False)