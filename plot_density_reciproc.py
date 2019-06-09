import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# color mapping: red = attack, mesages = blue, trade = green

def plot_mean_std_density_reciprocity(edge_type, color):
	file_name = "Results/Community_density_reciprocity/{}/{}_community_density_reciprocity{}.csv"
	density_mean = []
	density_std = []
	reciprocity_mean = []
	reciprocity_std = []
	for i in range(1, 31):
		df = pd.read_csv(file_name.format(edge_type, edge_type, i))
		most_relevant_communities = ["alliance43", "alliance103", "alliance38", "alliance44"]
		df = df[df["alliance_name"].isin(most_relevant_communities)]
		density_mean.append(np.mean(df["density"]))
		density_std.append(np.std(df["density"]))
		reciprocity_mean.append(np.mean(df["reciprocity"]))
		reciprocity_std.append(np.std(df["reciprocity"]))
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), density_mean, linestyle = '-', 
		linewidth = 2.5, color = 'black', label = "Average", antialiased = True)
	plt.plot(range(1, 31), [m - s for m, s in zip(density_mean, density_std)],
			 color = color, linewidth = 0.2, antialiased = True)
	plt.plot(range(1, 31), [m + s for m, s in zip(density_mean, density_std)],
			 color = color, linestyle = '-', linewidth = 0.2, antialiased = True)
	plt.fill_between(range(1, 31), 
					 [m - s for m, s in zip(density_mean, density_std)],
					 [m + s for m, s in zip(density_mean, density_std)],
					 color = color, alpha = 0.5)
	plt.xlim(1, 30)
	plt.xlabel("Days", fontsize = 15)
	plt.ylabel("Density", fontsize = 15)
	plt.tick_params(labelsize = 12)
	plt.legend()
	plt.title("Average density over time")
	plt.savefig("Results/Community_density_reciprocity/images/png/{}_density.png".format(edge_type))
	plt.savefig("Results/Community_density_reciprocity/images/pdf/{}_density.pdf".format(edge_type))
	plt.close()

	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), reciprocity_mean, linestyle = '-', 
		linewidth = 2.5, color = 'black', label = "Average", antialiased = True)
	plt.plot(range(1, 31), [m - s for m, s in zip(reciprocity_mean, reciprocity_std)],
			 color = color, linewidth = 0.2, antialiased = True)
	plt.plot(range(1, 31), [m + s for m, s in zip(reciprocity_mean, reciprocity_std)],
			 color = color, linestyle = '-', linewidth = 0.2, antialiased = True)
	plt.fill_between(range(1, 31), 
					 [m - s for m, s in zip(reciprocity_mean, reciprocity_std)],
					 [m + s for m, s in zip(reciprocity_mean, reciprocity_std)],
					 color = color, alpha = 0.5)
	plt.xlim(1, 30)
	plt.xlabel("Days", fontsize = 15)
	plt.ylabel("Reciprocity", fontsize = 15)
	plt.tick_params(labelsize = 12)
	plt.legend()
	plt.title("Average reciprocity over time")
	plt.savefig("Results/Community_density_reciprocity/images/png/{}_reciprocity.png".format(edge_type))
	plt.savefig("Results/Community_density_reciprocity/images/pdf/{}_reciprocity.pdf".format(edge_type))
	plt.close()

