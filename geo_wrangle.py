import os
import pandas as pd
import glob
import sys

outfile = sys.argv[1]

input_path = '/data/damoncrockett/flickr_data/raw/'

counter=-1
for file in glob.glob(os.path.join(input_path,'*.csv')):
    counter +=1
    df = pd.read_csv(file)
    
    # pick your region as a bounding box
    box = [-117.306505726,-116.866998115,32.4296783572,33.1303436061]

    df = df[df.lat.notnull()]
    df = df[df.lon>box[0]]
    df = df[df.lon<box[1]]
    df = df[df.lat>box[2]]
    df = df[df.lat<box[3]]
    print counter
    if counter==0:
        tmp = df
    else:
        tmp = tmp.append(df)

tmp.to_csv('/data/damoncrockett/flickr_data/'+outfile,index=False)
