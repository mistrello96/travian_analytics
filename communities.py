from collections import Counter

def read_alliances(t):
	communities_t = []
	file = "./datas_paper/Dataset/communities/communities-2009-12-{}.txt".format(t)
	with open(file) as f:
		communities_t = [c.rstrip().split() for c in f.readlines()]
	return communities_t

def add_old_alliance_tmp(name, tmp):
	if name in tmp: # if there is already an alliance who wants that name
		tmp[name].append(set(c))
		return
	tmp[name] = [set(c)]

def update_nodes_alliance(nodes_alliance, alliance_set, alliance_name, t):
	for m in alliance_set:
		if m in nodes_alliance: # if he was in a community before
			nodes_alliance[m].append(alliance_name)
		else:
			nodes_alliance[m] = [''] * (t - 1)
			nodes_alliance[m].append(alliance_name)

if __name__ == "__main__":
	nodes_alliance = {} # key = label of node, value = list of alliance he belongs to at time t
	alliance_members = {} # key = name of alliance, value = list of sets of node of the ally at time t
	alliance_id = 0

	communities_t = read_alliances(1)
	for c in communities_t:
		alliance_name = "alliance{}".format(alliance_id)
		alliance_members[alliance_name] = [set(c)]
		for m in c:
			nodes_alliance[m] = [alliance_name]
		alliance_id += 1

	for t in range(2, 31):
		communities_t = read_alliances(t)
		tmp = {} # key = alliance name, value = candidate set for that name
		for c in communities_t:
			votes = Counter([nodes_alliance[m][-1] for m in c if m in nodes_alliance and nodes_alliance[m][-1] != ''])

			if not votes: # if votes is empty, all nodes are in their first alliance
				alliance_name = "alliance{}".format(alliance_id)
				tmp[alliance_name] = [set(c)]
				alliance_id += 1
				continue

			most_common_votes = votes.most_common(2) # most_common returns a list of tuples: (name, votes)
			# please note that if most_common receives a parameter larger than the length of the counter,
			# only the entire list will be returned. e.g., counter is Counter({"foo": 42}), 
			# counter.most_common(3) -> [("foo", 42)] 
			if len(most_common_votes) > 1:
				if most_common_votes[0][1] == most_common_votes[1][1]: # if votes are even -> new name
					alliance_name = "alliance{}".format(alliance_id)
					tmp[alliance_name] = [set(c)]
					alliance_id += 1
				else:
					add_old_alliance_tmp(most_common_votes[0][0], tmp)
			else:
				add_old_alliance_tmp(most_common_votes[0][0], tmp)

		# resolve name conflicts
		for alliance_name in tmp:
			if len(tmp[alliance_name]) == 1: # no conflict
				if alliance_name in alliance_members: # if that name already exists
					alliance_members[alliance_name].append(tmp[alliance_name][0])
					update_nodes_alliance(nodes_alliance, tmp[alliance_name][0], alliance_name, t)
				else:
					alliance_members[alliance_name] = [set()] * (t - 1)
					alliance_members[alliance_name].append(tmp[alliance_name][0])
					update_nodes_alliance(nodes_alliance, tmp[alliance_name][0], alliance_name, t)
			else: # if there is conflict
				index_intersection = [] # list of tuples (index, cardinality of intersection)
				for i in range(len(tmp[alliance_name])):
					index_intersection.append((i, len(tmp[alliance_name][i].intersection(alliance_members[alliance_name][-1]))))
				highest_intersection = max(index_intersection, key = lambda x: x[1])
				for i in range(len(tmp[alliance_name])):
					if i == highest_intersection[0]:
						alliance_members[alliance_name].append(tmp[alliance_name][i])
						update_nodes_alliance(nodes_alliance, tmp[alliance_name][i], alliance_name, t)
						continue
					new_name = "alliance{}".format(alliance_id)
					alliance_members[new_name] = [set()] * (t - 1)
					alliance_members[new_name].append(tmp[alliance_name][i])
					update_nodes_alliance(nodes_alliance, tmp[alliance_name][i], new_name, t)
					alliance_id += 1

		# if some member was in a community before but not now, we need to track it
		# in the same way the communities
		for m in nodes_alliance:
			if len(nodes_alliance[m]) != t:
				nodes_alliance[m].append('')
		for a in alliance_members:
			if len(alliance_members[a]) != t:
				alliance_members[a].append(set())

	# Now, we have two dictionaries:
	
	# alliance_members: for each community name (key) we have a list representing the members of the alliances at time t,
	# if they have no members at time t an empty set is used
	# key = name of alliance, value = list of sets of node of the ally at time t
	
	# nodes_alliance: for each node the alliance is part of at time t, if he is not in any alliance -> value for time t is ''
	# key = label of node, value = list of alliance he belongs to at time t
	
	# we save them on files and we elabrate them in other scripts!

	nodes_alliance_file = open("alliances/nodes_alliance.py", 'w')
	nodes_alliance_file.writelines(["nodes_alliance = ", str(nodes_alliance), '\n'])
	nodes_alliance_file.close()

	alliance_members_file = open("alliances/alliance_members.py", 'w')
	alliance_members_file.writelines(["alliance_members = ", str(alliance_members), '\n'])
	alliance_members_file.close()