def plot_mean_vs_mean():
	file_name_messages = "Results/Community_density_reciprocity/messages/messages_community_density_reciprocity{}.csv"
	file_name_trades = "Results/Community_density_reciprocity/trades/trades_community_density_reciprocity{}.csv"
	density_means = {"messages": [], "trades": []}
	density_stds = {"messages": [], "trades": []}
	reciprocity_means = {"messages": [], "trades": []}
	reciprocity_stds = {"messages": [], "trades": []}
	for i in range(1, 31):
		df_messages = pd.read_csv(file_name_messages.format(i))
		df_trades = pd.read_csv(file_name_trades.format(i))
		
		density_means["messages"].append(np.mean(df_messages["density"]))
		density_stds["messages"].append(np.std(df_messages["density"]))
		density_means["trades"].append(np.mean(df_trades["density"]))
		density_stds["trades"].append(np.std(df_trades["density"]))

		reciprocity_means["messages"].append(np.mean(df_messages["reciprocity"]))
		reciprocity_stds["messages"].append(np.std(df_messages["reciprocity"]))	
		reciprocity_means["trades"].append(np.mean(df_trades["reciprocity"]))
		reciprocity_stds["trades"].append(np.std(df_trades["reciprocity"]))	

	# density
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), density_means["messages"], color = "blue", label = "Messages")
	plt.plot(range(1, 31), density_means["trades"], color = "green", label = "Trades")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Average", fontsize = 15)
	plt.title("Density of messages' average vs density of trades' average")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Community_density_reciprocity/images/png/msg_vs_trades_density.png")
	plt.savefig("Results/Community_density_reciprocity/images/pdf/msg_vs_trades_density.pdf")
	plt.close()

	df_most = pd.read_csv("Results/Most_relevant_community_analysis/messages/messages_most_relevant_community_density_reciprocity.csv")
	# most relevant community analysis - density
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), density_means["messages"], color = "blue", label = "Average of all relevant alliances")
	plt.plot(df_most["day"], df_most["density"], '--', color = "black", label = "Most releval community")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Density", fontsize = 15)
	plt.title("Density of messages' average vs density of most relevant community")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Community_density_reciprocity/images/png/msg_vs_most_density.png")
	plt.savefig("Results/Community_density_reciprocity/images/pdf/msg_vs_most_density.pdf")
	plt.close()

	# reciprocity
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), reciprocity_means["messages"], color = "blue", label = "Messages")
	plt.plot(range(1, 31), reciprocity_means["trades"], color = "green", label = "Trades")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Average", fontsize = 15)
	plt.title("Reciprocity of messages' average vs reciprocity of trades' average")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Community_density_reciprocity/images/png/msg_vs_trades_reciprocity.png")
	plt.savefig("Results/Community_density_reciprocity/images/pdf/msg_vs_trades_reciprocity.pdf")

	# most relevant community analysis - reciprocity
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), reciprocity_means["messages"], color = "blue", label = "Average of all relevant alliances")
	plt.plot(df_most["day"], df_most["reciprocity"], '--', color = "black", label = "Most releval community")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Reciprocity", fontsize = 15)
	plt.title("Reciprocity of messages' average vs reciprocity of most relevant community")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Community_density_reciprocity/images/png/msg_vs_most_reciprocity.png")
	plt.savefig("Results/Community_density_reciprocity/images/pdf/msg_vs_most_reciprocity.pdf")
	plt.close()

	# trades - most relevant community
	df_most = pd.read_csv("Results/Most_relevant_community_analysis/trades/trades_most_relevant_community_density_reciprocity.csv")
	# most relevant community analysis - density
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), density_means["trades"], color = "green", label = "Average of all relevant alliances")
	plt.plot(df_most["day"], df_most["density"], '--', color = "black", label = "Most releval community")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Density", fontsize = 15)
	plt.title("Density of trades' average vs density of most relevant community")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Community_density_reciprocity/images/png/trades_vs_most_density.png")
	plt.savefig("Results/Community_density_reciprocity/images/pdf/trades_vs_most_density.pdf")
	plt.close()

	# most relevant community analysis - reciprocity
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(range(1, 31), reciprocity_means["trades"], color = "green", label = "Average of all relevant alliances")
	plt.plot(df_most["day"], df_most["reciprocity"], '--', color = "black", label = "Most releval community")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Reciprocity", fontsize = 15)
	plt.title("Reciprocity of trades' average vs reciprocity of most relevant community")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Community_density_reciprocity/images/png/trades_vs_most_reciprocity.png")
	plt.savefig("Results/Community_density_reciprocity/images/pdf/trades_vs_most_reciprocity.pdf")
	plt.close()


if __name__ == "__main__":
	print("print messages density and reciprocity over time")
	plot_mean_std_density_reciprocity("messages", "blue")
	print("print trades density and reciprocity over time")
	plot_mean_std_density_reciprocity("trades", "green")
	print("print mean vs mean")
	plot_mean_vs_mean()