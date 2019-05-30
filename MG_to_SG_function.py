import networkx as nx

def MG_to_SG (M):
	# remove the attribute timestamp, not usefull for our analisis
	try:
		for n1, n2, d in M.edges(data=True):
			d.pop('timestamp', None)
	except:
		pass

	# create weighted graph from M
	G = nx.DiGraph()
	# iterate over edges
	# this can trow an exception if type attribute is not present
	try:
		for u,v,data in M.edges(data=True):
			# create attribute weight if not present
		    w = data['weight'] if 'weight' in data else 1.0
		    # copy the edge type
		    # this can trow an exception if the attribute is not present
		    t = data['type']
		    # accumulate the weights if present
		    if G.has_edge(u,v):
		        G[u][v]['weight'] += w
		    else:
		        G.add_edge(u, v, weight=w, type = t)
	except:
		for u,v,data in M.edges(data=True):
			# create attribute weight if not present
		    w = data['weight'] if 'weight' in data else 1.0
		    # accumulate the weights if present
		    if G.has_edge(u,v):
		        G[u][v]['weight'] += w
		    else:
		        G.add_edge(u, v, weight=w)
	return G