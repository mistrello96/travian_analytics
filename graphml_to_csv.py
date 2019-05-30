import networkx as nx
import sys
from os import walk

path = sys.argv[1]
save_path = sys.argv[2]

for x in range(0,30):
	M = nx.read_graphml(path + "trades-timestamped-2009-12-" + str(x+1) + ".graphml")
	nx.write_edgelist(M, save_path + "trades-timestamped-2009-12-" + str(x+1) + ".csv", comments='#', delimiter = ",")