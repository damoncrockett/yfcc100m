import pandas as pd
print "reading data..."
l = pd.read_table("./raw/yfcc100m_autotags-v1",sep="\t",header=None)
print "...done."
print "renaming columns..."
columns = {0:"id",1:"tags"}
l.rename(columns=columns,inplace=True)
print "...done."
print "making list..."
l = list(l.tags.str.split(","))
print "...done."
print "unnesting list..."
l = [item for sublist in l for item in sublist]
print "...done"
print "...selecting words"
l = [item.split(":")[0] for item in l]
print "...done."
print "running Counter..."
from collections import Counter
c = Counter(l)
l = []
print "...done"
print "saving results..."
c = pd.DataFrame(c.items())
c.to_csv("./concepts.csv",index=False)
print "...done."
