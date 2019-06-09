from alliances.alliance_members import alliance_members
import pandas as pd 

df = pd.DataFrame(columns=["number_of_registerd_community", "number_of_relevant_community"])

# iterate over days
for day in range (0, 30):
	total = 0
	relevant = 0
	# iterate over alliances
	for alliance in alliance_members:
		# if not empty, total ++
		if alliance_members[alliance][day] != set() and alliance_members[alliance][day] != '':
			total +=1
			# if > 9, relevant ++
			if len (alliance_members[alliance][day]) > 9:
				relevant +=1
	df.loc[len(df)] = [total, relevant]

df.to_csv("community_distribution.csv", index=False)