import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# color mapping: red = attack, mesages = blue, trade = green

def plot_clustering(edge_type, color):
	df = pd.read_csv("Results/Aggregate/{}_clustering_coefficient.csv".format(edge_type))
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.yscale("log")	
	(vs, bins) = np.histogram(df["clustering_coefficient"], bins = 'fd', density = False) #sturges does not work so well Hyndman, R.J. (1995), fd = Freedman Diaconis Freedman, David; Diaconis, Persi (December 1981)
	normed_vs = [v / len(df["clustering_coefficient"]) for v in vs]
	for i in range(len(bins) - 1):
		m = (bins[i] + bins[i + 1]) / 2
		plt.scatter(m, normed_vs[i], marker = '.', color = color, s = 10)
	plt.xlim(left = 10 ** (-10))
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Clustering coefficient", fontsize = 15)
	plt.ylabel("Probability", fontsize = 15)
	plt.title("Distribution of {} clustering_coefficient".format(edge_type))
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/clustering_distribution/{}.png".format(edge_type))
	plt.savefig("Results/Aggregate/images/clustering_distribution/{}.pdf".format(edge_type))
		
def plot_attacks_in_degree():
	df = pd.read_csv("Results/Aggregate/attacks_degree.csv")
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.yscale("log")
	(vs, bins) = np.histogram(df["in-degree"], bins = 'fd', density = False) #sturges does not work so well Hyndman, R.J. (1995), fd = Freedman Diaconis Freedman, David; Diaconis, Persi (December 1981)
	normed_vs = [v / len(df["in-degree"]) for v in vs]
	for i in range(len(bins) - 1):
		m = (bins[i] + bins[i + 1]) / 2
		plt.scatter(m, normed_vs[i], marker = '.', color = "red", s = 10)
	plt.xlim(left = -10)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("In-degree", fontsize = 15)
	plt.ylabel("Probability", fontsize = 15)
	plt.title("Distribution of attacks out-degree in aggregate graph")
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/attacks_in_degree.png")
	plt.savefig("Results/Aggregate/images/degree/attacks_in_degree.pdf")
	

def plot_attacks_out_degree():
	df = pd.read_csv("Results/Aggregate/attacks_degree.csv")
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.yscale("log")
	no_outliers = [x for x in df["out-degree"] if x < 3001] # 3e+03 means 100 attacks per day -> we consider them outliers
	# print((len(no_outliers) / len(df["out-degree"])) * 100) # percentage of datas remaining = 99.09% if 3000 is considered
	(vs, bins) = np.histogram(no_outliers, bins = 'fd', density = False) #sturges does not work so well Hyndman, R.J. (1995), fd = Freedman Diaconis Freedman, David; Diaconis, Persi (December 1981)
	normed_vs = [v / len(df["out-degree"]) for v in vs]
	for i in range(len(bins) - 1):
		m = (bins[i] + bins[i + 1]) / 2
		plt.scatter(m, normed_vs[i], marker = '.', color = "red", s = 10)
	plt.xlim(left = -10)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Out-degree", fontsize = 15)
	plt.ylabel("Probability", fontsize = 15)
	plt.title("Distribution of attacks out-degree in aggregate graph")
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/attacks_out_degree.png")
	plt.savefig("Results/Aggregate/images/degree/attacks_out_degree.pdf")

	plt.figure(figsize = (8, 6), dpi = 300)
	#plt.yscale("log")
	outliers = [x for x in df["out-degree"] if x > 3000] # 3e+03 means 100 attacks per day
	(vs, bins) = np.histogram(outliers, bins = 'fd') #sturges does not work so well Hyndman, R.J. (1995), fd = Freedman Diaconis Freedman, David; Diaconis, Persi (December 1981)
	for i in range(len(bins) - 1):
		m = (bins[i] + bins[i + 1]) / 2
		plt.scatter(m, vs[i], marker = '.', color = "red", s = 10)
	# plt.xlim([2990, max(outliers) + 50])
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Out-degree", fontsize = 15)
	plt.ylabel("Number", fontsize = 15)
	plt.title("Distribution of attacks out-degree in aggregate graph (Outliers)")
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/attacks_out_degree_outliers.png")
	plt.savefig("Results/Aggregate/images/degree/attacks_out_degree_outliers.pdf")

