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
		df = pd.read_csv(file_name.format(edge_type[0].upper() + edge_type[1:], edge_type, i))
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
	plt.savefig("Results/Community_density_reciprocity/{}/images/png/density.png".format(edge_type[0].upper() + edge_type[1:]))
	plt.savefig("Results/Community_density_reciprocity/{}/images/pdf/density.pdf".format(edge_type[0].upper() + edge_type[1:]))
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
	plt.savefig("Results/Community_density_reciprocity/{}/images/png/reciprocity.png".format(edge_type[0].upper() + edge_type[1:]))
	plt.savefig("Results/Community_density_reciprocity/{}/images/pdf/reciprocity.pdf".format(edge_type[0].upper() + edge_type[1:]))
	plt.close()

if __name__ == "__main__":
	print("print messages density and reciprocity over time")
	plot_mean_std_density_reciprocity("messages", "blue")
	print("print trades density and reciprocity over time")
	plot_mean_std_density_reciprocity("trades", "green")