from alliances.alliance_members import alliance_members
import numpy as np 

alliance_count = dict()

for alliance in alliance_members:
	lenght = list()
	for day_alliance in alliance_members[alliance]:
		lenght.append(len(day_alliance))
	alliance_count[alliance] = lenght

alliance_measures = dict()

for alliance in alliance_count:
	alliance_measures[alliance] = [np.mean(alliance_count[alliance]), np.std(alliance_count[alliance])]

sorted_by_mean = sorted(alliance_measures.values(), key=lambda tup: tup[0])

print(sorted_by_mean[-1])

print([k for k,v in alliance_measures.items() if v == sorted_by_mean[-1]][0])


'''
means = list()
for element in alliance_measures:
	#print(str(alliance_measures[element][0]) + " " + str(alliance_measures[element][1]))
	means.append(alliance_measures[element][0])

print(sorted(range(len(means)), key=lambda k: means[k], reverse=True))

for x in range (0,5):
	print(means[x])

	'''