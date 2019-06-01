import numpy as np 
# import alliance dictionary
from alliances.alliance_members import alliance_members

# create a dictionary
alliance_count = dict()

# count the members of each alliance for each day
for alliance in alliance_members:
	lenght = list()
	for day_alliance in alliance_members[alliance]:
		lenght.append(len(day_alliance))
	alliance_count[alliance] = lenght

alliance_measures = dict()

# comupte mean and sd of the number of members of each alliance
for alliance in alliance_count:
	alliance_measures[alliance] = [np.mean(alliance_count[alliance]), np.std(alliance_count[alliance])]

# sort the community for the mean of the members over 30 days
sorted_by_mean = sorted(alliance_measures.values(), key=lambda tup: tup[0])

# extract mean and sd of the most relevant community
print(sorted_by_mean[-1])

# extract the name of the most relevant community
print([k for k,v in alliance_measures.items() if v == sorted_by_mean[-1]][0])
print([k for k,v in alliance_measures.items() if v == sorted_by_mean[-2]][0])
print([k for k,v in alliance_measures.items() if v == sorted_by_mean[-3]][0])
print([k for k,v in alliance_measures.items() if v == sorted_by_mean[-4]][0])
print([k for k,v in alliance_measures.items() if v == sorted_by_mean[-5]][0])
print([k for k,v in alliance_measures.items() if v == sorted_by_mean[-6]][0])