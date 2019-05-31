library(MASS)
mydata = read.csv("/home/mistrello96/Projects/travian_analytics/Results/Aggregate/trades_degree.csv")
fitted = fitdistr(mydata[ , 4], "normal")
fitted