def plot_attacks_total_degree():
	df = pd.read_csv("Results/Aggregate/attacks_degree.csv")
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.yscale("log")
	no_outliers = df.loc[df["out-degree"] < 3001] # removal of outliers
	(vs, bins) = np.histogram(no_outliers["edge-count"], bins = 'fd', density = False)
	normed_vs = [v / len(no_outliers["edge-count"]) for v in vs]
	for i in range(len(bins) - 1):
		m = (bins[i] + bins[i + 1]) / 2
		plt.scatter(m, normed_vs[i], marker = '.', color = "red", s = 10)
	plt.xlim(left = -10)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Total degree", fontsize = 15)
	plt.ylabel("Probability", fontsize = 15)
	plt.title("Distribution of attacks total degree in aggregate graph")
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/attacks_total_degree.png")
	plt.savefig("Results/Aggregate/images/degree/attacks_total_degree.pdf")

	plt.figure(figsize = (8, 6), dpi = 300)
	no_outliers = df.loc[df["out-degree"] > 3000] # removal of outliers
	(vs, bins) = np.histogram(no_outliers["edge-count"], bins = 'fd', density = False)
	for i in range(len(bins) - 1):
		m = (bins[i] + bins[i + 1]) / 2
		plt.scatter(m, vs[i], marker = '.', color = "red", s = 10)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Total degree", fontsize = 15)
	plt.ylabel("Number", fontsize = 15)
	plt.title("Distribution of total degree in aggregate graph")
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/attacks_total_degree_outliers.png")
	plt.savefig("Results/Aggregate/images/degree/attacks_total_degree_outliers.pdf")	

def plot_degrees_datas_no_outliers(edge_type, color): # for messages and trades
	df = pd.read_csv("Results/Aggregate/{}_degree.csv".format(edge_type))
	for l in ["in-degree", "out-degree", "edge-count"]:
		plt.figure(figsize = (8, 6), dpi = 300)
		plt.yscale("log")	
		(vs, bins) = np.histogram(df[l], bins = 'fd', density = False) #sturges does not work so well Hyndman, R.J. (1995), fd = Freedman Diaconis Freedman, David; Diaconis, Persi (December 1981)
		normed_vs = [v / len(df[l]) for v in vs]
		for i in range(len(bins) - 1):
			m = (bins[i] + bins[i + 1]) / 2
			plt.scatter(m, normed_vs[i], marker = '.', color = color, s = 10)
		plt.xlim(left = -10)
		plt.xticks(fontsize = 12)
		plt.yticks(fontsize = 12)
		# x label if
		if l == "in-degree":
			plt.xlabel("In-degree", fontsize = 15)
		if l == "out-degree":
			plt.xlabel("Out-degree", fontsize = 15)
		if l == "edge-count":
			plt.xlabel("Total degree", fontsize = 15)
		plt.ylabel("Probability", fontsize = 15)
		# title if
		if l == "edge-count":
			plt.title("Distribution of {} {} in aggregate graph".format(edge_type, "total degree"))
		else:	
			plt.title("Distribution of {} {} in aggregate graph".format(edge_type, l))
		plt.tight_layout()
		# save if
		if l == "in-degree":
			plt.savefig("Results/Aggregate/images/degree/{}_in_degree.png".format(edge_type))
			plt.savefig("Results/Aggregate/images/degree/{}_in_degree.pdf".format(edge_type))
		if l == "out-degree":
			plt.savefig("Results/Aggregate/images/degree/{}_out_degree.png".format(edge_type))
			plt.savefig("Results/Aggregate/images/degree/{}_out_degree.pdf".format(edge_type))
		if l == "edge-count":
			plt.savefig("Results/Aggregate/images/degree/{}_total_degree.png".format(edge_type))
			plt.savefig("Results/Aggregate/images/degree/{}_total_degree.pdf".format(edge_type))

