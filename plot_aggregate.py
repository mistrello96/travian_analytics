import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("Results/Aggregate/attacks_clustering_coefficient.csv")

plt.figure(1, figsize = (8, 6), dpi = 300)
plt.yscale("log")
(ds, bins, _) = plt.hist(df["clustering_coefficient"], bins = "fd", color = "red") # fd is the same binning strategy used by seaborn

plt.figure(2, figsize = (8, 6), dpi = 300)
plt.yscale("log")
sns.distplot(df["clustering_coefficient"], kde = False)
(ds, bins, _) = plt.hist(df["clustering_coefficient"], bins = "fd", color = "red") # fd is the same binning strategy used by seaborn
for i in range(len(bins) - 1):
	m = (bins[i] + bins[i + 1]) / 2
	plt.scatter(m, ds[i], marker = 'x', color = "black")
plt.xlim([10 ** (-10), max(df["clustering_coefficient"]) + 5 * 10 ** (-5)])
plt.tight_layout()
plt.savefig("Results/Aggregate/images/clustering_distribution/attacks.png")
plt.savefig("Results/Aggregate/images/clustering_distribution/attacks.pdf")

