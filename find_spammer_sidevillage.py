from alliances.alliance_members import alliance_members
import sys
import networkx as nx
import pandas as pd

# import path
attacks = sys.argv[1]
messages = sys.argv[2]
trades = sys.argv[3]

# read aggregate graphs
MG_attacks = nx.read_graphml(attacks)
MG_messages = nx.read_graphml(messages)
MG_trades = nx.read_graphml(trades)

# compute degree for each layer
a_out_degree = MG_attacks.out_degree(weight = "weight")
m_in_degree = MG_messages.in_degree(weight = "weight")
m_out_degree = MG_messages.out_degree(weight = "weight")
t_in_degree = MG_trades.in_degree(weight = "weight")
t_out_degree = MG_trades.out_degree(weight = "weight")

# push the info into the node
nx.set_node_attributes(MG_messages, m_in_degree, name="in-degree")
nx.set_node_attributes(MG_messages, m_out_degree, name="out-degree")
nx.set_node_attributes(MG_trades, t_in_degree, name="in-degree")
nx.set_node_attributes(MG_trades, t_out_degree, name="out-degree")

# extract all nodes in a relevat alliance
community_set = set()
for alliance in alliance_members:
	for t in range(0, 30):
		if len(alliance_members[alliance][t]) > 9:
			community_set = community_set.union(alliance_members[alliance][t])

all_nodes = set(MG_messages.nodes).union(set(MG_trades.nodes))

# remove node just found from the possible spammer_side/side
possible_spammer_side = all_nodes - community_set

# create results dataframe
res = pd.DataFrame(columns=["node", "attacks_out","message_in", "message_out", "trade_in", "trade_out"])

# spammer_side set
spammer_side = set()

# iterate over possibele soammer
# a spammer_side is a node with out_deg/in_deg >10 and at least 30 message in message layer
# a side village is a node with out_deg/in_deg > 5 and at least 15 trade in trade layer
for n in possible_spammer_side:
	if n in MG_messages.nodes:
		if n in MG_trades.nodes:
				if (m_in_degree[n] == 0 and m_out_degree[n] > 30) or ((m_in_degree[n] != 0 and m_out_degree[n] / m_in_degree[n]) > 10):
					print(n + " is a possible spammer");
					spammer_side.add(n)
				if (t_in_degree[n] == 0 and t_in_degree[n] > 15) or ((t_in_degree[n] != 0 and t_out_degree[n] / t_in_degree[n]) > 5):
					print(n + " is a possible side village")
					spammer_side.add(n)
		else:
				if (m_in_degree[n] == 0 and m_out_degree[n] > 30) or ((m_in_degree[n] != 0 and m_out_degree[n] / m_in_degree[n]) > 10):
					print(n + " is a possible spammer")
					spammer_side.add(n)
	else:
		if (t_in_degree[n] == 0 and t_in_degree[n] > 15) or ((t_in_degree[n] != 0 and t_out_degree[n] / t_in_degree[n]) > 5):
			print(n + " is a possible side village")
			spammer_side.add(n)

# save info of the spammer_side in a csv
# NOTE: not all of the founfd node are going to be guilty. Still need a human check
for n in spammer_side:
	if n in MG_messages.nodes:
		if n in MG_trades.nodes:
			if n in MG_attacks:
				res.loc[len(res)] = [n, a_out_degree[n],m_in_degree[n], m_out_degree[n], t_in_degree[n], t_out_degree[n]]
			else:
				res.loc[len(res)] = [n, 0,m_in_degree[n], m_out_degree[n], t_in_degree[n], t_out_degree[n]]
			
		else:
			if n in MG_attacks:
				res.loc[len(res)] = [n, a_out_degree[n] ,m_in_degree[n], m_out_degree[n], 0, 0]
			else:
				res.loc[len(res)] = [n, 0 ,m_in_degree[n], m_out_degree[n], 0, 0]
	else:
		if n in MG_attacks:
			res.loc[len(res)] = [n, a_out_degree[n], 0, 0, t_in_degree[n], t_out_degree[n]]
		else:
			res.loc[len(res)] = [n, 0, 0, 0, t_in_degree[n], t_out_degree[n]]
res.to_csv("spammer_side.csv", index=False)