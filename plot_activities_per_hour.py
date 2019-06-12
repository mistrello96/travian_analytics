import matplotlib.pyplot as plt
import pandas as pd



if __name__ == "__main__":
	df = pd.read_csv("Results/Activity/activity_per_hour.csv")
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(df["hour"], df["total"], '-o', color = "black")
	plt.xlim(left = -0.2, right = 23.3)
	plt.xticks(range(0, 25), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Hour", fontsize = 15)
	plt.ylabel("Number of activities", fontsize = 15)
	plt.title("Total number of activities performed during the observation period throughout the hours")
	plt.tight_layout()
	plt.savefig("Results/Activity/images/png/total_over_hours.png")
	plt.savefig("Results/Activity/images/pdf/total_over_hours.pdf")
	plt.close()

	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(df["hour"], df["attacks"], '-o', color = "red")
	plt.plot(df["hour"], df["messages"], '-o', color = "blue")
	plt.plot(df["hour"], df["trades"], '-o', color = "green")
	plt.xlim(left = -0.2, right = 23.3)
	plt.xticks(range(0, 25), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Hour", fontsize = 15)
	plt.ylabel("Number of activities", fontsize = 15)
	plt.title("Comparison of total number of different activities throughout the hours")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Activity/images/png/different_over_hours.png")
	plt.savefig("Results/Activity/images/pdf/different_over_hours.pdf")
	plt.close()
