from alliances.alliance_members import alliance_members
import pandas as pd 

# import alliances
df = pd.DataFrame(alliance_members)

res = list()
# iterate over time
for i in range(0, 30):
	# comunt all community and relevant (>9) communities
	comm = 0
	relevant = 0
	# extract members of a community
	elements = df.loc[i].values
	for e in elements:
		comm +=1
		if (len(e) > 9):
			relevant += 1
	res.append([comm, relevant])
print(res)