from alliances.alliance_members import alliance_members
import pandas as pd 

df = pd.DataFrame(alliance_members)
#print(df)
res = list()
for i in range(0, 30):
	counter0 = 0
	elements = df.loc[i].values
	for e in elements:
		if (len(e) > 9):
			counter += 1
	res.append(counter)
print(res)