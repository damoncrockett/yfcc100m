import pandas as pd

DIR = "/data/damoncrockett/flickr_data/"
DATA = DIR + "raw/id-url/all_static_tags.csv"

print "reading data...",
df = pd.read_csv(DATA)
print "done."

d = pd.read_csv(DIR+"concepts.csv")
concept_list = list(d['0'])

counter = -1
for concept in concept_list:
    counter+=1
    tmp = df[df.tags.str.contains(concept)]
    tmp.reset_index(drop=True,inplace=True)
    tmp.to_csv(DIR+"raw/concepts/"+concept+".csv",index=False)
    print counter, concept