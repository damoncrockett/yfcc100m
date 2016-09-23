d = read.csv("year_counts.csv")
t = d[c(1:15),]
library(ggplot2)
tmp = t[order(t$index),]
ggplot(tmp,aes(index,X0)) + geom_bar(stat='identity')
