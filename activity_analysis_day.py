import sys
import networkx as nx
from datetime import datetime
from collections import Counter
import pandas as pd

# import path to the 30-days folder
attacks = sys.argv[1]
messages = sys.argv[2]
trades = sys.argv[3]
# set day treshold to identify number of player unactive after that day
treshold = sys.argv[4]

# set of active player before that day
before_treshold = set()
for day in range(0, int(treshold) - 1):

	A = nx.read_graphml(attacks + "attacks-timestamped-2009-12-" + str(day+1) + ".graphml")
	M = nx.read_graphml(messages + "messages-timestamped-2009-12-" + str(day+1) + ".graphml")
	T = nx.read_graphml(trades + "trades-timestamped-2009-12-" + str(day+1) + ".graphml")
	before_treshold = before_treshold.union(A.nodes())
	before_treshold = before_treshold.union(M.nodes())
	before_treshold = before_treshold.union(T.nodes())

# set of active player after that day
after_treshold = set()
for day in range (int(treshold) - 1 , 30):
	A = nx.read_graphml(attacks + "attacks-timestamped-2009-12-" + str(day+1) + ".graphml")
	M = nx.read_graphml(messages + "messages-timestamped-2009-12-" + str(day+1) + ".graphml")
	T = nx.read_graphml(trades + "trades-timestamped-2009-12-" + str(day+1) + ".graphml")
	after_treshold = after_treshold.union(A.nodes())
	after_treshold = after_treshold.union(M.nodes())
	after_treshold = after_treshold.union(T.nodes())

# set difference
print("People delta " + str(len(before_treshold - after_treshold)))

# activity per hour distribution of the selected day
# see activity_per_hour file for further info
res_att= list()
res_mes = list()
res_tra = list()

M = nx.read_graphml(attacks + "attacks-timestamped-2009-12-" + treshold + ".graphml")
times = nx.get_edge_attributes(M, 'edgetime')
for element in times:
	hour = int (datetime.utcfromtimestamp(times[element]).strftime("%H"))
	res_att.append(hour)

M = nx.read_graphml(messages + "messages-timestamped-2009-12-" + treshold + ".graphml")
times = nx.get_edge_attributes(M, 'edgetime')
for element in times:
	hour = int (datetime.utcfromtimestamp(times[element]).strftime("%H"))
	res_mes.append(hour)

M = nx.read_graphml(trades + "trades-timestamped-2009-12-" + treshold + ".graphml")
times = nx.get_edge_attributes(M, 'edgetime')
for element in times:
	hour = int (datetime.utcfromtimestamp(times[element]).strftime("%H"))
	res_tra.append(hour)

output = pd.DataFrame(columns = ["hour", "attacks", "messages", "trades", "total"])
count_attacks = Counter(res_att)
count_messages = Counter(res_mes)
count_trades = Counter(res_tra)
count_all = Counter([item for sublist in [res_att, res_mes, res_tra] for item in sublist])

for x in range (0, 24):
	output.loc[len(output)] = [x, count_attacks[x], count_messages[x], count_trades[x], count_all[x]]

output.to_csv("day" + treshold + "_activity_per_hour.csv", index = False)