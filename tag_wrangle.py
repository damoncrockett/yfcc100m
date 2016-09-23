import pandas as pd
import glob
import os

DIR = "/data/damoncrockett/flickr_data/raw/concepts/"

counter = -1

for file in glob.glob(os.path.join(DIR,"*.csv")):
    counter+=1
    concept = os.path.splitext(os.path.basename(file))[0]
    df = pd.read_csv(file)
    conf_list = []
    n = len(df)
    
    for i in range(n):
        tmp = df.tags.loc[i].split(",")
        try:
            conf = float([item.split(":")[1] for item in tmp if item.split(":")[0]==concept][0])
            conf_list.append(conf)
        except:
            conf_list.append("variant")
    
    df[concept] = conf_list
    df.to_csv(file,index=False)
    print counter,file  
        