def plot_messages_out_degree_strictly_under(value):
	df = pd.read_csv("Results/Aggregate/messages_degree.csv")
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.yscale("log")
	no_outliers = [x for x in df["out-degree"] if x < value]
	(vs, bins) = np.histogram(no_outliers, bins = 'fd', density = False)
	normed_vs = [v / len(no_outliers) for v in vs]
	for i in range(len(bins) - 1):
		m = (bins[i] + bins[i + 1]) / 2
		plt.scatter(m, normed_vs[i], marker = '.', color = "blue", s = 10)
	plt.xlim(left = -10)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Out-degree", fontsize = 15)
	plt.ylabel("Probability", fontsize = 15)
	plt.title("Distribution of messages out-degree in aggregate graph (values under {})".format(value))
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/messages_out_degree{}.png".format(value))
	plt.savefig("Results/Aggregate/images/degree/messages_out_degree{}.pdf".format(value))

def jointplot_degrees(edge_type, color):
	df = pd.read_csv("Results/Aggregate/{}_degree.csv".format(edge_type))
	g = sns.jointplot(x = "out-degree", y = "in-degree", data = df, color = color, height = 8)
	g.ax_joint.set_xlabel("Out-degree", fontsize = 15)
	g.ax_joint.set_ylabel("In-degree", fontsize = 15)
	g.fig.suptitle("Jointplot {} degree".format(edge_type), fontsize = 20)
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/{}_jointplot.png".format(edge_type))
	plt.savefig("Results/Aggregate/images/degree/{}_jointplot.pdf".format(edge_type))

def custom_jointplot_degrees(edge_type1, parameter1, edge_type2, parameter2, color):
	df1 = pd.read_csv("Results/Aggregate/{}_degree.csv".format(edge_type1))
	df2 = pd.read_csv("Results/Aggregate/{}_degree.csv".format(edge_type2))
	g = sns.jointplot(x = df1[parameter1], y = df2[parameter2], color = color, height = 8)
	g.ax_joint.set_xlabel("Out-degree", fontsize = 15)
	g.ax_joint.set_ylabel("In-degree", fontsize = 15)
	g.fig.suptitle("Jointplot {}-{} vs {}-{} degree".format(edge_type1, parameter1, edge_type2, parameter2), fontsize = 20)
	plt.tight_layout()
	plt.savefig("Results/Aggregate/images/degree/{}_{}_vs_{}_{}_jointplot.png".format(edge_type1, parameter1, edge_type2, parameter2))
	plt.savefig("Results/Aggregate/images/degree/{}_{}_vs_{}_{}_jointplot.pdf".format(edge_type1, parameter1, edge_type2, parameter2))	

if __name__ == "__main__":
	'''
	print("clustering attacks")
	plot_clustering("attacks", "red")
	print("clustering messages")
	plot_clustering("messages", "blue")
	print("clustering trades")
	plot_clustering("trades", "green")
	
	print("attacks in-degree")
	plot_attacks_in_degree()
	print("attacks out-degree")
	plot_attacks_out_degree()
	print("attacks total degree")
	plot_attacks_total_degree()

	print("messages degrees")
	plot_degrees_datas_no_outliers("messages", "blue")
	print("trades degrees")
	plot_degrees_datas_no_outliers("trades", "green")
	print("messages under 2000")
	plot_messages_out_degree_strictly_under(2001)
	
	print("jointplot attacks")
	jointplot_degrees("attacks", "red")	
	print("jointplot messages")
	jointplot_degrees("messages", "blue")
	print("jointplot trades")
	jointplot_degrees("trades", "green")	
	'''
	print("messages vs attacks jointplot")
	custom_jointplot_degrees("messages", "out-degree", "attacks", "out-degree", "purple")
	print("messages vs trades jointplot")
	custom_jointplot_degrees("messages", "out-degree", "trades", "out-degree", "orange")