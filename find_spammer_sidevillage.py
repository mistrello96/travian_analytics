from alliances.alliance_members import alliance_members
import sys
import networkx as nx
import pandas as pd

messages = sys.argv[1]
trades = sys.argv[2]

MG_messages = nx.read_graphml(messages)
MG_trades = nx.read_graphml(trades)

m_in_degree = MG_messages.in_degree(weight = "weight")
m_out_degree = MG_messages.out_degree(weight = "weight")
t_in_degree = MG_trades.in_degree(weight = "weight")
t_out_degree = MG_trades.out_degree(weight = "weight")

nx.set_node_attributes(MG_messages, m_in_degree, name="in-degree")
nx.set_node_attributes(MG_messages, m_out_degree, name="out-degree")
nx.set_node_attributes(MG_trades, t_in_degree, name="in-degree")
nx.set_node_attributes(MG_trades, t_out_degree, name="out-degree")

community_set = set()
for alliance in alliance_members:
	for t in range(0, 30):
		if len(alliance_members[alliance][t]) > 9:
			community_set = community_set.union(alliance_members[alliance][t])

all_nodes = set(MG_messages.nodes).union(set(MG_trades.nodes))

possible_spammer = all_nodes - community_set

res = pd.DataFrame(columns=["node", "message_in", "message_out", "trade_in", "trade_out"])

for n in possible_spammer:

	if n in MG_messages.nodes:
		if n in MG_trades.nodes:
				if (m_in_degree[n] == 0 and m_out_degree[n] > 30) or ((m_in_degree[n] != 0 and m_out_degree[n] / m_in_degree[n]) > 10):
					print(n + " is a possible spammer");
				if (t_in_degree[n] == 0 and t_in_degree[n] > 15) or ((t_in_degree[n] != 0 and t_out_degree[n] / t_in_degree[n]) > 5):
					print(n + " is a possible side village")
		else:
				if (m_in_degree[n] == 0 and m_out_degree[n] > 30) or ((m_in_degree[n] != 0 and m_out_degree[n] / m_in_degree[n]) > 10):
					print(n + " is a possible spammer");
	else:
		if (t_in_degree[n] == 0 and t_in_degree[n] > 15) or ((t_in_degree[n] != 0 and t_out_degree[n] / t_in_degree[n]) > 5):
			print(n + " is a possible side village")

	if n in MG_messages.nodes:
		if n in MG_trades.nodes:
			res.loc[len(res)] = [n, m_in_degree[n], m_out_degree[n], t_in_degree[n], t_out_degree[n]]
		else:
			res.loc[len(res)] = [n, m_in_degree[n], m_out_degree[n], 0, 0]
	else:
		res.loc[len(res)] = [n, 0, 0, t_in_degree[n], t_out_degree[n]]
res.to_csv("spammer_side.csv", index=False)