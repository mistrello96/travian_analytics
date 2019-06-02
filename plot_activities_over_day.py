import matplotlib.pyplot as plt
import pandas as pd

# color mapping: red = attack, mesages = blue, trade = green

if __name__ == "__main__":
	# players each day
	df = pd.read_csv("Results/Activity/nodes_activity.csv")
	plt.figure(figsize = (8, 6), dpi = 300)
	sunday = 6.5
	while sunday < 30:
		plt.axvline(x = sunday, color = "red", alpha = 0.7)
		sunday += 7
	plt.plot(df["day"], df["nnodes"], '-o', color = "black")
	plt.ylim(2000, 4000)
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Number", fontsize = 15)
	plt.title("Number of players for each day")
	plt.tight_layout()
	plt.savefig("Results/Activity/images/png/player_each_day.png")
	plt.savefig("Results/Activity/images/pdf/player_each_day.pdf")
	plt.close()

	df_attacks = pd.read_csv("Results/Activity/attacks_activity.csv")
	df_messages = pd.read_csv("Results/Activity/messages_activity.csv")
	df_trades = pd.read_csv("Results/Activity/trades_activity.csv")
	total_activities = [a + m + t for a, m, t in zip(df_attacks["edges"], df_messages["edges"], df_trades["edges"])]

	# number of activity each day: an activity is a trade, a single message or an attack
	plt.figure(figsize = (8, 6), dpi = 300)
	sunday = 6.5
	while sunday < 30:
		plt.axvline(x = sunday, color = "red", alpha = 0.7)
		sunday += 7
	plt.plot(df_attacks["day"], total_activities, '-o', color = "black")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Number", fontsize = 15)
	plt.title("Total activities for each day")
	plt.tight_layout()
	plt.savefig("Results/Activity/images/png/total_activities_each_day.png")
	plt.savefig("Results/Activity/images/pdf/total_activities_each_day.pdf")
	plt.close()

	# n_players vs n_activities
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.yscale("log")
	sunday = 6.5
	while sunday < 30:
		plt.axvline(x = sunday, color = "red", alpha = 0.7)
		sunday += 7
	plt.plot(df["day"], df["nnodes"], '-o', color = "purple", label = "Number of players")
	plt.plot(df_attacks["day"], total_activities, '-o', color = "orange", label = "Number of activities")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Number", fontsize = 15)
	plt.title("Players vs activities for each day")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Activity/images/png/players_vs_activities_each_day.png")
	plt.savefig("Results/Activity/images/pdf/players_vs_activities_each_day.pdf")
	plt.close()

	# attacks vs messages vs trades over time
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(df_attacks["day"], df_attacks["edges"], '-o', color = "red", label = "Number of attacks")
	plt.plot(df_messages["day"], df_messages["edges"], '-o', color = "blue", label = "Number of messages")
	plt.plot(df_trades["day"], df_trades["edges"], '-o', color = "green", label = "Number of trades")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Number", fontsize = 15)
	plt.title("Number of the activities for each day")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Activity/images/png/n_each_activity_each_day.png")
	plt.savefig("Results/Activity/images/pdf/n_each_activity_each_day.pdf")
	plt.close()

	# players doing attacks vs messages vs trades over time
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(df_attacks["day"], df_attacks["nodes"], '-o', color = "red", label = "Number of player attacking")
	plt.plot(df_messages["day"], df_messages["nodes"], '-o', color = "blue", label = "Number of player messaging")
	plt.plot(df_trades["day"], df_trades["nodes"], '-o', color = "green", label = "Number of player trading")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Number", fontsize = 15)
	plt.title("Number of the players performing an actvity for each day")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Activity/images/png/player_each_activity_each_day.png")
	plt.savefig("Results/Activity/images/pdf/player_each_activity_each_day.pdf")
	plt.close()