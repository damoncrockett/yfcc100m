from numpy import repeat as rep
import sys

feature = sys.argv[1]
ext = sys.argv[2]
TARGET = "/data/damoncrockett/flickr_data/raw/"+feature+"/"

DIR = "http://multimedia-commons.s3-us-west-2.amazonaws.com/features/image/"
PREFIX = DIR+feature+"/"

l = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
n = len(l)
m = n * n

l1 = list(rep(l,m))
l2 = list(rep(l,n)) * n
l3 = l * m

hexes = []
for i in range(len(l1)):
    hexes.append(l1[i]+l2[i]+l3[i])
    
urls = [PREFIX+hex+"."+ext for hex in hexes]

import requests
import shutil
import os

for url in urls:
    path = TARGET+os.path.basename(url)
    print path

    try:
        r = requests.get(url,stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        print e

