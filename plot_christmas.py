import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
	df_days = pd.read_csv("Results/Activity/activity_per_hour.csv")
	df_christmas = pd.read_csv("Results/Christmas/day25_activity_per_hour.csv")

	plt.figure(figsize = (8, 6), dpi = 300)

	plt.plot(df_days["hour"], [x / 30 for x in df_days["attacks"]], '-o', color = "darkred", label = "attacks average")
	plt.plot(df_days["hour"], [x / 30 for x in df_days["messages"]], '-o', color = "darkblue", label = "messages average")
	plt.plot(df_days["hour"], [x / 30 for x in df_days["trades"]], '-o', color = "darkgreen", label = "trades average")

	plt.plot(df_christmas["hour"], df_christmas["attacks"], '--o', color = "red", label = "attacks on Christmas")
	plt.plot(df_christmas["hour"], df_christmas["messages"], '--o', color = "blue", label = "messages on Christmas")
	plt.plot(df_christmas["hour"], df_christmas["trades"], '--o', color = "green", label = "trades on Christmas")

	plt.xlim(left = -0.2, right = 23.3)
	plt.xticks(range(0, 25), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Hour", fontsize = 15)
	plt.ylabel("Number of activities", fontsize = 15)
	plt.title("Comparison between the average activity per hour and the activities on Christmas")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Christmas/images/png/christmas.png")
	plt.savefig("Results/Christmas/images/pdf/christmas.pdf")
	plt.close()

	plt.figure(figsize = (8, 6), dpi = 300)

	plt.plot(df_days["hour"], [x / 30 for x in df_days["total"]], '-o', color = "black", label = "total activities average")

	plt.plot(df_christmas["hour"], df_christmas["total"], '--o', color = "black", label = "total activities on Christmas")

	plt.xlim(left = -0.2, right = 23.3)
	plt.xticks(range(0, 25), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Hour", fontsize = 15)
	plt.ylabel("Number of activities", fontsize = 15)
	plt.title("Comparison between the average total activity per hour and the total activity on Christmas")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Christmas/images/png/christmas_total.png")
	plt.savefig("Results/Christmas/images/pdf/christmas_total.pdf")
	plt.close()