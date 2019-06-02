import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
	df = pd.read_csv("Results/Community_over_time/community_distribution.csv")
	_, axes = plt.subplots(nrows = 3, ncols = 1, sharex = True, figsize = (8, 6), dpi = 300)
	plt.subplots_adjust(left = 0.1, right = 0.97, hspace = 0.25)
	plt.suptitle("Evolution of number of communities over the days", fontsize = 20)
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 14)
	
	sunday = 6.5
	while sunday < 30:
		axes[0].axvline(x = sunday, color = "red", alpha = 0.7)
		axes[1].axvline(x = sunday, color = "red", alpha = 0.7)
		axes[2].axvline(x = sunday, color = "red", alpha = 0.7)
		sunday += 7

	axes[0].plot(range(1, 31), df["number_of_registerd_community"], '-o', color = "black")
	axes[0].set_title("Number of alliances", fontsize = 15)	
	axes[0].set_ylabel("Number", fontsize = 14)
	axes[0].set_ylim(min(df["number_of_registerd_community"]) - 5, max(df["number_of_registerd_community"]) + 5)
	
	axes[1].plot(range(1, 31), df[" number_of_relevant_community"], '-o', color = "black")
	axes[1].set_title("Number of relevant alliances", fontsize = 15)
	axes[1].set_ylabel("Number", fontsize = 14)
	axes[1].set_ylim(min(df[" number_of_relevant_community"]) - 5, max(df[" number_of_relevant_community"]) + 5)
	
	percentage = [(r / t) * 100 for r, t in zip(df[" number_of_relevant_community"], df["number_of_registerd_community"])]
	axes[2].plot(range(1, 31), percentage, '-o', color = "black")
	axes[2].set_title("Relevant alliances over total", fontsize = 15)
	axes[2].set_ylabel("Percentage", fontsize = 14)
	axes[2].set_ylim(min(percentage) - 3, max(percentage) + 3)
	
	plt.savefig("Results/Community_over_time/images/png/alliances_each_day.png")
	plt.savefig("Results/Community_over_time/images/pdf/alliances_each_day.pdf")
	plt.close()