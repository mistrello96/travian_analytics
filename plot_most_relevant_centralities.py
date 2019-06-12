import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def centrality_distribution(centrality):
	df = pd.read_csv("Results/Most_relevant_community_analysis/messages/messages_most_relevant_community_node_centrality.csv")
	plt.figure(figsize = (8, 6), dpi = 300)
	(vs, bins) = np.histogram(df["{}-mean".format(centrality)], bins = 'fd', density = False)
	normed_vs = [v / len(df["{}-mean".format(centrality)]) for v in vs]
	for i in range(len(bins) - 1):
		if normed_vs[i] != 0:
			m = (bins[i] + bins[i + 1]) / 2
			plt.scatter(m, normed_vs[i], marker = '.', color = "black", s = 28)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	if centrality == "pagerank":
		plt.xlabel("PageRank", fontsize = 15)
	else:
		plt.xlabel("{}".format(centrality[0].upper() + centrality[1:]), fontsize = 15)
	plt.ylabel("Distribution", fontsize = 15)
	if centrality == "pagerank":
		plt.title("Average 30-day PageRank distribution")
	else:
		plt.title("Average 30-day {} distribution".format(centrality))
	plt.tight_layout()
	plt.savefig("Results/Most_relevant_community_analysis/messages/images/png/distribution/{}_distribution.png".format(centrality))
	plt.savefig("Results/Most_relevant_community_analysis/messages/images/pdf/distribution/{}_distribution.pdf".format(centrality))
	plt.close()

def centraly_of_each_node_each_day(centrality):
	plt.figure(figsize = (8, 6), dpi = 300)
	for i in range(1, 31):
		df = pd.read_csv("Results/Most_relevant_community_analysis/messages/messages_most_relevant_community_centrality{}.csv".format(i))
		plt.scatter([str(x) for x in df["node"]], df[centrality], marker = '.', color = "black", s = 5)
	plt.xticks(fontsize = 12)
	plt.tick_params(axis = 'x', labelbottom = False)
	plt.yticks(fontsize = 12)
	if centrality == "pagerank":
		plt.ylabel("PageRank", fontsize = 15)
	else:
		plt.ylabel("{}".format(centrality[0].upper() + centrality[1:]), fontsize = 15)
	plt.xlabel("Nodes", fontsize = 15, labelpad = 10)
	if centrality == "pagerank":
		plt.title("PageRank of each node over 30 days")
	else:
		plt.title("{} of each node over 30 days".format(centrality[0].upper() + centrality[1:]), fontsize = 15)
	plt.tight_layout()
	plt.savefig("Results/Most_relevant_community_analysis/messages/images/png/each_node/{}_each_node.png".format(centrality))
	plt.savefig("Results/Most_relevant_community_analysis/messages/images/pdf/each_node/{}_each_node.pdf".format(centrality))

if __name__ == "__main__":
	print("in-degree")
	centrality_distribution("in-degree")
	print("out-degree")
	centrality_distribution("out-degree")
	print("closeness")
	centrality_distribution("closeness")
	print("betweenness")
	centrality_distribution("betweenness")
	print("pagerank")
	centrality_distribution("pagerank")
	
	print("in-degree each node")
	centraly_of_each_node_each_day("in-degree")
	print("out-degree each node")
	centraly_of_each_node_each_day("out-degree")
	print("pagerank each node")
	centraly_of_each_node_each_day("pagerank")
	print("betweenness each node")
	centraly_of_each_node_each_day("betweenness")
	print("closeness each node")
	centraly_of_each_node_each_day("closeness")