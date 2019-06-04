import matplotlib.pyplot as plt
import pandas as pd

# color mapping: red = attack, mesages = blue, trade = green

def plot_zero_percentage():
	file_name_trades = "Results/Community_density_reciprocity/Trades/trades_zeroes_percentage.csv"
	file_name_messages = "Results/Community_density_reciprocity/Messages/messages_zeroes_percentage.csv"
	df_trades = pd.read_csv(file_name_trades)
	df_messages = pd.read_csv(file_name_messages)
	plt.figure(figsize = (8, 6), dpi = 300)
	plt.plot(df_trades["day"], [x * 100 for x in df_trades["zero_percentage"]], color = "green", label = "Trades")
	plt.plot(df_messages["day"], [x * 100 for x in df_messages["zero_percentage"]], color = "blue", label = "Messages")
	plt.xlim(0.8, 30.5)
	plt.xticks(range(1, 31), fontsize = 12)
	plt.yticks(fontsize = 12)
	plt.xlabel("Day", fontsize = 15)
	plt.ylabel("Percentage", fontsize = 15)
	plt.title("Percentage of relevant alliances with density equals to zero")
	plt.legend()
	plt.tight_layout()
	plt.savefig("Results/Community_density_reciprocity/images/png/density_zero_per.png")
	plt.savefig("Results/Community_density_reciprocity/images/pdf/density_zero_per.pdf")
	plt.close()


if __name__ == "__main__":
	plot_zero_percentage()