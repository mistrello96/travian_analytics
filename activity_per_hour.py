import sys
import networkx as nx
from datetime import datetime
from collections import Counter
import pandas as pd

# read path to 30-days folder
path_att = sys.argv[1]
path_mes = sys.argv[2]
path_tra = sys.argv[3]

# list of timestamps for each activity
res_att= list()
res_mes = list()
res_tra = list()

# iterate over days
for day in range(0,30):
	# read graph
	M = nx.read_graphml(path_att + "attacks-timestamped-2009-12-" + str(day + 1) + ".graphml")
	# read all timestamps present
	times = nx.get_edge_attributes(M, 'edgetime')
	# extract for each timestamp the hour and push it in the attack list
	for element in times:
		hour = int (datetime.utcfromtimestamp(times[element]).strftime("%H"))
		res_att.append(hour)

	M = nx.read_graphml(path_mes + "messages-timestamped-2009-12-" + str(day + 1) + ".graphml")
	times = nx.get_edge_attributes(M, 'edgetime')
	for element in times:
		hour = int (datetime.utcfromtimestamp(times[element]).strftime("%H"))
		res_mes.append(hour)

	M = nx.read_graphml(path_tra + "trades-timestamped-2009-12-" + str(day + 1) + ".graphml")
	times = nx.get_edge_attributes(M, 'edgetime')
	for element in times:
		hour = int (datetime.utcfromtimestamp(times[element]).strftime("%H"))
		res_tra.append(hour)

# count how many timestamp for each hour
output = pd.DataFrame(columns = ["hour", "attacks", "messages", "trades", "total"])
count_attacks = Counter(res_att)
count_messages = Counter(res_mes)
count_trades = Counter(res_tra)
count_all = Counter([item for sublist in [res_att, res_mes, res_tra] for item in sublist])

for x in range (0, 24):
	output.loc[len(output)] = [x, count_attacks[x], count_messages[x], count_trades[x], count_all[x]]

# save to file
output.to_csv("activity_per_hour.csv", index = False)